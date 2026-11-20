# Civil Comments

Civil Comments attests scored toxicity and harm-subtype risk annotations (`[0, 1]` crowd-rater fractions) on platform comments under one corpus trunk, feeding the `RISK` and `consensus` planes (`BELIEF ≠ RISK ≠ ACTION`).

The source is Jigsaw's Civil Comments release (Dataset Card for `civil_comments`): user comments from the Civil Comments archive annotated by crowd raters for general toxicity and six harm subtypes under the Perspective API rating guidelines. Parquet is the publisher's native container format and is slated for direct native columnar decoding in the Engine; as an interim step, [`comments.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/civil-comments/comments.recipe) reads the three TSV splits (`train-*.tsv`, `validation-*.tsv`, `test-*.tsv`) extracted alongside the Parquet shards without duplicating rows across both encodings.

## Source

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `civil-comments` | `civil_comments` source trunk | class `AcademicCuratedWithUserInput` | `unicode`, `iso-639` | Parquet splits (`*.parquet`) in target native decode; currently `train-*.tsv`, `validation-*.tsv`, `test-*.tsv` | [`comments.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/civil-comments/comments.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior bounds the trust every attestation of the source plays at ([30. Conflicts](../Sequence/Conflicts.md) C4), and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## The comments

Each row is one comment and the seven continuous `[0, 1]` annotator-fraction scores Jigsaw measured on it: `toxicity`, `severe_toxicity`, `obscene`, `threat`, `insult`, `identity_attack`, and `sexual_explicit`. A comment has no publisher record ID in these splits; its identity is its decoded UTF-8 `text`, whose words and phrases collide through containment with every other corpus. An empty field attests nothing.

Under the Recording Law ([INVENTOR_RECORD](../Repositories/Laplace/docs/INVENTOR_RECORD.md), [20. Forward](../Sequence/Forward.md)), toxicity and harm-subtype probabilities are **scored negative/harm/risk attestations** (`LP_OUTCOME_SCORE` on `[0, 1]`) feeding the `RISK` and `consensus` planes so Laplace recognizes toxic, threatening, obscene, and identity-attacking language, scores it as harm/risk, and avoids generating it—never recording raw floats as uncalibrated `WIN` string literals.

| Piece | Laplace reads it as | Target attestation & current recipe state | Specification |
| --- | --- | --- | --- |
| `text` | the subject: the comment, as decoded UTF-8 text | canonical comment entity and sentence/word trajectory | "text" |
| `toxicity` | scored toxicity/risk attestation on the comment (`[0, 1]`) | target: `[comment, toxicity]` scored by the `[0, 1]` rater fraction on the `RISK` / `consensus` plane (`Batch 2` recipe gap: `comments.recipe` currently retains the float in the row without emitting a scored risk claim) | "A value between 0 and 1 indicating the fraction of annotators that assigned the attribute to the comment text" ([TensorFlow Datasets, `civil_comments`](https://www.tensorflow.org/datasets/catalog/civil_comments)) |
| `severe_toxicity`, `obscene`, `threat`, `insult`, `identity_attack`, `sexual_explicit` | scored harm-subtype risk attestations on the comment (`[0, 1]`) | target: scored risk claims on `comment` for each Perspective subtype (`Batch 2` recipe gap: currently retained as unattested row content) | Perspective crowd-rating subtype fractions in `[0, 1]` ([TensorFlow Datasets, `civil_comments`](https://www.tensorflow.org/datasets/catalog/civil_comments)) |
| `asian`, `female`, `male`, `white`, and other identity-mention columns | target-identity risk annotations where `CivilCommentsIdentities` splits are admitted | absent from the base `civil_comments` splits; when `CivilCommentsIdentities` is admitted, each `[0, 1]` fraction supplies a scored identity-mention observation | TensorFlow Datasets notes identity tags exist on the `CivilCommentsIdentities` subset |

## Relations

A relation is what the source means, never a raw column header ([10. Recipes](../Sequence/Recipes.md#1011-disposition-every-recovered-field)). The seven attributes follow the Perspective crowd-rating definitions cited by the Civil Comments paper (*Nuanced Metrics for Measuring Unintended Bias with Real Data for Text Classification*): general toxicity, severe toxicity, obscenity, threat of violence, insult, identity attack, and sexually explicit content. In `Batch 2`, `comments.recipe` binds each column to its semantic risk predicate and emits the rater fraction in `[0, 1]` as the attestation's score rather than leaving the numbers inert in the row or recording column-name string literals as wins.
