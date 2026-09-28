# Chess

Glicko-2 ratings computed from observed chess games alone, one game at a time in the order the games were played, predicted over-the-board results better than the official ratings once each player entered at an attested rating.

Every number on this page was measured with a prototype script on the local chess corpus.

## The corpus

| Source | Contents |
| --- | --- |
| LumbrasGigaBase | online and over-the-board games, 1900–2026, 18 GB |
| The Week in Chess | 210,500 over-the-board games, 2025–2026 |
| chess.com archives | games of Magnus Carlsen, Hikaru Nakamura, Anish Giri, Alireza Firouzja, Gukesh Dommaraju, Nihal Sarin, Fabiano Caruana, the inventor, and others, with per-move clocks |
| FIDE rating list | a snapshot of the official ratings |
| Opening names | ECO codes and names by move sequence |
| Syzygy tablebases | the exact result of every position with 3 to 5 pieces |

## Method

- The 24 chess.com archive files and the Week in Chess games were parsed, and games were deduplicated by a content hash of the players, date, round, and moves, so a game in two players' archives counts once.
- Games were pooled by platform and game mode. chess.com modes come from the time control (bullet, blitz, rapid, classical, daily); over-the-board modes come from the event name (blitz, rapid, otherwise classical).
- Each pool was replayed in the order the games were played, one game per rating period, with Lichess's settings: τ = 0.75, deviation clamped to [45, 500], volatility capped at 0.1, deviation growing with idle time at 0.21436 periods per day.
- The most recent 10% of each pool's games were scored before each game was rated, against the platform's own ratings on the same games, by Brier score (lower is better).

## Results

With every player entering at the stock default of 1500 ± 350, the computed ratings predicted worse than the platforms' ratings in every pool: most players appear in only a few games and never leave the cold start.

With each player entering at their first attested rating (the platform or FIDE rating in their first observed game) and a deviation of 100:

| Pool | Held-out games | Computed ratings | Platform or FIDE ratings |
| --- | --- | --- | --- |
| Over-the-board classical | 19,008 | **0.1522** | 0.1648 |
| Over-the-board rapid | 830 | **0.1492** | 0.1573 |
| Over-the-board blitz | 695 | 0.1411 | 0.1402 |
| chess.com daily | 38 | **0.1790** | 0.1806 |
| chess.com classical | 46 | 0.1132 | 0.1112 |
| chess.com rapid | 761 | 0.2141 | 0.2074 |
| chess.com blitz | 11,545 | 0.1299 | 0.1186 |
| chess.com bullet | 8,015 | 0.1401 | 0.1282 |

- Over the board, the computed ratings predicted results better than FIDE's ratings on 19,008 unseen classical games. Per-game Glicko-2 reacts faster than FIDE's monthly Elo updates, which accounts for part of the difference.
- On chess.com the computed ratings still trail, because every game header carries chess.com's current rating for both players, and only the first was used. Each header is a fresh attestation.
- Of 422,968 games parsed from 55 files, 8,604 were duplicates removed by content ID, leaving 414,364 distinct games.

## Sources

- Mark E. Glickman. [Example of the Glicko-2 system](http://www.glicko.net/glicko/glicko2.pdf) and [Parameter estimation in large dynamic paired comparison experiments](http://www.glicko.net/research/glicko.pdf).
- Lichess rating implementation: [Glicko.scala](https://github.com/lichess-org/lila/blob/master/modules/rating/src/main/Glicko.scala) and [scalachess glicko](https://github.com/lichess-org/scalachess/tree/master/rating/src/main/scala/glicko).
- See [Learning](Learning.md#rating-one-matchup-at-a-time) for per-game Glicko-2 in general.
