# FrameNet

FrameNet attests what its XML says of each frame, frame element, lexical unit, semantic type, corpus, document and sentence, each the thing its name is, and the release's numbers for them are FrameNet's internal pointers, resolved to what they name and recorded nowhere; the README, book and schemas attest nothing.

One source reads Berkeley FrameNet Release 1.7 (<https://framenet.icsi.berkeley.edu/>): frames with their frame elements and lexical units, frame-to-frame inheritance and subframe relations, semantic types, and annotated sentences across lexical-unit subcorpora and full-text documents, read by [`framenet.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/framenet/framenet.recipe).

## Source

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `framenet` | `FrameNet` source trunk | class `AcademicCurated` | `unicode`, `iso-639` | `*.xml` under `framenet_v17` | [`framenet.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/framenet/framenet.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior bounds the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## Highway types, sentence-aligned layers & empirical POS counts

FrameNet's highway nodes are content-addressed identifiers (`fnframe`: 1,218 frames such as `Abandonment`; `fnfe`: 11,428 frame-scoped elements `[Abandonment, Agent]`; `fnlu`: 13,572 frame-scoped lexical units `[Abandonment, abandon.v]`; [Types](../Reference/Types.md)). Release-local integer IDs (`ID="2031"`, `feID`, `luID`, `frameID`, `corpID`, `docID`, `sentNo`, `lemmaID`) are internal pointers resolved at ingest (`type FE.ID fnfe`, `type luID fnlu`, ...) and recorded nowhere. Author initials (`cBy`) are participant content inside FrameNet's records under the single `FrameNet` witness trunk (`Batch 2` closes `own cBy` per-author witness splitting), and entry timestamps (`cDate`) are packaging metadata (`omit`).

Two Recording Law invariants govern `<sentence>` and `<annotationSet>` layers (*FrameNet II*):

1. **Sentence-aligned annotation layer trajectories ([Types: Layers](../Reference/Types.md#layers)):** Each `<annotationSet>` annotates a specific `<sentence>` for an evoked `frame` and `lexUnit` (`Target`), laying `FE` (frame element), `GF` (grammatical function), `PT` (phrase type), `NER`, and null-instantiation (`DNI`, `CNI`, `INI`) spans in order along that sentence's trajectory. Per-span roles (`[Abandonment, Theme]`, `Head`, `NP`) belong strictly to **that sentence's aligned annotation layer**, never floated globally as unconditional claims on bare words (`[her car, FE, Theme]` or `[dog, GF, Head]`).
2. **Empirical token POS counts preserved via tagset crosswalks:** FrameNet's `PENN` (Penn Treebank `ptb` tagset) and `BNC` (CLAWS C5 tagset) layers tag sentence spans with fine-grained part-of-speech labels (`nns`, `NN1`, `VVZ`) that crosswalk onto `upos` (`NOUN`, `VERB`, ...) via `manifest/slots/edges-tagsets.tsv` (`upos` bank: `5` bits at offset `8`). Those empirical token POS occurrences—alongside aligned sentence POS layer trajectories—supply genuine corpus frequency evidence weighted under FrameNet's witness series, **never** discarded as "packaging".

| Piece | Written as | Laplace reads it as | Target attestation & current recipe state | Specification |
| --- | --- | --- | --- | --- |
| `<frame name="Abandonment" ID="2031">` | frame XML root | `fnframe` highway node `Abandonment`; `ID` resolved and unrecorded (`cDate` omitted) | `[Abandonment, definition, text]` | *FrameNet II* |
| `<FE ID="12338" name="Agent" coreType="Core">` | inside `<frame>` | `fnfe` highway node `[Abandonment, Agent]` | `[[Abandonment, Agent], coreType, Core]`, `definition`, `requiresFE` / `excludesFE` | Frame Elements (*FrameNet II*) |
| `<lexUnit ID="14839" name="abandon.v" POS="V">` | inside `<frame>` or LU XML root | `fnlu` highway node `[Abandonment, abandon.v]`, POS crosswalked to `upos`, `valenceUnit` triples (`[FE, GF, PT]`) composed together | `[Abandonment, [Abandonment, abandon.v]]`, valence patterns, `semType` | Lexical Units (*FrameNet II*) |
| `<frameRelation type="Inherits from">` & `<FERelation>` | in frame files & `frRelation.xml` | frame-to-frame and FE-to-FE inheritance, subframe, causative, and perspective relations (`supID`/`subID` resolved to `fnfe`) | `[Abandonment, Inherits from, Intentionally_affect]`, FE-to-FE alignment strands | `frameRelations.xsd` |
| `<corpus>`, `<document>`, `<sentence><text>…</text>` | in `fulltext/` and `lu/` XMLs | document hierarchy and canonical UTF-8 sentence trajectory | sentence trajectory holding aligned `<annotationSet>` layers | `fullText.xsd`, `sentence.xsd` |
| `<annotationSet>` with `Target`, `FE`, `GF`, `PT`, `Other`, `Sent`, `Verb`/`Noun`/`Adj` layers | `<label start="…" end="…" name="…" feID="…"/>` & `itype="DNI"` | span-aligned semantic/syntactic layer trajectories tied to the evoked `fnframe`/`fnlu` (`feID` resolved to `[frame, FE]`, attribute name `feID` recorded nowhere) | sentence-aligned `FE`/`GF`/`PT`/`Target` layer trajectories (`Batch 2` upgrades `framenet.recipe` from flat span-under-layer-name claims `[span, FE, Theme]` to aligned layer trajectories) | *FrameNet II* valence constellations |
| `PENN` & `BNC` POS `<layer>`s | `<label start="…" end="…" name="nns"/>` / `NN1` | PTB (`ptb`) and CLAWS C5 tagset tokens crosswalked to `upos`, preserving empirical token POS counts + sentence POS layer trajectory | `[token, ptb/claws_tag]` → `upos` empirical series + sentence POS layer (`Batch 2` replaces `[token, PENN, nns]` markup-name triples) | PTB & BNC POS tagsets |

## Relations

`framenet.recipe` already resolves numeric `ID`, `feID`, `luID`, and `frameID` pointers onto `fnframe`, `fnfe`, and `fnlu` highway nodes and preserves frame-to-frame relation names (`Inherits from`, `Uses`, `Subframe of`). Closing the `Batch 2` recipe items composes sentence-aligned `Target`/`FE`/`GF`/`PT` and POS layers, routes `PENN`/`BNC` tags through `type ... upos crosswalk` while preserving empirical token POS counts, consolidates `cBy` as participant content under the single `FrameNet` trunk, and fixes `fnfe`→`fnframe` parent resolution in `laplace highway`.
