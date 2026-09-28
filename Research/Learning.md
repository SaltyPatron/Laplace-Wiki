# Learning

Research on how ratings can be updated one matchup at a time, how retrieval compares with knowledge stored in model weights, and what the literature reports about softmax, unlearning, execution feedback, and interpretability.

Numbers marked measured come from a local script; everything else is from the sources.

## Rating one matchup at a time

- Glickman's Glicko paper says a rating period "could be as short as one minute", with ratings then "updated on a game-by-game basis", and recommends a deviation floor of about 30 for frequent competitors. The Glicko-2 paper leaves period length to the administrator.
- Lichess updates Glicko-2 after every game, treating each game as its own rating period, and grows deviation with elapsed time instead (0.21436 periods per day, so deviation rises from 60 to 110 over a year of inactivity). It clamps deviation to [45, 500], caps volatility at 0.1, and uses τ = 0.75.
- Measured, with a reimplementation that reproduces Glickman's worked example:
  - Replaying the same 2,000-game log gave bit-identical ratings: per-matchup updates are deterministic for a given order.
  - Order matters, and recent results weigh most: ten games against a 1500-rated opponent end at 1452 in the order WWWWWLLLLL and at 1548 in the order LLLLLWWWWW.
  - Deviation falls from 350 to 248 after one win, 138 after ten, and 76 after a hundred.

## Matchups as learning updates

Each matchup changes one rating by an amount set by how uncertain it is, the way a training step changes a weight by an amount set by a learning rate:

| Machine learning | One matchup |
| --- | --- |
| One example gives one update | One attestation gives one matchup |
| A per-parameter adaptive learning rate, such as [Adam](https://arxiv.org/abs/1412.6980)'s | The rating deviation: large while a standing is uncertain, small once it is established |
| A per-example weight | The witness's trust, played as the opponent's deviation |
| A reward from a verifier, as in [execution feedback](#execution-feedback) | A win, draw, or loss from a compiler, a test, or a tablebase |
| A Bayesian filter's update of a state estimate | Glicko's update: Glickman derives it as an approximate Bayesian update of a normal prior on the rating |

The differences are in what is updated: one named record rather than a distributed weight, readable and replayable in order, and removable by replaying without it.

## Retrieval instead of weights

| System | Finding |
| --- | --- |
| [kNN-LM](https://arxiv.org/abs/1911.00172) | adding nearest-neighbor retrieval over a datastore lowers perplexity from 18.65 to 15.79 with no extra training |
| [RETRO](https://arxiv.org/abs/2112.04426) | retrieving from a 2-trillion-token database matches GPT-3 with 25 times fewer parameters |
| [Memorizing Transformers](https://arxiv.org/abs/2203.08913) | an 8K-token memory matches a model with 5 times more parameters |
| [infini-gram](https://arxiv.org/abs/2401.17377) | exact n-gram counts reach 47% next-token accuracy and cut perplexity by up to 73% combined with a neural model |

Transformer feed-forward layers themselves behave as key-value memories ([Geva et al. 2021](https://arxiv.org/abs/2012.14913)), and a stored fact can be edited as a rank-one key-value write ([ROME](https://arxiv.org/abs/2202.05262)).

## Softmax

- Softmax limits what a model's output distribution can express ([Yang et al. 2018](https://arxiv.org/abs/1711.03953)).
- Attention concentrates on otherwise meaningless tokens, "attention sinks" ([Xiao et al. 2023](https://arxiv.org/abs/2309.17453)).
- Modern networks are overconfident ([Guo et al. 2017](https://arxiv.org/abs/1706.04599)).

## Unlearning

Exact unlearning is defined as the result of retraining without the removed data. [SISA](https://arxiv.org/abs/1912.03817) approaches it by sharding training, 4.63 times faster than retraining on one dataset, but only 1.36 times faster on ImageNet with a 19.45-point loss in top-5 accuracy. For large language models, exact unlearning is infeasible and published methods are approximate.

## Execution feedback

The strongest code models learn from execution: [CodeRL](https://arxiv.org/abs/2207.01780) uses unit-test results as reward, and [RLEF](https://arxiv.org/abs/2410.02089) raises a 70B model on CodeContests from 27.5 to 40.1. [DeepSeek-R1](https://arxiv.org/abs/2501.12948) and Tülu 3 train with rule-based rewards from checkers and compilers.

## Interpretability

A [review of mechanistic interpretability](https://arxiv.org/abs/2404.14082) and the field's open-problems papers name its limits: scale, completeness, and reconstruction error that remains large and structured even with sparse dictionary learning, the leading method.

## Sources

- Mark E. Glickman. [The Glicko system](http://www.glicko.net/glicko/glicko.pdf) and [Example of the Glicko-2 system](http://www.glicko.net/glicko/glicko2.pdf).
- Mark E. Glickman. [Parameter estimation in large dynamic paired comparison experiments](http://www.glicko.net/research/glicko.pdf). Applied Statistics 48, 1999.
- Diederik P. Kingma and Jimmy Ba. [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980). ICLR 2015.
- Lichess: [Glicko.scala](https://github.com/lichess-org/lila/blob/master/modules/rating/src/main/Glicko.scala), [PerfsUpdater.scala](https://github.com/lichess-org/lila/blob/master/modules/round/src/main/PerfsUpdater.scala), [liglicko2](https://github.com/niklasf/liglicko2).
- The papers linked in each section above.
