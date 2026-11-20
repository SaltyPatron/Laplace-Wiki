# Games

The Engine reads PGN collections through its compiled chess grammar and Lichess opening tables through a TSV recipe with injected PGN move text.

## Sources

[`recipes/order`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/order) admits five PGN and opening sources ahead of `syzygy` ([Syzygy](Syzygy.md)):

| Source | Witness & trust class | Packaging | Recipe |
| --- | --- | --- | --- |
| `chess-com` | `Chess.com` source trunk (`StructuredCorpus`) | Chess.com PGN archives | [`recipes/chess-com/`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/chess-com) |
| `twic` | `The Week in Chess` source trunk (`AcademicCurated` / OTB archive) | TWIC PGN issues | [`recipes/twic/`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/twic) |
| `lumbras-gigabase` | `Lumbra's Gigabase` source trunk (`StructuredCorpus`) | Lumbra's Gigabase PGN archives | [`recipes/lumbras-gigabase/`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/lumbras-gigabase) |
| `laplace-chess` | `Laplace` runtime witness (`AppDerived`) | PGN games played by Laplace in web, Lichess, Arena, and `fastchess` sessions | [`recipes/laplace-chess/`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/laplace-chess) |
| `openings` | `Lichess chess-openings` source trunk (`AcademicCurated`) | Lichess TSV tables `a.tsv` through `e.tsv` (`eco`, `name`, `pgn`) | [`recipes/openings/`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/openings) |

Each source has one corpus witness trunk; players, events, sites, clocks, and annotations are content under its records and never mint extra corpus witnesses. The compiled `tree-sitter-pgn` grammar feeds `Laplace-Engine/src/chess.c` and `src/chess_rules.c`, composing canonical BLAKE3 positions (`[board, turn, castling, ep]`), moves, `[P, M, P']` transitions, and full game trajectories (`[P0, M0, P1, …]`). Decisive and drawn completed games score their transition series by game outcome (`1-0`, `0-1`, `1/2-1/2`); unfinished games (`*`) record the trajectory without an outcome; opening rows bind an `[eco, name]` classification onto the replayed line and terminal `position` (`product position`) without inventing a game result.

## Format & player identity (`FIDE ID` highway node vs. literal PGN tags)

| Record | Fields in order | What a record is | Specification |
| --- | --- | --- | --- |
| PGN game | Seven Tag Roster (`Event`, `Site`, `Date`, `Round`, `White`, `Black`, `Result`), optional supplemental tags (`FEN`, `Variant`, `WhiteElo`, `BlackElo`, `WhiteFideId`, `BlackFideId`, `TimeControl`, `ECO`), then movetext | Tag-pair metadata + replayed move trajectory (`[P0, M0, P1, …]`) and `[P, M, P']` transition attestations | [PGN Standard](https://github.com/fsmosca/PGN-Standard/blob/master/PGN-Standard.txt) §8.1.1, §8.2 |
| Opening row (`a.tsv`..`e.tsv`) | `eco`, `name`, `pgn` | ECO code and English opening name bound to the replayed PGN move trajectory and resulting position | Lichess `chess-openings` TSV specification |
| FIDE rating-list player (`Batch 3` recipe queue) | `FideId`, `Name`, `Federation`, `Sex`, `Title`, `Standard`, `Rapid`, `Blitz`, `BirthYear`, `Flag` | Official FIDE player record (`rating-list.snapshot.json.gz`), queued for declarative `.recipe` admission in `Batch 3` (`Laplace#833`) | FIDE Rating List snapshot |

Under the Recording Law ([INVENTOR_RECORD](../Repositories/Laplace/docs/INVENTOR_RECORD.md), [27. Chess](../Sequence/Chess.md), [30. Conflicts](../Sequence/Conflicts.md) R4, S1), player identity and Elo ratings follow two clean rules with zero contradiction:

1. **FIDE IDs as shared highway nodes vs. unlinked PGN name tags:** A `FideId` (`1503014`) is a publicly shared identifier across sources and scripts, and therefore a **highway node** for that human player—exactly as an `ILI` is for a concept. When `rating-list.snapshot.json.gz` (queued `.recipe`) or PGN `WhiteFideId`/`BlackFideId` tags are present, the player's `Name` in FIDE, localized script spellings, and PGN `"Carlsen, Magnus"` tag strings link as attested name lexicalizations onto that `FideId` node. Where an online or historical PGN game carries only `White` and `Black` strings and no `FideId`, the recipe records the exact literal tag text written in the PGN—never fabricating a synthetic player hash and never guessing entity merges on ambiguous strings.
2. **Source Elo tags ≠ Laplace Glicko-2 `consensus`:** `WhiteElo`, `BlackElo`, and FIDE `Standard`/`Rapid`/`Blitz` numbers are **source-stated rating observations** (`INVENTOR_RECORD.md:223–225`), strictly separated from Laplace's Glicko-2 claim `consensus` over `[P, M, P']` transitions and from `fastchess` + `Ordo` engine-ladder Elo ([30. Conflicts](../Sequence/Conflicts.md) K1).

## Record kinds

| Kind | How the source marks it | Laplace representation |
| --- | --- | --- |
| Played game | Seven Tag Roster + `1-0`, `0-1`, or `1/2-1/2` | Canonical `[P0, M0, P1, …]` line shared across every game playing those moves, `[P, M, P']` transition claims scored for the side to move, and game occurrence tags |
| Custom start | `[SetUp "1"]` + `[FEN "…"]` | Trajectory starts at `P0` decoded from the FEN's four canonical position fields |
| Chess960 / rule variants | `[Variant "Chess960" \| "Crazyhouse" \| "Atomic" \| "Antichess" \| "King of the Hill" \| "3-check" \| "Horde" \| "Racing Kings"]` | Rulesets are declarative axes in `Laplace-Engine/firmware/chess.firmware` executed by `src/chess_rules.c` ([28. Games](../Sequence/Games.md)); variant names never pollute position hashes, and variant-extra state (pocket hands, promoted squares, check counters `+W+B`) enters the position composition only when non-empty |
| Incomplete game | `[Result "*"]` or abandoned/forfeit termination | Trajectory and tags recorded as observed content with zero win/loss transition claim |
| Annotated study / puzzle | Rav variations `(...)`, `{comments}`, NAG glyphs (`$1`, `!?`), or composed puzzle solution | Tree of candidate lines, commentary text, and annotator judgments under the study's witness, distinct from played OTB occurrences |

## Recording & reading games on the unified substrate

Games played by Laplace across the web Chess Lab, Lichess bot sessions, Arena matches, and `fastchess` gauntlets ([27. Chess](../Sequence/Chess.md)) are written as standard PGN files (with `[%clk]` annotations) under `$LAPLACE_DATA/Games/Chess/laplace`, named by content BLAKE3 so identical games deduplicate, and admitted through `Laplace-Engine` (`laplace witness --as Laplace --class AppDerived FILE` or `laplace ingest laplace-chess`). Ad-hoc single PGN files admit directly via `laplace ingest FILE` using stock `pgn.recipe`.

All read surfaces—`Laplace-Engine` (`reader.h` / `program.c` under `chess.firmware`), `Laplace-MCP` (`/v1/chess_*`), and the `Laplace` web application (`Laplace.Native.Interop` over the canonical `laplace` database)—query the **same** 4 substrate tables (`entity`, `physicality`, `attestation`, `consensus`) for `[P, M, P']` transition standings, opening classifications, player game histories, and live `Syzygy` probes, with no separate monorepo SQL schema or `laplace-mono` CLI.
