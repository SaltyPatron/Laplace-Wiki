# Formats

Every byte layout Laplace writes or reads: the 128-bit ID, the 64-byte tier-0 record and its fingerprint, the 32-byte flags record and its layout file, the fixed-point coordinate and the wall, the Hilbert value, the packed path vertex, the EWKB path, the binary parameters and COPY rows, and the engine's in-memory node table.

## The ID

`lp_id`: 16 bytes, `uint8_t b[16]`. The first 16 bytes of BLAKE3's 256-bit output; BLAKE3 is an extendable-output function whose shorter outputs are prefixes of longer ones, so `digest(16) == digest(32)[:16]`.

| Of | Input to BLAKE3 | Function |
| --- | --- | --- |
| a codepoint | its UTF-8 bytes, 1 to 4; a surrogate written in the generalized 3-byte form | `lp_id_codepoint` |
| a composition of *n* ≥ 2 children | the children's 16-byte IDs, contiguous, in order, repeats included: `16 n` bytes | `lp_id_compose` |
| a composition of one child | no hash: the child's ID | `lp_id_compose`, `lp_ref_compose` |
| a UTF-8 string as one composition of its codepoints | the codepoint IDs in order | `lp_id_codepoints_utf8` |
| a file's bytes | never: a file is named by its trunk, the composition of its metadata and content | `file_close` |

Text form: 32 lowercase hexadecimal digits, byte 0 first (`id_text`, `blake3_out`). Golden values: `A` is `32684bfa28c0c84d6f210511aace0efc`; the word `Holmes`, `[H,o,l,m,e,s]`, is `5b7e40e9a23ae55eaccd45646934977d`.

## The tier-0 record

`lp_tier0_record`, 64 bytes, `_Static_assert`ed; the file is `LP_NCP` = 1,114,112 records indexed by codepoint, 71,303,168 bytes, at `$LAPLACE_TIER0`:

| Offset | Size | Field | Content |
| --- | --- | --- | --- |
| 0 | 16 | `id` | the codepoint's ID |
| 16 | 32 | `m[4]` | four `int64_t`: the fixed-point coordinate, value `m / 2^53` on each axis |
| 48 | 8 | `hilbert` | `uint64_t`: the 4D Hilbert value of the coordinate |
| 56 | 4 | `rank` | `uint32_t`: the codepoint's rank in the DUCET total order |
| 60 | 4 | `pad` | 0 |

`lp_tier0_map` refuses a file whose size is not exactly `LP_NCP × 64`. Its fingerprint is BLAKE3-256 over the whole table (`lp_tier0_fingerprint`), which `laplace tier0` prints beside a second BLAKE3-256 over the DUCET order written as 3-byte big-endian codepoints in rank order. The prototype's `fingerprint.txt` recorded the same table's SHA-256, `1710d2d9…`, and the order's SHA-256, `31548536…`; the built fingerprint is BLAKE3 and is what `laplace_fingerprint()` reports.

## The flags record

`lp_flags`, 32 bytes, 256 bits, one per codepoint; the file is `LP_NCP × 32` bytes at `lp_flags_path()`. A bit for each binary property in the order `PropertyAliases.txt` lists them, then a field for each enumerated or catalog property as wide as its value list needs, the value being its place in `PropertyValueAliases.txt`'s list. Bits are set with `set_bits(rec, bit, width, v)`: bit *i* of the field goes to bit `bit + i` of the record, least-significant first within each byte.

The layout file, the flags path plus `.layout`, is tab-separated, one field per line, `#` lines ignored: `bit`, `width`, `name` (the short property name), `say` (the long name), and the values as `short=long` pairs separated by spaces. `lp_flags_map` reads it once into `lp_layout`: `lp_field { name[32], say[64], bit, width, nvalues, first }` and `lp_value { name[48], say[64] }`. Names match by UAX #44's loose rule, LM3: case, spaces, underscores, and hyphens do not count (`lp_name_same`).

## Coordinates and the wall

`lp_coord`: `int64_t m[4]`, value `m / 2^53` per axis; `LP_FIXED_ONE` = 2^53 = 9007199254740992.0. Every such value is an exact `double`, so the columns stay `float8` while all arithmetic is integer.

