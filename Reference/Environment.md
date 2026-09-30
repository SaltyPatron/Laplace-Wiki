# Environment

One file, `Laplace-Engine/laplace.env`, defines where everything is; every build and the `laplace` program read the same variables, each with a compiled-in default for when it is unset.

`source /repos/src/Laplace-Engine/laplace.env` before building or running anything. The file exports the variables below, sources Intel oneAPI's `setvars.sh`, sets `PG_CONFIG`, and puts the engine's build directory and PostgreSQL's `bin` on the path. `cmake/LaplacePaths.cmake` in Laplace-Native reads the same names at configure time, taking the environment when a variable is set and the default when it is not; `-D` on the CMake command line overrides both.

## Paths

| Variable | Default | Read by | What |
| --- | --- | --- | --- |
| `LAPLACE_SRC` | `/repos/src` | `laplace.env`, `LaplacePaths.cmake`, `build.sh` | the source root: Laplace's repositories and its dependencies' |
| `LAPLACE_BUILD` | `/repos/build` | the CMake presets (`binaryDir`), `build.sh` | build trees: `$LAPLACE_BUILD/<repo>/icx-release` |
| `LAPLACE_WORK` | `/repos/work` | `laplace.env`, `laplace ingest` (logs) | generated data, logs, scripts that need root |
| `LAPLACE_DEPS` | `/repos/deps` | `laplace.env` | installed dependencies |
| `LAPLACE_DATA` | `/vault/Data` | recipe `root` lines (`$LAPLACE_DATA`), `laplace.env` | corpora and the Unicode data |
| `LAPLACE_MODELS` | `/vault/models` | recipe `files` lines | model checkpoints and tokenizers |
| `LAPLACE_NATIVE` | `$LAPLACE_SRC/Laplace-Native` | the extension's and engine's `CMakeLists.txt` | where to `add_subdirectory` the library from |
| `LAPLACE_SQL` | `$LAPLACE_SRC/Laplace-postgres/sql` | `laplace deploy`, `laplace index` | the schema, semantics, lookup, and index scripts |
| `LAPLACE_RECIPES` | `$LAPLACE_SRC/Laplace-Engine/recipes` | `laplace ingest`, `sources`, `tree`; `firmware_path()` | the recipes directory, holding `order` and one directory per source |
| `LAPLACE_FIRMWARE` | `$LAPLACE_SRC/Laplace-Engine/firmware/program.firmware` | `laplace pull`, `hop`, `translate`, `degrees`, `fills` | the firmware a pull runs under; `--firmware FILE` overrides it per command |
| `LAPLACE_TIER0` | `$LAPLACE_WORK/tier0/tier0.bin`; compiled default `/repos/work/tier0/tier0.bin` | `lp_tier0_path()` in every program and backend; `laplace tier0` writes it | the tier-0 perf-cache |
| `LAPLACE_FLAGS` | tier 0's path with `.flags` in place of its ending | `lp_flags_path()` | the flags that go with tier 0; its layout is the same path plus `.layout` |
| `LAPLACE_GRAMMARS` | `$LAPLACE_BUILD/grammars`; compiled default `/repos/build/grammars` | `grammar_load()` in the engine | `libtree-sitter-<name>.so`, written by `tools/build_grammars.sh` |
| `LAPLACE_UCD` | `$LAPLACE_DATA/UCD`; compiled default `/vault/Data/UCD` | `laplace tier0`, `laplace flags` (`$LAPLACE_UCD/Public/UCD/latest`) | the Unicode data tier 0 is generated from |
| `LAPLACE_ICU_DIR` | `$LAPLACE_DEPS/icu78` | Laplace-Native, the engine's rpath | ICU 78, Unicode 17 |
| `LAPLACE_PG_DIR` | `/usr/local/pgsql` | Laplace-postgres (`pg_config`), the engine (libpq, rpath) | PostgreSQL 18, built with `icx` |
| `LAPLACE_BLAKE3_DIR` | `$LAPLACE_SRC/blake3/c` | Laplace-Native | BLAKE3 C sources |
| `LAPLACE_COREMATH` | `$LAPLACE_SRC/core-math` | Laplace-Native | CORE-MATH sources |
| `LAPLACE_TREESITTER` | `$LAPLACE_SRC/tree-sitter` | the engine | the tree-sitter runtime |
| `LAPLACE_CONNINFO` | `host=/tmp port=5432 user=laplace dbname=laplace_engine` | every command that touches the database; `-d conninfo` overrides per command | the database, as a libpq connection string |
| `PG_CONFIG` | `$LAPLACE_PG_DIR/bin/pg_config` | Laplace-postgres | the target server |

## Run-time controls

| Variable | Default | Read by | Effect |
| --- | --- | --- | --- |
| `OMP_NUM_THREADS`, `MKL_NUM_THREADS` | `nproc`, set by `laplace.env` | OpenMP and MKL kernels | how many cores the kernels use; a shell that sets them to 1 makes every kernel single-threaded, measured at 110.8 s against 19.9 s |
| `LAPLACE_ISA` | unset | `lp_cpu_active()` | `scalar`, `sse2`, `avx2`, or `avx512` lowers the dispatch level, never raises it past what the CPU has; the native test suite runs the matching test at each level |
| `LAPLACE_BATCH_MB` | 1024 | `laplace ingest` | the bytes of files decomposed per batch before the node table is written and emptied |
| `LAPLACE_ROOM_FACTOR` | 65 | `laplace ingest` with no source named | for a source whose `source` file gives no `room`, the multiplier of its files' size taken as what it will take in the database |
| `LAPLACE_TRUNKS` | unset | `laplace ingest` | when set, prints each file's trunk ID after the recompose check |
| `LAPLACE_ONE_PARSE` | unset | the engine's parsers | diagnostic: parse on one thread |

## Database settings the engine sets

| Setting | Set by | Value | Read by |
| --- | --- | --- | --- |
| `laplace.tier0` | `laplace deploy`: `ALTER DATABASE … SET laplace.tier0 = '<path>'` | `lp_tier0_path()` at deploy time | every backend, which memory-maps the file on first use; `laplace_fingerprint()` and `laplace status` report it |
| `laplace.flags` | `laplace deploy`: `ALTER DATABASE … SET laplace.flags = '<path>'` | `lp_flags_path()` | the flag functions of [SQL](SQL.md#the-flags-that-go-with-tier-0) |
| `synchronous_commit` | every connection of `load()` | `off` | the bulk session |
| `plan_cache_mode` | `db_ask()` on its first prepared statement per connection | `force_generic_plan` | the read commands' prepared statements, planned once per connection |
| `client_min_messages` | `db_connect()` | `warning` | every connection |
| `enable_parallel_append` | `schema.sql` | `off` for the database | the planner |
| `parallel_workers` | `schema.sql` | 0 on every `physicality_t*` partition | the planner |
| statistics on `physicality.path` | `schema.sql` | 0 | `ANALYZE` |
| `maintenance_work_mem`, `max_parallel_maintenance_workers` | `indexes.sql`, for the session | 8 GB, 6 | the index builds |

The server-level settings of [Operations: Database](../Operations/Database.md), memory, I/O, WAL, planning, and observability, are set with `ALTER SYSTEM` by the operator and are not set by any Laplace program.
