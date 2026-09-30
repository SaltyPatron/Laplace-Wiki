# SQL

The extension installs one type, `blake3`, its operators and operator classes, and 46 functions, 42 of them in C calling Laplace-Native and 4 in SQL over them; every function is `IMMUTABLE STRICT PARALLEL SAFE` unless stated, so a constant argument folds at plan time and a lookup by computed ID becomes an index lookup.

`laplace--1.0.sql` declares them in the order below; `laplace_pg.c` defines them. Four declared C functions have no definition in the current source, marked **missing** below: `CREATE EXTENSION laplace` fails at the first of them on a server whose `laplace.so` was built from that source. That is a defect of the current head, recorded, not resolved here.

## The type

| Object | Definition |
| --- | --- |
| `blake3` | 16 fixed bytes, `INTERNALLENGTH = 16`, `ALIGNMENT = char`, `STORAGE = plain`; text form 32 hexadecimal digits (`blake3_in`, `blake3_out`); binary send and receive as the raw 16 bytes |
| `=`, `<>`, `<`, `<=`, `>`, `>=` | byte comparison (`memcmp`), with commutators, negators, and the standard selectivity estimators; `=` hashes and merges |
| `blake3_ops` | the default B-tree operator class, `blake3_cmp` |
| `blake3_hash_ops` | the default hash operator class: `blake3_hash` takes the first 4 bytes as the hash, `blake3_hash_extended` hashes all 16 with a seed |

## Identity

| Function | Returns | Computes | Native |
| --- | --- | --- | --- |
| `laplace_cp_id(integer)` | `blake3` | a codepoint's ID | `lp_id_codepoint`; **missing** in the C source |
| `laplace_text_id(text)` | `blake3` | a text's codepoints composed directly as one word | `lp_id_codepoints_utf8`; **missing** |
| `laplace_compose(blake3[])` | `blake3` | the composition of the given IDs in order | `lp_id_compose`; **missing** |
| `laplace_id(text)` | `blake3` | the entity the engine records for the same text: `laplace_id('Sherlock Holmes')` is `[[S,h,e,r,l,o,c,k], ' ', [H,o,l,m,e,s]]` | `lp_text_decompose` over the mapped tier 0, composing without recording |
| `laplace_tier(text)` | `smallint` | that entity's tier | the same |
| `laplace_parts(text)` | `blake3[]` | its constituents in order, repeats included: the phrase to look for inside paths, `path @> laplace_parts('…')` | `lp_text_parts` |
| `laplace_codepoint(blake3)` | `integer` | the codepoint an atom is, or NULL | `lp_tier0_codepoint` |

## Paths

| Function | Returns | Computes | Native |
| --- | --- | --- | --- |
| `laplace_path_ewkb(blake3[])` | `bytea` | the EWKB path of these children | `lp_ewkb_path`; **missing** |
| `laplace_path(blake3[])` | `geometry` | SQL: `ST_GeomFromEWKB(laplace_path_ewkb($1))` | |
| `laplace_vertex_ids(geometry)` | `blake3[]` | the distinct IDs a path holds, the GIN key; `COST 10000`, measured: at lower costs the planner scans the partition of whole books and decodes every one on every lookup, 90 ms of a 111 ms query | `lp_xyz_to_id` per vertex |
| `laplace_path_times(geometry, blake3[]) → SETOF (id blake3, times bigint)` | rows | how many times a path holds each given ID, runs included, only the IDs it holds; `COST 1000 ROWS 4`; one pass over the path with a binary search per vertex | `lp_m_run` |
| `laplace_follows(geometry, blake3[])` | `blake3[]` | the ID after every run of the phrase inside the path; `COST 1000` | `lp_follows` |
| `laplace_text(blake3)` | `text` | the entity recomposed to its text, walking paths down to tier 0 through SPI, one prepared `SELECT st_asewkb(path) FROM physicality WHERE entity = $1 LIMIT 1` per composition, at most 64 tiers deep; `STABLE` | `lp_tier0_codepoint`, `lp_ewkb_vertices` |

### Containment and the GIN

| Object | Definition |
| --- | --- |
| `path @> blake3[]` | `laplace_path_contains`: the path holds every given ID; `COST 10000` outside the index; `RESTRICT = contsel, JOIN = contjoinsel` |
| `path && blake3[]` | `laplace_path_overlaps`: the path holds any of them; the same cost and selectivity |
| `laplace_path_ops` | GIN operator class for `geometry`, `STORAGE blake3`: strategy 3 `&&`, strategy 7 `@>`; support 1 `blake3_cmp`, 2 `laplace_gin_extract_value`, the sorted distinct IDs of the path, 3 `laplace_gin_extract_query`, the given IDs, an empty `@>` query searching all, 4 `laplace_gin_consistent`, every key present for `@>` and any for `&&`, with `recheck = false` because the keys are the exact IDs, 6 `laplace_gin_triconsistent` |

