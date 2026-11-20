# ToxiGen

ToxiGen witnesses machine-generated and human-annotated group-targeted statements under one corpus trunk, supplying scored toxicity, framing, stereotyping, lewdness, and intent risk attestations for the `RISK` and `consensus` planes while decoding serialized text cleanly to UTF-8 and never asserting toxic statements themselves as true.

The source is Microsoft's ToxiGen dataset ([dataset card](https://huggingface.co/datasets/toxigen/toxigen-data), Hartvigsen et al. 2022): 274k machine-generated toxic and benign statements across 13 minority groups, prompt sets, and human crowd annotations. Parquet and CSV are the publisher's container formats; native Parquet/CSV admission reads one canonical copy per table without external `parquet-to-text.py` staging or duplicate ingestion across format copies (the four current recipes read the extracted TSV tables pending native Parquet wiring in `Batch 2`).

## Source

| Source | Witness | Trust class | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `toxigen` | `ToxiGen` source trunk | class `AcademicCurated` | `unicode`, `iso-639` | Four tables (`train`, `prompts`, `annotated`, `annotations`) via native Parquet/CSV or extracted TSV splits (one copy per table) | [`generations.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/toxigen/generations.recipe), [`prompts.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/toxigen/prompts.recipe), [`annotated.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/toxigen/annotated.recipe), [`annotations.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/toxigen/annotations.recipe) |

As decided in [30. Conflicts](../Sequence/Conflicts.md) I9, ToxiGen is one corpus witnessing its records, just as a PGN archive witnesses its games: the generator (`ALICE` / `TopK` + prompt) and the human annotators (`HashedWorkerId`) are participants recorded inside each record, never separate witnesses, and ToxiGen never asserts a generated statement itself as true. Under the Recording Law ([INVENTOR_RECORD](../Repositories/Laplace/docs/INVENTOR_RECORD.md)), its toxicity labels, RoBERTa probabilities, and `1..5` human harm/intent/stereotyping ratings supply **scored negative/harm/risk attestations** feeding the `RISK` and `consensus` planes (`BELIEF ≠ RISK ≠ ACTION`).

## The generations (`train`)

Each row pairs a machine-generated statement (`generation`) with the `prompt` used to produce it, the `generation_method`, `roberta_prediction`, `prompt_label`, and `group`.

| Piece | Laplace reads it as | Target attestation & current recipe state | Specification |
| --- | --- | --- | --- |
| `generation` | canonical UTF-8 text of the generated statement | subject of generation provenance and RoBERTa toxicity score | "`generation` is the TOXIGEN generated text." |
| `prompt` | canonical UTF-8 text of the conditioning prompt | linked to `generation` (`[generation, the prompt used for generation, prompt]`) and subject of `prompt_label` and `group` | "`prompt` is the prompt used for generation." |
| `generation_method` | decoding method (`ALICE`, `TopK`) | attested on `generation` (`value -`) | "`generation_method` denotes whether or not ALICE was used" |
| `roberta_prediction` | classifier toxicity probability in `[0, 1]` | target: scored classifier risk attestation on `generation` (`Batch 2` gap: currently held unattested in the row) | "`roberta_prediction` is the probability predicted by our corresponding RoBERTa model" |
| `prompt_label` | binary toxicity label on `prompt` (`1` toxic, `0` benign) | target: scored harm/risk vs. benign contrast attestation on `prompt` (`Batch 2` gap: currently uncalibrated value) | "`prompt_label` is the binary value indicating whether or not the prompt is toxic (1 is toxic, 0 is benign)." |
| `group` | demographic group referenced by `prompt` | `[prompt, target group, group]` | "`group` indicates the target group of the prompt." |

## The seed prompts (`prompts`)

Files such as `hate_asian_1k` and `neutral_women_1k` hold one column (`text`), attesting the prompt set's polarity (`hate` vs. `neutral`) and target group on each prompt text.

## The aggregated human-annotated set (`annotated`)