- **Centroid** (`lp_coord_centroid`, `lp_ref_compose`): `s[d] = Σ m_i[d]` in `__int128`; `out[d] = s[d] / n` with C's division, which truncates toward zero. Golden: `[2, −2, 0, 0]` from children summing to `[5, −5, 0, 0]` over 2; no overflow at `INT64_MAX / 2`.
- **The wall** (`lp_coord_inside`): `Σ m[d]²` in `unsigned __int128`, inside when `≤ 2^106`. The edge is inside; one more is outside.
- **Tier-0 nudge** (`laplace tier0`): `m = rint(x · 2^53)`; while `Σ m² > 2^106`, the largest `|m[j]|` moves one unit toward zero. 624,971 units moved on the reference generation.
- **A real point as geometry**: `lp_ewkb_point4` writes a POINT ZM of 37 bytes, `x[d] = m[d] / 2^53`, M carrying the fourth axis. The database column `entity.coord` is `geometry(PointZM)`.

## The Hilbert value

`lp_hilbert4`: the grid is `g[d] = floor((x + 1) / 2 · 65536)`, `x = m / 2^53`, clamped to `[0, 65535]`, computed in IEEE double without contraction so the bits are the same on every CPU. Skilling's axes-to-transpose over 4 axes of 16 bits, branchless (`hilbert_transpose`), then the interleave: bit *b* of axis *i* goes to bit `4b + (3 − i)` of the 64-bit value; `pdep` on x86-64-v3, scalar otherwise, same result. Stored in `entity.hilbert` and `physicality.hilbert` as `bigint` with the top bit flipped, `h ^ 0x8000000000000000`, so `bigint` order equals Hilbert order.

## The packed path vertex

A path is a POINT ZM or LINESTRING ZM whose vertices are not positions. Each vertex is 32 bytes: X, Y, Z, M as doubles.

- **X, Y, Z carry the constituent's ID** (`lp_id_to_xyz`): the 16 bytes read as one little-endian 128-bit integer *v*; `part0 = v & (2^43 − 1)`, `part1 = (v >> 43) & (2^43 − 1)`, `part2 = v >> 86` (42 bits); each part is placed in the low mantissa bits of a double whose exponent field is 1021 (`EXP_BITS = 1021 << 52`), sign 0, so every value lies in `[0.25, 0.5)`. `lp_xyz_to_id` reads only the ID's own bits of each, 43, 43 and 42 (`lp_xyz_id_mask`), and reassembles *v*. The 28 bits the ID leaves, 9, 9 and 10, are the vertex's spare bits (`lp_xyz_spare`, `lp_xyz_spare_set`): bits 0 to 3 a tag saying which layout they are in, 4 to 27 its payload, 0 for none; a value there never changes which entity the vertex is, and the scans compare through the ID's bits only. Round-trip is exact for every ID; measured 104 M per second per core.
- **M carries the vertex's metadata** as an integer in a double: the low 30 bits (`LP_M_RUN_BITS`) are the run length, how many times the child is repeated, 1 or more; above them, what the vertex is: `LP_SAID_CLAIM` = 1, `LP_SAID_RECORD` = 2, `LP_SAID_TUPLE` = 3, `LP_SAID_METADATA` = 4; `lp_m_run(m)`, `lp_m_said(m)`. A run of identical children is one vertex.
- **Atoms**: a POINT ZM holding the codepoint's own ID with run 1.

### EWKB

`lp_ewkb_path` and `lp_ewkb_runs` write little-endian EWKB: byte 0 = 1; type = `1 | 0x80000000 | 0x40000000` (POINT ZM, `0xC0000001`) when there is one run, else `2 | Z | M` (LINESTRING ZM, `0xC0000002`) followed by the 4-byte vertex count; then the vertices. A one-run path is 37 bytes; an *n*-run path is `9 + 32 n`. `lp_ewkb_vertices` parses either, with an optional SRID, and returns a pointer to the first vertex. The extension reads PostGIS's serialization version 2 directly (`geo_of`): flags byte 7 must have `Z`, `M`, and `VERSION`; an extended header or bounding box is skipped; the vertex block is the same 32-byte layout, so Native's kernels take it after a 9-byte header is built on the stack (`as_ewkb`).

