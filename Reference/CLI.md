# CLI

Laplace is one program, `laplace`, with thirty-one commands: the generators of tier 0 and its flags, the deployment of a database, ingestion and its inverses, the indexes, the read commands, and the measurements.

`laplace` with no command prints the commands and where it will look: the database, tier 0, the recipes, the grammars, the firmware. Where things are comes from the environment, [Environment](Environment.md), else from what the engine was built with. Every command that touches the database takes `-d conninfo`. A command exits 0 when it did what it says, 1 on a failure it reports, 2 on a usage error or a broken recipe or firmware.

## laplace tier0

`laplace tier0 [-u UCD_ROOT] [-o tier0.bin]`. Reads `$LAPLACE_UCD` and writes `$LAPLACE_TIER0` by default. Phases, each timed on stdout: UCD properties and decompositions read (`DerivedGeneralCategory.txt`, `PropList.txt`, `Blocks.txt`, `UnicodeData.txt`); `allkeys.txt` read; the DUCET total order built by `qsort` over the non-ignorable L1, L2, L3 sort key with ties by NFD then codepoint; the Super-Fibonacci points, n = 1,114,112, in the exact operation order of the specification's reference with CORE-MATH's `cr_sin` and `cr_cos`, walked in Hilbert order; coordinates fixed to the exact grid, the units moved inward counted, and IDs hashed; the table written. Prints the table's BLAKE3-256 fingerprint and the order's BLAKE3-256.

## laplace flags

`laplace flags [-u UCD_ROOT] [-o tier0.flags]`. Reads `PropertyAliases.txt` for the binary and enumerated properties in the standard's order, `PropertyValueAliases.txt` for each enumerated property's values, and `ucd.all.flat.xml` for every codepoint's values; writes the 256-bit records and the `.layout` file beside them, and prints a fingerprint.

## laplace highway

