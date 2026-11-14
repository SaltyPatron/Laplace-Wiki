# Recording chess state transitions

A recorded line contains its initial position and its ordered typed moves. Each
position composes the complete state needed to reproduce the transition. Board
occupancy alone is insufficient for reserves, castling, en passant, or check-count
objectives. Source PGN remains source testimony; legal replay and analysis are
calculations over it.

The monorepo recording path executes every law the Engine's
`firmware/chess.firmware` declares: standard chess, Chess960, From Position,
Crazyhouse, King of the Hill, Three-check, Atomic, Antichess, Horde and Racing
Kings. Chess960 changes the initial arrangement and designated castling rooks.
Crazyhouse adds pockets, drop actions, and promoted-piece provenance. Three-check
adds the checks delivered by each side. King of the Hill and Racing Kings add the
king's goal squares. Atomic explodes captures, Antichess makes captures compulsory
and the king a piece like any other, and Horde starts White with pawns that step two
from the first rank. A variant name no law declares does not imply executable rules:
the game fails explicitly with its game and source location.

The rules have one implementation, the Engine's `src/chess_rules.c`. `laplace_core`
compiles it from the canonical Engine checkout, and `engine/core/src/chess_board.c`
only carries the managed board's state into it. The firmware names each law as every
source writes it: the PGN Variant tag, Lichess's API key, and the `UCI_Variant`
value. The Lichess bot accepts every variant the firmware declares and tells its
engine the variant through `UCI_Variant`, which Laplace's UCI engine offers as the
conventional combo.

The Engine resolves and replays nonstandard-rule games in one batch.
The existing composition owners emit their state atoms, moves, trajectories and
observations. Stored reconstruction restores rules and state before generating SAN,
FEN, or later analysis. Ordinary-chess tablebases cannot answer other rule sets.

The chess perfcache accelerates these same compositions. The finite alphabet
includes reserve-origin moves, pocket counts, promoted squares and check counters.
A cache miss composes through the canonical owner; it does not reject a valid
state. Standard position and move identities remain unchanged.

## Use the installed monorepo client

From any working directory, with the installed profile selecting runtime and database:

```text
laplace-mono --where
laplace-mono chess record "path to games.pgn"
```

`record` uses the same ingestor as provider imports in the chess UI. It requires
complete source games, persists their observations, verifies exact stored move
trajectories, and reconstructs them through the browsing/analysis reader. Repeating
the same source verifies existing recordings without creating another playing.
The command exits nonzero if any selected game cannot be recorded or reconstructed.
Earlier committed chunks remain available; no whole-file transaction is claimed.

Native comparison against the pinned independent reference is available through
`scripts/verify-native-chess.py --library <library> --pgn <file>
--provider-cache <directory> --output <receipt>`. This compares every legal move
set, resolved SAN, resulting board, pockets, promoted provenance, and counters.
It is separate from the database-backed recording check.

The regression fixtures retain all thirteen nonstandard-rule games from Hikaru's
May 2016 Chess.com archive. They cover composition, analysis and typed reconstruction;
the complete 663-game archive is the installed-client ingestion verification input.

Rule references: [Crazyhouse](https://lichess.org/variant/crazyhouse),
[three-check](https://lichess.org/variant/threeCheck),
[King of the Hill](https://lichess.org/variant/kingOfTheHill), [Atomic](https://lichess.org/variant/atomic),
[Antichess](https://lichess.org/variant/antichess), [Horde](https://lichess.org/variant/horde) and
[Racing Kings](https://lichess.org/variant/racingKings).
