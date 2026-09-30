# Predicate Matrix

Predicate Matrix attests, of each row's index, the path of its language, part of speech, predicate, and role, every one of the other 23 columns as written, prefix and NULL included, and its README attests nothing.

One source reads the Predicate Matrix v1.3, "a role of a predicate, mapped over VerbNet, WordNet, the MCR, FrameNet, PropBank and ESO". The file is a tab-separated table whose first row names its 27 columns, and the README says of it: "Each row of the Predicate Matrix represents the mapping of a role over the different resources and includes all the aligned knowledge about its corresponding verb." Predicate Matrix is a hop between lexicons, as [Hops](Hops.md) lists it.

## Source

| Source | Witness | Uncertainty | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `predicate-matrix` | `Predicate Matrix v1.3`, "named as the README's title names it" | deviation 90 | `unicode`, `iso-639` | `PredicateMatrix.v*.txt` under `PredicateMatrix.v1.3` | [`matrix.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/predicate-matrix/matrix.recipe) |

The uncertainty is the deviation the witness's attestations enter at, as [Consensus](../Semantics/Consensus.md#entry) describes. The source says of its 90 that it is "this recipe's choice for a curated academic resource; the specification does not give one": the number is not settled, and [Corpora](README.md#not-settled) lists it among what stays missing.

## The matrix

"The Predicate Matrix v1.3 file is structured in 27 columns. The first four form the index of the row." "Each row is indetified by the unique index formed by the first four columns." A row is one record, said together: what it speaks of is its index, the path of its first four fields in the row's order, and every other column is said of that index under the column's own name, as the header row writes it. Every field is recorded as the file writes it, with the prefix it carries: `id:`, `vn:`, `wn:`, `mcr:`, `fn:`, `pb:`, `eso:`.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `1_ID_LANG`, `2_ID_POS`, `3_ID_PRED`, `4_ID_ROLE` | `id:cat`, `id:v`, `id:abaixar.1.default`, `id:arg0` | the subject: the path of the four fields, in the row's order | the first part of every claim of the row | "This column contains the language of the predicate." "This column contains the part-of-speech of the predicate." "This column contains the predicate." "This column contains the role." README |
| `5_VN_CLASS` | `vn:51.3.1` | said of the index under the column's name | `[index, 5_VN_CLASS, vn:51.3.1]` | "This column contains the information of the VerbNet class." |
| `6_VN_CLASS_NUMBER` | `vn:51.3.1` | the same way | `[index, 6_VN_CLASS_NUMBER, vn:51.3.1]` | "This column contains the information of the VerbNet class number." |
| `7_VN_SUBCLASS` | `vn:NULL` | the same way | `[index, 7_VN_SUBCLASS, vn:NULL]` | "This column contains the information of VerbNet subclass." |
| `8_VN_SUBCLASS_NUMBER` | `vn:NULL` | the same way | `[index, 8_VN_SUBCLASS_NUMBER, vn:NULL]` | "This column contains the information of the VerbNet subclass number." |
| `9_VN_LEMA` | `vn:drop` | the same way; the header spells the name `LEMA` and so does the predicate | `[index, 9_VN_LEMA, vn:drop]` | "This column contains the information of the verb lemma." |
| `10_VN_ROLE` | `vn:Agent` | the same way | `[index, 10_VN_ROLE, vn:Agent]` | "This column contains the information of the VerbNet thematic-role." |
| `11_WN_SENSE` | `wn:drop%2:38:00` | the same way | `[index, 11_WN_SENSE, wn:drop%2:38:00]` | "This column contains the information of the word sense in WordNet." |
| `12_MCR_iliOffset` | `mcr:ili-30-01976841-v` | the same way | `[index, 12_MCR_iliOffset, mcr:ili-30-01976841-v]` | "This column contains the information of the ILI number in the MCR3.0." |
| `13_FN_FRAME` | `fn:Body_movement` | the same way | `[index, 13_FN_FRAME, fn:Body_movement]` | "This column contains the information of the frame in FrameNet." |
| `14_FN_LE` | `fn:drop.v` | the same way | `[index, 14_FN_LE, fn:drop.v]` | "This column contains the information of the corresponding lexical-entry in FrameNet." |
| `15_FN_FRAME_ELEMENT` | `fn:Agent` | the same way | `[index, 15_FN_FRAME_ELEMENT, fn:Agent]` | "This column contains the information of the frame-element in FrameNet." |
| `16_PB_ROLESET` | `pb:drop.01` | the same way | `[index, 16_PB_ROLESET, pb:drop.01]` | "This column contains the information of the predicate in PropBank." |
| `17_PB_ARG` | `pb:0` | the same way | `[index, 17_PB_ARG, pb:0]` | "This column contains the information of the predicate argument in PropBank." |
| `18_MCR_BC` | `mcr:0` | the same way | `[index, 18_MCR_BC, mcr:0]` | "This column contains the information if the verb sense it is Base Concept or not in the MCR3.0." |
| `19_MCR_DOMAIN` | `mcr:factotum` | the same way | `[index, 19_MCR_DOMAIN, mcr:factotum]` | "This column contains the information of the WordNet domain aligned to WordNet 3.0 in the MCR3.0." |
| `20_MCR_SUMO` | `mcr:Motion` | the same way | `[index, 20_MCR_SUMO, mcr:Motion]` | "This column contains the information of the AdimenSUMO in the MCR3.0." |
| `21_MCR_TO` | `mcr:Dynamic;Location` | the same way: the field is one value, `;` and all, because the recipe names no list | `[index, 21_MCR_TO, mcr:Dynamic;Location]` | "This column contains the information of the MCR Top Ontology in the MCR3.0." |
| `22_MCR_LEXNAME` | `mcr:motion` | the same way | `[index, 22_MCR_LEXNAME, mcr:motion]` | "This column contains the information of the MCR Lexicographical file name." |
| `23_MCR_BLC` | `mcr:ili-30-01835496-v` | the same way | `[index, 23_MCR_BLC, mcr:ili-30-01835496-v]` | "This column contains the information of the Base Level Concept of the WordNet verb sense in the MCR3.0." |
| `24_WN_SENSEFREC` | `wn:21` | the same way | `[index, 24_WN_SENSEFREC, wn:21]` | "This column contains the information of the frecuency of the WordNet 3.0 verb sense." |
| `25_WN_SYNSET_REL_NUM` | `wn:007` | the same way | `[index, 25_WN_SYNSET_REL_NUM, wn:007]` | "This column contains the information of the number of relations of the WordNet 3.0 verb sense." |
| `26_ESO_CLASS` | `eso:Motion` | the same way | `[index, 26_ESO_CLASS, eso:Motion]` | "This column contains the information of the class of the ESO ontology." |
| `27_ESO_ROLE` | `eso:NULL` | the same way | `[index, 27_ESO_ROLE, eso:NULL]` | "This column contains the information of the role of the ESO ontology." |
| the prefix of a field | `id:`, `vn:`, `wn:`, `mcr:`, `fn:`, `pb:`, `eso:` | part of the value, as written: the README does not mention the prefixes, and the recipe does not strip them | the value above, prefix and all | |
| `NULL` | `vn:NULL`, `wn:NULL`, `mcr:NULL`, `fn:NULL`, `pb:NULL`, `eso:NULL` | recorded as written. The recipe says: "README.txt does not mention NULL anywhere, so this recipe does not decide that such a field is one the source leaves empty: it is recorded as written. If it is the source's empty marker, this one line says so: `empty-matches ^[a-z]+:NULL$`" | `[index, 7_VN_SUBCLASS, vn:NULL]` | |
| an empty field | nothing between two tabs | what the file leaves empty: attests nothing | none | |

The row is what is witnessed, once, as one ledger row; every claim in it plays its matchup as [Consensus](../Semantics/Consensus.md#matchups) describes. The README also names NomBank, AnCora, and the Basque Verb Index among the sources integrated; the header has no column of theirs, so nothing is recorded of them.

## Not read

`README.txt` is read as ordinary text, as the source's `reads text` says: it is observed content, as [Attestations](../Semantics/Attestations.md#observations) describes, and attests nothing. The specification quoted above is its "File description of the Predicate Matrix v1.3".
