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

Threading matters as much as SIMD. The same kernel run over TinyLlama's vocabulary took 110.8 s on one thread and 19.9 s on twelve (37 against 213 GFLOP/s). The environment it first ran in had set `OMP_NUM_THREADS` and `MKL_NUM_THREADS` to 1.

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

### Vocabularies

Every tokenizer in a farm of 33 models was ingested as content: each token decomposed like any text, each byte token written as its notation (`<0xAB>`), and each vocabulary recorded as the path of its tokens in index order.

- 24 tokenizer files and 2,700,090 tokens deduplicated to 240,450 compositions in 5.1 s, and loaded in 19.5 s.
- The 24 files held 11 distinct vocabularies. Files with the same token list became the same trunk, and vocabularies that share their tokens but add or order some differently stayed distinct, like Qwen2.5's and Qwen3's.
- 50,149 of the tokens were already recorded, as words of the Gutenberg texts.

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

## Storage at volume

Tatoeba's 13.56 million sentences in 424 languages (605 MB of text) were ingested in four equal chunks after the Gutenberg texts:

| Chunk | Input | Database growth | Ratio |
| --- | --- | --- | --- |
| 1 | 151 MB | 4,928 MB | 32.6× |
| 2 | 151 MB | 4,579 MB | 30.3× |
| 3 | 151 MB | 4,047 MB | 26.8× |
| 4 | 151 MB | 4,534 MB | 30.0× |

By the fourth chunk, 74% of word segments were already recorded, but 99% of sentences were new: Tatoeba's sentences are short and almost never repeat. Per sentence, averaging 16.6 vertices in its path, storage came to about 1,117 bytes:

| Part | Bytes per sentence |
| --- | --- |
| Path (physicality heap) | 599 |
| Entity row | 101 |
| 4D GiST index | 82 |
| GIN container index | 76 |
| Statistics row and its indexes | 139 |
| ID indexes (entity and physicality) | 91 |
| Hilbert index | 29 |

The same 1.68 million Gutenberg sentence paths stored as `uuid[]` with run lengths took 1,310 MB, against 1,785 MB as geometry ZM, with the same GIN size and the same query times: containers 0.28 against 0.32 ms, continuations 25.1 against 25.3 ms, and every container of the hub `the` (864,949) 309 against 376 ms.

## Consensus writes

Five million attestations, Zipf-distributed over a million claims so that a few hub claims receive most of them, were written in batches of 100,000:

- The ledger appended at about 245,000 rows per second, taking 301 MB with its index.
- Standings updated in place by one set-based statement per batch absorbed 740,000–780,000 attestations per second, because a batch's repeated hits on a claim collapse (100,000 attestations touched about 19,500 claims). The standing table stayed at 66 MB with dead rows levelling off near 34,000 under a fill factor of 80.
- Reading the hottest claim's standing took 0.1 ms. Aggregating its 474,628 ledger rows instead took 115 ms.

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

`laplace_text` recomposes any entity by walking its paths down to tier 0: twenty words in 13 ms, and all of Alice in Wonderland in 828 ms, byte for byte (the same MD5 as the file).

The same queries on the prototype, whose database sat on a USB hard disk, took 0.2 ms, 6.1 ms, 23 ms, 206 ms, 3.8 s, and 25 ms, respectively. Queries that start from an ID prune to one partition. Queries that search for containers, or search by position, visit every partition's index.
