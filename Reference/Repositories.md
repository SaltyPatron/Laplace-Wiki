# Repositories

Four repositories implement Laplace: Laplace-Native is the shared library, Laplace-postgres is the PostgreSQL extension that links it, Laplace-Engine is the one program that links it and runs the database, and Laplace-Prototype is the test bench the three are checked against.

## What each holds

| Repository | Version | Holds | Builds | Links |
| --- | --- | --- | --- | --- |
| Laplace-Native | 0.2.0 | `include/laplace/laplace.h`, the one public header; `src/`: `cpu.c`, `flags.c`, `utf8.c`, `identity.c`, `coord.c`, `compose.c`, `geometry.c`, `follows.c`, `consensus.c`, `tier0.c`, `geom4d.c`, `pull.c`, `text.c`, `rowsig.c`, `isa/` kernels; `tests/`; `cmake/LaplacePaths.cmake`, `cmake/LaplaceFlags.cmake` | `liblaplace.a` and `liblaplace.so` (everything but text and model); `liblaplace_text` (needs ICU 78); `liblaplace_model` (needs MKL and OpenMP); `lp_crmath` (CORE-MATH `cr_sin`, `cr_cos`); BLAKE3 with its assembly | BLAKE3, libm, pthread |
| Laplace-postgres | 1.0 | `src/laplace_pg.c`; `sql/laplace--1.0.sql` (the install script), `schema.sql`, `semantics.sql`, `lookup.sql`, `indexes.sql`; `laplace.control`; `bench/bench_queries.py` | `laplace.so` into PostgreSQL's `pkglibdir`; the control and SQL files into `sharedir/extension` | Laplace-Native statically, PostgreSQL 18 headers, PostGIS geometry serialization |
| Laplace-Engine | | `src/`: `main.c`, `engine.h`, `recipe.c`, `elements.c`, `members.c`, `records.c`, `table.c`, `file.c`, `vocab.c`, `ingest.c`, `db.c`, `read.c`, `pull.c`, `forward.c`, `fills.c`, `forget.c`, `deploy.c`, `tier0.c`, `flags.c`, `firmware.c`, `bench.c`, `model.c`; `recipes/`; `firmware/program.firmware`; `laplace.env`; `build.sh`; `deploy.sh`; `tools/build_grammars.sh` | `laplace`, one executable | `laplace_text`, `laplace_static`, `lp_crmath`, BLAKE3, the tree-sitter runtime, libpq, OpenMP, zlib, dl; `laplace_model` when MKL is present |
| Laplace-Prototype | | `tier0/gen_tier0.py`, `ducet_order.py`, `nfd17.py`, `fingerprint.txt`; `dag/ingest.c`; `db/schema.sql`, `indexes.sql`, `load.sh`, `ext/`; `tests/verify.py`, `queries.py`, `gap_query.py`, `breaktest.c`; `chess/`, `semantics/`, `models/`, `code/`, `recipes/` | the golden values the native tests reproduce | ICU 78, BLAKE3, PostgreSQL 18 at port 5439 |

Laplace-postgres and Laplace-Engine build Laplace-Native as part of themselves with `add_subdirectory` and keep no copy of anything in it. The engine and the extension share one implementation of every operation through the header.

## The artifact graph

```mermaid
flowchart LR
    UCD[Unicode data<br>$LAPLACE_UCD] --> T0[tier0.bin<br>laplace tier0]
    UCD --> FL[tier0.flags + .layout<br>laplace flags]
    BL[BLAKE3, CORE-MATH,<br>ICU 78, tree-sitter] --> NAT[liblaplace, liblaplace_text<br>Laplace-Native]
    NAT --> EXT[laplace.so, laplace--1.0.sql<br>Laplace-postgres]
    NAT --> ENG[laplace<br>Laplace-Engine]
    GR[grammar sources] -->|build_grammars.sh| SO[libtree-sitter-*.so<br>$LAPLACE_GRAMMARS]
    SO --> ENG
    EXT --> DB[(PostgreSQL 18 + PostGIS<br>laplace deploy)]
    T0 --> DB
    FL --> DB
    T0 --> ENG
    FL --> ENG
    REC[recipes/, order] --> ENG
    FW[program.firmware] --> ENG
    DATA[corpora<br>$LAPLACE_DATA] --> ENG
    ENG -->|COPY, set statements| DB
    DB -->|paths, standings| ENG
```

An arrow is a build-time or run-time dependency: the artifact at its tail must exist, at the version the head was built or configured for, before the head can run. Tier 0 and the flags are generated from the Unicode data by the engine and read by both the engine and the extension; the two must map the same file, which [`laplace status`](CLI.md#laplace-status) checks by fingerprint.

## What the prototype is for

The prototype established the golden values: the tier-0 IDs, coordinates, and Hilbert values in `tier0/tier0.bin` and its fingerprint; the decomposition of plain text; the schema; the checks in `tests/verify.py`. Laplace-Native's tests reproduce those values bit for bit, on both compilers. The prototype's schema differs from the built one in two tables, `source` and `entity_stats`, which the built schema does not have; see [Schema](Schema.md#what-the-prototype-had).
