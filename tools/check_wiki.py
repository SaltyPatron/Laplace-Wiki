#!/usr/bin/env python3
"""Check the Laplace-Wiki page catalog and links.

Rules enforced:
  1. Every page is listed in the README.md "## Pages" section, and every
     listed page exists.
  2. Every README entry's summary matches the page's summary line (the first
     paragraph after the page's title), ignoring the case of the first letter.
  3. Every page has exactly one H1, on its first line.
  4. Every relative link in every Markdown file resolves to a file, and every
     #anchor resolves to a heading in the target file.

Run from anywhere: python3 tools/check_wiki.py
Exits non-zero and prints each problem when a rule is broken.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Markdown files that are repository mechanics, not documentation pages.
NOT_PAGES = {"README.md", "AGENTS.md", "CLAUDE.md"}
SKIP_DIRS = {".git", ".github", "tools", "node_modules"}

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
ENTRY_RE = re.compile(r"^- \[([^\]]+)\]\(([^)]+)\) — (.+)$")
FENCE_RE = re.compile(r"^(```|~~~)")


def markdown_files():
    for path in sorted(ROOT.rglob("*.md")):
        rel = path.relative_to(ROOT)
        if not any(part in SKIP_DIRS for part in rel.parts):
            yield rel


def strip_code(text):
    """Drop fenced code blocks and inline code so links inside them are ignored."""
    lines, in_fence = [], False
    for line in text.splitlines():
        if FENCE_RE.match(line.strip()):
            in_fence = not in_fence
            lines.append("")
            continue
        lines.append("" if in_fence else re.sub(r"`[^`]*`", "", line))
    return lines


def slugify(heading):
    """GitHub's heading anchor algorithm."""
    slug = heading.strip().lower()
    slug = re.sub(r"[^\w\- ]", "", slug)
    return slug.replace(" ", "-")


def anchors(path):
    seen, result = {}, set()
    for line in strip_code(path.read_text(encoding="utf-8")):
        m = re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", line)
        if not m:
            continue
        base = slugify(m.group(1))
        n = seen.get(base, 0)
        seen[base] = n + 1
        result.add(base if n == 0 else f"{base}-{n}")
    return result


def summary_line(lines):
    """First paragraph after the H1, joined into one line."""
    para = []
    for line in lines[1:]:
        if line.strip():
            if line.startswith("#"):
                break
            para.append(line.strip())
        elif para:
            break
    return " ".join(para)


def same_summary(a, b):
    return a[:1].lower() == b[:1].lower() and a[1:] == b[1:]


def main():
    errors = []
    pages = [p for p in markdown_files() if p.name not in NOT_PAGES or p.parent != Path(".")]

    # Rule 1 and 2: the README catalog.
    readme = (ROOT / "README.md").read_text(encoding="utf-8").splitlines()
    in_pages, catalog = False, {}
    for n, line in enumerate(readme, 1):
        if line.startswith("## "):
            in_pages = line.strip() == "## Pages"
            continue
        if in_pages and line.startswith("- "):
            m = ENTRY_RE.match(line)
            if not m:
                errors.append(f"README.md:{n}: entry is not '- [Title](Page.md) — summary.'")
                continue
            catalog[Path(m.group(2))] = (n, m.group(1), m.group(3))

    for page in pages:
        if page not in catalog:
            errors.append(f"{page}: page is not listed in README.md ## Pages")

    for target, (n, title, summary) in catalog.items():
        path = ROOT / target
        if not path.is_file():
            errors.append(f"README.md:{n}: listed page {target} does not exist")
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        if lines and lines[0] != f"# {title}":
            errors.append(f"README.md:{n}: title '{title}' does not match {target} H1 '{lines[0]}'")
        page_summary = summary_line(lines)
        if not same_summary(summary, page_summary):
            errors.append(
                f"README.md:{n}: summary does not match {target}\n"
                f"    README: {summary}\n"
                f"    page:   {page_summary}"
            )

    # Rule 3: one H1, on the first line.
    for page in pages:
        lines = strip_code((ROOT / page).read_text(encoding="utf-8"))
        h1s = [i for i, line in enumerate(lines, 1) if re.match(r"^#\s", line)]
        if not lines or not lines[0].startswith("# "):
            errors.append(f"{page}:1: first line must be the page's '# Title'")
        if len(h1s) > 1:
            errors.append(f"{page}:{h1s[1]}: page has more than one H1")

    # Rule 4: links resolve.
    anchor_cache = {}
    for md in markdown_files():
        for n, line in enumerate(strip_code((ROOT / md).read_text(encoding="utf-8")), 1):
            for m in list(LINK_RE.finditer(line)) + list(IMAGE_RE.finditer(line)):
                href = m.group(1)
                if re.match(r"^[a-z][a-z0-9+.-]*:", href, re.I):
                    continue  # external: http, https, mailto, ...
                file_part, _, anchor = href.partition("#")
                target = (ROOT / md.parent / file_part).resolve() if file_part else ROOT / md
                if not target.exists():
                    errors.append(f"{md}:{n}: broken link {href}")
                    continue
                if anchor and target.suffix == ".md":
                    if target not in anchor_cache:
                        anchor_cache[target] = anchors(target)
                    if anchor.lower() not in anchor_cache[target]:
                        errors.append(f"{md}:{n}: no heading for anchor #{anchor} in {file_part or md}")

    for e in errors:
        print(e)
    if errors:
        print(f"\n{len(errors)} problem(s).")
        return 1
    print(f"OK: {len(pages)} page(s), catalog and links consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
