# Ingest

`laplace ingest` runs one pipeline for every source: enumerate, bind recipes, decompose a batch on every core into the node table, recompose and compare, then load: probe trunks, deduplicate trunk to leaf, COPY new rows into every leaf partition a tier at a time, play the attestations first in first out, write witnesses, attestations, and standings in one transaction, and write the file trunks last.

This page is `ingest.c` and `db.c` phase by phase. Everything shared with the database extension is Laplace-Native's; SQL only fetches and writes.

## 1. Enumerate

Files and directories named on the command line, walked with `nftw`; hidden directories are skipped, hidden and empty files are skipped. A source named is found under the first of its `root`s that exists, or by its `files` patterns. With nothing named, every source in `order`, each in a forked process of its own with the same options, its output in `$LAPLACE_WORK/logs/ingest/<source>.log`, after the room check: the source's files' bytes, `.gz` counted eight times, times its `room` or `LAPLACE_ROOM_FACTOR` 65, must leave the database volume at least a tenth of itself. A source that fails stops the run.

## 2. Bind recipes

`recipes_load` reads every recipe under `$LAPLACE_RECIPES` and `sources_loaded` the sources in `order`. Each file gets the recipe whose `match` fits its name, among its source's recipes when it belongs to one; its trust is the recipe's, or the source's for a format recipe. A recipe that did not load stops its source and no other. Files with no recipe are counted by extension and reported. `--plan` stops here. A source's files are sorted most trusted witness first, equals in the order found.

## 3. Batch and decompose

A source's files are taken most trusted witness first, then by how deep their recipes' `refer` lines go: a file whose recipe refers to another recipe's keys comes after that recipe's files, and a batch never crosses from one depth to the next. Files are taken in batches of at most `LAPLACE_BATCH_MB` (1024) MB of input. A file longer than a batch is read a stretch at a time when its recipe is curated and has no header, no quoted outermost tier and no `split`, and its `refer` lines are not within the file. Each batch is decomposed as OpenMP tasks, one file per task, with one `lp_text` context per thread, into the node table: one lock-free table of open-addressing slots, each a word holding a 24-bit tag of the ID over the node's index, claimed by compare-and-swap and published once its node is written, doubling when half full; the nodes and their vertices in two arrays reserved once and filled a thread's chunk at a time. A node holds `id`, `m[4]`, its vertex offset and count, its tier (the lowest it is composed at), and `keep`. Every composition goes through `compose()`, which finds or adds the node and counts reuse (`hits`), a thread's recent finds answered from its own cache. A batch's files are begun longest first. A file too long for one batch whose records can be parted, at a line's end or at a blank line, is read a stretch at a time twice: first for its trunk with nothing recorded, and, if that trunk is not recorded, again to record it. The first pass ends at the first stretch attesting a claim that is not recorded, since a trunk is written only after every claim of every stretch; each stretch's load writes its parts, which the trunk holds. A record longer than a stretch fails the file.

