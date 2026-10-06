# SemLink

SemLink attests of each PropBank roleset the VerbNet classes it maps to and, of each pairing, which thematic role each argument plays, and of each VerbNet class the FrameNet frames it maps to; the same files give the highway its edges, between the identifiers PropBank, VerbNet and FrameNet write, each content as written.

SemLink 2 is "the mappings between PropBank, VerbNet and FrameNet". The README says the release is "designed to handle the latest versions of each of its linked resources: VerbNet 3.3, the Unified PropBank frame files, and FrameNet 1.7", and that "we don't include direct links from PB to FN, but they can be retrieved through VN". SemLink is a hop, as [Hops](Hops.md) lists it, not a lexicon.

## Source

| Source | Witness | Files | Read by |
| --- | --- | --- | --- |
| `semlink` | `SemLink`, class `AcademicCurated`, after `propbank` and `verbnet` | `instances/pb-vn2.json`, `instances/vn-fn2.json` | [`pb-vn.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/semlink/pb-vn.recipe), [`vn-fn.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/semlink/vn-fn.recipe); their `maps` lines feed `laplace highway` ([Types](../Reference/Types.md#perf-caches)) |

`pb-vn.recipe` makes each roleset and each class under it a thing (`type … pbroleset`, `type … vnclass`), attests the pair `[roleset, class]` and, of it, each argument's role: `[[roleset, class], ARG0, agent]`. `vn-fn.recipe` attests `[class, frame]`, the class named by the number before its dash. Each mapping is one interchange strand, where a route changes road class, never a claim per column.

## What is read

| Piece | Written as | Read as | Recorded, and on the highway |
| --- | --- | --- | --- |
| a key of `pb-vn2.json` | `"abduct.01": { ... }` | the roleset the key points at, by PropBank's own id ([PropBank](PropBank.md)) | the slot of `[abduct, kidnap]`, the roleset's lemma and name |
| the keys under it | `"10.5": { "ARG0": "agent", "ARG1": "theme" }` | the VerbNet class the number names: the class whose ID ends in it, `abduct-10.5` ([VerbNet](VerbNet.md)) | `[abduct.01's roleset, abduct-10.5]`; an edge `pbroleset`→`vnclass` |
| the argument-to-role object | `{ "ARG0": "agent" }` | of the pair, the role the argument plays | `[[roleset, class], ARG0, agent]` |
| a key of `vn-fn2.json` | `"26.5-shake": [ ... ]` | the class the number before the dash names | |
| its list | `["Moving_in_place", "Body_movement"]` | the frames, by name ([FrameNet](FrameNet.md)) | `[class, frame]`; edges `vnclass`→`fnframe` |
| `external_vn2pb.json` | `"change_bodily_state-40.8.4": ["sicken.01"]` | not taken | nothing |

## Not read

The annotated instances under `instances`, the role mappings and supporting files under `other_resources`, the tools, and `README.md` are read by nothing.
