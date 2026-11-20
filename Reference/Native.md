# Native

Laplace-Native's eight public headers under `include/laplace/` (`laplace.h`, `consensus.h`, `geometry.h`, `highway.h`, `json.h`, `linalg.h`, `perfcache.h`, `tier0.h`) declare every shared operation: identity, UTF-8, tier 0 and its flags, fixed-point coordinates, composition, text decomposition, geometry packing, trajectory matching, 4D and S³ geometry, consensus, perf-caches, JSON, linear algebra, model kernels, and the pull's search frontier, with bit-identical results on every CPU whichever SIMD path runs.

`Laplace-postgres`, `Laplace-Engine`, and `Laplace-MCP` consume the installed `LaplaceNative` CMake package (`find_package(LaplaceNative CONFIG REQUIRED)`) and keep no copy of any operation, while .NET consumers bind to the AST-generated `Laplace.Native.Interop` package (`tools/csharp/generate.mjs`). Exported targets: `Laplace::laplace` and `Laplace::laplace_static` (core library, linked with `Laplace::math` over CORE-MATH), `Laplace::text` (UAX #29 decomposition over ICU 78), `Laplace::model` (model kernels over MKL and OpenMP), and `Laplace::linalg` (Eigen and Spectra compiled scalar with fixed blocking).

## Public headers

| Header | Scope |
| --- | --- |
| `laplace/laplace.h` | Core constants, CPU dispatch, allocator and growable buffers, big-endian/hex/mmap/sort helpers, 128-bit BLAKE3 identity and DAG multiplicity, UTF-8, 4D fixed-point coordinates and Hilbert ball/box ranges, mantissa geometry packing, trajectory matching (`lp_follows`, `lp_precedes`, `lp_path_*`), `lp_idmap`/`lp_strmap`, PostgreSQL binary wire/COPY streams, 4D shape (`lp_frechet4`, `lp_dtw4`, `lp_edr4`, `lp_hausdorff4`), S³ operators (`lp_angle4`, `lp_slerp4`, `lp_karcher_mean4`, `lp_eigen_centroid4`), `lp_dot_i8`, `lp_rowsig`/`lp_knn_exact`/`lp_mkl_reproducible`, Glicko-2 (`lp_attest_series`, `lp_series_floor`), Tier-0/flags/highway core APIs, `lp_realize`, and `lp_frontier` |
| `laplace/consensus.h` | `LP_SAID_DEPENDENCE` (`7`), `lp_series_entry`, `lp_standing`, `lp_tally`/`lp_tally_edge`, `lp_series_attested`, rooted concave multi-source posteriors (`lp_series`, `lp_series_update`, `lp_series_evaluate`), and `lp_witness_precision` |
| `laplace/geometry.h` | Arbitrary EWKB ZM span validation and traversal (`lp_ewkb_visit`, `lp_ewkb_vertex`, `lp_ewkb_keys`) and `lp_ewkb_point_zm`, `lp_ewkb_line_zm`, `lp_ewkb_polygon_zm`, `lp_ewkb_collection_zm` writers |
| `laplace/highway.h` | `lp_mask` (`uint64_t`), modular highway shards (`CORE`, `WORDNET`, `FRAMES`), single-file `lp_highway_write`, identifier component lookup and decomposition (`lp_highway_identifier_parts`, `lp_highway_decompose`, `lp_highway_find`, `lp_highway_resolve`), and 64-bit mask-bank operators (`lp_mask_field`, `lp_mask_put`, `lp_mask_has`, `lp_mask_get`, `lp_mask_clear`, `lp_mask_merge`, `lp_mask_add_id`) |
| `laplace/json.h` | RFC 8259 parser (`lp_json_parse`, `lp_json_parse_prefix`, `lp_json_get`, `lp_json_string`, `lp_json_number`, `lp_json_integer`, `lp_json_bool`) and string writer (`lp_json_str`) |
| `laplace/linalg.h` | Deterministic scalar Eigen/Spectra kernels (`lp_eigenmap`, `lp_procrustes`, `lp_gram_schmidt`) in `Laplace::linalg` |
| `laplace/perfcache.h` | Generic `LPPC0001` fingerprinted ROM container (`LP_PERFCACHE_DENSE`, `SPARSE`, `PAIRS`; `lp_perfcache_write`, `lp_perfcache_map`, `lp_perfcache_at`, `lp_perfcache_find`, `lp_perfcache_pair`, used by `chess.bin`) |
| `laplace/tier0.h` | Disjoint Tier-0 and flags script shards (`ascii` 128, `utf` 22,112, `cjk` 115,920, `ext` 975,952), `lp_tier0_at`, `lp_tier0_find`, `lp_tier0_from_ucd`, `lp_tier0_write_shards`, and `lp_flags_map_branches` |

## Constants and dispatch

| Name | Value | Meaning |
| --- | --- | --- |
| `LP_NCP` | 1114112 | codepoints in the codespace |
| `LP_FIXED_ONE` | 2^53 | a coordinate `m` has the value `m / 2^53` |
| `LP_GLICKO_SCALE` | 173.7178 | Glicko-2's scale (`LP_GLICKO_RATING = 1500.0`, `LP_GLICKO_DEVIATION = 350.0`, `LP_ATTEST_FLOOR = 30.0`) |
| `LP_M_RUN_BITS` | 30 | bits `0..29` of M holding a vertex's run length |
| `LP_SAID_CLAIM` … `LP_SAID_DEPENDENCE` | 1 … 7 | bits `30..32` of M (`LP_M_SAID_BITS = 3`): `CLAIM = 1`, `RECORD = 2`, `TUPLE = 3`, `METADATA = 4`, `HOLDS = 5`, `VOICE = 6`, `DEPENDENCE = 7` (`consensus.h`) |
| `LP_OUTCOME_WIN`, `DRAW`, `LOSS`, `SCORE` | 0, 1, 2, 3 | bits `33..34` of M (`LP_M_OUTCOME_BITS = 2`); `SCORE` reads `score × 2^24` from spare tag `LP_SPARE_SCORE = 1` |
| `LP_M_POSITION_SHIFT`, `LP_M_POSITION_BITS` | 35, 18 | bits `35..52` of M holding the 1-based ordinal position among claims said together (`0` = none) |
| `LP_MASK_BITS` | 64 | width of the single `uint64_t` / SQL `bit(64)` mask carrier defined by `manifest/banks.tsv` |
| `LP_CPU_SSE2` … `LP_CPU_AMX` | bit flags | SSE2, SSE4.1, AVX2 with FMA and BMI2 (`x86-64-v3`), AVX-512 F/BW/VL/DQ (`x86-64-v4`), AVX-512 VNNI, AVX-VNNI, AMX |

`lp_cpu_features()` (`cpu.c`) reads `cpuid` and `xgetbv` once. `lp_cpu_active()` returns the active dispatch mask, with `LAPLACE_ISA` lowering it for testing (`scalar`, `sse2`, `avx2`, `avxvnni`, `avx512`, `avx512vnni`) and never raising it past what the CPU supports. `lp_cpu_describe(f)` names a feature set. Dispatched SIMD kernels: vertex scan (`scalar`, `avx2`, `avx512`), 4D squared-distance row (`scalar`, `avx2`, `avx512`), S³ half-chord (`scalar`, `avx2`), 4D Hilbert interleave (`scalar`, `bmi2`), and quantized `int8` dot products (`lp_dot_i8` / `lp_dot_i8_batch`: `scalar`, `avx2`, `avxvnni`, `avx512`, `avx512vnni`). Every floating-point summation uses one fixed association order (`((dx² + dy²) + dz²) + dm²`), placing one vertex pair per SIMD lane under `-fp-model=precise -ffp-contract=off` so every ISA path produces identical bits.

## Identity: identity.c, utf8.c

| Function | Contract |
| --- | --- |
| `void lp_id_codepoint(uint32_t cp, lp_id *out)` | BLAKE3-128 of the codepoint's UTF-8 bytes; a surrogate in the generalized 3-byte form |
| `void lp_id_compose(const lp_id *children, size_t n, lp_id *out)` | BLAKE3-128 over the children's 16-byte IDs, contiguous and in order, repeats included; `n == 1` returns the child |
| `bool lp_id_codepoints_utf8(const char *s, size_t len, lp_id *out)` | the string as one composition of its codepoints; false on invalid UTF-8 or an empty string |
| `size_t lp_utf8_put(uint32_t cp, uint8_t out[4])` | the codepoint's UTF-8, 1 to 4 bytes, surrogates in 3 |
| `bool lp_utf8_next(const uint8_t *s, size_t n, size_t *i, uint32_t *cp)` | the codepoint at `s[*i]`, advancing; false, leaving `*i`, on a malformed sequence or a value outside the codespace |

## Coordinates: coord.c

| Function | Contract |
| --- | --- |
| `void lp_coord_centroid(const lp_coord *c, size_t n, lp_coord *out)` | the exact integer average, summed in 128-bit, truncated toward zero; `n == 0` gives 0 |
| `bool lp_coord_inside(const lp_coord *c)` | `Σ m² ≤ 2^106`, exactly, in 128-bit |
| `uint64_t lp_hilbert4(const lp_coord *c)` | the 4D Hilbert value on the 16-bit grid over `[−1, 1]^4`, the grid taken in IEEE double exactly as tier 0 was generated |
| `uint64_t lp_hilbert4_grid(const uint32_t g[4])` | the same from grid coordinates |

## Geometry packing: geometry.c

| Function | Contract |
| --- | --- |
| `void lp_id_to_xyz(const lp_id *id, double xyz[3])` | the 128 bits into the X, Y, Z mantissas, 43 + 43 + 42, exponent −2, values in `[0.25, 0.5)` |
| `void lp_xyz_to_id(const double xyz[3], lp_id *out)` | the inverse, exact, read through the ID's own 43, 43 and 42 bits (`lp_xyz_id_mask[3]`): the spare bits do not change which entity a vertex is |
| `size_t lp_ewkb_path(const lp_id *children, size_t n, uint8_t *out, size_t cap)` | EWKB for a path: POINT ZM when there is one run, else LINESTRING ZM, one vertex per run of identical children with the run length in M; returns bytes written, or bytes needed if `cap` is too small, 0 for `n == 0` |
| `size_t lp_ewkb_runs(const lp_id *ids, const uint64_t *m, size_t nv, uint8_t *out, size_t cap)` | the same from runs already collapsed; `m[i]` is M as it is written, run and said bits (`lp_m_of`) |
| `size_t lp_ewkb_runs_spare(const lp_id *ids, const uint64_t *m, const uint32_t *spare, size_t nv, uint8_t *out, size_t cap)` | the same, each vertex carrying a value in its spare bits (`spare[i]`; 0 none; NULL none at all) |
| `LP_SPARE_BITS` 28, `LP_SPARE_TAG_BITS` 4; `lp_spare_of(tag, payload)`, `lp_spare_tag(v)`, `lp_spare_payload(v)`; `uint32_t lp_xyz_spare(const double xyz[3])`, `void lp_xyz_spare_set(double xyz[3], uint32_t v)` | a vertex's 28 spare bits: bits 0 to 3 the layout's tag, 4 to 27 its payload |
| `size_t lp_path_ids(ewkb, len, lp_id *out, size_t cap)`, `size_t lp_path_vertices(ewkb, len, lp_vertex *out, size_t cap)` | a path's IDs in order, runs expanded; or its vertices, `lp_vertex { id; run; said; spare; outcome; position; }` (`lp_ewkb_enrich_path` merges compatible annotations over identical constituents) |
| `lp_m_bits`, `lp_m_run`, `lp_m_said`, `lp_m_outcome`, `lp_m_position`, `lp_m_of`, `lp_m_full`, `lp_outcome_of`, `lp_outcome_score` | a vertex's M: run in bits `0..29`, `said` in bits `30..32` (`1..7`), `outcome` in bits `33..34` (`WIN = 0`, `DRAW = 1`, `LOSS = 2`, `SCORE = 3` with `LP_SPARE_SCORE = 1`), and `position` in bits `35..52` |
| `size_t lp_ewkb_point4(const double xyzm[4], uint8_t *out, size_t cap)` | a POINT ZM of real coordinates, 37 bytes (`geometry.h` adds `lp_ewkb_visit` and `lp_ewkb_line_zm`/`polygon_zm`/`collection_zm`) |
| `size_t lp_ewkb_vertices(const uint8_t *ewkb, size_t len, const uint8_t **vertices)` | parse a POINT ZM or LINESTRING ZM, little-endian, optional SRID; the vertex count and a pointer to the first 32-byte vertex; 0 on malformed input |

## Trajectory matching: follows.c

`size_t lp_follows(const uint8_t *ewkb, size_t len, const lp_id *phrase, size_t np, lp_id *out, size_t cap)` and `lp_precedes(...)`: every place the phrase occurs as a run inside the path, vertices expanded by run length, returning the ID of the vertex after (`lp_follows`) or before (`lp_precedes`) it. The phrase is encoded once into vertex bytes; a SIMD scan finds candidate starts by the phrase's first vertex's 24 bytes of X, Y, Z; the rest of the window is compared through the ID's own bits (`lp_xyz_id_mask`) in the scalar, AVX2 and AVX-512 kernels alike, so spare values do not hide a match; only continuations are decoded. Returns the matches found; at most `cap` are written. Measured at one core's memory bandwidth, 14.2 GB/s scalar and 15.0 GB/s AVX2.

## Shape measures and S³: geom4d.c, s3.c

On `n × 4` doubles of real coordinates, never packed vertices:

| Function | Measure | With a stray vertex | With a repeat |
| --- | --- | --- | --- |
| `double lp_distance4(const double a[4], const double b[4])` | Euclidean distance | | |
| `double lp_frechet4(a, na, b, nb)` | discrete Fréchet (Eiter and Mannila), row by row in `O(nb)` memory; the distance, not its square; a metric | one stray vertex sets the distance | nothing |
| `double lp_frechet4_outliers(a, na, b, nb, unsigned k)` | the same with up to *k* interior vertices of each skipped, three rows of state kept | skipping it gives 0 | nothing |
| `double lp_dtw4(a, na, b, nb, size_t *steps)` | the sum of gaps along the best walk; `steps` the walk's length | adds its distance once | absorbed |
| `size_t lp_edr4(a, na, b, nb, double eps)` | edits, vertices within `eps` counting as equal | one edit | one edit |
| `double lp_hausdorff4(a, na, b, nb)` | undirected Hausdorff distance, order-invariant | one stray vertex sets it | nothing |
| `bool lp_centroid4_exact(const double *points, size_t n, double out[4])` | the exact centroid of fixed-point points; false if any coordinate is not `m / 2^53` | | |
| `lp_angle4`, `lp_angle4_batch`, `lp_s3_log`, `lp_s3_exp`, `lp_slerp4`, `lp_karcher_mean4`, `lp_eigen_centroid4` | unit-direction angles in `[0, π]`, geodesic log/exp/SLERP, canonical-order Karcher mean, and cyclic-Jacobi Markley average on S³ | | |

Measured: discrete Fréchet on 1,000 × 1,000 vertices, 3.8 ms; 4D squared distances 1.1 G/s scalar, 1.4 G/s AVX2; on 60-point trajectories one outlier scores 1.39 against 1.72 for an unrelated sequence, the same pair with the outlier skipped 0, jitter the size of those fields 0.087.

## Model and linear-algebra kernels: rowsig.c, knn.c, linalg.cpp

- `int lp_mkl_reproducible(void)`: pins Intel MKL CNR to strict AVX2 conditional numerical reproducibility before any MKL call so every machine produces identical bits (`lp_rowsig` and `lp_knn_exact` call it automatically).
- `size_t lp_rowsig(const float *A, size_t m, const float *B, size_t n, size_t r, float scale, float zmin, uint32_t cap, lp_rowsig_hit *out, size_t out_cap, lp_rowsig_stats *stats)`: for each row *a* of *A*, scores against every row of *B* scaled, computes the row's mean and spread over all *n*, and emits candidates above `mean + zmin · sd`, at most `cap` per row, highest first; `lp_rowsig_hit { row, col, score, z }`; `lp_rowsig_stats { rows, candidates, above[3] (z ≥ zmin, 4, 5), rows_without, flops }`. Needs MKL (`Laplace::model`); called per circuit by `laplace model`.
- `int lp_knn_exact(...)` / `lp_knn_exact_d(...)` (`knn.c`, `Laplace::model`): exact *k* nearest neighbors by squared Euclidean distance summed in `double` in dimension order, ordered by `(distance, base_row_index)` independently of OpenMP thread count.
- `lp_eigenmap`, `lp_procrustes`, `lp_gram_schmidt` (`linalg.h`, `Laplace::linalg`): Laplacian eigenmaps (Spectra symmetric Lanczos), orthogonal Procrustes (JacobiSVD), and Householder QR orthonormalization over scalar fixed-blocking Eigen.

## Consensus: consensus.c, consensus.h

| Function | Contract |
| --- | --- |
| `void lp_glicko2(lp_rating *r, const lp_rating *opponents, const double *scores, size_t n, double tau)` | one conventional rating period against *n* opponents: Glickman's steps 1 to 8, volatility by the Illinois algorithm to `ε = 1e−6` |
| `void lp_matchup(lp_rating *r, const lp_rating *opponent, double score, double tau)` | one matchup as it arrives: no rating period, so deviation is never widened for elapsed time |
| `const lp_trust_class *lp_trust_class_named(const char *label)`, `lp_trust_class_at(size_t i)`, `lp_trust_class_count(void)`, `lp_trust_class_for_id(text, id)` | the trust-class law generated at build time from `manifest/trust_classes.toml` into `trust_class_law.h` (`trust.c`); unknown labels return NULL |
| `double lp_trust_deviation(double trust)` | the deviation φ where `g(φ) = \|t\|`: `173.7178 · (π/√3) · √(1/t² − 1)` (`0` at `\|t\| = 1`, `∞` at `0`) |
| `double lp_series_floor(double trust, double floor)` | the least deviation one witness of trust `t` can bring a claim to: `clamp(lp_trust_deviation(t), floor, LP_GLICKO_DEVIATION)` (trust `0.95`: `103.6`, `0.9`: `152.6`, `≤ 0.669`: `350`) |
| `void lp_attest_series(lp_rating *r, double trust, uint32_t games, double score, double floor)` | one witness's game series on a claim solved in `O(1)` by bisection on the concave log-posterior slope against the `1500` anchor (`g = 1`): negative trust flips `score` first, then `s_eff = 0.5 + \|t\|(score − 0.5)` pulls the mean outcome toward a draw so repetition never crosses the witness's trust ceiling (`2011.5` at trust `0.9`, `1570.4` at `0.2`), and `deviation` never falls below `lp_series_floor(trust, floor)` ([13. Consensus](../Sequence/Consensus.md) operation 13.2) |
| `void lp_attest(lp_rating *r, double trust, double score, double opponent_rating, double tau, double floor)` | single-matchup update at `opponent_rating` with `lp_trust_deviation(trust)` and `floor` |
| `bool lp_series(entries, n, out)`, `lp_series_update(prior, entries, n, out)`, `lp_series_evaluate(prior, entries, n, out, info, cap, written)`, `lp_witness_precision(trust, floor)` | (`consensus.h`) order-independent rooted multi-source posterior over `lp_series_entry`: folds shared `dependence_root` observations (`LP_SAID_DEPENDENCE = 7`) so source copies saturate at `1/ω_r²` while independent roots add Fisher precision, returning exact per-root curvature `lp_series_information` for `share_bp = 10000` attribution |
| `double lp_confidence(const lp_rating *r, double k)` | `σ((rating − 1500)/173.7178 − k · deviation/173.7178)` |
| `double lp_cost(const lp_rating *r, double k, double per_hop)` | `−ln(confidence) + per_hop`, computed as `log1p(e^−x) + per_hop` |
| `bool lp_series_attested(lp_id root, double games, double wins, double trust, lp_series_entry *out)` | validates an `attestation` row (`games` whole in `[1, 2^53]`, `wins` in `[0, games]`, signed `trust` in `[−1, 1]`) into a canonical `lp_series_entry` |
| `lp_tally`, `lp_tally_add`, `lp_tally_edge(t, count, times, record, outcome, spare, position)` | tallies containment testimony (`games`, `tokens`, `wins`, least positive `position`) |
| `lp_dag_multiplicity`, `lp_dag_order`, `lp_dag_count`, `lp_dag_count_reach`, `lp_dag_count_exact` | topological DAG multiplicity counters (`ELOOP` on cycles, `EOVERFLOW` past `2^64 − 1`) shared by Engine ingest/replay and PostgreSQL containment/attribution |

Golden: `1500/200/0.06` against `1400/30` win, `1550/100` loss, `1700/300` loss, τ 0.5, gives `1464.06 / 151.52 / 0.05999`. Trust 0.9 plays at deviation 152.6, 0.669 at 350. A standing of 1774.3 with deviation 93.3 reads 0.829 at *k* = 0 and 0.624 at *k* = 2, cost 0.472 at *k* = 2. Measured 7.8 M matchups per second per core.

## Tier 0: tier0.c, tier0_map.c (`tier0.h`)

| Function | Contract |
| --- | --- |
| `const char *lp_tier0_path(void)` | `$LAPLACE_TIER0`, else the path compiled in |
| `const lp_tier0_record *lp_tier0_map(const char *path)` | memory-map 1,114,112 ID-sorted records read-only and shared; NULL if missing, malformed, or unsorted (`lp_tier0_at(t0, cp)` in `tier0.h` resolves by codepoint) |
| `int64_t lp_tier0_codepoint(const lp_tier0_record *t0, const lp_id *id)` | the codepoint with this ID, or −1; `O(1)` (`lp_tier0_find` returns the record) |
| `void lp_tier0_fingerprint(const lp_tier0_record *t0, uint8_t out[32])` | BLAKE3-256 of the table |
| `lp_ref lp_ref_atom(const lp_tier0_record *t0, uint32_t cp)` | the codepoint as a reference: its ID, coordinate, tier 0 |

`tier0.bin` (68 MB) also shards into four disjoint branch files while preserving exact global BLAKE3 IDs and 4D Super-Fibonacci coordinates (`tier0.h`): `tier0.ascii.bin` (128 records, 8 KB), `tier0.utf.bin` (22,112 records, 1.35 MB), `tier0.cjk.bin` (115,920 records, 7.08 MB), and `tier0.ext.bin` (975,952 records, 59.57 MB), selectable via `LAPLACE_TIER0_PROFILE` or `@profile` path suffixes (`lp_tier0_map_branches`).

## The flags: flags.c

| Function | Contract |
| --- | --- |
| `const char *lp_flags_path(void)` | `$LAPLACE_FLAGS`, else tier 0's path with `.flags` in place of its ending |
| `const lp_layout *lp_flags_map(const char *path)` | map the records and read `path.layout`; NULL if either is missing or the records are not `LP_NCP × 32` bytes |
| `const lp_layout *lp_flags_map_branches(const char *path, uint32_t mask)` | map the requested branch shards (`tier0.flags.ascii.bin`, `tier0.flags.utf.bin`, `tier0.flags.cjk.bin`, `tier0.flags.ext.bin`) along the same four codepoint branches as tier 0 (`34 MB` full) |
| `const lp_field *lp_flags_field(const lp_layout *, const char *property)` | a field by short or long name, by the standard's matching rule; NULL if none |
| `uint32_t lp_flags_get(const lp_layout *, uint32_t cp, const lp_field *)` | 0 or 1 for a binary property; a value's place in its list for an enumerated one |
| `int32_t lp_flags_value(const lp_layout *, const lp_field *, const char *value)` | a value's place by short or long name; −1 if the list does not hold it |
| `bool lp_name_same(const char *a, size_t al, const char *b, size_t bl)` | UAX #44 LM3: case, spaces, underscores, and hyphens do not count |

## Composition: compose.c

`lp_ref { lp_id id; lp_coord c; uint8_t tier; uint8_t said; uint8_t outcome; uint32_t position, spare; }`: an entity as it is composed; `said`, `outcome`, `position`, and `spare` belong to the vertex within its parent path and are never part of any ID.

| Function | Contract |
| --- | --- |
| `lp_ref lp_ref_compose(const lp_ref *children, size_t n, uint8_t tier)` | ID from the children's, coordinate the exact average of theirs, and tier `1 + max(child.tier)` (`lp_tier_above`); one child (`n == 1`) is that child unchanged (`lp_ref_compose_runs` composes directly from RLE runs) |
| `typedef lp_ref (*lp_compose_fn)(void *sink, const lp_ref *children, uint32_t n, uint8_t tier)` | what receives every composition as it is made and returns it: the engine's node table, or NULL to compose without recording, as the database does |
| `size_t lp_factor(const lp_ref *children, size_t n, lp_ref *out, lp_compose_fn compose, void *sink)` | repeats within a composition, factored from the content alone: a block of two or more constituents repeated adjacently becomes one entity, composed through `compose`/`sink` one tier above its highest constituent, and stands in the sequence once per repeat, so the path writer makes the run. Leftmost, the shortest period, recursive, so the same content always factors the same way. A repeated single constituent is a run already and is left as it is. `out` holds at most `n`; the count written is returned |

## Text: text.c, laplace_text

UAX #29 through ICU's break iterators: codepoint → grapheme → word segment → sentence → paragraph → text, where `n == 1` collapses to its single child and every composition of `n >= 2` children has `tier = 1 + max(child.tier)`. Nothing is dropped, so the text recomposes byte for byte. A single line break inside a paragraph is read as a space for segmentation only; the bytes recorded are the original. One `lp_text` per thread. This is the one decomposition of text in Laplace: the engine records what it composes, the database composes without recording.

| Function | Contract |
| --- | --- |
| `lp_text *lp_text_new(const lp_tier0_record *t0)` | opens the sentence, word, and character break iterators once |
| `lp_ref lp_text_decompose(lp_text *, const uint8_t *s, size_t n, lp_compose_fn compose, void *sink)` | the text's trunk (`lp_text_segments` and `lp_text_decompose_segments` visit exact word-segment occurrences in source order) |
| `lp_ref lp_text_parts(lp_text *, const uint8_t *s, size_t n, lp_ref *parts, size_t cap, size_t *nparts)` | the same, also the trunk's own constituents in order, repeats included; a trunk that is one codepoint has itself as its only part |

Realization is the inverse, one walk for every reader (`realize.c`): `lp_realize(w, t0, root, mode, reader, sink, ctx, &result)` walks a DAG the caller supplies through `lp_realize_reader` (an id answers KNOWN with its children `{id, run, said}` and flags TUPLE/OPAQUE/SCALAR, PENDING when not yet fetched, or ABSENT), writing tier-0 codepoints as UTF-8 to `lp_realize_sink`, which can stop the walk. `LP_REALIZE_TEXT` is the exact text: each child its run times, and a record reads as its thing, so CLAIM and VOICE vertices are left out. `LP_REALIZE_LABELS` is the display form: a run once with `× n`, children joined by ` · `, a non-text node as its hex ID. Iterative, no allocation per node; a reusable `lp_realizer` workspace keeps the active path and known surfaces; a cycle is ELOOP. Callers: `laplace_text`, `laplace_text_batch`, `laplace_labels`, `laplace_resolve_refs`, `laplace_claim_preview` (extension) and the Engine's `reader_text` (CLI and MCP).

Golden: `[H,o,l,m,e,s]` is a tier-1 word of 6 parts; `Sherlock Holmes` is tier 2 with 3 parts, the space a codepoint, its coordinate the average of its constituents' and inside the wall; one codepoint is that codepoint.

## The pull's frontier: pull.c

The open set of a best-first search over rated claims, Dijkstra or A*: entities by ID in O(1), the entity of least order in O(log n); costs only fall, so an entity reached again more cheaply is queued again and its older entry passed over when it surfaces.

| Function | Contract |
| --- | --- |
| `lp_frontier *lp_frontier_new(void)`, `void lp_frontier_free(lp_frontier *)` | |
| `bool lp_frontier_reach(f, id, from, claim, cost, estimate, hops)` | reach `id` at this cost through `claim` from `from`, `estimate` the lower bound of the remaining cost, 0 for Dijkstra; true if this is the cheapest chain so far; a closed entity stays closed |
| `const lp_reached *lp_frontier_next(f)` | close and return the open entity of least `cost + estimate`, or NULL |
| `double lp_frontier_least(f)` | the least order among open entities, or infinity |
| `const lp_reached *lp_frontier_find(f, id)`, `size_t lp_frontier_count(f)` | |

`lp_reached { id, from, claim; double cost, order; uint32_t hops; bool closed; }`.

## The highway and perf-caches: highway.c (`highway.h`), perfcache.c (`perfcache.h`)

The third perf-cache: one record per type, in the form of a tier-0 record whose rank is the type's slot, the lists in order, then the edges between them ([Formats: The highway's files](Formats.md#the-highways-files)).

| Function | Does |
| --- | --- |
| `const char *lp_highway_path(void)` | `$LAPLACE_HIGHWAY`, or tier 0's path with `.highway` |
| `const lp_highway *lp_highway_map(const char *path)` | memory-maps the single-file highway and reads its layout, keys, and identifier components; NULL when missing or invalid |
| `const lp_highway *lp_highway_map_branches(const char *path, uint32_t branches)` | maps the highway under modular domain shards (`CORE`, `WORDNET`, `FRAMES` via `LAPLACE_HIGHWAY_PROFILE`) |
| `const lp_list *lp_highway_list(h, name)` | a list by name: its name, title, first record and count |
| `const lp_tier0_record *lp_highway_at(h, list, slot)`, `int64_t lp_highway_slot(h, list, id)` | a slot's record; a type's slot by its content's ID, -1 when the list has none |
| `int64_t lp_highway_key(h, list, key)`, `lp_highway_resolve(h, ns, key)`, `lp_highway_find(h, id)` | resolves local or cross-list source keys and canonical records in `O(1)` |
| `size_t lp_highway_edges(h, a, slot, b, const lp_edge **out)` | the slots of list `b` a slot of list `a` maps to |
| `void lp_highway_fingerprint(h, uint8_t out[32])` | the highway's BLAKE3-256 fingerprint |
| `const lp_bank *lp_highway_bank(h, name)`, `const lp_bank *lp_highway_bank_of(h, id, int32_t *bit)` | a bank by name; the bank a type belongs to, and its slot. `lp_bank { name, group, carrier, width, list, offset, flags }` |
| `lp_mask_field`, `lp_mask_put`, `lp_mask_has`, `lp_mask_get`, `lp_mask_clear`, `lp_mask_merge`, `lp_mask_add_id` | disjoint 64-bit carrier operations (`kind` flags + `slot + 1` closed enums) |
| `LP_KIND_CLAIM` 0, `LP_KIND_RECORD` 1, `LP_KIND_TUPLE` 2, `LP_KIND_FILE` 3, `LP_MASK_BITS` **64** | the `kind` bank's flag bits and the 64-bit mask width |
| `lp_perfcache_write`, `lp_perfcache_map`, `lp_perfcache_at`, `lp_perfcache_find`, `lp_perfcache_pair` | (`perfcache.h`) generic `LPPC0001` ROM container bound to `tier0.bin`'s fingerprint (`chess.bin`) |

## Helpers and JSON: ids.c, wire.c, json.c

`lp_idmap_*` and `lp_strmap_*` provide deterministic open-addressing maps preserving insertion order; `lp_be(p, n)`, `lp_be_f64(p)`, `lp_pg_ids`, and `lp_copy_*` read and write PostgreSQL binary wire arrays and `COPY` streams; `lp_json_parse`, `lp_json_get`, and `lp_json_str` (`json.h`) parse and emit RFC 8259 JSON across the CLI and HTTP/MCP tools.