## Geometry on real coordinates

| Function | Returns | Computes | Native |
| --- | --- | --- | --- |
| `laplace_distance4d(geometry, geometry)` | `float8` | Euclidean distance between two POINT ZM | `lp_distance4` |
| `laplace_hilbert4(geometry)` | `bigint` | the Hilbert value of a POINT ZM, unflipped | `lp_hilbert4` |
| `laplace_inside(geometry)` | `boolean` | whether a POINT ZM is inside the wall, exactly | `lp_coord_inside` |
| `laplace_centroid4d_ewkb(geometry)` aggregate | `bytea` | the exact 4D centroid of POINT ZM values, as EWKB; `laplace_centroid4d_step` and `laplace_centroid4d_final` | `lp_centroid4_exact` |

## Shape measures

Each takes two paths' real-coordinate vertex sequences, POINT ZM or LINESTRING ZM, never packed paths:

| Function | Returns | Measure |
| --- | --- | --- |
| `laplace_frechet4d(geometry, geometry)` | `float8` | discrete Fréchet distance, `lp_frechet4` |
| `laplace_frechet4d(geometry, geometry, integer)` | `float8` | with up to *k* interior vertices of each skipped, 0 ≤ *k* ≤ 8, `lp_frechet4_outliers` |
| `laplace_dtw4d(geometry, geometry)` | `float8` | dynamic time warping, `lp_dtw4` |
| `laplace_edr4d(geometry, geometry, float8)` | `bigint` | edits, vertices within `eps` equal, `lp_edr4` |

## Tier 0 in place

Coordinates from the memory-mapped tier 0 at `laplace.tier0`, computed in the backend, so a lookup by computed Hilbert key prunes to the one partition that can hold the entity:

| Function | Returns | Computes | Native |
| --- | --- | --- | --- |
| `laplace_text_coord_ewkb(text)` | `bytea` | the real coordinate of the text's word composition, as a POINT ZM | `lp_ref_compose` over atoms |
| `laplace_text_coord(text)` | `geometry` | SQL: `ST_GeomFromEWKB(laplace_text_coord_ewkb($1))` | |
| `laplace_text_hilbert(text)` | `bigint` | its Hilbert value | `lp_hilbert4` |
| `laplace_cp_coord_ewkb(integer)` | `bytea` | a codepoint's coordinate | the tier-0 record |
| `laplace_coord_ewkb(text)`, `laplace_coord(text)` | `bytea`, `geometry` | the real coordinate of the entity `laplace_id` names, by the one decomposition of text | `lp_text_decompose` |
| `laplace_hilbert(text)` | `bigint` | its Hilbert value | |
| `laplace_fingerprint()` | `text` | the BLAKE3-256 of the tier 0 the database computes with, 64 hex digits; `STABLE` | `lp_tier0_fingerprint` |

## The flags that go with tier 0

Read from the memory-mapped flags at `laplace.flags` by the standard's own names; no table is read. Names match by UAX #44's loose rule.

| Function | Returns | Computes |
| --- | --- | --- |
| `laplace_flags(integer)` | `bytea` | a codepoint's 256 bits |
| `laplace_said(integer, text)`, `laplace_said(blake3, text)` | `text` | what a property is of a codepoint or an atom: `laplace_said(65, 'General_Category')` is `Uppercase_Letter`; NULL when the entity is not an atom or the property is unknown |
| `laplace_is(integer, text, text)`, `laplace_is(blake3, text, text)` | `boolean` | whether a property has a value: `laplace_is(id, 'script', 'Greek')` |

## Consensus

| Function | Returns | Computes |
| --- | --- | --- |
| `laplace_confidence(rating float8, deviation float8, k float8 DEFAULT 2)` | `float8` | how hard a strand tugs back: the chance the claim beats the anchor, rating 1500, read *k* deviations below its rating, `lp_confidence` |

## Observability

| Function | Returns | Computes |
| --- | --- | --- |
| `laplace_isa()` | `text` | `cpu: …; dispatch: …`, the CPU's features and the level the dispatcher uses; `STABLE` |

## How the engine calls the database

The engine never calls these functions in its hot paths; it computes IDs, coordinates, and paths itself with the same native code and asks the database only to find and write. The statements it issues are listed under [Ingest](Ingest.md#the-statements) and [Reads](Reads.md). The query benchmark and interactive SQL use the functions above.
