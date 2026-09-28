# Prototype

A working prototype of the storage layer was built from the specification and tested against 195 Project Gutenberg texts, and every number on this page was measured on it.

The prototype is a test bench, not Laplace-Engine; its code is at [Laplace-Prototype](https://github.com/SaltyPatron/Laplace-Prototype). It runs on one core of an Intel Core i7-6850K, with no tuning beyond indexes, and its database sat on a USB hard disk, so its times are upper bounds. The real implementation's measurements are in [Engine Measurements](Engine.md).

## What was built

| Part | Built with |
| --- | --- |
| Tier 0 generator | Python and NumPy, from the local Unicode 17.0.0 `allkeys.txt` and UCD |
| Decomposer and ingestion | C, with ICU 78.3 (Unicode 17 segmentation) and BLAKE3 1.8.3 with every SIMD variant and runtime dispatch |
| Store | PostgreSQL 18.6, PostGIS 3.6.4, and a small C extension that decodes entity IDs from geometry ZM vertices and finds continuations |
| Checks and queries | Python, computing IDs and coordinates client-side from tier 0 alone |

## Tier 0

- All 1,114,112 codepoints, each a 64-byte record: BLAKE3-128 ID, fixed-point coordinate, Hilbert value, DUCET rank. The whole table is 68 MiB.
- Order: the DUCET total order described in [Unicode](Unicode.md#the-deterministic-total-order). Placement: H1, described in [Placement](Placement.md).
- Coordinates are integers *m* with value *m* / 2⁵³. Rounding left some computed points a few ULP outside the S³, so 624,971 ULP steps in total moved them inward until every point satisfied *m*·*m* ≤ 2¹⁰⁶ exactly.
- Leaf ID: the first 16 bytes of BLAKE3 over the codepoint's UTF-8 bytes, with surrogates written as 3-byte sequences. Every one of the 1,114,112 IDs is unique.
- Build fingerprint: `1710d2d9899ce403c73513642250b80a0827cf77819fbd79a8ae93c5aae482a5` (SHA-256 of the table).

## Plain-text decomposition

The prototype's one decomposition, for UTF-8 text:

```text
file = [paragraph ...] ; paragraph = [sentence ...] ; sentence = [word segment ...]
word segment = [grapheme | codepoint ...] ; grapheme = [codepoint ...] when it has more than one
```

- Sentence and word boundaries are UAX #29's, from ICU. Plain UAX #29 treats every line break as a paragraph separator, and Gutenberg hard-wraps lines at about 70 characters, so 38% of Alice in Wonderland's "sentences" ended mid-sentence at a line wrap. The prototype gives ICU a copy of the text in which single line breaks inside a paragraph are spaces, and applies the boundaries to the original bytes, so every byte stays in the content. A blank line ends a paragraph.
- A composition's ID is BLAKE3 over its children's 16-byte IDs, repeats included, truncated to 16 bytes. A composition with one child is that child.
- A composition's coordinate is the exact integer average of its children's coordinates, truncated toward zero.
- The physicality path stores each child's ID bit-packed into a vertex's X, Y, and Z mantissas (43 + 43 + 42 bits, exponent −2, so the coordinates lie between 0.25 and 0.5, inside the 4-ball), and a run of identical children as one vertex with the run length in M. An atom's physicality is a POINT ZM holding its own ID.
- Each source records its normalization form (NFC, NFD, both, or mixed) as a filter; content is stored exactly as it arrived. Of the 195 texts, 123 are NFC, 70 are both (plain ASCII and the like), and 2, `galileo.txt` and `odyssey.txt`, are mixed.

## Ingestion

| Measure | Result |
| --- | --- |
| Input | 195 files, 199.4 MB |
| Decompose, hash, deduplicate, and recompose every file | 35.3 s |
| Whole run, including occurrence counts and 6.1 GB of load files | 71.7 s |
| Files recomposed byte for byte | 195 of 195 |
| Children mismatched on an ID match | 0 |

| Tier | Distinct entities | Times reused |
| --- | --- | --- |
| Multi-codepoint graphemes | 15 | 1,162,123 |
| Word segments | 765,412 | 34,634,002 |
| Sentences | 1,678,740 | 432,015 |
| Paragraphs | 356,549 | 19,231 |
| Files | 194 | 0 |

Two of the 195 files, `moby_dick.txt` and `mobydick.txt`, are the same content, so they share one trunk. In total there are 2,800,910 compositions and 82,342,657 path vertices after run-length encoding.

## Store

| Table | Rows |
| --- | --- |
| `entity`: ID, real coordinate (POINT ZM), tier, Hilbert value | 3,915,022 |
| `physicality`: path geometry ZM, keyed to its entity | 3,915,022 |
| `source`: trunk, origin, format, size, content hash | 195 |
| `entity_stats`: containers and occurrences | 2,802,943 |

- Loading took 40 s. Building the keys and indexes took 4 minutes 47 seconds, including converting the tables to logged.
- The database is 4.0 GB: `entity` 951 MB and `physicality` 2.8 GB.
- Indexes:
  - the primary keys and the physicality → entity foreign key;
  - a 4D GiST on the real coordinates (338 MB);
  - a B-tree on the Hilbert value;
  - a GIN on the entity IDs decoded from each path's vertices, which finds containers (450 MB). It indexes the path geometry directly; no array column exists.

## Verification

Run against the database itself:

| Check | Result |
| --- | --- |
| Every entity has exactly one physicality | 3,915,022 = 3,915,022 |
| Entity IDs are unique | 3,915,022 distinct |
| All 1,114,112 codepoints recorded at tier 0 | yes |
| Nothing falls outside the wall, in exact integer arithmetic | 0 of 3,915,022 |
| Pure repeats sit exactly on their constituent's point | 280 of 280 |
| IDs recompute from children alone | 20,000 of 20,000 sampled |
| Tiers only go up | 20,000 of 20,000 sampled |
| Every composition is at least as deep as its constituents' average | 20,000 of 20,000 sampled |
| Alice in Wonderland and Sherlock Holmes recomposed from the database | byte for byte |
| Re-ingesting Alice in Wonderland adds nothing | 5,156 of 5,156 entities already present, same trunk |

## Queries

IDs and coordinates were computed client-side from tier 0; the database was asked only to find and count.

| Query | Result | Time |
| --- | --- | --- |
| Look up "Holmes" and read its stored counts | 527 containers, 574 occurrences | 1.3 ms |
| Look up "Watson", "Laplace", "probability"; a word not stored | found with counts; not found | 0.1–0.2 ms each |
| Every container of "Holmes", through GIN | 527 records | 6.1 ms |
| The run `[Sherlock, ' ', Holmes]` inside containers | 92 sentences | 23 ms |
| Every `[Captain, ' ', ?]` in Moby Dick | Ahab 55, Peleg 27, Bildad 14, Sleet 5, Pollard 3, Mayhew 3, Scoresby 2, Boomer 2, Butler 1, and ordinary words such as "in" and "of" | 206 ms |
| What follows "the capital of" | the 456, a 82, an 15, his 12, one 7, Italy 6, Armenia 3, … | 30 ms, [as geometry](#continuation-as-geometry) |
| The most frequent word segments | the 2,332,304; of 1,648,858; and 950,111; … | 3.9 s |
| The 4D nearest word segments to "king", through GiST | gin, nig, ing, ign, slighting, lights, … | 25 ms |

### Continuation as geometry

A phrase is a trajectory, like every stored path: "the capital of " is the path `[the, ' ', capital, ' ', of, ' ']`. Its continuations are the vertices that follow each window of a container's path matching it, which is a window at Fréchet distance 0. One GIN lookup finds the 3,846 containers holding every constituent (36 ms); they hold 289,623 vertices. Each method found the same 792 continuations, 174 distinct:

| Method | Time |
| --- | --- |
| Decode every candidate sentence into its children in Python and scan for the run | 4,558 ms |
| In SQL, a window at every vertex, each compared to the phrase with `ST_FrechetDistance` | 2,397 ms |
| The same, with windows only where the phrase's rarest constituent sits | 293 ms |
| `laplace_follows`, a C function in the extension: the phrase is encoded once into vertex bytes and compared with the raw stored vertices, 16 bytes per SSE compare, and only continuations are decoded | 30 ms |

With the native function, the index lookup and fetching the containers' rows account for nearly all of the time. `ST_Covers` of the phrase by each path took 6.4 s and matched 3,710 containers, because it compares point sets in 2D rather than ordered windows.

The nearest-neighbor result shows what a centroid carries: with 765,412 distinct word segments in the Latin region, the nearest centroids are words with the same letters in any order. Order is carried by the path, not the centroid.

## Choices the prototype made

The prototype keeps a `tier` column on each entity as a query aid; tier is an observation, never part of an ID. Its plain-text decomposition above, including the line-break tailoring, is the prototype's own; recipes will define decomposition.
