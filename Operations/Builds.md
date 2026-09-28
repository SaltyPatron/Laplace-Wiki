# Builds

PostgreSQL, Laplace-Native, and Laplace-postgres are built from source with Intel's compilers, with floating-point settings that give the same bits on every CPU.

## PostgreSQL

PostgreSQL is built with `icx` so that the server and the extensions share one compiler, into its own prefix such as `/usr/local/pgsql`:

```sh
source toolchain.env
mkdir -p $BUILD/postgresql && cd $BUILD/postgresql
$SRC/postgresql/configure --prefix=$PREFIX --with-icu --with-ssl=openssl --with-lz4 --with-zstd \
    --with-liburing CC=icx CXX=icpx
make -j$(nproc) && make -j$(nproc) -C contrib
sudo make install && sudo make -C contrib install
```

- The contrib modules include `pg_stat_statements`, `auto_explain`, and `pg_buffercache`, which Laplace uses for observability.
- The Autoconf build does not track header dependencies unless it is configured with `--enable-depend`. After changing configure options, run `make clean` first, or the new options never reach the binary. Meson tracks dependencies and avoids this.
- Extensions built with PGXS take their flags from the compiler PostgreSQL was built with. A gcc-built server hands `icx` flags it rejects, which is one reason to build the server with `icx` too.

## Laplace-Native

```sh
source toolchain.env
cmake --preset icx-release && cmake --build --preset icx-release
cmake --preset gcc-release && cmake --build --preset gcc-release
```

- **Outputs:**
  - `liblaplace`, static and shared;
  - `laplace-bench`, which measures every operation with each SIMD kernel beside its scalar form;
  - `laplace-ingest`, which needs ICU and libpq.
- **Determinism:**
  - `icx` defaults to fast floating-point math, and its `-fp-model=precise` still fuses multiplies and adds into FMAs, which round once where two operations round twice. The build turns fusing off (`-ffp-contract=off`) and never uses fast math.
  - Every summation has one fixed order in every code path, so scalar and SIMD kernels agree bit for bit.
  - IDs and coordinates are exact integers or fixed point.
- **ISA levels:** the baseline is x86-64-v2. Kernels are compiled per ISA level in their own translation units and chosen at run time, so one binary runs everywhere and uses everything. `LAPLACE_ISA=scalar|sse2|avx2` lowers the level to compare kernels.
- **The two compilers:** the `icx` and `gcc` builds must agree on every golden value, such as the tier-0 IDs and Hilbert values, bit for bit.
- **BLAKE3:** its CMake recognizes gcc, clang, and MSVC but not `icx`, so Laplace-Native supplies BLAKE3's assembly sources itself, and enables C, C++, and assembly in its own project.

## Laplace-postgres

```sh
cmake --preset icx-release && cmake --build --preset icx-release
cmake --install $BUILD/Laplace-postgres/icx-release
```

- **Build:** CMake reads only the paths from `pg_config` and links Laplace-Native in statically.
- **Install:** into PostgreSQL's library and extension directories. Making those directories group-writable for an extensions group lets a build install without root.
- **Changing the extension:** use versioned upgrade scripts (`ALTER EXTENSION laplace UPDATE`), never a drop. Dropping the extension drops every index built on its functions, such as the GIN container index.
