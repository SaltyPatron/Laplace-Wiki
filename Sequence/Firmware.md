# 18. Firmware

The decisions a pull makes are written as a versioned, content-addressed program over the instruction set, one firmware image per human being or task, loaded once per pass, named in every receipt, rated by its consequences, and kept out of the records.

The world is the tool; firmware is the hand that uses it. Knowledge records what exists and what was observed. Firmware decides what to do with it: which trajectories receive computation, how evidence is valued, how aggressively gaps and contradictions are pursued, when uncertainty is sufficient, how a selection is made, and how a result is expressed. Knowing does not decide doing, and doing never edits knowing. The same world under different firmware behaves differently, and both read the same truth. Personality firmware is the individual steps of the conventional GPT mapped to semantic instruction sets: the operations of [20. Forward](Forward.md), and this is the program over them.

## Before this stage

[15. Web](Web.md): the operations a firmware chooses between. [16. Authority](Authority.md) and [17. Envelope](Envelope.md): the boundaries it can never widen. [6. Registries](Registries.md) operation 6.9: the policy kinds it may bind. Nothing in the records: the firmware is kept out of them on purpose.

## Operations, per firmware image

### 18.1 Separate control from knowledge

- **In:** the records of [11. Content](Content.md) to [13. Consensus](Consensus.md).
- **Do:** the knowledge is the training data: the records of entities, physicalities, claims, attestations, and standings. Governance, control, limitations, restrictions, and behaviour are the firmware. They stay isolated from that knowledge so they do not contaminate it, and every later pull would otherwise inherit someone else's way of navigating it. A record that something exists is not a decision to act with it: guns exist and violence exists, and both can be stored and attested; whether a given pull hops toward that knowledge, fans out through it, or picks it is that human's firmware. Operation, program, firmware, orchestration, OODA, evidence learning, and Gödel extension are separate machine layers, and collapsing any two makes the machine impossible to audit: orchestration that chooses truth or ranking has become a second engine.
- **Out:** a firmware image, separate from the database.
- **From:** [Personality firmware: Knowledge and control](../Semantics/Firmware.md#knowledge-and-control); `docs/specs/39_Personality_Firmware.md` §0 and §2; `docs/plan/ASSIMILATION_ROADMAP.md` law 17.

### 18.2 Declare the image

- **In:** the policy kinds of [6. Registries](Registries.md) operation 6.9.
- **Do:** an image declares its class, personality, coding, game or rules, or default; its parent image, or none; a goal policy, how ORIENT declares objective, success, acceptable uncertainty, and termination; a work policy, how much of the granted envelope each stage may spend; a valuation policy, the election order over typed evidence dimensions; a disposition policy, what to do with ambiguous, impossible, exhausted, and unauthorized states; an exploration policy, how aggressively gaps are investigated and contradictions sought; a sufficiency policy, when uncertainty is low enough to commit; a selection policy, the SELECT rule and its replay seed law; a realization policy, register, form, verbosity, language preference, abstention wording; habits, scheduling preferences for proven skills; and every tie rule, explicit. Personality, coding, and game firmware are the same object: precision versus exploration and realization style; a complete engineering procedure over the code lane; the rules, eligibility, and completion law of a game.
- **Out:** the declared policy values.
- **From:** `docs/specs/39_Personality_Firmware.md` §1.

### 18.3 Give it a content identity (and allow turn-level prompt framing without privilege escalation)

- **In:** the declaration of 18.2, plus any `system`, `developer`, or user instructions on the active turn.
- **Do:** the `.firmware` image is a Laplace composition like any other content: its identity is the content address of its policy declarations; its parent is attested lineage and never hashed; changing any stored policy mints a new `firmware_id` while historical versions stay addressable and replayable. Distinguish **turn-level presentation and framing instructions** from **immutable firmware safety and authority boundaries**: `system`, `developer`, and user prompt instructions legitimately steer turn-level output format (JSON, Markdown, code-only, bullet list), target language, verbosity/conciseness, register, and conversational persona within `ORIENT`, `STEER`, and `REALIZE` for that request or session without mutating the stored `.firmware` image on disk. What prompt text can **never** do is escalate capabilities or authority ([16. Authority](Authority.md)), widen the compute envelope ([17. Envelope](Envelope.md)), bypass governance boundaries, or alter `consensus` standing.
- **Out:** `firmware_id`, plus turn-scoped presentation/framing bindings.
- **From:** `docs/specs/39_Personality_Firmware.md` §1.1; [Reference: Firmware](../Reference/Firmware.md).

### 18.4 Decide which operation runs

- **In:** the operations of [15. Web](Web.md) and [19. Pull](Pull.md).
- **Do:** containment of a trunk through the GIN; a gap read from the next vertex of a trajectory; a shape on the real coordinates; which relation of the trajectory to follow, precedes, contains, co-occurrence; whether optional geometry or ordinal-continuity operators run inside SCAN. These are different operations, and the firmware is which one a pull runs, within the routed program.
- **Out:** the operator choices.
- **From:** [Personality firmware: The decision tree](../Semantics/Firmware.md#the-decision-tree); `docs/specs/39_Personality_Firmware.md` §3, SCAN row.

### 18.5 Decide the segment and the combination

- **In:** the tree of the observation across tiers.
- **Do:** which segment of which branch to pull, at which tier, and which of those segments to combine, and the semantic-act preference, answer, ask, explain, abstain, act. A step is not required to emit one token. On "the cat", 599 observed paths continue most often into a space, 409 times, and the tier-3 sentence "The cat sat on the mat" holds `sat on the mat` as a later segment of the same branch: emitting the space is one token; taking the later segment, or taking `cat` together with an attestation of it, is the tree.
- **Out:** the segment rule and the act preference.
- **From:** [Personality firmware: The decision tree](../Semantics/Firmware.md#the-decision-tree); [Pull: The forward pass](../Semantics/Pull.md#the-forward-pass); `docs/specs/39_Personality_Firmware.md` §3, PROPOSE row.

### 18.6 Set the work: *k*, λ, hops, fanout, steps, stride

- **In:** the reading of [15. Web](Web.md) operations 15.3 to 15.5 and the envelope of [17. Envelope](Envelope.md).
- **Do:** *k*, how far below the rating a standing must still hold; λ, the tax on another hop; the top-standing `fanout` kept on a hop and on a search (filtering unconstrained enum nodes via `mask` while crossing high-degree content hubs via top-standing scans, [15. Web](Web.md) operation 15.5); how many coupling rounds and semantic hops; the meeting hops, fanout, and frontier for a joint meeting of constituents; the beam and depth of a walk or lookahead search; and the emission steps and ordinal-continuation stride. The compute envelope is the hard ceiling, and firmware chooses how much of it to spend; it can never spend more.
- **Out:** the work numbers.
- **From:** [Personality firmware: How a standing is read](../Semantics/Firmware.md#how-a-standing-is-read); [Personality firmware: One set of decisions](../Semantics/Firmware.md#one-set-of-decisions); `docs/specs/39_Personality_Firmware.md` §3 and §10; [Reference: Firmware](../Reference/Firmware.md).

### 18.7 Set domain/plane scope, exclusions, and exploration

- **In:** the eligible planes, mask banks, providers, and strand kinds.
- **Do:** declare which domain planes, `mask` banks, and calculation providers this firmware engages (`chess.firmware` scoping `COUPLE` and `SCAN` directly to chess board, transition, opening, Syzygy, and engine planes without scanning unrelated corpora; `code.firmware` engaging AST, symbol, and toolchain planes; `deductive`..`adversarial` weighting deductive, taxonomic, causal, or refutation channels), always intersected with—and never widening—the caller's hard authority scope ([16. Authority](Authority.md) operation 16.4). Likewise declare which noisy strand kinds are excluded (such as raw punctuation or layout edges in semantic hops), how aggressively unresolved obligations are pursued across extra routing rounds, and whether refutation channels are actively probed alongside support.
- **Out:** the firmware's domain/plane scope, exclusions, and exploration policy.
- **From:** [Reference: Firmware](../Reference/Firmware.md); `docs/specs/39_Personality_Firmware.md` §3.

### 18.8 Set contextual and lexical-fallback role weights

- **In:** the occurrences of a prompt or context window, aligned parse layers, and word-level lexical/UD POS claims.
- **Do:** role weight governs how hard each occurrence pulls as a content obligation versus grammatical framing; it is a `.firmware` decision, never a column of `consensus`. Typical conversational weights assign content nouns, adjectives, and numerals `1.0`, proper nouns `0.75–1.0`, lexical verbs and adverbs `0.5–0.75`, pronouns, determiners, conjunctions, adpositions, and punctuation `0.05–0.25`, and grammatical auxiliaries `0.0–0.1`. Determine each occurrence's part of speech in two tiers so stop-words **never** default to `1.0` obligations when an exact word pair has not been seen in a treebank:
  1. **Contextual alignment first:** where aligned sentence/phrase parse layers or local syntactic context disambiguate the occurrence in place (distinguishing `"can"` as `NOUN` after `"a"` from `"can"` as `AUX` before a bare verb, or `"work"` as `VERB` after `"does ..."`), use that contextual POS reading;
  2. **Word-level lexical/UD POS fallback:** whenever no exact local bigram or span parse matches (`"does lightning"` in `"How does lightning work?"`), fall back immediately to attested word-level lexical and UD POS standings (`[lightning, NOUN]`, `[does, AUX]`, `[How, ADV]`, `[a, DET]`, including single-codepoint Tier-0 words from [12. Attestations](Attestations.md) operation 12.1). Content words (`lightning`) therefore keep full obligation weight while interrogative and auxiliary frame words (`How`, `does`, `is`, `the`, `of`) drop to frame weight instead of matching unrelated sentences like `"How does this shirt fit?"`. Only genuinely unknown out-of-vocabulary identifiers or proper names with zero lexical POS claims default to content weight (`0.75–1.0`).
- **Out:** context-sensitive role weights with guaranteed word-level lexical POS fallback.
- **From:** [Personality firmware: Weights that are not standings](../Semantics/Firmware.md#weights-that-are-not-standings); [Research: Trust: Role trust in word sense disambiguation](../Research/Trust.md#role-trust-in-word-sense-disambiguation); [30. Conflicts](Conflicts.md) S3.

### 18.9 Set the election order and the sufficiency bound

- **In:** the typed response set of [15. Web](Web.md) operation 15.2.
- **Do:** the valuation policy is an election order over typed dimensions, first key, second key, and so on: relation rank as a salience floor, grounded obligations, the conservative bound `rating − 2·RD` against `rating + 2·RD`, ordinal continuity, least-shared meeting first among equally grounded candidates. It is never a cross-family scalar product, a global popularity score, or a normalized share; typed state stays typed. The sufficiency bound is how much deviation is tolerated before a claim counts as supported; whether the multiplier of two deviations is firmware or standing law shared by every reader is open, Q2.
- **Out:** the election order and the bound.
- **From:** `docs/specs/39_Personality_Firmware.md` §3, STEER row, §4 item 6; `docs/INVENTION.md` §19.

### 18.10 Set the choice, the temperature, and the seed

- **In:** the ordered set of [15. Web](Web.md) operation 15.5.
- **Do:** whether the top of the resulting set is taken every time, and the temperature of that choice: how near a tie has to be before another strand can be taken. The pull has no softmax; the set is already in hand, and the firmware says whether 0.972 against 0.969 is an answer or a tie. Today's native pass elects by ordinal rank and then, unless spread is 0, draws with a Gumbel-max key over the first top_k ranks, with a replayable seed derived from BLAKE3 of the prompt; such a draw is as deterministic as always taking the top, both functions of their inputs, and how creative the choice is belongs to the firmware: the method is deterministic and replays from the substrate state, observation, firmware, and seed, while the answer moves with the evidence, conflict C2, decided; the rule inside a near tie is open there. On an open claim, whether the witness's own order is taken before the standing: the program does that for a translation and for a claim with a part left open, and does not for a hop on one entity.
- **Out:** the selection rule and its replay seed law.
- **From:** [Research: Semantics Experiments: What was measured on one entity](../Research/Semantics-Experiments.md#what-was-measured-on-one-entity); `docs/specs/39_Personality_Firmware.md` §3, SELECT row, and §9 C2.

### 18.11 Set the shape measure

- **In:** the shape measures of [19. Pull](Pull.md) operation 19.6.
- **Do:** which shape of the tree to favour: angular separation, Fréchet, Fréchet with outliers skipped, DTW, or EDR, and how many variable vertices, a timestamp, a request id, the match may skip. Plain Fréchet will not find a pattern when one vertex is a timestamp: measured on 60-point trajectories, one outlier scores 1.39 against 1.72 for an unrelated sequence, the same pair with the outlier skipped scores 0, and jitter the size of those fields scores 0.087. The logs do not change; the favour does.
- **Out:** the measure and its tolerance.
- **From:** [Personality firmware: The decision tree](../Semantics/Firmware.md#the-decision-tree); [Query: Shape](../Query.md#shape); [Research: Numerics: Trajectory measures](../Research/Numerics.md#trajectory-measures).

### 18.12 Set the fact branch and non-silent ambiguity dispositions

- **In:** the set of strands and candidate interpretations.
- **Do:** decide when a curated fact leads directly and how polysemy, partial obligation coverage, or contested evidence is expressed—**never aborting silently with `budget = 0` or empty output merely because multiple valid senses tie or a multi-part prompt spans several claims**:
  1. When one interpretation or sense leads clearly by joint contextual fit, empirical usage (`tokens` / `tag_cnt`), and conservative standing, answer directly from that strongest attested structure (and compose multiple clauses when different obligations are grounded by complementary attested claims);
  2. When multiple senses are genuinely co-equal on an underspecified prompt or independent high-trust witnesses actively disagree, surface the primary attested senses or contested perspectives explicitly with their provenance; or
  3. When a user action or narrow query requires disambiguation before proceeding, ask one concise clarifying question naming the alternatives.

  Reserve `ABSTAIN` strictly for when **zero relevant witnessed evidence exists** in the authorized world (or when [16. Authority](Authority.md) forbids disclosure) ([30. Conflicts](Conflicts.md) Q5).
- **Out:** the fact rule and non-silent ambiguity/partial-coverage dispositions.
- **From:** [Personality firmware: The decision tree](../Semantics/Firmware.md#the-decision-tree); `docs/specs/39_Personality_Firmware.md` §3, ORIENT and REALIZE rows; [30. Conflicts](Conflicts.md) Q5.

### 18.13 Set the voice

- **In:** the firmware's realization defaults and any turn-level `system`/`developer`/user style instructions from 18.3.
- **Do:** set register, output format (prose, Markdown, JSON, code), verbosity, target language preference, and clear wording for contested evidence or genuine abstention. Turn-level style, language, verbosity, and persona instructions refine realization within the principal's realization authority without reclassifying unsupported guesses into facts.
- **Out:** the voice and output-format contract.
- **From:** `docs/specs/39_Personality_Firmware.md` §3, REALIZE row.

### 18.14 Record what it can never do

- **In:** the image.
- **Do:** firmware cannot acquire authority: read-only stays read-only when it investigates aggressively or recommends an effect, and authority is checked again at the act. It cannot change truth: it cannot write, fold, re-rate, or hide a claim's standing, and two images over one pinned substrate read identical standing. It cannot bypass the effect envelope: every path to an external effect reaches the same admissibility contract, whichever firmware selected the act, and safety is not a firmware and not a habit. It cannot alter knowledge. It cannot substitute for ORIENT. It cannot flatten typed state. It cannot exceed the compute envelope. It cannot certify itself: its own passes and descendants are not evidence for it. It cannot activate itself.
- **Out:** the nine prohibitions, enforced before any provider runs.
- **From:** `docs/specs/39_Personality_Firmware.md` §4.

### 18.15 Ship baseline `.firmware` profiles

- **In:** the governed directive set of [6. Registries](Registries.md) operation 6.9.
- **Do:** ship `firmware/program.firmware` as the attributable baseline conversational profile alongside specialized profiles (`deductive`, `inductive`, `abductive`, `constructive`, `adversarial`, `chess`), each content-addressed: contextual + lexical-fallback POS role weights (18.8), top-standing hub traversal (`fanout` without hub dead-ends, 18.6), conservative standing `rating − k·RD`, multi-clause composition over attested claims and trajectories rather than rigid scaffold templates, non-silent polysemy/dispute handling (18.12), and `ABSTAIN` reserved strictly for zero relevant witnessed evidence.
- **Out:** `program.firmware` and the shipped reasoning/domain `.firmware` suite.
- **From:** [Reference: Firmware](../Reference/Firmware.md); `docs/specs/39_Personality_Firmware.md` §10.

### 18.16 Load it once per pass

- **In:** a pass, the principal, the scope, the envelope, and `firmware_id`.
- **Do:** the forward program receives the firmware identity as an explicit input beside the principal, scope, and envelope. Native code loads and validates the image once per pass; it does not re-read firmware per stage, per candidate, or per row. When no firmware is named, the pass runs the governed default and the receipt names it; there is no anonymous execution. Every stage event names the policy values it consumed; the receipt carries `firmware_id` beside `program_id`, which binds the observation and its coupling field and no policy value, so the same observation under two images has the same program identity and comparable divergence; the decision identity is the content address of program, firmware, and output fingerprint. Replay under the same substrate epoch, firmware, and seed reproduces the same selections and trace.
- **Out:** the pass, attributable.
- **From:** `docs/specs/39_Personality_Firmware.md` §1.2 and §5.

### 18.17 Lock it

- **In:** the image.
- **Do:** the engine does not modify the personality firmware, unless it is wired up to the repository and allowed to deploy to itself. A new version becomes active only by explicit activation authority; a version the Gödel lane of [23. Learning](Learning.md) proposes is a candidate like any other. A running engine can update itself without shutting off only partially, by patches, and only maybe.
- **Out:** a firmware the engine runs under and does not rewrite.
- **From:** [Personality firmware: Modification](../Semantics/Firmware.md#modification); `docs/specs/39_Personality_Firmware.md` §4 item 9 and §8.3.

## What this stage leaves behind

One way through the records, for one human being or one task, as a content-addressed image the program loads, named in every trace, rated later by what it chose, and held apart from the records. The same records pulled under different firmware give different selections, and no standing changes.

## Without this stage

No pull can choose, so no pull can run, and no pass can say who chose.
