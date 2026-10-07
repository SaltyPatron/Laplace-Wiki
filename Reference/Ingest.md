# Ingest

`laplace ingest` runs one pipeline for every source: enumerate, bind recipes, decompose a batch on every core into the node table, recompose and compare, then load: probe trunks, deduplicate trunk to leaf, COPY new rows into every leaf partition a tier at a time, write the file trunks last; then, the whole source in, play its series once each (a claim's records under the source, folded over every batch) and stage the standings, write the source's trunk, merge, and record the trunk as the witness.

This page is `ingest.c` and `db.c` phase by phase. Everything shared with the database extension is Laplace-Native's; SQL only fetches and writes.

## 1. Enumerate

Files and directories named on the command line, walked with `nftw`; hidden directories are skipped, hidden and empty files are skipped. A source named is found under the first of its `root`s that exists, or by its `files` patterns. With nothing named, every source in `order`; with sources named, those and every source they come `after`, in `order`; each in a forked process of its own with the same options (`LAPLACE_INGEST_ONE` set, so it takes its source alone), its output in `$LAPLACE_WORK/logs/ingest/<source>.log`, after the room check: the source's files' bytes, `.gz` counted eight times, times its `room` or `LAPLACE_ROOM_FACTOR` 65, must leave the database volume at least a tenth of itself. A source that fails stops the run; a source that comes after one that did not go in, absent or short of room, is not begun.

## 2. Bind recipes

`recipes_load` reads every recipe under `$LAPLACE_RECIPES` and `sources_loaded` the sources in `order`. Each file gets the recipe whose `match` fits its name, among its source's recipes when it belongs to one; its trust is the recipe's, or the source's for a format recipe. A recipe that did not load stops its source and no other. Files with no recipe are counted by extension and reported. `--plan` stops here. A source's files are sorted most trusted witness first, equals in the order found.

## 3. Batch and decompose

A source's files are taken most trusted witness first, then by how deep their recipes' `refer` lines go: a file whose recipe refers to another recipe's keys comes after that recipe's files, and a batch never crosses from one depth to the next. Files are taken in batches of at most `LAPLACE_BATCH_MB` (1024) MB of input. A file longer than a batch is read a stretch at a time when its recipe is curated and has no header, no quoted outermost tier and no `split`, and its `refer` lines are not within the file. Each batch is decomposed as OpenMP tasks, one file per task, with one `lp_text` context per thread, into the node table: one lock-free table of open-addressing slots, each a word holding a 24-bit tag of the ID over the node's index, claimed by compare-and-swap and published once its node is written, doubling when half full; the nodes and their vertices in two arrays reserved once and filled a thread's chunk at a time. A node holds `id`, `m[4]`, its vertex offset and count, its tier (the lowest it is composed at), and `keep`. Every composition goes through `compose()`, which finds or adds the node and counts reuse (`hits`), a thread's recent finds answered from its own cache. A batch's files are begun longest first. A file too long for one batch whose records can be parted, at a line's end or at a blank line, is read a stretch at a time twice: first for its trunk with nothing recorded, and, if that trunk is not recorded, again to record it. The first pass ends at the first stretch attesting a claim that is not recorded, since a trunk is written only after every claim of every stretch; each stretch's load writes its parts, which the trunk holds. A record longer than a stretch fails the file.

Per recipe: text through `text_ref` (UAX #29); a tree-sitter grammar through the parser and `attest_elements` for XML read as what it says; tables through `attest_fields`, records through `attest_records`, JSON through `attest_members`, lines through `attest_lines`; a vocabulary through `vocabulary_ref`. Each produces the file's trunk and its events: `EV_CLAIM`, a claim that is its own record; `EV_RECORD`, a record; `EV_MEMBER`, a claim within the record before it. Each event carries the claim's ID, the ID of what was witnessed, the score, the entry rating and deviation of its kind, its position, and its own witness when the source names one statement by statement.

Live counters go to stderr: files done, MB, MB/s, nodes.

## 4. Recompose and compare

Every file of the batch that is not curated and not a vocabulary is rebuilt from the node table and tier 0 (`expand`) and compared with its bytes; a mismatch is reported and makes the run exit 1. A curated source is not kept as a file, so it is not compared; a vocabulary is the text its tokens stand for.

Then `file_take` keeps what each file witnessed for its content and `file_close` composes its trunk, `[metadata, content]`, its metadata tree the OS's record of it as its recipes dispose of it (`file_record`, [Recipes](Recipes.md#how-a-file-is-recorded)).

## 5. Load

`load()` opens one connection per thread with `synchronous_commit = off`, reads which tiers are split from `pg_class`, and counts the atoms in `entity` at tier 0: none, and all 1,114,112 are written with the first load; fewer than all (a first load cut off between tier 0's sixteen transactions), and each atom's ID is asked through `recorded()` and only the missing ones are written.

### Trunk to leaf

The files' trunks are probed first: a file whose trunk is recorded is recorded with everything under it and everything it attested, and nothing of it is looked for, played, or written again. Then the frontier: every file's trunk, its witness, its lineage, every claim, every record, every own witness. Each round, `recorded()` asks the database which of the frontier's IDs it already has. The client composed every node, so it knows each ID's tier; the tier and the ID's first hex digit name the one partition the ID can be in. The IDs of a partition go to that partition as one set, in ID order, `SELECT u.i FROM unnest($1::blake3[]) WITH ORDINALITY AS u(id, i) WHERE EXISTS (SELECT 1 FROM entity_t2_a e WHERE e.id = u.id)`, in chunks of 500,000 on every connection at once. No statement names more than one partition, and no tier is searched. A hit marks the node recorded (`keep = 2`) and nothing below it is checked; a miss marks it new (`keep = 1`) and its children join the next round. Rounds continue until the frontier is empty. `--whole` puts every node in the first frontier instead. Counters: rounds, IDs checked, subtrees already recorded, new nodes.

### COPY

New nodes are bucketed by partition, `part_of(id, tier)`: the tier, 16 and above in the default, and the first hex digit where the tier is split. A tier at a time from the lowest: each partition's new rows are sorted in Hilbert order and cut into stretches of max(rows / (connections × 4) + 1, 20,000), and every stretch is its own transaction on whichever connection is free, `BEGIN`, `COPY entity_t… (id, tier, coord, hilbert) FROM STDIN (FORMAT binary)`, `COPY physicality_t… (entity, tier, hilbert, path, mask) FROM STDIN (FORMAT binary)`, `COMMIT`. The default partition, every tier past 15, is one transaction, so no node there is committed before what it holds. `mask` is 256 bits: its length as an `int32`, then 32 bytes, bit *b* in byte *b* >> 3 under `0x80 >> (b & 7)`; only the `kind` bank is set.

### Records and the series

What a source says is held by containment ([Attestations: Witnesses](../Semantics/Attestations.md#witnesses)): there is no table of attestations. Every part a recipe speaks of whole is a record, composed where it is read (`say.c`, `records_of`), a path in its file's content tree:

- the part's thing first (the sentence, the row), its rows' layers and tree where the recipe gives them (`layers`, `tree`), then each claim it says, in the order said, a vertex said to be a claim (`LP_SAID_CLAIM`) whose run is how many times the record says it, and whose M says how: the outcome (a win; a draw; a loss; or a score, carried in the vertex's spare bits) and its position among the claims said together (`together`), [Physicality](../Storage/Physicality.md#physicality);
- who in the record says a claim (a column of annotators, a speaker: `voices`, `by`, `voice`), a vertex said to be a voice (`LP_SAID_VOICE`) right before the claim: content of the record, never a witness;
- a record that is one claim said once is that claim, standing in the content tree as its own record (`LP_SAID_RECORD`); each part of a part wide enough to be read on every core is a record of its own;
- the blocks of a file's content that hold records are said to (`LP_SAID_HOLDS`), and so is a file's content, so a walk down from a trunk passes over content that says nothing.

A record composed again under the same ID whose claims were said otherwise (another outcome or place) is counted and said; the first is kept. A claim no reference could be made of is counted and said.

The series: before each batch is loaded, the files whose trunks are recorded are found (`files_known`; they say nothing again), and what the rest say is folded into one map for the whole source, a claim's games (its records) and the sum of their scores, as their vertices carry them. When every batch is in, the series are played once each (`standings_write`): every claim's recorded or staged standing read (`SELECT claim, rating, deviation, volatility, matches FROM {public,stage}.consensus_<h> WHERE claim = ANY($1::blake3[])`), `lp_attest_series(&standing, trust, games, score / games, LP_ATTEST_FLOOR)` on every core, `matches` plus the games, and the standings staged per partition (`DELETE FROM stage.consensus_<h> WHERE claim = ANY(…)`, `COPY stage.consensus_<h> …`), one transaction a connection. The trust is the source's: its trunk is the witness, and a recipe naming a class or lineage of its own under the source is said and not used.

### After the load

When every file was of one source, its trunk, `[record, its files' trunks]`, composed in an emptied node table and written by a load of its own, so it is recorded only after every file is; then merge; then the trunk is the witness, its row in `witness` written unless it is there, its trust and lineage the source's. A part of a source (`-s`), or files of several sources, have no trunk: what they say is held by their files' trunks, and no witness holds them. The summary on stdout: decomposition (files, MB, recomposed or curated, mismatched), compositions and reused, the claims said by records; phases: decompose, recompose and compare, deduplication (IDs checked, rounds, subtrees recorded), COPY (entities, paths, rows per second), the series played once each (claims, standings new and updated: read, played, staged), the source's trunk and its ID, merge, the witness, total.

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
| standings | once a source, per partition of the claim's first hex digit: `SELECT claim, rating, deviation, volatility, matches FROM {public,stage}.consensus_<h> WHERE claim = ANY($1::blake3[])`, `DELETE FROM stage.consensus_<h> WHERE claim = ANY($1::blake3[])`, `COPY stage.consensus_<h> … FROM STDIN (FORMAT binary)`; the series are played in the engine, native, before the one write |
| the witness | `INSERT INTO witness (id, lineage, trust) SELECT … WHERE NOT EXISTS (SELECT 1 FROM witness WHERE id = …)`: the source's trunk, after merge |
| end | the GIN indexes from `pg_index`, largest first; `SELECT gin_clean_pending_list($1::regclass)` for each, on every connection at once |

No `ON CONFLICT`, no per-row statement, no cursor, no function call in a predicate.

## Measured

On the reference machine: decompose, hash, deduplicate, and recompose at 8 MB/s on one thread; 2,800,910 IDs deduplicated in 8.2 s; where the bytes differ but the content tree is known, 195 IDs checked in 11 ms and nothing sent; ingesting the 195 Gutenberg texts again, 0.1 s; entity COPY 954,000 rows per second, physicality COPY 215,000 rows per second; 5 million attestations appended at about 245,000 rows per second; standings updated in place at 740,000 to 780,000 attestations per second.
