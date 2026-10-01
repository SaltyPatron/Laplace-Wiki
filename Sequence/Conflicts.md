# 30. Conflicts

The wiki's specification pages and the monorepo's invention documents state some things differently, and each difference is recorded here as both positions with their sources, unresolved, for the inventor.

None of these is settled by this page. Where an operation in another Sequence page touches one of them, it says so and points here.

## Placement and packing

### P1. Rank *r* takes the *r*-th Hilbert-ordered point, or the open radical-inverse point

- **Wiki.** [4. Projection](Projection.md): n = 1,114,112 Super-Fibonacci points with φ = √2 and ψ = 1.5337…, sorted by Hilbert value, and DUCET rank *r* takes the *r*-th point of the walk, H1. n is fixed in advance and every point is permanent within a version. [Atoms: Placement](../Storage/Atoms.md#placement), [Research: Placement](../Research/Placement.md).
- **Monorepo.** `docs/INVENTION.md` §2 and §17.2: tier-0 placement is the open Super-Fibonacci law `t = radicalInverse(rank), r = √t, cap = √(1 − t)`, injective, on the unit glome, with no terminal N, so that extending the realized prefix densifies the shell without moving earlier addresses; the codepoint perf-cache stores UCA order explicitly and carries exactly the native open-placement coordinates, and the loader accepts only that format. `docs/INVENTIONS.md` #4.
- **Agree.** Both place codepoints on the S³ in DUCET order, both derive IDs from the codepoint and never from the point, both fingerprint the generation.
- **Open.** Whether rank-to-point goes through the Hilbert walk over a fixed-n set, or through the radical inverse with no fixed n, and therefore whether a later Unicode version moves points or only appends them.

### P2. The vertex packs 43/43/42 bits of ID with 28 spare bits, or 212 bits

- **Wiki.** [11. Content](Content.md) operation 11.7: the 128-bit ID in the mantissas of X, Y, Z as 43, 43, and 42 bits at a fixed exponent in [0.25, 0.5), 28 spare bits parsed by the entity's type, and M as a fixed-length metadata field. [Physicality: Physicality](../Storage/Physicality.md#physicality), [Research: Hashing: Packing into IEEE-754 doubles](../Research/Hashing.md#packing-into-ieee-754-doubles).
- **Monorepo.** `docs/INVENTION.md` §4: each binary64 component contributes 53 reversible bits with the sign and 52-bit mantissa as payload at a fixed exponent, so a vertex carries exactly 212 bits: 128 id, 16 packed ordinal, 16 run length, 52 flags. `docs/INVENTIONS.md` #14, #15. The 16-bit ordinal and run fields are local carrier fields, and long runs are split.
- **Agree.** Both pack the complete ID into the vertex, both keep a run length, both say the packed values are not positions and must not enter geometry.
- **Open.** Which layout the extension, the GIN operator class, and the native pack and unpack implement; whether an ordinal is carried in the vertex at all, given that the wiki says the vertex sequence is the order and no ordinal is needed.

### P3. A composition's coordinate is the exact integer centroid, or a Karcher mean

- **Wiki.** [11. Content](Content.md) operation 11.6: the exact integer average of the children's fixed-point coordinates, truncated toward zero, which the wall theorem depends on. [Physicality: Real coordinates](../Storage/Physicality.md#real-coordinates).
- **Monorepo.** `docs/INVENTION.md` §2 proves the bounded-domain theorem for the Euclidean centroid, and the native composer uses it; `docs/plan/MODEL_INGESTION_DESIGN.md` §9 and `docs/specs/38_Collections_Are_Compositions.md` §3 record that current managed model, chess, and collection paths place by Karcher mean, and that a permutation-invariant placement is what makes a set a well-defined composition. Reconciliation is owned by monorepo issue 1050 and is not declared resolved.
- **Agree.** The bounded-domain theorem holds for the centroid; a set must land at one coordinate regardless of member order.
- **Open.** One placement law for every lane, and whether the sorted-member composition of a collection makes the centroid already permutation-invariant for sets.

## Firmware and witnessing

### C1. Do Laplace's own outputs, and user prompts, become attestations?

- **This repository's archived design and current code:** responses self-witness; feedback on a response is an attestation folding into the same consensus the next walk reads; prompt and response are deposited as witnesses at `UserPromptContent` 0.30 and `ResponseContent` 0.20; the reply attests `DEPENDS_ON` the prompt; user feedback deposits confirm and refute attestations. `docs/INVENTION.md` §5 lists Laplace itself as a possible witness, and §13 says a generated response may be witnessed with its derivation and does not become truth because the system produced it.
- **Laplace-Refactor, written from the inventor's direct requirements:** user prompts and live activity create exact observation, occurrence, and trajectory state and zero semantic attestations merely by being observed; internal cognition and generated output likewise do not self-attest; later independently observed or adjudicated outcomes may update standing.
- **Wiki.** [Attestations: Observations](../Semantics/Attestations.md#observations): normal digital content gives observations, not attestations; [Consensus: Trust](../Semantics/Consensus.md#trust): where a user's input is played as an attestation it enters at user-prompt trust.
- **Agree.** A response is content with an occurrence; it is never truth because Laplace produced it; an independently observed consequence changes standing.
- **Open.** Whether a response or prompt may mint attestations at all; whether turn bookkeeping claims, `APPEARS_IN`, `HAS_ATTRIBUTION`, `DEPENDS_ON`, are semantic attestations or record-lane structure; whether explicit user feedback is testimony by the user or an assertion that becomes a matchup only after adjudication; whether a response's source should carry the firmware identity. `docs/specs/39_Personality_Firmware.md` §9 C1.

### C2. Is SELECT stochastic?

- **Monorepo, this repository.** `docs/specs/36_Laplace_Forward_Pass.md` SELECT: "under the declared deterministic or stochastic policy"; the native pass elects by ordinal rank and then, unless spread is 0, draws with a Gumbel-max key over the first top_k ranks with a seed derived from the prompt, which is mathematically a sample from a softmax over rank positions; the default is spread 0.7 or 0.6, top_k 10.
- **Laplace-Refactor and the inventor.** Laplace does not use softmax continuation to create an answer; selection is a deterministic, inspectable execution; firmware is a deterministic cognitive policy; typed state is never a softmax or a distribution.
- **Wiki.** [Research: Semantics Experiments: What was measured on one entity](../Research/Semantics-Experiments.md#what-was-measured-on-one-entity): the pull has no softmax; temperature is how near a tie must be before another strand can be taken, a decision of the tree over a set already in hand.
- **Open.** Whether a seeded, replayable draw over the rank order is a lawful exploration personality, or every SELECT policy must be deterministic, making spread and top_k retire or become deterministic window rules. `docs/specs/39_Personality_Firmware.md` §9 C2.

### C3. Is the Gödel engine the OODA loop?

- **This repository and the inventor.** The archived spec 15 is "Gödel engine: closing the OODA loop", self-reference where outputs become inputs; roadmap law 17: the Gödel engine is its OODA loop; the inventor: "the godel engine, forward pass, etc is that personality."
- **Laplace-Refactor.** OODA is the control and effect cycle, evidence learning is an epoch change, and Gödel is candidate calculus and procedure discovery with falsification; "Gödel = multi-scale OODA" is marked historical terminology.
- **Open.** Whether "Gödel engine" names the whole self-referential loop of [23. Learning](Learning.md) or only its discovery lane, 23.7 to 23.10. `docs/specs/39_Personality_Firmware.md` §9 C3.

### Q1 to Q5

- **Q1.** Is firmware a source, witnessed and rated like any other source, or a rated participant with no trust class, the chess-player model, because it observes nothing?
- **Q2.** Is the sufficiency bound's multiplier of two deviations firmware or standing law shared by every reader?
- **Q3.** Is relation rank a registry value every firmware reads unchanged, or a valuation firmware may re-weight?
- **Q4.** May Laplace pick among already activated firmware by standing, or must the principal or governance always name it?
- **Q5.** Does the default firmware abstain and report alternatives on ambiguity, or ask a clarifying question?
- `docs/specs/39_Personality_Firmware.md` §9.

## Tables and registries

### T1. Five tables, or five tables plus governed registries

- **Inventor.** "Entity, Physicality, Attestation, Consensus... why do i need more tables than this"; "entity, physicality, attestation, consensus, witness... Aside from these core tables, i shouldn't have any fake lookup tables"; canonical names and lookup tables are hacks. `docs/INVENTOR_RECORD.md` §Entities.
- **Monorepo.** Relations, qualifiers, trust classes, entity types, vocabularies, and firmware policy kinds are governed registries with stable bits generated from manifests into native law and perf-cache ROMs, never seeded as rows; a type's, class's, or relation's id is the content id of its label. `docs/plan/ASSIMILATION_ROADMAP.md` law 4. The monorepo's workstream G lists the fake machinery still to remove: blake3 source ids, marker entities, the canonical-names table, `ByteAtoms` as a second alphabet, static registries.
- **Wiki.** [8. Database](Database.md): entity, physicality, source, statistics, witness, claim, attestation, consensus.
- **Agree.** No lookup table holds semantics; a registry value is the content entity of its label.
- **Open.** Whether a statistics table and a claim table are "fake lookup tables" or the physicality and attestation the inventor names; and whether a registry held outside the database as generated code and ROM satisfies "no more tables than this."

### T2. Two claim hashes, or one typed cell plus a qualifier mask

- **Wiki.** [Claims: IDs](../Semantics/Claims.md#ids): a witnessing ID over the claim's specifics and a consensus ID over what makes it unique; masks in separate columns for part of speech, sense, dependency relation.
- **Monorepo.** `docs/specs/05_Substrate_Invariants.txt` Rule #6: the consensus address is the typed `(subject, relation, object)` triple; the attestation row carries the witness, context, outcome, score, and a 256-bit qualifier mask; consensus has no qualifiers yet, so a reader needing one variant probes the attestations behind the cell.
- **Agree.** Two witnesses of the same claim land on one consensus cell; the specifics live on the attestation.
- **Open.** Whether the wiki's masks and the monorepo's qualifier mask are one column, and whether qualifiers reach consensus.

### T3. No consensus folds, or a set-sized fold

- **Wiki.** [Consensus: No ETL](../Semantics/Consensus.md#no-etl): there are no consensus folds; standings are updated in place, one matchup per attestation as it arrives, and ETL is forbidden.
- **Monorepo.** The ingest spine ends in "fold completion" and "set-sized evidence fold (attestations → consensus)"; roadmap workstream C measures that the current fold reads every touched cell's evidence back over SPI and refolds from neutral on every working set, and targets folding each witness's rating period per cell in memory natively and emitting consensus deltas.
- **Agree.** The update is native Glicko-2 per cell, set-sized per batch, never per record, never delayed, never SQL doing the arithmetic.
- **Open.** Only the word: the monorepo's "fold" names the batch Glicko-2 update; the wiki forbids "folds" meaning delayed aggregation. Whether a witness's whole rating period is played as one matchup per cell, or each attestation as its own period.

## Reading standings

### R1. Confidence and cost as one scalar per strand, or typed channels never collapsed

- **Wiki.** [15. Web](Web.md) operations 15.3 and 15.4: a standing is read as *p* = σ((*r* − 1500)/173.7178 − *k*·RD/173.7178) and a cost −ln *p* + λ, so that A* and Dijkstra are exact.
- **Monorepo.** `docs/INVENTION.md` §19: typed state stays typed; geometry, evidence, standing, contradiction, role compatibility, source dependence, and path cost are not flattened into one scalar merely because a priority queue needs a key; the firmware declares an election order over typed dimensions.
- **Agree.** The standing is never changed by a read; a search operator needs an ordering; the conservative reading takes the rating some deviations down.
- **Open.** Whether the −ln *p* + λ cost is the declared fold of one channel that an A* operator inside SCAN is allowed to use, or a collapse ORIENT and STEER forbid.

## What this page leaves behind

The list of decisions that are the inventor's. Every other Sequence page is written to hold under either answer where it can, and says which answer it assumed where it cannot.
