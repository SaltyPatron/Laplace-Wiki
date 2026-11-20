# 8. Database

The server is tuned, the extensions are created, the database is told its tier 0, and the partitioned content and semantics schema is made.

PostgreSQL's defaults suit small general-purpose servers; Laplace tunes memory, I/O, and planning to its hardware and to the way it uses geometry and indexes. A Laplace database goes from empty to benchmarked in five steps: extensions, schema, ingestion, indexes, and measurement. This stage is the server and the first two steps.

## Before this stage

[3. Builds](Builds.md): the server, PostGIS, and the extension. [5. Tier 0](Tier-0.md): the file the extension maps. [2. Toolchain](Toolchain.md): the drives.

## Operations

### 8.1 Initialize the cluster on the drives

- **In:** the drive layout of [2. Toolchain](Toolchain.md) operation 2.2.
- **Do:** the heap and indexes on the NVMe; the write-ahead log on its own SSD; a tablespace for temporary files on another SSD.
- **Out:** a cluster whose random reads, sequential writes, and spills do not compete.
- **From:** [Setup: Storage](../Operations/Setup.md#storage).

### 8.2 Set memory

- **In:** the machine's RAM.
- **Do:** with `ALTER SYSTEM`; settings marked *restart* take effect when the server restarts. `shared_buffers` about a quarter of RAM, sized to fit the reserved huge pages, *restart*; `huge_pages` to `try`, then check `huge_pages_status` is `on`, because another process using huge pages can take them and the server silently falls back; `effective_cache_size` to the memory the page cache can use; `work_mem` generous, because Laplace runs few, heavy sessions; `maintenance_work_mem` large, because GIN index builds use it all. `SHOW shared_memory_size_in_huge_pages` gives the number of huge pages the server needs. Reference values: 31 GB on 16,744 huge pages of 2 MB, 88 GB, 256 MB, 8 GB.
- **Out:** the memory settings.
- **From:** [Database: Memory](../Operations/Database.md#memory).

### 8.3 Set I/O

- **In:** the drives and the kernel.
- **Do:** `io_method` to `worker` unless `io_uring` passes a cold-read stress test on the running kernel, *restart*; `io_workers` about two thirds of the cores; `effective_io_concurrency` and `maintenance_io_concurrency` high on SSDs; `random_page_cost` 1.1 on SSDs; `default_toast_compression` `lz4`, because long paths are compressed and decompressed often. The stress test drops the operating system's page cache and PostgreSQL's buffers before every round, so that every read goes to disk, then runs a parallel index build and a parallel scan.
- **Out:** the I/O settings.
- **From:** [Database: I/O](../Operations/Database.md#io), [Research: Engine Measurements: Server settings](../Research/Engine.md#server-settings).

### 8.4 Set the write-ahead log

- **In:** the WAL drive.
- **Do:** `max_wal_size` and `min_wal_size` large, so bulk loads do not force checkpoints, 32 GB and 4 GB on the reference machine; `wal_buffers` 64 MB, *restart*; `wal_compression` `zstd`; `checkpoint_timeout` 30 min. Bulk ingestion sessions set `synchronous_commit = off`.
- **Out:** the WAL settings.
- **From:** [Database: Write-ahead log](../Operations/Database.md#write-ahead-log).

### 8.5 Set observability

- **In:** the contrib modules built in [3. Builds](Builds.md).
- **Do:** `shared_preload_libraries` to `pg_stat_statements, auto_explain` as an unquoted list, *restart*, because a quoted `'a,b'` is stored as one library named `a,b` and the server then does not start; `pg_stat_statements.track` `all`; `auto_explain.log_min_duration` 5 s; `track_io_timing` and `track_wal_io_timing` on.
- **Out:** every statement's cost and every slow plan, recorded.
- **From:** [Database: Observability](../Operations/Database.md#observability).

### 8.6 Restart, and check the huge pages

- **In:** the settings of 8.2 to 8.5.
- **Do:** restart the server through a logged root script.
- **From:** [Database: Memory](../Operations/Database.md#memory), [Setup: Toolchain](../Operations/Setup.md#toolchain).

### 8.7 Create the role, the database, and the extensions

- **In:** the running server.
- **Do:** create a dedicated non-superuser owner/runtime role (`laplace` / `laplace-runner`, `LOGIN NOSUPERUSER`; bootstrap superuser privileges are used only where PostgreSQL requires them to install C extensions initially, never by serving runtime connections); `CREATE DATABASE laplace OWNER laplace`; then install `postgis`, `laplace`, `pg_stat_statements`, and `pg_buffercache`. `CREATE EXTENSION laplace` creates the `blake3` type and the four persistent substrate tables. Conventional operational tables—authentication, sessions, compute-envelope reservations, Patreon entitlement state, and `app.billing_royalties` (`SUM(share_bp) = 10000`)—live strictly in the separate `app.*` schema inside the **same** `laplace` PostgreSQL database, keeping the four substrate tables completely clean while enabling single-transaction ACID settlement of compute reservations and Knowledge Seeder royalties ([17. Envelope](Envelope.md) operation 17.7).
- **Out:** the `laplace` database with its extensions, non-superuser runtime role, four substrate tables, and `app.*` operational schema.
- **From:** [Deployment](../Operations/Deployment.md), [Reference: Schema](../Reference/Schema.md), [Architecture: Databases](../Architecture.md#databases).

### 8.8 Tell the database its tier 0, flags, and highway

- **In:** `tier0.bin`, `tier0.flags`, and `highway.bin` with their fingerprints from [5. Tier 0](Tier-0.md) and [7. Perfcaches](Perfcaches.md).
- **Do:** set `laplace.tier0`, `laplace.flags`, `laplace.highway`, and any enabled domain ROM settings (`chess.bin`) to their perf-cache paths. Each backend memory-maps them read-only on first use. The perf-caches are thereby available inside PostgreSQL as `IMMUTABLE` native C functions, so constant ID, coordinate, Hilbert, and mask-bit expressions fold once at plan time and turn into direct index probes, while client processes map the exact same files to run deterministic decomposition and realization in-process with zero database round trips.
- **Out:** a database and client fleet that compute bit-identical IDs, coordinates, and mask descriptors.
- **From:** [Deployment](../Operations/Deployment.md), [Reference: Schema](../Reference/Schema.md), [Query: Functions in queries](../Query.md#functions-in-queries), [Atoms: Generation](../Storage/Atoms.md#generation).

### 8.9 Make the four persistent substrate tables

- **In:** `CREATE EXTENSION laplace` in the database of 8.7.
- **Do:** persist the entire world in exactly **four** substrate tables (`Laplace-postgres/sql/laplace.sql.in`), with zero fake `source`, `witness`, `claim`, or `statistics` lookup tables beside them ([30. Conflicts](Conflicts.md) T1):
  - `entity(id blake3, tier smallint, coord geometry(PointZM), hilbert bigint, mask bit(64))` — canonical identity, compositional tier, real 4D fixed-point coordinate inside the S³ ball, sign-flipped 4D Hilbert key (`h ^ 0x8000000000000000` so signed `bigint` order matches unsigned Hilbert order), and the 64-bit `mask` validated by `laplace_mask_valid` (`manifest/banks.tsv`).
  - `physicality(entity blake3, tier smallint, hilbert bigint, path geometry, mask bit(64))` — foreign key `(tier, entity) → entity(tier, id) ON UPDATE CASCADE`, holding the binary EWKB `POINT ZM` / `LINESTRING ZM` trajectory packing 128-bit constituent IDs (`43/43/42 + 28 spare`) in X/Y/Z and `run30/said3/outcome2/pos18` in M, plus the row's 64-bit `mask` (`CLAIM`, `RECORD`, `TUPLE`, `FILE`, and grammatical/lexical banks). Sources, files, records, collections, and claims are all entities + physicalities; containment and occurrence queries resolve directly from `physicality.path`.
  - `attestation(claim blake3, witness blake3, lineage blake3, games bigint, tokens bigint, score double precision, "position" integer, trust double precision)` — `UNIQUE NULLS NOT DISTINCT (claim, witness, lineage)`, recording each witness trunk's folded game series, empirical token count, score, position, causal lineage, and trust on a claim alongside containment provenance in `physicality.path`.
  - `consensus(claim blake3 PRIMARY KEY, rating double precision, deviation double precision, volatility double precision, matches bigint)` — folded Glicko-2 standing updated in place off the GIN-indexed `physicality` heap so standing updates never trigger GIN re-insertions. Reading a claim's standing takes 0.1 ms versus 115 ms to re-aggregate 474,628 raw attestations on the fly.
- **Out:** `entity`, `physicality`, `attestation`, and `consensus`.
- **From:** [Reference: Schema](../Reference/Schema.md#the-four-tables), [Physicality: Entity and physicality](../Storage/Physicality.md#entity-and-physicality), [Consensus](../Semantics/Consensus.md), [30. Conflicts](Conflicts.md) T1, T2, I3.

### 8.10 Partition by tier on content and by hex prefix on claims

- **In:** the four tables of 8.9.
- **Do:** range-partition `entity` and `physicality` into **9 tier partitions (`t0`..`t8plus`, `RANGE (tier)`)** with primary keys `(tier, id)` and `(tier, entity)` plus per-partition `UNIQUE (id)` / `UNIQUE (entity)`, and range-partition `attestation` and `consensus` **16 ways by the first hex digit of `claim` (`_0`..`_f`, `RANGE (claim)`)** with `fillfactor = 80` ([30. Conflicts](Conflicts.md) P4). Why tier partitioning on `entity` and `physicality`: because every parent composition sits strictly above its constituents (`tier = 1 + max(child.tier)`), upward containment lookups (`tier > child.tier`) prune lower and equal tier partitions immediately instead of fanning across 256 hash partitions on every probe, while Hilbert ordering preserves 4D locality inside each tier. Why 16 hex partitions with `fillfactor = 80` on `attestation` and `consensus`: lookups by `claim` prune to one partition, and in-place Glicko-2 updates find free space on the same heap page (HOT updates).
- **Out:** 9 tier partitions on `entity` and `physicality`, and 16 hex partitions on `attestation` and `consensus`.
- **From:** [Reference: Schema](../Reference/Schema.md#the-four-tables), [30. Conflicts](Conflicts.md) P4.

### 8.11 Register the highway entities and reconcile bindings

- **In:** the partitioned schema of 8.10 and mapped `highway.bin` of 8.8.
- **Do:** `laplace deploy` registers the highway's identifier entities directly from mapped `highway.bin` and restores all replaceable C/SQL routines, casts, operators, and operator classes via `laplace.reconcile.sql`. Because `Laplace-postgres` hashes the persistent storage DDL (`laplace-storage:<16-hex>`) separately from replaceable functions and indexes, code upgrades run `ALTER EXTENSION laplace UPDATE TO ...` in place without dropping loaded data.
- **Out:** the schema reconciled and ready for bulk ingestion or incremental updates.
- **From:** [Reference: Schema](../Reference/Schema.md#versions), [3. Builds](Builds.md) operation 3.4.

### 8.12 Apply the planning settings

- **In:** the schema of 8.9 to 8.11.
- **Do:** PostgreSQL and PostGIS assume that a geometry's coordinates are positions and that a function in an index is cheap. A Laplace path's coordinates are packed IDs, and its index key decodes a whole trajectory, so the defaults misjudge both. Set the cost of the function that decodes a path's IDs to 10,000; statistics on the path column to 0; `enable_parallel_append` off in the Laplace database; `parallel_workers` on physicality partitions to 0; `jit` off; `max_parallel_maintenance_workers` about half the cores. An analytic session can turn parallelism back on for itself.
- **Out:** a planner that chooses the index.
- **From:** [Database: Planning](../Operations/Database.md#planning), [Research: Engine Measurements: Server settings](../Research/Engine.md#server-settings).

## What this stage leaves behind

A tuned server, a database with non-superuser runtime access that maps `tier0.bin`, `tier0.flags`, and `highway.bin`, the four persistent substrate tables (`entity` and `physicality` partitioned by tier, `attestation` and `consensus` partitioned 16 ways by claim ID) alongside `app.*` operational tables in the same database, and a planner that knows what the columns really are.

## Without this stage

There is nowhere to record a composition, the database cannot compute an ID in place, and no index has a table to sit on.
