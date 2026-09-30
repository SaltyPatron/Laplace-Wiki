# RealToxicityPrompts

RealToxicityPrompts attests what each instance says of its file name and what its prompt and its continuation each say of their text, as a witness whose lineage is the Perspective API, and a score is recorded as the number written, not as an outcome.

The source names itself by its dataset card's summary, RealToxicityPrompts: sentence snippets from the web, each split into a prompt and a continuation, with scores. One recipe reads its one file.

## Source

| Source | Witness | Uncertainty | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `real-toxicity-prompts` | `RealToxicityPrompts`, lineage `Perspective API` | deviation 90 | `unicode`, `iso-639` | `prompts.jsonl` | [`prompts.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/real-toxicity-prompts/prompts.recipe) |

The witness derives from the Perspective API: the source names that lineage because, as the [dataset card](https://huggingface.co/datasets/allenai/real-toxicity-prompts) says, "The scores accompanying the prompt and the continuation are generated using the Perspective API". The lineage is the source's, so every claim of the file carries it, the texts as well as the scores, and copies of one lineage play one matchup per claim as [Attestations](../Semantics/Attestations.md#witnesses) requires. The uncertainty is the deviation the witness's attestations enter at, as [Consensus](../Semantics/Consensus.md#entry) describes. The source says of its 90 that it is "this recipe's choice for a curated academic resource; the specification does not give one": the number is not settled, and [Corpora](README.md#not-settled) lists it among what stays missing.

## The prompts

A JSON object on every line: "Each instance represents a prompt and its metadata" (dataset card). The instance holds `filename` and is the thing it names; the objects under `prompt` and `continuation` each hold a `text` and are the thing it names, and their scores are said of that text under the score's own key. Everything one line says it says together: one record, witnessed once, and its claims within it. Every key and value is recorded as written; a number is the text of its digits, and no member is a score the row gives its claim.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `filename` | a text | the subject of the instance: what its name names | | the card's example holds it and does not define it |
| `begin`, `end` | a number | said of the instance, as written | `[filename, begin, value]` | the card's example holds them and does not define them |
| `challenging` | `true` or `false` | said of the instance, as written | `[filename, challenging, true]` | the card's example holds it and does not define it |
| `prompt` | an object holding `text` | a thing inside the instance: the prompt, as the text it is, and its place | `[filename, prompt, text]` | "Each instance represents a prompt and its metadata" |
| `continuation` | an object holding `text` | a thing inside the instance: the continuation, as the text it is, and its place | `[filename, continuation, text]` | the sentence was split into a prompt and a continuation |
| `toxicity`, `severe_toxicity`, `profanity`, `sexually_explicit`, `identity_attack`, `flirtation`, `threat`, `insult`, under `prompt` or `continuation` | a number | said of that text under the score's own key, the number as written | `[text, toxicity, value]` | "The scores accompanying the prompt and the continuation are generated using the Perspective API"; the attributes of the API, as the [Perspective annotation scheme](https://github.com/conversationai/conversationai.github.io/blob/master/crowdsourcing_annotation_schemes/toxicity_with_subattributes.md) and the [toxicity model card](https://github.com/conversationai/perspectiveapi/blob/main/model-cards/English/toxicity.md) describe them |
| `null` | | nothing | none | |

Nothing else is attested. The card is ordinary text, observed as [Attestations](../Semantics/Attestations.md#observations) says of ordinary content.
