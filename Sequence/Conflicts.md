# 30. Conflicts

The wiki's specification pages and the monorepo's invention documents state some things differently, and each difference is recorded here as both positions with their sources, with the inventor's decision where one has been made and open for the inventor where none has.

An entry marked **Decided** records the inventor's decision, and the Sequence pages state it; every other entry is open, and none of those is settled by this page. Where an operation in another Sequence page touches one of them, it says so and points here.

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

### C4. Trust is a fixed opponent's deviation, or a bound on each vote

- **Wiki.** [13. Consensus](Consensus.md) operation 13.2 and [Research: Trust](../Research/Trust.md#trust-as-a-glicko-2-opponent), as first written: the witness's trust alone sets the opponent; setting g(φ) = |*t*| turns trust into the deviation the witness plays with.
- **Built.** Laplace-Native's `lp_trust_deviation` and `lp_attest` play every witness as a fixed 1500 opponent whose trust sets only its deviation, g(φ) = |*t*|, φ = (π / √3) · √(1/*t*² − 1), trust 1.0 at deviation 0, 0.9 at 153, 0.5 at 546, 0.1 at 3,135, and a claim enters at the witness's deviation; computed with that code, an affirming series leaves a claim higher and more certain the lower the witness's trust, an inversion of the rule: over 1,000 games, trust 0.2 ends at 3235 with deviation 55, and trust 0.9 at 1884 with deviation 30.
- **Decided.** Trust bounds a vote: each game's outcome is pulled toward a draw by the witness's trust, *s*_eff = 0.5 + *t*(*s* − 0.5), so no repetition takes a source past its trust's ceiling, symmetrically for affirmation and refutation and monotone in trust, and one witness alone can give a claim only bounded certainty, a per-witness floor on its deviation; a negative *t* flips the outcome, because being reliably wrong is informative and being randomly wrong is not. Count is never independence: witnesses sharing a dependence root or a trust class count as one root, capped, wherever low-trust voices do attest, explicit feedback, model outputs, Laplace's own responses. A prompt is an observation and attests nothing merely by being said, [22. Users](Users.md) operation 22.6: Laplace records that people say a thing, a fact about discourse, without its standing moving. A witness's own trust is its own rating, starting at its trust class's default and earned only through agreement or disagreement with independent witnesses and verified outcomes, never by repeating itself. The inventor's test: user prompts screaming that the earth is flat must not drown out GPS, photographs, mathematics, reports, and NASA. Computed with a series solver, the round-earth evidence alone stands at 2000, *p* 0.947; a million flat-earth prompts as a million independent witnesses drown it, 1393, *p* 0.351, even with a per-witness cap; as one capped root they dent it, 1765, *p* 0.821; as observations only it stands, 2027, *p* 0.954. [13. Consensus](Consensus.md) operation 13.2.

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
- **Decided.** A registry is a perf-cache. Its members are content entities like everything else, `noun` the same `[n,o,u,n]` as the word anywhere, and a stable bit or slot is an index over them, never the identity of a meaning. "Never seeded as rows" means a registry is not a lookup table of made-up IDs, not that its members have no entities. A member's meaning is attested and realizable in any language; English names in manifests and code are developer handles, no code path tests for an English value, and no identity is derived from an invented label such as `WordNet_Synset` or `AcademicCurated`. [6. Registries](Registries.md).
- **Open.** Whether a statistics table and a claim table are "fake lookup tables" or the physicality and attestation the inventor names.

### T2. Two claim hashes, or one typed cell plus a qualifier mask

- **Wiki.** [Claims: IDs](../Semantics/Claims.md#ids): a witnessing ID over the claim's specifics and a consensus ID over what makes it unique; masks in separate columns for part of speech, sense, dependency relation.
- **Monorepo.** `docs/specs/05_Substrate_Invariants.txt` Rule #6, line 131: the consensus address is the typed `(subject, relation, object)` triple; the attestation row carries the witness, context, outcome, score, and a 256-bit qualifier mask; consensus has no qualifiers yet, so a reader needing one variant probes the attestations behind the cell.
- **Agree.** Two witnesses of the same claim land on one consensus cell; the specifics live on the attestation.
- **Decided.** A claim is a composition of content IDs with referential integrity, of any arity and any tier: a lexicalization `[lemma, language, ILI]`, a concept relation `[ILI, hypernym, ILI]`, a role inside a roleset, a valence pattern. The `(subject, relation, object)` triple is one shape among many. The consensus ID covers the claim's composition; the witnessing ID adds the witness, the context, and the qualifiers. Consensus is keyed on the claim's composition, never on BLAKE3(subject‖type‖object) with a missing object filled with zeros. The qualifier mask is on the attestation and says which variants of one proposition a source asserts; the part-of-speech, dependency, and other enum masks are bits set where a source asserts them, at the tier it asserts them. [12. Attestations](Attestations.md) operations 12.5 to 12.7.
- **Open.** Whether the consensus row carries the OR of its attestations' qualifier masks.

### T3. No consensus folds, or a set-sized fold

- **Wiki.** [Consensus: No ETL](../Semantics/Consensus.md#no-etl): there are no consensus folds; standings are updated in place, one matchup per attestation as it arrives, and ETL is forbidden.
- **Monorepo.** The ingest spine ends in "fold completion" and "set-sized evidence fold (attestations → consensus)"; roadmap workstream C measures that the current fold reads every touched cell's evidence back over SPI and refolds from neutral on every working set, and targets folding each witness's rating period per cell in memory natively and emitting consensus deltas.
- **Agree.** The update is native Glicko-2 per cell, set-sized per batch, never per record, never delayed, never SQL doing the arithmetic.
- **Built.** Laplace-Engine `src/db.c` plays one `lp_attest` for a claim the first time a lineage attests it, ever; every later occurrence only adds to the attestation's `games` and averages its score, so an attestation's games are counted and never played.
- **Decided.** A witness asserting the same claim *n* times is one attestation with *n* games, played as that series: if WordNet says a dog is a noun 30 times, that is one attestation with 30 games. The client folds every repeat from one witness before the database sees anything, and the database receives one update per strand per witness; different witnesses play first in, first out. The client solves the series as that one update, not by Glicko-2's single period step: it finds the rating where the claim's prior standing and the series' score agree, the log posterior being concave so bisection on its slope always converges, and the deviation from the series' games, at a cost independent of *n*. The single period step is one linearized move, fine for small moves and wrong for a long series: a 450 player against a 3400 player, 1,000 games, 100 wins and 100 draws, is one series with score 0.15; played game by game Glicko-2 converges to 3100 with deviation 15, where an expected score of 0.15 against 3400 sits, 3097; solved as one update it gives 3092 with deviation 16; the single period step from 450 gives 105,823. "No rating periods" and "no folds" mean no global, delayed, ETL-style periods or aggregation. A number a source states, such as WordNet's `tag_cnt`, is an observation, not games. [13. Consensus](Consensus.md) operation 13.4.

## Reading standings

### R1. Confidence and cost as one scalar per strand, or typed channels never collapsed

- **Wiki.** [15. Web](Web.md) operations 15.3 and 15.4: a standing is read as *p* = σ((*r* − 1500)/173.7178 − *k*·RD/173.7178) and a cost −ln *p* + λ, so that A* and Dijkstra are exact.
- **Monorepo.** `docs/INVENTION.md` §19: typed state stays typed; geometry, evidence, standing, contradiction, role compatibility, source dependence, and path cost are not flattened into one scalar merely because a priority queue needs a key; the firmware declares an election order over typed dimensions.
- **Agree.** The standing is never changed by a read; a search operator needs an ordering; the conservative reading takes the rating some deviations down.
- **Open.** Whether the −ln *p* + λ cost is the declared fold of one channel that an A* operator inside SCAN is allowed to use, or a collapse ORIENT and STEER forbid.

## Strands and meaning

### S1. An ILI is a key recorded nowhere, or a highway node a word bubbles up to

- **Wiki.** [Corpora](../Corpora/README.md): an ILI number is a source's key, resolved to the thing it names and recorded nowhere. [Semantics](../Semantics/README.md) and [Claims: Tuples](../Semantics/Claims.md#tuples): `dog` has an ILI; bubble up to it, change the language, bubble down, and there is `Hund`; `dog → ILI i46360`. [Claims: Masks](../Semantics/Claims.md#masks): an ILI is an identifier and gets no mask.
- **Monorepo.** `docs/plan/ASSIMILATION_ROADMAP.md` workstream B: a word binds to a language-neutral key (`dog —HAS_SENSE→ i46360 @eng`), and facts about the key are language-neutral.
- **Agree.** The concept is the highway node that translation passes through, and it has no mask bit.
- **Decided.** A source writes two kinds of identifier. A highway ID is a highway node, from a shared vocabulary that other sources cite too: an ILI, a PropBank roleset, a VerbNet class, a FrameNet frame, frame element, or lexical unit, a VerbAtlas frame, a language code. It is content, `i46360` is `[i,4,6,3,6,0]` exactly as `3.14159` is `[3,.,1,4,1,5,9]`, every source that cites it lands on the same node, and that it is an ILI is attested by CILI, the source that says so; it is never canonicalized into a governed reference or a made-up key. An internal pointer is how a source addresses its own records or another release's: a WordNet offset, a synset or sense id, a FrameNet number, a UD token number or `sent_id`, a Tatoeba sentence number, a GeoNames geonameid, a dataset's row id, a line or row number. It is packaging: the recipe decomposes it by the source's own notation only to extract the facts it carries, a WordNet offset's part of speech `v`, a sense key's lexicographer file `38`, resolves it to the ID of what it points at, through the source's own tree or the highway perf-cache, and does not record it; the Engine's `key`, `refer`, and `type` do exactly this. A WordNet 3.0 offset is the byte position of its synset's line in that release's `data.<pos>` file: byte 1,976,841 of `data.verb` starts `01976841 38 v 01 drop`; it is unique only with its part of speech, 73 offsets occurring in both `data.noun` and `data.verb`, `00001740` being noun 'entity' and verb 'breathe', and only within its release. A synset cannot be identified by its words either: 19,619 of WordNet 3.0's 117,659 synsets share their exact word list with another, eleven verb synsets being just `drop`; a synset is its ILI. Nothing is order-dependent: every node is content-derived, so what two sources say links by entity collision whichever is ingested first, and a synset whose ILI is `in` is given no stand-in identity for a later CILI release to replace; its content-derived nodes link by collision when CILI states its ILI. A publicly known identifier used across sources and languages is a highway node: a FIDE ID is the node for a player as an ILI is for a concept, the player's names in every language and script are its lexicalizations, and the languages the player speaks are attested relations. Laplace cares about identifiers and links, not the text underneath, until it renders: an identifier is decomposed by its notation, `va:0001f` a namespace `va`, a number, and a kind, and a name such as `TOLERATE` is a label attested of the node, used to realize it. Traversal bubbles up from a word to its highway node through the lexicalization strand, `[dog, eng, i46360]`, changes the language or hops along a highway mapping, roleset to VerbNet class to frame, and bubbles down to words, every step a GIN read over strands; facts about the highway node are language-neutral. Positions, a line, a byte offset, a row number, an ordinal, are never part of any ID. A sense key is a pointer, I7. [10. Recipes](Recipes.md) operation 10.11, [12. Attestations](Attestations.md) operation 12.4.

### S2. The stock default a claim enters at, when relations are content

- **Wiki.** [Consensus: Entry](../Semantics/Consensus.md#entry): a claim entering for the first time starts from a stock default for its level of attestation: whether synonyms matter more or less than meronyms, nouns than verbs, proper nouns than stopwords, and the source's trust, stability, and uncertainty. [Claims: Tuples](../Semantics/Claims.md#tuples): `is a` is a sentence, not an enum name.
- **Monorepo.** `docs/plan/ASSIMILATION_ROADMAP.md` workstream A, decided 2026-09-25: a claim's standing comes from the witness's trust alone; relation rank is salience, applied at reading.
- **Built.** Laplace-Engine `src/db.c` `entry_deviation`: a claim enters at the rating and deviation its recipe gives that kind of statement, or else at Glicko-2's 1500 and the deviation its witness's trust plays with; every matchup then plays at the witness's trust alone.
- **Agree.** A matchup weighs a witness by its trust, never by its relation.
- **Open.** Whether the entry default differs by kind of statement at all, and if it does, what names the kind now that a relation is the content its source writes: a recipe line, a flagged enum of the source's relation inventory, or the firmware.

### S3. Relation salience from a hard-coded rank table, or from content

- **Wiki.** [Claims: Tuples](../Semantics/Claims.md#tuples): nothing is hard-coded except pregenerated relations, types, and kinds that act like a perf-cache or flagged enums. Q3 above.
- **Monorepo.** `engine/manifest/relation_types.toml` `[ranks]`: thirteen rank tiers over 233 English canonical relation names (`HAS_POS` lexical glue 0.18, `IS_A` taxonomic 0.90), read as salience by the forward pass and by model export.
- **Built.** Laplace-Engine has no rank table. Its firmware weighs strands by predicate content (`weigh N KIND...`) and words by what is attested of them (`role by UPOS`, `role 1 NOUN ADJ NUM`), names resolved to their entities when the firmware loads.
- **Decided.** English is never identity: the 233 English names of `relation_types.toml` are developer handles, a relation is the content its source writes, with its meaning attested and realizable in any language, and a registry bit is a perf-cache index over it. No code path tests for an English value. [6. Registries](Registries.md) operation 6.1.
- **Open.** Whether salience is a flagged enum per source relation inventory, a value the firmware supplies by naming content, or something measured, as [Research: Trust: Role trust](../Research/Trust.md#role-trust) measures the information a part of speech carries.

### S4. Firmware is a file never a record, or a content-addressed program over the operation ISA

- **Wiki.** [Glossary](../Reference/Glossary.md): firmware is a file, never a record. [18. Firmware](Firmware.md) operation 18.3: a firmware image has a content identity.
- **Monorepo.** `docs/specs/39_Personality_Firmware.md` §1 and §1.1: a versioned, content-addressed, replayable program over the operation ISA of spec 37, loaded as data; policy kinds are a governed registry.
- **Built.** Laplace-Engine `src/firmware.c` reads parameters for five fixed operations (`hop`, `search`, `translate`, `follows`, `pull`); `src/program.c` fixes the stage order RESOLVE to WITNESS and STEER's election order in C. The firmware chooses numbers and names; it does not program the stages.
- **Agree.** Firmware never writes knowledge or standing, and the same records read under two firmwares give two behaviours over one truth.
- **Open.** Whether a firmware is content (an ID, not attested), and how much of the stage order and election order is the firmware's program rather than the engine's code.

## Identity

### I1. A composition's hash input has a domain byte, or only its children's IDs

- **Wiki.** [Identity: Pure content](../Storage/Identity.md#pure-content) and [11. Content](Content.md) operation 11.5: a composition's ID is BLAKE3 over its children's 16-byte IDs, in order, and nothing else. [Research: Hashing: Hash input](../Research/Hashing.md#hash-input).
- **Monorepo.** `docs/ARCHITECTURE.md` line 55: the executable id is a BLAKE3-derived hash over the Merkle domain byte plus the ordered child-id sequence; `hash128_merkle` prepends `0x01`.
- **Built.** Laplace-Native and Laplace-Engine hash the child IDs alone.
- **Decided.** There is no domain byte. A leaf hashes the 1 to 4 bytes of one codepoint's UTF-8 and a node at least 32, and a composition with one child is that child, so a node can never collide with a leaf. The monorepo's domain byte is wrong.

### I2. The same content under the same recipe, or the same content

- **Wiki.** [Identity](../Storage/Identity.md): the same content always has the same ID.
- **Monorepo.** `docs/INVENTION.md` line 169: composite identity is Merkle-style over the ordered child identities under the selected recipe/domain separation. `docs/INVENTIONS.md` #1, line 7: equal canonical content under one declared recipe converges across sources and modalities.
- **Decided.** The same content has the same ID; the recipe decides the tree. The same bytes under a different decomposition can give a different trunk, but a recipe never salts a hash, and no recipe name or version is in a hash input.

### I3. The witness is `[authority, release]`, or the source trunk

- **Wiki.** [9. Sources](Sources.md) operation 9.4 and [12. Attestations](Attestations.md) operation 12.2, as first written: the witness is the content composition `[authority, release]`, one per lexicon. [10. Recipes](Recipes.md) operation 10.4: a source is a trunk entity above its files.
- **Monorepo.** `docs/plan/ASSIMILATION_ROADMAP.md` law 1, line 48: the witness identity is the content composition `[authority, release]` (`SourceWitness.Id`), one per lexicon, `[omw-fr, 2.0]`.
- **Agree.** The witness is a content-derived entity, never a blob hash of a name or an ID made from a made-up key such as `substrate/source/X/v1`. A source is the trunk over its files, a release is its files, and version suffixes never appear in IDs.
- **Built.** Laplace-Engine names a witness by the name its source gives itself, emits claims as events only (`say.c` `claim()` and `together()`: no entity is made of the claims together), and keeps provenance only in the `attestation` table, a row of claim, witness, score, and position.
- **Decided.** The witness is the source trunk, `[source record, its files' trunks in path order]`. The corpus is the trunk: Universal Dependencies, Open Multilingual Wordnet, the WSD evaluation framework, and HateCheck are each one source trunk and one witness, and a treebank, a lexicon, or a dataset under one of them is files, with their paths, under that trunk, never a witness of its own. Annotators, workers, speakers, and members a corpus names are content, not witnesses: the corpus is the witness, and what it reports of them, that this annotator labelled this case hateful, that this speaker said this sentence, that this member added this sentence, are relations the corpus attests, added to the web explicitly. Provenance by containment is the target: a record is a path over the strands, the claims, it asserts, inside its file's content tree, with each strand's outcome or score in its vertex's M, and many source trunks can reference the same strand, several parents found through the GIN. Standing, rating, deviation, volatility, and matches, is one metadata table keyed by the strand ID, beside the path, never on the GIN-indexed path row, where a non-HOT update would re-insert GIN entries for every vertex. The per-claim-and-witness attestation table, with its qualifier masks, stays until a working prototype on real data shows that containment answers everything the table answers today, who said a claim, its games, score, and position, its qualifiers, forgetting and replay, with nothing lost; the two run side by side until then. Trust and lineage are keyed by the trunk ID. Standing is stored on every strand. Forgetting a source removes its attestations and its trunk, sweeps what nothing references, and replays the standings it touched. Entities, an ID and a coordinate, and physicality, the content, stay separate rows. A source's own name stays content inside its source record. Witnessing is not attribution: that any entity was witnessed is calculated by a walk up to the trunks that hold it, and never stored; that a source asserted a claim is its attestation row, and in the target the strand in a record path under that source's trunk. What the Engine does now is as built, including the witnesses it names below the corpus, a treebank by its directory (`witness {dir}`), a lexicon by its label (`{first label}`), and an annotator column as a witness of its own (`voices`, `own`, `by`); the target is the one corpus trunk as the only witness, with those treebanks, lexicons, and annotators content under it. [9. Sources](Sources.md) operation 9.4, [12. Attestations](Attestations.md) operations 12.2 and 12.9, [Attestations: Witnesses](../Semantics/Attestations.md#witnesses).

### I4. Records, files, and packaging are not content, or they have trunks

- **Wiki.** [11. Content](Content.md) operations 11.2 and 11.3: a file is a trunk, `[metadata, content]`, under a source trunk.
- **Monorepo.** `docs/plan/ASSIMILATION_ROADMAP.md` law 2, line 49: curated sources are mined for knowledge, not recorded bit-perfect; records, files and packaging are not content; only user content needs exact reconstruction.
- **Agree.** A curated source is mined for what it teaches, and only user content needs exact reconstruction.
- **Decided.** A curated source's records, files, and packaging need not reproduce the admitted bytes, but the records, the files, and the source still have trunks and IDs like any content: one Merkle DAG from leaf to source trunk. [10. Recipes](Recipes.md) operation 10.8.

### I5. An external identifier is a typed reference, or content

- **Wiki.** [Claims: Tuples](../Semantics/Claims.md#tuples): every part of a claim is an entity.
- **Monorepo.** `docs/plan/INGEST_BOUNDARY_AND_RECIPE_LAW.md` lines 82 and 168: an opaque external identity lowers to a typed reference; a sense key, synset id, frame id, roleset id, or external record key is a typed reference under a governed identity, and not ordinary text content just because the identifier is UTF-8.
- **Decided.** It depends on the kind of identifier. A highway ID is content, a highway node, the same entity wherever its text occurs, and what kind of identifier it is is attested by the source that says so; it is never a typed reference under a governed identity. An internal pointer is decomposed by the source's notation only for the facts it carries, resolved to the ID of what it points at, and not recorded. Structured notation decomposes by the source's grammar, declared in the recipe, never by word segmentation: `mcr:ili-30-01976841-v` is a prefix, a scheme, release 30, an offset, and a part of speech; `drop%2:38:00::` is a lemma, part of speech 2, lexicographer file 38, and lex_id 00. S1 above. [10. Recipes](Recipes.md) operation 10.11.

### I6. How repetition counts at each level

- **Wiki.** [13. Consensus](Consensus.md) operation 13.4 and [Consensus: Matchups](../Semantics/Consensus.md#matchups), as first written: a witness's repeats of one claim are run-length games, folded on the client into one rating period per cell. [21. Sessions](Sessions.md): the same prompt text in two turns is one content entity occurring twice.
- **Agree.** Repetition is read off the tree at its level: inside one message's tree, across the turns of one session, across users, across tenants.
- **Built.** Laplace-Engine `src/db.c` plays one `lp_attest` for a claim the first time a lineage attests it, ever; every later occurrence only adds to the attestation's `games` and averages its score, so an attestation's games are counted and never played.
- **Decided.** If WordNet says a dog is a noun 30 times, that is one attestation with 30 games. An attestation is one per strand and witness: its games, how many times that witness asserts the strand, and a score; a claim is a game series, games plus a score, played at the witness's trust. The client folds a source's repeats before the database sees anything, so the database takes one update per strand per witness. The client solves the series as that one update, not by Glicko-2's single period step: it finds the rating where the claim's prior standing and the series' score agree, the log posterior being concave so bisection on its slope always converges, and the deviation from the series' games, at a cost independent of *n*. The single period step is one linearized move, fine for small moves and wrong for a long series: a 450 player against a 3400 player, 1,000 games, 100 wins and 100 draws, is one series with score 0.15; played game by game Glicko-2 converges to 3100 with deviation 15, where an expected score of 0.15 against 3400 sits, 3097; solved as one update it gives 3092 with deviation 16; the single period step from 450 gives 105,823. Run-length encoding is content structure only: identical consecutive children in a path, with the run in M. A sentence pasted a million times into one prompt is a run in that prompt's content, an observation that attests nothing; the same message across turns lengthens the session's trajectory, a turn being itself a trajectory of referenced IDs. Across users or witnesses, repeats are separate witnesses, independent only as far as their dependence roots are. A number a source states, such as WordNet's `tag_cnt`, is an observation, not games. Packaging is not repetition: a cross-product table layout or an automatic tagger's per-token output repeating one fact is not the source saying it again. [13. Consensus](Consensus.md) operation 13.4.

### I7. A sense key is an internal pointer, or a lexicalization in its own right

- **Wiki.** [Corpora: Wordnets](../Corpora/Wordnets.md) and [Corpora: Hops](../Corpora/Hops.md): sense keys, `abandon%2:40:00::`, are among the identifiers the highway's `ili` list resolves to a concept; VerbNet's members, SemCor's gold labels, and the Predicate Matrix write them.
- **Built.** Laplace-Engine resolves a sense key to the concept it names (`type sense_key ili`, `type wn ili`) and records nothing of it.
- **Agree.** A sense key is structured notation, decomposed by WordNet's grammar into a lemma, a part of speech, a lexicographer file, and a lex_id, and the facts those parts carry are extracted.
- **Decided.** A sense key, `dog%1:05:00::`, is WordNet's internal pointer to a lexicalization. It is decomposed for its facts, the lemma, the part of speech, and the lexicographer file, resolved through the highway perf-cache to the lexicalization strand it addresses, and not recorded. Other sources that cite a sense key land, through the same resolution, on that lexicalization. [10. Recipes](Recipes.md) operation 10.11.

### I8. Language is a part of the lexicalization strand, or a flag on it

- **Wiki.** [12. Attestations](Attestations.md) operation 12.5 and [9. Sources](Sources.md), the ISO 639 row of the estate: a lexicalization is `[lemma, language, ILI]`, with the language a part of it and not a context column; bubbling changes the language on the strand filter.
- **Agree.** Language is never a context column, and a word in two languages is two lexicalizations.
- **Decided.** The language is a part of the lexicalization strand, `[dog, eng, i46360]`, an ISO 639 highway node in the path, never a flag or a mask bit, and no mask bank holds languages. Changing the language is intersecting on the ILI and a different language part, the same GIN read. [12. Attestations](Attestations.md) operation 12.5.

### I9. ToxiGen's generated and human text: two witnesses, or one trunk

- **Wiki.** [9. Sources](Sources.md), the ToxiGen row of the estate, as first written: labels under two witnesses, AcademicCurated for the human annotations and AIModelProbe for the generated text.
- **Monorepo.** `docs/source-estate.tsv` line 54: admit generated and human provenance separately.
- **Built.** Laplace-Engine admits ToxiGen as one witness, `ToxiGen`, class AcademicCurated (`recipes/toxigen/source`).
- **Decided.** ToxiGen is one corpus witnessing its records, as a PGN is, and one source trunk and one witness, I3, its trust class keyed by that trunk. The generator, a model and its prompt, and the annotators are participants recorded in each record, as White and Black are in a game, never witnesses; ToxiGen attests that these annotators rated this statement so, and that this model generated it from this prompt, never that the statement is true. No model is the witness, so a model's class such as AIModelProbe is not the trunk's; the trunk takes the class of the corpus that witnesses its records, AcademicCurated as built. [9. Sources](Sources.md) operation 9.4 and the ToxiGen row of the estate, [Corpora: ToxiGen](../Corpora/ToxiGen.md).

## What this page leaves behind

The list of decisions that are the inventor's, and the decisions already made. Every other Sequence page states a decided entry's decision, is written to hold under either answer of an open one where it can, and says which answer it assumed where it cannot.
