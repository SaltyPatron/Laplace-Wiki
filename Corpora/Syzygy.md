# Syzygy

The Syzygy endgame tablebases are read, not recorded: a position's verdict is a probe of the tables, and the source records only the endings they add, the best-play lines from the positions of up to five pieces that recorded games and openings reach.

## Source

| Source | Packaging | Recipe |
| --- | --- | --- |
| `syzygy` | Syzygy tables, `NAME.rtbw` (WDL) and `NAME.rtbz` (DTZ), the 3-4-5 piece set of the lichess mirror (`tablebase.lichess.ovh/tables/standard/3-4-5-wdl`, `3-4-5-dtz`; `files-345.txt` lists them) | [Syzygy](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/syzygy) |

The witness is the tablebase, one trunk; its class is `StandardsDerived`, the class [`trust_classes.toml`](https://github.com/SaltyPatron/Laplace-Native/blob/main/manifest/trust_classes.toml) gives tablebases. The files are kept under `$LAPLACE_DATA/Games/Chess/syzygy/<set>/`. A table's `.rtbw` is the source's file. Its `.rtbz` beside it is read only by the probe. The source comes after the chess sources in `recipes/order` (`chess-com`, `twic`, `lumbras-gigabase`, `laplace-chess`, `openings`), because its lines begin where their records stand.

## Format

A table is not a list of positions. It is an index over the placements of its material, folded by the board's symmetries (8 for a pawnless table, the left-right mirror for one with pawns) and compressed with pair encoding; the values are right only where no capture decides the position, and a DTZ table holds one side to move. One table answers for its material either way round: KQvK holds KvKQ too. The format is Ronald de Man's ([syzygy-tables.info](https://syzygy-tables.info/metrics)); [Fathom](https://github.com/jdart1/Fathom) (MIT) is the reference prober.

| File | What a position's value is |
| --- | --- |
| `.rtbw` | its result for the side to move under the 50-move rule: win, cursed win (a win the 50-move rule draws), draw, blessed loss (a loss it saves), loss |
| `.rtbz` | its distance to zeroing: the plies to the next capture or pawn move under best play, positive where the side to move wins, negative where it loses, beyond 100 where the 50-move rule turns the result. A probe's DTZ may be one ply more than the true distance where the table rounds |

## A verdict is a read

A table is a deterministic provider ([INVENTIONS](../Repositories/Laplace/docs/INVENTIONS.md) #101), so its verdicts are derived when asked and are never stored per position (#102). The Engine's prober is `src/chess_tablebase.c`, in `laplace_engine_reader`, the library Laplace-MCP links. It carries over Fathom's law: the index encoding, pair decompression, `probe_wdl`, `probe_dtz` and the ranking of a root's moves. Every move, check and position in it is the Engine's one chess, `chess_rules.c`.

| Entry | What it gives |
| --- | --- |
| `lp_tablebase_open(root, max_open)` | the tables under `root/NAME.rtbw` and `root/DIR/NAME.rtbw`; root `NULL` is `$LAPLACE_SYZYGY`, else `$LAPLACE_DATA/Games/Chess/syzygy` |
| `lp_tablebase_wdl`, `lp_tablebase_dtz` | the verdict for the side to move; 0 where the tables do not cover the position (more pieces than they hold, castling rights) |
| `lp_tablebase_rank` | every legal move, best first: the mover's result, then a win's soonest zeroing and a loss's latest, then the position that zeroes again soonest |
| `lp_tablebase_line` | the best-play line, rank's first move each ply, to mate, through each zeroing move into the smaller tables, with its result under the 50-move rule |
| `lp_tablebase_probe_fen`, `lp_tablebase_line_fen` | the same from a FEN, each move and ply with its SAN, UCI, the IDs of the move and the position it makes, and the ID of its `[P, M, P']` claim |

A table is mapped (`os_map_read`) when a probe first needs it and is never read whole. At most `max_open` tables are mapped at once (64 by default), and the least recently used one no probe holds is unmapped first. A 5-piece pawn position's line maps only the tables its probes reach: ten for `8/4k3/8/8/8/3PK3/8/2R2r2 w`, and the same line comes out with two mapped at most (`laplace tablebase -n 2`).

`laplace tablebase [-T tables] [-n open] [--line | --pgn] FEN...` prints the read ([CLI](../Reference/CLI.md#laplace-tablebase)). Laplace-MCP answers its native read `/v1/chess_tablebase {fen}` and the web host's `GET /api/chess/tablebase?fen=` from the same probe:

```text
{position, tables, covered, wdl, dtz,
 moves: [{san, uci, position, claim, wdl, dtz, value, zeroing, mate, recorded}],
 line: {id, result, plies: [{san, uci, position, claim, recorded}]} | null,
 claims, database}
```

The database is read beside the probe, in one containment probe of the position and the line's positions: `recorded` is the standing of a move's or ply's transition where the database holds that claim, and `claims` counts the claims that hold the position. Without a database the read answers from the tables alone.

## What is recorded: endings

The recipe (`lines.recipe`) says `grammar pgn`, `records played` and `input decode syzygy` ([Recipes](../Reference/Recipes.md)). The decoder (`src/chess_syzygy.c`) works once a run, when the first table is opened:

1. It reads the database the ingest loads into, through the Engine's reader. It takes the trunks of the sources whose recipes read chess (`grammar pgn`, or a part read by it) and walks down a level at a time to their records, the vertices said `RECORD`.
2. From each record it finds the line the record holds, at most three levels down. A line is a composition of an odd number of constituents, at least three, whose first and last are positions. Only a path's ends and length cross the socket (`ends_of`).
3. It decodes the last position of each line. For each line that ends within the tables' pieces, it decodes every position of the line. A position is decoded from its constituents by the IDs `chess_rules.c` composes, and each is checked by composing its ID again. A position with castling rights is in no table.
4. From each reached position it probes the best-play line. A drawn position has none. A line another reached position's line holds from its start on, with the same result, is that line's tail and is not written again.
5. Each table's file is then the lines that begin in its material, either colouring, in their positions' ID order.

A line is written as the PGN a game of it is, its start a FEN tag of the position's four fields and its result under the 50-move rule, a cursed win or a blessed loss a draw:

```text
[FEN "7k/1Q6/8/8/8/8/8/K7 b - -"]

1... Kg8 2. Kb2 Kh8 3. Kc3 Kg8 4. Kd4 Kh8 5. Ke5 Kg8 6. Kf6 Kh8 7. Qg7# 1-0
```

`chess.c` reads it as it reads every game ([Chess](../Sequence/Chess.md)): the record `[line, [FEN, text]]`, its line `[P0, M0, P1, …, P12]`, and for each move the `[P, M, P']` claim a game that plays it records, scored for the side that moves (1 for White's moves here, 0 for Black's), attested by the Syzygy trunk. The IDs, from the Engine's `tests/syzygy-tablebase.sh`:

| | ID |
| --- | --- |
| P0, `7k/1Q6/8/8/8/8/8/K7 b`, a loss in 12 | `ba7239ecffb26a06aca87a451b8fea07` |
| the line `[P0, M0, …, P12]` | `6554c79ccee9acdcb4aa4adfa1b4a6d3` |
| the first transition, `[P0, Kh8-g8, P1]` | `ac29dc80b021cf10a8981eff93aff99b` |
| the last, `Qg7#` | `af54408d836efc56137dcc45c70a0f9e` |

P0 is the position after `1. Qxb7` in the Engine's `reaches.pgn`, a game that takes Black's last pawn, and that game's `1... Kg8` is the tables' move: the game and the tablebase line claim one transition, by identity alone.

## What the substrate shares

Content addressing shares whatever lines hold in common, and the source writes nothing but lines:

- A tablebase transition is the same claim a game records when it plays that move, so the tables' lines converge with the games that stand on them, and each transition's standing gathers both kinds of witness.
- Lines converge with one another. Best play from a position is a function of the position, so two lines that meet share every position, move and transition from there on. A line wholly the tail of another reached position's line is not written.
- Positions, boards, `[piece, square]` pairs, squares and moves are one entity wherever they stand.

Eight lines from the positions the Engine's checks probe hold 161 plies. Read into an empty node table they make 866 compositions, about five a ply, with 240 reused within them. What the source adds therefore grows with the positions recorded games reach, not with the tables. The tables themselves hold 3,891,168 legal positions in the five 3-piece tables, counted by the former decoder that wrote them all, and about $1.1 \times 10^9$ in the 30 4-piece tables and $2 \times 10^{11}$ in the 110 5-piece tables, counting placements with about 80% legal as in the 3-piece tables. Every one of those verdicts is a read, and none is a row.
