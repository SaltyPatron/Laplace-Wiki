# Database

PostgreSQL's defaults suit small general-purpose servers; Laplace tunes memory, I/O, and planning to its hardware and to the way it uses geometry and indexes.

`sudo ./setup.sh settings` makes every setting here with `ALTER SYSTEM`, from the declaration at the top of `setup.sh`, and restarts the server itself when one marked *restart* changed; while an ingest is running, the restart waits for the next run of `setup.sh`. The values in the examples are the reference machine's, with 125 GB of RAM, 12 threads, and an NVMe heap.

## Memory

| Setting | Rule | Example |
| --- | --- | --- |
| `shared_buffers` | about a quarter of RAM, sized to fit the reserved huge pages; *restart* | 31 GB on 16,744 huge pages of 2 MB |
| `huge_pages` | `try`, then check `huge_pages_status` is `on`. Another process using huge pages can take them, and the server silently falls back. | |
| `effective_cache_size` | the memory the page cache can use | 88 GB |
| `work_mem` | generous: Laplace runs few, heavy sessions | 256 MB |
| `maintenance_work_mem` | large: GIN index builds use it all | 8 GB |

`SHOW shared_memory_size_in_huge_pages` gives the number of huge pages the server needs. `setup.sh` (part `kernel`) writes `vm.nr_hugepages` to `/etc/sysctl.d/60-laplace.conf`: that need, or the declared buffers' if larger, and 3% over.

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
| `max_wal_size` / `min_wal_size` | three eighths of the log's volume, read from the volume (setup.sh): the log runs past it under load while a checkpoint catches up, and a checkpoint a whole cycle late still leaves a quarter free. At 64 GB on a 64 GB volume it filled the volume and stopped the server. `max_slot_wal_keep_size` is held to the same bound | 24 GB / 4 GB |
| `wal_buffers` | large enough that a bulk load's backends do not fill it; *restart* | 256 MB |
| `wal_compression` | `zstd`: a load's log is mostly full-page images of random-key indexes. **Measured** on 23,450 of ConceptNet's B-tree images: 3,781 bytes a page against lz4's 4,711 (-20%), at 57 µs a page against 17, about a quarter of one core at 6,500 images a second | |
| `checkpoint_timeout` | 60 min | |
| `checkpoint_completion_target` | 0.9 | |
| `bgwriter_lru_maxpages` | high, so the background writer cleans buffers before backends must | 1000 |

Every page a checkpoint has not yet seen modified goes into the log whole the first time it changes (a full-page image), and each is compressed by the backend that writes it. **Measured** over the first four hours of a full ingest at 32 GB, 30 min and `zstd`: 273 GB of log, 999,307,239 records, 47,175,989 full-page images (about 377 GB before compression), and the log's buffers full 2,616,329 times; client backends wrote 10,051,406 relation pages themselves. Fewer checkpoints mean fewer full-page images, and larger buffers keep backends from writing the log themselves. That run used `max_wal_size` 32 GB and a 30-minute `checkpoint_timeout`; the settings are now the table's.

Bulk ingestion sessions set `synchronous_commit = off`.

A batch's witnesses, attestations and standings are one transaction written in parts, one a connection, a partition at a time on every connection, and committed together by two-phase commit: every part is prepared, the part that holds the witnesses and the files' trunks last; that part is committed first, and its commit decides the rest. A part left prepared by a load that stopped is committed or rolled back by the next load, as its batch's first part was.

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
| `gin_pending_list_limit` on the container index (each partition) | 256 MB | A load's entries go into the pending list in order and are merged once, when the source is in. At the default 4 MB the list merged every few thousand paths into random pages of the index, each written into the log whole: **measured** 4.05 GB of full-page images per GB of paths loaded, and 1.02 GB at 256 MB. |
| `jit` | off | Compiling a short lookup costs more than it saves. |
| `max_parallel_maintenance_workers` | about half the cores | Index builds, including GIN, run in parallel. |
| `max_worker_processes`, `max_parallel_workers`, `max_parallel_workers_per_gather` | the cores and four; the cores; half the cores | |
| `temp_tablespaces` | `pgtemp`, on its own volume | |

An analytic session can turn parallelism back on for itself.

## Observability

| Setting | Value |
| --- | --- |
| `shared_preload_libraries` | `pg_stat_statements, auto_explain`; *restart* |
| `pg_stat_statements.track` | `all` |
| `auto_explain.log_min_duration` | 5 s |
| `track_io_timing`, `track_wal_io_timing` | on |

`ALTER SYSTEM SET shared_preload_libraries` takes an unquoted list. A quoted `'a,b'` is stored as one library named `a,b`, and the server then does not start. `ALTER SYSTEM` also rejects values the running binary does not know, such as `io_uring` before a server built with liburing runs.

## Access

`setup.sh` (part `access`) writes the whole of `pg_hba.conf`, never a line added to what is there, and listens on every address with `ssl` on, `port` 5432, and `max_connections` 100:

| Who | How |
| --- | --- |
| `postgres` over the socket | peer |
| `laplace` over the socket | peer, through the map `laplace`: the members of the shared group, the runners' user, the server's user |
| `laplace` and `postgres` from this host | scram-sha-256 |
| `laplace` and `postgres` from `$LAPLACE_LAN` | scram-sha-256 over TLS only |
| anything else without TLS | rejected |

The role `laplace` is made `LOGIN SUPERUSER`; its password is kept in `/etc/laplace/pgpass` and copied into each operator's `~/.pgpass`, and set again on a cluster made again after `drop`. The firewall allows the port from `$LAPLACE_LAN`.
