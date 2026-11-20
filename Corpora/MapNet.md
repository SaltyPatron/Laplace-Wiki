# MapNet

MapNet attests interchange mappings joining FrameNet frames and `[frame, lu]` lexical units (`fnframe`, `fnlu`) to WordNet synsets across `mapping_lus_synsets.txt` and `mapping_frame_synsets.txt`, resolving WordNet 1.6 offsets through the WordNet 1.6→3.0→`ILI` crosswalk onto `ILI` highway nodes.

MapNet v0.1 ("FrameNet 1.3 frames and lexical units mapped to WordNet 1.6 synsets", Tonelli & Pianta) bridges FrameNet and WordNet/MultiWordNet. It is an interchange source under [Hops](Hops.md), read by two recipes under one `MAPNET v.0.1` witness trunk.

## Source

| Source | Witness | Trust class | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `mapnet` | `MAPNET v.0.1` source trunk | class `AcademicCurated` | `unicode`, `iso-639`, `framenet`, `cili` | `mapping_lus_synsets.txt`, `mapping_frame_synsets.txt` under `MapNet-0.1` | [`lus-synsets.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/mapnet/lus-synsets.recipe), [`frame-synsets.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/mapnet/frame-synsets.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares. The publisher's README notes an evaluated mapping precision of `0.794` over automatic alignment, which informs witness/edge calibration without inventing per-row scores where the file states none.

## Target highway resolution vs. current recipes

A WordNet 1.6 offset (`a#00057580`, `n#05593650`) is an edition-local byte offset in WordNet 1.6 (`pos#offset`). Under the Recording Law ([30. Conflicts](../Sequence/Conflicts.md) S1, I5), edition byte offsets are internal pointers: `highway.bin` resolves WordNet 1.6 `(pos, offset)` pairs through the published WordNet 1.6 → WordNet 3.0 → CILI crosswalk (e.g., UPC/MCR WordNet version mappings) directly onto canonical `ILI` highway nodes (`i46360`), while composing FrameNet lexical units as `[frame, lu]` (`fnlu`, e.g., `[Abounding_with, bejewelled.a]`) so every MapNet row forms a clean `[fnframe, fnlu, ILI]` or `[fnframe, ILI]` interchange strand and contributes `fnlu`↔`ili` and `fnframe`↔`ili` edges to `highway.bin`.

`Batch 2` recipe gap: `lus-synsets.recipe` and `frame-synsets.recipe` already read both files and type `frames` onto `fnframe`, but retain the raw `a#00057580` string as `content synsets` until the WN 1.6 → `ILI` alias table is wired into `highway` and `lus` is composed as `[frames, lus]` (`fnlu`).

| File & Piece | Written as | Laplace reads it as | Target attestation & current recipe state | Specification |
| --- | --- | --- | --- | --- |
| `mapping_lus_synsets.txt` col 1 (`frames`) | `Abounding_with` | FrameNet frame highway node (`type frames fnframe node`) | first element of the interchange strand | "`mapping_lus_synsets.txt`: mapping between FrameNet frames, lus and WordNet synsets (5,162 mappings)" |
| `mapping_lus_synsets.txt` col 2 (`lus`) | `bejewelled.a` | FrameNet lexical unit `[Abounding_with, bejewelled.a]` (`fnlu`) | `[fnframe, fnlu, ILI]` interchange strand + `fnlu`→`ili` highway edge (`Batch 2` gap: compose `[frames, lus]` onto `fnlu`) | FrameNet v1.3 lexical unit |
| `mapping_lus_synsets.txt` col 3 (`synsets`) | `a#00057580` | WordNet 1.6 `(pos, offset)` pointer resolved via WN 1.6→3.0→`ILI` crosswalk to `ILI`, recorded nowhere | `ILI` highway node (`Batch 2` gap: currently retained as raw `a#00057580` content until WN 1.6 crosswalk lands in `highway`) | "All synsets refer to WordNet version 1.6, compatible with MultiWordNet" |
| `mapping_frame_synsets.txt` cols 1–2 (`frames`, `synsets`) | `Abounding_with`, `a#00057580` | FrameNet `fnframe` paired with `ILI` resolved from the WN 1.6 offset | `[fnframe, ILI]` interchange strand + `fnframe`→`ili` highway edge (`Batch 2` gap: `frame-synsets.recipe` currently pairs `fnframe` with raw `synsets` text) | frame-to-synset mappings |
| empty field | | attests nothing | none | |

## Relations

Both MapNet tables express cross-lexicon equivalence/evocation interchanges rather than field-name predicates (`pair` / interchange strands). Wiring the WordNet 1.6 → `ILI` alias map into `Laplace-Native/manifest/` and `laplace highway` in `Batch 2` puts all of MapNet directly onto the linguistic superhighway.
