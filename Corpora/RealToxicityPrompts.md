# RealToxicityPrompts

RealToxicityPrompts attests `[prompt, continuation]` web-text trajectories, challenging-prompt flags, and Perspective API toxicity and harm-subtype risk scores (`[0, 1]`) under lineage `Perspective API`, feeding the `RISK` and `consensus` planes (`BELIEF ≠ RISK ≠ ACTION`).

The source is AllenAI's RealToxicityPrompts corpus ([dataset card](https://huggingface.co/datasets/allenai/real-toxicity-prompts)): 100k web sentence snippets split into a `prompt` prefix and a `continuation` suffix, accompanied by Perspective API toxicity and subtype probabilities. One recipe reads `prompts.jsonl`.

## Source

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `real-toxicity-prompts` | `RealToxicityPrompts` source trunk, lineage `Perspective API` | class `AIModelProbe` | `unicode`, `iso-639` | `prompts.jsonl` | [`prompts.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/real-toxicity-prompts/prompts.recipe) |

Because the scores come from an automated classifier ("The scores accompanying the prompt and the continuation are generated using the Perspective API"), the witness carries lineage `Perspective API` and trust class `AIModelProbe` ([6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes), [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it)), ensuring copies or sister datasets sharing that classifier lineage do not multiply independent votes ([30. Conflicts](../Sequence/Conflicts.md) C4).

## The prompts

Each line is one JSON object. `filename`, `begin`, and `end` address the OpenWebText file and byte/character offsets from which the sentence was sliced; they are source-local pointers resolved at ingest (`key record filename`, `key record begin`, `key record end`) and recorded nowhere. Each record composes the ordered trajectory `[prompt.text, continuation.text]`, while `prompt` and `continuation` each stand as canonical UTF-8 text entities (`thing prompt text`, `thing continuation text`).

Under the Recording Law ([INVENTOR_RECORD](../Repositories/Laplace/docs/INVENTOR_RECORD.md)), the eight Perspective API probabilities in `[0, 1]` (`toxicity`, `severe_toxicity`, `profanity`, `sexually_explicit`, `identity_attack`, `flirtation`, `threat`, `insult`) supply **scored harm/risk attestations** on `prompt.text` and `continuation.text` feeding the `RISK` and `consensus` planes—never uncalibrated `WIN` string literals and never inert floats left unattested in the row.

| Piece | Written as | Laplace reads it as | Target attestation & current recipe state | Specification |
| --- | --- | --- | --- | --- |
| `filename`, `begin`, `end` | `"0766186-bc7f….txt"`, `340`, `564` | OpenWebText document pointer and slice offsets (`key`), recorded nowhere | none | OpenWebText extraction coordinates (Gehman et al. 2020) |
| `[prompt.text, continuation.text]` | two `text` strings | ordered `[prompt, continuation]` instance trajectory (`thing record prompt/text continuation/text`) | subject of `challenging` | "Each instance represents a prompt and its metadata" |
| `challenging` | `true` or `false` | indicator of prompts that consistently trigger toxic continuations across models | `[[prompt, continuation], consistently cause all models to generate toxicity, true/false]` | Gehman et al. (2020), §"Prompts That Challenge All Models" |
| `prompt`, `continuation` | objects holding `text` and Perspective attribute floats | canonical UTF-8 text entities | subjects of their respective risk scores | prefix and suffix split of the web sentence |
| `toxicity`, `severe_toxicity`, `profanity`, `sexually_explicit`, `identity_attack`, `flirtation`, `threat`, `insult` | floats in `[0, 1]`, or `null` | scored Perspective harm/risk probabilities on `prompt.text` or `continuation.text` | target: scored risk claims on `prompt.text` and `continuation.text` (`LP_OUTCOME_SCORE` in `[0, 1]`) feeding `RISK` / `consensus` (`Batch 2` recipe gap: `prompts.recipe` currently keeps these floats in the record without emitting scored risk claims) | Gehman et al. (2020) Table 13; [Perspective annotation scheme](https://github.com/conversationai/conversationai.github.io/blob/master/crowdsourcing_annotation_schemes/toxicity_with_subattributes.md) |
| `null` | `null` | absent measurement | none | |

## Relations

`prompts.recipe` already strips `filename`, `begin`, and `end`, composes `[prompt, continuation]`, and maps `challenging` to Gehman et al. (2020)'s semantic definition rather than the raw JSON key. In `Batch 2`, `prompts.recipe` binds the eight Perspective attributes to their Table 13 semantic risk definitions and emits each `[0, 1]` probability as a scored `RISK` attestation (`class AIModelProbe`, lineage `Perspective API`).
