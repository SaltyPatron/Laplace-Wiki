# Chess

Glicko-2 ratings computed from observed chess games alone, one game at a time in the order the games were played, predicted over-the-board results better than the official ratings once each player entered at an attested rating. Fitted instead over each player's whole history by played date, with the stated ratings as observations, they predicted as well and came out the same in any order the games arrived in.

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

## Order-free ratings

The replay above depends on the order the games are rated in. Ingested in any other order, Glicko-2 gives other ratings, so a game that arrives late, whether it was played earlier or later than the games already rated, cannot simply be added. A second prototype rated the same players so that the order does not matter, with and without the ratings the games state.

### Method

- **Whole-History Rating.** Each player's strength is a curve over time with a Wiener-process prior, *r*(*t*₂) − *r*(*t*₁) ~ N(0, *w*² |*t*₂ − *t*₁|), one value per day the player played or was observed, fitted to all of the player's games at once by their played dates under the Bradley–Terry model, a draw scoring ½ (Coulom 2008). The log-posterior is strictly concave, so it has one maximum, a function of the set of games and not of their order. It was solved by Newton's method on the whole sparse Hessian, with conjugate gradients preconditioned by each player's own tridiagonal block, where Coulom iterates the same Newton step player by player. A late game changes the problem only through the players in it; the prototype re-solves everything.
- **Observation channels.** What a source states and what is computed from the moves enter as separate Gaussian observations on a player's curve, never merged into one source's claim:
  - **R**, the results of the games.
  - **E**, the Elo the game header states, the source's claim `HAS_RATING`. A number a source repeats in many games is one observation: one per player, stated value, and month, on the first day it was stated.
  - **I**, an intrinsic estimate from move quality, below.
  - A weak prior sits on each player's first day: N(1500, 350²), or N(the weighted mean of the I channel, 350²) when I is the only source of level.
- **Intrinsic estimate.** A simplified version of Regan and Haworth's model (2011). For every turn after move 8 that is not a repetition and is within three pawns either way, Stockfish 19 evaluated the five best moves, and the played move alone when it was not among them (Threads 1, Hash 16 MB, 100,000 nodes a search, a new game before each game). A move's scaled error δ is the integral of d*x* / (1 + |*x*|) from its evaluation to the best move's, in pawns; the proxy is *y* = exp(−(δ/*s*)^*c*); the probabilities solve *p*ᵢ = *p*₀^(1/*y*ᵢ), Σ *p*ᵢ = 1. Simplifications: *c* is fixed at 0.5 (the paper's fitted *c* lies between 0.43 and 0.55); every other legal move takes the fifth move's error; *s* is fitted per player per game on a log grid, as the maximum a posteriori under a weak prior on ln *s* centred on the median of the per-game fits, a prior that uses no rating (without it a game in which every move was the engine's first choice has *s* → 0). The fitted *s* depends on that game's moves alone, on no opponent's rating and no other game. It was calibrated to Elo by regressing ln *s* on the stated Elo, ln *s* = *a* + *b*·Elo, and inverting, with the residual variance a function of the number of turns, cross-fitted in two folds by game ID so that no game is calibrated with its own Elo.
- **Data.** The Week in Chess over-the-board classical games, parsed and deduplicated as above: 194,643 games, 2025-05-10 to 2026-06-22. The most recent 10%, 19,465 games from 2026-06-04, were held out, 19,005 of them with both players' Elo. Each held-out day was predicted by a fit to every earlier day, with the ratings stated on that day's headers, so each method saw what the replay sees.
- **Engine sample.** One training game for each of the 3,098 held-out players who had played before the cut, their most recent, preferring games covering two of them: 2,516 games, 4,783 player-games with at least five scored turns.
- **Tuning.** *w*² and the E channel's deviation were chosen on the games from 81% to 90% of the pool: *w*² = 8 Elo² a day (2, 8, and 30 were tried; the Brier scores differed by at most 0.0003), and a deviation of 200 for the stated Elo (50, 100, 200, and 400 were tried, at *w*² = 8: 0.1610, 0.1556, 0.1546, 0.1577).

### Results

Brier score on the held-out games, lower is better:

| Method | Order-free | All 19,005 | Both players with an intrinsic estimate, 14,143 | Decisive games, 15,328 |
| --- | --- | --- | --- | --- |
| Always ½ | yes | 0.2016 | 0.2015 | 0.2500 |
| FIDE, the header Elo | — | 0.1647 | 0.1708 | 0.1928 |
| Glicko-2, cold start | no | 0.1682 | 0.1634 | 0.2012 |
| Glicko-2, first attested rating | no | **0.1520** | 0.1561 | **0.1791** |
| WHR: I | yes | 0.2127 | 0.2140 | 0.2580 |
| WHR: E | yes | 0.1645 | 0.1704 | 0.1938 |
| WHR: R | yes | 0.1637 | 0.1594 | 0.1954 |
| WHR: R + I | yes | 0.1642 | 0.1596 | 0.1960 |
| WHR: R + E | yes | 0.1521 | **0.1552** | 0.1793 |
| WHR: R + E + I | yes | 0.1521 | **0.1552** | 0.1794 |

