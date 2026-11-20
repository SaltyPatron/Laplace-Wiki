# Architecture boundaries

Architecture boundaries state which layer owns which law: the native engine owns every semantic operation, and SQL and C# orchestrate generated typed bindings to it.

> [!IMPORTANT]
> These boundaries apply across every active Laplace repository (`Laplace-Native`, `Laplace-postgres`, `Laplace-Engine`, `Laplace-MCP`, `Laplace-UCI`, `Laplace-Operations`, and `Laplace`). `Laplace` (the product application) converges onto the modular `Laplace-Native` + `Laplace-postgres` + `Laplace-Engine` packages (`one-substrate`) so every semantic law has one native implementation.

## Authority flow

```text
 External callers (OpenAI /v1/*, Web/Glome, Chess Lab, Foundry, Arena, MCP, UCI, CLI)
               |                                      |
               v                                      v
 C# thin hosts (Laplace.Hosting/Data/Mcp)    Native CLI/HTTP/UCI (Laplace-Engine, lpm)
               |                                      |
               +-------------------+------------------+
                                   |
          +------------------------+------------------------+
          | (0 DB round-trips)                              | (indexed binary probes & stage COPY)
          v                                                 v
 In-process Laplace-Native C                       PostgreSQL 18 + PostGIS + Laplace-postgres
 + mmap'd ROMs (tier0, flags, highway, chess)      + same Laplace-Native C beside GIN/GiST/B-tree
                                                            |
                                                            v
                                                   4 canonical substrate tables
                                                   (entity, physicality, attestation, consensus)
                                                   + app.* operational/billing tables
```

SQL and C# are peer orchestrators. Neither is a semantic layer above the other and neither becomes a second engine. Modularity in Laplace is **compounding overlap in one shared space, never vertical feature silos**: every corpus, lexicon, repository, `.git` history, compiler symbol graph, PGN archive, media stream, and Safetensors/GGUF checkpoint decomposes into the same 16-byte BLAKE3 IDs across the same four tables, and one C `Forward + Highway A* + Gödel` program (`program.c`) steered by detached `.firmware` profiles serves conversation, code construction, chess, and discovery without domain-specific engine forks.

## Pure C17 core (`Laplace-Native`)

`Laplace-Native` is pure C17 compiled with `icx` (`-fp-model=precise`, `-ffp-contract=off`), plus `src/linalg.cpp` wrapping scalar Eigen and Spectra (`lp_eigenmap`, `lp_procrustes`, and Householder QR Gram-Schmidt) behind a pure `extern "C"` ABI (`include/laplace/linalg.h`, compiled with `EIGEN_DONT_VECTORIZE`, `EIGEN_NO_CPUID`, and `EIGEN_DONT_PARALLELIZE`). It owns:

