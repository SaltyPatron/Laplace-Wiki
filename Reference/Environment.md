# Environment

One file, `Laplace-Operations/laplace.env`, defines where everything is; every build and the `laplace` program read the same variables, each with a compiled-in default for when it is unset.

`source /repos/src/Laplace-Operations/laplace.env` before building or running anything. The file exports the variables below, sources Intel oneAPI's `setvars.sh`, sets `PG_CONFIG`, and puts the engine's build directory and PostgreSQL's `bin` on the path. `cmake/LaplacePaths.cmake` in Laplace-Native reads the same names at configure time, taking the environment when a variable is set and the default when it is not; `-D` on the CMake command line overrides both.

## Paths

| Variable | Default | Read by | What |
| --- | --- | --- | --- |
| `LAPLACE_SRC` | `/repos/src` | `laplace.env`, `LaplacePaths.cmake`, `build.sh` | the source root: Laplace's repositories and its dependencies' |
| `LAPLACE_BUILD` | `/repos/build` | the CMake presets (`binaryDir`), `build.sh` | build trees: `$LAPLACE_BUILD/<repo>/icx-release` |
| `LAPLACE_WORK` | `/repos/work` | `laplace.env`, every Operations script, `laplace ingest` | generated data and logs: `logs/root` (setup.sh, agents.sh), `logs/deploy`, `logs/ingest-runs`, `logs/ingest`, and tier 0 |
| `LAPLACE_DEPSRC` | `$LAPLACE_SRC` | `laplace.env`, `setup.sh` | the dependencies' sources (BLAKE3, CORE-MATH, tree-sitter, PostgreSQL, …): beside Laplace's, or elsewhere |
| `LAPLACE_DEPS` | `/repos/deps` | `laplace.env` | installed dependencies |
| `LAPLACE_DATA` | `/vault/Data` | recipe `root` lines (`$LAPLACE_DATA`), `laplace.env` | corpora and the Unicode data |
| `LAPLACE_MODELS` | `/vault/models` | recipe `files` lines | model checkpoints and tokenizers |
| `LAPLACE_NATIVE` | `$LAPLACE_SRC/Laplace-Native` | the extension's and engine's `CMakeLists.txt` | where to `add_subdirectory` the library from |
| `LAPLACE_RECIPES` | `$LAPLACE_SRC/Laplace-Engine/recipes` | `laplace ingest`, `sources`, `tree`; `firmware_path()` | the recipes directory, holding `order` and one directory per source |
| `LAPLACE_FIRMWARE` | `$LAPLACE_SRC/Laplace-Engine/firmware/program.firmware` | `laplace pull`, `turn`, `hop`, `translate`, `degrees` | the firmware a pull runs under; `--firmware FILE` overrides it per command |
| `LAPLACE_HIGHWAY` | `${LAPLACE_TIER0%.bin}.highway` | `lp_highway_path()` in every program and backend; `laplace highway` writes it | the highway perf-cache: the types the resources list, and the mappings between them |
| `LAPLACE_MANIFEST` | Laplace-Native's `manifest` (compiled in, `LAPLACE_MANIFEST_DEFAULT`) | `laplace highway` | `banks.tsv` and the frozen slots `slots/LIST.tsv`, which the highway reads and writes back |
| `LAPLACE_TIER0` | `$LAPLACE_WORK/tier0/tier0.bin`; compiled default `/repos/work/tier0/tier0.bin` | `lp_tier0_path()` in every program and backend; `laplace tier0` writes it | the tier-0 perf-cache |
| `LAPLACE_FLAGS` | tier 0's path with `.flags` in place of its ending | `lp_flags_path()` | the flags that go with tier 0; its layout is the same path plus `.layout` |
| `LAPLACE_GRAMMARS` | `$LAPLACE_BUILD/grammars`; compiled default `/repos/build/grammars` | `grammar_load()` in the engine | `libtree-sitter-<name>.so`, written by `tools/build_grammars.sh` |
| `LAPLACE_UCD` | `$LAPLACE_DATA/UCD`; compiled default `/vault/Data/UCD` | `laplace tier0`, `laplace flags` (`$LAPLACE_UCD/Public/UCD/latest`) | the Unicode data tier 0 is generated from |
| `LAPLACE_ICU_DIR` | `$LAPLACE_DEPS/icu78` | Laplace-Native, the engine's rpath | ICU 78, Unicode 17 |
| `LAPLACE_PG_DIR` | `/usr/local/pgsql` | Laplace-postgres (`pg_config`), the engine (libpq, rpath) | PostgreSQL 18, built with `icx` |
| `LAPLACE_BLAKE3_DIR` | `$LAPLACE_DEPSRC/blake3/c` | Laplace-Native | BLAKE3 C sources |
| `LAPLACE_COREMATH` | `$LAPLACE_DEPSRC/core-math` | Laplace-Native | CORE-MATH sources |
| `LAPLACE_TREESITTER` | `$LAPLACE_DEPSRC/tree-sitter` | the engine | the tree-sitter runtime |
| `LAPLACE_CONNINFO` | `host=/tmp port=5432 user=laplace dbname=laplace` | every command that touches the database; `-d conninfo` overrides per command | the database, as a libpq connection string |
| `PG_CONFIG` | `$LAPLACE_PG_DIR/bin/pg_config` | Laplace-postgres | the target server |

