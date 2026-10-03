# Recorded Content

Measurements of what the `laplace` database held on 2026-10-03, before it was dropped, and of the loads made after each change to the Engine, show where the bytes went, how much of what was recorded repeated itself, and what each change removed.

The database figures were read with SELECTs and Engine dry runs only, before the database was dropped at about 04:50 UTC; they cannot be measured again until the sources are loaded again. The loads and the highway were measured afterwards, on the code named. The open work these numbers support is SaltyPatron/Laplace-Engine#12.

## Where the bytes went

`pg_database_size`, the sum of `reltuples` over the entity partitions, and a 0.5% `TABLESAMPLE SYSTEM` of the first tier-3 partitions:

| Measure | Value |
| --- | --- |
| Database | 382 GB |
| Entities | 437,188,192 |
| Bytes per entity, everything included | 938 |
| Tables, indexes | 217 GB, 163 GB |
| A tier-3 path: vertices, path bytes, mask bytes, row bytes | 4.7, 186, 37, 279 |
| A tier-3 entity: coordinate bytes, row bytes | 45, 96 |

Entities by tier, about: tier 2 19.8M, tier 3 153M, tier 4 140M, tier 5 85M, tier 6 9.7M, tier 7 35.6M. The median composition of tiers 3 to 5 had 3 constituents: most of the bulk was triples of the form `[thing, attribute, value]`, such as `[token, UPOS, NOUN]`, `[codepoint, OIDC, N]`, `[synset, lexicalized, false]`, `[token, SpaceAfter, No]`.

## Repeated attestations

A 3,190-row Bernoulli sample of `attestation`, with exact counts per (claim, witness), and exact counts per witness for some sources:

- 512M rows over 258M standings. Only 51.7% of the rows were distinct (claim, witness) pairs: about 248M repeats, carrying nothing, since `position` was empty in every sampled row.
- Repeats by witness: Universal Dependencies 75%, FrameNet 79% (7.01M of 8.88M), Predicate Matrix 80% (7.03M of 8.78M), Wiktextract about 35%, ConceptNet about 16%. One pair, `[., UPOS, PUNCT]`, was written 208,764 times by one witness.
- Whole re-runs wrote everything again: Unicode's 33,332,308 rows were exactly two runs of 16.7M; Kaikki's first stretch was written twice (9,887,045 rows).

