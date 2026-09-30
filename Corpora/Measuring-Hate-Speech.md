# Measuring Hate Speech

Measuring Hate Speech attests what each annotator says of a comment as that annotator's own witness, and what the set measured of the comment and holds of the annotator, and the Parquet files and the card attest nothing.

The source names itself by its dataset card's title, "Dataset card for Measuring Hate Speech": comments, each annotated by several annotators. Its data is Parquet, read as it is written out beside it as a table (`extracted/`, by `parquet-to-text.py`), the first row the columns' own names, every value as the file holds it. One recipe reads that table.

## Source

| Source | Witness | Uncertainty | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `measuring-hate-speech` | `Measuring Hate Speech`; each annotator is a witness of their own, `[Measuring Hate Speech, annotator_id, value]` | deviation 90 | `unicode`, `iso-639` | `train-*.tsv`; not `*.parquet` or `extracted/measuring-hate-speech.tsv` | [`annotations.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/measuring-hate-speech/annotations.recipe) |

The uncertainty is the deviation the witness's attestations enter at, as [Consensus](../Semantics/Consensus.md#entry) describes. The source says of its 90 that it is "this recipe's choice for a curated academic resource; the specification does not give one": the number is not settled, and [Corpora](README.md#not-settled) lists it among what stays missing.

## The annotations

The table is tab-separated, and a `\` makes the character after it itself: a tab, a line's end, or `\`. A field written `\N` alone is left as written, what the source leaves unknown. An empty field attests nothing. The [dataset card](https://huggingface.co/datasets/ucberkeley-dlab/measuring-hate-speech/raw/main/README.md), "Key dataset columns", is quoted below.

A row is one annotator's reading of one comment. The comment is named by its `comment_id` and the annotator by their `annotator_id`; both are the set's own numberings, so the comment is the path `[Measuring Hate Speech, comment_id, value]` and the annotator the path `[Measuring Hate Speech, annotator_id, value]`, "comment" and "annotator" below. What the annotator answered of the comment, the ten labels and whom the comment targets, the annotator says, of the comment: those claims are witnessed by the annotator. What the set measured of the comment, and what it holds of the annotator, the set says. Each claim is its own ledger row. The card does not say which of the columns it does not list belong to the comment and which to the reading: `infitms`, `outfitms`, `std_err`, and `hypothesis` are recorded of the comment, as the columns beside `hate_speech_score`.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| `comment_id` | the subject of what is said of the comment | `[Measuring Hate Speech, comment_id, value]` | "unique ID for each comment" |
| `annotator_id` | the witness of the annotator's answers, and the subject of what is said of the annotator | `[Measuring Hate Speech, annotator_id, value]` | "unique ID for each annotator" |
| `text` | said of the comment, by the set | `[comment, text, text]` | "lightly processed text of a social media post" |
| `platform` | said of the comment, by the set | `[comment, platform, value]` | the card lists it and does not define it |
| `hate_speech_score` | said of the comment, by the set, the number as written | `[comment, hate_speech_score, value]` | "continuous hate speech measure" |
| `infitms`, `outfitms`, `std_err`, `hypothesis` | said of the comment, by the set | `[comment, std_err, value]` | the card lists them and does not assign them |
| `sentiment`, `respect`, `insult`, `humiliate`, `status`, `dehumanize`, `violence`, `genocide`, `attack_defend`, `hatespeech` | said of the comment, by the annotator | `[comment, hatespeech, value]` | "ordinal label that is combined into the continuous score" |
| `target_race`, `target_race_asian`, and every column whose name begins `target_`, including the `target_politics` columns where the file has them | said of the comment, by the annotator | `[comment, target_race_asian, value]` | the release includes 8 target identity groups and 42 target identity subgroups |
| `annotator_severity` | said of the annotator, by the set | `[annotator, annotator_severity, value]` | "annotator's estimated survey interpretation bias" |
| `annotator_infitms`, `annotator_outfitms` | said of the annotator, by the set | `[annotator, annotator_infitms, value]` | the card lists them and does not assign them |
| `annotator_gender` and `annotator_gender_*`; `annotator_trans`, `annotator_transgender`, `annotator_transgender_prefer_not_to_say`; `annotator_educ` and `annotator_education_*`; `annotator_income` and `annotator_income_*`; `annotator_ideology` and `annotator_ideology_*`; `annotator_age`; `annotator_race_*`; `annotator_religion_*`; `annotator_sexuality_*` | said of the annotator, by the set: every column whose name so begins | `[annotator, annotator_gender, value]` | the release includes 6 annotator demographics and 40 subgroups |
| `annotator_cisgender` | not read: no pattern of the recipe names it | none | |

Nothing else is attested. The Parquet files are not the source, and `extracted/measuring-hate-speech.tsv`, the same rows without the `target_politics` columns, is not either. The card is ordinary text, observed as [Attestations](../Semantics/Attestations.md#observations) says of ordinary content.