## The machine

`laplace.env` also names the machine `setup.sh`, `deploy.sh`, `ingest.sh` and `agents.sh` work on; each is `${VAR:-default}`.

| Variable | Default | What |
| --- | --- | --- |
| `LAPLACE_PREFIX` | `/usr/local` | where the dependencies built from source install |
| `LAPLACE_PGDATA`, `LAPLACE_PGWAL`, `LAPLACE_PGTEMP` | `/data/pgdata`, `$LAPLACE_PGDATA/pg_wal`, `/data/pgtemp` | the cluster, its write-ahead log and its temporary files, each on its own volume |
| `LAPLACE_VOLUMES` | the volumes of this machine | `vg lv size fs mount` per volume; an existing volume is never resized or reformatted |
| `LAPLACE_PGUSER`, `LAPLACE_PGSERVICE` | `postgres`, `pgdata` | the server's user and its systemd unit |
| `LAPLACE_ROLE` | `laplace` | the database role Laplace connects as |
| `LAPLACE_LAN` | `192.168.1.0/24` | the network the server is reachable from, over TLS |
| `LAPLACE_SOURCES` | empty: every source in `recipes/order` | the sources `ingest.sh` takes when none is named |
| `LAPLACE_LOCKS` | `/run/lock/laplace` | the per-database locks of `deploy.sh` and `ingest.sh`, made at boot |
| `LAPLACE_GITHUB`, `LAPLACE_REPOS` | `SaltyPatron`; the five repositories | what `agents.sh` registers runners for |
| `LAPLACE_AGENT_USER`, `LAPLACE_AGENT_HOME`, `LAPLACE_AGENT_LABELS` | `laplace-runner`, `/var/lib/agents/laplace-runner`, `laplace` | the runners' user, their directories, their labels |
| `LAPLACE_GROUP`, `LAPLACE_PG_GROUP` | `laplace-runner`, `postgres-extensions` | the group the operator and the runners share; the group that installs extensions |
| `LAPLACE_GRAMMAR_SRC` | `$LAPLACE_DATA/TreeSitter` | the grammars' sources `build_grammars.sh` compiles |
| `LAPLACE_DROP` | unset | `setup.sh drop` runs only when it names the data directory |
| `LAPLACE_AGENT_TOKEN_<REPO>`, `LAPLACE_CHECKOUT_TOKEN` | unset | `agents.sh`: a registration token per repository, and the token stored as the secret `LAPLACE_CHECKOUT` |

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
| `laplace.highway` | `laplace deploy`: `ALTER DATABASE … SET laplace.highway = '<path>'` | `lp_highway_path()` | the highway's functions of [SQL](SQL.md) |
| `synchronous_commit` | every connection of `load()` | `off` | the bulk session |
| `plan_cache_mode` | `db_ask()` on its first prepared statement per connection | `force_generic_plan` | the read commands' prepared statements, planned once per connection |
| `client_min_messages` | `db_connect()` | `warning` | every connection |
| `enable_parallel_append` | `laplace deploy` | `off` for the database | the planner |
| `parallel_workers` | the extension's install script | 0 on every `physicality_t*` partition | the planner |
| statistics on `physicality.path` | the extension's install script | 0 | `ANALYZE` |
| `maintenance_work_mem` | `laplace index` | 8 GB for the session | index builds |

The server-level settings of [Operations: Database](../Operations/Database.md), memory, I/O, WAL, planning, and observability, are set with `ALTER SYSTEM` by `sudo ./setup.sh settings` and are not set by any Laplace program.
