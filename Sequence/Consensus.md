# 13. Consensus

Each attestation, one per strand and witness, is played as one Glicko-2 game series at the witness's trust, as it arrives: its games, how many times the witness asserts the strand, solved on the client as one update, with its score; witnesses play first in, first out, with no global or delayed folds.

Everything attested about a claim, as a whole, provides its overall score: a Glicko-2 standing that tells how hard a strand tugs back. Glicko-2 replaces a lot of conventional AI mechanisms.

## Before this stage

[12. Attestations](Attestations.md): the attestations, in order, each with its witness's trust and outcome.

## Operations, per claim and witness

### 13.1 Find the claim's standing

- **In:** the canonical `claim` `lp_id` from [12. Attestations](Attestations.md) operation 12.6.
- **Do:** same content means the same hash, and deduplication applies directly to claims to form consensus: look up `consensus(claim)` by the claim's composition `lp_id`, whatever its arity. Every witness speaking about that claim folds into the same standing row while its own `(claim, witness, lineage)` series stays inspectable in `attestation`. If none exists, the claim enters at stock default: rating 1500, deviation 350, volatility 0.06. Consensus is not an ad-hoc answer vote; it is the persistent evidence standing read during [20. Forward](Forward.md).
- **Out:** the standing: rating *r*, deviation RD, volatility σ, and matches.
- **From:** [Consensus: Deduplication](../Semantics/Consensus.md#deduplication), [Consensus: Entry](../Semantics/Consensus.md#entry), `docs/specs/05_Substrate_Invariants.txt` Rule #6, [Research: Engine Measurements: Consensus writes](../Research/Engine.md#consensus-writes).

### 13.2 Bound the vote by the witness's trust

- **In:** the witness's trust *t* from [12. Attestations](Attestations.md) operation 12.3.
- **Do:** the witness's trust bounds what its testimony can change; predicate salience is applied at reading by `.firmware` and never enters the fold, because a `HAS_SCRIPT` fact from Unicode is certain and merely low-salience in open chat, and multiplying salience into the vote would record it as uncertain. Trust bounds each series: every game's outcome is pulled toward a draw by the witness's trust, *s*_eff = 0.5 + *t*(*s* − 0.5), so no amount of self-repetition takes a single witness past its trust ceiling, symmetrically for affirmation and refutation and strictly monotone in trust, and one witness alone can shrink deviation only to a per-witness floor; a negative *t* flips the outcome, because being reliably wrong is informative whereas noise is not. **Dependence capping applies strictly to shared causal lineage and Sybil-governed unverified accounts—never across an entire trust class:** independent academic corpora (`UD`, `FrameNet`, `VerbNet`) and independently trained models (`Llama`, `Qwen`, `DeepSeek` at `AIModelProbe`) have distinct causal lineages and genuinely corroborate or challenge one another as a true round table ([24. Models](Models.md) operation 24.10). Meanwhile, ordinary user prompts are observations that emit zero semantic attestations merely by being said ([22. Users](Users.md) operation 22.6), and unverified user feedback accounts are Sybil-bounded under [16. Authority](Authority.md), satisfying the inventor's flat-earth test: round-earth evidence stands above 2000 (*p* ≈ 0.95) while a million flat-earth prompts as observations leave standing untouched and Sybil-capped unverified feedback cannot overturn independent standards and academic witnesses. `Laplace-Native`'s `lp_attest_series` (called in bulk by `laplace_attest_series`) implements trust-bounded series folding directly.
- **Out:** the trust-bounded effective score *s*_eff and per-witness certainty ceiling/floor.
- **From:** [Consensus: Trust](../Semantics/Consensus.md#trust), [Research: Trust: Trust as a Glicko-2 opponent](../Research/Trust.md#trust-as-a-glicko-2-opponent), [30. Conflicts](Conflicts.md) C4.

### 13.3 Check causal lineage (never collapse independent witnesses by trust class)

- **In:** the witness's `lineage` and the claim's existing `(claim, witness, lineage)` rows in `attestation`.
- **Do:** check whether this witness shares a **causal `lineage` / derivation root** with testimony already folded on this claim (for example, Open English WordNet derived from Princeton WordNet under `WordNet` lineage, a ConceptNet edge imported from Wiktionary, or a deterministic calculation repeated under the same analyzer generation, [12. Attestations](Attestations.md) operation 12.11). Witnesses sharing a causal `lineage` fold under that single dependence root so copied sources never masquerade as independent corroboration. **Never cap or merge witnesses merely because they share a `trust_class`:** independent lexicons, independent UD treebanks, and independent frontier models (`Llama + Qwen + DeepSeek`) do not share causal lineage and each plays its own independent series on shared claims.
- **Out:** independent series update for distinct causal lineages; shared-lineage merge when derived from the same upstream root.
- **From:** [Attestations: Witnesses](../Semantics/Attestations.md#witnesses), [24. Models](Models.md) operation 24.10, [30. Conflicts](Conflicts.md) C4.

### 13.4 Play the matchup

- **In:** the standing of 13.1, the trust bounds of 13.2, the witness's outcome on this claim, 1, ½, or 0, or a score *s* in [0, 1] a calculated witness supplies, and its games *n*, how many times the witness asserts the claim.
- **Do:** a claim is a game series: games plus a score, a draw at 0.5. If WordNet says a dog is a noun 30 times, that is one attestation with 30 games. An attestation is one per strand and witness: its games, how many times that witness asserts the strand, and its score. The client folds a source's repeats before the database sees anything, and the database receives one update per strand per witness. One game is Glicko-2's update:

  ```text
  Scale:       μ = (r − 1500) / 173.7178,   φ = RD / 173.7178
  Helpers:     g(φ_j) = 1 / sqrt(1 + 3φ_j²/π²)
               E = 1 / (1 + exp(−g(φ_j)(μ − μ_j)))
  Variance:    v = [ g(φ_j)² E (1 − E) ]⁻¹
  Improvement: Δ = v g(φ_j)(s − E)
  Volatility:  σ' solves f(x) = 0 by the Illinois method, where
               f(x) = e^x(Δ² − φ² − v − e^x) / (2(φ² + v + e^x)²) − (x − ln σ²) / τ²
  Pre-period:  φ* = sqrt(φ² + σ'²)
  Update:      φ' = 1 / sqrt(1/φ*² + 1/v)
               μ' = μ + φ'² g(φ_j)(s − E)
  Convert:     r' = 173.7178 μ' + 1500,   RD' = 173.7178 φ'
  ```

  A series is those games played one after another, and the client solves it as one update instead of playing it game by game: it finds the rating at which the claim's prior standing and the series' score agree, the maximum of the log posterior, which is concave, so bisection on its slope always converges, and takes the deviation from the series' games, 1/φ'² = 1/φ² + *n* g(φ_j)² E(1 − E) at that rating, at a cost that does not depend on *n*. It is not Glicko-2's single period step over the *n* games: that step is one linearized move from the prior, which assumes a period moves a rating only a little, fine for small moves and wrong for a long series, and a seeding series moves a rating a long way. The inventor's example: a 450 player against a 3400 player over 1,000 games, 100 wins and 100 draws, is one series with score 0.15: played game by game, Glicko-2 converges to 3100 with deviation 15, where an expected score of 0.15 against 3400 sits, 3097; solved as one update, the series gives 3092 with deviation 16; the single period step from 450 gives 105,823.

  There are no global, delayed, ETL-style rating periods: each witness's game series on a strand is its own period, solved in O(1) by `lp_attest_series` (`laplace_attest_series`) as content is admitted, with different independent witnesses playing first in, first out. Run-length encoding is content structure only—identical consecutive children in a path with their run in `M`—so a prompt pasting one sentence a million times is a run in observed content and attests nothing. Genuine empirical corpus occurrences—such as 800 annotated tokens of `[dog, NOUN]` across a UD treebank—preserve their full `games` and `tokens` counts in `attestation` rather than being flattened to 1 game, while artificial Cartesian repeats inside a denormalized join table are deduplicated per logical assertion ([12. Attestations](Attestations.md) operation 12.9; [30. Conflicts](Conflicts.md) I6).
- **Out:** the new standing.
- **From:** [Consensus: Glicko-2](../Semantics/Consensus.md#glicko-2), [Consensus: Matchups](../Semantics/Consensus.md#matchups), [Research: Relations Research: The Glicko-2 update](../Research/Relations.md#the-glicko-2-update), [Research: Learning: Rating one matchup at a time](../Research/Learning.md#rating-one-matchup-at-a-time), [Research: Engine Measurements: Native operations](../Research/Engine.md#native-operations).

### 13.5 Write the standing in place

- **In:** the new standing of 13.4.
- **Do:** update `consensus(claim)` in place (with `fillfactor = 80` across its 16 hex partitions), completely separate from the GIN-indexed `physicality` heap. The claim's witness series live in `attestation(claim, witness, lineage)`; where its content came from is also reachable by walking up containment through the GIN. There are no delayed consensus folds and no batch ETL jobs: `laplace_attest_series` folds arriving series natively in set-based batches during ingestion and turn/feedback witnessing.
- **Out:** the standing, current as of this attestation.
- **From:** [Consensus: No ETL](../Semantics/Consensus.md#no-etl), [Research: Engine Measurements: Consensus writes](../Research/Engine.md#consensus-writes).

## What the standing is

The standing is rating, deviation, volatility, match count, and attributable witness series in `attestation`, and every reader gets all of them: epistemic strength, uncertainty, volatility, empirical `games`/`tokens` frequency, and provenance, never one opaque confidence scalar. Confirmation, draw, and refutation stay distinct in it, and a claim with no rows is unknown. A calculated proxy never overwrites the recorded outcome it estimates. See `docs/INVENTION.md` §5, `docs/INVENTIONS.md` #23 and #24, and `docs/specs/08_Record_vs_Calculate_Spec.txt`.

## Standing versus empirical sense frequency

Querying reads standing and never mutates it. Epistemic standing in `consensus` says *whether* a lexicalization or proposition holds (`dog` as the animal, a ratchet catch, and a scoundrel are all genuinely valid English senses in OEWN/OMW/Wiktionary and therefore reach high standing), whereas empirical usage frequency—`attestation.tokens` / `games` from annotated treebanks and SemCor/WordNet `tag_cnt` sense-tagged counts, plus witness sense order—tells [18. Firmware](Firmware.md) and [20. Forward](Forward.md) *how often* each valid sense or POS role is used in practice when context alone leaves valid senses tied. Preserving both standing and empirical frequency keeps rare senses true without letting `"ratchet catch"` tie `"canine"` on an everyday prompt. See [Consensus: Matchups](../Semantics/Consensus.md#matchups) and [Research: Semantics Experiments: Translation through the ILI](../Research/Semantics-Experiments.md#translation-through-the-ili).

## Role trust

There are also trusts that differentiate subjects, pronouns, stopwords, and so on: a trust level for part of speech, for sense, and for dependency relation, so that filler does not drown everything. These are not standings and not columns of a claim; they are weights on which kind of word is allowed to pull, and belong to [18. Firmware](Firmware.md). See [Consensus: Trust](../Semantics/Consensus.md#trust) and [Research: Trust: Role trust](../Research/Trust.md#role-trust).

## What this stage leaves behind

A standing on every claim that tells how hard it tugs back, current as of the last attestation, and every attestation that produced it.

## Without this stage

Attestations are records with no score, and a pull has nothing to order strands by.
