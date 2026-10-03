# CLI

Laplace is one program, `laplace`, with twenty-one commands: the generators of tier 0 and its flags, the deployment of a database, ingestion and its inverses, the indexes, the read commands, and the measurements.

`laplace` with no command prints the commands and where it will look: the database, tier 0, the recipes, the grammars, the firmware. Where things are comes from the environment, [Environment](Environment.md), else from what the engine was built with. Every command that touches the database takes `-d conninfo`. A command exits 0 when it did what it says, 1 on a failure it reports, 2 on a usage error or a broken recipe or firmware.

## laplace tier0

`laplace tier0 [-u UCD_ROOT] [-o tier0.bin]`. Reads `$LAPLACE_UCD` and writes `$LAPLACE_TIER0` by default. Phases, each timed on stdout: UCD properties and decompositions read (`DerivedGeneralCategory.txt`, `PropList.txt`, `Blocks.txt`, `UnicodeData.txt`); `allkeys.txt` read; the DUCET total order built by `qsort` over the non-ignorable L1, L2, L3 sort key with ties by NFD then codepoint; the Super-Fibonacci points, n = 1,114,112, in the exact operation order of the specification's reference with CORE-MATH's `cr_sin` and `cr_cos`, walked in Hilbert order; coordinates fixed to the exact grid, the units moved inward counted, and IDs hashed; the table written. Prints the table's BLAKE3-256 fingerprint and the order's BLAKE3-256.

## laplace flags

`laplace flags [-u UCD_ROOT] [-o tier0.flags]`. Reads `PropertyAliases.txt` for the binary and enumerated properties in the standard's order, `PropertyValueAliases.txt` for each enumerated property's values, and `ucd.all.flat.xml` for every codepoint's values; writes the 256-bit records and the `.layout` file beside them, and prints a fingerprint.

## laplace highway

`laplace highway [-o highway.bin]`. Generates the highway from what the resources' recipes say of their types (`types`, `keyed`, `alias`, `maps`; [Recipes](Recipes.md#the-highway)), reading every source that says any in order by the one decomposer: the lists, each type's record, the edges, the keys, the layout and the types' contents as compositions beside it, what it left out by lists, and its fingerprint. Each list's slots are frozen by Laplace-Native's manifest (`$LAPLACE_MANIFEST`, `slots/LIST.tsv`): read, kept, new types appended and gone ones retired, never moved, and written back, with the kept, new and retired counts printed. The layout carries the `bank` lines of `banks.tsv`; a list wider than its bank, or than 256 bits, is refused. Beside `highway.bin` it writes `.layout`, `.keys` and `.nodes`.

## laplace deploy

`laplace deploy [-d conninfo]`. Makes the database if the server has none of that name, asking `postgres` over the same connection parameters; then `CREATE EXTENSION IF NOT EXISTS` for `postgis`, `laplace`, `pg_stat_statements`, `pg_buffercache`; `ALTER EXTENSION laplace UPDATE`; `ALTER DATABASE … SET laplace.tier0`, `laplace.flags` and `laplace.highway` to this engine's paths; the tables a database had before the extension owned them made the extension's (`ALTER EXTENSION laplace ADD TABLE`); `SELECT laplace_schema_indexes()`; the highway's own records, from its `.nodes` file, loaded as any content is; `enable_parallel_append` off for the database; then `laplace status`. Each statement is timed on stdout. Idempotent.

## laplace sources

