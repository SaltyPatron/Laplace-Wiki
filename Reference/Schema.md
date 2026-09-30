# Schema

Five tables hold the world: `entity` and `physicality`, list-partitioned by tier and the large tiers range-partitioned sixteen ways by the ID's first hex digit; and `witness`, `attestation`, and `consensus` for what is not content.

`laplace deploy` runs `schema.sql` when there is no partitioned table `entity`, then `semantics.sql` and `lookup.sql` every time; `laplace index` runs `indexes.sql` after a bulk load. The SQL is Laplace-postgres's; the engine reads the files from `$LAPLACE_SQL`, strips `\` commands and comment lines, and runs them.

## Content: schema.sql

```sql
CREATE TABLE entity (
  id       blake3   NOT NULL,
  tier     smallint NOT NULL,
  coord    geometry(PointZM) NOT NULL,           -- the real 4D coordinate; M is W
  hilbert  bigint   NOT NULL                     -- top bit flipped: bigint order = Hilbert order
) PARTITION BY LIST (tier);

CREATE TABLE physicality (
  entity   blake3   NOT NULL,
  tier     smallint NOT NULL,
  hilbert  bigint   NOT NULL,
  path     geometry NOT NULL                     -- children's IDs in X/Y/Z, run lengths in M
) PARTITION BY LIST (tier);
```

Partitions, made by a `DO` block: for tiers 0 to 15, `entity_t<t>` and `physicality_t<t>`; for the tiers in `ARRAY[0, 2, 3, 4, 5, 6]`, each of those is itself `PARTITION BY RANGE (id)` into sixteen children `entity_t<t>_<h>` for `h` in `0`..`f`, bounded by the 32-digit hexadecimal literals `h000…0` to `(h+1)000…0`, with `MINVALUE` and `MAXVALUE` at the ends; and `entity_tx`, `physicality_tx` as the `DEFAULT` partitions for every tier deeper than 15. The split tiers are the ones measured largest: atoms, words, sentences and their like, and the tiers claims and records fall in. The engine reads which tiers are split from `pg_class` at every load (`parts_plan`) and never assumes it.

Settings applied by the same file: `ALTER TABLE physicality ALTER COLUMN path SET STATISTICS 0`; `ALTER TABLE <every physicality_t*> SET (parallel_workers = 0)`; `ALTER DATABASE <this> SET enable_parallel_append = off`.

## Semantics: semantics.sql

```sql
CREATE TABLE IF NOT EXISTS witness (
  id       blake3 PRIMARY KEY,                   -- an entity: whatever testifies, named as content
  lineage  blake3,                               -- the witness it derives from
  trust    double precision NOT NULL             -- -1 .. 1
);
CREATE TABLE IF NOT EXISTS attestation (         -- the ledger: append-only, in reading order
  claim    blake3 NOT NULL,
  witness  blake3 NOT NULL,
  score    real NOT NULL,                        -- win 1, draw 0.5, loss 0, or between
  position integer                               -- the position the witness gave the claim among its like
);
CREATE TABLE IF NOT EXISTS consensus (           -- updated in place as matchups are played
  claim       blake3 PRIMARY KEY,
  rating      double precision NOT NULL,
  deviation   double precision NOT NULL,
  volatility  double precision NOT NULL,
  matches     integer NOT NULL
) WITH (fillfactor = 80);
```

A claim is not a row here. It is a composition, an entity with a physicality path of the entities it relates, hashed like any path, living in `entity` and `physicality` with all other content, so the GIN finds every claim that touches an entity. `attestation.claim` is the ID of what was witnessed, the claim with its specifics, or a record; `consensus.claim` is the ID of the claim that holds the standing. A record's claims are witnessed within it: one ledger row per record.

## Indexes

`lookup.sql`, run at deploy, present from the start because ingestion needs them:

