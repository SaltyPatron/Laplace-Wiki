# ProsocialDialog

ProsocialDialog attests multi-turn dialogue trajectories pairing potentially unsafe utterances with prosocial responses grounded in rules-of-thumb and scored safety/risk annotations (`casual` through `needs_intervention`) feeding the `RISK` and `consensus` planes.

The source is AllenAI's ProsocialDialog dataset ([dataset card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md)): 58k multi-turn dialogues responding to potentially unsafe, unethical, or harmful user contexts with constructive social-norm reasoning (`rots`) and three-worker safety ratings. One source trunk reads `train.json`, `valid.json`, and `test.json`.

## Source

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `prosocial-dialog` | `ProsocialDialog` source trunk | class `AcademicCurated` | `unicode`, `iso-639` | `train.json`, `valid.json`, `test.json` | [`dialogues.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/prosocial-dialog/dialogues.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior bounds the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## The dialogues

Each line is a JSON object representing one turn `response_id` inside dialogue `dialogue_id`, with `episode_done` marking the final turn of the episode.

Under the Recording Law ([INVENTOR_RECORD](../Repositories/Laplace/docs/INVENTOR_RECORD.md), [21. Sessions](../Sequence/Sessions.md)):

- **Multi-turn dialogue trajectory**: `dialogue_id` and `response_id` are internal corpus indices used at ingest (`key`/`refer`) to group and order turns `[turn_0, turn_1, ...]` into one ordered multi-turn dialogue trajectory (bounded by `episode_done`), after which the raw integer indices `dialogue_id`, `response_id`, and `episode_done` are discarded and recorded nowhere (`Batch 2` recipe gap: `dialogues.recipe` currently keys `dialogue_id` and `response_id` per line without assembling the cross-line multi-turn trajectory composition).
- **Scored safety/risk plane (`BELIEF ≠ RISK ≠ ACTION`)**: `safety_label` (`__casual__`, `__possibly_needs_caution__`, `__probably_needs_caution__`, `__needs_caution__`, `__needs_intervention__`) and the three workers' `safety_annotations` (`casual`, `needs caution`, `needs intervention`) supply **scored risk/intervention attestations** on `context` feeding the `RISK` and `consensus` planes, paired with `rots` and `response` showing constructive action under risk rather than blind refusal or unsafe compliance.

| Piece | Written as | Laplace reads it as | Target attestation & current recipe state | Specification |
| --- | --- | --- | --- | --- |
| `dialogue_id`, `response_id` | integers | internal dialogue and turn pointers (`key`): group and order `[context, response]` turns into a multi-turn dialogue trajectory, then discard raw IDs | ordered dialogue trajectory (`Batch 2` gap: `dialogues.recipe` currently emits per-turn records without cross-line dialogue composition) | "the dialogue index"; "the response index" |
| `episode_done` | `true` or `false` | dialogue boundary marker (`omit` once multi-turn trajectory ends at `true`) | none (encoded by trajectory termination) | "an indicator of whether it is the end of the dialogue" |
| `context` | string | the turn's input utterance, as decoded UTF-8 text | subject of the turn's risk assessment and prosocial response | "the potentially unsafe utterance" |
| `response` | string | constructive prosocial reply to `context` | `[context, the guiding utterance grounded on rules-of-thumb, response]` | "the guiding utterance grounded on rules-of-thumb (rots)" |
| `rots` | JSON array of strings, or `null` | rules-of-thumb grounding the response (colliding with [Social Chemistry](Social-Chemistry.md) RoTs where shared) | `[context, the relevant rules-of-thumb, rot]` for each non-empty RoT | "the relevant rules-of-thumb for text not labeled as `__casual__`" |
| `safety_label` | string | aggregated ordinal safety/risk verdict on `context` | target: scored `RISK` attestation mapping `__casual__` → `0.0` through `__needs_intervention__` → `1.0` (`Batch 2` gap: `dialogues.recipe` currently records `value - safety_label` uncalibrated) | "the final verdict of the context according to `safety_annotations`" |
| `safety_annotations` | JSON array of 3 strings | three workers' ordinal risk ratings (`casual`, `needs caution`, `needs intervention`) | target: 3-game scored `RISK` series on `context` (`Batch 2` gap: currently uncalibrated vocabulary values) | "raw annotations from three workers: casual, needs caution, needs intervention" |
| `safety_annotation_reasons` | JSON array of strings | free-text risk explanations | `[context, the reasons behind the safety annotations, reason]` | "the reasons behind the safety annotations in free-form text from each worker" |
| `source` | string | upstream seed origin (`socialchemistry`, `sbic`, `ethics_amt`, `ethics_reddit`) | `[context, the source of the seed text, value]` | "the source of the seed text that was used to craft the first utterance" |
| `etc` | string or `null` | auxiliary note when non-empty | `[context, other information, value]` | "other information" |
| `null` or `""` | empty | attests nothing | none | |

## Relations

`dialogues.recipe` already maps `response`, `rots`, `safety_annotation_reasons`, `source`, and `etc` onto the dataset card's semantic descriptions rather than JSON keys, and omits `episode_done` and raw `dialogue_id`/`response_id` strings. Closing the `Batch 2` gap composes ordered multi-turn dialogue trajectories across `dialogue_id`/`response_id` and calibrates `safety_label` and `safety_annotations` onto scored `RISK` outcomes.