After the Engine wrote a (claim, witness) once a batch (Laplace-Engine d0a2e29), the repeated share of a load fell from 47.8% to 0%. Repeats are now dropped, not counted; [Attestations: Strands](../Semantics/Attestations.md#strands) says they are games.

## Records that never deduplicate

Every row or line of a curated file was also recorded as an entity of its own, carrying the file's keys, so no two were ever the same content:

| Source | What the record held | About |
| --- | --- | --- |
| ConceptNet | the whole line: URI, dataset, licence, contributor, weight | 33M entities, 7.4% of all; 22-36M URI nodes besides |
| Universal Dependencies | each word line with its `ID`, `HEAD`, `DEPS` | 21.6M records, against 12.0M without those parts |
| Open Multilingual Wordnet | id strings such as `omw-es-hermana-10595164-n` | 9M |
| ATOMIC | each tuple line | 8M |

With keys left out of the records (Laplace-Engine d0a2e29), three sources loaded into an empty database and then loaded again:

| | First load | Second load |
| --- | --- | --- |
| File trunks found already recorded | 0 | all 35 |
| Entities written | 3,997,589 | 0 |
| Attestations written | 1,938,569, every one distinct | 0 |
| Time | 56.4 s | 10.1 s |

## What each source wasted

Estimated from the samples and from Engine dry runs (`--plan`, `--claims`); "about" marks an estimate.

| Source | Estimated waste | What it was |
| --- | --- | --- |
| ConceptNet | about 100M of 173M attestations; about 110M of 143M entities | `/r/ExternalURL` edges split on `/`, so their end became `wiki`: `[wiki, en.wiktionary.org]` ×755,058, about 49M attestations; the line records above |
| Universal Dependencies | about 174M repeated rows, 9.6M row entities, 18M placeholder attestations, 8M id claims | per-token repeats; MISC keys (`UI`, `AlignBegin`, `XmlId`, …) about 7-8M claims; `SpaceAfter=No` 7.14M, derivable from the text; `DEPS` restating `HEAD:DEPREL` 9.55M of 11.78M |
| ATOMIC10x | about 39M of 45M attestations; about 51M of 59M entities | `rec_0.5` to `rec_0.9`, thresholds of `p_valid_model` (each flag is `p_valid_model` at least 0.96755, 0.95577, 0.92709, 0.83781, 0.65344, checked on 1M lines), 32.3M claims, 71% |
| Kaikki's Wiktionary | about 30-35M of 48.7M rows | a doubled run and an older recipe's claims |
| Unicode | about 31M of 33.3M rows; 14.5M of 16.6M claim entities | properties the flags perf-cache already holds, stated again as claims; a doubled run |
| Predicate Matrix, FrameNet | about 7M repeats each | per-occurrence repeats |
| Open Multilingual Wordnet | about 7-8M of 9.5M rows | id strings; English definitions equal to CILI's (about 117K) |
| Mapping files | about 8.9M rows | SemLink, Predicate Matrix, CILI's maps, VerbAtlas's bridges and MapNet attested besides feeding the highway |

With the `perfcache` recipe line (Laplace-Engine d0a2e29), a Unicode load records 79% fewer compositions and 87% fewer attestations: the properties the flags perf-cache holds are not stated again.

## The write-ahead log

`pg_walinspect` over the log of a load, by relation:

| Relation | Kind | Page images | Images GB | Data GB |
| --- | --- | --- | --- | --- |
| `physicality_paths` | GIN | 1,107,424 | 4.23 | 0.59 |
| `entity_id` | log records | 293,821 | 1.49 | 0.00 |
| `physicality_entity` | B-tree | 278,660 | 1.42 | 0.12 |
| `entity` | log records | 126,359 | 0.66 | 0.00 |
| `entity_id` | B-tree | 97,217 | 0.50 | 0.08 |
| `entity_coord` | GiST | 89,965 | 0.38 | 0.39 |

Full-page images of index pages, not the data, were the log. Before and after the container index's pending list was raised to 256 MB and the log compressed with zstd ([Database](../Operations/Database.md)):

| | Paths loaded | GIN images | Per GB loaded | B-tree images | All of the log |
| --- | --- | --- | --- | --- | --- |
| Before | 10.11 GB | 41.00 GB | 4.05 | 118.2 GB | 217.7 GB |
| After | 1.70 GB | 1.73 GB | 1.02 | 23.0 GB | 33.6 GB |

The B-tree images are what remains: a B-tree keyed by a random 128-bit ID touches a different page with nearly every row, so every page a checkpoint interval first touches is written whole.

## The highway's mappings

The `edges` lines of the highway built 2026-10-03 07:31 (`tier0.highway.layout`) against the one built 2026-10-01 21:10:

| Edges | 2026-10-01 | 2026-10-03 |
| --- | --- | --- |
| all | 91,749 | 73,700 |
| FrameNet frame element → frame | 11,410 | 0 |
| PropBank roleset → FrameNet frame | 8,141 | 5,562 |
| PropBank roleset → VerbNet class | 8,358 | 4,186 |
| FrameNet lexical unit → frame | 13,552 | 13,572 |
| ILI → FrameNet frame | 7,617 | 7,622 |

The build of 05:18 logged "223,284 mappings name a key no list holds, or a type of another list: left out". The highway is keyed only to WordNet 3.0; Open English WordNet is numbered as 3.1, ConceptNet's WordNet links are 3.1, MapNet and WordFrameNet are 1.6, and CILI's 3.1 and 1.6 maps are on disk and read by nothing. That the mapping files are keyed to older VerbNet, FrameNet and PropBank editions is the likely reason for the left-out mappings, and is not verified.

The highway's lists, as built: ILI concepts 116,698, PropBank rolesets 11,205, FrameNet lexical units 13,631, FrameNet frame elements 11,428, FrameNet frames 1,221, VerbNet classes 609, VerbAtlas frames 432, WordNet lexicographer files 45, VerbNet thematic roles 39, dependency relations 37, parts of speech 17: 155,362 records.
