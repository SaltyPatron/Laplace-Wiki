# Setup

Laplace runs on x86-64 CPUs, uses every SIMD level the CPU has, never requires a GPU, and wants its database heap, write-ahead log, and temporary files on separate fast drives.

## Hardware

- **CPU:** x86-64-v2 at minimum. Every Laplace kernel is compiled for each ISA level and chosen at run time:
  - x86-64-v3 with AVX2, FMA, and BMI2;
  - AVX-VNNI;
  - x86-64-v4 with AVX-512;
  - AVX-512 VNNI.

  A CPU without a level runs the next level down, with the same results. Some consumer CPUs have AVX-VNNI but not AVX-512 (Intel's hybrid cores), while server CPUs and AMD Zen 4 and later have AVX-512. Intel's Software Development Emulator (SDE) runs AVX-512 paths on a CPU that lacks them.
- **GPU:** Laplace never requires one. Third-party tools that produce input for Laplace, such as a neural dependency parser used as a witness, may use one. As an example, that parser ran ten times faster on a GTX 1080 Ti than on six CPU threads.
- **Memory:** enough for PostgreSQL's shared buffers (about a quarter of RAM) on huge pages, plus the operating system's page cache.

## Storage

| Data | Put it on | Why |
| --- | --- | --- |
| PostgreSQL heap and indexes | the fastest drive, NVMe | random reads for index lookups |
| Write-ahead log | a separate SSD | sequential writes that do not compete with reads |
| PostgreSQL temporary files | a separate SSD, as a tablespace | sorts and index builds that spill |
| Repositories and build trees | an SSD | |
| Datasets and archives | any bulk storage | read once, at ingestion |

A database on a spinning disk works, and every time it measures is an upper bound: the prototype's database sat on a USB hard disk.

## Repositories

All repositories, Laplace's and its dependencies' alike, live under one source root, such as `/repos/src`, with build trees kept outside it, such as `/repos/build` and `/repos/work`.

| Repository | Role |
| --- | --- |
| Laplace-Native | the shared native library, its tools, and its benchmarks |
| Laplace-postgres | the PostgreSQL extension, the content schema, and the query benchmark |
| Laplace-Engine | the engine |
| Laplace-Prototype | the test bench the implementation is checked against |
| Laplace-Wiki | this documentation |
| BLAKE3, PostgreSQL, PostGIS, GEOS, PROJ, GDAL, Eigen, Spectra | dependencies, built from source |

## Toolchain

| Tool | Requirement | Use |
| --- | --- | --- |
| Intel oneAPI: `icx`, `icpx`, MKL, TBB, IPP | 2025 or newer | the primary compilers and libraries |
| gcc | any current | a second compiler, to check that results do not depend on the compiler |
| CMake | 3.24 or newer; 4.x for `icx` 2026 | Laplace builds |
| Meson and Ninja | Meson 0.61 or newer | PostgreSQL's own build system |
| ICU | 78 or newer | Unicode 17 segmentation |
| PostgreSQL | 18 | with liburing, LZ4, zstd, ICU, and OpenSSL |
| PostGIS | 3.6 | |
| liburing | 2.1 or newer | optional; see [Database](Database.md#io) |

Thread counts come from the environment: `OMP_NUM_THREADS` and `MKL_NUM_THREADS` set how many cores MKL and OpenMP kernels use. Some shells and agents set them to 1, which makes every kernel single-threaded. Set them to the number of cores for ingestion and measurement.

An environment file sources oneAPI and points the builds at Eigen, Spectra, BLAKE3, and the custom PostgreSQL. It is sourced for Laplace and PostgreSQL builds only, not for anything built against another PostgreSQL.

Anything that needs root is written as a script that logs its output, so the result can be read afterward.
