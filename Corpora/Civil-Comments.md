# Civil Comments

Civil Comments attests the seven numbers Jigsaw gave each comment under their own names, as numbers and not as scores, and the identity columns of other releases are not in these files.

The source names itself by its dataset card's title, Dataset Card for "civil_comments": comments from the Civil Comments platform with the labels Jigsaw added. Its data is Parquet, read as it is written out beside it as a table (`extracted/`, by `parquet-to-text.py`), the first row the columns' own names, every value as the file holds it. One recipe reads the three splits.

## Source

| Source | Witness | Uncertainty | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `civil-comments` | `civil_comments` | deviation 90 | `unicode`, `iso-639` | `train-*.tsv`, `validation-*.tsv`, `test-*.tsv`; not `*.parquet` | [`comments.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/civil-comments/comments.recipe) |

The uncertainty is the deviation the witness's attestations enter at, as [Consensus](../Semantics/Consensus.md#entry) describes. The source says of its 90 that it is "this recipe's choice for a curated academic resource; the specification does not give one": the number is not settled, and [Corpora](README.md#not-settled) lists it among what stays missing.

## The comments

The table is tab-separated, and a `\` makes the character after it itself: a tab, a line's end, or `\`. A field written `\N` alone is left as written, what the source leaves unknown. An empty field attests nothing.

The card, "Data Fields", names the columns: `text`, `toxicity`, `severe_toxicity`, `obscene`, `threat`, `insult`, `identity_attack`, `sexual_explicit`. It says nothing of what a number stands for, so each is recorded as the number the set gives the comment under that name, and is not taken for a score: the recipe names no score, and a claim's outcome is a win. A comment has no name of its own in the set: it is the text it is. What a row says it says together: one record, witnessed once by `civil_comments`, and its claims within it.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| `text` | the subject: the comment, as the text it is | | "text" |
| `toxicity` | said of the comment, the number as written | `[comment, toxicity, value]` | "A value between 0 and 1 indicating the fraction of annotators that assigned the attribute to the comment text" [TensorFlow Datasets, civil_comments](https://www.tensorflow.org/datasets/catalog/civil_comments) |
| `severe_toxicity`, `obscene`, `threat`, `insult`, `identity_attack`, `sexual_explicit` | said of the comment, the number as written | `[comment, insult, value]` | the same, for each attribute |
| `asian`, `female`, `male`, `white`, and the other identity columns; `rating` | not read: not columns of these files | none | TensorFlow Datasets says the identity tags exist only for a fraction of examples and are included on `CivilCommentsIdentities`, and the civility labels only in the raw data |

Nothing else is attested. The Parquet files are not the source. The card is ordinary text, observed as [Attestations](../Semantics/Attestations.md#observations) says of ordinary content.
