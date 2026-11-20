# Ingest

`laplace ingest` runs one pipeline for every source: enumerate, bind recipes, decompose a batch on every core into the node table, recompose and compare, then load: probe trunks, deduplicate trunk to leaf, COPY new rows into every leaf partition a tier at a time, write the file trunks last; then, the whole source in, play its series once each (a claim's records under the source, folded over every batch) and stage the standings, write the source's trunk, merge, and record the trunk as the witness.

This page is `ingest.c` and `db.c` phase by phase. Everything shared with the database extension is Laplace-Native's; SQL only fetches and writes.

## 1. Enumerate

Files and directories named on the command line, walked with `nftw`; hidden directories are skipped, hidden and empty files are skipped. A source named is found under the first of its `root`s that exists, or by its `files` patterns. With nothing named, every source in `order`; with sources named, those and every source they come `after`, in `order`; each in a forked process of its own with the same options (`LAPLACE_INGEST_ONE` set, so it takes its source alone), its output in `$LAPLACE_WORK/logs/ingest/<source>.log`, after the room check: the source's files' bytes, `.gz` counted eight times, times its `room` or `LAPLACE_ROOM_FACTOR` 65, must leave the database volume at least a tenth of itself. A source that fails stops the run; a source that comes after one that did not go in, absent or short of room, is not begun.

## 2. Bind recipes

`recipes_load` reads every recipe under `$LAPLACE_RECIPES` and `sources_loaded` the sources in `order`. Each file gets the recipe whose `match` fits its name, among its source's recipes when it belongs to one; its trust is the recipe's, or the source's for a format recipe. A recipe that did not load stops its source and no other. Files with no recipe are counted by extension and reported. `--plan` stops here. A source's files are sorted most trusted witness first, equals in the order found.

## 3. Batch and decompose

A source's files are taken most trusted witness first, then by how deep their recipes' `refer` lines go: a file whose recipe refers to another recipe's keys comes after that recipe's files, and a batch never crosses from one depth to the next. Files are taken in batches of at most `LAPLACE_BATCH_MB` (1024) MB of input. Before reading or decomposing a file's bytes, its OS metadata / file trunk is probed in $O(1)$ against the database (`files_known`). A file longer than a single batch is streamed in a **single pass** sectioned strictly on top-level grammar/record boundaries (XML element, Turtle statement block, JSONL object, CoNLL-U sentence block, PGN game, TSV row)—never split at arbitrary byte offsets and never read or decomposed twice (`read_file_twice` is retired). Each batch or grammar-bounded section is decomposed as OpenMP tasks, one file/section per task, with one `lp_text` context per thread, bottom-up (**leaf to trunk**) from the mmap'd `tier0.bin` and `highway.bin` perf-caches into the node table: one lock-free table of open-addressing slots, each a word holding a 24-bit tag of the ID over the node's index, claimed by compare-and-swap and published once its node is written, doubling when half full; the nodes and their vertices in two arrays reserved once and filled a thread's chunk at a time. A node holds `id`, `m[4]`, its vertex offset and count, its tier (the lowest it is composed at), and `keep`. Every composition goes through `compose()`, which finds or adds the node and counts reuse (`hits`), a thread's recent finds answered from its own cache and persistent `staged_set`. A batch's files are begun longest first.

Per recipe: text through `text_ref` (UAX #29); a tree-sitter grammar through the parser and `attest_elements` for XML read as what it says; tables through `attest_fields`, records through `attest_records`, JSON through `attest_members`, lines through `attest_lines`; a vocabulary through `vocabulary_ref`. Each produces the file's trunk and its events: `EV_CLAIM`, a claim that is its own record; `EV_RECORD`, a record; `EV_MEMBER`, a claim within the record before it. Each event carries the claim's ID, the ID of what was witnessed, the score, the entry rating and deviation of its kind, its position, and its own witness when the source names one statement by statement.

Live counters go to stderr: files done, MB, MB/s, nodes.

## 4. Recompose and compare

Every file of the batch that is not curated and not a vocabulary is rebuilt from the node table and tier 0 (`expand`) and compared with its bytes; a mismatch is reported and makes the run exit 1. A curated source is not kept as a file, so it is not compared; a vocabulary is the text its tokens stand for.

Then `file_take` keeps what each file witnessed for its content and `file_close` composes its trunk, `[metadata, content]`, its metadata tree the OS's record of it as its recipes dispose of it (`file_record`, [Recipes](Recipes.md#how-a-file-is-recorded)).

## 5. Load

`load()` opens one connection per thread with `synchronous_commit = off` and counts the atoms in `entity` at tier 0: none, and all 1,114,112 are written with the first load; fewer than all (a first load cut off mid-flight), and each atom's ID is asked through `recorded()` and only the missing ones are written.

### Trunk to leaf

The files' trunks are probed first: a file whose trunk is recorded is recorded with everything under it and everything it attested, and nothing of it is looked for, played, or written again. Then `prune()` (`src/db.c`) walks **trunk to leaf** by tier (`255` down to `1`), skipping synthetic `blocks_of` spine nodes and pruning any node already present in `tier0.bin`, an admitted chess cache, or `writer.known`. Each round, `recorded()` probes the frontier's candidate IDs in set-oriented batches through `pg_contract.c` (`laplace_present_stage` / partition index probes). A hit marks the node and its entire descendant DAG recorded (`keep = 2`), caching it in `writer.known` so its subtree is amputated on the client and never re-queried; a miss marks it new (`keep = 1`) and queues its logical children for the next tier. `--whole` puts every node in the initial frontier instead. Counters: rounds, IDs checked, subtrees already recorded, new nodes.

### COPY

New nodes (and existing carriers gaining mask or spare annotations) are ordered by topological wave, lane, and Hilbert key (`hilbert_order`), then streamed via binary `COPY` into per-run, per-lane `UNLOGGED` `stage.lp_entity_<xid>_<lane>` and `stage.lp_physicality_<xid>_<lane>` tables (`lanes = min(cores, pool, available)`), without two-phase commit (`PREPARE TRANSACTION`) and without writing partial sections directly into `public.*` while a file is mid-stream. Both `entity.mask` and `physicality.mask` are 64-bit carriers (`bit(64)`, serialized as a 4-byte bit length `64` followed by 8 bytes). Each window merges set-wise inside PostgreSQL through `laplace_merge_stage` and `laplace_enrich_stage`, preserving Hilbert locality and parent-table invariants.

### Records and the series

What a source says is recorded both by containment in its content tree ([Attestations: Witnesses](../Semantics/Attestations.md#witnesses)) and in `public.attestation` (`(claim, witness, lineage)`): every part a recipe speaks of whole is a record (`say.c`), a path in its file's content tree:

- the part's thing first (the sentence, the row), its rows' layers and tree where the recipe gives them (`layers`, `tree`), then each claim it says, in the order said, a vertex said to be a claim (`LP_SAID_CLAIM`) whose run is how many times the record says it, and whose M says how: the outcome (a win; a draw; a loss; or a score, carried in the vertex's spare bits) and its position among the claims said together (`together`), [Physicality](../Storage/Physicality.md#physicality);
- who in the record says a claim (a column of annotators, a speaker: `voices`, `by`, `voice`), a vertex said to be a voice (`LP_SAID_VOICE`) right before the claim: content of the record, never a witness;
- a record that is one claim said once is that claim, standing in the content tree as its own record (`LP_SAID_RECORD`); each part of a part wide enough to be read on every core is a record of its own;
- the blocks of a file's content that hold records are said to (`LP_SAID_HOLDS`), and so is a file's content, so a walk down from a trunk passes over content that says nothing.

A record composed again under the same ID whose claims were said otherwise (another outcome or place) is counted and said; the first is kept. A claim no reference could be made of is counted and said.

The series: before each batch is loaded, the files whose trunks are recorded are found (`files_known`; they say nothing again), and what the rest say is accumulated in-stream into per-witness `(claim, games, score)` series as records flow through the assembly line (retiring the legacy end-of-source `standings_write()` loop and 16-connection `PREPARE TRANSACTION` two-phase commit on unlogged tables). As batches stream into `stage.*`, the per-claim `(claim, games, score)` series update standings inside PostgreSQL via the C extension (`laplace_attest_series(&standing, trust, games, score / games, LP_ATTEST_FLOOR)`), joining against `public.consensus_<h>` in set-based SQL + C rather than pulling `consensus_<h>` rows back over the socket to the client. The trust is the source's: its trunk is the witness, and a recipe naming a class or lineage of its own under the source is said and not used.

### After the load

When every file was of one source, its trunk, `[record, its files' trunks]`, composed in an emptied node table and written by a load of its own, so it is recorded only after every file is; then merge; then the trunk is the witness, known once it has attestations, its trust and lineage the source's, carried on each attestation row. A part of a source (`-s`), or files of several sources, have no trunk: what they say is held by their files' trunks, and no witness holds them. The summary on stdout: decomposition (files, MB, recomposed or curated, mismatched), compositions and reused, the claims said by records; phases: decompose, recompose and compare, deduplication (IDs checked, rounds, subtrees recorded), COPY (entities, paths, rows per second), the series played once each (claims, standings new and updated: read, played, staged), the source's trunk and its ID, merge, the witness, total.

## What a runtime witness states

`laplace witness` is this pipeline with one difference: the source is named on the command line and not by a directory of recipes. `cmd_witness` resolves the files, takes the directory they share as the source's root, and calls `cmd_ingest` with the witness (`--as`), its class (`--class`) and its lineage (`--lineage`, by default its own name) held as a source of that run, which `source_runtime` appends to the loaded sources after the recipes are read; it is in no `order`, and its files are read as any format reads them. From there nothing is its own: recipes are bound, the files decompose through the record VM, trunks are probed, new nodes are staged and merged, the series are accumulated by `laplace_accumulate_series`, the source's trunk `[WITNESS, its files' trunks in path order]` is written last, `load_register` rewrites the provisional witness to that trunk, and `merge` writes the `attestation` rows and folds the standings with `laplace_attest_stage`.

A `.statement` is read by the stock recipe `statement`: a row a line, `subject`, `relation`, `object` and `score` between tabs, each part the text it is, the claim `[subject, relation, object]`, or `[subject, relation]` where no object is written, the score its outcome. The recipe omits `pathname` and `filename`, so a statement's trunk is its content alone: the same lines written to another file are the same trunk, a file the database already holds, and the same witness trunk, so stating it again writes no entity, no attestation and no standing. Its row is `strict` ([Recipes](Recipes.md#what-a-file-attests)): a line that attests nothing, or whose score is no number from 0 to 1, is said (`refused: part N ...`), counted in `refused_parts` of the `ingest rejected` line, and the run exits 1 before the witness is registered, so nothing is attested.

For the statement (`<tab>` a tab)

```text
Paris is the capital of France <tab> is <tab> true <tab> 1
the earth is flat <tab> is <tab> true <tab> 0
```

stated by `--as alice --class UserPromptContent`, the record holds: the content `Paris is the capital of France`, `the earth is flat`, `is`, `true`, each the entity that text is anywhere; the claims `[Paris is the capital of France, is, true]` and `[the earth is flat, is, true]`, each its own record in the statement's content, the first a win and the second a loss in its vertex's M; the statement's trunk over them; the witness trunk `[alice, the statement's trunk]`; two `attestation` rows `(claim, the witness trunk, lineage alice)` with games 1, scores 1 and 0, and trust 0.3; and a `consensus` row for each claim. Another witness stating the same lines adds its own trunk and its own two rows, and the two claims keep one standing each.

## The statements

Every statement the ingest issues, all parameters binary, all sets:

| Phase | Operation (`pg_contract.c` / `Laplace-postgres`) |
| --- | --- |
| trunk & frontier probe | `SELECT 1 FROM entity WHERE id = ANY($1::blake3[])` and `laplace_present_stage` per tier frontier |
| session | `SET synchronous_commit = off` on loader connections; `laplace_ensure_stage` allocates per-run `UNLOGGED` `stage.lp_*` lanes |
| COPY (`stage.*`) | binary `COPY` into `stage.lp_entity_<xid>_<lane>` and `stage.lp_physicality_<xid>_<lane>` with 64-bit `mask` (`bit(64)`) and binary EWKB `coord`/`path` |
| stage merge | `laplace_merge_stage` and `laplace_enrich_stage` merge novel entities, paths, and mask/spare enrichments in Hilbert order |
| series & witness | `laplace_accumulate_series` folds per-batch events; once the source trunk `[record, file trunks]` is merged, `laplace_attest_stage` writes `public.attestation` `(claim, witness, lineage, games, tokens, score, "position", trust)` and folds `public.consensus` |
| GIN cleanup | `laplace_clean_stage` / `laplace_clean_partitions` drains GIN pending lists across touched partitions |

No inline SQL outside `pg_contract.c`, no per-row statement, no cursor, no function call in a predicate.

## Measured

On the reference machine: decompose, hash, deduplicate, and recompose at 8 MB/s on one thread; 2,800,910 IDs deduplicated in 8.2 s; where the bytes differ but the content tree is known, 195 IDs checked in 11 ms and nothing sent; ingesting the 195 Gutenberg texts again, 0.1 s; entity COPY 954,000 rows per second, physicality COPY 215,000 rows per second; 5 million attestations appended at about 245,000 rows per second; standings updated in place at 740,000 to 780,000 attestations per second.