Paths move only as EWKB and binary COPY; WKT at default precision changed 93.5% of coordinates.

## Binary wire formats

- **A `blake3[]` parameter** (`ids_param`): a 20-byte array header of big-endian `int32`s, `ndim = 1`, `flags = 0`, `elem oid = id_oid` (the type's OID, read once with `SELECT 'blake3'::regtype::oid`), `n`, `lbound = 1`; then per element a 4-byte length 16 and the 16 bytes. `20 + 20 n` bytes, sent in binary with `PQexecParams`.
- **Binary COPY** (`db.c`): the 19-byte header `PGCOPY\n\xff\r\n\0` + flags 0 + extension length 0; per row a big-endian `int16` field count, then per field a big-endian `int32` length and the bytes; NULL is length `0xFFFFFFFF`; the trailer is `int16` −1. Rows:

| Table | Fields |
| --- | --- |
| `entity_t*` | `id` 16 B; `tier` int16; `coord` EWKB POINT ZM 37 B; `hilbert` int64, top bit flipped |
| `physicality_t*` | `entity` 16 B; `tier` int16; `hilbert` int64; `path` EWKB; `mask` bit varying: its length in bits as int32 (256), then 32 bytes, bit *b* in byte *b* >> 3 under `0x80 >> (b & 7)` |
| `witness` | `id` 16 B; `lineage` 16 B or NULL; `trust` float8 |
| `attestation` | `claim` 16 B; `witness` 16 B; `score` float4; `position` int32 or NULL |
| `consensus` | `claim` 16 B; `rating`, `deviation`, `volatility` float8; `matches` int32 |

Results are requested in binary (`PQexecParams` with result format 1); `float8` columns are read as big-endian 8-byte values and `int` as big-endian 4-byte.

## The engine's node table

In memory during an ingest (`table.c`): one flat table of slots shared by every thread without a lock, open addressing by linear probing; a slot is empty, or the ID's tag over the node's index, claimed by compare-and-swap. `Node { id; int64_t m[4]; uint64_t voff; uint32_t nv, len; uint8_t tier, keep, kind, live; }` (`kind`: the bits of what whatever holds it says it is; `live`: a node, not an unused place) and the vertex array `Vtx { id; uint64_t m; }` packed, where `m` is M as it will be written, run length and said bits together. `keep` states during a load: 0 not looked for, 1 new and to be written, 2 recorded already, 3 in the frontier, 5 a file trunk held back to be written last.

## The highway's files

`laplace highway` writes the highway beside tier 0 (`$LAPLACE_HIGHWAY`):

| File | What |
| --- | --- |
| `tier0.highway` | one record per type in the form of a tier-0 record, its rank the type's slot and its pad the content's tier; then the edges, each a pair of 32-bit slots, grouped by the pair of lists |
| `.layout` | text, a line each: `records N`; `edges-count N`; `list NAME TITLE FIRST COUNT`, the lists in order with the record each begins at; `edges A B FIRST COUNT`; `bank NAME LIST GROUP CARRIER WIDTH`, copied from `banks.tsv` |
| `.keys` | `LIST KEY SLOT` a line: the identifiers the resources point at their types with, each to its slot, an index over that content. As built the readers resolve them through this file and record nothing of them; the law records an identifier as content and attests that it names its type |
| `.nodes` | the content of every type as the composition it is: `N` lines (a node, its ID, its tier and its path) and `S` lines (a list's slot and its content's ID), which `laplace deploy` records |

Laplace-Native's manifest keeps what must not move between builds: `manifest/banks.tsv` (`bank list group carrier width`, a line a bank) and `manifest/slots/LIST.tsv` (`slot id status key`, `status` `live` or `retired`), written back by `laplace highway` and never by hand.

## The recipe, firmware, and layout text files

Their grammars are on [Recipes](Recipes.md) and [Firmware](Firmware.md). All three are plain text, one directive per line, `#` starting a comment, names of several words between double quotes.
