# Predicate Matrix

The Predicate Matrix attests of each row, the role of a predicate its predicate and role columns name, every column under its own name, and gives the highway its edges between the WordNet sense, the ILI number, the VerbNet class, the FrameNet frame and the PropBank roleset each row ties.

Predicate Matrix v1.3 is "a role of a predicate, mapped over VerbNet, WordNet, the MCR, FrameNet, PropBank and ESO": a tab-separated table whose first row names its 27 columns, "Each row of the Predicate Matrix represents the mapping of a role over the different resources and includes all the aligned knowledge about its corresponding verb." It is a hop, as [Hops](Hops.md) lists it.

## Source

| Source | Witness | Files | Read by |
| --- | --- | --- | --- |
| `predicate-matrix` | `Predicate Matrix v1.3` | `PredicateMatrix.v1.3.txt` | [`matrix.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/predicate-matrix/matrix.recipe); its `maps` lines feed `laplace highway` ([Types](../Reference/Types.md#perf-caches)) |

The source directory holds `source` and `matrix.recipe`, which matches `PredicateMatrix.v*.txt`; `README.txt` is not read: the source has no `reads` line.

## What is read

A row is the thing its `3_ID_PRED` and `4_ID_ROLE` name (`thing row 3_ID_PRED 4_ID_ROLE`), and every column is attested of it under its own name (`attest row *`); `NULL` in any family (`id:NULL`, `vn:NULL`, …) is empty and attests nothing. The four lists' identifiers are content as written, each naming the type the highway's list holds a slot for.

| Column | Written as | Read as | On the highway |
| --- | --- | --- | --- |
| `12_MCR_iliOffset` | `mcr:ili-30-01976841-v` | the WordNet 3.0 synset `01976841-v`, resolved to its ILI concept by CILI's map | the `ili` slot |
| `11_WN_SENSE` | `wn:drop%2:38:00` | the sense key, attested as written; on the highway resolved to its concept by WordNet's `index.sense`, as the offset is, each mapped on its own | the `ili` slot |
| `5_VN_CLASS` | `vn:51.3.1` | the VerbNet class whose ID ends in the number | the `vnclass` slot |
| `13_FN_FRAME` | `fn:Body_movement` | the frame by its name | the `fnframe` slot |
| `16_PB_ROLESET` | `pb:drop.01` | the roleset by PropBank's id | the `pbroleset` slot |
| each row | | every pair of the four that resolved | edges `ili`→`vnclass`, `ili`→`fnframe`, `ili`→`pbroleset`, `vnclass`→`fnframe`, `pbroleset`→`vnclass`, `pbroleset`→`fnframe`, each once |
| `NULL` in any of them | `vn:NULL` | resolves nothing | no edge |
| the other 22 columns | roles, lemmas, MCR domains, SUMO classes, ESO classes, frequencies | attested of the row under their own names, as written | nothing |
