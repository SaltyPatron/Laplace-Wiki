# Predicate Matrix

The Predicate Matrix is the highway's input: every row ties a WordNet sense, an ILI number, a VerbNet class, a FrameNet frame and a PropBank roleset by the keys each resource uses, and the highway holds those ties as edges. No recipe reads the file, and no claim holds a Predicate Matrix key.

Predicate Matrix v1.3 is "a role of a predicate, mapped over VerbNet, WordNet, the MCR, FrameNet, PropBank and ESO": a tab-separated table whose first row names its 27 columns, "Each row of the Predicate Matrix represents the mapping of a role over the different resources and includes all the aligned knowledge about its corresponding verb." It is a hop, as [Hops](Hops.md) lists it.

## Source

| Source | Witness | Files | Read by |
| --- | --- | --- | --- |
| `predicate-matrix` | `Predicate Matrix v1.3` | `PredicateMatrix.v1.3.txt` | `laplace highway` ([Types](../Reference/Types.md#perf-caches)) |

The source directory holds a `source` file and no recipe; `README.txt` is read as text through the source's `reads text`, observed content that attests nothing.

## What the highway takes

| Column | Written as | Read as | On the highway |
| --- | --- | --- | --- |
| `12_MCR_iliOffset` | `mcr:ili-30-01976841-v` | the WordNet 3.0 synset `01976841-v`, resolved to its ILI concept by CILI's map | the `ili` slot |
| `11_WN_SENSE`, when the offset resolves nothing | `wn:drop%2:38:00` | the sense key, resolved to its concept by WordNet's `index.sense` | the `ili` slot |
| `5_VN_CLASS` | `vn:51.3.1` | the VerbNet class whose ID ends in the number | the `vnclass` slot |
| `13_FN_FRAME` | `fn:Body_movement` | the frame by its name | the `fnframe` slot |
| `16_PB_ROLESET` | `pb:drop.01` | the roleset by PropBank's id | the `pbroleset` slot |
| each row | | every pair of the four that resolved | edges `ili`→`vnclass`, `ili`→`fnframe`, `ili`→`pbroleset`, `vnclass`→`fnframe`, `pbroleset`→`vnclass`, `pbroleset`→`fnframe`, each once |
| `NULL` in any of them | `vn:NULL` | resolves nothing | no edge |
| the other 22 columns | roles, lemmas, MCR domains, SUMO classes, ESO classes, frequencies | not taken: role mappings and classifications the highway does not yet carry | nothing |

The highway counted 2,242,016 Predicate Matrix edges when it was last generated.
