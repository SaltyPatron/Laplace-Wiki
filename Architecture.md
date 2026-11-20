# Architecture

Laplace is native C, with SQL and C# as orchestration.

## Compounding mechanisms, not feature silos

Laplace is greater than the sum of its parts because its mechanisms overlap inside the exact same bytes rather than sitting in separate domain silos:

- **Bit-packed mantissa trajectories over PostGIS:** Packing 128-bit BLAKE3 child IDs (`43 + 43 + 42` bits + `28` spare bits in `[0.25, 0.5)`) and `M` (`run30 / said3 / outcome2 / position18`) into IEEE-754 `POINT ZM` and `LINESTRING ZM` vertices turns battle-tested PostgreSQL/PostGIS storage, TOAST slicing, binary `COPY`, GiST R-trees, and GIN (`laplace_path_ops`) into a microsecond sequence, containment, gap, and continuation engine with zero `precedes`/`contains` edge tables — while unpacking those exact same IDs through `tier0.bin` / `entity.coord` yields real 4D curves inside the $S^3$ 4-ball for Fréchet, DTW, and EDR shape comparison.
- **Snap-in codecs, recipes, perfcaches, and firmware:** Every digital modality — text, curated lexicons, encyclopedias, source code, `.git` history, chess games, images, audio, video, and conventional AI checkpoints (`Safetensors`/`GGUF`) — enters through generic grammars/codecs + declarative `.recipe` files onto the **same** 16-byte BLAKE3 content IDs in the **same** four tables (`entity`, `physicality`, `attestation`, `consensus`). Every source or model snapped in automatically cross-braces every other modality, steered at runtime by one native C `Forward + Highway A* + Gödel` loop and detached `.firmware` programs, and read out as UTF-8, code, moves, media, or CPU-synthesized `laplace-blake3-v1` checkpoints with Fisher `share_bp = 10000` witness attribution.

## Native C

Every semantic and numerical operation lives once in `Laplace-Native` C (`icx`, `-fp-model=precise`, `-ffp-contract=off`, SIMD/AVX/VNNI, CORE-MATH, Eigen, Spectra, MKL) with zero GPU requirement.

Because `tier0.bin`, `tier0.flags`, `highway.bin`, and `chess.bin` are deterministic, fingerprinted ROMs memory-mapped identically on both client and server, deterministic operations (BLAKE3 IDs, UAX #29 segmentation, case/lexical variant flags, 4D integer centroids, 4D Hilbert keys, mantissa pack/unpack, 64-bit masks, Syzygy probes, in-memory Fréchet/DTW/EDR, Glicko-2 / Fisher royalty math, and UTF-8 realization) run **in-process in `Laplace-Native` C on the client (`Laplace.Native.Interop`) with zero database round-trips**.

Bit-perfect determinism across hardware and operating systems requires the pinned compiler and floating-point configuration; every build carries a verifiable fingerprint. See [Research: Numerics](Research/Numerics.md).

## SQL

SQL is purely an indexed set orchestrator over the four persistent substrate tables (`entity`, `physicality`, `attestation`, `consensus`). It executes prepared binary set probes, GiST/GIN/B-tree index filters, and staged `COPY` merges (`Laplace-postgres`), offloading all math, traversal, and composition to `Laplace-Native` C. C# (`Laplace`) orchestrates HTTP/OpenAI/MCP/UCI/Web transport, authentication, workspace tenancy, and entitlement workflows over generated `Laplace.Native.Interop` bindings and `LaplaceEngine` (`reader.h`), never reimplementing substrate logic.

## Databases

The Laplace substrate holds the four persistent tables (`entity`, `physicality`, `attestation`, `consensus`) with pure content-addressed BLAKE3 identities and deterministic UTF-8 collation where text metadata exists. Conventional operational tables (`app.*` accounts, API keys, entitlements, and royalty settlements) remain strictly separated from substrate identity.

## Repositories

| Repository | Role |
| --- | --- |
| [Laplace-Native](https://github.com/SaltyPatron/Laplace-Native) | Shared deterministic C library (`LaplaceNative` CMake package + auto-generated `Laplace.Native.Interop` NuGet). |
| [Laplace-postgres](https://github.com/SaltyPatron/Laplace-postgres) | 4D expansion of PostgreSQL 18 + PostGIS (`CREATE EXTENSION laplace`) with in-place `laplace.reconcile.sql` upgrades. |
| [Laplace-Engine](https://github.com/SaltyPatron/Laplace-Engine) | `laplace` CLI, `LaplaceEngine` (`reader.h`), generic Tree-sitter + `.recipe` ingest VM, Forward/Firmware/Gödel pass, and model assimilation/synthesis. |
| [Laplace-MCP](https://github.com/SaltyPatron/Laplace-MCP) | Native HTTP (`Laplace::http`) + MCP server (`lpm`) and IIS host. |
| [Laplace](https://github.com/SaltyPatron/Laplace) | Product application (`/v1/*` OpenAI API, Web/Glome, Chess Lab, Foundry, Code player, Knowledge Arena, `app.*` billing/royalties). |
| [Laplace-UCI](https://github.com/SaltyPatron/Laplace-UCI) | UCI relay and Lichess connector. |
| [Laplace-Operations](https://github.com/SaltyPatron/Laplace-Operations) | Host provisioning, `components.lock.tsv`, `data.tsv`, `laplace-ops`, and canonical `agents/` instructions. |

Laplace expands PostGIS to 4D throughout (`POINT ZM`, `LINESTRING ZM`, 4D centroids, 4D GiST boxes/cones, mantissa path GIN) alongside 40+ years of battle-tested PostgreSQL storage and indexing, executing every capability end to end against real deployed data rather than mock harnesses.
