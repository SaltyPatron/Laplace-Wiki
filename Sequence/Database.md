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
- **Mechanism:** done by the operator with `initdb` and tablespaces; no Laplace program does it. Status: **operator**.
- **From:** [Setup: Storage](../Operations/Setup.md#storage).

### 8.2 Set memory

- **In:** the machine's RAM.
- **Do:** with `ALTER SYSTEM`; settings marked *restart* take effect when the server restarts. `shared_buffers` about a quarter of RAM, sized to fit the reserved huge pages, *restart*; `huge_pages` to `try`, then check `huge_pages_status` is `on`, because another process using huge pages can take them and the server silently falls back; `effective_cache_size` to the memory the page cache can use; `work_mem` generous, because Laplace runs few, heavy sessions; `maintenance_work_mem` large, because GIN index builds use it all. `SHOW shared_memory_size_in_huge_pages` gives the number of huge pages the server needs. Reference values: 31 GB on 16,744 huge pages of 2 MB, 88 GB, 256 MB, 8 GB.
- **Out:** the memory settings.
- **Mechanism:** done by the operator with `ALTER SYSTEM` ([Environment: Database settings the engine sets](../Reference/Environment.md#database-settings-the-engine-sets), last paragraph). Status: **operator**.
- **From:** [Database: Memory](../Operations/Database.md#memory).

### 8.3 Set I/O

- **In:** the drives and the kernel.
- **Do:** `io_method` to `worker` unless `io_uring` passes a cold-read stress test on the running kernel, *restart*; `io_workers` about two thirds of the cores; `effective_io_concurrency` and `maintenance_io_concurrency` high on SSDs; `random_page_cost` 1.1 on SSDs; `default_toast_compression` `lz4`, because long paths are compressed and decompressed often. The stress test drops the operating system's page cache and PostgreSQL's buffers before every round, so that every read goes to disk, then runs a parallel index build and a parallel scan.
- **Out:** the I/O settings.
- **Check:** on Linux 5.15, `io_uring` failed 1 of 12 parallel index builds with "could not read blocks: Operation canceled", while `worker` failed none and ran 5–10% faster. `ALTER SYSTEM` rejects values the running binary does not know, such as `io_uring` before a server built with liburing runs.
- **Mechanism:** done by the operator with `ALTER SYSTEM`. Status: **operator**.
- **From:** [Database: I/O](../Operations/Database.md#io), [Research: Engine Measurements: Server settings](../Research/Engine.md#server-settings).

### 8.4 Set the write-ahead log

- **In:** the WAL drive.
- **Do:** `max_wal_size` and `min_wal_size` large, so bulk loads do not force checkpoints, 32 GB and 4 GB on the reference machine; `wal_buffers` 64 MB, *restart*; `wal_compression` `zstd`; `checkpoint_timeout` 30 min. Bulk ingestion sessions set `synchronous_commit = off`.
- **Out:** the WAL settings.
- **Mechanism:** done by the operator with `ALTER SYSTEM`; `laplace ingest` sets `synchronous_commit = off` on every load connection ([Environment: Database settings the engine sets](../Reference/Environment.md#database-settings-the-engine-sets)). Status: **operator; `synchronous_commit` built**.
- **From:** [Database: Write-ahead log](../Operations/Database.md#write-ahead-log).

### 8.5 Set observability

- **In:** the contrib modules built in [3. Builds](Builds.md).
- **Do:** `shared_preload_libraries` to `pg_stat_statements, auto_explain` as an unquoted list, *restart*, because a quoted `'a,b'` is stored as one library named `a,b` and the server then does not start; `pg_stat_statements.track` `all`; `auto_explain.log_min_duration` 5 s; `track_io_timing` and `track_wal_io_timing` on.
- **Out:** every statement's cost and every slow plan, recorded.
- **Mechanism:** done by the operator with `ALTER SYSTEM`; `laplace deploy` creates `pg_stat_statements` and `pg_buffercache` ([CLI: laplace deploy](../Reference/CLI.md#laplace-deploy)). Status: **operator**.
- **From:** [Database: Observability](../Operations/Database.md#observability).

### 8.6 Restart, and check the huge pages

- **In:** the settings of 8.2 to 8.5.
- **Do:** restart the server through a logged root script.
- **Check:** `huge_pages_status` is `on`.
- **Mechanism:** done by the operator. Status: **operator**.
- **From:** [Database: Memory](../Operations/Database.md#memory), [Setup: Toolchain](../Operations/Setup.md#toolchain).

### 8.7 Create the role, the database, and the extensions

- **In:** the running server.
- **Do:** `CREATE ROLE laplace LOGIN SUPERUSER`; `CREATE DATABASE laplace OWNER laplace`; then in it `CREATE EXTENSION postgis`, `CREATE EXTENSION laplace`, `CREATE EXTENSION pg_stat_statements`, `CREATE EXTENSION pg_buffercache`. The Laplace content database holds entities, physicalities, and sources; operational data such as logs, authentication, and billing stays conventional, in a separate database.
- **Out:** the Laplace database with its four extensions.
- **Mechanism:** `laplace deploy`: the database if the server lacks it, then `CREATE EXTENSION IF NOT EXISTS` for `postgis`, `laplace`, `pg_stat_statements`, `pg_buffercache` ([CLI: laplace deploy](../Reference/CLI.md#laplace-deploy), [Schema: Extension control](../Reference/Schema.md#extension-control)); the role is the operator's. Status: **built**.
- **From:** [Deployment](../Operations/Deployment.md), [Architecture: Databases](../Architecture.md#databases).

### 8.8 Tell the database its tier 0

- **In:** the tier-0 file and its fingerprint from [5. Tier 0](Tier-0.md).
- **Do:** set the extension's setting to the path of the tier-0 perf-cache, the setting for the flags that go with it, and the settings for each other ROM the database serves, the vocabulary and the chess floors. Each backend memory-maps it on first use. The perf-cache is thereby available inside the database as native functions, so queries can compute IDs and coordinates in place instead of scanning tables; such a function is evaluated once when the query is planned, and the query becomes an index lookup on the result.
- **Out:** a database that computes the same IDs and coordinates the client does.
- **Check:** the database reports the same fingerprint as the engine's tier 0.
- **Mechanism:** `laplace deploy`: `ALTER DATABASE … SET laplace.tier0` and `laplace.flags` ([Environment: Database settings the engine sets](../Reference/Environment.md#database-settings-the-engine-sets)); the functions of [SQL: Tier 0 in place](../Reference/SQL.md#tier-0-in-place) compute over the mapping. Status: **built; settings for other ROMs specified**.
- **From:** [Deployment](../Operations/Deployment.md), [Query: Functions in queries](../Query.md#functions-in-queries), [Atoms: Generation](../Storage/Atoms.md#generation).

### 8.9 Make the content schema

- **In:** the database of 8.7.
- **Do:** every entity is its own record, with its ID as the key and its real coordinate as a normal POINT ZM with M as the fourth coordinate, its tier as a query aid, and its Hilbert value. Every entity also has a physicality, related to it by foreign key, holding the path geometry ZM. A source records its trunk, origin, format, size, content hash, and normalization form. Statistics hold each entity's containers and occurrences. The few text columns, such as a source's origin, use UTF-8 with a deterministic, operating-system-independent collation.
- **Out:** the entity, physicality, source, and statistics tables. Four families persist the world: entities, canonical identity; physicalities, typed realization with coordinate, Hilbert address, and packed trajectory; attestations, source-attributed typed testimony; consensus, folded standing. Identity, physicality, occurrence, testimony, consensus, and calculation never collapse into one another, and the inventor's list of core tables is entity, physicality, attestation, consensus, witness, with no fake lookup tables beside them, [30. Conflicts](Conflicts.md) T1.
- **Mechanism:** `schema.sql`: `entity (id, tier, coord, hilbert)` and `physicality (entity, tier, hilbert, path)` ([Schema: Content](../Reference/Schema.md#content-schemasql)). No `source` table and no statistics table: a file is a trunk in the DAG and occurrences are computed at read time ([Schema: What the prototype had](../Reference/Schema.md#what-the-prototype-had)). Status: **built**.
- **From:** [Physicality: Entity and physicality](../Storage/Physicality.md#entity-and-physicality), [Physicality: Real coordinates](../Storage/Physicality.md#real-coordinates), [Architecture: Databases](../Architecture.md#databases), [Research: Prototype: Store](../Research/Prototype.md#store).

### 8.10 Partition it

- **In:** the tables of 8.9.
- **Do:** list-partition entities, paths, and statistics by tier. Split the largest tiers again into 16 partitions by the first hex digit of their ID. Partitions go by the ID hash, not by Hilbert value: remember the 4-ball against the 4-box.
- **Out:** partitions that stay equal and prune to one on a lookup by ID.
- **Check:** Hilbert ranges failed: with word segments and sentences each split into 8 equal Hilbert ranges of the 4-cube, all 765,412 word segments and all 1,678,740 sentences landed in the first range, because English text lies in one small region of the 4-ball and Hilbert ranges divide the 4-cube around it. ID prefixes worked: by first hex digit, the word segments fell 47,628 to 47,964 per partition. An ID is a hash, so any content divides evenly.
- **Mechanism:** the `DO` block of `schema.sql`: list by tier for 0 to 15, tiers 0, 2, 3, 4, 5, 6 range-split sixteen ways by the first hex digit, `entity_tx` and `physicality_tx` the defaults ([Schema: Content](../Reference/Schema.md#content-schemasql)); the engine reads the split from `pg_class` at every load. Status: **built**.
- **From:** [Physicality: Partitions](../Storage/Physicality.md#partitions), [Deployment](../Operations/Deployment.md), [Research: Engine Measurements: Partitions](../Research/Engine.md#partitions).

### 8.11 Make the semantics schema

- **In:** the database of 8.7.
- **Do:** the tables for witnesses, claims, attestations, and consensus, filled in [12. Attestations](Attestations.md) and [13. Consensus](Consensus.md): a claim as a tuple of entity IDs with its own ID hashed like a composition's; the bitmask columns, such as 256-bit masks, that denote which part of speech, sense, dependency relation, and so on apply; the ledger of attestations, each with its witness, lineage, and outcome; and the standing, one row per claim, with rating, deviation, and volatility. Consensus is the standing updated in place, not an aggregate over the ledger: reading the hottest claim's standing took 0.1 ms against 115 ms to aggregate its 474,628 ledger rows.
- **Out:** the semantics tables, empty.
- **Mechanism:** `semantics.sql`: `witness`, `attestation`, `consensus` ([Schema: Semantics](../Reference/Schema.md#semantics-semanticssql)). A claim is no row: it is a composition in `entity` and `physicality`. No mask columns. Status: **built; the masks specified**.
- **From:** [Claims: IDs](../Semantics/Claims.md#ids), [Claims: Masks](../Semantics/Claims.md#masks), [Consensus](../Semantics/Consensus.md), [Research: Engine Measurements: Consensus writes](../Research/Engine.md#consensus-writes).

### 8.12 Apply the planning settings

- **In:** the schema of 8.9 to 8.11.
- **Do:** PostgreSQL and PostGIS assume that a geometry's coordinates are positions and that a function in an index is cheap. A Laplace path's coordinates are packed IDs, and its index key decodes a whole trajectory, so the defaults misjudge both. Set the cost of the function that decodes a path's IDs to 10,000; statistics on the path column to 0; `enable_parallel_append` off in the Laplace database; `parallel_workers` on physicality partitions to 0; `jit` off; `max_parallel_maintenance_workers` about half the cores. An analytic session can turn parallelism back on for itself.
- **Out:** a planner that chooses the index.
- **Check:** at lower costs the planner scans the partition of whole books and decodes every one on every lookup, 90 ms of a 111 ms query. `ANALYZE` took 332 s with histograms of packed IDs and 2.5 s without. Starting parallel workers takes about 15 ms; a container lookup takes 1 ms.
- **Mechanism:** `schema.sql`: statistics 0 on `path`, `parallel_workers = 0` on every `physicality_t*`, `enable_parallel_append = off`; `laplace_vertex_ids` at `COST 10000` in `laplace--1.0.sql` ([SQL: Paths](../Reference/SQL.md#paths)); `indexes.sql` sets `maintenance_work_mem` and `max_parallel_maintenance_workers` for its session ([Environment: Database settings the engine sets](../Reference/Environment.md#database-settings-the-engine-sets)); `jit` is the operator's. Status: **built**.
- **From:** [Database: Planning](../Operations/Database.md#planning), [Research: Engine Measurements: Server settings](../Research/Engine.md#server-settings).

## What this stage leaves behind

A tuned server, a database that knows its tier 0 and computes IDs in place, the content tables partitioned by tier and by ID hash, the semantics tables, and a planner that knows what the columns really are.

## Without this stage

There is nowhere to record a composition, the database cannot compute an ID in place, and no index has a table to sit on.
