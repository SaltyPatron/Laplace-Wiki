# Schema

`CREATE EXTENSION laplace` makes the schema: a database is a Laplace database by that statement alone, as PostGIS makes `spatial_ref_sys` by its own. `laplace deploy` makes the database if the server has none, creates the extensions, names the database's tier 0, flags and highway, makes every index (`laplace_schema_indexes()`), registers the highway's identifier entities directly from the mapped highway perf-cache, and sets `enable_parallel_append` off; a database that had the tables before the extension owned them keeps them, and `laplace deploy` makes them the extension's. The tables' data goes with `pg_dump`.

## The four tables

| Table | Columns | Partitioned |
| --- | --- | --- |
| `entity` | `id blake3`, `tier smallint`, `coord geometry(PointZM)` (the real 4D coordinate), `hilbert bigint`, `mask bit(64)` (`CHECK laplace_mask_valid`) | 9 tier range partitions (`entity_t0`..`entity_t8plus`, `RANGE (tier)`), primary key `(tier, id)`, per-partition unique index on `(id)` (see [30. Conflicts](../Sequence/Conflicts.md) P4) |
| `physicality` | `entity blake3`, `tier smallint`, `hilbert bigint`, `path geometry` (the constituents' IDs in X/Y/Z; each vertex's M its run, role, outcome, and position: [Physicality](../Storage/Physicality.md#physicality)), `mask bit(64)` (`CHECK laplace_mask_valid`) | 9 tier range partitions (`physicality_t0`..`physicality_t8plus`, `RANGE (tier)`), primary key `(tier, entity)`, foreign key `(tier, entity) → entity(tier, id) ON UPDATE CASCADE`, per-partition unique index on `(entity)` |
| `attestation` | `claim blake3`, `witness blake3` (the source's trunk ID), `lineage blake3` (or NULL), `games bigint`, `tokens bigint`, `score double precision`, `"position" integer` (or NULL), `trust double precision` | 16 ways by the first hex digit of the claim's ID (`attestation_0`..`attestation_f`, `RANGE (claim)`), each with `fillfactor` 80; `UNIQUE NULLS NOT DISTINCT (claim, witness, lineage)` |
| `consensus` | `claim blake3` (primary key), `rating double precision`, `deviation double precision`, `volatility double precision`, `matches bigint` | 16 ways by the first hex digit of the claim's ID (`consensus_0`..`consensus_f`, `RANGE (claim)`), each with `fillfactor` 80 (updated in place) |

An ID is the extension's type `blake3`: 16 bytes, the BLAKE3 hash. Hilbert values are stored with the top bit flipped (`h ^ 0x8000000000000000`) so signed `bigint` order is unsigned Hilbert order. The path's statistics target is 0 and the `physicality_*` partitions take `parallel_workers = 0`, as [Operations: Database](../Operations/Database.md) says.

## The mask

Both `entity.mask` and `physicality.mask` are 64-bit carriers (`bit(64)`, [Claims: Masks](../Semantics/Claims.md#masks)) partitioned into disjoint fields by Laplace-Native's `manifest/banks.tsv` ([Types: Masks](Types.md#masks)): `kind` is an 8-bit row-role flag set at bit 0 (claim, record, tuple, file), while every other bank (`upos` 5@8, `lexfile` 6@13, `deprel` 6@19, `vnrole` 6@25, `wnframe` 6@31) is an enum field storing `slot + 1` (`0` = absent) from its frozen list in `manifest/slots/LIST.tsv`.

Operators: `mask ? bit`, `mask ?& bits`, `mask ?| bits` (`smallint` / `smallint[]`, `laplace_mask_has`, `_has_all`, `_has_any`). `laplace_bank_bit(bank text, value text) → smallint` gives a value's field descriptor from its content as text (`-1` when absent, an error for an unknown bank). `laplace_bank_of(blake3) → (bank, grp, carrier, bit)` gives the bank a type's ID belongs to.

## The indexes

`laplace_schema_indexes()` (`sql/operations.sql`) makes them all on the partitioned parents, one per partition; the install and reconcile scripts call it, and `laplace index` calls it again if one was dropped:

- `entity_hilbert` on `entity (hilbert)` and `entity_tier_hilbert` on `entity (tier, hilbert, id)`;
- `entity_coord` on `entity USING gist (coord laplace_point4d_ops)` and `entity_angular` on `entity USING gist (coord laplace_angular4d_ops)`;
- `physicality_paths` on `physicality USING gin (path laplace_path_ops, mask laplace_mask_ops) WITH (gin_pending_list_limit = 32768)` — one composite GIN over decoded vertex IDs and mask fields;
- `physicality_assertions` partial GIN on `physicality USING gin (path laplace_path_ops) WITH (gin_pending_list_limit = 32768) WHERE laplace_path_has_roles(path, 6)`;
- `attestation_witness_lineage` on `attestation (witness, lineage NULLS FIRST) INCLUDE (trust)`.

## The highway, in place

`laplace.highway` names the perf-cache; `laplace_type(list, value)` gives a type's slot from its content, `laplace_type_key(list, key)` the slot a resource's key names (through the `.keys` file), `laplace_type_id(list, slot)` the content's ID, `laplace_type_edges(a, slot, b)` the slots one type maps to in another list, `laplace_highway_fingerprint()` the fingerprint every install agrees on.

## Versions

`Laplace-postgres` hashes persistent storage DDL (`CREATE TYPE blake3` and the four table definitions in `sql/laplace.sql.in`) into `laplace-storage:<16-hex>` (`COMMENT ON TABLE entity`) separately from the full install script hash (`default_version` in `laplace.control`), and emits `laplace.reconcile.sql` for all replaceable C and SQL routines, casts, operators, opclasses, and indexes. When storage DDL is unchanged, `laplace deploy` prepares a transition script and runs `ALTER EXTENSION laplace UPDATE TO ...` in place while keeping all loaded rows and indexes intact; `laplace deploy --recreate` drops and recreates the database only when the persistent storage layout changes. Never run `DROP EXTENSION laplace CASCADE` in place: the tables' columns and indexes depend on the extension's types and functions.
