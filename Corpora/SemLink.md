# SemLink

SemLink's three mapping files are the highway's input: every key in them is a PropBank roleset id, a VerbNet class number or a FrameNet frame name, and what they say is that this roleset is that class and that class is that frame. No recipe reads them, and no claim holds a SemLink key.

SemLink 2 is "the mappings between PropBank, VerbNet and FrameNet". The README says the release is "designed to handle the latest versions of each of its linked resources: VerbNet 3.3, the Unified PropBank frame files, and FrameNet 1.7", and that "we don't include direct links from PB to FN, but they can be retrieved through VN". SemLink is a hop, as [Hops](Hops.md) lists it, not a lexicon.

## Source

| Source | Witness | Files | Read by |
| --- | --- | --- | --- |
| `semlink` | `SemLink` | `instances/pb-vn2.json`, `instances/vn-fn2.json` | `laplace highway` ([Types](../Reference/Types.md#perf-caches)) |

The source directory holds a `source` file and no recipe. `laplace ingest semlink` has nothing to read.

## What the highway takes

| Piece | Written as | Read as | On the highway |
| --- | --- | --- | --- |
| a key of `pb-vn2.json` | `"abduct.01": { ... }` | the roleset the key points at, by PropBank's own id ([PropBank](PropBank.md)) | the slot of `[abduct, kidnap]`, the roleset's lemma and name |
| the keys under it | `"10.5": { "ARG0": "agent", "ARG1": "theme" }` | the VerbNet class the number names: the class whose ID ends in it, `abduct-10.5` ([VerbNet](VerbNet.md)) | an edge `pbroleset`→`vnclass` |
| the argument-to-role object | `{ "ARG0": "agent" }` | not taken: a role mapping, which the highway does not yet carry | nothing |
| a key of `vn-fn2.json` | `"26.5-shake": [ ... ]` | the class the number before the dash names | |
| its list | `["Moving_in_place", "Body_movement"]` | the frames, by name ([FrameNet](FrameNet.md)) | edges `vnclass`→`fnframe` |
| `external_vn2pb.json` | `"change_bodily_state-40.8.4": ["sicken.01"]` | not taken | nothing |

The highway counted 7,527 SemLink edges when it was last generated ([Research](../Research/README.md) holds the measurements).

## Not read

The annotated instances under `instances`, the role mappings and supporting files under `other_resources`, the tools, and `README.md` are read by nothing.
