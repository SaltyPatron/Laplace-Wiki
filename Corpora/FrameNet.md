# FrameNet

FrameNet attests what its XML says of each frame, frame element, lexical unit, semantic type, corpus, document and sentence, each the thing its name is, and the release's numbers for them are FrameNet's internal pointers, resolved to what they name and recorded nowhere; the README, book and schemas attest nothing.

One source reads FrameNet: Release 1.7 of the Berkeley FrameNet data, in the form NLTK redistributes, "frames with their frame elements and lexical units, the relations between frames, the semantic types, the lemma and lexeme tables, and the annotated sentences of the lexical units and of the full texts". Every file is XML, read as what it says by [`framenet.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/framenet/framenet.recipe). The project's site is <https://framenet.icsi.berkeley.edu/>.

## Source

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `framenet` | `FrameNet` | class `AcademicCurated` | `unicode`, `iso-639` | `*.xml` under `framenet_v17` | [`framenet.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/framenet/framenet.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior is the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## The things

FrameNet's things are what it names them. A frame is its name (`Abandonment`); a frame element is its frame and its name (`[Abandonment, Agent]`); a lexical unit its frame and its name (`[Abandonment, abandon.v]`). These are the types the highway lists from FrameNet's own indexes (`fnframe` 1,218, `fnfe` 11,428, `fnlu` 13,572; [Types](../Reference/Types.md)), so an element that carries only FrameNet's number for one (`<FE ID="12338">`, `<lexUnit ID="14839">`, `feID`, `luID`, `frameID`) is read as the type that number points at (`type FE.ID fnfe`, `type luID fnlu`, …). The frames, frame elements and lexical units are highway IDs by their names, content that other sources cite too. The numbers themselves, with the ids of sentences, annotation sets, corpora and documents (`ID`, `id`, `corpID`, `docID`, `lemmaID`), are FrameNet's internal pointers into its own release: resolved to what they name and recorded nowhere. Who made an entry (`cBy`) is bookkeeping, read by nothing.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `<frame name="Abandonment" ID="2031" ...>` | the root of a frame file | the frame, by its name; its other attributes said of it; its `ID` a pointer, recorded nowhere | `[Abandonment, cDate, …]`, `[Abandonment, definition, text]` | "A semantic frame is a script-like conceptual structure…" *FrameNet II* |
| `<FE ID="12338" name="Agent" coreType="Core" ...>` | inside a frame | the frame element the number points at: `[Abandonment, Agent]`; its place in the frame; its attributes said of it | `[Abandonment, FE, [Abandonment, Agent]]`, `[[Abandonment, Agent], coreType, Core]`, `[[Abandonment, Agent], definition, text]` | "We call these roles frame elements (FEs)" |
| `<lexUnit ID="14839" name="abandon.v" ...>` | inside a frame, or the root of a lexical unit file | the lexical unit the number points at: `[Abandonment, abandon.v]`; its attributes said of it; `frame` and `frameName` are frame names, content | `[Abandonment, lexUnit, [Abandonment, abandon.v]]`, `[[Topic, on.prep], POS, PREP]`, `[[Topic, on.prep], frame, Topic]` | "A lexical unit (LU) is a pairing of a word with a meaning." |
| `<lu ID="16601" ...>` | in the index of lexical units | the same lexical unit | | |
| `<semType name="..." ...>`, `<superType superTypeName="...">` | in the semantic types file, and inside a frame, FE or lexical unit | the semantic type by its name; its place in what it is inside | `[[Abandonment, abandon.v], semType, Intentional_act]` | *FrameNet II*; `semTypes.xsd` |
| `<memberFE ID="...">`, `<requiresFE ID="...">`, `<excludesFE ID="...">` | inside a frame or an FE | the frame element the number names, spoken of again in its place | `[[Abandonment, Agent], requiresFE, [Abandonment, Theme]]` | "a coreness set, or CoreSet" |
| `<frameRelation type="Inherits from"><relatedFrame>Name</relatedFrame>` | inside a frame | the frame's relation to the frame named, under the type as written | `[Abandonment, Inherits from, Intentionally_affect]` | "Inheritance is the strongest relation between frames" |
| `<frameRelation superFrameName="..." subFrameName="..." supID="..." subID="...>`, `<FERelation ...>` | in the frame relations file | not a thing: the names said of the relation type they are inside; `subID` and `supID` read as the frame elements they name | `[[frameRelationType, …], superFrameName, Parent]`, `[…, supID, [frame, FE]]` | `frameRelations.xsd` |
| `<corpus name="...">`, `<document name="...">` | in the full text index and a full text's header | the corpus by its name; the document by its name within its corpus | `[PropBank, document, [PropBank, BellRinging]]` | `fullText.xsd` |
| `<sentence ID="..." ...><text>…</text>` | in a lexical unit's subcorpus or a full text | the sentence is its text (`thing sentence text`); `sentNo`, `paragNo`, `aPos` said of it | `[Thus at the recent …, paragNo, 10]` | "The sentence element must contain, first, a text element" |
| `<annotationSet ID="..." ...>`, `<layer name="PENN" rank="1">` | inside a sentence | not things: what they carry is said of the sentence; `luID` and `frameName` as the lexical unit and frame they name | `[sentence, status, UNANN]`, `[sentence, name, PENN]` | `sentence.xsd` |
| `<label start="0" end="3" name="rb" feID="..."/>` | inside `<layer name="PENN">` | the stretch of the sentence's text from `start` to `end`, the end included; the label's `name` is said of that stretch under the layer's name (`span label start end text inclusive name under layer.name`), `feID` as the frame element | `[Thus, PENN, rb]`, `[her car, FE, Theme]`, `[stretch, feID, [Abandonment, Theme]]` | "Each constituent tagged with a frame element…" |
| a label without `start` and `end` | `itype="DNI"` | said of the sentence | `[sentence, itype, DNI]` | |
| `<lexeme>`, `<sentenceCount>`, `<valences>`, and any other element inside a thing | | speaks of the thing it is inside, each attribute under its name, its text under the element's name; together, one record | `[[Abandonment, abandon.v], headword, false]` | |
| `xmlns`, `xmlns:xsi`, `xsi:schemaLocation` | on roots | XML's own plumbing: nothing | nothing | |
| an empty attribute value | | nothing | nothing | |

A thing's own attributes and text are one record, witnessed once, and every thing inside it is a record of its own. Nothing is renamed, reordered, or filled in.

## Not read

`README.txt` is not read: the source has no `reads` line and no recipe of its own matches it. The book under `docs` and the schemas under `schema` match no recipe and are not read.