- With stated Elo, the whole-history fit predicted as well as the first-attested Glicko-2 replay, 0.1521 against 0.1520, and both beat FIDE's ratings, 0.1647. The fit reads every stated rating, each once, where the replay reads only the first.
- With no Elo at all, from results alone, the whole-history fit, 0.1637, beat the cold-start replay, 0.1682, and FIDE's ratings, 0.1647.
- The intrinsic estimates added nothing to the prediction: R + I scored 0.1642 against R's 0.1637, and I alone scored worse than always predicting ½. From one game a player the estimate is too noisy: ln *s* correlated with the stated Elo at −0.31 per player-game, and the inverted calibration has a deviation of 836 Elo at 10 scored turns, 691 at 23 (the median), 637 at 40, and 597 at 80. The median *s* still fell with Elo, as the paper's did: 0.31 at 1400–1599, 0.26 at 1600–1799, 0.23 at 1800–1999, 0.21 at 2000–2199, 0.16 at 2200–2399, 0.11 at 2400–2599, 0.11 at 2600–2799.
- Without metadata, what the intrinsic channel supplied is the scale. Results fix only differences, so results alone put held-out players 566 below their stated Elo on average. With the intrinsic estimates the offset was 162, and 113 for the players who had one.

Each held-out player's rating at their first held-out game, against the Elo stated in that game:

| Channels | Players | Mean difference | Root mean square | Correlation |
| --- | --- | --- | --- | --- |
| R | 4,056 | −566 | 594 | 0.74 |
| I | 4,056 | +92 | 285 | 0.25 |
| R + I | 4,056 | +162 | 246 | 0.72 |
| R + I, players with an intrinsic estimate | 2,981 | +113 | 169 | 0.84 |
| R + E | 4,056 | −71 | 98 | 0.97 |
| R + E + I | 4,056 | −69 | 97 | 0.97 |

### Order

The 175,178 training games were rated in the order they were played, in three shuffled orders, in reverse, and with a tenth of them, chosen by content hash, arriving after all the rest. Differences in Elo from the played order, over the 15,183 players:

| Arrival order | WHR R + E: largest difference | WHR: players moved over 1 | Glicko-2, first attested: largest difference | Mean difference | Players moved over 1 |
| --- | --- | --- | --- | --- | --- |
| Shuffled, seed 1 | 1.4 × 10⁻⁹ | 0 | 279 | 13.3 | 12,299 |
| Shuffled, seed 2 | 1.0 × 10⁻⁹ | 0 | 273 | 13.3 | 12,277 |
| Shuffled, seed 3 | 1.1 × 10⁻⁹ | 0 | 257 | 13.4 | 12,358 |
| 10% late | 1.4 × 10⁻⁹ | 0 | 151 | 4.6 | 8,306 |
| Reversed | 1.0 × 10⁻⁹ | 0 | 425 | 13.4 | 12,893 |

- The whole-history ratings were the same in every order to within 1.4 × 10⁻⁹ Elo, the solver's tolerance, although the solver numbered the players' days in arrival order.
- The Glicko-2 replay moved most players. Trained in shuffled order, its held-out Brier went from 0.1520 to 0.1539; with 10% of the games late, to 0.1523.
- The engine analysis is a function of each game alone. 20 games analysed again on hart-server in reverse order, once with two processes and once with one, gave output identical to each other and to the analysis on HART-DESKTOP, all 1,529 turns, from Stockfish 19 built for Linux and for Windows.

### Cost

- The engine analysis of the 2,516 games, 179,815 turns and 26,555 further searches for a played move outside the top five, took 56 minutes on 8 processes at idle priority on HART-DESKTOP, about 10.7 core-seconds a game.
- Inferred, not measured: the whole pool of 194,643 games at that rate is about 580 core-hours, about two days on hart-server's 12 threads if it had them to itself.
- One whole-history fit of the training games, 136,534 player-days, took 4.5 to 6.7 seconds on hart-server at the lowest priority while a reseed loaded it; fitting the intrinsic model to the 4,783 player-games took about 8 minutes there, in Python.
- Scripts: Laplace-Prototype `chess/order_free.py`, `whr.py`, `intrinsic.py`, `analyze.py`, `select_games.py`, `glicko2.py`, and `pool.py`; the run's output is in `chess/results/`, and the games, analysis, and per-game predictions are on hart-server under `/vault/Data/LaplacePrototype/chess-order-free/`.

### What this does not settle

- Inferred, not measured: intrinsic estimates would carry weight only over many games a player. Regan and Haworth fitted thousands of turns per rating level; one game gave a median of 23 scored turns.
- Inferred, not measured: the stated Elo being worth a deviation of 200 rather than 50 says the header is a lagging, monthly witness of a player's strength on the day, not that it is wrong.
- Whether a player's rating over time is a quantity of its own, solved over a whole history, or the standing of a claim played first in, first out, is open: [30. Conflicts](../Sequence/Conflicts.md) R4.

## Sources

- Mark E. Glickman. [Example of the Glicko-2 system](http://www.glicko.net/glicko/glicko2.pdf) and [Parameter estimation in large dynamic paired comparison experiments](http://www.glicko.net/research/glicko.pdf).
- Lichess rating implementation: [Glicko.scala](https://github.com/lichess-org/lila/blob/master/modules/rating/src/main/Glicko.scala) and [scalachess glicko](https://github.com/lichess-org/scalachess/tree/master/rating/src/main/scala/glicko).
- Kenneth W. Regan and Guy McC. Haworth. [Intrinsic Chess Ratings](https://cse.buffalo.edu/~regan/papers/pdf/ReHa11c.pdf). AAAI 2011.
- Rémi Coulom. [Whole-History Rating: A Bayesian Rating System for Players of Time-Varying Strength](https://www.remi-coulom.fr/WHR/WHR.pdf). Computers and Games 2008.
- See [Learning](Learning.md#rating-one-matchup-at-a-time) for per-game Glicko-2 in general.
