# Measuring Hate Speech

Measuring Hate Speech attests continuous Rasch hate-speech risk measures, ten ordinal harm survey judgments, targeted identity groups, and annotator demographics on social media comments under one corpus trunk, feeding the `RISK` and `consensus` planes.

The source is UC Berkeley D-Lab's Measuring Hate Speech corpus ([dataset card](https://huggingface.co/datasets/ucberkeley-dlab/measuring-hate-speech/raw/main/README.md)): 39,565 social media comments annotated across 135,556 rows by 7,912 annotators. Parquet is the publisher's primary distribution format and is slated for direct native columnar decoding in the Engine; [`annotations.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/measuring-hate-speech/annotations.recipe) currently reads the extracted `train-*.tsv` split (excluding duplicate subsets such as `measuring-hate-speech.tsv` so rows are never double-counted).

## Source

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `measuring-hate-speech` | `Measuring Hate Speech` source trunk | class `AcademicCurated` | `unicode`, `iso-639` | Parquet release (`*.parquet`) in target native decode; currently `train-*.tsv` | [`annotations.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/measuring-hate-speech/annotations.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior bounds the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## The annotations

A row is one annotator's reading of one comment. The comment is its decoded UTF-8 `text`; `comment_id` is the corpus's internal pointer to it, resolved at ingest and recorded nowhere (`key row comment_id`). `annotator_id` is participant content inside the corpus's records, never a separate witness (`content annotator_id`, `attest ... with annotator_id`), so `Measuring Hate Speech` is the sole witness trunk ([30. Conflicts](../Sequence/Conflicts.md) I3). An empty field or `\N` attests nothing.

Under the Recording Law ([INVENTOR_RECORD](../Repositories/Laplace/docs/INVENTOR_RECORD.md)), `hate_speech_score` and the ten ordinal harm survey items (`sentiment`, `respect`, `insult`, `humiliate`, `status`, `dehumanize`, `violence`, `genocide`, `attack_defend`, `hatespeech`) supply **scored negative/harm/risk attestations** feeding the `RISK` and `consensus` planes (`BELIEF ≠ RISK ≠ ACTION`), never blind `WIN` string literals and never inert row floats.

| Piece | Laplace reads it as | Target attestation & current recipe state | Specification |
| --- | --- | --- | --- |
| `comment_id` | internal pointer to the comment (`key row comment_id`), recorded nowhere | none | "unique ID for each comment" |
| `annotator_id` | participant content identifying the rater on their judgments and demographics | participant qualifier (`with annotator_id`) and demographic subject (`of annotator_id`) | "unique ID for each annotator" |
| `text` | the subject: the comment, as decoded UTF-8 text | canonical comment entity | "lightly processed text of a social media post" |
| `platform` | source platform of the comment | `[comment, Social media comments were collected from, value]` | Kennedy et al. (2020): YouTube, Reddit, and Twitter |
| `hate_speech_score` | continuous Rasch hate-speech risk measure on the comment | target: scored hate-speech risk attestation on `comment` feeding the `RISK` / `consensus` plane (`Batch 2` recipe gap: `annotations.recipe` currently keeps the float in the row without a scored risk claim) | "continuous hate speech measure" |
| `sentiment`, `respect`, `insult`, `humiliate`, `status`, `dehumanize`, `violence`, `genocide`, `attack_defend`, `hatespeech` | ordinal harm/risk judgments by `annotator_id` on `comment` | target: scored harm/risk attestations per survey dimension qualified by `annotator_id` (`Batch 2` recipe gap: currently held as unattested row content) | "ordinal label that is combined into the continuous score" (Sachdeva et al. 2022, Table 1) |
| `target_race`, `target_race_asian`, and all `target_*` columns (8 groups and 42 subgroups, including `target_politics*`) | boolean target-group checklist answers by `annotator_id` on `comment` | `[comment, directed at or about individuals: …, true/false]` qualified `with annotator_id` | Sachdeva et al. (2022), §4.3–4.4 and Appendix B |
| `annotator_severity`, `annotator_infitms`, `annotator_outfitms` | Rasch rater-bias and fit diagnostics on `annotator_id`, usable to weight rater reliability | target: rater-calibration observations on `annotator_id` (`Batch 2` recipe gap: currently held in the row) | "annotator's estimated survey interpretation bias"; Rasch infit/outfit mean-square diagnostics |
| `infitms`, `outfitms`, `hypothesis`, `std_err` | item fit, stratification prior, and measurement uncertainty on `comment` | comment-level Rasch diagnostics (`std_err` remains an explicit documentation obligation where unassigned) | Kennedy et al. (2020) §4.2; Sachdeva et al. (2022) |
| `annotator_gender*`, `annotator_trans*`, `annotator_cisgender`, `annotator_educ*`, `annotator_income*`, `annotator_ideology*`, `annotator_age`, `annotator_race_*`, `annotator_religion_*`, `annotator_sexuality_*` | self-reported demographics attested of `annotator_id` | `[annotator, self-reported …, value]` (`attest row … of annotator_id`) | 6 annotator demographic groups and 40 subgroups (Sachdeva et al. 2022) |

## Relations

`annotations.recipe` maps `platform`, all `target_*` group columns, and all `annotator_*` demographic columns onto explicit semantic relations from Kennedy et al. (2020) and Sachdeva et al. (2022) rather than raw column headers, with `Measuring Hate Speech` as the sole witness trunk. Closing the remaining `Batch 2` gap maps `hate_speech_score` and the ten ordinal harm scales (`insult`, `humiliate`, `dehumanize`, `violence`, `genocide`, `hatespeech`, etc.) onto normalized `[0, 1]` risk scores feeding the `RISK` and `consensus` planes, modulated by Rasch fit/severity diagnostics.