`annotated/train` and `annotated/test` hold per-statement human-aggregated ratings (`toxicity_human`, `toxicity_ai` on `1..5` scales, `intent`, `stereotyping`, `lewd`, `framing`, `factual?`, `ingroup_effect`, `target_group`, `predicted_group`, `predicted_author`, `actual_method`). Under the Recording Law, `toxicity_human`, `toxicity_ai`, and `intent` supply **scored human harm/risk attestations** (`1..5` normalized onto `[0, 1]` on the `RISK` / `consensus` plane; `Batch 2` gap: `annotated.recipe` currently leaves numeric scales unattested in the row).

## The raw worker annotations (`annotations`)

Each row records one `HashedWorkerId`'s survey answers (`Answer.*`) on one shown statement (`Input.text`).

> [!IMPORTANT]
> **UTF-8 content identity law (`Input.text`):** In the publisher's raw `annotations` table, `Input.text` was exported through Python `str(bytes)` serialization (`b'...'` / `b"..."` with `\xNN` and `\n` escapes). At ingest, `Input.text` **must be unwrapped and decoded to clean UTF-8** before hashing so `Input.text` produces the **exact same `lp_id`** as the identical statement in `annotated` (`text`), `generations` (`generation`), and every other corpus (`same content = same hash`). Treating `b'...'` wrapper characters as literal text is forbidden (`Batch 2` recipe/decoder fix for `annotations.recipe`).

| Piece | Laplace reads it as | Target attestation & current recipe state | Specification |
| --- | --- | --- | --- |
| `Input.text` | decoded UTF-8 statement text (unwrapped from Python `b'...'` byte-repr packaging) | canonical statement entity colliding with `annotated.text` and `generations.generation` (`Batch 2` gap: `annotations.recipe` awaits `b'...'` unwrapping) | statement shown to the worker |
| `HashedWorkerId` | anonymized participant identifier (`content HashedWorkerId`) | participant qualifier (`with HashedWorkerId`) on answers and subject (`of HashedWorkerId`) of worker demographics | "all WorkerIDs were hashed to anonymize the annotators" ([TOXIGEN README](https://github.com/microsoft/TOXIGEN)) |
| `Input.prompt`, `Input.generation_method`, `Input.prompt_label`, `Input.target_group`, `Input.binary_prompt_label` | generation metadata on `Input.text` | attested under semantic relations from the card | conditioning metadata |
| `Answer.factSelect`, `Answer.framingQ`, `Answer.refTarget`, `Answer.stateFrame`, `Answer.stateGroup` | categorical framing and group-reference answers | attested on `Input.text` qualified `with HashedWorkerId` | Hartvigsen et al. (2022), Figure 6 survey items |
| `Answer.toPER.1..5`, `Answer.toAI.1..5`, `Answer.intent.1..5`, `Answer.lewd.1..3`, `Answer.stereo.1..3`, `Answer.ingroup.1..3`, `Answer.writer.1..2` | one-hot checkbox columns encoding the worker's `1..5` / `1..3` harm, intent, lewdness, and stereotyping ratings | target: collapsed to the selected scale ordinal and emitted as scored `RISK` attestations qualified `with HashedWorkerId` (`Batch 2` gap: one-hot checkbox collapse pending in `annotations.recipe`) | Figure 6 Likert checkboxes |
| `Answer.annotatorAge`, `Answer.annotatorGender`, `Answer.annotatorMinority`, `Answer.annotatorPolitics.1..5`, `Answer.annotatorRace` | self-reported worker demographics | attested `of HashedWorkerId` | worker demographic survey |

## Relations

The ToxiGen recipes already establish `ToxiGen` as the single witness trunk, keep `HashedWorkerId` as participant content, and map documented categorical fields to Hartvigsen et al. (2022)'s survey questions. Closing the `Batch 2` gaps decodes `b'...'` wrappers on `Input.text` to pure UTF-8, collapses one-hot Likert checkboxes, and emits `toxicity_human`, `toxicity_ai`, `intent`, `roberta_prediction`, and `prompt_label` as scored `RISK` attestations.
