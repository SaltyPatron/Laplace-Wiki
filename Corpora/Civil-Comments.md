# Civil Comments

Civil Comments attests the seven numbers Jigsaw gave each comment, as built under their own names, as numbers and not as scores, and the identity columns of other releases are not in these files.

The source names itself by its dataset card's title, Dataset Card for "civil_comments": comments from the Civil Comments platform with the labels Jigsaw added. Its data is Parquet, read as it is written out beside it as a table (`extracted/`, by `parquet-to-text.py`), the first row the columns' own names, every value as the file holds it. One recipe reads the three splits.

## Source

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `civil-comments` | `civil_comments` | class `AcademicCuratedWithUserInput` | `unicode`, `iso-639` | `train-*.tsv`, `validation-*.tsv`, `test-*.tsv`; not `*.parquet` | [`comments.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/civil-comments/comments.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior is the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## The comments

The table is tab-separated, and a `\` makes the character after it itself: a tab, a line's end, or `\`. A field written `\N` alone is left as written, what the source leaves unknown. An empty field attests nothing.

The card, "Data Fields", names the columns: `text`, `toxicity`, `severe_toxicity`, `obscene`, `threat`, `insult`, `identity_attack`, `sexual_explicit`. It says nothing of what a number stands for, so each is recorded as the number the set gives the comment under that name, and is not taken for a score: the recipe names no score, and a claim's outcome is a win. A comment has no name of its own in the set: it is the text it is. What a row says it says together: one record, witnessed once by `civil_comments`, and its claims within it.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| `text` | the subject: the comment, as the text it is | | "text" |
| `toxicity` | said of the comment, the number as written | `[comment, toxicity, value]` | "A value between 0 and 1 indicating the fraction of annotators that assigned the attribute to the comment text" [TensorFlow Datasets, civil_comments](https://www.tensorflow.org/datasets/catalog/civil_comments) |
| `severe_toxicity`, `obscene`, `threat`, `insult`, `identity_attack`, `sexual_explicit` | said of the comment, the number as written | `[comment, insult, value]` | the same, for each attribute |
| `asian`, `female`, `male`, `white`, and the other identity columns; `rating` | not read: not columns of these files | none | TensorFlow Datasets says the identity tags exist only for a fraction of examples and are included on `CivilCommentsIdentities`, and the civility labels only in the raw data |

Nothing else is attested. The Parquet files are not the source. The card is not read: no recipe of the source matches it, and the source does not read text (`reads`), so nothing of it is recorded.

## Relations

As built, the relation of every claim above is the column's name, `[comment, toxicity, value]`, `[comment, insult, value]`: markup, not meaning. A relation is what the source means, never the name of a field, column, attribute, or layer, [10. Recipes](../Sequence/Recipes.md#1011-disposition-every-recovered-field). The target for each column is what the source documents it to mean, quoted in the Specification column; a column whose meaning the source does not document is an explicit unresolved obligation, its target the meaning the source documents. each is "the fraction of annotators that assigned the attribute to the comment text", a number the set states, an observation.
