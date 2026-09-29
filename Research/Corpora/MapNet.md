# MapNet

MapNet attests a generated mapping from FrameNet 1.3 to WordNet 1.6, with the precision its own README states and no score on a row.

## Files

| Path | Bytes | What the file is | Proof |
| --- | ---: | --- | --- |
| `/vault/Data/MapNet-0.1/README` | 1977 | This file. Title line `MAPNET v.0.1`. | The file |
| `/vault/Data/MapNet-0.1/mapping_frame_synsets.txt` | 124887 | "Mapping between FrameNet frames and WordNet synsets (5,162 mappings)." 5,162 lines, two tab-separated fields, no header. | `/vault/Data/MapNet-0.1/README` and the file |
| `/vault/Data/MapNet-0.1/mapping_lus_synsets.txt` | 174794 | "Mapping between FrameNet frames, lus and WordNet synsets (5,162 mappings)." 5,162 lines, three tab-separated fields, no header. | `/vault/Data/MapNet-0.1/README` and the file |
| `/vault/Data/MapNet-0.1/MapNet-0.1.zip` | 76435 | The same three files packed. See Lineage. | SHA-256 of the zip members |

## Attestations

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| Hop | A generated mapping from FrameNet 1.3 to WordNet 1.6. [Claims](../../Semantics/Claims.md#the-linguistic-super-highway) names MapNet. [Pull](../../Semantics/Pull.md#hop-and-fanout) is the pull across a hop. [Hops](Hops.md) lists the edge. | FrameNet v. 1.3 and WordNet 1.6 | The two mapping files | MAPNET v.0.1 | `/vault/Data/MapNet-0.1/README` |
| FrameNet version | "All frames and lexical units included in the resource are described in FrameNet v. 1.3." | FrameNet v. 1.3 | The frames and lexical units in the two files | MAPNET v.0.1 | `/vault/Data/MapNet-0.1/README` |
| WordNet version | "All synsets refer to WordNet version 1.6, compatible with MultiWordNet." | WordNet 1.6 | The synset side of the mapping | MAPNET v.0.1 | `/vault/Data/MapNet-0.1/README` |
| `mapping_frame_synsets.txt` | "Mapping between FrameNet frames and WordNet synsets (5,162 mappings)." | FrameNet frames and WordNet synsets | 5,162 lines. An opened line is `Abounding_with` then `a#00057580`. | MAPNET v.0.1 | `/vault/Data/MapNet-0.1/README`, `/vault/Data/MapNet-0.1/mapping_frame_synsets.txt` |
| Columns of `mapping_frame_synsets.txt` | The README names no column and does not say which field is the frame. | The two fields of a line | Two tab-separated fields | MAPNET v.0.1 | `/vault/Data/MapNet-0.1/README` |
| `mapping_lus_synsets.txt` | "Mapping between FrameNet frames, lus and WordNet synsets (5,162 mappings)." | FrameNet frames, lus, and WordNet synsets | 5,162 lines. An opened line is `Abounding_with`, `bejewelled.a`, `a#00057580`. | MAPNET v.0.1 | `/vault/Data/MapNet-0.1/README`, `/vault/Data/MapNet-0.1/mapping_lus_synsets.txt` |
| Columns of `mapping_lus_synsets.txt` | The README names no column. The file description names frames, lus, and synsets and does not assign them to positions. | The three fields of a line | Three tab-separated fields | MAPNET v.0.1 | `/vault/Data/MapNet-0.1/README` |
| Generation | "The resource was automatically generated." | The mapping as a whole | The two files | MAPNET v.0.1 | `/vault/Data/MapNet-0.1/README` |
| Precision | "The evaluated precision of the mapping 0.794." | The mapping as a whole | 0.794. The README puts no score on a row. | MAPNET v.0.1 | `/vault/Data/MapNet-0.1/README` |

## Records

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| `mapping_frame_synsets.txt` | Field one, field two, tab-separated. No names. | One mapping between a FrameNet frame and a WordNet synset. 5,162 lines, every line width 2. | `/vault/Data/MapNet-0.1/README`, the file |
| `mapping_lus_synsets.txt` | Field one, field two, field three, tab-separated. No names. | One mapping between FrameNet frames, lus, and WordNet synsets. 5,162 lines, every line width 3. | `/vault/Data/MapNet-0.1/README`, the file |

## Lineage

| Paths | What is shared | Proof |
| --- | --- | --- |
| `/vault/Data/MapNet-0.1/MapNet-0.1.zip` and `README`, `mapping_frame_synsets.txt`, `mapping_lus_synsets.txt` | The zip members match the three files byte for byte. The zip is that drop again. | SHA-256 |
| `/vault/Data/MapNet-0.1/` | No MapNet directory under `/vault/Data/.refresh-20260903`. | Directory listing |
| FrameNet 1.7 and WordNet 3.0 on the other corpus pages | Not the versions this README names. This file says FrameNet v. 1.3 and WordNet 1.6. | `/vault/Data/MapNet-0.1/README` |
