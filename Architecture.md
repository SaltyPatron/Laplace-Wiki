# Architecture

Laplace is native C, with SQL and C# as orchestration.

## Native C

Every operation goes into native C, with SQL and C# as orchestration, in all cases. The one exception is a client-side operation that would be faster in native C# than marshalled to native C.

SIMD, AVX, VNNI, and the like are heavily preferred. Native C is preferred over SQL or C#, with marshalling of shared, reusable code: code centralization, deduplication, generics, abstractions, base classes.

Bit-perfect determinism across hardware and operating systems requires a specific build configuration. Every build has a fingerprint.

## SQL

SQL is purely an orchestrator. It fetches and writes records. Every other operation, including row-by-row processing, cursors, CTEs, and any other complex operation, is offloaded to native C.

## Repositories

| Repository | Role |
| --- | --- |
| [Laplace-Engine](https://github.com/SaltyPatron/Laplace-Engine) | Laplace itself. |
| [Laplace-Native](https://github.com/SaltyPatron/Laplace-Native) | The library with the shared code. |
| [Laplace-postgres](https://github.com/SaltyPatron/Laplace-postgres) | The expansion of PostgreSQL to 4D, with real math from Laplace-Native. |

Laplace needs 4D everything. PostGIS functions such as `ST_Centroid` give 2D or 3D results, not 4D, so Laplace-postgres expands PostgreSQL to 4D throughout.
