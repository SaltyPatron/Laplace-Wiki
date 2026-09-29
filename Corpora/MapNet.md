# MapNet

MapNet attests a generated mapping from FrameNet 1.3 to WordNet 1.6, with the precision its own README states and no score on a row.

## Value

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| Hop | A generated mapping from FrameNet 1.3 to WordNet 1.6. [Claims](../Semantics/Claims.md#the-linguistic-super-highway) names MapNet. [Pull](../Semantics/Pull.md#hop-and-fanout) is the pull across a hop. [Hops](Hops.md) lists the edge. | FrameNet v. 1.3 and WordNet 1.6 | The two mapping files | MAPNET v.0.1 | `/vault/Data/MapNet-0.1/README` |
| FrameNet version | "All frames and lexical units included in the resource are described in FrameNet v. 1.3." | FrameNet v. 1.3 | The frames and lexical units in the two files | MAPNET v.0.1 | `/vault/Data/MapNet-0.1/README` |
| WordNet version | "All synsets refer to WordNet version 1.6, compatible with MultiWordNet." | WordNet 1.6 | The synset side of the mapping | MAPNET v.0.1 | `/vault/Data/MapNet-0.1/README` |
| `mapping_frame_synsets.txt` | "Mapping between FrameNet frames and WordNet synsets (5,162 mappings)." | FrameNet frames and WordNet synsets | 5,162 lines. An opened line is `Abounding_with` then `a#00057580`. | MAPNET v.0.1 | `/vault/Data/MapNet-0.1/README`, `/vault/Data/MapNet-0.1/mapping_frame_synsets.txt` |
| Columns of `mapping_frame_synsets.txt` | The README names no column and does not say which field is the frame. | The two fields of a line | Two tab-separated fields | MAPNET v.0.1 | `/vault/Data/MapNet-0.1/README` |
| `mapping_lus_synsets.txt` | "Mapping between FrameNet frames, lus and WordNet synsets (5,162 mappings)." | FrameNet frames, lus, and WordNet synsets | 5,162 lines. An opened line is `Abounding_with`, `bejewelled.a`, `a#00057580`. | MAPNET v.0.1 | `/vault/Data/MapNet-0.1/README`, `/vault/Data/MapNet-0.1/mapping_lus_synsets.txt` |
| Columns of `mapping_lus_synsets.txt` | The README names no column. The file description names frames, lus, and synsets and does not assign them to positions. | The three fields of a line | Three tab-separated fields | MAPNET v.0.1 | `/vault/Data/MapNet-0.1/README` |
| Generation | "The resource was automatically generated." | The mapping as a whole | The two files | MAPNET v.0.1 | `/vault/Data/MapNet-0.1/README` |
| Precision | "The evaluated precision of the mapping 0.794." | The mapping as a whole | 0.794. The README puts no score on a row. | MAPNET v.0.1 | `/vault/Data/MapNet-0.1/README` |

## Format

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| `mapping_frame_synsets.txt` | Field one, field two, tab-separated. No names. | One mapping between a FrameNet frame and a WordNet synset. 5,162 lines, every line width 2. | `/vault/Data/MapNet-0.1/README`, the file |
| `mapping_lus_synsets.txt` | Field one, field two, field three, tab-separated. No names. | One mapping between FrameNet frames, lus, and WordNet synsets. 5,162 lines, every line width 3. | `/vault/Data/MapNet-0.1/README`, the file |
