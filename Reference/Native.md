# Native

Laplace-Native's one header, `include/laplace/laplace.h`, declares every shared operation: identity, UTF-8, tier 0 and its flags, fixed-point coordinates, composition, text decomposition, geometry packing, trajectory matching, shape measures, consensus, the model kernel, and the pull's search frontier; every function is deterministic, the same bits on every CPU whichever SIMD path runs.

Laplace-Engine and Laplace-postgres call these and keep no copy of any of them. Three libraries: `laplace` holds everything but the next two; `laplace_text` holds the decomposition of text and needs ICU 78; `laplace_model` holds the model kernel and needs MKL and OpenMP.

## Constants and dispatch

| Name | Value | Meaning |
| --- | --- | --- |
| `LP_NCP` | 1114112 | codepoints in the codespace |
| `LP_FIXED_ONE` | 2^53 | a coordinate `m` has the value `m / 2^53` |
| `LP_GLICKO_SCALE` | 173.7178 | Glicko-2's scale |
| `LP_M_RUN_BITS` | 30 | the low bits of M that hold a run length |
| `LP_SAID_CLAIM`, `LP_SAID_RECORD`, `LP_SAID_TUPLE`, `LP_SAID_METADATA` | 1, 2, 3, 4 | what a vertex is, above the run bits of M |
| `LP_CPU_SSE2` … `LP_CPU_AMX` | bit flags | SSE2, SSE4.1, AVX2 with FMA and BMI2 (x86-64-v3), AVX-512 F/BW/VL/DQ (x86-64-v4), AVX-512 VNNI, AVX-VNNI, AMX |

`lp_cpu_features()` reads `cpuid` once: what the CPU and the OS (`xgetbv`) support. `lp_cpu_active()` is the level the dispatcher uses, `LAPLACE_ISA` lowering it to `scalar`, `sse2`, `avx2`, or `avx512` and never raising it. `lp_cpu_describe(f)` names a feature set. Kernels with a SIMD variant: the vertex scan (`scalar`, `avx2`, `avx512`), the 4D squared-distance row (`scalar`, `avx2`), the Hilbert interleave (`scalar`, `bmi2`). Every summation has one fixed order in every path, `((dx² + dy²) + dz²) + dm²`, and the SIMD kernels put one vertex pair per lane rather than one axis per lane to keep it.

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
| `void lp_xyz_to_id(const double xyz[3], lp_id *out)` | the inverse, exact |
| `size_t lp_ewkb_path(const lp_id *children, size_t n, uint8_t *out, size_t cap)` | EWKB for a path: POINT ZM when there is one run, else LINESTRING ZM, one vertex per run of identical children with the run length in M; returns bytes written, or bytes needed if `cap` is too small, 0 for `n == 0` |
| `size_t lp_ewkb_runs(const lp_id *ids, const uint32_t *runs, size_t nv, uint8_t *out, size_t cap)` | the same from runs already collapsed; `runs[i]` is M as it is written, run and said bits |
| `size_t lp_ewkb_point4(const double xyzm[4], uint8_t *out, size_t cap)` | a POINT ZM of real coordinates, 37 bytes |
| `size_t lp_ewkb_vertices(const uint8_t *ewkb, size_t len, const uint8_t **vertices)` | parse a POINT ZM or LINESTRING ZM, little-endian, optional SRID; the vertex count and a pointer to the first 32-byte vertex; 0 on malformed input |

## Trajectory matching: follows.c

`size_t lp_follows(const uint8_t *ewkb, size_t len, const lp_id *phrase, size_t np, lp_id *out, size_t cap)`: every place the phrase occurs as a run inside the path, vertices expanded by run length, the ID of the vertex that follows it. The phrase is encoded once into vertex bytes; a SIMD scan finds candidate starts by the phrase's first vertex's 24 bytes of X, Y, Z; the rest of the window is compared byte for byte; only continuations are decoded. Returns the continuations found; at most `cap` are written. Measured at one core's memory bandwidth, 14.2 GB/s scalar and 15.0 GB/s AVX2.

