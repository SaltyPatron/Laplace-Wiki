# Architecture

Laplace is native C, with SQL and C# as orchestration.

## Native C

Every operation goes into native C, with SQL and C# as orchestration, in all cases. The one exception is a client-side operation that would be faster in native C# than marshalled to native C.

SIMD, AVX, VNNI, and the like are heavily preferred. Native C is preferred over SQL or C#, with marshalling of shared, reusable code: code centralization, deduplication, generics, abstractions, base classes.

The 4D math runs in extension functions, optimized with libraries such as Intel's, Eigen, and Spectra.

Laplace does not require a GPU. Third-party tools that produce input for Laplace, or work alongside it, may use one.

PostgreSQL has defaults that are tuned to the hardware.

Development favors observability and benchmarks over a heavy focus on tests and gates: the invention should speak for itself.

Bit-perfect determinism across hardware and operating systems requires a specific build configuration. Every build has a fingerprint. See [Research: Numerics](Research/Numerics.md).

## SQL

SQL is purely an orchestrator. It fetches and writes records. Every other operation, including row-by-row processing, cursors, CTEs, and any other complex operation, is offloaded to native C.

## Databases

The Laplace content database holds entities, physicalities, and sources; its few text columns, such as a source's origin, use UTF-8 with a deterministic, operating-system-independent collation. Operational data such as logs, authentication, and billing stays conventional, in a separate database.

## Repositories

| Repository | Role |
| --- | --- |
| [Laplace-Engine](https://github.com/SaltyPatron/Laplace-Engine) | Laplace itself. |
| [Laplace-Native](https://github.com/SaltyPatron/Laplace-Native) | The library with the shared code. |
| [Laplace-postgres](https://github.com/SaltyPatron/Laplace-postgres) | The expansion of PostgreSQL to 4D, with real math from Laplace-Native. |

Laplace needs 4D everything. PostGIS functions such as `ST_Centroid` give 2D or 3D results, not 4D, so Laplace-postgres expands PostgreSQL to 4D throughout.

Those 4D capabilities are expansions of GIS, not replacements. Laplace uses the standard geometry types, such as a normal POINT ZM, and adds 4D functions alongside what PostGIS already provides, rather than stepping on more than 40 years of battle-testing.
