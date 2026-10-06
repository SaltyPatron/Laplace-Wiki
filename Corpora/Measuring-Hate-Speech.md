# Measuring Hate Speech

Measuring Hate Speech attests what each annotator said of a comment, and what the set measured of the comment and holds of the annotator, and the Parquet files and the card attest nothing.

The source names itself by its dataset card's title, "Dataset card for Measuring Hate Speech": comments, each annotated by several annotators. Its data is Parquet, read as it is written out beside it as a table (`extracted/`, by `parquet-to-text.py`), the first row the columns' own names, every value as the file holds it. One recipe reads that table.

## Source

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `measuring-hate-speech` | `Measuring Hate Speech`; as built, each annotator is also a witness of their own, `[Measuring Hate Speech, annotator_id, value]` (`own annotator_id`) | class `AcademicCurated` | `unicode`, `iso-639` | `train-*.tsv`; not `*.parquet` or `extracted/measuring-hate-speech.tsv` | [`annotations.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/measuring-hate-speech/annotations.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior is the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## The annotations

The table is tab-separated, and a `\` makes the character after it itself: a tab, a line's end, or `\`. A field written `\N` alone is left as written, what the source leaves unknown. An empty field attests nothing. The [dataset card](https://huggingface.co/datasets/ucberkeley-dlab/measuring-hate-speech/raw/main/README.md), "Key dataset columns", is quoted below.

A row is one annotator's reading of one comment. The comment is its `text`; its `comment_id` is the set's internal pointer to it, recorded nowhere (`key row comment_id`). The annotator is named as the set names them, the path `[Measuring Hate Speech, annotator_id, value]`, "comment" and "annotator" below. What the annotator answered of the comment, the ten labels and whom the comment targets, the set reports of the annotator: the annotator is content, never a witness, and that this annotator gave this comment this label is a relation of the annotator and the comment that Measuring Hate Speech attests, added to the web explicitly. As built, those claims are witnessed by the annotator, a witness of their own (`own annotator_id`); the target is the set's relation. What the set measured of the comment, and what it holds of the annotator, the set says. Each claim is its own attestation. The card does not say which of the columns it does not list belong to the comment and which to the reading: `infitms`, `outfitms`, `std_err`, and `hypothesis` are recorded of the comment, as the columns beside `hate_speech_score`.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| `comment_id` | the set's pointer to the comment: recorded nowhere | nothing | "unique ID for each comment" |
| `annotator_id` | the annotator, content: the subject of what is said of the annotator, and a part of each relation of an answer; as built, also the witness of the annotator's answers | `[Measuring Hate Speech, annotator_id, value]` | "unique ID for each annotator" |
| `text` | the subject: the comment, as the text it is | | "lightly processed text of a social media post" |
| `platform` | said of the comment, by the set | `[comment, platform, value]` | the card lists it and does not define it |
| `hate_speech_score` | said of the comment, by the set, the number as written | `[comment, hate_speech_score, value]` | "continuous hate speech measure" |
| `infitms`, `outfitms`, `std_err`, `hypothesis` | said of the comment, by the set | `[comment, std_err, value]` | the card lists them and does not assign them |
| `sentiment`, `respect`, `insult`, `humiliate`, `status`, `dehumanize`, `violence`, `genocide`, `attack_defend`, `hatespeech` | said of the comment by the annotator, which the set attests; as built, witnessed by the annotator | target `[comment, annotator, hatespeech, value]`; as built `[comment, hatespeech, value]` | "ordinal label that is combined into the continuous score" |
| `target_race`, `target_race_asian`, and every column whose name begins `target_`, including the `target_politics` columns where the file has them | said of the comment by the annotator, which the set attests; as built, witnessed by the annotator | target `[comment, annotator, target_race_asian, value]`; as built `[comment, target_race_asian, value]` | the release includes 8 target identity groups and 42 target identity subgroups |
| `annotator_severity` | said of the annotator, by the set | `[annotator, annotator_severity, value]` | "annotator's estimated survey interpretation bias" |
| `annotator_infitms`, `annotator_outfitms` | said of the annotator, by the set | `[annotator, annotator_infitms, value]` | the card lists them and does not assign them |
| `annotator_gender` and `annotator_gender_*`; `annotator_trans`, `annotator_transgender`, `annotator_transgender_prefer_not_to_say`; `annotator_educ` and `annotator_education_*`; `annotator_income` and `annotator_income_*`; `annotator_ideology` and `annotator_ideology_*`; `annotator_age`; `annotator_race_*`; `annotator_religion_*`; `annotator_sexuality_*` | said of the annotator, by the set: every column whose name so begins | `[annotator, annotator_gender, value]` | the release includes 6 annotator demographics and 40 subgroups |
| `annotator_cisgender` | said of the annotator, as every `annotator_*` column is (`attest row annotator_* of annotator_id`) | `[annotator, annotator_cisgender, value]` | |

Nothing else is attested. The Parquet files are not the source, and `extracted/measuring-hate-speech.tsv`, the same rows without the `target_politics` columns, is not either. The card is not read: no recipe of the source matches it, and the source does not read text (`reads`), so nothing of it is recorded.