- **Content identity (`lp_id`):** 16-byte BLAKE3-128 hashes (`uint8_t b[16]`) with zero domain byte, salt, tier prefix, or case folding; codepoint UTF-8 leaf hashing (`lp_id_codepoint`), singleton collapse (`n == 1` returns child `0`), ordered $16n$-byte child composition (`lp_id_compose`, `lp_ref_compose`), and intrinsic Merkle height (`tier = 1 + max(child.tier)`).
- **Memory-mapped fingerprinted ROMs:** `tier0.bin` (all 1,114,112 Unicode codepoints on the $S^3$ surface in DUCET/Super-Fibonacci order), `tier0.flags` (256-bit Unicode Character Database property records + `.layout`), `highway.bin` (shared concept/frame/bank slots and crosswalk edges generated from `manifest/` + `tier0.bin`), and `chess.bin` (canonical chess board, position, and transition tables).
- **Segmentation and compositional scalars:** Tailored UAX #29 grapheme/word/sentence/paragraph breakdown (`src/text.c`), deterministic leftmost shortest-period block factoring (`lp_factor` in `src/compose.c`), and universal compositional scalars (`255` $\rightarrow$ `['2','5','5']`) shared across prose, code literals, IPv4 octets, RGB(A) channels, PCM samples, and mathematical constants.
- **4D geometry and Hilbert locality:** Exact `__int128`-accumulated integer centroids ($m / 2^{53}$, truncated toward zero) strictly inside the 4-ball ($\sum_{d=0}^3 m_d^2 \le 2^{106}$, `lp_coord_inside`) and 64-bit 4D Skilling/BMI2 `pdep` Hilbert keys (`lp_hilbert4`, `lp_hilbert_key`).
- **Mantissa trajectory carriers and 64-bit bank masks:** Binary EWKB `POINT ZM` / `LINESTRING ZM` packing (`src/geometry.c`), placing `43 + 43 + 42 = 128` child-ID bits plus `9 + 9 + 10 = 28` tagged spare bits (`4-bit tag + 24-bit payload`, such as `LP_SPARE_SCORE`) into IEEE-754 `binary64` X/Y/Z mantissas in `[0.25, 0.5)`, `53` exact integer metadata bits into `M` (`run30 / said3 / outcome2 / pos18`), and frozen 64-bit `manifest/banks.tsv` bitmasks (`kind`, `upos`, `lexfile`, `deprel`, `vnrole`, `wnframe`).
- **Realized-curve 4D shape metrics:** Euclidean 4-ball chord distance, $S^3$ angular separation, discrete Fréchet (`lp_frechet4d` and outlier-tolerant Fréchet), Dynamic Time Warping (`lp_dtw4d`), Edit Distance on Real sequence (`lp_edr4d`), and Hausdorff distance (`lp_hausdorff4d`) over unpacked real `entity.coord` curves.
- **Consensus, lineage trust, and Fisher attribution:** Concave log-posterior Glicko-2 series solving (`lp_series`, `lp_series_update`, `lp_series_evaluate`, `lp_attest_series`) with bounded signed witness trust ($s_{\text{eff}} = 0.5 + t(s - 0.5)$), shared `dependence_root` precision saturation ($1/\omega_r^2$), and rooted Fisher information royalty attribution (`share_bp = 10000` integer conservation).
- **Realization, search, shared primitives, and SIMD dispatch:** Deterministic UTF-8 realization (`lp_realize`), best-first A* search frontier (`lp_frontier`), OS/buffer/JSON helpers (`Laplace::os`, `lp_buf_*`, `laplace/json.h`), reproducible MKL pinning (`lp_mkl_reproducible()`), and one-time `cpuid`/`xgetbv` SIMD kernel selection (`src/cpu.c` over `scalar`, `sse2`, `avx2`, `avxvnni`, `avx512`, `avx512vnni`, capped by `LAPLACE_ISA` for parity testing).

## Client-determinism vs. in-database C split

Every semantic calculation lives once in `Laplace-Native` C, while execution splits cleanly between client RAM and PostgreSQL shared buffers according to **where the bytes already sit**:

- **In-process on the client (`0` DB round-trips):** `Laplace-Engine`, `Laplace-MCP`, `Laplace-UCI`, and C# (`Laplace.Native.Interop`) map `tier0.bin`, `tier0.flags`, `highway.bin`, and `chess.bin` directly into process memory and run pure deterministic operations locally — computing `lp_id`s, segmenting UAX #29 text, expanding `tier0.flags` case/property variants, computing 4D centroids and Hilbert keys, packing/unpacking EWKB path mantissas, encoding 64-bit `banks.tsv` masks, resolving highway slots and Syzygy tablebases, evaluating Fréchet/DTW/EDR on already-fetched curves, solving local Glicko-2 / Fisher math, and realizing UTF-8 (`lp_realize`) over cached paths. **Why:** because the ROMs are immutable and fingerprinted identically on client and server, crossing TCP, `libpq` framing, and the SQL executor for pure CPU/ROM math wastes round-trip latency and server cores while producing the exact same bits.
- **In-database in C (`Laplace-postgres`):** PostgreSQL (`laplace` DB) stores only the four canonical substrate tables (`entity`, `physicality`, `attestation`, `consensus`) plus `app.*` operational schemas, and exposes ~40 C-backed set probes and bulk stage routines: B-tree frontier presence and batch fetches (`laplace_present_ids`, `laplace_entities`, `laplace_physicalities`, `laplace_standings`), GIN containment, role, and mask scans (`laplace_path_ops`, `laplace_mask_ops`, `laplace_holders`, `laplace_held_files`, `laplace_claims_each`, `laplace_couple`, `laplace_pull`), 4D GiST box/angular k-NN and Hilbert ball pruning (`laplace_point4d_ops`, `laplace_angular4d_ops`, `laplace_hilbert_ball_ranges`), staged binary `COPY` merges and GIN pending-list cleanup (`laplace_merge_stage`, `laplace_enrich_stage`, `laplace_clean_stage`), cumulative series folding (`laplace_attest_series`), and containment royalty attribution (`laplace_attribution`, `laplace_source_attribution`). **Why:** these routines intersect posting lists, prune partitions, fold witness series, or walk upward containment across millions of index and heap pages; executing the C predicate next to the index keeps intermediate rows inside PostgreSQL shared buffers rather than shipping gigabytes of raw tuples over TCP. Pre-modular SQL catalogs (`extension/laplace_substrate`, `sql_catalog.def`) collapse into this split rather than being ported one-for-one.

