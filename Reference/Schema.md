# Schema

`CREATE EXTENSION laplace` makes the schema: a database is a Laplace database by that statement alone, as PostGIS makes `spatial_ref_sys` by its own. `laplace deploy` makes the database if the server has none, creates the extensions, names the database's tier 0, flags and highway, makes every index (`laplace_schema_indexes()`), registers the highway's identifier entities directly from the mapped highway perf-cache, and sets `enable_parallel_append` off; a database that had the tables before the extension owned them keeps them, and `laplace deploy` makes them the extension's. The tables' data goes with `pg_dump`.

## The four tables

| Table | Columns | Partitioned |
| --- | --- | --- |
| `entity` | `id blake3`, `tier smallint`, `lexical smallint`, `kind smallint`, `coord geometry(PointZM)` (the real 4D coordinate), `hilbert bigint` | 256 ways by the first byte of `id` (`entity_00`..`entity_ff`, `RANGE (id)`) |
| `physicality` | `entity blake3`, `tier`, `hilbert`, `path geometry` (the constituents' IDs in X/Y/Z; each vertex's M its run, what it is, and, a claim in a record, how the record said it: [Physicality](../Storage/Physicality.md#physicality)), `mask bit(256)` | 256 ways by the first byte of `entity` (`physicality_00`..`physicality_ff`, `RANGE (entity)`) |
| `attestation` | `claim blake3`, `witness blake3` (the source's trunk ID), `lineage blake3` (or NULL), `games bigint`, `tokens bigint`, `score double precision`, `"position" integer` (or NULL), `trust double precision` | 16 ways by the first hex digit of the claim's ID (`attestation_0`..`attestation_f`, `RANGE (claim)`), each with `fillfactor` 80; `UNIQUE NULLS NOT DISTINCT (claim, witness, lineage)` |
| `consensus` | `claim` (primary key), `rating`, `deviation`, `volatility`, `matches` | 16 ways by the first hex digit of the claim's ID (`consensus_0`..`consensus_f`), each with `fillfactor` 80 (updated in place) |

An ID is the extension's type `blake3`: 16 bytes, the BLAKE3 hash. Hilbert values are stored with the top bit flipped so `bigint` order is Hilbert order. The path's statistics target is 0 and the `physicality_*` partitions take no parallel workers, as [Operations: Database](../Operations/Database.md) says.

## The mask

`physicality.mask` is 256 bits ([Claims: Masks](../Semantics/Claims.md#masks)). As built it holds one bank, `kind`, bits 0 to 7: what the row is, a claim (0), a record (1), a tuple (2), a file (3), set when the row is first written. The banks are Laplace-Native's `manifest/banks.tsv`, one per semantic group, each on the row its group describes ([Types: Masks](Types.md#masks)); a value's bit in its bank is its frozen slot in `manifest/slots/LIST.tsv`. The lexical banks (`upos`, `lexfile`) belong on the entity's row and the structural banks (`deprel`, `vnrole`) on a layer's occurrences, and neither carrier is built yet.

Operators: `mask ? bit`, `mask ?& bits`, `mask ?| bits` (`smallint` bit positions, `laplace_mask_has`, `_has_all`, `_has_any`). `laplace_bank_bit(bank text, value text) → smallint` gives a value's bit in a bank, by its content as text (for `kind`, the kinds by name); -1 when the bank does not hold it, an error for a bank that does not exist. `laplace_bank_of(blake3) → (bank, grp, carrier, bit)` gives the bank a type's ID is a value of, and its bit there; nulls when it is a value of none. `laplace_mask_bit` of 1.7 and before is gone.

## The indexes

`laplace_schema_indexes()` makes them all, each on the partitioned parent, one per partition; the install script calls it, and `laplace index` calls it again if one was dropped: `entity (id)`, `entity (hilbert)`, `entity USING gist (coord gist_geometry_ops_nd)`, `physicality (entity)`, `physicality USING gin (path laplace_path_ops, mask laplace_mask_ops) WITH (gin_pending_list_limit = 262144)` (256 MB a partition: a load's entries are merged once, when the source is in). The one GIN over the path's constituents and the mask's bits answers "the claims that hold X" as one intersection of posting lists.

## The highway, in place

`laplace.highway` names the perf-cache; `laplace_type(list, value)` gives a type's slot from its content, `laplace_type_key(list, key)` the slot a resource's key names (through the `.keys` file), `laplace_type_id(list, slot)` the content's ID, `laplace_type_edges(a, slot, b)` the slots one type maps to in another list, `laplace_highway_fingerprint()` the fingerprint every install agrees on.

## Versions

The extension is greenfield until a release is deployed. The build generates one install script, `laplace--<version>.sql`, from `sql/laplace.sql.in`, where the version is `default_version` in `laplace.control`; it removes any other `laplace--*.sql` it generated before, and there are no update scripts. A database holding another version of the extension is recreated: `laplace deploy` stops and says so. Never `DROP EXTENSION laplace CASCADE`: the tables' columns are the extension's type.