```sql
CREATE INDEX IF NOT EXISTS entity_id ON entity (id);
CREATE INDEX IF NOT EXISTS physicality_entity ON physicality (entity);
CREATE INDEX IF NOT EXISTS attestation_claim ON attestation (claim);
```

`indexes.sql`, run by `laplace index` after a bulk load, each created on the partitioned parent, which builds one per partition, with `maintenance_work_mem = '8GB'` and `max_parallel_maintenance_workers = 6` for the session, then `ANALYZE`:

```sql
CREATE INDEX IF NOT EXISTS entity_hilbert ON entity (hilbert);
CREATE INDEX IF NOT EXISTS entity_coord ON entity USING gist (coord gist_geometry_ops_nd);
CREATE INDEX IF NOT EXISTS physicality_paths ON physicality USING gin (path laplace_path_ops);
CREATE INDEX IF NOT EXISTS attestation_claim ON attestation (claim);
CREATE INDEX IF NOT EXISTS attestation_witness ON attestation (witness);
```

| Index | Serves | Cost note |
| --- | --- | --- |
| `entity_id`, per partition | lookup by ID; with `tier` in the predicate it prunes to one partition | measured 0.02 ms with tier, 0.08 ms over 14 partitions without |
| `physicality_entity` | an entity's path; recomposition | |
| `entity_hilbert` | ordering and ranges by Hilbert value | |
| `entity_coord`, n-D GiST | 4D nearest neighbour, `coord <<->> laplace_coord('king')`; float32 boxes rounded outward, so it is a candidate filter and the exact doubles are rechecked | 16 nearest to `king`, 7.7 ms |
| `physicality_paths`, GIN with `laplace_path_ops` | containers: `path @> blake3[]`, `path && blake3[]`; the keys are the distinct IDs decoded from the vertices; no recheck | every container of `Holmes`, 0.80 ms over 52 partitions; the run `Sherlock Holmes`, 1.76 ms |
| `attestation_claim`, `attestation_witness` | the ledger by claim and by witness; `laplace forget` | |
| `consensus` primary key | a standing by claim | 0.1 ms |

During a load the GIN keeps what it is handed in a pending list; `laplace ingest` merges it once at the end with `gin_clean_pending_list` over every GIN index, so no lookup pays for the load.

## Extension control

`laplace.control`: `comment = 'Laplace: 4D expansion of PostgreSQL and PostGIS'`, `default_version = '1.0'`, `module_pathname = '$libdir/laplace'`, `requires = 'postgis'`, `relocatable = true`. `laplace deploy` runs `CREATE EXTENSION IF NOT EXISTS` for `postgis`, `laplace`, `pg_stat_statements`, `pg_buffercache`, then `ALTER EXTENSION laplace UPDATE`.

## What the prototype had

`Laplace-Prototype/db/schema.sql` had, beside `entity` and `physicality` (unpartitioned, `bytea` IDs, `entity.coord` PointZM, `physicality.path` with the GIN on `laplace_vertex_ids(st_asewkb(path))`), two tables the built schema does not have:

- `source (trunk, origin, modality, format, bytes, content_blake3)`: what was ingested and where from. In the built schema a file is no row: it is a trunk in the DAG, `[metadata, content]`, whose metadata holds its name, and whether it is recorded is answered by deduplication on its trunk.
- `entity_stats (id, parents, occurrences)`: containers and occurrences per entity. In the built schema these are not stored; `laplace fills` computes occurrences at read time, leaf to trunk and back, from the paths.

The wiki's [Storage](../Storage/README.md) pages and the Sequence pages that name a source table or a statistics table describe the prototype; the built schema is the five tables above.

## Storage measured

At volume, a Tatoeba sentence of 16.6 vertices cost about 1,117 bytes: 599 in its path, 101 in its entity row, and the rest in indexes and statistics. Standings updated in place absorbed 740,000 to 780,000 attestations per second, the consensus table staying at 66 MB with dead rows levelling near 34,000 under fill factor 80.