Per recipe: text through `text_ref` (UAX #29); a tree-sitter grammar through the parser and `attest_elements` for XML read as what it says; tables through `attest_fields`, records through `attest_records`, JSON through `attest_members`, lines through `attest_lines`; a vocabulary through `vocabulary_ref`. Each produces the file's trunk and its events: `EV_CLAIM`, a claim that is its own record; `EV_RECORD`, a record; `EV_MEMBER`, a claim within the record before it. Each event carries the claim's ID, the ID of what was witnessed, the score, the entry rating and deviation of its kind, its position, and its own witness when the source names one statement by statement.

Live counters go to stderr: files done, MB, MB/s, nodes.

## 4. Recompose and compare

Every file of the batch that is not curated and not a vocabulary is rebuilt from the node table and tier 0 (`expand`) and compared with its bytes; a mismatch is reported and makes the run exit 1. A curated source is not kept as a file, so it is not compared; a vocabulary is the text its tokens stand for.

Then `file_take` keeps what each file witnessed for its content and `file_close` composes its trunk, `[metadata, content]`.

## 5. Load

`load()` opens one connection per thread with `synchronous_commit = off`, reads which tiers are split from `pg_class`, and counts the atoms in `entity` at tier 0: none, and all 1,114,112 are written with the first load; fewer than all (a first load cut off between tier 0's sixteen transactions), and each atom's ID is asked through `recorded()` and only the missing ones are written.

### Trunk to leaf

The files' trunks are probed first: a file whose trunk is recorded is recorded with everything under it and everything it attested, and nothing of it is looked for, played, or written again. Then the frontier: every file's trunk, its witness, its lineage, every claim, every record, every own witness. Each round, `recorded()` asks the database which of the frontier's IDs it already has. The client composed every node, so it knows each ID's tier; the tier and the ID's first hex digit name the one partition the ID can be in. The IDs of a partition go to that partition as one set, in ID order, `SELECT u.i FROM unnest($1::blake3[]) WITH ORDINALITY AS u(id, i) WHERE EXISTS (SELECT 1 FROM entity_t2_a e WHERE e.id = u.id)`, in chunks of 500,000 on every connection at once. No statement names more than one partition, and no tier is searched. A hit marks the node recorded (`keep = 2`) and nothing below it is checked; a miss marks it new (`keep = 1`) and its children join the next round. Rounds continue until the frontier is empty. `--whole` puts every node in the first frontier instead. Counters: rounds, IDs checked, subtrees already recorded, new nodes.

### COPY

New nodes are bucketed by partition, `part_of(id, tier)`: the tier, 16 and above in the default, and the first hex digit where the tier is split. A tier at a time from the lowest: each partition's new rows are sorted in Hilbert order and cut into stretches of max(rows / (connections × 4) + 1, 20,000), and every stretch is its own transaction on whichever connection is free, `BEGIN`, `COPY entity_t… (id, tier, coord, hilbert) FROM STDIN (FORMAT binary)`, `COPY physicality_t… (entity, tier, hilbert, path, mask) FROM STDIN (FORMAT binary)`, `COMMIT`. The default partition, every tier past 15, is one transaction, so no node there is committed before what it holds. `mask` is 256 bits: its length as an `int32`, then 32 bytes, bit *b* in byte *b* >> 3 under `0x80 >> (b & 7)`; only the `kind` bank is set.

### Semantics

One transaction in parts, so that what the files attested and their trunks are recorded together or not at all: the parts are min(connections, 16), and part *j* holds the attestations and standings of partitions *j*, *j* + parts, …, part 0 among them; part 0, on the first connection, also holds the witnesses and the trunks. A load begins by finishing what a stopped batch left prepared (only parts prepared more than two minutes ago): committed where its part 0 committed, rolled back where it did not.

1. Every claim of every event enters the standings map at its stock default: rating 1500, and the deviation the witness's trust plays with, floored at 30, or 350 at trust 0 (no recipe line sets another); volatility 0.06.
2. Claims already recorded get their recorded standing: `SELECT claim, rating, deviation, volatility, matches FROM consensus WHERE claim = ANY($1::blake3[])`, in chunks of 100,000 on every connection.
3. What each lineage witnessed before is read per partition: `SELECT a.claim, w.id, w.lineage FROM attestation_<h> a JOIN witness w ON w.id = a.witness WHERE a.claim = ANY($1::blake3[])`, into a seen-set keyed by what was witnessed and the lineage, and a map of what each witness already witnessed.
4. The matchups: which attestations play is decided first, in reading order (what was witnessed plays once per lineage, a copy being a row in `attestation` and nothing more; a record's members play as their record does); then the plays run on every core in 64 sets of claims, each claim's in its reading order. A claim entering for the first time only enters; every later attestation plays `lp_attest(&standing, trust, score, enter_rating, τ = 0.5, floor = 30)` and counts a match.
5. Witnesses not yet in `witness`: `COPY witness (id, lineage, trust)`, including own witnesses named statement by statement, each its own lineage at the source's trust.
6. The attestations, in reading order, its order the order of play: `COPY attestation_h (claim, witness, score, position)` for each of the 16 partitions, each on the connection whose part it is, one row per record or standalone claim, members within their record; a row whose witnessed thing and witness are already in `attestation`, or were already written in this batch, is that witness's observation read again and is not written: each (witnessed, witness) once.
7. New standings: `COPY consensus_h (claim, rating, deviation, volatility, matches)`, on the same connection as the partition's attestations; recorded ones whose matches this batch changed updated set-based, 100,000 at a time: `UPDATE consensus s SET … FROM unnest($1::blake3[], $2::float8[], $3::float8[], $4::float8[], $5::int[]) AS u(c, r, d, v, m) WHERE s.claim = u.c`.
8. The file trunks, last, in part 0. Every part prepared (`PREPARE TRANSACTION 'laplace X j'`, X part 0's transaction), part 0 last; then part 0 committed, which decides, then the rest (`COMMIT PREPARED`).

### After the load

`gin_clean_pending_list` over every GIN index, once, so no lookup pays for the load. The summary on stdout: decomposition (files, MB, recomposed or curated, mismatched), compositions and reused, attestations; phases: decompose, recompose and compare, deduplication (IDs checked, rounds, subtrees recorded), COPY (entities, paths, rows per second), witnesses, attestations, standings (new, updated), the index merge, total.

## The statements

Every statement the ingest issues, all parameters binary, all sets:

| Phase | Statement |
| --- | --- |
| trunk known | `SELECT 1 FROM entity WHERE tier = N AND id = ANY($1::blake3[])`; a long file read in stretches also asks, per partition, whether up to 4,096 of a stretch's claims are all recorded (`db_all_recorded`) |
| session | `SET synchronous_commit = off` on every connection |
| partitions | `SELECT c.relname FROM pg_class c WHERE c.relkind = 'r' AND c.relname ~ '^entity_t([0-9]+\|x)_[0-9a-f]$'`: which tiers are split |
| a stopped batch | `SELECT gid, … FROM pg_prepared_xacts WHERE gid LIKE 'laplace %' AND … prepared < now() - interval '2 minutes'`; `COMMIT PREPARED` or `ROLLBACK PREPARED` each |
| atoms | `SELECT count(*) FROM entity WHERE tier = 0` |
| dedup | the per-digit `EXISTS` chain above |
| COPY | per stretch: `BEGIN`, the two `COPY … FROM STDIN (FORMAT binary)`, `COMMIT` |
| the batch's transaction | `BEGIN` on every part, `SELECT pg_current_xact_id()` on part 0, `PREPARE TRANSACTION 'laplace X j'` per part, `COMMIT PREPARED` |
| standings | per partition of the claim's first hex digit: `SELECT claim, rating, deviation, volatility, matches FROM consensus_<h> WHERE claim = ANY($1::blake3[])`, `COPY consensus_<h> … FROM STDIN (FORMAT binary)`, `UPDATE consensus_<h> s SET … FROM unnest($1::blake3[], $2::float8[], $3::float8[], $4::float8[], $5::int[]) AS u(c, r, d, v, m) WHERE s.claim = u.c`; the matchups themselves are played in the engine, native, before the one update |
| attestation | per partition: `COPY attestation_<h> (claim, witness, score, position) FROM STDIN (FORMAT binary)` |
| lineage | the attestation and witness join above |
| witnesses | `SELECT u.i FROM unnest($1::blake3[]) WITH ORDINALITY AS u(id, i) JOIN witness w ON w.id = u.id`; `SELECT id FROM witness WHERE id = ANY($1::blake3[])`; `COPY witness` |
| end | the `gin_clean_pending_list` aggregate over `pg_index` |

No `ON CONFLICT`, no per-row statement, no cursor, no function call in a predicate.

## Measured

On the reference machine: decompose, hash, deduplicate, and recompose at 8 MB/s on one thread; 2,800,910 IDs deduplicated in 8.2 s; where the bytes differ but the content tree is known, 195 IDs checked in 11 ms and nothing sent; ingesting the 195 Gutenberg texts again, 0.1 s; entity COPY 954,000 rows per second, physicality COPY 215,000 rows per second; 5 million attestations appended at about 245,000 rows per second; standings updated in place at 740,000 to 780,000 attestations per second.
