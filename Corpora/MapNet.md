# MapNet

MapNet's lexical-unit file attests of each FrameNet frame the lexical units it lists for it, as written; its synset column is a WordNet 1.6 offset, a pointer into an edition no source here has, and is recorded nowhere; its frame-to-synset file holds nothing else and is not read; and the README attests nothing.

MapNet is "FrameNet 1.3 frames and lexical units mapped to WordNet 1.6 synsets". The README says "All frames and lexical units included in the resource are described in FrameNet v. 1.3." and "All synsets refer to WordNet version 1.6, compatible with MultiWordNet." It is listed under [Hops](Hops.md), but its synset offsets cannot be resolved: the highway's `ili` list knows WordNet 3.0 offsets and sense keys, not 1.6 offsets, so MapNet is not on the highway.

## Source

| Source | Witness | Trust class | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `mapnet` | `MAPNET v.0.1`, "named as the README's title names it" | class `AcademicCurated` | `unicode`, `iso-639` | `mapping_lus_synsets.txt` under `MapNet-0.1` | [`lus-synsets.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/mapnet/lus-synsets.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior is the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source. The README says of the resource: "The resource was automatically generated." and "The evaluated precision of the mapping 0.794." It gives no score to a row.

## The lexical units

`mapping_lus_synsets.txt` is a tab-separated table with no header row: "mapping between FrameNet frames, lus and WordNet synsets (5,162 mappings)". The recipe names the columns `frames`, `lus`, `synsets` to point at them.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| the first field | `Abounding_with` | the frame, as FrameNet names it: the same entity as the highway's frame and [FrameNet](FrameNet.md)'s | the subject | "- file 'mapping_lus_synsets.txt': mapping between FrameNet frames, lus and WordNet synsets" README |
| the second field | `bejewelled.a` | the lexical unit as written, said of the frame under `lus` | `[Abounding_with, lus, bejewelled.a]` | |
| the third field | `a#00057580` | a WordNet 1.6 offset: a pointer (`key synsets`), recorded nowhere | nothing | "All synsets refer to WordNet version 1.6" |
| an empty field | | what the file leaves empty | nothing | |

Each claim stands alone, witnessed once. That is as built: a row is one mapping, one interchange strand of the frame, the lexical unit and the synset, never a claim per column. How the synset is named in it while its WordNet 1.6 offset resolves to nothing is not decided.

## Not read

`mapping_frame_synsets.txt` pairs a frame with a WordNet 1.6 offset and nothing else: with the offset a pointer that resolves to nothing, a row would say nothing, so the file is not read. `README` is not read: there is no recipe for it, and the source has no `reads` line.
