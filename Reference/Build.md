# Build

Every Laplace build uses one compiler, one set of floating-point flags, and one set of presets; `build.sh` builds the extension and the engine, `deploy.sh` runs the whole deployment, and the native tests run after every build of the library.

## Flags

`Laplace-Native/cmake/LaplaceFlags.cmake` sets the flags every target of every repository compiles with:

| Compiler | Flags | Why |
| --- | --- | --- |
| `icx` | `-fp-model=precise -ffp-contract=off -fno-fast-math -march=x86-64-v2 -Wno-overriding-option -O3` | `icx` defaults to `-fp-model=fast`; `precise` alone still fuses multiplies and adds into FMAs, which round once where two operations round twice, so contraction is turned off explicitly |
| `gcc` | `-ffp-contract=off -fno-fast-math -march=x86-64-v2 -O3` | the cross-compiler determinism check |
| per-ISA translation units | `-march=x86-64-v3 -mavxvnni` for `isa/scan_avx2.c`, `isa/row_avx2.c`, `isa/hilbert_bmi2.c`; `-march=x86-64-v4 -mavx512vnni` for `isa/scan_avx512.c` | kernels compiled per level in their own units and chosen at run time by `lp_cpu_active()` |

C17, position-independent code (the library is linked into a PostgreSQL extension), hidden visibility with `LP_API` exporting the public functions. `LP_HAVE_AVX2` and `LP_HAVE_AVX512` are defined for the library; `LP_TIER0_DEFAULT` is compiled in from `LAPLACE_TIER0`.

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
| Laplace-Native | `laplace_static` (`liblaplace.a`), `laplace` (`liblaplace.so`) | `cpu.c flags.c utf8.c identity.c coord.c compose.c geometry.c follows.c consensus.c tier0.c geom4d.c pull.c` + `isa/*` | `BLAKE3::blake3 m pthread` | |
| Laplace-Native | `laplace_text` | `text.c` | `laplace_static`, ICU | ICU 78 at `$LAPLACE_ICU_DIR` |
| Laplace-Native | `laplace_model` | `rowsig.c` | MKL, OpenMP | `MKLROOT`, set by oneAPI |
| Laplace-Native | `lp_crmath` | CORE-MATH `sin`, `cos` | | `$LAPLACE_COREMATH` |
| Laplace-Native | `blake3` | BLAKE3's C and its Unix assembly for SSE2, SSE4.1, AVX2, AVX-512, supplied by name because BLAKE3's CMake does not recognize `icx` | | `$LAPLACE_BLAKE3_DIR` |
| Laplace-postgres | `laplace_pg` (`laplace.so`) | `src/laplace_pg.c` | `laplace_static` | `pg_config` of the target server; installed to `pkglibdir`, with `laplace.control` and the SQL files to `sharedir/extension` |
| Laplace-Engine | `laplace_engine` (`laplace`) | `src/*.c` | `laplace_text laplace_static lp_crmath BLAKE3::blake3 ts_runtime pq OpenMP::OpenMP_C z dl m pthread`, and `laplace_model` when built | libpq at `$LAPLACE_PG_DIR`, the tree-sitter runtime at `$LAPLACE_TREESITTER`; rpath to ICU and PostgreSQL's `lib`; linked `-rdynamic` |

## Commands

```sh
source /repos/src/Laplace-Operations/laplace.env

# the library, both compilers, with its tests
cd $LAPLACE_SRC/Laplace-Native
cmake --preset icx-release && cmake --build --preset icx-release && ctest --preset icx-release
cmake --preset gcc-release && cmake --build --preset gcc-release && ctest --preset gcc-release

# the extension and the engine, each with the library built as part of it
cd $LAPLACE_SRC/Laplace-Operations
./build.sh            # configures and builds Laplace-postgres and Laplace-Engine under $LAPLACE_BUILD with icx
./build.sh install    # also installs the extension into PostgreSQL's directories

# the grammars the code recipes read
tools/build_grammars.sh [/vault/Data/TreeSitter] [$LAPLACE_GRAMMARS]
```

`build_grammars.sh` finds every `src/parser.c` under the grammar root, reads the grammar's name from its `tree_sitter_<name>` symbol, compiles it with `$CC` (default `icx`) at `-O2 -fPIC -shared` together with `src/scanner.c` when present, into `libtree-sitter-<name>.so`, and skips a grammar whose library is newer than its parser. A grammar that fails to compile is reported and its library removed.

## deploy.sh

`Laplace-Operations/deploy.sh` runs the five steps of [Operations: Deployment](../Operations/Deployment.md) in order, each as a logged step under `$LAPLACE_WORK/logs/deploy/<UTC timestamp>/<step>.log` with its exit status in `<step>.exit`, stopping at the first that does not finish:

| Step | Command | Skipped when |
| --- | --- | --- |
| `build` | `build.sh install` | never; what is built is not rebuilt |
| `tier0` | `laplace tier0` | `$LAPLACE_TIER0` exists and is not empty |
| `flags` | `laplace flags` | `${LAPLACE_TIER0%.bin}.flags` exists and is not empty |
| `deploy` | `laplace deploy` | never; idempotent |
| `ingest` | `laplace ingest` | never; recorded files are passed over by their trunks |
| `index` | `laplace index` | never; `CREATE INDEX IF NOT EXISTS` |
| `status` | `laplace status` | never |
| `bench` | `laplace bench` | never |

It needs PostgreSQL 18 with PostGIS running, a role that may create databases and extensions, and the data under `$LAPLACE_DATA`. `LAPLACE_CONNINFO="… dbname=NAME" ./deploy.sh` deploys another database, made if the server does not have it. A run that was cut off is taken up by running it again.

## Tests after a build

`ctest` in Laplace-Native runs, each against the tier 0 at `LAPLACE_TIER0`: `identity`, `geometry`, `coord`, `follows`, `consensus`, `shape`, `pull`, `flags`, then `follows_scalar`, `follows_sse2`, `follows_avx2` with `LAPLACE_ISA` set to each level, and `text` when ICU is present. What each checks is in [Checks](Checks.md#the-native-tests). The `icx` and `gcc` builds must both pass; both reproduce the prototype's tier-0 IDs and Hilbert values.
