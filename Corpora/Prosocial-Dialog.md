# ProsocialDialog

ProsocialDialog attests everything a line says of its context, the potentially unsafe utterance, as one record of the set, and a member that is null attests nothing.

The source names itself by its dataset card's title, "Dataset Card for ProsocialDialog Dataset": dialogues in which an utterance is answered by a response grounded in rules-of-thumb, with the safety labels three workers gave. One recipe reads its three splits.

## Source

| Source | Witness | Uncertainty | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `prosocial-dialog` | `ProsocialDialog` | deviation 90 | `unicode`, `iso-639` | `train.json`, `valid.json`, `test.json` | [`dialogues.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/prosocial-dialog/dialogues.recipe) |

The uncertainty is the deviation the witness's attestations enter at, as [Consensus](../Semantics/Consensus.md#entry) describes. The source says of its 90 that it is "this recipe's choice for a curated academic resource; the specification does not give one": the number is not settled, and [Corpora](README.md#not-settled) lists it among what stays missing.

## The dialogues

A JSON object on every line. The [dataset card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md): `context` is "the potentially unsafe utterance", `safety_label` "the final verdict of the context", `safety_annotations` "raw annotations from three workers". So an object is the thing its `context` names, and every other member is said of it under its own key, every key and value as written. Everything one line says it says together: one record, witnessed once by ProsocialDialog, and its claims within it. The three workers are not witnesses of their own: the card does not name them, and the set says what they answered.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `context` | a text | the subject: the utterance, as the text it is | | "the potentially unsafe utterance" |
| `response` | a text | said of the context | `[context, response, text]` | "the guiding utterance grounded on rules-of-thumb (rots)" |
| `rots` | a list of texts, or `null` | each text said of the context under `rots` | `[context, rots, text]` | "the relevant rules-of-thumb for text not labeled as __casual__" |
| `safety_label` | a text | said of the context | `[context, safety_label, __needs_caution__]` | "the final verdict of the context according to safety_annotations: __casual__, __possibly_needs_caution__, __probably_needs_caution__, __needs_caution__, __needs_intervention__" |
| `safety_annotations` | a list of three texts | each text said of the context under `safety_annotations` | `[context, safety_annotations, needs caution]` | "raw annotations from three workers: casual, needs caution, needs intervention" |
| `safety_annotation_reasons` | a list of texts | each text said of the context under `safety_annotation_reasons` | `[context, safety_annotation_reasons, text]` | "the reasons behind the safety annotations in free-form text from each worker" |
| `source` | a text | said of the context | `[context, source, socialchemistry]` | "the source of the seed text that was used to craft the first utterance of the dialogue: socialchemistry, sbic, ethics_amt, ethics_reddit" |
| `etc` | a text, or `null` | said of the context | `[context, etc, text]` | "other information" |
| `dialogue_id` | a number | said of the context, the number as written | `[context, dialogue_id, value]` | "the dialogue index" |
| `response_id` | a number | said of the context, the number as written | `[context, response_id, value]` | "the response index" |
| `episode_done` | `true` or `false` | said of the context, as written | `[context, episode_done, true]` | "an indicator of whether it is the end of the dialogue" |
| `null`, an empty text | | nothing | none | |

Nothing else is attested. The card is ordinary text, observed as [Attestations](../Semantics/Attestations.md#observations) says of ordinary content.
