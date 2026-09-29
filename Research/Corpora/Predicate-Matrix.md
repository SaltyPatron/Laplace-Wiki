# Predicate Matrix

Predicate Matrix attests one predicate role joined across VerbNet, WordNet, FrameNet, and PropBank.

## Files

| Path | Bytes | What the file is | Proof |
| --- | ---: | --- | --- |
| `/vault/Data/PredicateMatrix.v1.3/PredicateMatrix.v1.3.txt` | 140813653 | Predicate Matrix file. Header plus 426,696 data rows, 27 tab-separated columns, every data row the same width. | `/vault/Data/PredicateMatrix.v1.3/README.txt` and the file |
| `/vault/Data/PredicateMatrix.v1.3/README.txt` | 5954 | README file for Predicate Matrix v1.3. | The file's own contents list |

## Attestations

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| Row | "Each row of the Predicate Matrix represents the mapping of a role over the different resources and includes all the aligned knowledge about its corresponding verb." The README says each row is "indetified by the unique index formed by the first four columns." [Claims](../../Semantics/Claims.md#the-linguistic-super-highway) writes the edge as PredicateMatrix. [Pull](../../Semantics/Pull.md#hop-and-fanout) is the pull across a hop. [Hops](Hops.md) lists it. | The role named by the first four columns | One tab-separated record | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| Integrated sources | "The integration of multiple sources of predicate information including FrameNet, VerbNet, PropBank, WordNet, NomBank, ESO, AnCora and Basque Verb Index," plus "ontological knowledge from the Multilingual Central Repository (MCR)." The header has no column named NomBank, AnCora, or Basque Verb Index. | Those named sources, only where a column below says so | The row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt`, the header line of `PredicateMatrix.v1.3.txt` |
| `1_ID_LANG` | "This column contains the language of the predicate." | The row index | The file writes `id:cat` on the first data row. The README does not define the code after `id:`. | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `2_ID_POS` | "This column contains the part-of-speech of the predicate." | The row index | `id:v` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `3_ID_PRED` | "This column contains the predicate." | The row index | `id:abaixar.1.default` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `4_ID_ROLE` | "This column contains the role." | The row index | `id:arg0` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `5_VN_CLASS` | "This column contains the information of the VerbNet class." | The row index | `vn:51.3.1` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `6_VN_CLASS_NUMBER` | "This column contains the information of the VerbNet class number." | The row index | `vn:51.3.1` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `7_VN_SUBCLASS` | "This column contains the information of VerbNet subclass." | The row index | `vn:NULL` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `8_VN_SUBCLASS_NUMBER` | "This column contains the information of the VerbNet subclass number." | The row index | `vn:NULL` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `9_VN_LEMA` | "This column contains the information of the verb lemma." The header spells the name `LEMA`. | The row index | `vn:drop` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `10_VN_ROLE` | "This column contains the information of the VerbNet thematic-role." | The row index | `vn:Agent` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `11_WN_SENSE` | "This column contains the information of the word sense in WordNet." | The row index | `wn:drop%2:38:00` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `12_MCR_iliOffset` | "This column contains the information of the ILI number in the MCR3.0." | The row index | `mcr:ili-30-01976841-v` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `13_FN_FRAME` | "This column contains the information of the frame in FrameNet." | The row index | `fn:Body_movement` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `14_FN_LE` | "This column contains the information of the corresponding lexical-entry in FrameNet." | The row index | `fn:drop.v` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `15_FN_FRAME_ELEMENT` | "This column contains the information of the frame-element in FrameNet." | The row index | `fn:Agent` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `16_PB_ROLESET` | "This column contains the information of the predicate in PropBank." | The row index | `pb:drop.01` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `17_PB_ARG` | "This column contains the information of the predicate argument in PropBank." | The row index | `pb:0` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `18_MCR_BC` | "This column contains the information if the verb sense it is Base Concept or not in the MCR3.0." | The row index | `mcr:0` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `19_MCR_DOMAIN` | "This column contains the information of the WordNet domain aligned to WordNet 3.0 in the MCR3.0." | The row index | `mcr:factotum` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `20_MCR_SUMO` | "This column contains the information of the AdimenSUMO in the MCR3.0." | The row index | `mcr:Motion` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `21_MCR_TO` | "This column contains the information of the MCR Top Ontology in the MCR3.0." | The row index | `mcr:Dynamic;Location` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `22_MCR_LEXNAME` | "This column contains the information of the MCR Lexicographical file name." | The row index | `mcr:motion` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `23_MCR_BLC` | "This column contains the information of the Base Level Concept of the WordNet verb sense in the MCR3.0." | The row index | `mcr:ili-30-01835496-v` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `24_WN_SENSEFREC` | "This column contains the information of the frecuency of the WordNet 3.0 verb sense." | The row index | `wn:21` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `25_WN_SYNSET_REL_NUM` | "This column contains the information of the number of relations of the WordNet 3.0 verb sense." | The row index | `wn:007` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `26_ESO_CLASS` | "This column contains the information of the class of the ESO ontology." | The row index | `eso:Motion` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `27_ESO_ROLE` | "This column contains the information of the role of the ESO ontology." | The row index | `eso:NULL` on the first data row | Predicate Matrix v1.3 | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| Prefixes `id:` `vn:` `wn:` `mcr:` `fn:` `pb:` `eso:` | Not defined. `README.txt` does not mention them. | Every cell of a data row | The file writes one of those prefixes before the field text. | Predicate Matrix v1.3 file, not the README | `/vault/Data/PredicateMatrix.v1.3/PredicateMatrix.v1.3.txt` |
| `NULL` | Not defined. `README.txt` does not mention NULL. | The cell that writes it | The file writes the prefix and then `NULL`, as in `vn:NULL` and `eso:NULL`. | Predicate Matrix v1.3 file, not the README | `/vault/Data/PredicateMatrix.v1.3/PredicateMatrix.v1.3.txt` |

## Records

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| Header | `1_ID_LANG`, `2_ID_POS`, `3_ID_PRED`, `4_ID_ROLE`, `5_VN_CLASS`, `6_VN_CLASS_NUMBER`, `7_VN_SUBCLASS`, `8_VN_SUBCLASS_NUMBER`, `9_VN_LEMA`, `10_VN_ROLE`, `11_WN_SENSE`, `12_MCR_iliOffset`, `13_FN_FRAME`, `14_FN_LE`, `15_FN_FRAME_ELEMENT`, `16_PB_ROLESET`, `17_PB_ARG`, `18_MCR_BC`, `19_MCR_DOMAIN`, `20_MCR_SUMO`, `21_MCR_TO`, `22_MCR_LEXNAME`, `23_MCR_BLC`, `24_WN_SENSEFREC`, `25_WN_SYNSET_REL_NUM`, `26_ESO_CLASS`, `27_ESO_ROLE` | The names of the 27 columns, one per field, tab-separated. | `/vault/Data/PredicateMatrix.v1.3/PredicateMatrix.v1.3.txt` |
| Data row | Those 27 fields in that order | The mapping of one role. 426,696 such rows. | `/vault/Data/PredicateMatrix.v1.3/README.txt` |

## Lineage

| Paths | What is shared | Proof |
| --- | --- | --- |
| `/vault/Data/PredicateMatrix.v1.3/` | The only copy on this machine. No `PredicateMatrix` directory under `/vault/Data/.refresh-20260903`. | Directory listing |
| The README's sources and the 27 columns | The README names NomBank, AnCora, and Basque Verb Index as integrated sources. None of those words is a column name. | `/vault/Data/PredicateMatrix.v1.3/README.txt` and the header |
