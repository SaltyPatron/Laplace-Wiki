# Laplace-Wiki

This repository is the Laplace documentation. It explains how everything at every level works.

Before any Laplace work, read `README.md` and every page it lists, in full.

Every documentation page in this repository is listed in `README.md`. Add a page to that list when the page is created.

`Spitball.md` holds text that has not been properly considered for the documentation as a whole. Settled documentation is every other page.

Add text only from words the inventor supplies. A missing section stays missing until those words exist. Pages are not imported from any other tree. Status updates and reports are not pages.

## Page format

A page is a Markdown file. Its first line is `# Title`. Its first paragraph is one summary sentence. The page's `README.md` entry is `- [Title](Page.md) — summary.`, with the same title and the same summary sentence.

Links between pages are relative Markdown links, such as `[Spitball](Spitball.md)` or `[Spitball](Spitball.md#heading)`.

## Checks

`python3 tools/check_wiki.py` checks the page catalog, the page format, and every relative link. Run it before every commit. The same check runs on every push and pull request.
