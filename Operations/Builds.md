# Builds

PostgreSQL, Laplace-Native, and Laplace-postgres are built from source with Intel's compilers, with floating-point settings that give the same bits on every CPU.

## PostgreSQL

PostgreSQL is built with `icx` so that the server and the extensions share one compiler, into its own prefix such as `/usr/local/pgsql`:

`setup.sh` (part `deps`) builds it as root, from `REL_18_STABLE` under `$LAPLACE_DEPSRC`, in `$LAPLACE_WORK/postgresql`:

```sh
$LAPLACE_DEPSRC/postgresql/configure --prefix=$LAPLACE_PG_DIR --with-icu --with-ssl=openssl --with-lz4 --with-zstd \
    --with-liburing CC=icx CXX=icpx ICU_CFLAGS=-I$LAPLACE_ICU_DIR/include \
    ICU_LIBS="-L$LAPLACE_ICU_DIR/lib -licui18n -licuuc -licudata"
make -j$(nproc) && make install
```

- The contrib modules Laplace uses are installed one by one, each when its library is missing: `pg_stat_statements` and `auto_explain` (preloaded by the settings), `pg_buffercache`, and `pg_walinspect` (read by `ingest.sh` while it loads).
- `psql` and `pg_config` are linked into `$LAPLACE_PREFIX/bin`.
- The Autoconf build does not track header dependencies unless it is configured with `--enable-depend`. After changing configure options, run `make clean` first, or the new options never reach the binary.
- Extensions built with PGXS take their flags from the compiler PostgreSQL was built with. A gcc-built server hands `icx` flags it rejects, which is one reason to build the server with `icx` too.

## Laplace-Native

```sh
source /repos/src/Laplace-Operations/laplace.env
cmake --preset icx-release && cmake --build --preset icx-release && ctest --test-dir $LAPLACE_BUILD/Laplace-Native/icx-release
cmake --preset gcc-release && cmake --build --preset gcc-release
```

- **Outputs:** `liblaplace` (static and shared, linked with `Laplace::math` over CORE-MATH), `laplace_text` (needs ICU), `laplace_model` (needs MKL and OpenMP), `laplace_linalg` (needs Eigen and Spectra headers), `Laplace.Native.Interop` (generated C# bindings from the public headers' AST), `laplace-tier0`, and the tests. `Laplace-Native` installs the `LaplaceNative` CMake package (`native-package.sh`), which `Laplace-postgres`, `Laplace-Engine`, and `Laplace-MCP` consume via `find_package(LaplaceNative CONFIG REQUIRED)` rather than `add_subdirectory`.
- **Determinism:**
  - `icx` defaults to fast floating-point math, and its `-fp-model=precise` still fuses multiplies and adds into FMAs, which round once where two operations round twice. The build turns fusing off (`-ffp-contract=off -fno-fast-math`) and never uses black-box compiler auto-dispatch (`-ax…` or `-xHost`).
  - Every summation has one fixed order in every code path, so scalar and SIMD kernels agree bit for bit.
  - IDs and coordinates are exact integers or fixed point.
- **ISA levels:** the baseline is `x86-64-v2`. Explicit per-ISA translation units are compiled under `icx -fp-model=precise -ffp-contract=off` (`x86-64-v3` AVX2/BMI2, `avxvnni`, `x86-64-v4` AVX-512, `avx512vnni`) and `Laplace-Native/src/cpu.c` dispatches bit-identical kernels at run time, so one binary runs everywhere and uses everything. `LAPLACE_ISA=scalar|sse2|avx2|avxvnni|avx512|avx512vnni` lowers the active level to compare kernels.
- **Model kernels:** `laplace_model` and its `lp_rowsig` kernel need MKL and OpenMP; a build without MKL's headers on its path (a gcc build outside the oneAPI environment) fails there. The core library and the PostgreSQL extension do not depend on them.
- **The two compilers:** the `icx` and `gcc` builds must agree on every golden value, such as the tier-0 IDs and Hilbert values, bit for bit.
- **BLAKE3:** its CMake recognizes gcc, clang, and MSVC but not `icx`, so Laplace-Native supplies BLAKE3's assembly sources itself, and enables C, C++, and assembly in its own project.

## Laplace-postgres

```sh
./build.sh            # Laplace-postgres and Laplace-Engine, icx, RelWithDebInfo, Ninja, under $LAPLACE_BUILD/<repo>/icx-release
./build.sh install    # and the extension installed
```

- **Build:** CMake reads the paths from `pg_config` and consumes the `LaplaceNative` CMake package (`find_package(LaplaceNative CONFIG REQUIRED)`), linking `Laplace::laplace_static` and `Laplace::text`. Laplace-Engine's build makes the one program, `laplace`.
- **Install:** into PostgreSQL's library and extension directories, staged with `DESTDIR` and renamed over the files there, so a backend that has the old library mapped keeps its inode. `setup.sh` makes those directories group-writable for `postgres-extensions` (mode 2775), so a build installs without root. The extension's own CI builds it and runs only checks that need no database; its regression cases run after the deployment, against the deployed database and the installed extension ([Checks](../Reference/Checks.md#the-database-checks)).
- **Changing the extension:** the build hashes only `blake3` and the four persistent storage table DDLs into `laplace-storage:<hash>` and emits `laplace.reconcile.sql` for all replaceable C/SQL functions, casts, operators, opclasses, and indexes. When storage DDL is unchanged, `laplace deploy` reconciles the installed extension in place (`ALTER EXTENSION laplace UPDATE TO ...`) while preserving all loaded rows and indexes; a database is recreated (`laplace deploy --recreate`) only when persistent storage DDL changes. The extension is never dropped out of a database that is kept (`DROP EXTENSION laplace CASCADE` would drop every column and index built on its types and functions).
