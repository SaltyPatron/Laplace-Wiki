# 2. Toolchain

The machine, the drives, the source root, and every dependency built from source with one compiler and the flags that give the same bits everywhere.

Laplace is native C, with SQL and C# as orchestration. Bit-perfect determinism across hardware and operating systems requires a specific build configuration, and every build has a fingerprint. This stage fixes what every later stage is compiled and measured with.

## Before this stage

[1. Unicode](Unicode.md): the version that the ICU build in 2.6 must match.

## Operations

### 2.1 Place the machine

- **In:** an x86-64 machine.
- **Do:** require x86-64-v2 at minimum. Every Laplace kernel is compiled for each ISA level and chosen at run time: x86-64-v3 with AVX2, FMA, and BMI2; AVX-VNNI; x86-64-v4 with AVX-512; AVX-512 VNNI. A CPU without a level runs the next level down, with the same results. No GPU is required; a third-party tool that produces input for Laplace may use one. Memory: enough for PostgreSQL's shared buffers, about a quarter of RAM, on huge pages, plus the operating system's page cache.
- **Out:** the ISA levels this machine will run.
- **Check:** Intel's Software Development Emulator runs AVX-512 paths on a CPU that lacks them, for comparing kernels.
- **From:** [Setup: Hardware](../Operations/Setup.md#hardware).

### 2.2 Lay out the drives

- **In:** the machine's drives.
- **Do:** put the PostgreSQL heap and indexes on the fastest drive, NVMe, for random reads; the write-ahead log on a separate SSD, for sequential writes that do not compete with reads; PostgreSQL temporary files on a separate SSD as a tablespace, for sorts and index builds that spill; repositories and build trees on an SSD; datasets and archives on any bulk storage, read once at ingestion.
- **Out:** the paths the database in [6. Database](Database.md) is initialized on.
- **Check:** a database on a spinning disk works, and every time it measures is an upper bound: the prototype's database sat on a USB hard disk.
- **From:** [Setup: Storage](../Operations/Setup.md#storage).

### 2.3 Lay out the source root

- **In:** the repositories.
- **Do:** put all repositories, Laplace's and its dependencies' alike, under one source root, such as `/repos/src`, with build trees kept outside it, such as `/repos/build` and `/repos/work`: build trees under `/repos/build`, installed dependencies under `/repos/deps`, generated data and logs and root scripts under `/repos/work`, and the corpora and Unicode data on the bulk storage. Laplace's own repositories are Laplace-Native, Laplace-postgres, Laplace-Engine, Laplace-Prototype, and Laplace-Wiki.
- **Out:** one source root, one build root, one work root.
- **From:** [Setup: Repositories](../Operations/Setup.md#repositories).

### 2.4 Install the compilers

- **In:** Intel oneAPI 2025 or newer, and a current gcc.
- **Do:** oneAPI's `icx`, `icpx`, MKL, TBB, and IPP are the primary compilers and libraries; every build uses them. gcc is the second compiler, used to check that results do not depend on the compiler. CMake 3.24 or newer, 4.x for `icx` 2026, builds Laplace; Meson 0.61 or newer and Ninja build PostgreSQL.
- **Out:** both compilers on the path.
- **From:** [Setup: Toolchain](../Operations/Setup.md#toolchain).

### 2.5 Fix the floating-point configuration

- **In:** the compilers.
- **Do:** every build uses strict IEEE-754 semantics, so every operation rounds exactly as specified; no fast-math, so no reassociation, reciprocal approximation, or flushing; no FP contraction, `-ffp-contract=off`, so `a*b + c` is not silently fused into one rounding; SSE2 floating point, binary64 throughout, no x87 80-bit intermediates; and a correctly rounded libm. `icx` defaults to fast floating-point math, and its `-fp-model=precise` still fuses multiplies and adds into FMAs, which round once where two operations round twice, so fusing is turned off explicitly.
- **Out:** the flags every Laplace build and every dependency is compiled with.
- **Check:** [3. Builds](Builds.md) operation 3.5, where `icx` and `gcc` must agree bit for bit.
- **From:** [Builds: Laplace-Native](../Operations/Builds.md#laplace-native), [Research: Numerics: Deterministic builds](../Research/Numerics.md#deterministic-builds).

### 2.6 Build the dependencies from source

- **In:** the dependency sources under the source root.
- **Do:** clone and build each one with `icx`, with the flags of 2.5 and the math libraries that give the same bits across hardware, operating systems, and linkers:
  - **ICU 78** or newer, into `/repos/deps/icu78`: the Unicode 17 segmentation, at the version fixed in [1. Unicode](Unicode.md).
  - **BLAKE3**: the identity hash. Its CMake recognizes gcc, clang, and MSVC but not `icx`, so Laplace-Native supplies BLAKE3's assembly sources itself.
  - **CORE-MATH**: correctly rounded `sin` and `cos`. libm `sin` and `cos` are not required to be correctly rounded, and glibc, musl, MSVC, and CUDA differ in the last bits, so without this the same codepoint gets different points on different machines. Its binary64 `sin` and `cos` hard-to-round cases have been fully solved.
  - **Eigen 3.4** and **Spectra**: the 4D math in the extension functions.
  - **hnswlib**.
  - **GEOS, PROJ, GDAL**: PostGIS's own dependencies.
  - **PostGIS 3.6**: built against the PostgreSQL of [3. Builds](Builds.md).
  - **tree-sitter**: the runtime and the grammars that code recipes read in [7. Recipes](Recipes.md).
  - **liburing 2.1** or newer: optional, for the I/O method test in [6. Database](Database.md).
  - **PostgreSQL 18** is built in [3. Builds](Builds.md), not here, because the extension's flags come from it.
- **Out:** installed dependencies under `/repos/deps`, each with its build fingerprint.
- **From:** [Setup: Repositories](../Operations/Setup.md#repositories), [Setup: Toolchain](../Operations/Setup.md#toolchain), [Builds: Laplace-Native](../Operations/Builds.md#laplace-native), [Research: Numerics: Deterministic builds](../Research/Numerics.md#deterministic-builds).

### 2.7 Write the environment file

- **In:** every path from 2.2 to 2.6.
- **Do:** one environment file sources oneAPI and points the builds at Eigen, Spectra, BLAKE3, and the custom PostgreSQL. It is sourced for Laplace and PostgreSQL builds only, not for anything built against another PostgreSQL. It sets `OMP_NUM_THREADS` and `MKL_NUM_THREADS` to the number of cores: some shells and agents set them to 1, which makes every kernel single-threaded, and the same kernel run over one vocabulary took 110.8 s on one thread and 19.9 s on twelve.
- **Out:** the one definition of where everything is.
- **From:** [Setup: Toolchain](../Operations/Setup.md#toolchain), [Research: Engine Measurements: Native operations](../Research/Engine.md#native-operations).

### 2.8 Script everything that needs root

- **In:** every step that needs root: installing to system prefixes, reserving huge pages, starting the server.
- **Do:** write it as a script that logs its output, so the result can be read afterward.
- **Out:** a log for every privileged step.
- **From:** [Setup: Toolchain](../Operations/Setup.md#toolchain).

## What this stage leaves behind

One machine, one source root, one environment file, and one toolchain that every Laplace build and every dependency is compiled with, under one floating-point configuration.

## Without this stage

Nothing compiles, and anything that compiles elsewhere does not agree bit for bit, so no two installs could share a fingerprint and no measurement would be comparable.
