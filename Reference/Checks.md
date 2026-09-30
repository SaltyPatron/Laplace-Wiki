# Checks

Every check that proves the built machine: the native golden tests, the prototype's verification of a loaded database, the engine's own checks during ingest, the fingerprint comparison of `laplace status`, the operation benchmark, and the query benchmark.

## The native tests

`ctest` in Laplace-Native, each executable against the tier 0 at `LAPLACE_TIER0`, both compilers:

| Test | Checks |
| --- | --- |
| `identity` | every codepoint's ID equals tier 0's; no duplicate codepoint IDs; `A` is `32684bfa28c0c84d6f210511aace0efc`; `Holmes` is `5b7e40e9a23ae55eaccd45646934977d` and equals the composition of its codepoints; one-child collapse; invalid UTF-8 rejected |
| `coord` | no tier-0 point outside the wall; every tier-0 Hilbert value recomputes; truncation toward zero; no overflow in the sum; the wall exact at its edge |
| `geometry` | every ID round-trips through the mantissas; every packed value in `[0.25, 0.5)`; a three-run path is `9 + 32·3` bytes with three vertices and run lengths 3, 1, 1; a pure repeat is one POINT ZM of 37 bytes with the run in M and type `0xC0000001` |
| `follows` | over random paths and phrases, the continuations found equal the expected, count and content; run at `LAPLACE_ISA=scalar`, `sse2`, `avx2` |
| `consensus` | Glickman's example gives `1464.06 / 151.52 / 0.05999`; trust 1 plays at deviation 0, 0.9 at 152.6, 0.669 at 350, 0 carries no information; negative trust equals flipping the outcome; trust 0 changes nothing; a win raises; low trust moves less |
| `shape` | identical sequences: Fréchet 0, DTW 0 over N steps, EDR 0; a stray vertex sets Fréchet above 4, skipping it gives 0, one EDR edit, DTW adds its distance once; a repeat is nothing to Fréchet and DTW and one EDR edit; `outliers 0` equals Fréchet |
| `pull` | 5,000 entities reached; a dearer chain is not kept, a cheaper one is; the cheapest comes first; a closed entity stays closed; entities come out in cost order, every one once |
| `flags` | `A` is `Uppercase_Letter`, `a` `Lowercase_Letter`; scripts Latin, Greek, Han; alef `Right_To_Left`; `Alphabetic`, `White_Space`, `Emoji`; `U+10FFFF` `Unassigned`, `U+D800` `Surrogate`; values by short and long name |
| `text` | `[H,o,l,m,e,s]` a tier-2 word of 6 parts; `Sherlock Holmes` tier 3 of 3 parts in order, the space a codepoint, its coordinate the average and inside the wall; one codepoint is that codepoint; an ID that is no codepoint |
| `confidence` (in `consensus`) | 1774.3 / 93.3 reads 0.624 at *k* = 2 and 0.829 at *k* = 0; cost 0.472; copies counted once, 1.986 |

## The prototype's verification

`Laplace-Prototype/tests/verify.py` against a loaded database, recomputing everything from `tier0.bin` and the rows, printing PASS or FAIL per check:

1. every entity has exactly one physicality: the counts match;
2. entity IDs are unique;
3. all 1,114,112 codepoints are recorded at tier 0;
4. nothing falls outside the wall, `Σ m² ≤ 2^106` in exact integer arithmetic over every entity;
5. pure repeats `[n, n, …]` sit exactly on n's point, for repeats of codepoints and of compositions;
6. IDs recompute from children alone, repeats included, on a random sample of 20,000;
7. tiers only go up: every child below its parent;
8. the depth law: each composition at least as deep as its constituents' average, exactly, in 80-digit decimal;
9. Alice and Sherlock recomposed from the database byte for byte, the same BLAKE3 as the file;
10. re-ingesting Alice finds the same trunk and adds nothing new.

The prototype passed every one on 3,915,022 entities. The checks that read the prototype's `source` table are the two the built schema cannot run as written; the engine's own recompose check covers them.

## The engine's checks

- **During ingest**: every non-curated file recomposed from the node table and compared with its bytes, a mismatch exiting 1; a part not read whole reported and exiting 1; `nodes` reported against `reused`; a recipe that does not load stopping its source.
- **`laplace status`**: the database's `laplace_fingerprint()` against this engine's `lp_tier0_fingerprint`, reporting the same or **DIFFERS**; the counts by tier; the semantics counts; the indexes present.
- **`laplace deploy`**: every statement's success, and `laplace status` after.
- **`laplace ingest --no-load`**: the whole decomposition and the recompose check without writing.

## The operation benchmark

`laplace bench`, one line per operation; the reference machine's values, one core:

| Operation | Reference |
| --- | --- |
| wall check | 296 M/s |
| exact centroid | 211 M points/s |
| ID into and out of the mantissas | 104 M/s |
| 4D Hilbert value | 12 M/s, 83 ns |
| codepoint ID | 8 to 12 M/s |
| Glicko-2 matchup | 7.8 M/s |
| vertex scan | 14.2 GB/s scalar, 15.0 GB/s AVX2 |
| 4D squared distances | 1.1 G/s scalar, 1.4 G/s AVX2 |
| discrete Fréchet 1,000 × 1,000 | 3.8 ms |

## The query benchmark

`Laplace-postgres/bench/bench_queries.py [conninfo] [warm_runs] [setting=value …]`: ten queries, each once cold with PostgreSQL's buffers evicted and then `warm_runs` times, reporting the server's execution time from `EXPLAIN (ANALYZE, BUFFERS)`, the client round trip, buffers read and hit, the partitions the plan touched, and the first rows. The queries compute their IDs and coordinates in place with the `IMMUTABLE` functions, so the database is only asked to find and count:

| Query | Reference, warm | Partitions |
| --- | --- | --- |
| a word by computed ID, every partition | 0.08 ms | 14 |
| a word by computed ID and tier | 0.02 ms | 1 |
| `Sherlock Holmes` by the ID of its own tree | | 1 |
| a word never recorded | 0.01 ms | 1 |
| every container of `Holmes`, GIN | 0.80 ms | 52 |
| the run `Sherlock Holmes` inside containers | 1.76 ms | 52 |
| what follows "the capital of " | 24.7 ms | 52 |
| what fills `[Captain, ' ', ?]` | 9.2 ms | 52 |
| the 16 word segments nearest `king` in 4D, GiST | 7.7 ms | 16 |
| everything attested about `dog` with its confidence | | |

The tenth query joins a table named `standing`; the built schema names it `consensus`, so the benchmark's last query needs that name corrected before it runs.

## What is not checked anywhere yet

No test covers the engine's `load()` beyond its own recompose check and `laplace status`; the prototype's verification is the closest, against the prototype's schema. No check covers `forget` and `sweep` beyond `--dry`. No check exists for the four extension functions declared without a definition, which fail at `CREATE EXTENSION`.
