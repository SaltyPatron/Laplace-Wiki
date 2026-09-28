# Laplace-Wiki

This repository is the Laplace documentation. It explains how everything at every level works.

Before any Laplace work, read `README.md` and every page it lists, in full.

Every documentation page in this repository is listed in `README.md`. Add a page to that list when the page is created.

`Spitball.md` holds text that has not been properly considered for the documentation as a whole. Settled documentation is every other page.

Pages under `Research/` hold sourced research and measured results that support the specification. They cite their sources, mark what was measured, and are not specification.

Add specification text only from words the inventor supplies. A missing section stays missing until those words exist. Pages are not imported from any other tree. Status updates and reports are not pages.

## Page format

A page is a Markdown file. Its first line is `# Title`. Its first paragraph is one summary sentence. The page's `README.md` entry is `- [Title](Page.md) — summary.`, with the same title and the same summary sentence.

The `README.md` page list is the page tree, from the highest level down. A nested entry, indented two spaces per level, is a child of the entry above it. A page with children is the `README.md` of a folder, and its children live in that folder:

```markdown
- [Section](Section/README.md) — summary.
  - [Child](Section/Child.md) — summary.
```

On the site the tree becomes the navigation: top-level pages are tabs, every page shows its path, and a section page lists its children.

Links between pages are relative Markdown links, such as `[Spitball](Spitball.md)` or `[Spitball](Spitball.md#heading)`.

## Writing

These render both on github.com and on the site:

- Diagrams: a fenced code block labelled `mermaid`.
- Callouts: `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`.
- Math: `$...$` inline and `$$...$$` on its own lines.
- Footnotes: `[^1]` in the text and `[^1]: ...` at the end of the page.
- Collapsible sections: `<details><summary>Title</summary>` ... `</details>`.

Images and other files a page uses go in `assets/`, linked relatively, such as `![Diagram](assets/diagram.png)`.

## Checks

`python3 tools/check_wiki.py` checks the page catalog, the page format, and every relative link. `npx markdownlint-cli2` checks Markdown style against `.markdownlint-cli2.jsonc`. Both run before every commit through `.githooks/pre-commit`, enabled once per clone with `git config core.hooksPath .githooks`. Both run again on every push and pull request, along with a site build. Links to other sites are checked weekly, and a broken one opens an issue.

## Site

Every push to `main` publishes the pages to <https://saltypatron.github.io/Laplace-Wiki/> with search, navigation, and a "Linked from" list on each page. The navigation follows the order of the `README.md` page catalog. `mkdocs.yml` configures the site and `tools/site_hooks.py` builds it from the pages; the pages themselves are not changed.

Preview locally:

```sh
python3 -m venv .venv && .venv/bin/pip install -r tools/requirements.txt
python3 tools/site.py serve
```
