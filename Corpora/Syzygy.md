# Syzygy

The Syzygy endgame tablebases attest every position of three to five pieces its win/draw/loss and its distance to zeroing, each a claim of the position a game holds when it stands there.

## Source

| Source | Packaging | Recipe |
| --- | --- | --- |
| `syzygy` | Syzygy tables, `NAME.rtbw` (WDL) and `NAME.rtbz` (DTZ), the 3-4-5 piece set of the lichess mirror (`tablebase.lichess.ovh/tables/standard/3-4-5-wdl`, `3-4-5-dtz`; `files-345.txt` lists them) | [Syzygy](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/syzygy) |

The witness is the tablebase, one trunk; its class is `StandardsDerived`, the class [`trust_classes.toml`](https://github.com/SaltyPatron/Laplace-Native/blob/main/manifest/trust_classes.toml) gives tablebases. The files are kept under `$LAPLACE_DATA/Games/Chess/syzygy/<set>/`. Every table a probe reaches must be in the same directory: a capture in KQvKR leaves KQvK, KRvK, KvKR or KvK.

## Format

A table is not a list of positions. It is an index over the placements of its material, folded by the board's symmetries (8 for a pawnless table, the left-right mirror for one with pawns) and compressed with pair encoding; the values are right only where no capture decides the position, and a DTZ table holds one side to move. One table answers for its material either way round: KQvK holds KvKQ too. The format is Ronald de Man's ([syzygy-tables.info](https://syzygy-tables.info/metrics)); [Fathom](https://github.com/jdart1/Fathom) (MIT) is the reference prober.

| File | What a position's value is |
| --- | --- |
| `.rtbw` | its result for the side to move under the 50-move rule: win, cursed win (a win the 50-move rule draws), draw, blessed loss (a loss it saves), loss |
| `.rtbz` | its distance to zeroing: the plies to the next capture or pawn move under best play, positive where the side to move wins, negative where it loses, beyond 100 where the 50-move rule turns the result. A probe's DTZ may be one ply more than the true distance where the table rounds |

## Reading

The recipe says `input decode syzygy` ([Recipes](../Reference/Recipes.md)). The Engine's decoder (`src/chess_syzygy.c`) carries over the format's own law from Fathom, its index encoding and pair decompression, and probes every position as the format requires: the captures searched through the tables they reach, then the table. Every move, check and position in that search is the Engine's one chess, `chess_rules.c`. The decoder writes a line per legal position of the material, either colouring, either side to move, the side not to move not in check, a pawn on neither back rank, with each en passant square a pawn of the side to move can take on:

```text
8/8/8/8/8/8/1Q6/K6k w - -   win    (.rtbw; FEN, a tab, the verdict)
7k/1Q6/8/8/8/8/8/K7 b - -   -12    (.rtbz; a draw writes no line)
```

The recipe parts each line and reads the FEN as the position it names (`part fen grammar fen`), the same position a game, an opening or a FEN read anywhere else holds. Its first four fields are the position; no clock or move number is. Each line is one claim of that position, with a relation in the format's own terms:

| Claim | Example (IDs from the Engine's `tests/syzygy-tablebase.sh`) |
| --- | --- |
| `[P, "win/draw/loss", verdict]` | `8/8/8/8/8/8/1Q6/K6k w` is `23177bb0004139c5384d47fafc6f1061`, a win; Black to move there (`2908875bd2c911cdf96348c199b46476`) is a loss |
| `[P, "distance to zeroing", plies]` | `7k/1Q6/8/8/8/8/8/K7 b` (`ba7239ecffb26a06aca87a451b8fea07`), the position after `1. Qxb7` in a game that takes Black's last pawn, is `-12` |

The record of a line is `[P, claim]`. No move is recorded, because the tables give none: a position's best move is a read. The legal moves come from the Engine's chess (`lp_chess_successors`), and the verdict of each position they make is read in the same batch. Laplace-MCP answers `GET /api/chess/tablebase?fen=` with `{position, wdl, dtz, moves: [{san, position, wdl, dtz}]}`, the moves best first.

## What the substrate shares

Content addressing shares whatever two lines hold in common, and nothing else. Measured on the 3-piece tables loaded into a local database:

- A position is recorded once for both of its files. KQvK's DTZ file found all 690,808 of its positions already recorded by its WDL file; it added only its claims and records, 1,381,798 entities, two per line.
- A position's board is shared by its two sides to move, and every `[piece, square]`, verdict word, relation and number is one entity wherever it stands.
- A smaller table's positions are not part of a larger table's. A position is `[board, side, castling, en passant]` and its board is the flat list of `[piece, square]` in square order ([Chess](../Sequence/Chess.md)), so KQvKR's board holds KQvK's pieces but no KQvK board. The verdicts a smaller table would predict are still recorded as the larger table's own claims. The board's layout is the Engine's chess identity, and changing it would change every recorded position's ID.

| File | Lines | New entities | Already recorded |
| --- | ---: | ---: | ---: |
| KQvK.rtbw | 736,904 | 2,658,980 | 106 |
| KQvK.rtbz | 690,808 | 1,381,798 | 690,838 |
| KRvK.rtbw | 798,224 | 2,842,892 | 170 |
| KRvK.rtbz | 753,736 | 1,507,709 | 753,777 |
| KPvK.rtbw | 662,704 | 2,324,368 | 220 |
| KPvK.rtbz | 445,128 | 890,387 | 445,156 |
| KBvK.rtbw | 834,456 | 2,951,528 | 225 |
| KNvK.rtbw | 858,880 | 3,024,803 | 217 |

KBvK and KNvK are draws throughout, so their DTZ files write no lines. "Already recorded" counts the subtrees the load found in the database and did not write again. For a DTZ file these are its positions. For a WDL file they are the few shared pieces of other tables and of recorded games.

Each position costs about 3.6 entities for its WDL line (position, board share, claim, record) and two for its DTZ line. That puts the whole 3-4-5 set beyond any one database. The five 3-piece tables hold 3,891,168 legal positions (counted by the decoder). Counting placements, with about 80% of them legal as in the 3-piece tables, the 30 4-piece tables hold about $1.1 \times 10^9$ positions and the 110 5-piece tables about $2 \times 10^{11}$.
