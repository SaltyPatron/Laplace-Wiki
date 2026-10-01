# 3. Builds

PostgreSQL, Laplace-Native, Laplace-postgres, and Laplace-Engine are built in that order, each linking the one before it, and two compilers must agree on every golden value.

## Before this stage

[2. Toolchain](Toolchain.md): the compilers, the flags, the dependencies, and the environment file.

## Operations

### 3.1 Build PostgreSQL

- **In:** the PostgreSQL 18 source, `icx`, ICU, OpenSSL, LZ4, zstd, liburing.
- **Do:** configure with `--with-icu --with-ssl=openssl --with-lz4 --with-zstd --with-liburing CC=icx CXX=icpx` into its own prefix such as `/usr/local/pgsql`; build the server and contrib; install both. The contrib modules include `pg_stat_statements`, `auto_explain`, and `pg_buffercache`, which Laplace uses for observability. PostgreSQL is built with `icx` so that the server and the extensions share one compiler: extensions built with PGXS take their flags from the compiler PostgreSQL was built with, and a gcc-built server hands `icx` flags it rejects.
- **Out:** the server, its `pg_config`, and its library and extension directories.
- **From:** [Builds: PostgreSQL](../Operations/Builds.md#postgresql).

### 3.2 Build PostGIS against it

- **In:** PostGIS 3.6, GEOS, PROJ, GDAL, and the `pg_config` of 3.1.
- **Do:** build and install PostGIS into that server. PostGIS stores four dimensions exactly, as GSERIALIZED with raw `double` ordinate arrays, and its binary paths round-trip Z and M bit for bit. Its metric operations compute in two or three dimensions and treat M as a measure, not a coordinate: there is no 4D distance in PostGIS, which is why Laplace-postgres exists.
- **Out:** the `postgis` extension.
- **From:** [Architecture: Repositories](../Architecture.md#repositories), [Research: Geometry: Dimensionality](../Research/Geometry.md#dimensionality).

### 3.3 Build Laplace-Native, twice

- **In:** the Laplace-Native source, BLAKE3's sources, ICU, libpq, and both compilers.
- **Do:** `cmake --preset icx-release && cmake --build --preset icx-release`, then the same with the `gcc-release` preset. Outputs: `liblaplace`, static and shared; `laplace-bench`, which measures every operation with each SIMD kernel beside its scalar form; `laplace-ingest`, which needs ICU and libpq. The baseline is x86-64-v2; kernels are compiled per ISA level in their own translation units and chosen at run time, so one binary runs everywhere and uses everything, and `LAPLACE_ISA=scalar|sse2|avx2` lowers the level to compare kernels. Every summation has one fixed order in every code path, so scalar and SIMD kernels agree bit for bit. IDs and coordinates are exact integers or fixed point. The model tools need MKL and OpenMP and build only when the oneAPI environment is set; the core library and the extension do not depend on them.
- **Out:** two builds of the shared library.
- **From:** [Builds: Laplace-Native](../Operations/Builds.md#laplace-native).

### 3.4 Build Laplace-postgres and install the extension

- **In:** the Laplace-postgres source, the `pg_config` of 3.1, the static library of 3.3.
- **Do:** `cmake --preset icx-release && cmake --build --preset icx-release`, then `cmake --install`. CMake reads only the paths from `pg_config` and links Laplace-Native in statically. Install into PostgreSQL's library and extension directories; making those directories group-writable for an extensions group lets a build install without root. Changing the extension uses versioned upgrade scripts, `ALTER EXTENSION laplace UPDATE`, never a drop: dropping the extension drops every index built on its functions, such as the GIN container index.
- **Out:** the `laplace` extension, installed, expanding PostgreSQL to 4D throughout, with real math from Laplace-Native, alongside what PostGIS already provides rather than replacing it.
- **From:** [Builds: Laplace-postgres](../Operations/Builds.md#laplace-postgres), [Architecture: Repositories](../Architecture.md#repositories).

### 3.5 Compare the two compilers

- **In:** the `icx` and `gcc` builds of 3.3.
- **Do:** run both over the golden values: the tier-0 IDs and Hilbert values, and every other value a kernel produces.
- **Out:** proof that results do not depend on the compiler.
- **From:** [Builds: Laplace-Native](../Operations/Builds.md#laplace-native), [Research: Engine Measurements: Native operations](../Research/Engine.md#native-operations).

### 3.6 Build the tree-sitter grammars

- **In:** the tree-sitter runtime and the grammar checkouts.
- **Do:** compile each grammar the code recipes of [10. Recipes](Recipes.md) will read. Every node records its byte range, and whitespace is the gap between tokens, so the tokens plus the stored gaps rebuild a source file exactly. A grammar that ships without generated sources, such as LaTeX, needs `tree-sitter generate` before use.
- **Out:** the grammars under the build root.
- **From:** [Research: Recipes: Grammars](../Research/Recipes.md#grammars).

### 3.7 Build Laplace-Engine

- **In:** the Laplace-Engine source, the library of 3.3, libpq, the grammars of 3.6.
- **Do:** build Laplace itself against Laplace-Native, working against a database extended by Laplace-postgres. Every build has a fingerprint.
- **Out:** the engine.
- **From:** [Architecture: Repositories](../Architecture.md#repositories).

### 3.8 Record the fingerprints

- **In:** every build of this stage.
- **Do:** every build has a fingerprint. Record it, so an install knows which build it has.
- **Out:** the fingerprints an install is identified by, alongside the tier-0 fingerprint of [5. Tier 0](Tier-0.md). One deployed revision: the application, the prefix native libraries, the PostgreSQL execution module, and the tier-0 perf-cache identify one build, and [29. Maintenance](Maintenance.md) operation 29.7 proves it in the serving process.
- **From:** [Architecture: Native C](../Architecture.md#native-c).

## What this stage leaves behind

The server, PostGIS, the library, the extension, the grammars, and the engine, each fingerprinted, and the proof that two compilers give the same golden values.

## Without this stage

There is no generator for tier 0, no 4D functions in the database, no decomposer, no ingestion, and no engine.
