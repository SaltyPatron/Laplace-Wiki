# SemLink

SemLink attests what its three mapping files say of each key, a PropBank roleset or a VerbNet class and verb, as the path from the key to every value under it, and its annotated instances, role mappings, and README attest nothing.

One source reads SemLink 2, "the mappings between PropBank, VerbNet and FrameNet". The three files it reads are JSON, read as what they say: "Every key of the file is a thing (a PropBank roleset, a VerbNet class and verb), and what is written under it is said of it: the path from the key to each value." The README says the release is "designed to handle the latest versions of each of its linked resources: VerbNet 3.3, the Unified PropBank frame files, and FrameNet 1.7", and that "we don't include direct links from PB to FN, but they can be retrieved through VN". SemLink is a hop between lexicons, as [Hops](Hops.md) lists it, not a lexicon of its own.

## Source

| Source | Witness | Uncertainty | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `semlink` | `SemLink` | deviation 90 | `propbank`, `verbnet` | `pb-vn2.json`, `vn-fn2.json`, `external_vn2pb.json` | [`mappings.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/semlink/mappings.recipe) |

The uncertainty is the deviation the witness's attestations enter at, as [Consensus](../Semantics/Consensus.md#entry) describes. The source says of its 90 that it is "this recipe's choice for a curated academic resource; the specification does not give one": the number is not settled, and [Corpora](README.md#not-settled) lists it among what stays missing. SemLink is not lineage of PropBank or VerbNet: it comes after them in [`recipes/order`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/order), and it is the one saying that this roleset maps to that class.

## The mapping files

Each file is one JSON object. Every key of it is a thing, named as written, and what its value says is one record: the path from the key through every nested key to each value, every key and value as written. An array says each of its values under the same path.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| a key of `pb-vn2.json` | `"abduct.01": { ... }` | the roleset: a thing, the subject of its record | the first part of every claim under it | "To find which VerbNet senses a roleset in PB maps to." README |
| what is under it | `"10.5": { "ARG0": "agent", "ARG1": "theme" }` | the path from the roleset through the class number and the argument to the role | `[abduct.01, 10.5, ARG0, agent]`, `[abduct.01, 10.5, ARG1, theme]` | the README calls these lists of tuples of a PropBank argument and a VerbNet thematic role; the file stores an object |
| a key of `vn-fn2.json` | `"26.5-shake": [ ... ]` | the class and verb, one key: a thing | the first part of every claim under it | "To find which FrameNet frames a particular verb sense in VN belongs to." README |
| its list | `["Moving_in_place", "Body_movement", "Cause_to_move_in_place"]` | each frame said under the same path: the pair of the key and the frame | `[26.5-shake, Moving_in_place]`, `[26.5-shake, Body_movement]`, `[26.5-shake, Cause_to_move_in_place]` | |
| a key of `external_vn2pb.json` | `"change_bodily_state-40.8.4": ["sicken.01"]` | the key as a thing, and each roleset of its list as a pair with it | `[change_bodily_state-40.8.4, sicken.01]` | the README does not describe this file |
| `null`, an empty text | | nothing | none | |

Everything under one key it says together: one record, witnessed once, and its claims within it. Nothing is renamed, reordered, or filled in: the argument is `ARG0` and the role `agent`, as the file writes them.

## Not read

No recipe matches the annotated instances under `instances` (`semlink-2`), the role mappings and supporting files under `other_resources` (`VN-FNRoleMapping.txt`, `vn-fn2.s`, `common_objects`, `1.2.2c.okay`), the tools, or `README.md`, and the source names no `reads`: none of them is read, and none attests anything.
