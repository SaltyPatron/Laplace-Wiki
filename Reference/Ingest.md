# Ingest

`laplace ingest` runs one pipeline for every source: enumerate, bind recipes, decompose a batch on every core into the node table, recompose and compare, then load: probe trunks, deduplicate trunk to leaf, COPY new rows into every leaf partition a tier at a time, play the attestations first in first out, write witnesses, ledger, and standings in one transaction, and write the file trunks last.

This page is `ingest.c` and `db.c` phase by phase. Everything shared with the database extension is Laplace-Native's; SQL only fetches and writes.

## 1. Enumerate

Files and directories named on the command line, walked with `nftw`; hidden directories are skipped, hidden and empty files are skipped. A source named is found under the first of its `root`s that exists, or by its `files` patterns. With nothing named, every source in `order`, each in a forked process of its own with the same options, its output in `$LAPLACE_WORK/logs/ingest/<source>.log`, after the room check: the source's files' bytes, `.gz` counted eight times, times its `room` or `LAPLACE_ROOM_FACTOR` 65, must leave the database volume at least a tenth of itself. A source that fails stops the run.

## 2. Bind recipes

`recipes_load` reads every recipe under `$LAPLACE_RECIPES` and `sources_loaded` the sources in `order`. Each file gets the recipe whose `match` fits its name, among its source's recipes when it belongs to one; its trust is the recipe's, or the source's for a format recipe. A recipe that did not load stops its source and no other. Files with no recipe are counted by extension and reported. `--plan` stops here. A source's files are sorted most trusted witness first, equals in the order found.

## 3. Batch and decompose

Files are taken in batches of at most `LAPLACE_BATCH_MB` (1024) MB of input. Each batch is decomposed as OpenMP tasks, one file per task, with one `lp_text` context per thread, into the node table: 256 shards by the ID's first byte, each behind its own lock, a node holding `id`, `m[4]`, its vertex offset and count, its tier, and `keep`. Every composition goes through `compose()`, which finds or adds the node and counts reuse (`hits`). A file too long for one batch whose records can be parted, at a line's end or at a blank line, is read a stretch at a time twice: first for its trunk with nothing recorded, and, if that trunk is not recorded, again to record it; a record longer than a stretch fails the file.

