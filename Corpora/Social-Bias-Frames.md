# Social Bias Frames

Social Bias Frames attests per-worker and post-aggregated offense, intent, lewdness, targeted-group, and implied-stereotype social-bias risk annotations on social media posts under one corpus trunk, feeding the `RISK` and `consensus` planes (`BELIEF ≠ RISK ≠ ACTION`).

The source is v2 of the Social Bias Frames / Social Bias Inference Corpus (Sap et al. 2020): social media posts annotated by crowd workers with structured pragmatic frames explaining whether a post is offensive, intentional, lewd, whom it targets, and what stereotype it implies, plus per-post aggregations. Two recipes read the per-worker splits and the aggregated splits.

## Source

| Source | Witness | Trust class | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `social-bias-frames` | `Social Bias Frames` source trunk | class `AcademicCurated` | `unicode`, `iso-639` | `SBIC.v2.trn.csv`, `SBIC.v2.dev.csv`, `SBIC.v2.tst.csv`; `SBIC.v2.agg.*.csv` | [`annotations.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/social-bias-frames/annotations.recipe), [`aggregated.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/social-bias-frames/aggregated.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior bounds the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

Every file is RFC 4180 quoted CSV with a header row; unnamed leading row-index columns and empty fields attest nothing. `Social Bias Frames` is the sole corpus witness trunk; hashed `WorkerId` strings are participant content (`content WorkerId`), never separate witnesses ([30. Conflicts](../Sequence/Conflicts.md) I3).

## The annotations (`SBIC.v2.{trn,dev,tst}.csv`)

Each row is one worker's structured bias-frame reading of one `post`. `HITId` is MTurk's task pointer to the post, resolved at ingest and recorded nowhere (`key row HITId`). Under the Recording Law ([INVENTOR_RECORD](../Repositories/Laplace/docs/INVENTOR_RECORD.md)), `offensiveYN`, `intentYN`, `sexYN`, and `whoTarget` supply **scored harm/bias/risk attestations** feeding the `RISK` and `consensus` planes rather than blind `WIN` string literals.

| Piece | Laplace reads it as | Target attestation & current recipe state | Specification |
| --- | --- | --- | --- |
| `HITId` | MTurk task pointer to the post (`key row HITId`), recorded nowhere | none | "id that uniquely identifies each post" |
| `WorkerId` | participant content identifying the worker | qualifier (`with WorkerId`) on the worker's judgments and subject (`of WorkerId`) of worker demographics | "hashed version of the MTurk workerId" |
| `post` | the subject: the social media post, as decoded UTF-8 text | canonical post entity | "post that was annotated" |
| `dataSource` | origin corpus/subreddit of the post | `[post, source of the post, value]` | "source of the post" |
| `offensiveYN`, `intentYN`, `sexYN`, `whoTarget` | worker's coded `[0, 0.5, 1]` answers on offensiveness, intent to offend, sexual/lewd content, and group vs. individual targeting | target: scored harm/risk attestations on `post` qualified `with WorkerId` feeding `RISK` / `consensus` (`Batch 2` recipe gap: currently held in the row without scored risk emission) | "could the post be offensive to anyone"; "was the intent behind the statement to offend"; "is the post a sexual or lewd reference"; "group vs. individual target" |
| `sexReason`, `sexPhrase` | free-text explanation and span of sexual/lewd content | attested of `post` qualified `with WorkerId` | "free text explanations of what is sexual"; "part of the post that references something sexual" |
| `speakerMinorityYN` | in-group speaker indicator | attested of `post` qualified `with WorkerId` | "whether the speaker was part of the same minority group that's being targeted" |
| `targetMinority`, `targetCategory` | demographic subgroup and high-level category targeted | `[post, demographic group targeted, value]`, `[post, high-level category of the demographic group(s) targeted, value]` qualified `with WorkerId` | "demographic group targeted"; "high-level category of the demographic group(s) targeted" |
| `targetStereotype` | implied biased proposition | `[post, implied statement, text]` qualified `with WorkerId` (never asserted as a factual `BELIEF` claim!) | "implied statement" |
| `annotatorGender`, `annotatorMinority`, `annotatorPolitics`, `annotatorRace`, `annotatorAge` | worker demographics attested of `WorkerId` | `[WorkerId, demographic_relation, value]` | demographics of the MTurk worker |

## The aggregation (`SBIC.v2.agg.*.csv`)

Each row aggregates annotations per `post`: `targetMinority`, `targetCategory`, and `targetStereotype` are JSON string arrays (`part ... by json`), and `whoTarget`, `intentYN`, `sexYN`, and `offensiveYN` are mean rater scores in `[0, 1]`.

| Piece | Written as | Laplace reads it as | Target attestation & current recipe state | Specification |
| --- | --- | --- | --- | --- |
| `post` | string | the subject: the post, as decoded UTF-8 text | canonical post entity | |
| `targetMinority`, `targetCategory`, `targetStereotype` | JSON string arrays `["a", "b"]` | unpacked strings attested of `post` under their semantic relations | `[post, implied statement, stereotype]`, etc. | "To load the list of implications, use `json.loads`" |
| `whoTarget`, `intentYN`, `sexYN`, `offensiveYN` | floats in `[0, 1]` | mean worker scores across the post's annotations | target: scored `RISK` attestations (`LP_OUTCOME_SCORE` in `[0, 1]`) on `post` (`Batch 2` recipe gap: `aggregated.recipe` currently keeps these means unattested in the row) | mean over the post's annotations |
| `dataSource` | string | origin corpus of `post` | `[post, source of the post, value]` | |
| `hasBiasedImplication` | `0` or `1` | derived indicator `(len(targetStereotype) == 0)` (`omit`) | none (redundant with `targetStereotype`) | computed in the publisher's README script |
| unnamed first column | row number | internal CSV row index, ignored | none | |

## Relations

`annotations.recipe` and `aggregated.recipe` already map `targetMinority`, `targetCategory`, `targetStereotype`, and `dataSource` onto Sap et al. (2020)'s semantic relations under the single `Social Bias Frames` trunk, keeping implied stereotypes strictly as bias-frame attributions rather than true world claims. Closing the `Batch 2` gap wires the `[0, 1]` offense, intent, lewdness, and targeting scores onto the `RISK` and `consensus` planes.
