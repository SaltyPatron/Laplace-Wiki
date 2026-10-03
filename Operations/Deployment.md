# Deployment

A Laplace database is made, empty, by `deploy.sh` and filled by `ingest.sh`, both run by the role and never by root: the build and the perf-caches, the database with its extensions, schema and indexes, then the sources in order, measured as they go in.

1. **Deploy:** `./deploy.sh` (Laplace-Operations), on a push by the Operations workflow, or by hand.
   - The build (`build.sh install`); tier 0 and its flags when missing; the highway, always, its slots frozen by Laplace-Native's manifest; the grammars when `$LAPLACE_GRAMMARS` is empty.
   - `laplace deploy`: the database when missing, the extensions `postgis`, `laplace`, `pg_stat_statements` and `pg_buffercache`, `ALTER EXTENSION laplace UPDATE`, the settings `laplace.tier0`, `laplace.flags` and `laplace.highway` (each backend memory-maps the perf-caches on first use), the schema and every index (`CREATE EXTENSION laplace` and `laplace_schema_indexes()`), and the highway's own records.
   - `laplace status`.
   - It holds a lock per database and leaves while an ingest of it runs. `./deploy.sh drop` drops the database first, through the role, and deploys it again, empty; the workflow does that when dispatched with `drop`.

2. **Schema:** made by `CREATE EXTENSION laplace` itself (Laplace-postgres's install script).
   - Entities and paths are list-partitioned by tier; the largest tiers are split again into 16 partitions by the first hex digit of their ID. An ID is a hash, so the partitions stay equal, and a lookup by ID prunes to one partition.
   - Attestations and standings are partitioned 16 ways by the claim's ID.
   - The schema also applies the planning settings for paths from [Database](Database.md#planning).

3. **Ingest:** `./ingest.sh [source...]`, or the `Laplace-Ingest` workflow (dispatched, with the sources as its input).
   - `laplace ingest` takes the sources named, or every source in `recipes/order`; what is recorded is passed over by its trunk.
   - While it runs, the write-ahead log it makes is read each minute (`pg_walinspect`) and summed by table and index.
   - Then `laplace status` and `laplace bench`. Each step's output is kept under `$LAPLACE_WORK/logs/ingest-runs/<time>`.

4. **Indexes:** `laplace deploy` makes them before any load; `laplace index` makes one again if it was dropped. The container index's pending list is merged once at the end of each source.
   - IDs: B-tree.
   - Hilbert values: B-tree.
   - Real coordinates: 4D GiST.
   - IDs decoded from paths: GIN, which finds containers.
   - Attestations by claim and by witness: B-tree.

5. **Measurement:**
   - `laplace bench` measures every native operation.
   - `bench/bench_queries.py` in Laplace-postgres runs each query cold and warm, and reports execution and round-trip time, buffers read and hit, and the partitions the plan touched. No script or workflow runs it.