Per recipe: text through `text_ref` (UAX #29); a tree-sitter grammar through the parser and `attest_elements` for XML read as what it says; tables through `attest_fields`, records through `attest_records`, JSON through `attest_members`, lines through `attest_lines`; a vocabulary through `vocabulary_ref`. Each produces the file's trunk and its events: `EV_CLAIM`, a claim that is its own record; `EV_RECORD`, a record; `EV_MEMBER`, a claim within the record before it. Each event carries the claim's ID, the ID of what was witnessed, the score, the entry rating and deviation of its kind, its position, and its own witness when the source names one statement by statement.

Live counters go to stderr: files done, MB, MB/s, nodes.

## 4. Recompose and compare

Every file of the batch that is not curated and not a vocabulary is rebuilt from the node table and tier 0 (`expand`) and compared with its bytes; a mismatch is reported and makes the run exit 1. A curated source is not kept as a file, so it is not compared; a vocabulary is the text its tokens stand for.

Then `file_take` keeps what each file witnessed for its content and `file_close` composes its trunk, `[metadata, content]`.

## 5. Load

`load()` opens one connection per thread with `synchronous_commit = off`, reads which tiers are split from `pg_class`, and checks whether the 1,114,112 atoms are in `entity` at tier 0 (`atoms_needed`: they are written with the first load).

### Trunk to leaf

The files' trunks are probed first: a file whose trunk is recorded is recorded with everything under it and everything it attested, and nothing of it is looked for, played, or written again. Then the frontier: every file's trunk, its witness, its lineage, every claim, every record, every own witness. Each round, `recorded()` asks the database which of the frontier's IDs exist: the IDs are bucketed by their first hex digit, and for each digit one statement, built once from the partitions that hold anything, `SELECT u.i FROM unnest($1::blake3[]) WITH ORDINALITY AS u(id, i) WHERE EXISTS (SELECT 1 FROM entity_t0_a e WHERE e.id = u.id) OR EXISTS (…)` over every partition that can hold an ID with that digit, in chunks of 50,000 on every connection at once. A hit marks the node recorded (`keep = 2`) and nothing below it is checked; a miss marks it new (`keep = 1`) and its children join the next round. Rounds continue until the frontier is empty. `--whole` puts every node in the first frontier instead. Counters: rounds, IDs checked, subtrees already recorded, new nodes.

### COPY

New nodes are bucketed by partition, `part_of(id, tier)`: the tier, 16 and above in the default, and the first hex digit where the tier is split. A tier at a time from the lowest, every partition of that tier on its own connection in parallel: `COPY entity_t… (id, tier, coord, hilbert) FROM STDIN (FORMAT binary)` then `COPY physicality_t… (entity, tier, hilbert, path) FROM STDIN (FORMAT binary)`, the coordinate as a POINT ZM, the Hilbert value top bit flipped, the path from `lp_ewkb_runs`. Lowest tier first so that whatever is recorded has everything under it recorded even if the writing is cut off, which trunk-to-leaf deduplication rests on. The atoms are written into the tier-0 partitions on the first load. File trunks are held back (`keep = 5`).

### Semantics

In one transaction, so that what the files attested and their trunks are recorded together or not at all:

1. Every claim of every event enters the standings map at its stock default: rating 1500 or the recipe's `enter` rating, deviation the recipe's `enter` deviation, else the deviation the witness's trust plays with floored at 30, or 350 at trust 0; volatility 0.06.
2. Claims already recorded get their recorded standing: `SELECT claim, rating, deviation, volatility, matches FROM consensus WHERE claim = ANY($1::blake3[])`, in chunks of 100,000 on every connection.
3. What each lineage witnessed before is read from the ledger: `SELECT a.claim, w.id, w.lineage FROM attestation a JOIN witness w ON w.id = a.witness WHERE a.claim = ANY($1::blake3[])`, into a seen-set keyed by what was witnessed and the lineage.
4. The matchups, first in first out, file by file and event by event: what was witnessed plays once per lineage, a copy being a row in the ledger and nothing more; a record's members play within it; a claim entering for the first time only enters; every later attestation plays `lp_attest(&standing, trust, score, enter_rating, τ = 0.5, floor = 30)` and counts a match.
5. Witnesses not yet in `witness`: `COPY witness (id, lineage, trust)`, including own witnesses named statement by statement, each its own lineage at the source's trust.
6. The ledger, in reading order, its order the order of play: `COPY attestation (claim, witness, score, position)`, one row per record or standalone claim, members within their record.
7. New standings: `COPY consensus (claim, rating, deviation, volatility, matches)`; recorded ones updated set-based, 100,000 at a time: `UPDATE consensus s SET … FROM unnest($1::blake3[], $2::float8[], $3::float8[], $4::float8[], $5::int[]) AS u(c, r, d, v, m) WHERE s.claim = u.c`.
8. The file trunks, last. `COMMIT`.

### After the load

`gin_clean_pending_list` over every GIN index, once, so no lookup pays for the load. The summary on stdout: decomposition (files, MB, recomposed or curated, mismatched), compositions and reused, attestations; phases: decompose, recompose and compare, deduplication (IDs checked, rounds, subtrees recorded), COPY (entities, paths, rows per second), witnesses, ledger, standings (new, updated), the index merge, total.

## The statements

Every statement the ingest issues, all parameters binary, all sets:

| Phase | Statement |
| --- | --- |
| trunk known | `SELECT 1 FROM entity WHERE id = ANY($1::blake3[])` (a long file read in stretches) |
| partitions | `SELECT c.relname FROM pg_class c WHERE c.relkind = 'r' AND c.relname ~ '^entity_t([0-9]+\|x)(_[0-9a-f])?$'`; `SELECT 1 FROM <partition> LIMIT 1` |
| atoms | `SELECT count(*) FROM entity WHERE tier = 0` |
| dedup | the per-digit `EXISTS` chain above |
| COPY | the two `COPY … FROM STDIN (FORMAT binary)` per leaf partition |
| standings | the `consensus` select, `COPY consensus`, the `UPDATE … FROM unnest` |
| lineage | the ledger and witness join above |
| witnesses | `SELECT u.i FROM unnest($1::blake3[]) WITH ORDINALITY AS u(id, i) JOIN witness w ON w.id = u.id`; `SELECT id FROM witness WHERE id = ANY($1::blake3[])`; `COPY witness` |
| ledger | `COPY attestation` |
| end | the `gin_clean_pending_list` aggregate over `pg_index` |

No `ON CONFLICT`, no per-row statement, no cursor, no function call in a predicate.

## Measured

On the reference machine: decompose, hash, deduplicate, and recompose at 8 MB/s on one thread; 2,800,910 IDs deduplicated in 8.2 s; where the bytes differ but the content tree is known, 195 IDs checked in 11 ms and nothing sent; ingesting the 195 Gutenberg texts again, 0.1 s; entity COPY 954,000 rows per second, physicality COPY 215,000 rows per second; 5 million attestations appended at about 245,000 rows per second; standings updated in place at 740,000 to 780,000 attestations per second.
