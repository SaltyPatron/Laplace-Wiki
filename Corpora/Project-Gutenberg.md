# Project Gutenberg

Project Gutenberg's books are plain text, observed as content, and attest nothing.

The source is books from [Project Gutenberg](https://www.gutenberg.org/), as plain text. It has no recipe of its own: its source file says the files are ordinary content, read as `text`, and observed, as [Attestations](../Semantics/Attestations.md#observations) says of ordinary content.

## Source

| Source | Witness | Trust | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `project-gutenberg` | none: observed content has no witness | none | `unicode` | `*.txt` and `*.md` under the root, read as text | [`source`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/project-gutenberg/source), `reads text` |

## The text

| Piece | Laplace reads it as | Claim recorded |
| --- | --- | --- |
| the whole file, the book and the Project Gutenberg header and footer around it | plain text: UAX #29 codepoints, graphemes, word segments, sentences, paragraphs, and the file | none |
| the header's lines, such as the title, the author, and the language | text like the rest: nothing in the header is read as a statement of the book | none |
| a file under the root that is not `*.txt` or `*.md` | not read | none |
