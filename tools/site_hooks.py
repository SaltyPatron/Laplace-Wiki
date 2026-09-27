"""MkDocs hooks for the Laplace-Wiki site.

The pages live at the repository root, which MkDocs cannot use as its docs_dir
because mkdocs.yml is there too. Before each build these hooks:

  - copy the pages and their files into .site-src/ (the docs_dir), writing only
    files that changed so `mkdocs serve` does not rebuild in a loop;
  - build the site navigation from the README.md page tree, in its order;
  - list each section page's child pages at its bottom;
  - add a "Linked from" list of backlinks to the bottom of each page.

The backlinks exist only on the site. The Markdown files are not changed.
"""

import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_wiki  # noqa: E402

ROOT = check_wiki.ROOT
ASSETS = ROOT / "tools" / "site_assets"
NOT_COPIED = check_wiki.NOT_PAGES - {"README.md"}

_backlinks = {}
_catalog = {}


def _sources():
    """{path in docs_dir: source file} for every file the site publishes."""
    files = {}
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if (
            path.is_file()
            and not any(part.startswith(".") or part in check_wiki.SKIP_DIRS for part in rel.parts)
            and not (rel.parent == Path(".") and (rel.name in NOT_COPIED or rel.suffix != ".md"))
        ):
            files[rel] = path
    for path in ASSETS.rglob("*"):
        if path.is_file():
            files[path.relative_to(ASSETS)] = path
    return files


def _sync(docs_dir):
    docs_dir.mkdir(parents=True, exist_ok=True)
    files = _sources()
    for rel, src in files.items():
        dest = docs_dir / rel
        if not dest.exists() or dest.read_bytes() != src.read_bytes():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dest)
    for dest in sorted(docs_dir.rglob("*"), reverse=True):
        rel = dest.relative_to(docs_dir)
        if dest.is_file() and rel not in files:
            dest.unlink()
        elif dest.is_dir() and not any(dest.iterdir()):
            dest.rmdir()


def _nav(catalog, parent):
    items = []
    for path in check_wiki.children(catalog, parent):
        kids = _nav(catalog, path)
        title = catalog[path].title
        items.append({title: [str(path), *kids]} if kids else {title: str(path)})
    return items


def on_config(config):
    config["nav"] = [{"Home": "README.md"}, *_nav(check_wiki.read_catalog(), None)]
    return config


def on_pre_build(config):
    _sync(Path(config["docs_dir"]))

    # Backlinks: which catalog pages link to each page. The README catalog is
    # left out because it links to every page.
    catalog = check_wiki.read_catalog()
    _catalog.clear()
    _catalog.update(catalog)
    _backlinks.clear()
    for source, entry in catalog.items():
        title = entry.title
        if not (ROOT / source).is_file():
            continue
        for *_, target in check_wiki.local_links(source):
            if target.suffix != ".md" or not target.is_file():
                continue
            rel = target.relative_to(ROOT)
            if rel != source:
                _backlinks.setdefault(rel, {})[source] = title


def _list(paths_titles, here):
    return "\n".join(
        f"- [{title}]({Path(os.path.relpath(path, here.parent)).as_posix()})"
        + (f" — {summary}" if summary else "")
        for path, title, summary in paths_titles
    )


def on_page_markdown(markdown, page, config, files):
    rel = Path(page.file.src_path)
    extra = []

    # A section page lists its child pages, as the README.md catalog does.
    if rel in _catalog:
        kids = check_wiki.children(_catalog, rel)
        if kids:
            rows = [(k, _catalog[k].title, _catalog[k].summary) for k in kids]
            extra.append(f"**In this section**\n\n{_list(rows, rel)}")

    sources = _backlinks.get(rel)
    if sources:
        rows = [(src, title, None) for src, title in sources.items()]
        extra.append(f"**Linked from**\n\n{_list(rows, rel)}")

    if not extra:
        return markdown
    return markdown.rstrip() + "".join(f"\n\n---\n\n{block}\n" for block in extra)