## Shape measures: geom4d.c

On `n × 4` doubles of real coordinates, never packed vertices:

| Function | Measure | With a stray vertex | With a repeat |
| --- | --- | --- | --- |
| `double lp_distance4(const double a[4], const double b[4])` | Euclidean distance | | |
| `double lp_frechet4(a, na, b, nb)` | discrete Fréchet (Eiter and Mannila), row by row in `O(nb)` memory; the distance, not its square; a metric | one stray vertex sets the distance | nothing |
| `double lp_frechet4_outliers(a, na, b, nb, unsigned k)` | the same with up to *k* interior vertices of each skipped, three rows of state kept | skipping it gives 0 | nothing |
| `double lp_dtw4(a, na, b, nb, size_t *steps)` | the sum of gaps along the best walk; `steps` the walk's length | adds its distance once | absorbed |
| `size_t lp_edr4(a, na, b, nb, double eps)` | edits, vertices within `eps` counting as equal | one edit | one edit |
| `bool lp_centroid4_exact(const double *points, size_t n, double out[4])` | the exact centroid of fixed-point points; false if any coordinate is not `m / 2^53` | | |

Measured: discrete Fréchet on 1,000 × 1,000 vertices, 3.8 ms; 4D squared distances 1.1 G/s scalar, 1.4 G/s AVX2; on 60-point trajectories one outlier scores 1.39 against 1.72 for an unrelated sequence, the same pair with the outlier skipped 0, jitter the size of those fields 0.087.

## The model kernel: rowsig.c, laplace_model

`size_t lp_rowsig(const float *A, size_t m, const float *B, size_t n, size_t r, float scale, float zmin, uint32_t cap, lp_rowsig_hit *out, size_t out_cap, lp_rowsig_stats *stats)`: for each row *a* of *A*, scores against every row of *B* scaled, the row's mean and spread over all *n*, and the candidates above `mean + zmin · sd`, at most `cap` per row, highest first; `lp_rowsig_hit { row, col, score, z }`; `lp_rowsig_stats { rows, candidates, above[3] (z ≥ zmin, 4, 5), rows_without, flops }`. Needs MKL. The engine's `laplace model` calls it per circuit.

## Consensus: consensus.c

| Function | Contract |
| --- | --- |
| `void lp_glicko2(lp_rating *r, const lp_rating *opponents, const double *scores, size_t n, double tau)` | one rating period against *n* opponents: Glickman's steps 1 to 8, the volatility by the Illinois algorithm to `ε = 1e−6` |
| `void lp_matchup(lp_rating *r, const lp_rating *opponent, double score, double tau)` | one matchup as it arrives: no rating period, so the deviation is never widened for time gone by; it changes only by what the matchup tells |
| `double lp_trust_deviation(double trust)` | the deviation a witness of trust *t* plays with, the φ with `g(φ) = abs(t)`: `173.7178 · (π/√3) · √(1/t² − 1)`; 0 at trust 1, infinity at 0 |
| `void lp_attest(lp_rating *r, double trust, double score, double opponent_rating, double tau, double floor)` | one attestation as one matchup: the witness plays at `opponent_rating` with the deviation its trust gives and volatility 0.06; trust < 0 flips the score; trust 0 changes nothing; the deviation never falls below `floor` |
| `double lp_confidence(const lp_rating *r, double k)` | `σ((rating − 1500)/173.7178 − k · deviation/173.7178)` |
| `double lp_cost(const lp_rating *r, double k, double per_hop)` | `−ln(confidence) + per_hop`, computed as `log1p(e^−x) + per_hop` |

Golden: `1500/200/0.06` against `1400/30` win, `1550/100` loss, `1700/300` loss, τ 0.5, gives `1464.06 / 151.52 / 0.05999`. Trust 0.9 plays at deviation 152.6, 0.669 at 350. A standing of 1774.3 with deviation 93.3 reads 0.829 at *k* = 0 and 0.624 at *k* = 2, cost 0.472 at *k* = 2. Measured 7.8 M matchups per second per core.

