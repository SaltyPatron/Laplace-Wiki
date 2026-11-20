# Build

Every Laplace build uses one compiler, one set of floating-point flags, and one set of presets; `build.sh` builds the extension and the engine, `deploy.sh` makes the database, `ingest.sh` fills it, and the native tests run after every build of the library.

## Flags

`Laplace-Native/cmake/LaplaceFlags.cmake` sets the flags every target of every repository compiles with:

| Compiler | Flags | Why |
| --- | --- | --- |
| `icx` | `-fp-model=precise -ffp-contract=off -fno-fast-math -march=x86-64-v2 -Wno-overriding-option -O3` | `icx` defaults to `-fp-model=fast`; `precise` alone still fuses multiplies and adds into FMAs, which round once where two operations round twice, so contraction is turned off explicitly and compiler auto-dispatch (`-ax…`, `-xHost`) is never used |
| `gcc` | `-ffp-contract=off -fno-fast-math -march=x86-64-v2 -O3` | the cross-compiler determinism check |
| per-ISA translation units | `-march=x86-64-v3` for `isa/scan_avx2.c`, `isa/row_avx2.c`, `isa/s3_avx2.c`, `isa/hilbert_bmi2.c`, `isa/dot_avx2.c`; `+ -mavxvnni` for `isa/dot_avxvnni.c`; `-march=x86-64-v4` for `isa/scan_avx512.c`, `isa/row_avx512.c`, `isa/dot_avx512.c`; `+ -mavx512vnni` for `isa/dot_avx512vnni.c` | explicit kernels compiled per ISA level in their own units and dispatched at run time by `lp_cpu_active()` (`cpu.c`) |

C17, position-independent code (the library is linked into a PostgreSQL extension), hidden visibility with `LP_API` exporting the public functions. `LP_HAVE_AVX2`, `LP_HAVE_AVX512`, `LP_HAVE_AVXVNNI`, and `LP_HAVE_AVX512VNNI` are defined for the library; `LP_TIER0_DEFAULT` is compiled in from `LAPLACE_TIER0`.

## Presets

`CMakePresets.json` in each repository:

| Preset | Compiler | Type | Binary directory |
| --- | --- | --- | --- |
| `icx-release` | `icx`, `icpx` | RelWithDebInfo | `$LAPLACE_BUILD/<repo>/icx-release` |
| `icx-debug` (Native) | `icx`, `icpx` | Debug | `$LAPLACE_BUILD/Laplace-Native/icx-debug` |
| `gcc-release` (Native) | `gcc`, `g++` | RelWithDebInfo | `$LAPLACE_BUILD/Laplace-Native/gcc-release` |

Generator: Ninja. Test presets `icx-release` and `gcc-release` run `ctest` with output on failure.

## Targets

| Repository | Target | Sources | Links | Needs |
| --- | --- | --- | --- | --- |
| Laplace-Native | `Laplace::laplace_static` (`liblaplace.a`), `Laplace::laplace` (`liblaplace.so` / `laplace.dll`) | `platform.c mem.c map.c wire.c mapped.c path.c cpu.c flags.c utf8.c identity.c sequence.c dag.c coord.c compose.c geometry.c follows.c consensus.c tier0.c tier0_map.c geom4d.c s3.c pull.c highway.c perfcache.c trust.c dot.c realize.c bench.c json.c` + `isa/*` | `BLAKE3::blake3`, `Laplace::math`, `m pthread` | |
| Laplace-Native | `Laplace::text` (`laplace_text`) | `text.c ids.c` | `laplace_static`, ICU | ICU 78 at `$LAPLACE_ICU_DIR` |
| Laplace-Native | `Laplace::model` (`laplace_model`) | `rowsig.c knn.c` | `MKL::MKL`, `OpenMP::OpenMP_C` | oneAPI MKL + OpenMP |
| Laplace-Native | `Laplace::linalg` (`laplace_linalg`) | `linalg.cpp` | scalar fixed-blocking Eigen + Spectra | `$LAPLACE_EIGEN_DIR`, `$LAPLACE_SPECTRA_DIR` |
| Laplace-Native | `Laplace::math` (`lp_crmath` alias) | CORE-MATH binary64 functions under libm names | | `$LAPLACE_COREMATH` + `Laplace-Operations/math` |
| Laplace-Native | `blake3` | BLAKE3 C and SSE2/SSE4.1/AVX2/AVX-512 assembly | | `$LAPLACE_BLAKE3_DIR` |
| Laplace-Native | `csharp_bindings`, `csharp_package` | AST-generated `LaplaceNative.g.cs` + `Laplace.Native.Interop` NuGet (`win-x64` / `linux-x64`) | `laplace` | `node`, `dotnet` |
| Laplace-postgres | `laplace_pg` (`laplace.so` / `laplace.dll`) | `src/*.c` + `sql/laplace.sql.in`, `api.sql`, `operations.sql`, `path_set_match.sql` | `find_package(LaplaceNative CONFIG REQUIRED)` (`Laplace::laplace_static`, `Laplace::text`) | `pg_config` of the target server; emits install SQL and `laplace.reconcile.sql` |
| Laplace-Engine | `laplace_engine` (`laplace`) | `src/*.c` | `find_package(LaplaceNative CONFIG REQUIRED)` (`Laplace::text`, `Laplace::laplace_static`, `Laplace::math`, `Laplace::model`), `BLAKE3::blake3`, `ts_runtime`, `pq`, `OpenMP::OpenMP_C`, `z dl m pthread` | libpq at `$LAPLACE_PG_DIR`, tree-sitter runtime at `$LAPLACE_TREESITTER` |
| Laplace-MCP | `lpm`, `Laplace.Modular.Web` | `native/*.c`, `web/` | `find_package(LaplaceNative CONFIG REQUIRED)`, libpq, .NET | `laplace` CLI, `tier0.bin`, `highway.bin` |

