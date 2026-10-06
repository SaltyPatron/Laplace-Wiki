# 13. Consensus

A witness's assertions of one claim are run-length games, folded on the client into one Glicko-2 rating period per cell per witness and played at the witness's trust as they arrive; witnesses play first in, first out, with no global or delayed folds.

Everything attested about a claim, as a whole, provides its overall score: a Glicko-2 standing that tells how hard a strand tugs back. Glicko-2 replaces a lot of conventional AI mechanisms.

## Before this stage

[12. Attestations](Attestations.md): the attestations, in order, each with its witness's trust and outcome.

## Operations, per claim and witness

### 13.1 Find the claim's standing

- **In:** the attestation's consensus ID from [12. Attestations](Attestations.md) operation 12.6.
- **Do:** same content means the same hash, and the deduplication applies to the attestations, to form a consensus: look up the standing by the consensus ID, the claim's composition, whatever its arity. Every source speaking about that claim folds into the same standing while its own attestation stays inspectable. If none exists, the claim enters for the first time at its stock default for its level of attestation. Consensus is not an answer vote; it is the standing evidence state consumed before and during a forward pass.
- **Out:** the standing: rating *r*, deviation RD, volatility σ. Stock is rating 1500, deviation 350 or the level's default, volatility 0.06.
- **From:** [Consensus: Deduplication](../Semantics/Consensus.md#deduplication), [Consensus: Entry](../Semantics/Consensus.md#entry), `docs/specs/05_Substrate_Invariants.txt` Rule #6, [Research: Engine Measurements: Consensus writes](../Research/Engine.md#consensus-writes).

### 13.2 Set the opponent from the witness's trust

- **In:** the witness's trust *t* from [12. Attestations](Attestations.md) operation 12.3.
- **Do:** the witness's trust alone sets the opponent; relation rank is salience applied at reading and never enters the fold, because a `HAS_SCRIPT` fact from Unicode is certain and merely low-salience, and multiplying rank into the opponent would play it as weak and uncertain. Uncertainty, source trust, and the like all affect an attestation's weight and how much it can change a consensus. Glicko-2 weighs every matchup by g(φ) = 1 / √(1 + 3φ² / π²), where φ is the opponent's deviation. Setting g(φ) = |*t*| turns trust into the deviation the witness plays with, φ = (π / √3) · √(1/*t*² − 1): trust 1.0 plays at deviation 0, 0.9 at 153, 0.67 at 349, 0.5 at 546, 0.3 at 1,002, 0.1 at 3,135. The step a matchup makes scales with *t*; the information it adds scales with *t*². A negative *t* gives exactly the same update as flipping the outcome at weight |*t*|: being reliably wrong is informative, being randomly wrong is not.
- **Out:** the opponent's rating and deviation for this matchup.
- **From:** [Consensus: Trust](../Semantics/Consensus.md#trust), `docs/plan/ASSIMILATION_ROADMAP.md` workstream A, [Research: Trust: Trust as a Glicko-2 opponent](../Research/Trust.md#trust-as-a-glicko-2-opponent).

### 13.3 Check the lineage

- **In:** the witness's lineage and the claim's witness set.
- **Do:** a claim another lineage already attested plays one matchup; testimony from the same lineage joins the witness set without a second matchup, so copies do not count as independent consensus. The same holds for every dependence root of [12. Attestations](Attestations.md) operation 12.11: a deterministic calculation repeated under one generation, and a mapping copied from the source it maps, each play once.
- **Out:** whether this attestation is a matchup or a join.
- **From:** [Attestations: Witnesses](../Semantics/Attestations.md#witnesses), [Research: Trust: Trust as a Glicko-2 opponent](../Research/Trust.md#trust-as-a-glicko-2-opponent), [Research: Model Ingestion: Testimony from three families](../Research/Models.md#testimony-from-three-families).

### 13.4 Play the matchup

- **In:** the standing of 13.1, the opponent of 13.2, the witness's *n* games on this claim and their mean score *s*, each game an outcome of 1, ½, or 0, or a score in [0, 1] a calculated witness supplies.
- **Do:** a claim is a game series: games plus a score, a draw at 0.5. A witness that asserts the same claim *n* times plays *n* games, run-length like a repeat in a path; the client folds every repeat from one witness, per cell, into one rating period, and the database receives one update per cell per witness:

  ```text
  Scale:       μ = (r − 1500) / 173.7178,   φ = RD / 173.7178
  Helpers:     g(φ_j) = 1 / sqrt(1 + 3φ_j²/π²)
               E = 1 / (1 + exp(−g(φ_j)(μ − μ_j)))
  Variance:    v = [ n g(φ_j)² E (1 − E) ]⁻¹
  Improvement: Δ = v n g(φ_j)(s − E)
  Volatility:  σ' solves f(x) = 0 by the Illinois method, where
               f(x) = e^x(Δ² − φ² − v − e^x) / (2(φ² + v + e^x)²) − (x − ln σ²) / τ²
  Pre-period:  φ* = sqrt(φ² + σ'²)
  Update:      φ' = 1 / sqrt(1/φ*² + 1/v)
               μ' = μ + φ'² n g(φ_j)(s − E)
  Convert:     r' = 173.7178 μ' + 1500,   RD' = 173.7178 φ'
  ```

  There are no global, delayed, ETL-style rating periods: one witness's repeats of one claim are that witness's period for the cell, and different witnesses play first in, first out, as content is observed, each as its own period, with deviation growing with elapsed time instead, clamped to a floor and a cap, and volatility capped. Incoming records play existing records. The more something is attested to, the more its score rises or lowers, just like a chess rating, and repetition does not limit itself. For *n* identical results against one opponent, 1/v = n·g²·E(1 − E), and

  $$\mu' - \mu = \frac{n\,g\,(s - E)}{1/\phi^{*2} + n\,g^2 E(1 - E)} \;\to\; \frac{s - E}{g\,E(1 - E)} \quad (n \to \infty)$$

  one full Newton step, larger for a low-trust witness than for a high-trust one; low trust only needs more games to reach it. A million refutations at an opponent deviation of 1500 take a claim at 2300 with deviation 60 to −720, with deviation 1.9. So the rating does not stop spam: what limits one witness's repetition is structural (a prompt gives no semantic attestation merely by being said, and dependence roots count copies once), and how repeats count at each level is open in [Conflicts](Conflicts.md). A million identical repeats from one witness are still one row, one matchup with *n* = 1,000,000. Because a standing saturates, the run length *n* is also kept as a count beside the claim, never only merged into the standing. Copies count once, by 13.3.
- **Out:** the new standing.
- **From:** [Consensus: Glicko-2](../Semantics/Consensus.md#glicko-2), [Consensus: Matchups](../Semantics/Consensus.md#matchups), [Research: Relations Research: The Glicko-2 update](../Research/Relations.md#the-glicko-2-update), [Research: Learning: Rating one matchup at a time](../Research/Learning.md#rating-one-matchup-at-a-time), [Research: Engine Measurements: Native operations](../Research/Engine.md#native-operations).

### 13.5 Write the standing in place

- **In:** the new standing of 13.4.
- **Do:** update the standing row in place, one metadata table keyed by the strand ID beside the path, never on the GIN-indexed path row. The claim's witness set is the trunks that hold its strand, read by a walk up through the GIN and never stored. There are no delayed consensus folds. ETL is forbidden: no delayed segments that group everything together, no lazy, manually updated hot caches, and no SQL doing the heavy operations. The matchup arithmetic is native; a witness's repeats on one cell arrive already tallied into its one rating period, and the write is a set-based statement per batch of arriving rows, one update per cell per witness.
- **Out:** the standing, current as of this attestation.
- **From:** [Consensus: No ETL](../Semantics/Consensus.md#no-etl), [Research: Engine Measurements: Consensus writes](../Research/Engine.md#consensus-writes).

## What the standing is

The standing is rating, deviation, volatility, witness count, and source and context scope, and every reader gets all of them: strength, uncertainty, surprise, and breadth, never one opaque confidence scalar and never a normalized share. Confirmation, draw, and refutation stay distinct in it, and a cell with no rows is unknown. A calculated proxy in the same cell never overwrites the recorded outcome it estimates. See `docs/INVENTION.md` §5, `docs/INVENTIONS.md` #23 and #24, and `docs/specs/08_Record_vs_Calculate_Spec.txt`.

## What is not a matchup

Querying picks the records with higher scores, but does not change scores. Numbers a source states beside a claim, such as a usage count it writes and a witness's sense order, are content, recorded as given and not played as games: ordered by standing alone, `dog`'s senses tie, the animal, a ratchet catch, and a morally reprehensible person all standing at 1743 with the same three witnesses; standing says whether a lexicalization holds, and how often it is meant is a different measure. See [Consensus: Matchups](../Semantics/Consensus.md#matchups) and [Research: Semantics Experiments: Translation through the ILI](../Research/Semantics-Experiments.md#translation-through-the-ili).

## Role trust

There are also trusts that differentiate subjects, pronouns, stopwords, and so on: a trust level for part of speech, for sense, and for dependency relation, so that filler does not drown everything. These are not standings and not columns of a claim; they are weights on which kind of word is allowed to pull, and belong to [18. Firmware](Firmware.md). See [Consensus: Trust](../Semantics/Consensus.md#trust) and [Research: Trust: Role trust](../Research/Trust.md#role-trust).

## What this stage leaves behind

A standing on every claim that tells how hard it tugs back, current as of the last witness's rating period, and every attestation that produced it.

## Without this stage

Attestations are records with no score, and a pull has nothing to order strands by.