`laplace highway [-o highway.bin] [--fingerprint] [--identities]`. Generates the self-contained highway directly from Laplace-Native's manifest (`$LAPLACE_MANIFEST`: `slots/LIST.tsv`, `banks.tsv`, `maps/*.tsv`) and the mapped `tier0.bin` without requiring raw corpus files on disk: every highway slot is the canonical Tier-0 composition of its own shared identifier (`i46360`, `eng`, `abandon.01`, `give-13.1`, `va:0001f`, `NOUN`), deterministic from `tier0.bin` alone. When raw corpora are present, `laplace highway` also reads what the resources' recipes say of their types (`types`, `keyed`, `alias`, `maps`; [Recipes](Recipes.md#the-highway)), appending any newly discovered types to `slots/LIST.tsv` and `maps/*.tsv` while keeping existing slots frozen and never moving them. The layout carries the `bank` lines of `banks.tsv` inside the single **64-bit** mask carrier (`LP_MASK_BITS = 64`); a bank overflowing the 64-bit layout is refused. `--fingerprint` prints the existing `highway.bin` fingerprint without regenerating; `--identities` reports stored and canonical highway identifier IDs as TSV.

## laplace chess

`laplace chess [-o chess.bin] [-t tier0.bin] [-r recipes/] [-j threads] [-s source] [--verify] [--fingerprint] [what...]`. Generates or verifies the `LPPC0001` chess perf-cache (`$LAPLACE_CHESS`, else `${LAPLACE_TIER0%.bin}.chess`), mapped on both client and server (`laplace.chess`): dense direct-address sections (`square` 64, `piece_square` 768, `side` 2, `number` 256, `castling` 7,225, `en_passant` 17, `move`) plus sparse admitted `board`, `position`, `[P, M, P']` `transition`, and `(P, M) -> P'` `next` pair sections from the named sources or files. `--verify` recomputes every vocabulary record from the law and replays every stored move from the standard start; `--fingerprint` prints the existing module's fingerprint and counts.

## laplace deploy

`laplace deploy [-d conninfo] [--schema name] [--configure-server-cache | --prepare] [--recreate]`. Makes the database if the server has none of that name, asking `postgres` over the same connection parameters; creates `postgis` and `laplace`; when the database holds an earlier build of `laplace` whose `laplace-storage:<hash>` matches, transitions it in place through `laplace.reconcile.sql` (`ALTER EXTENSION laplace UPDATE TO ...` + `laplace_restore_function_bindings()`) without dropping data, recreating only when `--recreate` is passed for a persistent storage table DDL change; sets `laplace.tier0`, `laplace.flags`, `laplace.highway`, and `laplace.chess` when `--configure-server-cache` runs (`--prepare` preserves immutable modular server cache bindings); runs `SELECT laplace_schema_indexes()`; sets `enable_parallel_append` off for the database; then runs `laplace status` (unless `--prepare`). Each statement is timed on stdout. Idempotent.

## laplace sources

`laplace sources [-d conninfo] [--catalog]`. Every source there is a recipe directory for, in the order `recipes/order` gives: its number, name, how many recipes it has, whether it is in (a witness with `attestation` rows is a trunk `[record, file trunks]` whose record is the source's name), where it is kept on this machine or that it is at none of its roots, and the sources it comes after. `--catalog` emits all available sources, aliases, content locations, recipes, and formats as JSON without touching the database or perf-caches.

## laplace ingest

```text
laplace ingest [-d conninfo] [-t tier0.bin] [-r recipes/] [-j threads] [-s source] [--highway] [--whole] [--no-load] [--plan] [--catalog] [--list-sources] [--claims] [--claims-tsv] [--entities] [what...]
```

Files or directories, walked for every non-hidden non-empty file; a source by its name, its files found under its `root`s or by its `files` patterns; or nothing, which ingests every source in `recipes/order` (`ingest_every`). Options: `-j` threads, default every processor; `-s` names the source the given files are part of; `--highway` admits or validates the existing highway contents; `--whole` looks for every node instead of taking a recorded trunk as recorded; `--no-load` decomposes and checks without writing; `--plan` prints which recipe takes how many files and stops; `--catalog` and `--list-sources` inspect the recipe inventory without DB access; `--claims` and `--claims-tsv` print what the recipes attest without loading; `--entities` prints every composition a sample makes. The pipeline is [Ingest](Ingest.md). Exit 1 when any file does not recompose, a part was not read whole, or a source fails; the run of every source stops at the first source that fails, since what comes after counts on it.

With nothing named: each source runs in a process of its own with the same options, its output in `$LAPLACE_WORK/logs/ingest/<source>.log`; a source none of whose files is here is passed over as absent; one no recipe reads yet is passed over; one that would leave the database's volume with less than a tenth of itself, its files' size times its `room` or `LAPLACE_ROOM_FACTOR`, is not begun and that is said. Summary: sources in, absent, without a recipe, not begun for want of room, and the seconds.

## laplace witness

`laplace witness [-d conninfo] [-t tier0.bin] [-r recipes] [-j threads] --as WITNESS --class CLASS [--lineage NAME] [--root DIR] [--no-load] [--claims] FILE...`. What a witness named at run time states, recorded as a source is (`cmd_witness` in `ingest.c`): the files are read by the recipes any file of their kind is read by, a `.statement` by `recipes/statement.recipe`, a claim a line, `subject`, `relation`, `object` and a score from 0 to 1 between tabs; the trunk is `[the witness's name, its files' trunks]`, and that trunk is the witness its attestations are keyed by, at the prior of `CLASS` (one Laplace-Native's `manifest/trust_classes.toml` declares). `--lineage` names the witness it derives from, its own name when none is given, so what one witness states at different times is one lineage. `--root DIR` sets the base directory the files' pathnames are recorded from (default: the directory they share). `--no-load` and `--claims` read without a database.

## laplace merge

`laplace merge [-d conninfo] [-j jobs]`. Merges staged entities and paths (`stage.*`) into the partitioned `public.*` tables set-wise ([Ingest](Ingest.md)); `laplace ingest` runs stage merges automatically during admission.

## laplace projection

`laplace projection [-d conninfo] [--apply]`. Audits (`--apply` omitted) or atomically repairs (`--apply`) derived 4D `entity.coord` and `physicality.hilbert` values across the stored DAG via `laplace_recoordinate(apply)`, rejecting unknown or non-atomic leaves while preserving all content IDs, packed paths, 64-bit masks, witnesses, and `consensus` standings.

## laplace forget

`laplace forget [-d conninfo] [-j connections] [--except] [--trunk] witness...`. A witness is a source's trunk, `[its record, its files' trunks]`, named by the source's name its record is, or by its ID with `--trunk` (`--except` forgets every witness except those named). The claims its records say are found first, by a walk down from the trunk; its `attestation` rows are deleted; then, level by level down from the trunk, whatever it alone held goes: its files, their records, and the claims and content no other trunk or path holds, each with its `consensus` standing; atoms always stay. Last, the standings of every claim its records said that another witness still attests are replayed from the remaining witnesses; a claim no witness attests any more loses its standing.

## laplace sweep

`laplace sweep [-d conninfo] [-j connections] [--dry]`. One pass over every path counts, for every entity, the places that hold it; an entity no path holds goes, unless it is a witness trunk, a lineage, or a standalone file trunk, and its `consensus` row goes with it; what it held is counted down and goes in turn when its count reaches zero. `--dry` reports and deletes nothing.

## laplace held

`laplace held [-d conninfo] [--files] [--tsv FILE] PART...`. Who said a claim, how many times and how, by containment: the claims matching `PART...` (each `PART` a text, `LIST:KEY` a type of the highway, `?` a part left open) are walked up the GIN container index (`physicality_paths`), one set read a level, to the records that say them, the files, and the witness trunks at the top (`attestation` supplying each witness trunk's declared trust). The count is read off the tree (`lp_tally`): `games`, `tokens`, `score` (from each record vertex's outcome and spare bits), and the least positive `position`. `--files` gives the count under each file as well; `--tsv FILE` writes tab-separated containment rows (`games`, `tokens`, score sum, least position). The forward pass and `laplace_attested` read provenance the same way ([Reads](Reads.md)).

## laplace replay

`laplace replay [-d conninfo] [--write] [--tsv FILE] [--files]`. Recomputes standings from containment alone: each witness's trunk, in `recipes/order`, is walked down to the claims its records say (`laplace_contained_series`), each claim's series folded from the stock prior (`lp_series` / `laplace_attest_series`), and every standing compared bit for bit with `consensus`: identical, different, or missing. `--write` puts the replayed standings in place; `--tsv` and `--files` write the tallied containment series. Exit 1 when any differs.

## laplace pgn

`laplace pgn [-d conninfo] [-t tier0.bin] [-o file.pgn] [--verify] ID...`. Reconstructs the PGN of one or more recorded chess files, game records, or lines from the database alone (the read edge of `src/chess.c`, writing to `-o` or stdout). `--verify` recomputes every constituent ID under each root from Tier-0 codepoints with BLAKE3 alone and replays every legal move to confirm each resulting position matches `[P, M, P']`.

## laplace tablebase

`laplace tablebase [-T tables] [-n open] [--line | --pgn] [FEN...]`. A position's endgame tablebase read, from the Syzygy tables alone, with no database: each FEN given, or one a line of standard input. The tables are those under `-T` (`ROOT/NAME.rtbw` and `ROOT/DIR/NAME.rtbw`), else `$LAPLACE_SYZYGY`, else `$LAPLACE_DATA/Games/Chess/syzygy`. Each table is mapped when a probe first needs it, and at most `-n` are mapped at once (64). Tab-separated output: `position`, its ID, its win/draw/loss and distance to zeroing for the side to move (`none` where the tables do not cover it); then a `move` line for each legal move, best first, with its SAN, UCI, the mover's verdict and distance to zeroing of the position it makes, the mover's distance to zeroing through the move, and the IDs of that position and of the `[P, M, P']` claim. `--line` adds the best-play line: `line`, its ID, its result, its plies and their SAN, then a `claim` line for each ply. `--pgn` writes the line alone as the PGN the syzygy source records. Standard error says how many tables were mapped and the most at once. Exit 1 where a position is not covered. The prober is [Syzygy](../Corpora/Syzygy.md#a-verdict-is-a-read)'s.

## laplace index

`laplace index [-d conninfo]`. Calls `laplace_schema_indexes()`, making every index the schema declares where one is missing, followed by `ANALYZE`; `laplace deploy` makes them all from the start.

## laplace status

`laplace status [-d conninfo] [--joins]`. Prints the database and its size; the server version; the extension's version and `laplace_isa()`; the database's `tier0`, `highway`, and `chess` perf-cache paths and fingerprints against this engine's (**the same as this engine's** or **DIFFERS**); sampled entities by tier and total `entity`/`physicality` size; `attestation` and `consensus` partition row counts and sizes; and the GIN and GiST index counts on `entity` and `physicality`. With `--joins`, runs `cmd_highway_joins` reporting highway identifiers attested across at least 2, 3, and 4 independent source lineages.

## laplace text

`laplace text [--segments] TEXT`. Computed locally with no database and `tier0.bin` mapped: the entity's ID, tier, real coordinate, Hilbert value, depth `1 − ‖c‖`, wall check, its parts in order, the tier-0 fingerprint, and elapsed milliseconds. `--segments` emits the canonical tailored UAX #29 word-segment occurrence IDs (including whitespace and punctuation) as JSON.

## laplace firmware

`laplace firmware [--firmware FILE] [--operation hop|search|translate|follows|pull]`. Loads the firmware (`$LAPLACE_FIRMWARE` by default) for the named operation (default `pull`), resolves every `@RECIPE/FIELD` relation reference against `$LAPLACE_RECIPES`, computes the firmware file's content-addressed text ID (`firmware_id`), and prints `{firmware_id, operation, up, chains}` as JSON without database access.

## laplace tree

`laplace tree [-r recipes/] [-g grammar] [-n nodes] FILE`. Prints the file's syntax tree (default first 400 nodes) as its recipe's or `-g` Tree-sitter grammar reads it, for writing recipes.

## laplace structure

`laplace structure [-n nodes] LAYOUT FILE`. Prints the tree of the first megabyte of `FILE` (default 60 nodes) as `LAYOUT`'s format/tier rules part it, for writing recipes ([Recipes](Recipes.md)).

## laplace hop

`laplace hop [-d conninfo] [-n N] [--firmware FILE] [--fan F] [--k K] TEXT` or `SUBJECT PREDICATE OBJECT` with `?` for a part left open. Everything attested about the entity the text names, by confidence: `confidence rating dev matches given [claim]` for up to `N` claims, default 24, whether more exist than the fan reads, and for a whole entity what holds it, paths by tier. `--k` and `--fan` override the firmware to measure against it. Prints the milliseconds for claims and containers and the round trips made for text.

## laplace translate

`laplace translate [-d conninfo] [-n concepts] [--firmware FILE] WORD FROM TO...`. Follows the firmware's `for translate` recipe-bound `lexicalization` (`[lemma, language, ILI]`, ordered by `usages`, witness order, and standing) and `equivalent` ISO 639 codes from `WORD` in `FROM` up to up to `N` concepts (default 4), then back down into each target language `TO...` with each concept's `gloss` ([Firmware](Firmware.md)).

## laplace degrees

`laplace degrees [-d conninfo] [--firmware FILE] [-n N] [--fan F] [--hops H] [--batch B] [--k K] [--per-hop C] FROM [TO]`. How far one entity is from another over rated claims, a best-first search over `lp_cost` under the firmware's `k`, `lambda`, `fan`, and `hops` (default `-n 24`, `--batch 64`); or, with no target, what is nearest `FROM`.

## laplace fills

`laplace fills [-d conninfo] [-n N] [-t tier0.bin] PHRASE`. What follows the phrase (default `-n 12`), counted by occurrence across every source; the algorithm is [Reads](Reads.md#laplace-fills).

## laplace pull

`laplace pull [-d conninfo] [--firmware FILE] [--seed N] PROMPT`. The prompt broken down to its trunk and constituents, then the steps the firmware's `for pull` instruction set takes: `take segment`, `take attestations N`, `take constituents N`, `take fact`, `take chain N RELATION...`; `--seed` fixes the draw when the firmware's `top within N` allows a tie to be taken. It is `cmd_pull` in `forward.c`; `pull.c` holds `hop`, `translate` and `degrees`.

## laplace turn

`laplace turn [-d conninfo] [--firmware FILE] [--as USER] [--session NAME] [--seed N] [--read] [--files] [--receipt FILE] PROMPT`. A turn of a session, answered by the eleven-stage stateful forward program (`program.c`) under the firmware's `for pull` set, printing each stage's trace (`RESOLVE`, `COUPLE`, `ORIENT`, `ROUTE`, `SCAN`, `COMPOSE`, `PROPOSE`, `STEER`, `SELECT`, `REALIZE`, `WITNESS`). `RESOLVE` admits the prompt on the client (the prompt is never its own response), resolves `[USER, NAME]`'s prior turns as discourse, and weights word obligations by `role`; `COUPLE` probes trajectory segments, claims, BLAKE3-seeded random walks with restart, and 4D curve-shape neighbors; `ORIENT`, `ROUTE`, `SCAN` (walking both rated database claims and `lp_highway_edges`), and `COMPOSE` build the typed frontier; `PROPOSE`, `STEER` (comparing proposals across `elect` keys), `SELECT`, and `REALIZE` emit constituents step by step until remaining obligation falls within `enough` or `emit` is spent; and unless `--read`, `WITNESS` records `[prompt, response]`, `[session, turn]` under `UserPromptContent`, and `[response, prompt]` under `ResponseContent`. `--files` reads the prompt from a file; `--receipt FILE` streams JSONL stage/step receipts (`resolve`, `step`, `realize`, `witness`). (`Batch 2` is scheduled to collapse `program.c`'s current multi-round-trip SQL loop into 2–3 batched binary probes in `<100–200ms`, add Highway A* + N-ary traversal and Gödel OODA gates, and weight content obligations ahead of stop-word frames.)

## laplace said

`laplace said [-d conninfo] [--firmware FILE] [--as USER] [--session NAME] [--by NAME] [--files] [--receipt FILE] PROMPT RESPONSE`. A turn said elsewhere: another program gave the response (`--by`, `Laplace` when none is given) and nothing is generated. The prompt and the response are decomposed as `laplace turn` decomposes its own, and the same writer records the user's `[session, turn]` at its ordinal under `UserPromptContent` and the responder's `[response, prompt]` under `ResponseContent`. The turn `[prompt, response]` is content: said again in the same session it is the claim the session holds, and nothing is witnessed again. `--files` reads both texts from files; `--receipt` writes `resolve` and `witness` as `laplace turn` does.

## laplace bench

`laplace bench [-d conninfo] [--joins]`. Measures every native operation on this machine (`lp_bench`), one line each with rate, nanoseconds per operation, and bandwidth where applicable: codepoint ID; composition ID at 6, 24, and 96 children; ID into the mantissas and round trip; an EWKB path of 1 M children; 4D Hilbert value; wall check; exact centroid; vertex scan (`scalar`, `avx2`, `avx512`); 4D squared distances (`scalar`, `avx2`, `avx512`); quantized `int8` dot products; DTW, EDR, Fréchet with one outlier; text decomposition; codepoint lookup; frontier reach and pop over 1 M entities; Glicko-2 `lp_attest_series`. With `--joins`, reports cross-corpus convergence on highway nodes against `-d conninfo`. Reference machine numbers are in [Research: Engine Measurements](../Research/Engine.md#native-operations).

## laplace model

`laplace model MODEL_DIR [--layers N] [--z zmin] [--cap K] [--sample word ...]`. A safetensors checkpoint of the Llama architecture read as "b beats c given a": the circuits `embed`, `direct`, `Lk.Hh.qk`, `Lk.Hh.ov`, `Lk.ffn`, each rows *a* against candidates *b* through `lp_rowsig`, with timing, throughput, and how much survives each circuit's own noise floor. Prototype stage: it reports the numbers; recording the survivors as attestations comes after. Needs MKL.