`laplace sources [-d conninfo]`. Every source there is a recipe directory for, in the order `recipes/order` gives: its number, name, how many recipes it has, whether it is in (its witness's ID is in `witness`), where it is kept on this machine or that it is at none of its roots, and the sources it comes after.

## laplace ingest

```text
laplace ingest [-d conninfo] [-t tier0.bin] [-r recipes/] [-j threads] [-s source] [--whole] [--no-load] [--plan] [--claims] file...
laplace ingest [options] SOURCE
laplace ingest [options]
```

Files or directories, walked for every non-hidden non-empty file; a source by its name, its files found under its `root`s or by its `files` patterns; or nothing, which ingests every source in order (`ingest_every`). Options: `-j` threads, default every processor; `-s` names the source the given files are part of; `--whole` looks for every node instead of taking a recorded trunk as recorded, after a run that was cut off; `--no-load` decomposes and checks without writing; `--plan` prints which recipe takes how many files and stops; `--claims` prints every claim the recipes attest, as text, and loads nothing. The pipeline is [Ingest](Ingest.md). Exit 1 when any file does not recompose, a part was not read whole, or a source fails; the run of every source stops at the first source that fails, since what comes after counts on it.

With nothing named: each source runs in a process of its own with the same options, its output in `$LAPLACE_WORK/logs/ingest/<source>.log`; a source none of whose files is here is passed over as absent; one no recipe reads yet is passed over; one that would leave the database's volume with less than a tenth of itself, its files' size times its `room` or `LAPLACE_ROOM_FACTOR`, is not begun and that is said. Summary: sources in, absent, without a recipe, not begun for want of room, and the seconds.

## laplace forget

`laplace forget [-d conninfo] [-j connections] witness...` or `--except witness...`. The witnesses' rows leave `attestation`; what no other witness witnessed goes with its consensus; what others witnessed stays. Then, level by level down the DAG, whatever nothing holds any more goes: an entity stays while any path holds it, or while it is a file, a witness, or witnessed; a file whose content is what it witnessed stays while any of that is still witnessed; atoms always stay. SQL fetches and deletes sets of rows, in chunks of 50,000 IDs on every connection at once; what to delete is decided in the engine.

## laplace sweep

`laplace sweep [-d conninfo] [-j connections] [--dry]`. One pass over every path counts, for every entity, the places that hold it; an entity no path holds goes, unless it is a file, a witness, or something `attestation` says was witnessed, and its consensus with it; what it held is counted down and goes in turn when its count reaches nothing. `--dry` reports and deletes nothing.

## laplace index

`laplace index [-d conninfo]`. Sets `maintenance_work_mem` to 8 GB for the session and calls `laplace_schema_indexes()`, which makes every index the schema has where one is missing, then `ANALYZE`; `laplace deploy` makes them all from the start.

## laplace status

`laplace status [-d conninfo]`. Prints the database and its size; the server version; the extension's version and `laplace_isa()`; the tier-0 path the database is set to and `laplace_fingerprint()`; the highway's path and `laplace_highway_fingerprint()`, against this engine's; and whether that fingerprint is **the same as this engine's** or **DIFFERS from this engine's tier 0: the two would give the same content different coordinates**; entities by tier with the planner's counts and sizes; the witness, attestation, and consensus counts; and how many GIN and GiST indexes exist on `entity` and `physicality`.

## laplace text

`laplace text TEXT`. Computed here, no database, tier 0 mapped: the entity's ID, tier, real coordinate, Hilbert value, and depth, `1 − ‖c‖`; whether it is inside the wall; its parts in order, each with the same; the tier-0 fingerprint; the milliseconds.

## laplace tree

`laplace tree FILE`. The file's syntax tree as its recipe's grammar reads it, for writing recipes.

## laplace structure

`laplace structure LAYOUT FILE [-n nodes]`. The tree of the first megabyte of a file as a recipe's layout lines part it (tiers, parts, notes, empties), each outermost part with its named parts and texts, for writing recipes ([Recipes](Recipes.md)).

## laplace hop

`laplace hop [-d conninfo] [-n N] [--firmware FILE] [--k K] [--fan F] TEXT` or `SUBJECT PREDICATE OBJECT` with `?` for a part left open. Everything attested about the entity the text names, by confidence: `confidence rating dev matches given [claim]` for up to `N` claims, default 24, whether more exist than the fan reads, and for a whole entity what holds it, paths by tier. `--k` and `--fan` override the firmware to measure against it. Prints the milliseconds for claims and containers and the round trips made for text.

## laplace translate

`laplace translate [-d conninfo] [-n N] [--firmware FILE] WORD FROM TO...`. Up from the word to its concepts along the relations the firmware's `up` names for translate, each step in its witness's order then by standing, keeping what stands below a concept in the language FROM (read as the firmware's `language` says); then, for each target language, back down from the concept the same way to that language's words, with what the firmware's `gloss` names shown of each concept ([Firmware](Firmware.md)).

## laplace degrees

`laplace degrees [-d conninfo] [-n N] [--firmware FILE] [--batch B] FROM [TO]`. How far one entity is from another over rated claims, a best-first search over `lp_cost` under the firmware's `k`, `lambda`, `fan`, and `hops`; or, with no target, what is nearest one.

## laplace fills

`laplace fills [-d conninfo] [-n N] [-t tier0.bin] PHRASE`. What follows the phrase, counted by occurrence across every source; the algorithm is [Reads](Reads.md#laplace-fills).

## laplace pull

`laplace pull [-d conninfo] [--firmware FILE] [--seed N] PROMPT`. The prompt broken down to its trunk and constituents, then the steps the firmware's `for pull` instruction set takes: `take segment`, `take attestations N`, `take constituents N`, `take fact`, `take chain N RELATION...`; `--seed` fixes the draw when the firmware's `top within N` allows a tie to be taken. It is `cmd_pull` in `forward.c`; `pull.c` holds `hop`, `translate` and `degrees`.

## laplace turn

`laplace turn [-d conninfo] [--firmware FILE] [--as USER] [--session NAME] [--seed N] [--read] PROMPT`. A turn of a session, answered by the one forward program (`program.c`), under the firmware's `for pull` set; each stage's state is printed as the trace. RESOLVE admits the prompt as content, recorded before anything couples with the user witnessing it (not with `--read`), and its constituents as occurrences; the prompt is never its own response, not even its own nearest curve, and resolves the session from the record: the session is `[USER, NAME]`, its turns the claims `[session, turn]` its user witnessed, ordered by their positions in `attestation`, their constituents the discourse; a word is an obligation unless what is attested of it under the firmware's `role by` kind says it pulls nothing. COUPLE reads every strand of the occurrences, the prompt and the discourse at once, kept apart by route. ORIENT takes the responding entities that ground the most of what the obligations owe, each word as hard as it pulls, hubs last and the least shared first, and names the disposition: unique, ambiguous, or nothing responds. ROUTE sets the firmware's hops, fan, k, λ and emission budget; SCAN walks best-first from up to four centres; the firmware's chains are followed from each word still owed. Then, a constituent at a time: PROPOSE offers what follows the active trajectory as a run in what was observed, and a chain's answer while its word is owed (an entity the coupling merely reaches is not output); STEER elects by what a proposal grounds, then ordinal continuity, then confidence at k, then the least shared; SELECT takes the top, or a near tie as `top within` allows; REALIZE renders it; and the constituent joins the trajectory, what it grounds closes, and the next step is chosen from that state. The turn is complete when no more than the firmware's `enough` of what was owed remains, or the budget `emit` is spent. Unless `--read`, WITNESS records the response and the turn `[prompt, response]` as content, the user's `[session, turn]` at its ordinal under `UserPromptContent`, and Laplace's `[response, prompt]` under `ResponseContent`.

## laplace bench

`laplace bench`. Every native operation measured on this machine, one line each with rate, nanoseconds per operation, and bandwidth where it applies: codepoint ID; composition ID at 6, 24, and 96 children; ID into the mantissas and round trip; an EWKB path of 1 M children per child; the Hilbert value; the wall check; the exact centroid per point; the vertex scan scalar, AVX2, AVX-512; squared distances scalar and AVX2; DTW, EDR, Fréchet with one outlier; text to its trunk per call; codepoint of an ID; the frontier's reach and take per entity over 1 M; one Glicko-2 attestation. The reference machine's values are in [Research: Engine Measurements](../Research/Engine.md#native-operations).

## laplace model

`laplace model MODEL_DIR [--layers N] [--z zmin] [--cap K] [--sample word ...]`. A safetensors checkpoint of the Llama architecture read as "b beats c given a": the circuits `embed`, `direct`, `Lk.Hh.qk`, `Lk.Hh.ov`, `Lk.ffn`, each rows *a* against candidates *b* through `lp_rowsig`, with timing, throughput, and how much survives each circuit's own noise floor. Prototype stage: it reports the numbers; recording the survivors as attestations comes after. Needs MKL.
