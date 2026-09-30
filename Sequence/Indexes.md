# 14. Indexes

After a bulk load the indexes are built, the planner is told what the columns really are, and the install is measured and checked against itself.

Laplace exploits GiST and GIN indexing for novel mechanisms. Development favors observability and benchmarks over a heavy focus on tests and gates: the invention should speak for itself.

## Before this stage

[11. Content](Content.md), [12. Attestations](Attestations.md), and [13. Consensus](Consensus.md) loaded. [8. Database](Database.md) operation 8.12, the planning settings.

## Operations

### 14.1 B-tree on IDs

- **In:** the entity and physicality tables.
- **Do:** the primary keys on the ID, and the physicality → entity foreign key.
- **Out:** a lookup by ID that prunes to one partition and hits one index.
- **Check:** a word by computed ID and tier, 0.02 ms, 1 partition.
- **Mechanism:** `entity_id`, `physicality_entity`, `attestation_claim` in `lookup.sql`, present from deploy ([Schema: Indexes](../Reference/Schema.md#indexes)). The built schema has no primary key on `entity` and no foreign key from `physicality`. Status: **built**.
- **From:** [Deployment](../Operations/Deployment.md), [Research: Engine Measurements: Queries](../Research/Engine.md#queries).

### 14.2 B-tree on Hilbert values

- **In:** the entity table.
- **Do:** index the Hilbert value. It is derived from the real coordinate deterministically, so a range of space is a set of Hilbert intervals, and loading in key order keeps pages spatially coherent.
- **Out:** locality, partitioning, and ordering by Hilbert value.
- **Mechanism:** `entity_hilbert` in `indexes.sql`; the stored value has its top bit flipped so `bigint` order is Hilbert order ([Schema: Indexes](../Reference/Schema.md#indexes), [Formats: The Hilbert value](../Reference/Formats.md#the-hilbert-value)). Status: **built**.
- **From:** [Atoms: Placement](../Storage/Atoms.md#placement), [Research: Geometry: Hilbert curves](../Research/Geometry.md#hilbert-curves).

### 14.3 4D GiST on real coordinates

- **In:** the entity table's real coordinate.
- **Do:** the n-dimensional GiST operator class, which stores float32 boxes that round outward so the float box is larger than the double box, and supports n-D overlap and n-D distance for KNN ordering. A float32 box keeps 24 of a double's 53 significand bits, so the index is a conservative candidate filter and an exact lookup rechecks the exact doubles.
- **Out:** nearest neighbors in 4D, and shape searches with a candidate stage ahead of the exact recheck in C.
- **Check:** the 16 word segments nearest `king` in 4D, 7.7 ms; on the prototype the 4D GiST was 338 MB over 3.9 million entities.
- **Mechanism:** `entity_coord … USING gist (coord gist_geometry_ops_nd)` ([Schema: Indexes](../Reference/Schema.md#indexes)). Status: **built**.
- **From:** [Physicality: Indexes](../Storage/Physicality.md#indexes), [Research: Geometry: GiST](../Research/Geometry.md#gist), [Research: Prototype: Store](../Research/Prototype.md#store).

### 14.4 GIN on the IDs decoded from paths

- **In:** the physicality table's path.
- **Do:** GIN indexes each trajectory's constituents, read from the IDs in its geometry, to find every container of any node, such as every sentence that contains a word. It indexes the path geometry directly; no array column exists. The operator class Laplace-postgres provides supplies `extractValue`, which returns the constituents of a trajectory; `extractQuery`, which returns the keys in a query value; `consistent`, which decides whether a row matches given which query keys it contains; and `compare`. A posting list records presence, so order and multiplicity are rechecked on the row, where the trajectory holds both. The key function's cost is 10,000, from [8. Database](Database.md) operation 8.12.
- **Out:** every container of any node. The GIN, the first-id B-tree, and the trajectory probe are partial on the text-trajectory physicality type; a set trajectory of [12. Attestations](Attestations.md) operation 12.8 gets its own type value and its own partial GIN, so a collection membership probe, forms that are nominative and singular and masculine, is one `@>` probe on the bundle rather than an N-way self-join.
- **Check:** every container of `Holmes`, 527 records, 0.80 ms; the run `Sherlock Holmes`, 92 sentences, 1.76 ms; on the prototype the GIN was 450 MB.
- **Mechanism:** `physicality_paths … USING gin (path laplace_path_ops)`; the operator class's `extract_value`, `extract_query`, `consistent`, `triconsistent` over `blake3` keys, `recheck = false` ([SQL: Containment and the GIN](../Reference/SQL.md#containment-and-the-gin)); `gin_clean_pending_list` after every load ([Ingest: After the load](../Reference/Ingest.md#after-the-load)). One GIN over every physicality; no per-type partial index. Status: **built; partial indexes per physicality type specified**.
- **From:** [Physicality: Indexes](../Storage/Physicality.md#indexes), [Query: Containers and occurrences](../Query.md#containers-and-occurrences), `docs/specs/38_Collections_Are_Compositions.md` §2 and §4, [Research: Geometry: GIN](../Research/Geometry.md#gin).

### 14.5 B-tree on occurrences

- **In:** the statistics table.
- **Do:** index the occurrence and container counts.
- **Out:** the most frequent word segments, 0.15 ms.
- **Mechanism:** none: there is no statistics table; `laplace fills` computes occurrences ([Reads: laplace fills](../Reference/Reads.md#laplace-fills)). The prototype had `entity_stats`. Status: **prototype**.
- **From:** [Deployment](../Operations/Deployment.md), [Research: Engine Measurements: Queries](../Research/Engine.md#queries).

### 14.6 Indexes on the semantics tables

- **In:** the claim, ledger, and standing tables.
- **Do:** the claim's consensus ID and each of its parts, so a claim can be found by any part left open; the ledger by claim; the standing by claim.
- **Out:** `[dog, eng, ?]` in 3.3 ms and `[?, language, i46360]` for eight languages in 1.2 ms.
- **Mechanism:** `attestation_claim`, `attestation_witness`, the `consensus` and `witness` primary keys ([Schema: Indexes](../Reference/Schema.md#indexes)); a claim by any open part is the GIN on the claim's own path, `path @> $1::blake3[]` in `claims_like` ([Reads: The claims that hold an entity](../Reference/Reads.md#the-claims-that-hold-an-entity)). Status: **built**.
- **From:** [Research: Semantics Experiments: Translation through the ILI](../Research/Semantics-Experiments.md#translation-through-the-ili), [Research: Engine Measurements: Consensus writes](../Research/Engine.md#consensus-writes).

### 14.7 `ANALYZE`

- **In:** every table.
- **Do:** run `ANALYZE`, with statistics on the path column at 0, because histograms of packed IDs mean nothing.
- **Check:** 2.5 s, against 332 s with path histograms.
- **Mechanism:** the `ANALYZE` at the end of `indexes.sql`, with statistics 0 on `path` from `schema.sql` ([Schema: Indexes](../Reference/Schema.md#indexes)). Status: **built**.
- **From:** [Database: Planning](../Operations/Database.md#planning).

### 14.8 Measure every native operation

- **In:** the library of [3. Builds](Builds.md).
- **Do:** run the benchmark: every operation with each SIMD kernel beside its scalar form.
- **Out:** this machine's rates, to compare with the reference machine's: wall check 296 M/s; exact centroid 211 M points/s; ID into and out of the mantissas 104 M/s; 4D Hilbert value 12 M/s; codepoint ID 8–12 M/s; Glicko-2 matchup 7.8 M/s; vertex scan 14.2 GB/s scalar and 15.0 GB/s AVX2; 4D squared distances 1.1 G/s scalar and 1.4 G/s AVX2; discrete Fréchet on 1,000 × 1,000 vertices 3.8 ms.
- **Mechanism:** `laplace bench` ([CLI: laplace bench](../Reference/CLI.md#laplace-bench)). Status: **built**.
- **From:** [Deployment](../Operations/Deployment.md), [Research: Engine Measurements: Native operations](../Research/Engine.md#native-operations).

### 14.9 Measure every query

- **In:** the loaded database.
- **Do:** run each query cold and warm, and report execution and round-trip time, buffers read and hit, and the partitions the plan touched.
- **Out:** this install's numbers beside the reference: a word by computed ID and tier 0.02 ms in 1 partition; by ID alone 0.08 ms in 14; a word never recorded 0.01 ms; every container of `Holmes` 0.80 ms in 52; the run `Sherlock Holmes` 1.76 ms; what fills `[Captain, ' ', ?]` 9.2 ms; what follows "the capital of " 24.7 ms; the 16 nearest `king` in 4D 7.7 ms in 16; the 20 most frequent word segments 0.15 ms. Queries that start from an ID prune to one partition; queries that search for containers, or by position, visit every partition's index.
- **Mechanism:** `Laplace-postgres/bench/bench_queries.py` ([Checks: The query benchmark](../Reference/Checks.md#the-query-benchmark)); its last query names the table `standing`, which the built schema calls `consensus`. Status: **built, with that defect**.
- **From:** [Deployment](../Operations/Deployment.md), [Research: Engine Measurements: Queries](../Research/Engine.md#queries).

### 14.10 Check the install against itself

- **In:** the loaded database.
- **Do:** run the checks against the database itself.
- **Check:** every entity has exactly one physicality; entity IDs are unique; all 1,114,112 codepoints are recorded at tier 0; nothing falls outside the wall, in exact integer arithmetic; pure repeats sit exactly on their constituent's point; IDs recompute from children alone; tiers only go up; every composition is at least as deep as its constituents' average; a file recomposes from the database byte for byte; re-ingesting it adds nothing and lands on the same trunk. The prototype passed every one, on 3,915,022 entities.
- **Mechanism:** `Laplace-Prototype/tests/verify.py`, ten checks against the prototype's schema ([Checks: The prototype's verification](../Reference/Checks.md#the-prototypes-verification)); against the built schema its two checks that read `source` cannot run. The engine's own checks are the recompose comparison and `laplace status` ([Checks: The engine's checks](../Reference/Checks.md#the-engines-checks)). Status: **prototype**.
- **From:** [Research: Prototype: Verification](../Research/Prototype.md#verification), [Ingestion: Deduplication](../Storage/Ingestion.md#deduplication).

### 14.11 Confirm the fingerprints

- **In:** the fingerprints of [3. Builds](Builds.md) operation 3.8 and [5. Tier 0](Tier-0.md) operation 5.7.
- **Do:** the database reports whether its tier 0 is this engine's. Two installs with the same fingerprint produce the same coordinates for the same content.
- **Out:** an install that knows which build and which tier 0 it has.
- **Check:** one deployed revision: the application, the prefix native libraries, the PostgreSQL execution module, and the tier-0 perf-cache identify one build, and the deployed-revision check probes each served record against the canonical function in the serving process.
- **Mechanism:** `laplace status`: `laplace_fingerprint()` against `lp_tier0_fingerprint` ([CLI: laplace status](../Reference/CLI.md#laplace-status)). Status: **built for tier 0; the served-record probe of every ROM specified**.
- **From:** [Atoms: Generation](../Storage/Atoms.md#generation); `docs/OPERATING_SEQUENCE.md` §6.

### 14.12 Publish the hot cache generations

- **In:** the loaded database and the roster of [7. Perfcaches](Perfcaches.md).
- **Do:** from the canonical rows, emit the admitted and hot ROMs that depend on content: the pixel, patch, region, and image generations, the audio generations, the chess position and transition floors, the factor ROM, and the generation-corpus ROM, each binding the generations it depends on, published by write-to-temporary, checksum, and atomic replace, one way, never seeding the database back. A record present in a cache is thereafter a bounded lookup at [11. Content](Content.md) operation 11.8 and at [19. Pull](Pull.md).
- **Out:** the higher cache generations of this install.
- **Check:** each generation's parity receipt against the canonical path.
- **Mechanism:** none. Status: **specified**.
- **From:** `docs/specs/33_Perfcache_Blob_Law.md` §Roster; [7. Perfcaches](Perfcaches.md) operations 7.5 to 7.7.

## What this stage leaves behind

O(log N) lookups, and the numbers and checks that say whether this install matches the fingerprint and the measurements.

## Without this stage

Every lookup is a scan, no step of the forward pass is O(log N) + O(K), and nothing says whether the install is right.
