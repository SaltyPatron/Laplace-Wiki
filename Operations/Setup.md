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
| Write-ahead log | an SSD apart from the heap | sequential writes that do not compete with reads |
| PostgreSQL temporary files | an SSD apart from the heap (here the log's), as the tablespace `pgtemp` | sorts and index builds that spill |
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
| Laplace-Operations | the machine, the build, the deployment, the repair and the agents: `laplace.env`, `setup.sh`, `build.sh`, `deploy.sh`, `ingest.sh`, `agents.sh`, and the workflows `laplace.yml` and `ingest.yml` |
| Laplace-Prototype | the test bench the implementation is checked against |
| Laplace-Wiki | this documentation |
| GEOS, PROJ, GDAL, Spectra (headers), PostgreSQL, PostGIS, BLAKE3, CORE-MATH, tree-sitter | dependencies, built from source by `setup.sh` (`deps`); Eigen is the distribution's `libeigen3-dev`, and ICU 78 is unpacked by hand into `$LAPLACE_ICU_DIR` |

## Toolchain

| Tool | Requirement | Use |
| --- | --- | --- |
| Intel oneAPI: `icx`, `icpx`, MKL, TBB, IPP | 2025 or newer, installed by hand; `setup.sh` reports it missing | the primary compilers and libraries |
| gcc | any current | a second compiler, to check that results do not depend on the compiler |
| CMake | 3.24 or newer; 4.x for `icx` 2026; `setup.sh` installs Kitware's release under `$LAPLACE_PREFIX` when the distribution's is older | Laplace builds |
| Ninja | any current | Laplace's builds; PostgreSQL is built with its `configure` |
| ICU | 78 or newer | Unicode 17 segmentation |
| PostgreSQL | 18 | with liburing, LZ4, zstd, ICU, and OpenSSL |
| PostGIS | its `master` branch, as `setup.sh` clones it | |
| liburing | 2.1 or newer | PostgreSQL is always built with it; see [Database](Database.md#io) |

Thread counts come from the environment: `OMP_NUM_THREADS` and `MKL_NUM_THREADS` set how many cores MKL and OpenMP kernels use. Some shells and agents set them to 1, which makes every kernel single-threaded. Set them to the number of cores for ingestion and measurement.

`laplace.env` in Laplace-Operations is the one environment: every script sources it, and it sources oneAPI once, sets `PG_CONFIG`, the paths of BLAKE3, CORE-MATH and tree-sitter, and `PATH`.

Only `setup.sh` and `agents.sh` need root, and a person runs them; what they did is logged under `$LAPLACE_WORK/logs/root`. No runner has root or a sudo rule. `setup.sh` is parts, each comparing its declaration with the machine and making only what is missing: `volumes`, `packages`, `rights`, `kernel`, `deps`, `cluster`, `settings`, `access`, `report`; `drop`, never part of `all`, empties the cluster's directories when `LAPLACE_DROP` names the data directory and no ingest is running.
