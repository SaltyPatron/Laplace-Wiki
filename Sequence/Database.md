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
- **Do:** `CREATE ROLE laplace LOGIN SUPERUSER`; `CREATE DATABASE laplace OWNER laplace`; then in it `CREATE EXTENSION postgis`, `CREATE EXTENSION laplace`, `CREATE EXTENSION pg_stat_statements`, `CREATE EXTENSION pg_buffercache`. The Laplace content database holds entities, physicalities, and sources; operational data such as logs, authentication, and billing stays conventional, in a separate database.
- **Out:** the Laplace database with its four extensions.
- **From:** [Deployment](../Operations/Deployment.md), [Architecture: Databases](../Architecture.md#databases).

### 8.8 Tell the database its tier 0

- **In:** the tier-0 file and its fingerprint from [5. Tier 0](Tier-0.md).
- **Do:** set the extension's setting to the path of the tier-0 perf-cache, the setting for the flags that go with it, and the settings for each other ROM the database serves, the vocabulary and the chess floors. Each backend memory-maps it on first use. The perf-cache is thereby available inside the database as native functions, so queries can compute IDs and coordinates in place instead of scanning tables; such a function is evaluated once when the query is planned, and the query becomes an index lookup on the result.
- **Out:** a database that computes the same IDs and coordinates the client does.
- **From:** [Deployment](../Operations/Deployment.md), [Query: Functions in queries](../Query.md#functions-in-queries), [Atoms: Generation](../Storage/Atoms.md#generation).

### 8.9 Make the content schema

- **In:** the database of 8.7.
- **Do:** every entity is its own record, with its ID as the key and its real coordinate as a normal POINT ZM with M as the fourth coordinate, its tier as a query aid, and its Hilbert value. Every entity also has a physicality, related to it by foreign key, holding the path geometry ZM. A source records its trunk, origin, format, size, content hash, and normalization form. Statistics hold each entity's containers and occurrences. The few text columns, such as a source's origin, use UTF-8 with a deterministic, operating-system-independent collation.
- **Out:** the entity, physicality, source, and statistics tables. Four families persist the world: entities, canonical identity; physicalities, typed realization with coordinate, Hilbert address, and packed trajectory; attestations, source-attributed typed testimony; consensus, folded standing. Identity, physicality, occurrence, testimony, consensus, and calculation never collapse into one another, and the inventor's list of core tables is entity, physicality, attestation, consensus, witness, with no fake lookup tables beside them, [30. Conflicts](Conflicts.md) T1.
- **From:** [Physicality: Entity and physicality](../Storage/Physicality.md#entity-and-physicality), [Physicality: Real coordinates](../Storage/Physicality.md#real-coordinates), [Architecture: Databases](../Architecture.md#databases), [Research: Prototype: Store](../Research/Prototype.md#store).

### 8.10 Partition it

- **In:** the tables of 8.9.
- **Do:** list-partition entities, paths, and statistics by tier. Split the largest tiers again into 16 partitions by the first hex digit of their ID. Partitions go by the ID hash, not by Hilbert value: remember the 4-ball against the 4-box.
- **Out:** partitions that stay equal and prune to one on a lookup by ID.
- **From:** [Physicality: Partitions](../Storage/Physicality.md#partitions), [Deployment](../Operations/Deployment.md), [Research: Engine Measurements: Partitions](../Research/Engine.md#partitions).

### 8.11 Make the semantics schema

- **In:** the database of 8.7.
- **Do:** the tables for claims and their standing, filled in [12. Attestations](Attestations.md) and [13. Consensus](Consensus.md): a claim as a tuple of entity IDs with its own ID hashed like a composition's; the bitmask columns, such as 256-bit masks, that denote which part of speech, sense, dependency relation, and so on apply; provenance, an `attestation` table with a row per claim and witness, its outcome, score, games, and position, and the qualifier mask of [12. Attestations](Attestations.md) operation 12.7, beside a `witness` table; trust and lineage keyed by the trunk ID; and the standing, one metadata table keyed by the strand ID with rating, deviation, and volatility, beside the path and never on the GIN-indexed path row, where a non-HOT update would re-insert GIN entries for every vertex. The target is provenance by containment, each record a path over the claims it asserts inside its file's content tree under the source trunk, which is the witness, with the outcome in each vertex's M, so a claim's witnesses are the trunks that hold it, found through the GIN; the per-claim-and-witness attestation table stayed until a working prototype on real data showed that containment answers everything the table answered, who said a claim, its games, score, and position, its qualifiers, forgetting and replay, with nothing lost, and is retired (Laplace-Engine#47). Consensus is the standing updated in place, not an aggregate over the attestations: reading the hottest claim's standing took 0.1 ms against 115 ms to aggregate its 474,628 attestations.
- **Out:** the semantics tables, empty.
- **From:** [Claims: IDs](../Semantics/Claims.md#ids), [Claims: Masks](../Semantics/Claims.md#masks), [Consensus](../Semantics/Consensus.md), [Research: Engine Measurements: Consensus writes](../Research/Engine.md#consensus-writes).

### 8.12 Apply the planning settings

- **In:** the schema of 8.9 to 8.11.
- **Do:** PostgreSQL and PostGIS assume that a geometry's coordinates are positions and that a function in an index is cheap. A Laplace path's coordinates are packed IDs, and its index key decodes a whole trajectory, so the defaults misjudge both. Set the cost of the function that decodes a path's IDs to 10,000; statistics on the path column to 0; `enable_parallel_append` off in the Laplace database; `parallel_workers` on physicality partitions to 0; `jit` off; `max_parallel_maintenance_workers` about half the cores. An analytic session can turn parallelism back on for itself.
- **Out:** a planner that chooses the index.
- **From:** [Database: Planning](../Operations/Database.md#planning), [Research: Engine Measurements: Server settings](../Research/Engine.md#server-settings).

## What this stage leaves behind

A tuned server, a database that knows its tier 0 and computes IDs in place, the content tables partitioned by tier and by ID hash, the semantics tables, and a planner that knows what the columns really are.

## Without this stage

There is nowhere to record a composition, the database cannot compute an ID in place, and no index has a table to sit on.
