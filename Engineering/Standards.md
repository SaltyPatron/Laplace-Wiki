# Laplace engineering standards

These standards keep implementation choices subordinate to the complete invention.

They apply across every active Laplace repository: `Laplace-Native`, `Laplace-postgres`, `Laplace-Engine`, `Laplace-MCP`, `Laplace-UCI`, `Laplace-Operations`, and `Laplace`. Compiling or passing unit checks is never sufficient on its own: every change must preserve the invention's mathematical laws, state clearly why non-obvious constraints exist and which standard optimizations are lawful, reconcile cleanly onto the installed stack, and work end to end against real populated data.

> [!IMPORTANT]
> Where code, a test, a workflow, or a live database disagrees with the documented invention ([The Invention](../Repositories/Laplace/docs/INVENTION.md), [the inventor's record](../Repositories/Laplace/docs/INVENTOR_RECORD.md), and the decided entries of [30. Conflicts](../Sequence/Conflicts.md)), change the code to match the invention — never downgrade the specification to excuse agent drift.

## 1. Begin with the whole operation

Before changing a component, trace the complete end-to-end operation across every layer it touches: its grammar or codec input, compiled `.recipe`, `Laplace-Native` C execution, `Laplace-postgres` 4D index surface, Engine/MCP/C# orchestration, persistent and derived effects, attribution, and post-deployment behavior. A leaf spring is not the whole watch: never stop at an isolated helper, thin vertical slice, benchmark stub, or partial route while leaving the end-to-end product path unwired.

- **Why:** Laplace's value comes from compounding overlap across shared 16-byte BLAKE3 IDs, trajectories, and Glicko-2 standings; an isolated helper or mock-verified route hides plan blowups, round-trip storms, and semantic regressions that appear immediately on a populated database.
- **When incremental staging is lawful:** Developing a horizontal batch locally across sibling repositories in `$LAPLACE_BUILD` (`ninja` + `dotnet build` in seconds) before running one unified deploy and live behavioral proof at the end of the batch is required; shipping half-wired vertical stubs or per-ticket waterfall deploys is what is forbidden.

## 2. One semantic implementation

`Laplace-Native` and `Laplace-postgres` (driven by `Laplace-Engine`) own every semantic operation. Client processes execute deterministic ROM and CPU math in-process via `Laplace-Native` (`Laplace.Native.Interop` in C#) with zero DB round-trips, while PostgreSQL executes C-backed indexed set probes, staged binary `COPY` merges, and series/attribution folds (`pg_contract.h`, `LaplaceEngine` `reader.h`, `Laplace.Data`). Transports, source adapters, CLI wrappers, HTTP endpoints, scripts, and UI hosts must never contain a second implementation of identity, UAX #29 segmentation, AST lowering, 4D centroids, Hilbert keys, mantissa packing, Glicko-2 series math, Forward traversal, realization, or model synthesis.

- **Why:** Because content identity is hashed recursively (`BLAKE3-128` of ordered child IDs), a single mismatch in segmentation, singleton collapse, case handling, or coordinate rounding changes every ancestor ID up to the file and witness trunk, silently fracturing cross-modal convergence.
- **When client-side execution is lawful:** Running `Laplace-Native` C functions directly in client RAM over identically memory-mapped ROMs (`tier0.bin`, `tier0.flags`, `highway.bin`, `chess.bin`) is not duplication — it is the **same** compiled C binary avoiding unnecessary TCP and SQL executor round-trips.

## 3. Universal compositional scalars and lossless trees (zero chunking)

All digital content — text, source code, `.git` history, structured records, chess, RGB(A) pixels, PCM audio samples, and model tensors — decomposes losslessly down to Tier-0 Unicode codepoints without arbitrary chunking (`MaxLines`, sliding windows, or overlapping byte slices) and without raw binary numeric blobs. Scalars compose from digit codepoints (`255` $\rightarrow$ `['2','5','5']`, `3.14159` $\rightarrow$ `['3','.','1','4','1','5','9']`).

- **Why:** Arbitrary chunk boundaries destroy syntactic and structural identity so two files sharing a function, sentence, or patch no longer collide on the same Merkle node, whereas exact hierarchical decomposition + upward GIN containment (`laplace_path_ops`, `laplace_held_files`) recovers the exact lowest common ancestor in microseconds. Likewise, composing `255` once as `['2','5','5']` ensures prose (`"255"`), code literals, IPv4 octets, RGB(A) channel intensities, PCM samples, and digits of $\pi$ land on **one** `lp_id` while higher-tier `physicality.path` sequences and 30-bit `M` run-length encoding (`run`) supply modality form and compress homogeneous regions (such as millions of white pixels) without row bloat.
- **When structural blocking and precomputed scalar tables are lawful:** Precomputing reusable scalar compositions once in ROM perf-caches or the in-RAM lock-free node table (`O(1)` lookup, zero repeated hashing per pixel/sample) and balancing multi-megabyte flat sequences with deterministic content-defined `blocks_of` spines (up to 4,096 parts cut on intrinsic child-ID bits in `src/record_stream.c`, skipped transparently during `Trunk -> Leaf` deduplication) are 100% lawful and required for throughput.

## 4. Grammars, recipes, and compounding modularity

Tree-sitter parsers, standards readers, and edge media codecs recover concrete structure; declarative `.recipe` files (`Laplace-Engine/recipes/`, compiled to `recipe_program.h` bytecode) state what each recovered field becomes (`content`, `key`, `refer`, `type`, `metadata`, `omit`, `claim`, `voice`, `relation`, `games`, `dependence`). Opaque per-source C/C# walkers (`Laplace.Decomposers`), hardcoded English relation switches, and domain-forked reasoning loops (`chess_*`, `code_*`, `model_*`) are forbidden.

- **Why:** A bespoke walker per corpus or a forked mini-engine per domain traps each modality in a silo; compiling every source through one generic `.recipe` VM into the same four tables and steering one C `Forward + Highway A* + Gödel` loop (`program.c`) via detached `.firmware` files makes every new lexicon, codebase, game archive, or assimilated model immediately strengthen every other task.
- **When format codecs and helper grammars are lawful:** Standard container decoders (e.g., `libpng`, FLAC/WAV framing, decompression, Safetensors/GGUF header readers, Syzygy bitbase readers, Tree-sitter language grammars) are completely lawful at the edge to decode container framing into raw symbols/samples before `.recipe` composition takes over.

## 5. Native ABI and bit-exact SIMD determinism

Use fixed-width integer and IEEE-754 types at every persisted, generated, wire, and ABI boundary (`int32_t`, `uint64_t`, `lp_id`; never platform-varying C `long`, unions, or bit-fields in `LP_API` headers), with explicit ownership, lifetime, alignment, overflow checks, and error atomicity. Build canonical math with `icx -fp-model=precise -ffp-contract=off` and CORE-MATH (`cr_sin`, `cr_cos`).

- **Why compiler `-ffast-math`, `-ax` auto-reduction, and FMA contraction are forbidden:** Floating-point addition is non-associative, and fused multiply-add (`a * b + c`) rounds once where unfused multiply-then-add rounds twice. Letting the compiler reassociate reductions by target ISA or emit opportunistic FMA causes Broadwell (`avx2`) and Skylake/Zen (`avx512`) hosts to compute different coordinates, Hilbert keys, or curve distances for identical content.
- **When explicit SIMD, MKL, and C++ linear algebra are lawful:** Explicit runtime `cpuid`/`xgetbv` dispatch in `Laplace-Native/src/cpu.c` (`lp_kernels()`) to fixed-order `sse2`, `avx2`, `avxvnni`, `avx512`, `avx512vnni`, and BMI2 `pdep` kernels compiled under `-fp-model=precise -ffp-contract=off`, Intel MKL locked to conditional numerical reproducibility (`lp_mkl_reproducible()` enforcing `MKL_CBWR_AVX2_STRICT`), and `src/linalg.cpp` wrapping scalar Eigen/Spectra (`EIGEN_DONT_VECTORIZE`, `EIGEN_NO_CPUID`, `EIGEN_DONT_PARALLELIZE`) behind `extern "C"` are **fast, bit-exact across machines, verified across `LAPLACE_ISA=scalar..avx512vnni`, and required**. Bound worker threads, MKL threads, PostgreSQL workers, and managed pools explicitly so nested calls never oversubscribe physical cores.

## 6. Memoization, ROMs, and content-addressed caching

Perf-caches (`tier0.bin`, `tier0.flags`, `highway.bin`, `chess.bin`) are fingerprinted, rebuildable, memory-mapped ROMs derived deterministically from canonical law. Persistent mutable world state lives strictly in the four substrate tables (`entity`, `physicality`, `attestation`, `consensus`), separate from conventional operational/billing tables (`app.*`).

- **Why secondary ID caches and stale standing caches are forbidden:** Inventing surrogate integer IDs, salted cache keys, or lazy ETL materialized views over `consensus` creates a second truth that drifts as witnesses arrive or are forgotten first-in, first-out.
- **When memoization and incremental skip caches are lawful:** Because `lp_id` is a collision-resistant 128-bit BLAKE3 Merkle hash of immutable constituents, caching `lp_id -> immutable coord / path / realized UTF-8` (`lp_realizer`, `src/table.c` lock-free node table, `writer.known` staged-ID bitmaps, in-process ROM maps) and skipping unchanged files during ingest via recorded file-byte hashes or `O(1)` file-trunk presence probes (`laplace_present_ids`) are **100% mathematically sound and essential for performance**. Only caching mutable `consensus` standings across writes without re-reading or minting non-BLAKE3 IDs is forbidden.

## 7. PostgreSQL set probes and the three distinct spaces

Extension C functions and SPI queries are schema-qualified, prepared, binary-parameterized, and set-oriented. Database crossings scale as $O(\text{tiers})$ or `2–3` batched binary probes per turn, never $O(\text{rows})$ cursor or RBAR loops. Candidate generation pushes GIN containment (`laplace_path_ops`), 64-bit bank masks (`laplace_mask_ops`), 4D GiST boxes (`laplace_point4d_ops`, `laplace_angular4d_ops`), Hilbert ball ranges (`laplace_hilbert_ball_ranges`), and tier/claim partition bounds into index scans first, followed by exact native C verification.

- **Why raw `physicality.path` carrier doubles must never enter spatial metrics or Glome:** `physicality.path` packs `43/43/42 + 28` bits into IEEE-754 mantissas in `[0.25, 0.5)` strictly to exploit PostGIS binary storage, TOAST (`lz4`), and GIN/GiST indexing without edge tables; those carrier doubles are **identities, not positions**. Passing them directly into `laplace_frechet4d`/`dtw4d`/`edr4d` or plotting them on the Glome measures hash noise instead of geometry. Always unpack constituent IDs and resolve real `entity.coord` (`laplace_curves`, `laplace_couple`, `laplace_project_path`) first, and fail loudly rather than adding silent scalar fallbacks if an index is misconfigured.

## 8. Managed orchestration (`Laplace`)

C# owns service hosting (`Laplace.Hosting`), HTTP/OpenAI/MCP transport (`Laplace.Mcp`), principal authentication, tenancy, Patreon entitlement witnessing, royalty ledger persistence (`app.*`), and Web UI delivery. Deterministic client calls execute in-process via auto-generated `Laplace.Native.Interop` bindings, and database calls execute binary prepared probes through `LaplaceEngine` (`reader.h`) and `Laplace.Data`.

- **Why:** Keeping C# strictly in transport, auth, billing, and presentation guarantees that CLI (`laplace turn`), native MCP (`lpm`), UCI, and Web/OpenAI (`/v1/chat/completions`) invoke the exact same C Forward pass and return identical answers and `share_bp = 10000` attributions for the same world state, `.firmware`, and seed.

## 9. In-place lifecycle and live-server verification

Operate and verify the real installed PostgreSQL 18 stack in place (`laplace-ops deploy`, `laplace-ops verify -Installed`, `Laplace-postgres/tests/deployed.sh`). Routine C, SQL function, operator, opclass, `.firmware`, Engine, and C# changes apply **in place** via `laplace.reconcile.sql` (`ALTER EXTENSION laplace UPDATE`) and idempotent `db/schema/*.sql`, preserving all admitted corpora and indexes; single-source fixes use `laplace forget` + `laplace sweep` + re-ingest, while `--recreate` is reserved strictly for persistent table byte-layout (`laplace-storage:<16-hex>`) or `tier0.bin` coordinate changes.

- **Why disposable `initdb` clusters and mock substrates are forbidden:** Ephemeral `initdb` / `pg_regress --temp-instance` clusters and in-memory mock repositories run with toy row counts, unrepresentative planner statistics, default GUCs, and superuser shortcuts — masking partition-pruning failures, GIN pending-list bloat, extension-upgrade bugs, and permission errors that break real deployments.
- **When `pg_regress` and automated test harnesses are lawful:** Running `pg_regress --use-existing` and `isolationtester` against the live deployed PostgreSQL server inside rolled-back transactions (`Laplace-postgres/tests/deployed.sh`), native CTest ISA parity suites (`ctest --preset icx-release`), contract gates (`check-function-bindings.mjs`, `sql-contract-gate.py`, `generate.mjs --check`, `ReadPathArchitectureGateTests`), Python CLI/stage verification scripts (`stage-lifecycle.py`, `verify-admitted-data.py`), and `EXPLAIN (ANALYZE, BUFFERS)` / `laplace bench` measurements on populated data are **100% valid and required**.

## 10. Batch execution and repository hygiene

Shared contracts (`manifest/banks.tsv`, `manifest/slots/*.tsv`, `manifest/trust_classes.toml`, `manifest/function_bindings.tsv`, `pg_contract.h`, `Laplace.Native.Interop`, `components.lock.tsv`) are defined once and generated or checked automatically. Builds run out of tree in `$LAPLACE_BUILD`.

Execute cross-repository work in cohesive horizontal batches: iterate locally across affected repositories, deploy once in place, prove real behavioral quality against populated data, and advance `components.lock.tsv` once per batch. Judge leftover agent WIP critically against the invention (finish, fix, or delete cleanly), never commit status diaries or benchmark prose as a substitute for working code, and keep `Laplace-Wiki` (`python tools/check_wiki.py` and `npx markdownlint-cli2`) and `Laplace-Operations/agents/` (`sync.ps1`) synchronized with the built stack.
