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

- **Outputs:** `liblaplace`, static and shared; `laplace_text` (needs ICU); `laplace_model` (needs MKL); the tests. The programs that use it are Laplace-Engine's `laplace` and the extension, each of which builds Laplace-Native as part of itself.
- **Determinism:**
  - `icx` defaults to fast floating-point math, and its `-fp-model=precise` still fuses multiplies and adds into FMAs, which round once where two operations round twice. The build turns fusing off (`-ffp-contract=off`) and never uses fast math.
  - Every summation has one fixed order in every code path, so scalar and SIMD kernels agree bit for bit.
  - IDs and coordinates are exact integers or fixed point.
- **ISA levels:** the baseline is x86-64-v2. Kernels are compiled per ISA level in their own translation units and chosen at run time, so one binary runs everywhere and uses everything. `LAPLACE_ISA=scalar|sse2|avx2` lowers the level to compare kernels.
- **Model kernels:** `laplace_model` and its `lp_rowsig` kernel need MKL and OpenMP; a build without MKL's headers on its path (a gcc build outside the oneAPI environment) fails there. The core library and the PostgreSQL extension do not depend on them.
- **The two compilers:** the `icx` and `gcc` builds must agree on every golden value, such as the tier-0 IDs and Hilbert values, bit for bit.
- **BLAKE3:** its CMake recognizes gcc, clang, and MSVC but not `icx`, so Laplace-Native supplies BLAKE3's assembly sources itself, and enables C, C++, and assembly in its own project.

## Laplace-postgres

```sh
./build.sh            # Laplace-postgres and Laplace-Engine, icx, RelWithDebInfo, Ninja, under $LAPLACE_BUILD/<repo>/icx-release
./build.sh install    # and the extension installed
```

- **Build:** CMake reads only the paths from `pg_config` and links Laplace-Native in statically. Laplace-Engine's build makes the one program, `laplace`.
- **Install:** into PostgreSQL's library and extension directories, staged with `DESTDIR` and renamed over the files there, so a backend that has the old library mapped keeps its inode. `setup.sh` makes those directories group-writable for `postgres-extensions` (mode 2775), so a build installs without root. The extension's CI installs the extension fresh into a scratch database at its newest version before it updates the database.
- **Changing the extension:** use versioned upgrade scripts (`ALTER EXTENSION laplace UPDATE`), never a drop. Dropping the extension drops every index built on its functions, such as the GIN container index.
