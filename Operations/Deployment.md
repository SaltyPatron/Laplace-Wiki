# Deployment

A Laplace database goes from empty to benchmarked in five steps: extensions, schema, ingestion, indexes, and measurement.

1. **Role, database, and extensions:**

   ```sh
   psql -U postgres -c "CREATE ROLE laplace LOGIN SUPERUSER" -c "CREATE DATABASE laplace OWNER laplace"
   psql -U laplace -d laplace -c "CREATE EXTENSION postgis" -c "CREATE EXTENSION laplace" \
        -c "CREATE EXTENSION pg_stat_statements" -c "CREATE EXTENSION pg_buffercache"
   ```

   The extension's setting `laplace.tier0` points to the tier-0 perf-cache. Each backend memory-maps it on first use.

2. **Schema:** made by `CREATE EXTENSION laplace` itself (Laplace-postgres's install script).
   - Entities, paths, and statistics are list-partitioned by tier.
   - The largest tiers are split again into 16 partitions by the first hex digit of their ID. An ID is a hash, so the partitions stay equal, and a lookup by ID prunes to one partition.
   - The schema also applies the planning settings for paths from [Database](Database.md#planning).

3. **Ingestion:** `laplace-ingest [-d conninfo] [-t tier0.bin] file...`
   - It skips files whose bytes are already recorded, with one query over their BLAKE3-256 hashes.
   - It decomposes the rest.
   - It deduplicates them against the database, trunk to leaf, with one set-based query per tier.
   - It streams only new rows, by binary COPY.
   - It prints live counters and the time of every phase.

4. **Indexes,** after a bulk load: `sql/indexes.sql`.
   - IDs: B-tree.
   - Hilbert values: B-tree.
   - Real coordinates: 4D GiST.
   - IDs decoded from paths: GIN, which finds containers.
   - Occurrences: B-tree.
   - Then `ANALYZE`.

5. **Measurement:**
   - `laplace-bench` measures every native operation.
   - `bench/bench_queries.py` runs each query cold and warm, and reports:
     - execution and round-trip time;
     - buffers read and hit;
     - the partitions the plan touched.
