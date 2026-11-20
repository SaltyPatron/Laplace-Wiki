# Laplace engineering standards

These standards keep implementation choices subordinate to the complete invention.

They apply across every active Laplace repository: `Laplace-Native`, `Laplace-postgres`, `Laplace-Engine`, `Laplace-MCP`, `Laplace-UCI`, `Laplace-Operations`, and `Laplace`. Compiling or passing unit checks is never sufficient on its own: every change must preserve the invention's laws, deploy cleanly onto the installed stack, and work end to end against real data.

> [!IMPORTANT]
> Where code, a test, a workflow, or a live database disagrees with the documented invention ([The Invention](../Repositories/Laplace/docs/INVENTION.md), [the inventor's record](../Repositories/Laplace/docs/INVENTOR_RECORD.md), and the decided entries of [30. Conflicts](../Sequence/Conflicts.md)), change the code to match the invention — never downgrade the specification to match agent drift.

## 1. Begin with the whole operation

Before changing a component, trace the complete end-to-end operation across every layer it touches: its grammar or codec input, compiled recipe, native C execution, PostgreSQL 4D extension surface, Engine/MCP/C# orchestration, persistent and derived effects, receipts, and post-deployment behavior. A leaf spring is not the whole watch: never stop at an isolated helper, thin vertical slice, benchmark stub, or partial route while leaving the end-to-end product path unwired.

Every change answers:

- how the behavior serves the GPU-free transformer-replacement substrate;
- which exact distinctions it consumes, preserves, calculates, witnesses, or realizes;
- how it participates in the universal content-addressed Merkle-DAG world model;
- how SQL and C# orchestrate it and Native C executes it;
- how it behaves in batch, parallel, PostgreSQL, replay, cancellation, and failure paths;
- how it is deployed and verified end to end on the installed runtime without unnecessary database drops or reseeds.

Component compilation is not product completion. A capability is done when its complete public route builds cleanly, reconciles onto the installed stack, executes against real inputs, and produces the expected durable and observable result.

## 2. One semantic implementation

Native C and the PostgreSQL 4D integration (`Laplace-Native` and `Laplace-postgres`, driven by `Laplace-Engine`) own every semantic operation. SQL and C# only orchestrate typed surfaces (`pg_contract.c`, `sql_catalog.def`). A transport, source adapter, parser binding, cache, database serializer, test helper, CLI, HTTP endpoint, script, or target exporter must never contain a second implementation of identity, AST lowering, composition, physicality, mantissa packing, Hilbert encoding, Glicko-2 standing, cognition, realization, or model semantics.

Scalar operations lower to the deterministic vector-first implementation. Serial, partitioned, parallel, direct-native, PostgreSQL, SQL, and managed routes produce identical logical results and bit-exact canonical identities across supported x86-64 ISA levels (`scalar`, `sse2`, `avx2`, `avx512`).

## 3. Generics, interfaces, and reuse

Each functional layer is isolated as a clean, reusable modular component (`Laplace-Native` → `Laplace-postgres` → `Laplace-Engine` → `Laplace-MCP` → product consumers) consumed as a versioned package rather than copied across repositories.

Within the engine, stable repeated behavior belongs in shared generic pipelines: compilation, immutable context, lock-free node tables, bounded per-worker arenas, $O(\text{tier})$ top-down deduplication, staged binary `COPY`, set-wise merges, perf-cache mapping, cancellation, and receipts. A source or modality supplies only its varying declarations (Tree-sitter grammar or edge codec, `.format`, `.recipe`, manifest slots, firmware parameters). Source, language, modality, and model names select declarations or witnessed state; they never select a separate bespoke engine branch or per-format C/C# walker.

## 4. Grammars, recipes, and the universal AST

Every digital structure lowers to the universal content-addressed Merkle DAG. Tree-sitter parsers, standards readers, and media codecs are concrete-syntax providers; recipes (`Laplace-Engine/recipes/`) are compiled declarative bytecode (`recipe_program.h`) stating what each recovered field becomes (content, key, reference, type, metadata, omit, perf-cache, claim, voice, or relation). Opaque callbacks, hardcoded English relation switches, and hand-rolled per-source scanners are forbidden.

Exact round trips reproduce original bytes from PostgreSQL alone. Intentional transformations create new canonical compositions, preserve unchanged subtree identities, and record provenance. Unhandled fields or malformed inputs fail loudly rather than silently dropping data.

## 5. Native code and ABI

- Use fixed-width types at every persisted, generated, wire, and ABI boundary.
- Make ownership, lifetime, nullability, capacity, alignment, byte order, overflow behavior, and error atomicity explicit.
- Keep floating-point determinism exact (`icx` with `-fp-model=precise` and `-ffp-contract=off`, CORE-MATH `cr_sin`/`cr_cos`, fixed summation order across SIMD widths); fast-math and FMA contraction are forbidden in canonical math.
- Bound concurrency to hardware topology so OpenMP, MKL, TBB, PostgreSQL workers, and managed callers never oversubscribe the host.

## 6. PostgreSQL and SQL

PostgreSQL extension C routines and SPI plans are schema-qualified, prepared, parameterized, and set-oriented. Database crossings are $O(\text{tiers})$, never $O(\text{rows})$; per-row SQL, SPI, process, or network crossings on batch paths are forbidden.

SQL owns transactions, constraints, partitions, indexes, set routing, and result projection. It never implements recursive semantic walks, cursors, RBAR loops, string-hacked identity, or consensus math in SQL text.

For indexed cognition and retrieval, push containment (`laplace_path_ops`), 64-bit bank masks (`laplace_mask_ops`), 4D GiST boxes (`laplace_point4d_ops`, `laplace_angular4d_ops`), Hilbert intervals, and partition bounds into candidate generation first, then run exact native C verification, trajectory comparison, and series math over bounded sets. Never pass packed `physicality.path` carrier doubles into spatial distance functions without realizing constituent coordinates first, and never add silent scalar fallbacks when an indexed path is misconfigured — fail loudly and fix the root cause.

## 7. Managed orchestration

C# owns service hosting, HTTP/OpenAI/MCP/UCI transport, authentication, workspace tenancy, billing/entitlement orchestration, and Web UI delivery. All managed database access runs through `sql_catalog.def` and `NpgsqlCatalog` with zero handwritten SQL strings in `.cs` files. C# never computes substrate identities, case-folds or normalizes content, chunks text or code, blends heuristic ranking weights, or maintains a private substrate copy.

## 8. Persistence, perf-caches, and in-place lifecycle

Persistent world state lives in four substrate tables (`entity`, `physicality`, `attestation`, `consensus`), separate from conventional operational/billing tables (`app.*`). Perf-caches (`tier0.bin`, `tier0.flags`, `highway.bin`, `chess.bin`) are fingerprinted, memory-mapped ROM accelerators derived deterministically from the same canonical law; they never define a second identity space.

Routine C kernel, SQL function, operator, opclass, firmware, Engine, and application updates reconcile **in place** (`laplace.reconcile.sql` / `laplace deploy` / idempotent `db/schema/*.sql`) while preserving loaded corpora and indexes. Source corrections use per-witness `laplace forget` + `laplace sweep` + idempotent re-ingest. Database recreation (`--recreate`) is reserved strictly for persistent table storage-layout or `tier0.bin` coordinate changes and is never triggered automatically by build CI.

## 9. Deployed verification and real evidence

Verify against the real installed PostgreSQL 18 server and deployed services (`laplace-ops deploy`, `laplace-ops verify -Installed`, `deployed.sh`, `tests/deployed/run.sh`) — never spin up disposable private PostgreSQL clusters (`initdb`, `postgres_regress`, `laplace_regress_*`) or mock substrates.

Measure both correctness and physical execution (`EXPLAIN (ANALYZE, BUFFERS)`, `laplace bench`, `laplace status --joins`, phase timings, buffer hits, partition pruning) on real inputs so O(rows) regressions, hub blowups, or plan defects are caught immediately.

## 10. Package, worktree, and repository discipline

Shared contracts (`manifest/banks.tsv`, `manifest/slots/*.tsv`, `manifest/trust_classes.toml`, `manifest/function_bindings.tsv`, `sql_catalog.def`, `components.lock.tsv`) are defined once and consumed or generated deterministically rather than hand-copied.

Builds run out of tree (`$LAPLACE_BUILD`). Keep `main` cohesive across repositories: fold worktree branches promptly instead of stranding partial branches, evaluate leftover agent WIP critically against the invention rather than preserving broken state, and synchronize `Laplace-Wiki` and `Laplace-Operations/agents/` (`sync.ps1`) whenever architecture, commands, or schemas change.