## Engine, HTTP, and MCP (`Laplace-Engine`, `Laplace-MCP`, `Laplace-UCI`)

- **`Laplace-Engine` (`laplace` CLI and `LaplaceEngine` `reader.h`):** Owns ROM generation (`tier0`, `flags`, `highway`, `chess`), in-place database deployment and extension reconciliation (`src/deploy.c` + `laplace.reconcile.sql`), the generic Tree-sitter + compiled `.recipe` ingest VM (`src/recipe*.c`, `src/structure_*.c`, `src/say.c`, lock-free `src/table.c`, single-pass `stage.lp_*` binary `COPY`, per-witness `forget` and `sweep`), the single C `Forward + Highway A* + Gödel` loop (`src/program.c`, `src/pull.c`, `src/forward.c`) steered by detached `.firmware` files (`program.firmware`, `deductive.firmware`..`adversarial.firmware`, `chess.firmware`), shape-driven Safetensors/GGUF model assimilation (`raw_weight_bytes_retained = 0`) and native CPU Mold-a-Model `laplace-blake3-v1` checkpoint synthesis (`src/model.c`), and PGN/Syzygy chess pipelines (`src/chess.c`).
- **`Laplace-MCP` (`lpm` + `Laplace::http`) and `Laplace-UCI`:** Thin native HTTP/MCP and UCI protocol shells calling `Laplace-Native` and `LaplaceEngine` directly without duplicating substrate, retrieval, or search logic.

## C# product orchestration (`Laplace`)

Managed code in `Laplace` consists of thin host and transport assemblies (`Laplace.Hosting`, `Laplace.Data`, `Laplace.Mcp`, `Laplace.Native.Interop`) that own:

- **HTTP and OpenAI-compatible API (`/v1/*`):** Cleanly maps standard request fields (`messages[]`, `system`, `max_tokens`, `temperature`, `stop`, and `seed`) onto typed session/turn trajectories, `.firmware` selection, and compute envelopes executed by the native Forward loop, returning response text alongside proof/attribution metadata without C# prompt concatenation or managed token sampling.
- **Interactive product surfaces:** Web UI and 4D Glome explorer (always unpacking real `entity.coord` positions, never plotting raw `physicality.path` carrier mantissas), Chess Lab and Lichess bot streaming, Foundry / Recipe Studio, and the Knowledge Arena.
- **Tenancy, auth, and royalty accounting (`app.*`):** OIDC and API-key authentication, Knowledge Authority Package scoping, machine-cost Compute Envelopes, Patreon external entitlement witnessing, and `app.*` operational/billing tables (`app.billing_royalties` enforcing exact integer `SUM(share_bp) = 10000` conservation).

C# never computes BLAKE3 content IDs, segments or chunks text/code, case-folds strings, maintains per-format C# decomposers, blends heuristic search scores, or holds handwritten P/Invoke copies.

## Generated contracts

Cross-layer interfaces are generated deterministically from `Laplace-Native` headers and manifests and checked in CI so layers cannot drift:

- **Canonical C headers and manifests:** `Laplace-Native/include/laplace/*.h` and `Laplace-Native/manifest/{banks.tsv, slots/*.tsv, trust_classes.toml}` define all fixed-width ABI structs, `LP_API` entry points, 64-bit mask banks, highway slot vocabularies, and append-only witness trust priors.
- **PostgreSQL extension bindings:** `Laplace-postgres/manifest/function_bindings.tsv` (verified against `sql/*.sql*` and C exports by `Laplace-postgres/tools/check-function-bindings.mjs`) binds SQL functions and operator classes to `Laplace-Native` symbols and emits `laplace.reconcile.sql`.
- **Engine SQL contract:** `Laplace-Engine/src/pg_contract.h` and `pg_contract.c` (verified against `Laplace-postgres` by `Laplace-Engine/tests/sql-contract-gate.py`) bind every `libpq` binary prepared call to the extension's exact signature.
- **C# native interop (`Laplace.Native.Interop`):** `Laplace-Native/tools/csharp/generate.mjs` parses Clang's JSON AST (`-Xclang -ast-dump=json`) of the public headers to generate `LaplaceNative.g.cs` (`[LibraryImport("laplace")]` declarations, structs, and enum constants) plus `abi.g.c` and `Abi.g.cs` (verified by `csharp_abi` for exact struct size and field-offset parity on `win-x64` and `linux-x64`, rejecting platform-varying C types such as `long`, unions, or bit-fields), while `ReadPathArchitectureGateTests` enforces one-substrate read/write routing in `Laplace`.
