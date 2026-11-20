# 14. Indexes

After a bulk load the indexes are built, the planner is told what the columns really are, and the install is measured and checked against itself.

Laplace exploits GiST and GIN indexing for novel mechanisms, measured end to end on the deployed server against loaded content rather than simulated in mock harnesses.

## Before this stage

[11. Content](Content.md), [12. Attestations](Attestations.md), and [13. Consensus](Consensus.md) loaded. [8. Database](Database.md) operation 8.12, the planning settings.

## Operations

### 14.1 Primary and unique B-trees on `entity` and `physicality`

- **In:** `entity` and `physicality`, each range-partitioned 9 ways by `tier` (`t0`..`t8plus`).
- **Do:** build primary keys `(tier, id)` on `entity` and `(tier, entity)` on `physicality`, per-partition `UNIQUE (id)` / `UNIQUE (entity)` indexes, and the foreign key `(tier, entity) → entity(tier, id) ON UPDATE CASCADE` (`laplace_schema_indexes()`).
- **Out:** point lookups by `(tier, id)` that prune to one tier partition and hit one B-tree, and point lookups by `id` alone that probe at most the 9 tier partitions.
- **From:** [Reference: Schema](../Reference/Schema.md#the-four-tables), [Deployment](../Operations/Deployment.md), [Research: Engine Measurements: Queries](../Research/Engine.md#queries).

### 14.2 B-trees on Hilbert values

- **In:** the `entity` table.
- **Do:** build `entity_hilbert` on `entity (hilbert)` and `entity_tier_hilbert` on `entity (tier, hilbert, id)`, where `hilbert` is stored sign-flipped (`h ^ 0x8000000000000000`) so signed `bigint` B-tree order equals unsigned 4D Hilbert order. Because the Hilbert key derives deterministically from the 4D coordinate, spatial neighborhoods map to compact Hilbert intervals and bulk loads in Hilbert order keep heap pages spatially coherent.
- **Out:** locality, range scans, and tier-scoped Hilbert ordering.
- **From:** [Reference: Schema](../Reference/Schema.md#the-indexes), [Atoms: Placement](../Storage/Atoms.md#placement), [Research: Geometry: Hilbert curves](../Research/Geometry.md#hilbert-curves).

### 14.3 4D GiST on real coordinates

- **In:** `entity.coord` (`geometry(PointZM)`).
- **Do:** build `entity_coord USING gist (coord laplace_point4d_ops)` and `entity_angular USING gist (coord laplace_angular4d_ops)`. GiST bounding boxes conservatively bound the 4D fixed-point coordinates and support exact 4D Euclidean and angular k-NN candidate ordering ahead of exact fixed-point / binary64 recheck in C.
- **Out:** 4D spatial and angular nearest neighbors, plus fast endpoint candidate pruning for Fréchet, DTW, and EDR curve queries.
- **From:** [Reference: Schema](../Reference/Schema.md#the-indexes), [Physicality: Indexes](../Storage/Physicality.md#indexes), [Research: Geometry: GiST](../Research/Geometry.md#gist).

### 14.4 Composite GIN on `physicality.path` and `physicality.mask`

- **In:** `physicality.path` (`geometry`) and `physicality.mask` (`bit(64)`).
- **Do:** build `physicality_paths USING gin (path laplace_path_ops, mask laplace_mask_ops) WITH (gin_pending_list_limit = 32768)` and the partial assertion index `physicality_assertions USING gin (path laplace_path_ops) WITH (gin_pending_list_limit = 32768) WHERE laplace_path_has_roles(path, 6)`. `laplace_path_ops` extracts the 128-bit constituent `lp_id`s directly from the packed EWKB mantissas with zero array side-columns, while `laplace_mask_ops` indexes the 64-bit `mask` bank descriptors (`kind`, `upos`, `lexfile`, `deprel`, `vnrole`, `wnframe` from `manifest/banks.tsv`). Because `physicality` is partitioned by `tier` (`t0`..`t8plus`), upward containment probes (`tier > child.tier`) automatically prune lower and equal tier partitions, and intersecting constituent IDs with `mask` bits happens inside one composite GIN scan before exact SIMD vertex-order recheck on matching rows.
- **Out:** microsecond-to-millisecond containment, phrase, gap, collection-membership, and mask-filtered claim lookups with zero `contains` or `precedes` edge tables.
- **From:** [Reference: Schema](../Reference/Schema.md#the-indexes), [Physicality: Indexes](../Storage/Physicality.md#indexes), [Query: Containers and occurrences](../Query.md#containers-and-occurrences), [Research: Geometry: GIN](../Research/Geometry.md#gin).

### 14.5 Indexes on `attestation` and `consensus`

- **In:** `attestation` and `consensus`, each range-partitioned 16 ways by the first hex digit of `claim` (`_0`..`_f`) with `fillfactor = 80`.
- **Do:** build primary key `(claim)` on `consensus`, `UNIQUE NULLS NOT DISTINCT (claim, witness, lineage)` on `attestation`, and `attestation_witness_lineage` on `attestation (witness, lineage NULLS FIRST) INCLUDE (trust)` (`laplace_schema_indexes()`).
- **Out:** single-partition point and batch lookups for claim standing and witness series, HOT in-place Glicko-2 updates on `consensus`, and fast per-witness scans for `laplace forget` and Fisher-information royalty attribution (`share_bp = 10000`).
- **From:** [Reference: Schema](../Reference/Schema.md#the-indexes), [Research: Engine Measurements: Consensus writes](../Research/Engine.md#consensus-writes).

### 14.6 Combined claim and occurrence probes (zero side tables)

- **In:** `physicality_paths`, `physicality_assertions`, `consensus`, and `attestation`.
- **Do:** verify that open-slot claim queries (`[dog, eng, ?]`, `[?, language, i46360]`, `[word, NOUN]`) and occurrence/container counts resolve directly by intersecting constituent IDs and `mask` bits in `physicality_paths` and joining `consensus(claim)` / `attestation(claim)`—requiring no separate `claim` or `statistics` table.
- **Out:** `[dog, eng, ?]` and cross-language `[?, language, i46360]` probes in milliseconds from the four core tables alone.
- **From:** [Reference: Schema](../Reference/Schema.md), [Research: Semantics Experiments: Translation through the ILI](../Research/Semantics-Experiments.md#translation-through-the-ili).

### 14.7 `ANALYZE`

- **In:** every table.
- **Do:** run `ANALYZE`, with statistics on the path column at 0, because histograms of packed IDs mean nothing.
- **From:** [Database: Planning](../Operations/Database.md#planning).

### 14.8 Measure every native operation

- **In:** the library of [3. Builds](Builds.md).
- **Do:** run the benchmark: every operation with each SIMD kernel beside its scalar form.
- **Out:** this machine's rates, to compare with the reference machine's: wall check 296 M/s; exact centroid 211 M points/s; ID into and out of the mantissas 104 M/s; 4D Hilbert value 12 M/s; codepoint ID 8–12 M/s; Glicko-2 matchup 7.8 M/s; vertex scan 14.2 GB/s scalar and 15.0 GB/s AVX2; 4D squared distances 1.1 G/s scalar and 1.4 G/s AVX2; discrete Fréchet on 1,000 × 1,000 vertices 3.8 ms.
- **From:** [Deployment](../Operations/Deployment.md), [Research: Engine Measurements: Native operations](../Research/Engine.md#native-operations).

### 14.9 Measure every query

- **In:** the loaded database.
- **Do:** run each query cold and warm, and report execution and round-trip time, buffers read and hit, and the partitions the plan touched.
- **Out:** this install's numbers beside the reference: an entity by `(tier, id)` 0.02 ms in 1 tier partition; by `id` across the 9 tier partitions <0.1 ms; every container of `Holmes` (`tier > word.tier`) pruning lower/equal tiers in <1 ms; the run `Sherlock Holmes` 1.76 ms; what fills `[Captain, ' ', ?]` 9.2 ms; what follows "the capital of " 24.7 ms; the 16 nearest `king` in 4D 7.7 ms. Lookups on `consensus` and `attestation` prune to 1 of 16 hex partitions by `claim`; upward containment queries on `physicality` prune to strictly higher tier partitions.
- **From:** [Deployment](../Operations/Deployment.md), [Research: Engine Measurements: Queries](../Research/Engine.md#queries).

### 14.10 Check the install against itself

- **In:** the loaded database.
- **Do:** run the checks against the database itself.
- **From:** [Research: Prototype: Verification](../Research/Prototype.md#verification), [Ingestion: Deduplication](../Storage/Ingestion.md#deduplication).

### 14.11 Confirm the fingerprints

- **In:** the fingerprints of [3. Builds](Builds.md) operation 3.8 and [5. Tier 0](Tier-0.md) operation 5.7.
- **Do:** the database reports whether its tier 0 is this engine's. Two installs with the same fingerprint produce the same coordinates for the same content.
- **Out:** an install that knows which build and which tier 0 it has.
- **From:** [Atoms: Generation](../Storage/Atoms.md#generation); `docs/OPERATING_SEQUENCE.md` §6.

### 14.12 Publish the hot cache generations

- **In:** the loaded database and the roster of [7. Perfcaches](Perfcaches.md).
- **Do:** from the canonical rows, emit the admitted and hot ROMs that depend on content: the pixel, patch, region, and image generations, the audio generations, the chess position and transition floors, the factor ROM, and the generation-corpus ROM, each binding the generations it depends on, published by write-to-temporary, checksum, and atomic replace, one way, never seeding the database back. A record present in a cache is thereafter a bounded lookup at [11. Content](Content.md) operation 11.8 and at [19. Pull](Pull.md).
- **Out:** the higher cache generations of this install.
- **From:** `docs/specs/33_Perfcache_Blob_Law.md` §Roster; [7. Perfcaches](Perfcaches.md) operations 7.5 to 7.7.

## What this stage leaves behind

O(log N) lookups, and the numbers and checks that say whether this install matches the fingerprint and the measurements.

## Without this stage

Every lookup is a scan, no step of the forward pass is O(log N) + O(K), and nothing says whether the install is right.
