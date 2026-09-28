# Engine Measurements

The first shared components of the real implementation, Laplace-Native and Laplace-postgres, were measured on a tuned PostgreSQL server with the Gutenberg corpus, and every number on this page comes from their benchmarks.

## Setup

- Intel Core i7-6850K (AVX2, FMA, BMI2; no AVX-512), 125 GB RAM.
- PostgreSQL 18.6 and PostGIS 3.6.4, built with Intel oneAPI `icx`:
  - storage: heap on NVMe, WAL and temporary files on SATA SSDs;
  - memory: 31 GB of shared buffers on huge pages;
  - `pg_stat_statements` on.
- Laplace-Native and Laplace-postgres were built with `icx` and deterministic floating-point flags. Every SIMD level is compiled in and chosen at run time.
- The code is at [Laplace-Native](https://github.com/SaltyPatron/Laplace-Native) and [Laplace-postgres](https://github.com/SaltyPatron/Laplace-postgres).

## Native operations

One core, from `laplace-bench`:

| Operation | Rate |
| --- | --- |
| Wall check, exact 128-bit | 296 M/s |
| Exact centroid | 211 M points/s |
| ID into and out of the X/Y/Z mantissas | 104 M/s |
| 4D Hilbert value | 12 M/s (83 ns) |
| Codepoint ID, BLAKE3-128 | 8–12 M/s |
| Glicko-2 matchup | 7.8 M/s |
| Vertex scan for continuations | 14.2 GB/s scalar, 15.0 GB/s AVX2 |
| 4D squared distances | 1.1 G/s scalar, 1.4 G/s AVX2 |
| Discrete Fréchet, 1,000 × 1,000 vertices | 3.8 ms |

- The vertex scan runs at one core's memory bandwidth, so SIMD barely changes it.
- The Hilbert value fell from 227 ns to 83 ns once branches became masks and the bit interleave became `pdep`.

Both compilers, `icx` and `gcc`, reproduce the prototype's tier-0 IDs and Hilbert values bit for bit.

## Ingestion

`laplace-ingest` took the 195 Gutenberg texts (209 MB) into the database by binary COPY, in 60 s.

| Phase | Time | Notes |
| --- | --- | --- |
| Decompose, hash, deduplicate, recompose | 26.6 s | one thread, 8 MB/s; 195 of 195 files recomposed byte for byte |
| Occurrences and distinct parents | 0.7 s | 47.5 s before counting became linear |
| Deduplication against the database | 8.2 s | 2,800,910 IDs, trunk to leaf, one set-based query per tier per round |
| `entity` COPY | 4.1 s | 954,000 rows/s |
| `physicality` COPY | 18.2 s | 215,000 rows/s, 2.9 GB |

Ingesting the same files again took 0.1 s: one query over the files' BLAKE3-256 hashes found all 195 recorded, and nothing was decomposed. Where the bytes differ but the content tree is known, the trunk-to-leaf check stops at the first tier: 195 IDs checked in 11 ms, and nothing sent.

## Server settings

| Setting | Measured | Chosen |
| --- | --- | --- |
| `io_method` | io_uring on Linux 5.15 failed 1 of 12 cold parallel index builds ("could not read blocks: Operation canceled"). `worker` failed none and ran 5–10% faster. | `worker` |
| Statistics on path geometry | `ANALYZE` of the paths took 332 s: PostGIS built 4D histograms over packed IDs. | none; `ANALYZE` takes 2.5 s |
| Cost of the GIN key function | At low costs the planner scanned the partition of whole books and decoded every book on every lookup: 90 ms of a 111 ms query. | 10,000 |
| Parallel workers for container lookups | Starting workers took about 15 ms, against a lookup that takes 1 ms. | no parallel scans of paths, no parallel append |

PostgreSQL and PostGIS assume geometry coordinates are positions and index functions are cheap. Laplace's paths hold packed IDs, and its index key decodes a whole trajectory, so the defaults misjudge both.

## Partitions

- **Hilbert ranges failed.** With word segments and sentences each split into 8 equal Hilbert ranges of the 4-cube, all 765,412 word segments and all 1,678,740 sentences landed in the first range. English text lies in one small region of the 4-ball, and Hilbert ranges divide the 4-cube around it.
- **ID prefixes worked.** Split by the first hex digit of their ID, the word segments fell 47,628 to 47,964 per partition. An ID is a BLAKE3 hash, so any content divides evenly, and a lookup by ID prunes to one partition.

## Queries

Warm execution time, and the number of partitions each plan touched:

| Query | Result | Time | Partitions |
| --- | --- | --- | --- |
| A word by computed ID and tier | 527 containers, 574 occurrences | 0.02 ms | 1 |
| A word by computed ID alone | the same | 0.08 ms | 14 |
| A word never recorded | not found | 0.01 ms | 1 |
| Every container of `Holmes` | 527 | 0.80 ms | 52 |
| The run `Sherlock Holmes` | 92 | 1.76 ms | 52 |
| What fills `[Captain, ' ', ?]` | Ahab 105, Peleg 52, Bildad 27, … | 9.2 ms | 52 |
| What follows "the capital of " | the 456, a 82, an 15, his 12, … | 24.7 ms | 52 |
| The 16 word segments nearest `king` in 4D | king, then its anagrams | 7.7 ms | 16 |
| The 20 most frequent word segments | the, of, and, to, in, … | 0.15 ms | 16 |

The same queries on the prototype, whose database sat on a USB hard disk, took 0.2 ms, 6.1 ms, 23 ms, 206 ms, 3.8 s, and 25 ms, respectively. Queries that start from an ID prune to one partition. Queries that search for containers, or search by position, visit every partition's index.
