# Deployment

A Laplace database is created on first install and reconciled in place on existing installs by `deploy.sh` (`laplace.reconcile.sql`) without dropping data, using pre-built `tier0`, `flags`, and `highway` perf-caches, and filled by `ingest.sh`, both run by the role and never by root.

1. **Deploy:** `./deploy.sh` (`Laplace-Operations`, or `pwsh Laplace-Operations/laplace.ps1 deploy` on Windows), on a push by the Operations workflow, or by hand (`./deploy.sh as-is` deploys the local checkouts without fast-forwarding to upstream during unpushed Batch testing).
   - Verifies that pre-built `tier0.bin`, `tier0.flags` (and `.layout`), and `tier0.highway` (`highway.bin`) ROM artifacts are already present on disk or in `$LAPLACE_PREPARED_INPUTS` before touching the database (perf-cache generation is a separate `Laplace-Native` / `laplace tier0|flags|highway` qualification step, never regenerated inline from stale local corpora during deploy); runs `tune-pg.sh`, `build.sh install`, `tools/build_grammars.sh` (incrementally rebuilding changed grammars), and `laplace highway --fingerprint`.
   - `laplace deploy` (`--prepare` under modular release manifests, else `--configure-server-cache`): creates the database when missing, installs `postgis` and `laplace`, and on existing installs **reconciles replaceable C/SQL functions, operators, opclasses, casts, and indexes in place via `laplace.reconcile.sql` (`ALTER EXTENSION laplace UPDATE TO ...` + `laplace_restore_function_bindings()`)** without dropping data whenever `laplace-storage:<hash>` matches; recreates (`--recreate`) only when persistent table storage DDL changed, configures `laplace.tier0`, `laplace.flags`, `laplace.highway`, and `laplace.chess` when `--configure-server-cache` runs, ensures every index (`laplace_schema_indexes()`), and reports `laplace status`.
   - `laplace status`.
   - It holds a lock per database and leaves while an ingest of it runs. `./deploy.sh drop` drops the database first, through the role, and deploys it again, empty; the workflow does that when dispatched with `drop`.
   - In the Operations workflow (`laplace.yml`) the deployment is followed by `checks` (`verify.sh deployment`: the extension's version and tables, and Engine and PostgreSQL on the same tier 0 and highway), `tests` (`verify.sh tests`: every database check of the deployed revisions, against the deployed database; see [Checks](../Reference/Checks.md#the-database-checks)) and `reads` (`verify.sh reads`). The components' own CI starts no server and makes no database: a deployment is what their database checks run against.

2. **Schema:** made by `CREATE EXTENSION laplace` itself (Laplace-postgres's install script).
   - `entity` and `physicality` are range-partitioned (`entity_t0`..`entity_t8plus` and `physicality_t0`..`physicality_t8plus` in `sql/laplace.sql.in`; see [30. Conflicts](../Sequence/Conflicts.md) P4 on tier vs ID-byte partitioning).
   - Attestations (`attestation`) and standings (`consensus`) are range-partitioned 16 ways by the first hex digit of the claim's ID (`0`..`f`).
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