## Commands

```sh
source /repos/src/Laplace-Operations/laplace.env

# the library, both compilers, with its tests
cd $LAPLACE_SRC/Laplace-Native
cmake --preset icx-release && cmake --build --preset icx-release && ctest --preset icx-release
cmake --preset gcc-release && cmake --build --preset gcc-release && ctest --preset gcc-release

# package Laplace-Native once (native-package.sh) and build Laplace-postgres and Laplace-Engine against find_package(LaplaceNative CONFIG REQUIRED)
cd $LAPLACE_SRC/Laplace-Operations
./build.sh            # packages LaplaceNative, builds grammars, and configures/builds Laplace-postgres and Laplace-Engine under $LAPLACE_BUILD
./build.sh install    # also installs the extension into PostgreSQL's directories by atomic rename

# the grammars the recipes read
tools/build_grammars.sh [/vault/Data/TreeSitter] [$LAPLACE_GRAMMARS]
```

`build_grammars.sh` finds every `src/parser.c` under the grammar root, reads the grammar's name from its `tree_sitter_<name>` symbol, compiles it with `$CC` (default `icx`) at `-O2 -fPIC -shared` together with `src/scanner.c` when present, into `libtree-sitter-<name>.so`, and skips a grammar whose library and inputs match its stamp. A grammar that fails to compile is reported and its library removed.

## deploy.sh

`Laplace-Operations/deploy.sh` prepares or reconciles a Laplace database in place without dropping existing data (`./deploy.sh as-is` deploys local unpushed checkouts; `./deploy.sh drop` drops and recreates empty when explicitly requested). It verifies that pre-built `tier0.bin`, `tier0.flags` (and `.layout`), and `tier0.highway` (`highway.bin`) artifacts exist before touching the database. Each step is logged under `$LAPLACE_WORK/logs/deploy/<UTC timestamp>/<step>.log` with its exit status, stopping on the first failure:

| Step | Command | Notes |
| --- | --- | --- |
| `tune-pg` | `tune-pg.sh` | applies, reloads, and verifies cluster settings |
| `build` | `build.sh install` | packages `LaplaceNative`, builds Engine and extension, installs extension by rename |
| `grammars` | `tools/build_grammars.sh` | reuses stamped grammars, rebuilds changed ones |
| `highway-fingerprint` | `laplace highway --fingerprint` | verifies installed highway ROM |
| `deploy` | `laplace deploy --prepare` or `--configure-server-cache` | creates DB on first install; reconciles in place via `laplace.reconcile.sql` when `laplace-storage:<hash>` matches |
| `status` | `laplace status` | verifies Engine and PostgreSQL perf-cache fingerprints, partitions, and indexes |

It takes a lock per database in `$LAPLACE_LOCKS` and leaves with exit 3 while an ingest of that database runs. `./deploy.sh drop` first drops the database through the role, `DROP DATABASE … WITH (FORCE)`, refusing `postgres` and an empty name, then deploys it again, empty. It needs PostgreSQL 18 with PostGIS running and the role `setup.sh` made. `LAPLACE_CONNINFO="… dbname=NAME" ./deploy.sh` deploys another database, made if the server has none of that name.

## ingest.sh

`Laplace-Operations/ingest.sh [source...]` fills the database `laplace.env` names: the sources named, or every source in `recipes/order`. It holds a lock per database, builds and installs nothing, and needs `laplace`, tier 0 and the highway already deployed. Its steps, logged under `$LAPLACE_WORK/logs/ingest-runs/<UTC timestamp>`:

| Step | What |
| --- | --- |
| `ingest` | `laplace ingest` |
| `wal` | the write-ahead log the ingest made, by table, index and resource manager: full-page images and their bytes, and the records' own data, read each minute with `pg_walinspect` into `wal.tsv` |
| `status` | `laplace status` |
| `bench` | `laplace bench` |

## Tests after a build

`ctest` in Laplace-Native runs, each against the tier 0 at `LAPLACE_TIER0`: `identity`, `geometry`, `coord`, `follows`, `consensus`, `shape`, `pull`, `flags`, then `follows_scalar`, `follows_sse2`, `follows_avx2` with `LAPLACE_ISA` set to each level, and `text` when ICU is present. What each checks is in [Checks](Checks.md#the-native-tests). The `icx` and `gcc` builds must both pass; both reproduce the prototype's tier-0 IDs and Hilbert values.

The extension's, the Engine's and the MCP's own CI build them and run only checks that need no database. Their database checks run after the deployment, against the deployed database: [Checks](Checks.md#the-database-checks).
