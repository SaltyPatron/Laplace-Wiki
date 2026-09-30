# NLTK

The Brown Corpus in NLTK's tagged form has no recipe yet, so it is not ingested and attests nothing.

## Source

No directory under [`recipes/`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes) reads this collection, and `recipes/order` does not name it. Until a recipe exists, nothing in it is decomposed, recorded, or attested; see [Attestations](../Semantics/Attestations.md#observations). The format below is the publisher's, kept so that a recipe can be written from it.

## Format

| Record | Fields in order | What a record is | Specification |
| --- | --- | --- | --- |
| tagged text | word/tag tokens separated by whitespace | One Form C file. A token is a word, a slash, and a tag, as ca01 writes it. Paragraph breaks are blank lines. The tag inventory's meanings are not in the files opened. | corpora/brown/ca01 and corpora/brown/CONTENTS |
| cats.txt line | filename, genre | One line pairing a text filename with a genre word. 500 lines, ca01 news through cr09 humor. | corpora/brown/cats.txt |
