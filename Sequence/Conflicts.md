# 30. Conflicts

The wiki's specification pages and the monorepo's invention documents state some things differently, and each difference is recorded here as both positions with their sources, with the inventor's decision where one has been made and open for the inventor where none has.

An entry marked **Decided** records the canonical resolution implemented across the unified substrate (`Laplace-Native`, `Laplace-postgres`, `Laplace-Engine`, and `Laplace`), and the Sequence pages state it directly so engineering work never stalls on superseded pre-modular drafts. Entries still marked **Open** record genuine future research questions that do not block Laplace 1.0.

## Placement and packing

### P1. Rank *r* takes the *r*-th Hilbert-ordered point, or the open radical-inverse point

- **Wiki.** [4. Projection](Projection.md): n = 1,114,112 Super-Fibonacci points with φ = √2 and ψ = 1.5337…, sorted by Hilbert value, and DUCET rank *r* takes the *r*-th point of the walk (`Laplace-Native/src/tier0.c`). n is fixed to the Unicode codespace and every point is permanent within a Unicode version. [Atoms: Placement](../Storage/Atoms.md#placement), [Research: Placement](../Research/Placement.md).
- **Monorepo.** `docs/INVENTION.md` §2 and §17.2: tier-0 placement was written as the open radical-inverse law `t = radicalInverse(rank)` with no terminal N.
- **Agree.** Both place all 1,114,112 codepoints on the S³ in DUCET order, both derive `lp_id` strictly from UTF-8 bytes of the codepoint and never from the point or rank, and both fingerprint `tier0.bin`.
- **Decided for `tier0.bin` (with open research note on post-1,114,112 extension).** `Laplace-Native` (`src/tier0.c`) implements the 1,114,112 Hilbert-ordered Super-Fibonacci placement (`tier0.bin` 64-byte `lp_tier0_record`), which preserves collation-neighbor spatial locality on the S³ ([Research: Placement](../Research/Placement.md)). Because Unicode's codespace ceiling `U+10FFFF` (1,114,112 scalar positions) has been fixed by the Unicode Stability Policy since Unicode 2.0, `n = 1,114,112` covers the entire standard.

### P2. The vertex packs 43/43/42 bits of ID with 28 spare bits, or 212 bits

- **Wiki & `Laplace-Native`.** [11. Content](Content.md) operation 11.7 and `include/laplace/laplace.h` (`lp_id_to_xyz`, `lp_xyz_to_id`, `lp_xyz_spare`, `lp_m_*`): the 128-bit `lp_id` is packed into the low `43 + 43 + 42 = 128` mantissa bits of X, Y, Z at biased exponent 1021 (values in `[0.25, 0.5)`), leaving `9 + 9 + 10 = 28` upper mantissa spare bits (`4-bit tag + 24-bit payload`), while `M` is an exact integer-valued binary64 carrying `run` (bits `0..29`, 30b), `said` role (bits `30..32`, 3b), `outcome` (bits `33..34`, 2b), and `position` (bits `35..52`, 18b). [Reference: Formats](../Reference/Formats.md).
- **Legacy monorepo.** `Laplace/engine/core/src/mantissa.c`: packed `53/53/22` using the sign bit (212 bits total), retired under `one-substrate`.
- **Decided.** `43/43/42 + 28 spare` in X/Y/Z at biased exponent 1021 (`[0.25, 0.5)`) plus `run30 / said3 / outcome2 / pos18` in `M`, encoded as binary EWKB `POINT ZM` (37 B) or `LINESTRING ZM` (`9 + 32n` B). Constituent order is the vertex sequence itself with adjacent repeats run-length encoded in `M`; carrier doubles are never spatial coordinates and are unpacked to real `entity.coord` before any 4D metric (`frechet4d`, `dtw4d`, `edr4d`).

### P3. A composition's coordinate is the exact integer centroid, or a Karcher mean

- **Wiki & `Laplace-Native`.** [11. Content](Content.md) operation 11.6 and `Laplace-Native/src/coord.c`: the exact `__int128` integer average of the children's fixed-point coordinates (`trunc((Σ m_d) / n)` toward zero), which guarantees by convexity that every composition sits strictly inside the 4-ball wall (`Σ m_d² ≤ 2¹⁰⁶`).
- **Legacy monorepo.** Managed model, chess, and collection code once used an iterative floating-point Karcher mean to obtain permutation invariance on sets.
- **Decided.** One universal placement law everywhere: the **exact `__int128` integer centroid** (`lp_coord_centroid`). Because every collection ([12. Attestations](Attestations.md) operation 12.8) sorts its distinct member `lp_id`s ascending before composing, its constituent sequence—and therefore its exact integer centroid—is already strictly permutation-invariant without iterative floating-point spherical means.

### P4. Content partitioned by tier, and claims by hex prefix

- **Earlier experiments.** Partitioning `entity` and `physicality` 256 ways by the first byte of `id` forced upward containment queries (`laplace_couple`, `holds`) to touch all 256 GIN partitions on every lookup (~108–233 ms per word).
- **Decided.** `Laplace-postgres` (`sql/laplace.sql.in`, [Reference: Schema](../Reference/Schema.md#the-four-tables)) range-partitions `entity` and `physicality` into **9 tier partitions (`t0`..`t8plus`, `RANGE (tier)`)** with PK `(tier, id)` / `(tier, entity)` and per-partition `UNIQUE (id)` / `UNIQUE (entity)`, and range-partitions `attestation` and `consensus` **16 ways by the first hex digit of `claim` (`_0`..`_f`, `RANGE (claim)`, `fillfactor = 80`)**. Because every container sits strictly above its constituents (`tier = 1 + max(child.tier)`), upward containment lookups prune lower and equal tier partitions immediately, while claim/standing probes prune to 1 of 16 hex partitions and update `consensus` HOT off the GIN-indexed `physicality` heap. [8. Database](Database.md) operation 8.10.

## Firmware and witnessing

### C1. Do Laplace's own outputs, and user prompts, become attestations?

- **Inventor & Wiki.** Normal digital content and user prompts create exact observation and trajectory state and **zero semantic attestations** merely by being said; Laplace's own generated responses sit at `ResponseContent` (0.20), below `UserPromptContent` (0.30), and never self-certify as factual truth. `docs/INVENTOR_RECORD.md` §Attestations.
- **Decided.** Prompts decompose in C memory from `tier0.bin` in microseconds with zero synchronous DB `COPY` before answering and emit zero semantic attestations merely by being spoken ([22. Users](Users.md) operations 22.5 and 22.6). At turn completion, episodic session turns (`[prompt, response]`) are recorded on the session trajectory (`turn_witness` in `src/program.c`, or skipped on stateless read-only calls, [21. Sessions](Sessions.md) operation 21.5) as discourse provenance rather than factual truth claims. Explicit user feedback (`confirm` / `refute`) and verified external consequences (compiler/test results, game outcomes, tool executions) enter through governed witnessing bounded by causal lineage and Sybil governance ([16. Authority](Authority.md) operation 16.4).

### C2. Is SELECT deterministic?

- **Inventor, 2026-10-06 & 2026-09-04.** "the METHOD is deterministic... The steps and operations are all auditable, loggable, etc... Provenance and mechanistic interpretability are maintained... AI with ACID compliance." "how creative is it? How by the book is it? Does it care? (Random top-k? top-1? low hop count?)"
- **Decided.** A pass is a pure, deterministic function of `(substrate snapshot, observation, firmware, seed)` and replays identically from those inputs, while answers evolve naturally as new evidence is ingested into the world. At `temperature = 0` (`spread = 0`), `SELECT` deterministically elects the top-ranked candidate (`claim_id ASC` tie-break); at `temperature > 0`, `.firmware` permits seeded near-tie selection within overlapping confidence bounds using the caller's `seed` (or a deterministic BLAKE3 seed of the prompt/turn), mapping OpenAI `/v1/chat/completions` `temperature` and `seed` directly without reducing typed evidence to a dense-logit softmax ([18. Firmware](Firmware.md) operation 18.10; [21. Sessions](Sessions.md) operation 21.4).

### C3. Is the Gödel engine the OODA loop?

- **Inventor.** "compile failed... negative attestation... next iteration ... oh wait, we tried this… it failed hard... abort, rethink... try again... compile... positive attestation... next step... This is what my godel engine is for" (2026-08-09); and "use incompleteness as a discovery signal" (2026-08-24). `docs/INVENTOR_RECORD.md` §Gödel engine.
- **Decided.** Both halves belong to one unified Gödel OODA architecture in `program.c` and [23. Learning](Learning.md): (1) the **runtime consequence-driven OODA loop** over `Forward` (`BELIEF ≠ RISK ≠ ACTION`, updating active state in memory across clauses and turning verifier/compiler/test/search failures into negative evidence that steers the next attempt) and (2) the **structural incompleteness / bridge discovery lane** (`COMBINE` and typed fray hypotheses that activate only when corroborated by disjoint evidence).

### C4. Trust bounds each vote, and dependence caps causal lineage—never trust classes

- **Earlier bug.** Playing a witness as a fixed-1500 opponent whose trust only widened its deviation inverted Glicko-2 over long series (letting low-trust witnesses push ratings higher than high-trust witnesses), while an opposite over-correction proposed capping all witnesses in the same `trust_class` as a single root—which would prevent `Llama`, `Qwen`, and `DeepSeek` (or `UD`, `FrameNet`, and `VerbNet`) from corroborating one another!
- **Decided.** Implemented in `Laplace-Native` (`lp_attest_series`) and `Laplace-postgres` (`laplace_attest_series`):
  1. **Trust bounds each series' effective score:** *s*_eff = 0.5 + *t*(*s* − 0.5), solved in O(1) by concave log-posterior bisection over the witness's `games`, strictly monotone in trust *t* with a per-witness deviation floor; negative *t* inverts reliably wrong witnesses.
  2. **Dependence-root capping applies strictly to shared causal `lineage` and Sybil-governed unverified accounts—never across an entire `trust_class`:** OEWN and Princeton WordNet share `WordNet` lineage and count as one root on copied synsets, whereas independently curated corpora (`UD`, `FrameNet`, `VerbNet`) and independently trained models (`Llama`, `Qwen`, `DeepSeek` at `AIModelProbe`) have distinct causal roots and genuinely corroborate one another at the round table ([13. Consensus](Consensus.md) operations 13.2 and 13.3; [24. Models](Models.md) operation 24.10).
  3. **Empirical frequencies are preserved:** UD corpus token occurrences (`games` / `tokens`) and SemCor/WordNet `tag_cnt` sense counts are preserved rather than flattened from 800 occurrences to 1 game ([12. Attestations](Attestations.md) operation 12.9).

### C5. Coarse native C lookahead search inside `Forward`

- **Question.** How lookahead / tree search over legal transitions (such as playing chess or verifying multi-step repairs) fits inside `Forward`.
- **Decided.** Bounded lookahead search is a native C operator inside `SCAN`, `PROPOSE`, and `STEER` ([20. Forward](Forward.md), [27. Chess](Chess.md) operation 27.6), steered by `.firmware` (`chess.firmware`) within the request's compute/clock envelope. It expands legal transitions in C memory over mapped ROMs (`chess.bin`, Syzygy tablebases), exact domain evaluators, and batch-probed `consensus` / OTB trajectory priors with **zero per-node database round trips**. Imagined search branches never self-witness into durable tables; only played moves and verified tool/compiler outcomes are witnessed.

### C6. Domain/plane scoping in `.firmware` versus caller authority scope

- **Question.** Whether `.firmware` may scope planes and exclude noisy strands or witnesses when `consensus` is pre-folded.
- **Decided.** Domain and task `.firmware` files (`chess.firmware`, `code.firmware`, `deductive.firmware`) lawfully declare eligible domain planes, `mask` banks, operator families, and strand exclusions so `COUPLE` and `SCAN` do not waste probes on unrelated planes ([18. Firmware](Firmware.md) operation 18.7; [20. Forward](Forward.md) operation 20.2), always intersected with—and never widening—the caller's hard authority scope ([16. Authority](Authority.md) operation 16.4). Witnesses are identified by their source trunk `lp_id`; when an ablation or scoped export explicitly excludes a witness (`24.9`, `25.1`), `attestation` series are refolded over the authorized witness subset in native C without mutating global `consensus`.

### C7. Explicit disposition codes in `Forward`

- **Decided.** `Forward` receipts name the exact disposition (`complete`, `clarification_requested`, `contested_perspectives`, `declined_by_firmware`, `abstain_no_evidence`, `unauthorized`, `envelope_exhausted`) so a firmware or governance refusal is never confused with missing knowledge ([20. Forward](Forward.md) operation 20.12).

### C8. Static weight assimilation plus optional deep-head activation tracing

- **Monorepo & Research.** Static weight contraction recovers embeddings, unembeddings, and direct factor circuits directly from Safetensors/GGUF tiles (`raw_weight_bytes_retained = 0`), while [Research: Model Ingestion](../Research/Models.md) showed that deep residual-stream heads operate in context-rotated bases best observed on reference trajectories.
- **Decided.** Checkpoint assimilation ([24. Models](Models.md) operations 24.6 to 24.8) runs static native C weight contraction with **empirically calibrated two-sided significance thresholds** (preserving both excitatory and inhibitory/suppressive circuits rather than hardcoding a one-sided Gaussian `z ≥ +√(2 ln N)` floor), **and** permits optional deterministic CPU activation/circuit tracing over pinned corpus trajectories (or companion sparse-dictionary/transcoder checkpoints) under a versioned calculation recipe to capture deep contextual head behavior.

### Q1 to Q5

- **Q1 (Open).** Whether firmware standing uses a participant rating curve (like a chess player) or a source-style series record; in both cases firmware never has a truth-witness trust class over claims.
- **Q2 (Decided).** The conservative multiplier *k* in `rating − k·RD` is a `.firmware` parameter (`k = 2` default in `program.firmware`, tunable per reasoning profile, [18. Firmware](Firmware.md) operation 18.6).
- **Q3 (Decided).** Global magic salience float tables are retired; predicate and POS role weights live in `.firmware` (`weigh`, `role`, [6. Registries](Registries.md) operation 6.3 and [18. Firmware](Firmware.md) operation 18.8).
- **Q4 (Open).** Whether orchestration may auto-select among already-authorized `.firmware` profiles by task standing when the caller leaves firmware unset, versus always binding `program.firmware`.
- **Q5 (Decided).** **Never abort silently with `budget = 0` on sense ties or partial single-node obligation coverage:** `Forward` answers from the strongest/shared attested structure (composing multi-clause answers across complementary claims), surfaces contested or polysemous perspectives when genuinely disputed, or asks one concise clarifying question—reserving `ABSTAIN` strictly for when zero relevant witnessed evidence exists or authority denies disclosure ([18. Firmware](Firmware.md) operation 18.12; [20. Forward](Forward.md) operations 20.3, 20.8, 20.10).

## Tables and registries

### T1. Four persistent substrate tables (`entity`, `physicality`, `attestation`, `consensus`) plus `app.*` and ROM perf-caches

- **Inventor.** "Entity, Physicality, Attestation, Consensus... why do i need more tables than this"; lookup tables and salted canonical-name hashes are hacks. `docs/INVENTOR_RECORD.md` §Entities.
- **Decided.** `CREATE EXTENSION laplace` (`Laplace-postgres/sql/laplace.sql.in`, [Reference: Schema](../Reference/Schema.md)) defines **four** persistent substrate tables—`entity`, `physicality`, `attestation`, and `consensus`—with zero `source`, `witness`, `claim`, `statistics`, or `ByteAtoms` side tables. Sources, files, records, collections, and claims are ordinary `entity` + `physicality` rows indexed by the composite `(path laplace_path_ops, mask laplace_mask_ops)` GIN; governed `bit(64)` mask banks (`manifest/banks.tsv`) and highway slots (`highway.bin`) are memory-mapped ROM perf-caches over content-derived entities ([6. Registries](Registries.md)); and conventional auth, session, compute-envelope, and `app.billing_royalties` (`SUM(share_bp) = 10000`) tables live in the `app.*` schema inside the same `laplace` database ([8. Database](Database.md) operation 8.7).

### T2. Claim `lp_id` and 64-bit `mask`

- **Decided.** A claim is an n-ary composition of content `lp_id`s of any arity and any tier (`[dog, eng, i46360]`, `[France, capital, Paris]`, `[Q142, P36, Q90]`, `[dog, NOUN]`), hashed identically to any composition (`11.5`), never `BLAKE3(subject || type || object)` with zero-padding. `consensus` is keyed on `claim`; `attestation` is keyed on `(claim, witness, lineage)` with `UNIQUE NULLS NOT DISTINCT`; and `entity.mask` / `physicality.mask` carry the 64-bit `bit(64)` acceleration fields from `manifest/banks.tsv` (`kind`, `upos`, `lexfile`, `deprel`, `vnrole`, `wnframe`). Any content entity may serve as a claim predicate without C manifest edits ([6. Registries](Registries.md) operations 6.1 and 6.2; [12. Attestations](Attestations.md) operations 12.5 to 12.7).

### T3. Set-based series solving (`lp_attest_series`), zero delayed ETL folds

- **Decided.** Each witness asserting a claim *n* times plays one trust-bounded Glicko-2 series of *n* games, solved in O(1) via concave log-posterior bisection (`lp_attest_series` / `laplace_attest_series`) and merged in set-based batches into `attestation` and `consensus` as sources are admitted—never per-row RBAR, never linearized single-period jumps that explode over 1,000 games, and never delayed background ETL jobs ([13. Consensus](Consensus.md) operations 13.4 and 13.5).

## Reading standings

### R1. Cost `−ln p + λ` inside A* search versus typed multi-plane election

- **Agree & Practice.** Search operators inside `SCAN` (such as Highway A* and `degrees`, [15. Web](Web.md) operations 15.4 and 15.7) use `−ln p + λ` as an admissible non-negative path cost on a traversed channel, while `ORIENT` and `STEER` preserve separate typed dimensions (obligation coverage, conservative standing, empirical token/sense counts, continuity, provenance) in their election order rather than collapsing the whole world into one opaque scalar.

### R2. Deterministic repeatable-read snapshots and top-standing hub scans

- **Decided.** Every multi-probe read command runs under one repeatable-read snapshot; unconstrained enum nodes (`NOUN`, `eng`) act as `mask`/crosswalk filters rather than blind expansion pivots; and high-degree content hubs (`Paris`, `France`, `dog`, `i46360`) execute bounded top-standing scans ordered deterministically by `(confidence DESC, claim_id ASC)` rather than becoming uncrossable dead ends at `fanout = 8` or returning arbitrary heap order ([15. Web](Web.md) operation 15.5).

### R3. Replaying a historical pass across substrate growth

- **Open.** Because `consensus` updates in place as new sources and consequences arrive, bit-exact replay of an old turn after later ingestions requires either replaying from the turn receipt's recorded cell standings or pinning a historical snapshot/epoch (as ranked Arena challenges do in [28. Games](Games.md) operation 28.2).

### R4. Time-varying participant ratings (chess players) versus claim consensus

- **Agree & Open research.** Stated header Elos (`HAS_RATING`), Ordo tournament ladder ratings ([27. Chess](Chess.md) operation 27.7), and time-varying player strength curves ([Research: Chess](../Research/Chess.md#order-free-ratings)) stay strictly separate from factual claim standing in `consensus` so amateur game counts never place club players above Magnus Carlsen. Whether Whole-History Rating is also offered as an optional participant-rating analyzer for players and witnesses remains open research.

## Strands and meaning

### S1. Highway and cross-dataset identifiers (`i46360`, `oewn-*` when `ili="in"`, `Q937`, `geonameid`) versus ephemeral file-local pointers

- **Decided.** Recipes distinguish three cases cleanly ([10. Recipes](Recipes.md) operation 10.11):
  1. **Shared highway and cross-dataset external identifiers**—CILI `i46360`, PropBank `abandon.01`, VerbNet `give-13.1`, FrameNet frames/FEs/LUs, VerbAtlas `va:0001f`, ISO 639 codes (`eng`), FIDE player IDs, Wikidata items and properties (`Q937`, `Q142`, `P36`, `P1566`), and external authority keys such as `geonameid` when cited across datasets (Wikidata `P1566` ↔ GeoNames ↔ Natural Earth)—are canonical content/highway nodes (`i46360` is `[i,4,6,3,6,0]`, `Q937` is `[Q,9,3,7]`), linking every source that cites them by exact `lp_id` collision.
  2. **Unmapped WordNet/OEWN synsets (`ili="in"`):** while synsets with a CILI `i*` ID resolve to that `i*` node, synsets not yet assigned a CILI `i*` number (`ili="in"` in OEWN) **keep their stable `oewn-*` synset ID as their concept node** until CILI maps them—preserving distinct synset identity even when 19,619 synsets share word lists (`drop`).
  3. **Ephemeral file-local and release-local pointers**—WordNet byte offsets (`01976841` in `data.verb`), WSD instance IDs (`d000.s000.t000`), sense keys (`dog%1:05:00::`, see I7), FrameNet internal XML IDs, CoNLL-U token ordinals and `sent_id`, Tatoeba internal row numbers—decompose only for embedded grammatical facts, resolve at ingest to the target entity or lexicalization strand, and are recorded nowhere.

### S2. Claim entry defaults

- **Decided.** Claims enter `consensus` at Glicko-2 stock (`rating = 1500`, `deviation = 350`, `volatility = 0.06`), and every witness series plays via `lp_attest_series` bounded by that witness's trust *t* ([13. Consensus](Consensus.md) operations 13.1 and 13.2), while read-time predicate and POS weighing stay in `.firmware`.

### S3. Open-ended content predicates and contextual + lexical-fallback POS role weights

- **Decided.** English manifest handles are never identity, any content entity may serve as a claim predicate without C rebuilds, and hardcoded magic float salience tables (`0.12` burying numbers) are retired ([6. Registries](Registries.md) operations 6.1 and 6.3). At read time ([18. Firmware](Firmware.md) operation 18.8; [20. Forward](Forward.md) operation 20.3), `.firmware` weighs predicates by content and determines each prompt token's POS weight in two tiers: **contextual parse alignment first** (disambiguating `"can"` noun vs aux in context), followed immediately by **word-level lexical/UD POS fallback** (`[lightning, NOUN]`, `[does, AUX]`, `[a, DET]`) whenever an exact local bigram is unseen—guaranteeing that stop-words never default to `1.0` obligations or overpower content nouns!

### S4. Detached `.firmware` files with content-addressed receipts

- **Decided.** `.firmware` profiles (`program.firmware`, `deductive`..`adversarial`, `chess`) live outside the substrate's factual records so policy never contaminates truth, while each loaded image's canonical content hash (`firmware_id`) is recorded in turn/game receipts for deterministic audit and consequence rating ([18. Firmware](Firmware.md) operations 18.1, 18.3, 18.16).

## Identity

### I1. Pure child-ID composition hash (zero domain byte)

- **Decided.** Leaves hash the 1..4 UTF-8 bytes of one codepoint; `n == 1` collapses to the child itself (so single-character words like `"a"`, `"I"`, `"犬"` are Tier-0 entities and legitimately receive lexical/POS attestations, [12. Attestations](Attestations.md) operation 12.1); `n >= 2` hashes the $16n$ child bytes with zero `0x01` domain prefix, zero tier prefix, and zero salt ([11. Content](Content.md) operation 11.5).

### I2. Same content = same hash

- **Decided.** Equal canonical content has the exact same `lp_id` across every source and modality (`"King"` in Qwen == `"King"` in WordNet == `"King"` in Wikipedia == `"King"` in Chess == `"King"` in ASTs; `255 → ['2','5','5']` in pixels == bytes == IPv4 == prose). Recipes govern decomposition structure without ever salting hashes ([10. Recipes](Recipes.md) operations 10.5 and 10.6).

### I3. Witness identity is the source trunk (with replaceable sub-source trunks under multi-author collections)

- **Decided.** Every witness is a source trunk `[source record, its files' trunks in path order]`—never a salted string like `substrate/source/X/v1` ([9. Sources](Sources.md) operation 9.4; [12. Attestations](Attestations.md) operation 12.2). Multi-author umbrella collections (such as Universal Dependencies' 353 treebanks and Open Multilingual Wordnet's 32 language lexicons) allow individual treebanks and lexicons to stand as independently replaceable and corroborating sub-source trunks under the parent collection trunk (sharing `lineage` only where causally derived from the same upstream source), whereas individual annotators, crowd workers, speakers, and game players inside a dataset remain participant content entities inside records.

### I4. Curated sources have trunks without requiring bit-exact container bytes

- **Decided.** Curated sources, their files, and their records all form canonical trunks in the Merkle DAG for containment provenance, while compressed containers store lossless decoded content without requiring deflate-encoder-choice diffs ([10. Recipes](Recipes.md) operation 10.8; [11. Content](Content.md) operation 11.2). Operational ingest journals may check raw file byte-hashes on disk to skip re-parsing unchanged completed files before Tree-sitter/UAX #29 runs, without raw byte-hashes ever replacing `lp_id`.

### I5. External identifiers: highway content versus ephemeral pointers

- **Decided.** Shared highway and cross-dataset identifiers (`i46360`, `abandon.01`, `va:0001f`, `eng`, `Q937`, `P36`, cross-referenced `geonameid`, and `oewn-*` when `ili="in"`) are canonical content entities, while ephemeral file-local pointers (`d000.s000.t000`, release byte offsets, `sent_id`, internal row numbers) decompose for embedded facts, resolve at ingest, and are recorded nowhere (S1 above; [10. Recipes](Recipes.md) operation 10.11).

### I6. Repetition, RLE, and empirical corpus counts

- **Decided.** Run-length encoding (`run` in vertex `M`) compresses adjacent identical constituents in a path and never multiplies witness authority. Within a curated source, genuine empirical corpus occurrences—such as 800 annotated tokens of `[dog, NOUN]` in a UD treebank or SemCor `tag_cnt` counts—preserve their full `games` and `tokens` counts in `attestation` (folded via `lp_attest_series` up to the witness's trust ceiling and kept readable for empirical sense/POS disambiguation), while artificial Cartesian join repeats in denormalized mapping tables are deduplicated per logical assertion ([12. Attestations](Attestations.md) operation 12.9; [13. Consensus](Consensus.md) operation 13.4).

### I7. WordNet sense keys resolve through `highway.bin`

- **Decided.** A WordNet sense key (`dog%1:05:00::`) is decomposed by grammar into lemma, POS, and `lexfile`, resolved through `highway.bin` to the target lexicalization strand and concept, and not recorded as a standalone entity ([10. Recipes](Recipes.md) operation 10.11).

### I8. Language is an ISO 639 constituent in the lexicalization strand

- **Decided.** Language is an ISO 639 highway entity inside the n-ary lexicalization composition (`[dog, eng, i46360]`), never a separate SQL column or `bit(64)` mask bank ([12. Attestations](Attestations.md) operation 12.5).

### I9. ToxiGen is one corpus trunk witnessing participant annotations

- **Decided.** ToxiGen is admitted under one `AcademicCurated` corpus witness trunk; the generator model, prompt, and human annotators are participant entities in each record, attesting how each statement was generated and rated rather than asserting harmful text as truth ([9. Sources](Sources.md) operation 9.4; [Corpora: ToxiGen](../Corpora/ToxiGen.md)).

## Chess

### K1. The ladder's conductor: `fastchess` for matches and SPRT, `cutechess` for watched GUI play

- **Decided (2026-10-06).** `fastchess` conducts automated engine matches, pentanomial SPRT gates across ablation rungs, CPU-affinity pinning (`-use-affinity`), and UCI compliance checks; `cutechess` conducts watched GUI sessions and cross-checks; and Ordo computes chess-ladder ratings over closed match sets, kept strictly separate from Laplace `consensus` Glicko-2 standings ([27. Chess](Chess.md) operation 27.7).

## What this page leaves behind

Every architectural conflict resolved into one coherent, compounding specification across `Laplace-Native`, `Laplace-postgres`, `Laplace-Engine`, and `Laplace`, with the remaining open items (`Q1`, `Q4`, `R3`, `R4`) explicitly scoped as non-blocking research refinements.