## Tier 0: tier0.c

| Function | Contract |
| --- | --- |
| `const char *lp_tier0_path(void)` | `$LAPLACE_TIER0`, else the path compiled in |
| `const lp_tier0_record *lp_tier0_map(const char *path)` | memory-map the table read-only and shared; NULL if the file is missing or not exactly `LP_NCP × 64` bytes; NULL or "" for the default path |
| `int64_t lp_tier0_codepoint(const lp_tier0_record *t0, const lp_id *id)` | the codepoint with this ID, or −1; O(1) from a 4 M-slot open-addressed table built on first use over the IDs' own bits |
| `void lp_tier0_fingerprint(const lp_tier0_record *t0, uint8_t out[32])` | BLAKE3-256 of the table |
| `lp_ref lp_ref_atom(const lp_tier0_record *t0, uint32_t cp)` | the codepoint as a reference: its ID, coordinate, tier 0 |

## The flags: flags.c

| Function | Contract |
| --- | --- |
| `const char *lp_flags_path(void)` | `$LAPLACE_FLAGS`, else tier 0's path with `.flags` in place of its ending |
| `const lp_layout *lp_flags_map(const char *path)` | map the records and read `path.layout`; NULL if either is missing or the records are not `LP_NCP × 32` bytes |
| `const lp_field *lp_flags_field(const lp_layout *, const char *property)` | a field by short or long name, by the standard's matching rule; NULL if none |
| `uint32_t lp_flags_get(const lp_layout *, uint32_t cp, const lp_field *)` | 0 or 1 for a binary property; a value's place in its list for an enumerated one |
| `int32_t lp_flags_value(const lp_layout *, const lp_field *, const char *value)` | a value's place by short or long name; −1 if the list does not hold it |
| `bool lp_name_same(const char *a, size_t al, const char *b, size_t bl)` | UAX #44 LM3: case, spaces, underscores, and hyphens do not count |

## Composition: compose.c

`lp_ref { lp_id id; lp_coord c; uint8_t tier; uint8_t said; }`: an entity as it is composed; `said` is what it is within the path it is put in and never part of its ID.

| Function | Contract |
| --- | --- |
| `lp_ref lp_ref_compose(const lp_ref *children, size_t n, uint8_t tier)` | ID from the children's, coordinate the exact average of theirs; one child is that child |
| `typedef lp_ref (*lp_compose_fn)(void *sink, const lp_ref *children, uint32_t n, uint8_t tier)` | what receives every composition as it is made and returns it: the engine's node table, or NULL to compose without recording, as the database does |

## Text: text.c, laplace_text

UAX #29 through ICU's break iterators: codepoint → grapheme → word segment → sentence → paragraph → text, tiers 0 to 5. Nothing is dropped, so the text recomposes byte for byte. A single line break inside a paragraph is read as a space for segmentation only; the bytes recorded are the original. One `lp_text` per thread. This is the one decomposition of text in Laplace: the engine records what it composes, the database composes without recording.

| Function | Contract |
| --- | --- |
| `lp_text *lp_text_new(const lp_tier0_record *t0)` | opens the sentence, word, and character break iterators once |
| `lp_ref lp_text_decompose(lp_text *, const uint8_t *s, size_t n, lp_compose_fn compose, void *sink)` | the text's trunk |
| `lp_ref lp_text_parts(lp_text *, const uint8_t *s, size_t n, lp_ref *parts, size_t cap, size_t *nparts)` | the same, also the trunk's own constituents in order, repeats included; a trunk that is one codepoint has itself as its only part |

Golden: `[H,o,l,m,e,s]` is a tier-2 word of 6 parts; `Sherlock Holmes` is tier 3 with 3 parts, the space a codepoint, its coordinate the average of its constituents' and inside the wall; one codepoint is that codepoint.

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
