# MapNet

MapNet attests each row of its two mapping files as the pair or the triple of the row's fields in the row's own order, under no column name because its README gives none, and the README itself attests nothing.

One source reads MapNet, "FrameNet 1.3 frames and lexical units mapped to WordNet 1.6 synsets". The README says "All frames and lexical units included in the resource are described in FrameNet v. 1.3." and "All synsets refer to WordNet version 1.6, compatible with MultiWordNet." MapNet is a hop between lexicons, as [Hops](Hops.md) lists it.

## Source

| Source | Witness | Uncertainty | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `mapnet` | `MAPNET v.0.1`, "named as the README's title names it" | deviation 90 | `unicode`, `iso-639` | `mapping_frame_synsets.txt`, `mapping_lus_synsets.txt`, `README` under `MapNet-0.1` | [`frame-synsets.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/mapnet/frame-synsets.recipe), [`lus-synsets.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/mapnet/lus-synsets.recipe), [`readme.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/mapnet/readme.recipe) |

The uncertainty is the deviation the witness's attestations enter at, as [Consensus](../Semantics/Consensus.md#entry) describes. The source says of its 90 that it is "this recipe's choice for a curated academic resource; the specification does not give one", and adds: "The README says of the resource: 'The resource was automatically generated.' and 'The evaluated precision of the mapping 0.794.' It gives no score to a row." The number is not settled, and [Corpora](README.md#not-settled) lists it among what stays missing.

## The mapping files

Both files are tab-separated tables with no header row. The README names no column and nothing that stands between the fields, so a row is recorded in the row's own order and under no name: the names after `columns` in each recipe "only point at a position in the row and are never recorded".

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| a row of `mapping_frame_synsets.txt` | `Abounding_with`, then `a#00057580` | the pair of its two fields, in the row's order | `[Abounding_with, a#00057580]` | "- file 'mapping_frame_synsets.txt': mapping between FrameNet frames and WordNet synsets (5,162 mappings)." README |
| a row of `mapping_lus_synsets.txt` | `Abounding_with`, `bejewelled.a`, then `a#00057580` | the tuple of its three fields, in the row's order | `[Abounding_with, bejewelled.a, a#00057580]` | "- file 'mapping_lus_synsets.txt': mapping between FrameNet frames, lus and WordNet synsets (5,162 mappings)." README |
| an empty field | nothing between two tabs | what the file leaves empty: attests nothing | none | |

Each row is a claim of its own, witnessed once. Nothing is renamed, reordered, or filled in: which field is the frame, the lexical unit, or the synset is not said, because the README does not say it.

## Not read

`README`, which has no extension, is read as ordinary text by its own recipe (`like text`): it is observed content, as [Attestations](../Semantics/Attestations.md#observations) describes, and attests nothing.
