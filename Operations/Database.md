# Database

PostgreSQL's defaults suit small general-purpose servers; Laplace tunes memory, I/O, and planning to its hardware and to the way it uses geometry and indexes.

Settings are made with `ALTER SYSTEM`; those marked *restart* take effect when the server restarts. The values in the examples are the reference machine's, with 125 GB of RAM, 12 threads, and an NVMe heap.

## Memory

| Setting | Rule | Example |
| --- | --- | --- |
| `shared_buffers` | about a quarter of RAM, sized to fit the reserved huge pages; *restart* | 31 GB on 16,744 huge pages of 2 MB |
| `huge_pages` | `try`, then check `huge_pages_status` is `on`. Another process using huge pages can take them, and the server silently falls back. | |
| `effective_cache_size` | the memory the page cache can use | 88 GB |
| `work_mem` | generous: Laplace runs few, heavy sessions | 256 MB |
| `maintenance_work_mem` | large: GIN index builds use it all | 8 GB |

`SHOW shared_memory_size_in_huge_pages` gives the number of huge pages the server needs.

## I/O

| Setting | Rule | Example |
| --- | --- | --- |
| `io_method` | `worker`, unless `io_uring` passes a cold-read stress test on the running kernel; *restart* | `worker` |
| `io_workers` | about two thirds of the cores | 8 |
| `effective_io_concurrency`, `maintenance_io_concurrency` | high on SSDs | 256 |
| `random_page_cost` | 1.1 on SSDs | |
| `default_toast_compression` | `lz4`: long paths are compressed and decompressed often | |

The stress test drops the operating system's page cache and PostgreSQL's buffers before every round, so that every read goes to disk. Each round then runs a parallel index build and a parallel scan. On Linux 5.15, `io_uring` failed 1 of 12 parallel index builds with "could not read blocks: Operation canceled", while `worker` failed none and ran 5–10% faster.

## Write-ahead log

| Setting | Rule | Example |
| --- | --- | --- |
| `max_wal_size` / `min_wal_size` | large, so bulk loads do not force checkpoints | 32 GB / 4 GB |
| `wal_buffers` | *restart* | 64 MB |
| `wal_compression` | `zstd` | |
| `checkpoint_timeout` | 30 min | |

Bulk ingestion sessions set `synchronous_commit = off`.

A batch's witnesses, ledger and standings are one transaction written in parts, one a connection, a partition at a time on every connection, and committed together by two-phase commit: every part is prepared, the part that holds the witnesses and the files' trunks last; that part is committed first, and its commit decides the rest. A part left prepared by a load that stopped is committed or rolled back by the next load, as its batch's first part was.

| Setting | Rule | Example |
| --- | --- | --- |
| `max_prepared_transactions` | at least the 16 parts a batch is written in; *restart* | 32 |

## Planning

PostgreSQL and PostGIS assume that a geometry's coordinates are positions and that a function in an index is cheap. A Laplace path's coordinates are packed IDs, and its index key decodes a whole trajectory, so the defaults misjudge both:

| Setting | Value | Why |
| --- | --- | --- |
| Cost of `laplace_vertex_ids` | 10,000 | At lower costs the planner scans the partition of whole books and decodes every one on every lookup. |
| Statistics on `physicality.path` | 0 | Histograms of packed IDs mean nothing: `ANALYZE` took 332 s with them and 2.5 s without. |
| `enable_parallel_append` in the Laplace database | off | Starting parallel workers takes about 15 ms; a container lookup takes 1 ms. |
| `parallel_workers` on physicality partitions | 0 | the same |
| `jit` | off | Compiling a short lookup costs more than it saves. |
| `max_parallel_maintenance_workers` | about half the cores | Index builds, including GIN, run in parallel. |

An analytic session can turn parallelism back on for itself.

## Observability

| Setting | Value |
| --- | --- |
| `shared_preload_libraries` | `pg_stat_statements, auto_explain`; *restart* |
| `pg_stat_statements.track` | `all` |
| `auto_explain.log_min_duration` | 5 s |
| `track_io_timing`, `track_wal_io_timing` | on |

`ALTER SYSTEM SET shared_preload_libraries` takes an unquoted list. A quoted `'a,b'` is stored as one library named `a,b`, and the server then does not start. `ALTER SYSTEM` also rejects values the running binary does not know, such as `io_uring` before a server built with liburing runs.
