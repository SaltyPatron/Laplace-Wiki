# Relations Research

Research into rating models, evidence counts, search over rated relations, truth discovery, and provenance is background for Laplace's semantics layer.

> [!NOTE]
> This page was written before the inventor specified [Semantics](../Semantics/README.md), and it is kept as background. Where it differs from the specification, the specification holds:
>
> - Consensus is updated inline as content is observed, witnesses first in, first out. There are no global or delayed rating periods, ingest epochs, or batch folds of evidence counts; one witness's repeats of one claim are its run length, read off the tree and carried as the certainty of one matchup per strand per ingestion, never played as separate games.
> - A new witness or claim enters at a stock default for its level of attestation, not at a fixed 1500 ± 350 or a fixed anchor.
> - Normal content gives observations only; curated corpora give attestations.
>
> Anything described here as an option or mapping is a research suggestion, not a Laplace decision.

## Conventions

- **Measured**: computed by a local research script (a Glicko-2 implementation that reproduces Glickman's published example) or counted in a locally held dataset.
- **From the source**: quoted from the cited paper, with no marking.
- **Estimate** or **suggestion**: reasoning from the research, marked where it appears.

## Glicko-2

### Concepts

Glickman's rating systems ([The Glicko system](http://www.glicko.net/glicko/glicko.pdf); [Example of the Glicko-2 system](http://www.glicko.net/glicko/glicko2.pdf)) give each player three values:

| Value | Meaning |
| --- | --- |
| Rating `r` | The best estimate of strength. Elo is a special case of Glicko. |
| Rating deviation `RD` | The uncertainty of `r`, a standard deviation; a 95% interval is `r ± 1.96·RD` (Glicko-2's note uses `r ± 2·RD`). "Game outcomes always decrease a player's RD, and time passing without competing … always increases a player's RD." |
| Volatility `σ` (Glicko-2 only) | The expected fluctuation of the rating: high after erratic results, low for consistent performance. |

All games in a rating period are treated as simultaneous, and the update happens at the end of the period. Glicko-2 works best with at least 10–15 games per player per period. Rating changes are not zero-sum: a win against a player with a very uncertain rating teaches little. Glickman advises a floor on `RD` (for example 30) so that a very active player's rating can still move.

The theory is a state-space model for paired comparisons with approximate Bayesian filtering ([Glickman 1999](http://www.glicko.net/research/glicko.pdf); [Glickman 2001](http://www.glicko.net/research/dpcmsv.pdf)).

### The Glicko-2 update

```text
Initialise:  r = 1500, RD = 350, σ = 0.06; system constant τ typically 0.3–1.2
Scale:       μ = (r − 1500) / 173.7178,   φ = RD / 173.7178        (173.7178 = 400 / ln 10)
Helpers:     g(φ) = 1 / sqrt(1 + 3φ²/π²)
             E_j  = 1 / (1 + exp(−g(φ_j)(μ − μ_j)))
Variance:    v = [ Σ g(φ_j)² E_j (1 − E_j) ]⁻¹
Improvement: Δ = v Σ g(φ_j)(s_j − E_j)
Volatility:  σ' solves f(x) = 0 by the Illinois method, where
             f(x) = e^x(Δ² − φ² − v − e^x) / (2(φ² + v + e^x)²) − (x − ln σ²) / τ²
Pre-period:  φ* = sqrt(φ² + σ'²)
Update:      φ' = 1 / sqrt(1/φ*² + 1/v)
             μ' = μ + φ'² Σ g(φ_j)(s_j − E_j)
Convert:     r' = 173.7178 μ' + 1500,   RD' = 173.7178 φ'
```

- `μ` is on the natural log-odds scale: against an opponent with `μ_j` and `φ_j → 0`, the win probability is the logistic `σ(μ − μ_j)`.
- Precisions add: each game adds information `1/v`, so `RD` shrinks.
- In an inactive period only the pre-period step applies: `φ' = sqrt(φ² + σ²)`, with `μ` and `σ` unchanged.
- Glickman's worked example (1500/200/0.06 against 1400/30 win, 1550/100 loss, 1700/300 loss, `τ = 0.5`) gives `r' = 1464.06`, `RD' = 151.52`, `σ' = 0.05999`. The local script reproduces 1464.05 / 151.52 / 0.0600 (measured).

### Mapping onto relations

| Glicko assumption | Relation counterpart | Fit |
| --- | --- | --- |
| Two rated players play a game | A relation against what? | Poor: an opponent has to be supplied (see [Framings](#framings)) |
| Outcome of 0, ½, or 1, with both outcomes possible | An attestation counts as a win | Weak: texts rarely state that "X does not cause Y", so evidence is overwhelmingly positive |
| Games are independent | Attestations | Violated by copying and syndication (see [Truth discovery](#truth-discovery)) |
| Skill drifts over time | Facts can change (Pluto was reclassified in 2006) | Good for volatile facts; less so for stable ones, which should not grow uncertain because nobody repeated them in a period |
| 10–15 games per period | Attestations per ingest epoch | Most relations are long-tail, with one or two attestations |
| The order of periods matters | Content-addressed, re-ingestable data | In tension (see [Order dependence](#order-dependence)) |

The vocabulary maps directly: rating as consensus strength, `RD` as how well witnessed a relation is, `σ` as how contested or volatile it is, and the rating period as an ingest epoch.

### Order dependence

The same 1,013 outcomes (about 92% wins against a fixed anchor), with the same prior, give different ratings depending only on how they are split into rating periods (measured):

| Outcomes per period | `r` | `RD` | `σ` |
| --- | --- | --- | --- |
| 1,013 (one period) | 1795.7 | 11.0 | 0.0600 |
| 13 | 1942.4 | 42.6 | 0.0591 |
| 1 | 1950.8 | 82.3 | 0.0600 |

The maximum-likelihood logit of the win rate corresponds to `r = 1933.9` (measured).

- Glicko-2 makes one linearised step from the prior per period. A single large batch under-moves `μ` while `RD` collapses, and after that the rating barely moves.
- The equilibrium `RD` depends on the period length, because `σ²` is added once per period.
- Ingesting the same corpus in a different order or in different chunks therefore gives different ratings.

The research suggests one way to keep Glicko-2's vocabulary while making the result independent of ingestion order (suggestion): store per-relation evidence counts, which add, merge, and deduplicate regardless of order, and derive `(μ, φ)` from them on the same log-odds scale, with a `σ`-like inflation per epoch if decay over time is wanted. For a Beta posterior with counts `α` and `β`, `E[logit p] ≈ ψ(α) − ψ(β)` and `φ ≈ sqrt(ψ₁(α) + ψ₁(β))`, where `ψ` and `ψ₁` are the digamma and trigamma functions.

### Other rating models

| Model | State per relation | Uncertainty | Time decay | Independent of order |
| --- | --- | --- | --- | --- |
| Elo | `r` | None | None | No |
| Glicko | `r`, `RD` | Yes | `c²t` inflation | No |
| Glicko-2 | `μ`, `φ`, `σ` | Yes | Driven by `σ` | No |
| [TrueSkill](https://papers.nips.cc/paper_files/paper/2006/file/f44ee263952e65b3610b8ba51229d1f9-Paper.pdf) | Gaussian `μ`, `σ` | Yes | Additive dynamics | No; online message passing. Handles multi-way rankings, so one source ranking several candidates is one game. A Microsoft trademark and patent. |
| Beta-Bernoulli | Weighted positive and negative counts `α`, `β` | Exact posterior | Exponential forgetting per epoch | Yes: counts add |
| Dirichlet-multinomial | A count per alternative | Yes | Forgetting | Yes |
| Truth discovery (KBT, CATD) | Claim probability and source accuracy | CATD gives source confidence intervals | — | Iterative, deterministic given the data |

### Ratings and model weights

Neural-network weights are distributed, learned parameters that are not attached to any single fact. A relation's rating is an explicit, counted statistic per edge. Ratings have precedent as replacements for knowledge-graph edge weights, such as ConceptNet's `weight` or Knowledge Vault's confidence. Scoring unseen combinations is a separate problem: [Knowledge Vault](https://www.cs.ubc.ca/~murphyk/Papers/kv-kdd14.pdf) used learned priors for it (path ranking and a neural link predictor), which alone reached an AUC of 0.884 and 0.882, and 0.911 fused, against 0.927 for the fused extractors; priors and extractors together did better still.

## Evidence counts

### The worked example: smoking causes cancer

ConceptNet 5.7, held locally, has these edges from `smoking` (measured):

| Edge | Sources | Weight |
| --- | --- | --- |
| `/r/Causes` smoking → cancer | 12 | 5.657 |
| `/r/Causes` smoking → lung cancer | 13 | 7.483 |
| `/r/CapableOf` smoking → cause lung cancer | 2 | 2.0 |
| `/r/UsedFor` smoking → causing cancer | 1 | 1.0 |
| `/r/UsedFor` smoking → getting cancer | 1 | 1.0 |

- The 12 and 13 sources are Open Mind Common Sense contributors and votes.
- The `UsedFor` edges are mistyped relations.
- In all, eleven distinct edges express essentially one idea. Content addressing merges identical content, not paraphrases, so merging paraphrases would fall to the Relations layer.
- The weights look square-root scaled (5.657 = √32, 7.483 = √56). This is an observation from the data, not documented by ConceptNet in the sources here.

### Framings

Glicko needs an opponent. The research considered three (suggestions):

- **A null anchor.** The relation is the player; the opponent is a fixed anchor at 1500 with `RD` 30, standing for "no better than chance" or a base rate. Each independent witness asserting the relation is a win; each contradicting witness, such as a `NotCauses` edge, is a loss. Because `μ` is log-odds, `σ(μ − μ_anchor)` reads directly as a confidence.
- **Competing alternatives.** The players are the candidates for one slot, such as the relation types between smoking and cancer (`Causes`, `UsedFor`, `CapableOf`). A source asserting A where it could have asserted B is a win for A. This ranks outgoing edges, which is what search and top-k expansion need. For relations that are not exclusive (smoking causes cancer and heart disease), treating "A asserted, B not asserted" as a loss for B confuses absence with negation; Knowledge Vault's local closed-world assumption is the standard compromise.
- **The source as the opponent.** This rates sources rather than claims, which the joint source-and-claim models of [truth discovery](#truth-discovery) express directly.

Results of the null-anchor framing for one rating period (measured):

| Evidence | `r` | `RD` | P(win against anchor) | `p_low = σ(μ − 2φ)` | Cost `−ln p_low` |
| --- | --- | --- | --- | --- | --- |
| 12 independent witnesses, 1 contradiction | 1774.3 | 93.3 | 0.819 | 0.624 | 0.472 |
| 1,000 verbatim copies counted as 1,000 wins, plus 1 loss | 1848.0 | 11.0 | 0.880 | 0.867 | 0.143 |
| The same copies counted as 1 witness | 1675.1 | 247.2 | 0.688 | 0.137 | 1.986 |

- From 1774.3 / 93.3 with `σ = 0.06`, empty periods grow `RD` to 93.9 after one, 98.9 after ten, and 139.9 after a hundred (measured).
- A Beta-Bernoulli model with a Beta(1,1) prior gives a mean of 0.867 (sd 0.085) for 12 positives and 1 negative, and 0.998 (sd 0.0014) for 1,000 positives and 1 negative (computed).
- In both models, counting copies as witnesses makes the relation look almost certain. How copies are counted changes the result more than the choice of rating system does, and it changes the search cost by an order of magnitude.

## Search over rated relations

### A* definitions

A* orders its search by `f(n) = g(n) + h(n)`: the cost so far plus an estimate of the remaining cost ([Hart, Nilsson & Raphael 1968](https://ai.stanford.edu/~nilsson/OnlinePubs-Nils/PublishedPapers/astar.pdf)).

- **Admissible**: `h(n)` never exceeds the true remaining cost. The first goal expanded is then optimal.
- **Consistent**: `h(n) ≤ c(n, m) + h(m)` for every edge, and `h(goal) = 0`. Consistent implies admissible, and no node is expanded twice.
- In [Goldberg & Harrelson's](https://www.cs.princeton.edu/courses/archive/spr06/cos423/Handouts/GH05.pdf) formulation, a potential `π` is feasible when every reduced cost `ℓ(v, w) − π(v) + π(w)` is non-negative. Feasible is the same as consistent, and the maximum of feasible potentials is feasible.

### Edge cost

A cost from ratings (suggestion):

```text
p(e) = σ(μ_e − μ_anchor − k·φ_e)       k = 2 gives roughly a 97.7% lower bound
c(e) = −ln p(e) + λ                     λ ≥ 0 is an optional per-hop constant
```

- Costs are non-negative, so Dijkstra and A* are exact, and the cheapest path is the chain with the largest product of edge confidences.
- Using the pessimistic side of the rating penalises poorly witnessed edges.
- A per-hop constant `λ` prefers shorter explanations and gives every edge a minimum cost `c_min`, which heuristics can use.
- Ratings change, so costs change. A heuristic computed under an optimistic cost `c_opt(e) ≤ c(e)`, such as `−ln σ(μ + 2φ) + λ` or simply `λ`, stays admissible and consistent for `c`, because reduced costs only grow when `c ≥ c_opt`. Precomputed bounds then survive rating updates until an edge's cost could fall below its `c_opt`.

### Heuristics

**Landmarks (ALT).** Precompute distances to and from a small set of landmarks `L`. The triangle inequality gives `d(v, t) ≥ max over L of max(d(v, L) − d(t, L), d(L, t) − d(L, v))`, which is consistent on directed graphs ([Goldberg & Harrelson](https://www.cs.princeton.edu/courses/archive/spr06/cos423/Handouts/GH05.pdf); [Goldberg & Werneck](https://www.cs.princeton.edu/courses/archive/spr06/cos423/Handouts/GW05.pdf)).

- Farthest and planar landmark selection outperform random selection. In practice about 16 landmarks are stored and about 4 are active per query.
- ALT beat A* with Euclidean bounds "by a wide margin on road networks".
- Space is `O(|V| · |L|)` distances. Landmark tables for changing costs would be computed under `c_opt`.

**Geometric distance.** The geodesic distance on the S³, `arccos⟨x, y⟩`, is a metric, and two bounds follow from it:

- Lipschitz: with `α = min over edges of c(e) / d_geo(e)`, `h(v) = α · d_geo(v, t)` is consistent.
- Hops: if no relation edge spans more than `D_max`, `h(v) = c_min · ⌈d_geo(v, t) / D_max⌉` is consistent.

Both are always valid. They are informative only when geometric distance correlates with cost, that is, when strongly rated relations are geometrically short. When positions are derived from content rather than from relations, `α` and `1 / D_max` are small, `h` is close to zero, and A* behaves like Dijkstra: still exact, with no pruning gained. ALT needs no embedding and works on any graph.

**Where A\* applies.** A\* speeds up point-to-point queries: a start, a goal or goal set, and additive costs, such as "is there a credible chain from X to Y?". One-hop top-k lookups, such as "what does smoking cause?", are served by a per-node ordering by rating rather than by a search.

## Truth discovery

### Principles

The [survey by Li et al.](https://arxiv.org/pdf/1505.02463) states the principle: "If a source provides trustworthy information frequently, it will be assigned a high reliability; meanwhile, if one piece of information is supported by sources with high reliabilities, it will have big chance to be selected as truth." Truth discovery can recover a true value held by a minority of sources, which majority voting cannot.

| Family | Examples | Mechanism |
| --- | --- | --- |
| Iterative | Investment ([Pasternack & Roth](https://aclanthology.org/C10-1099.pdf)), TruthFinder, 2-Estimates, 3-Estimates | Claims and sources pass credit back and forth |
| Optimisation | CRH | Minimise the reliability-weighted distance between claims and truths by coordinate descent |
| Probabilistic graphical models | LTM | Claims are generated from the truth and the source's quality; LTM separates false-positive from false-negative rates, which suits relations with several true values |

The common assumptions are that a source is equally accurate across objects, and that sources do not copy one another. Reliability can instead be estimated per website and attribute.

### Long-tail sources

In [CATD](https://www.vldb.org/pvldb/vol8/p425-li.pdf), most sources make only one or two claims, so point estimates of their reliability are unreliable. CATD weights each source by the upper bound of a chi-squared confidence interval on its error variance, which shrinks small sources automatically. It is the source-side counterpart of rating by `r − 2·RD`.

### Knowledge Vault and Knowledge-Based Trust

[Knowledge Vault](https://www.cs.ubc.ca/~murphyk/Papers/kv-kdd14.pdf) (KDD 2014) extracted 1.6B triples, of which 271M have a confidence of at least 0.9, and about a third of the confident triples were new relative to Freebase.

- Fusion uses, per extractor, the square root of the number of sources that yielded the triple, and the mean extraction score. Its footnote: "we perform de-duplication of sources before running the extraction pipelines". Results were similar with `log(1+n)`.
- Probabilities are calibrated by Platt scaling.
- Labels use the local closed-world assumption: a triple absent from Freebase is false if Freebase has other objects for the same subject and predicate, and is excluded otherwise.

[Knowledge-Based Trust](https://arxiv.org/pdf/1502.03519) (VLDB 2015) estimates the accuracy of web sources from the correctness of their facts (2.8B triples, 119M pages, 5.6M sites) rather than from links.

- In its ACCU model each independent source contributes a vote `ln(n·A / (1 − A))`, additive log-odds on the same scale as Glicko-2's `μ`. Four sources with accuracy 0.6 and `n = 10` give 2.7 votes each.
- A multi-layer model separates extractor errors (did the page really say it?) from source errors (is what it says true?).
- Sources form a hierarchy of website, predicate, and page; small sources are merged into their parent and large ones split.
- Detecting copying "at billions of web sources remains an open problem", and KBT itself assumes independence.

### Copy detection

[Dong, Berti-Équille & Srivastava](http://www.vldb.org/pvldb/vol2/vldb09-pvldb47.pdf) (PVLDB 2009): "A false value can be spread through copying." When two sources share many values that few other sources give, one probably copies the other. Detection runs iteratively with truth finding, and a copier's vote counts only for what it did not copy. The survey adds that copiers share mistakes, so the signal fails when the copied source is correct, and that positively correlated sources "should not increase the belief".

## Observations, attestations, witnesses, and consensus

The inventor's vocabulary for relations includes observations, attestations, witnessing, and consensus ([Semantics](../Semantics/README.md)). The research separates four quantities along those lines; the mapping is a suggestion:

| Quantity | Meaning in the research | For 1,000 verbatim copies of one sentence |
| --- | --- | --- |
| Observations | Every place the content occurs | 1,000 |
| Attestations | Distinct statements of the relation: distinct compositions, including paraphrases, that express it | 1 |
| Witnesses | Independent source lineages behind the attestations | About 1, plus any that are shown to be independent |
| Consensus | The aggregate: a reliability-weighted sum of witness log-odds, as in KBT's vote count, mapped to `(μ, φ)` | Driven by witnesses, not observations |

Points from the research:

- Truth discovery has to infer copying from shared rare values. In Laplace, identical content is one node, and its containers list every place it occurs, so exact copies are found directly (see [Corpus Search](Corpus-Search.md#occurrence-counting)).
- Identical text is copy evidence weighted by how unlikely a coincidence is. Two independent authors are unlikely to write the same long sentence, and likely to both write "smoking causes cancer". A suggestion from the research is that the probability of a copy rises with the text's information content.
- Paraphrases are strong evidence of independence: the eleven ConceptNet edges above are more independent evidence than 1,000 identical copies.
- Occurrence count is a signal of salience, not of truth. Knowledge Vault counts sources sub-linearly after deduplication; the research suggests storing occurrences separately from witnesses.
- A KBT-style hierarchy of sources, with CATD-style confidence intervals for long-tail sources, is the published approach to source reliability.

## Provenance

[PROV-O](https://www.w3.org/TR/prov-o/), a W3C Recommendation of 30 April 2013 ([family overview](https://www.w3.org/TR/prov-overview/)), is an exchange vocabulary for provenance.

- Classes: `prov:Entity`, `prov:Activity`, `prov:Agent`.
- Relations: `wasGeneratedBy`, `used`, `wasAttributedTo`, `wasAssociatedWith`, `actedOnBehalfOf`, `wasDerivedFrom`, `wasInformedBy`, and the time properties.
- Subproperties of `wasDerivedFrom`: `wasQuotedFrom`, `wasRevisionOf`, `hadPrimarySource`. These name the copy-dependency between attestations.
- `specializationOf` and `alternateOf`, `Collection` and `hadMember`, and `wasInvalidatedBy` for a retracted or superseded claim.
- Qualified relations, such as `qualifiedDerivation` to a `prov:Derivation` node, carry extra attributes such as extractor confidence.
- `prov:Bundle` is a named set of provenance statements: provenance of provenance, such as "this consensus value was computed by algorithm X over witness set W at epoch t".

A mapping from the research (suggestion):

| Laplace concept | PROV-O term |
| --- | --- |
| Composition node | `Entity`, content-addressed |
| Document or source | `Entity`, attributed to an `Agent` |
| Ingestion or extraction | `Activity` |
| Attestation | `Entity` that `wasDerivedFrom` the sentence, `wasGeneratedBy` the extraction, and `wasAttributedTo` the source |
| Detected copying | `wasQuotedFrom` or `hadPrimarySource` |
| Consensus or rating snapshot | `Entity` generated by an aggregation `Activity` that `used` the attestations, inside a `Bundle` |

Nanopublications, which package an assertion with its provenance and publication information, are a common packaging for attested scientific relations; they were not reviewed here.

## Local datasets

These relation datasets are held locally. All counts are measured from the local copies.

| Dataset | Size | Relation structure |
| --- | --- | --- |
| ConceptNet 5.7 | 10.2 GB, 34,074,917 edges | 50 relation types. Each edge carries its sources (contributors, votes, Wiktionary, DBpedia, and others) and a weight, which makes it the local test bed for witness and consensus modelling. |
| WordNet 3.0 | 49 MB | Synsets: 82,115 noun, 13,767 verb, 18,156 adjective, 3,621 adverb. 377,592 pointers, many stored in both directions. Verb frames and sense frequencies. |
| CILI | 98 MB | 117,659 interlingual concept IDs with English definitions, mapped to WordNet 3.0 and 3.1. An identity and anchor layer, not relations. |
| Open Multilingual Wordnet | 245 MB, about 2.68M lines | 2.11M lemmas, 434K definitions, and 132K examples attached to WordNet 3.0 synsets; relations are inherited through the shared synsets. |
| FrameNet 1.7 | 942 MB | 1,221 frames, 13,572 lexical units, 107 annotated full-text documents. 2,070 frame-to-frame relations and 12,393 frame-element mappings. |
| VerbNet 3.4 | 14 MB | 329 class files, 280 subclasses, 6,740 member verbs, 1,603 syntactic frames. 39 thematic roles and 163 semantic predicates. |
| PropBank frames | 52 MB | 7,566 frameset files, 11,208 rolesets, 23,434 examples, 34,878 role links to VerbNet and FrameNet. No corpus annotations. |
| ATOMIC 2020 | 66 MB | 1,331,113 lines, 1,246,582 unique. 64,569 tuples appear more than once (84,531 extra copies, a natural witness-count test). 147,608 tails are `none`. 23 relations. |

Relation counts:

- **ConceptNet**: ExternalURL 9.74M, RelatedTo 9.13M, Synonym 6.70M, FormOf 3.83M, DerivedFrom 1.05M, HasContext 810K, IsA 611K, EtymologicallyRelatedTo 594K, SymbolOf 389K, EtymologicallyDerivedFrom 283K, AtLocation 109K, Causes 90K, UsedFor 80K, MotivatedByGoal 73K, HasSubevent 72K, Antonym 66K, DistinctFrom 65K, CapableOf 54K, SimilarTo 43K, PartOf 43K, NotDesires 26K, HasPrerequisite 25K, CausesDesire 25K, Desires 25K, HasProperty 22K, HasA 18K, MadeOf 17K, HasFirstSubevent 16K, MannerOf 13K, DefinedAs 11K, ReceivesAction 6K, ObstructedBy 5K, HasLastSubevent 3.4K, NotUsedFor 3.1K, InstanceOf 2.4K, Entails 405, CreatedBy 391, NotCapableOf 329, NotHasProperty 327, LocatedNear 49, and 10 DBpedia relations. The `Not*` relations are the only explicit negative evidence.
- **WordNet pointers**: hypernym and hyponym 89,089 each; derivationally related 74,717; similar to 21,386; member holonym and meronym 12,293 each; part holonym and meronym 9,097 each; instance hypernym and hyponym 8,577 each; pertainym 8,023; antonym 7,979; domain topic 6,654 each way; also see 3,272; verb group 1,750; domain usage 1,376 each way; domain region 1,360 each way; attribute 1,278; substance holonym and meronym 797 each; entailment 408; cause 220; participle 73.
- **FrameNet frame-to-frame**: Inheritance 781, Using 556, ReFraming_Mapping 217, Subframe 131, Perspective_on 127, Precedes 89, See_also 86, Causative_of 60, Inchoative_of 19, Metaphor 4.
- **ATOMIC 2020**: ObjectUse 165,590, xAttr 148,194, xWant 135,360, xNeed 128,955, xEffect 115,124, HinderedBy 106,658, oWant 94,548, xReact 81,397, oEffect 80,166, xIntent 72,677, oReact 67,236, isFilledBy 33,266, isBefore 23,208, isAfter 22,453, AtLocation 20,221, HasSubEvent 12,845, CapableOf 7,968, HasProperty 5,617, MadeUpOf 3,345, NotDesires 2,838, Desires 2,737, Causes 376, xReason 334.

The datasets cross-link: PropBank, VerbNet, and FrameNet through role links; VerbNet to WordNet sense keys; Open Multilingual Wordnet and CILI to WordNet 3.0 synsets. ConceptNet imports WordNet, and ATOMIC's relations overlap ConceptNet's. One grouping the research suggests: a lexical tier (WordNet, Open Multilingual Wordnet, CILI), a predicate-argument tier (PropBank, VerbNet, FrameNet), and a commonsense tier (ConceptNet, ATOMIC).

## Sources

- Glickman, [The Glicko system](http://www.glicko.net/glicko/glicko.pdf).
- Glickman, [Example of the Glicko-2 system](http://www.glicko.net/glicko/glicko2.pdf), revised 2022-03-22.
- Glickman, [Parameter estimation in large dynamic paired comparison experiments](http://www.glicko.net/research/glicko.pdf), Applied Statistics 48, 1999.
- Glickman, [Dynamic paired comparison models with stochastic variances](http://www.glicko.net/research/dpcmsv.pdf), Journal of Applied Statistics 28(6), 2001.
- Herbrich, Minka & Graepel, [TrueSkill: A Bayesian Skill Rating System](https://papers.nips.cc/paper_files/paper/2006/file/f44ee263952e65b3610b8ba51229d1f9-Paper.pdf), NIPS 2006.
- Hart, Nilsson & Raphael, [A Formal Basis for the Heuristic Determination of Minimum Cost Paths](https://ai.stanford.edu/~nilsson/OnlinePubs-Nils/PublishedPapers/astar.pdf), 1968.
- Goldberg & Harrelson, [Computing the Shortest Path: A* Search Meets Graph Theory](https://www.cs.princeton.edu/courses/archive/spr06/cos423/Handouts/GH05.pdf), SODA 2005.
- Goldberg & Werneck, [Computing Point-to-Point Shortest Paths from External Memory](https://www.cs.princeton.edu/courses/archive/spr06/cos423/Handouts/GW05.pdf), ALENEX 2005.
- Li et al., [A Survey on Truth Discovery](https://arxiv.org/pdf/1505.02463), SIGKDD Explorations 2015.
- Li et al., [A Confidence-Aware Approach for Truth Discovery on Long-Tail Data](https://www.vldb.org/pvldb/vol8/p425-li.pdf), PVLDB 8(4), 2015.
- Dong et al., [Knowledge Vault: A Web-Scale Approach to Probabilistic Knowledge Fusion](https://www.cs.ubc.ca/~murphyk/Papers/kv-kdd14.pdf), KDD 2014.
- Dong et al., [Knowledge-Based Trust: Estimating the Trustworthiness of Web Sources](https://arxiv.org/pdf/1502.03519), VLDB 2015.
- Dong, Berti-Équille & Srivastava, [Integrating Conflicting Data: The Role of Source Dependence](http://www.vldb.org/pvldb/vol2/vldb09-pvldb47.pdf), PVLDB 2(1), 2009.
- Pasternack & Roth, [Knowing What to Believe (when you already know something)](https://aclanthology.org/C10-1099.pdf), COLING 2010.
- W3C, [PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/), 2013; [PROV Overview](https://www.w3.org/TR/prov-overview/).
- Cited without a retrieved copy: Yin, Han & Yu, TruthFinder, TKDE 2008.
