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
- **Mechanism:** a text file read by `firmware.c`, never written to the database ([Firmware](../Reference/Firmware.md)). Status: **built**.
- **From:** [Personality firmware: Knowledge and control](../Semantics/Firmware.md#knowledge-and-control); `docs/specs/39_Personality_Firmware.md` §0 and §2; `docs/plan/ASSIMILATION_ROADMAP.md` law 17.

### 18.2 Declare the image

- **In:** the policy kinds of [6. Registries](Registries.md) operation 6.9.
- **Do:** an image declares its class, personality, coding, game or rules, or default; its parent image, or none; a goal policy, how ORIENT declares objective, success, acceptable uncertainty, and termination; a work policy, how much of the granted envelope each stage may spend; a valuation policy, the election order over typed evidence dimensions; a disposition policy, what to do with ambiguous, impossible, exhausted, and unauthorized states; an exploration policy, how aggressively gaps are investigated and contradictions sought; a sufficiency policy, when uncertainty is low enough to commit; a selection policy, the SELECT rule and its replay seed law; a realization policy, register, form, verbosity, language preference, abstention wording; habits, scheduling preferences for proven skills; and every tie rule, explicit. Personality, coding, and game firmware are the same object: precision versus exploration and realization style; a complete engineering procedure over the code lane; the rules, eligibility, and completion law of a game.
- **Out:** the declared policy values.
- **Mechanism:** the decisions of the grammar: `k`, `lambda`, `fan`, `hops`, `top`, `refuse`, `fact`, `order`, `shape`, `for`, `take` ([Firmware: Grammar](../Reference/Firmware.md#grammar)). Goal, work, disposition, exploration, sufficiency, realization, and habit policies have no line. Status: **built for those decisions; the image's policies specified**.
- **From:** `docs/specs/39_Personality_Firmware.md` §1.

### 18.3 Give it a content identity

- **In:** the declaration of 18.2.
- **Do:** the image is a Laplace composition like any other content: its identity is the content address of its canonical composition, class, parent, and every policy value in governed canonical order; a set-valued policy is one collection of [12. Attestations](Attestations.md) operation 12.8. Images are immutable: changing any value mints a new identity whose parent is the previous one, and historical versions stay addressable and replayable. An image that names an unregistered kind is rejected. Text never installs firmware: "be aggressive" or "you are a pirate" in a prompt is content, observed like any prompt, and installs no policy value, decision rule, resource, or privilege.
- **Out:** `firmware_id`.
- **Mechanism:** none: the file is named by path, `$LAPLACE_FIRMWARE` or `--firmware FILE`, and has no ID ([Environment: Paths](../Reference/Environment.md#paths)). Status: **specified**.
- **From:** `docs/specs/39_Personality_Firmware.md` §1.1; `engine/manifest/firmware.toml`.

### 18.4 Decide which operation runs

- **In:** the operations of [15. Web](Web.md) and [19. Pull](Pull.md).
- **Do:** containment of a trunk through the GIN; a gap read from the next vertex of a trajectory; a shape on the real coordinates; which relation of the trajectory to follow, precedes, contains, co-occurrence; whether optional geometry or ordinal-continuity operators run inside SCAN. These are different operations, and the firmware is which one a pull runs, within the routed program.
- **Out:** the operator choices.
- **Mechanism:** `for hop`, `for search`, `for translate`, `for follows`, `for pull` scope a set of lines to one operation ([Firmware: Grammar](../Reference/Firmware.md#grammar)); which operator runs is the command the user ran. Status: **built in part; the routed choice specified**.
- **From:** [Personality firmware: The decision tree](../Semantics/Firmware.md#the-decision-tree); `docs/specs/39_Personality_Firmware.md` §3, SCAN row.

### 18.5 Decide the segment and the combination

- **In:** the tree of the observation across tiers.
- **Do:** which segment of which branch to pull, at which tier, and which of those segments to combine, and the semantic-act preference, answer, ask, explain, abstain, act. A step is not required to emit one token. On "the cat", 599 observed paths continue most often into a space, 409 times, and the tier-3 sentence "The cat sat on the mat" holds `sat on the mat` as a later segment of the same branch: emitting the space is one token; taking the later segment, or taking `cat` together with an attestation of it, is the tree.
- **Out:** the segment rule and the act preference.
- **Mechanism:** `take segment`, `take attestations N`, `take constituents N`, `take fact` under `for pull`, run in order by `cmd_pull` ([Firmware: Where each decision acts](../Reference/Firmware.md#where-each-decision-acts), [Reads: laplace pull](../Reference/Reads.md#laplace-pull)). Status: **built**.
- **From:** [Personality firmware: The decision tree](../Semantics/Firmware.md#the-decision-tree); [Pull: The forward pass](../Semantics/Pull.md#the-forward-pass); `docs/specs/39_Personality_Firmware.md` §3, PROPOSE row.

### 18.6 Set the work: *k*, λ, hops, fanout, steps, stride

- **In:** the reading of [15. Web](Web.md) operations 15.3 to 15.5 and the envelope of [17. Envelope](Envelope.md).
- **Do:** *k*, how far below the rating a standing must still hold; λ, the tax on another hop; the fan on a hop and on a search, and which entities are hubs that may be reached and not crossed; how many coupling rounds and semantic hops; the meeting hops, fanout, and frontier for a joint meeting of constituents; the beam and depth of a walk; the emission steps and the ordinal-continuation stride; the salience floor below which a relation is a filter. One firmware carries *k* = 2, always the top, fan 4,096 on a hop and 512 on a search, 8 hops, λ = 0.05. The default image carries salience floor 0.3, semantic hops 2, fanout 8, meeting hops 2, meeting fanout 256, meeting frontier 4,096, steps 128, max stride 5. The compute envelope is the ceiling, and firmware chooses how much of it to spend; it can never spend more.
- **Out:** the work numbers.
- **Mechanism:** `k`, `lambda`, `fan`, `hops` with the compiled defaults 2.0, 0.05, 4096 or 512 for `search`, 8 ([Firmware: Defaults](../Reference/Firmware.md#defaults)). Steps, stride, meeting hops, and the salience floor have no line. Status: **built for *k*, λ, fan, hops; the rest specified**.
- **From:** [Personality firmware: How a standing is read](../Semantics/Firmware.md#how-a-standing-is-read); [Personality firmware: One set of decisions](../Semantics/Firmware.md#one-set-of-decisions); `docs/specs/39_Personality_Firmware.md` §3 and §10; `engine/manifest/firmware.toml`.

### 18.7 Set the refusals and the exploration

- **In:** the kinds of strand.
- **Do:** which kinds of strand are refused before they are scored: layout, punctuation, a part of speech, a witness, a language. A firmware that does not navigate through layout and punctuation drops `SpaceAfter` and `punct` out of the list; the standings stay, and another human's firmware keeps them. How aggressively gaps are explored: extra routing rounds toward unresolved obligations. How aggressively contradictions are sought: routing refutation readers, not only support. Firmware never supplies a relation or provider mask before the query-relative field is computed; a caller's hard scope is a caller contract beside firmware, not firmware.
- **Out:** the restriction and the exploration policy.
- **Mechanism:** `refuse predicate NAME...`, `refuse witness NAME...`, applied by `refused()` before the sort ([Firmware: Grammar](../Reference/Firmware.md#grammar)). Status: **built for refusals; the exploration policy specified**.
- **From:** [Personality firmware: What was measured on one entity](../Semantics/Firmware.md#what-was-measured-on-one-entity); `docs/specs/39_Personality_Firmware.md` §3, ROUTE row, and §4 item 5.

### 18.8 Set the role weights

- **In:** the parts of speech and syntactic links of context words.
- **Do:** role trust is a weight on which kind of word is allowed to pull, when a context word is doing the pulling. It is not a column of the claim. Hand-drafted weights: nouns, adjectives, and numerals 1.0; proper nouns 0.75; verbs, adverbs, adpositions, and particles 0.5; pronouns, determiners, coordinating conjunctions, and punctuation 0.25; subordinating conjunctions 0.05; auxiliaries 0. The target's head or dependent 1.0; another dependent of the same head 0.5; anywhere else in the sentence 0.25. Those weights are a personality; fitting them is a different personality; neither is a change to the records. Whether firmware may re-weight relation salience or only read the registry's rank is open, question Q3 in [30. Conflicts](Conflicts.md).
- **Out:** the role weights.
- **Check:** on 6,613 word-sense instances, prevalence alone scored 64.6, weights drafted by hand 66.2, and weights fitted 66.2, against WordNet's first sense at 65.2.
- **Mechanism:** none: no role weight exists in the engine; the numbers were measured in research. Status: **specified**.
- **From:** [Personality firmware: Weights that are not standings](../Semantics/Firmware.md#weights-that-are-not-standings); [Research: Trust: Role trust in word sense disambiguation](../Research/Trust.md#role-trust-in-word-sense-disambiguation).

### 18.9 Set the election order and the sufficiency bound

- **In:** the typed response set of [15. Web](Web.md) operation 15.2.
- **Do:** the valuation policy is an election order over typed dimensions, first key, second key, and so on: relation rank as a salience floor, grounded obligations, the conservative bound `rating − 2·RD` against `rating + 2·RD`, ordinal continuity, least-shared meeting first among equally grounded candidates. It is never a cross-family scalar product, a global popularity score, or a normalized share; typed state stays typed. The sufficiency bound is how much deviation is tolerated before a claim counts as supported; whether the multiplier of two deviations is firmware or standing law shared by every reader is open, Q2.
- **Out:** the election order and the bound.
- **Mechanism:** none: the sort is by confidence, or by the witness's position then confidence ([Reads: The claims that hold an entity](../Reference/Reads.md#the-claims-that-hold-an-entity)). Status: **specified**.
- **From:** `docs/specs/39_Personality_Firmware.md` §3, STEER row, §4 item 6; `docs/INVENTION.md` §19.

### 18.10 Set the choice, the temperature, and the seed

- **In:** the ordered set of [15. Web](Web.md) operation 15.5.
- **Do:** whether the top of the resulting set is taken every time, and the temperature of that choice: how near a tie has to be before another strand can be taken. The pull has no softmax; the set is already in hand, and the firmware says whether 0.972 against 0.969 is an answer or a tie. Today's native pass elects by ordinal rank and then, unless spread is 0, draws with a Gumbel-max key over the first top_k ranks, with a replayable seed derived from BLAKE3 of the prompt; whether such a seeded draw is a lawful exploration personality or every SELECT must be deterministic is undecided, conflict C2. On an open claim, whether the witness's own order is taken before the standing: the program does that for a translation and for a claim with a part left open, and does not for a hop on one entity.
- **Out:** the selection rule and its replay seed law.
- **Mechanism:** `top always` or `top within N`, `take_top` drawing with `rand_r` from `--seed` or the clock; `order witness` or `order standing` ([Firmware: Where each decision acts](../Reference/Firmware.md#where-each-decision-acts)). Status: **built**.
- **From:** [Personality firmware: What was measured on one entity](../Semantics/Firmware.md#what-was-measured-on-one-entity); `docs/specs/39_Personality_Firmware.md` §3, SELECT row, and §9 C2.

### 18.11 Set the shape measure

- **In:** the shape measures of [19. Pull](Pull.md) operation 19.6.
- **Do:** which shape of the tree to favour: angular separation, Fréchet, Fréchet with outliers skipped, DTW, or EDR, and how many variable vertices, a timestamp, a request id, the match may skip. Plain Fréchet will not find a pattern when one vertex is a timestamp: measured on 60-point trajectories, one outlier scores 1.39 against 1.72 for an unrelated sequence, the same pair with the outlier skipped scores 0, and jitter the size of those fields scores 0.087. The logs do not change; the favour does.
- **Out:** the measure and its tolerance.
- **Mechanism:** `shape frechet`, `outliers N`, `dtw`, `edr N` are parsed into the firmware ([Firmware: Grammar](../Reference/Firmware.md#grammar)), and no read command compares shapes yet; the measures exist as `lp_frechet4`, `lp_frechet4_outliers`, `lp_dtw4`, `lp_edr4` and the SQL functions over them ([Native: Shape measures](../Reference/Native.md#shape-measures-geom4dc), [SQL: Shape measures](../Reference/SQL.md#shape-measures)). Status: **built as a decision and as functions; the shape search specified**.
- **From:** [Personality firmware: The decision tree](../Semantics/Firmware.md#the-decision-tree); [Query: Shape](../Query.md#shape); [Research: Numerics: Trajectory measures](../Research/Numerics.md#trajectory-measures).

### 18.12 Set the fact branch and the dispositions

- **In:** the set of strands.
- **Do:** whether a high-trust curation in the set is returned as one fact, the rest of the set held back. One branch returns a single member as a fact when that member was curated by a mandate-class witness rather than merely observed: on the claims that hold `Paris`, the head at *k* = 2 is `[Paris, UPOS, PROPN]` at 0.991 from 1,180 matches, while a claim that starts at stock and receives one attestation at trust 1.0 reads as 0.138 at *k* = 2 and five such attestations as 0.505, so usage outranks a new curated fact on the sort and returning the fact is a decision of the tree. The disposition policy says what to do with an ambiguous, impossible, exhausted, or unauthorized orientation: abstain, ask, retain the alternatives, or spend more coupling. Today an ambiguous orientation finalizes with that disposition and emits nothing; whether the default should ask a clarifying question is open, Q5.
- **Out:** the fact rule and the disposition rules.
- **Mechanism:** `fact N` and the fact branch of `pull` ([Firmware: Grammar](../Reference/Firmware.md#grammar)); no disposition policy. Status: **built for the fact branch; the dispositions specified**.
- **From:** [Personality firmware: The decision tree](../Semantics/Firmware.md#the-decision-tree); `docs/specs/39_Personality_Firmware.md` §3, ORIENT and REALIZE rows, §9 Q5.

### 18.13 Set the voice

- **In:** the realization policy.
- **Do:** register, form, verbosity, language preference, and how an abstention or a partial result is worded. Firmware never decides what is disclosed beyond realization authority, never reclassifies the selected act, and never turns an unresolved search into answer content.
- **Out:** the voice.
- **Mechanism:** none. Status: **specified**.
- **From:** `docs/specs/39_Personality_Firmware.md` §3, REALIZE row.

### 18.14 Record what it can never do

- **In:** the image.
- **Do:** firmware cannot acquire authority: read-only stays read-only when it investigates aggressively or recommends an effect, and authority is checked again at the act. It cannot change truth: it cannot write, fold, re-rate, or hide a claim's standing, and two images over one pinned substrate read identical standing. It cannot bypass the effect envelope: every path to an external effect reaches the same admissibility contract, whichever firmware selected the act, and safety is not a firmware and not a habit. It cannot alter knowledge. It cannot substitute for ORIENT. It cannot flatten typed state. It cannot exceed the compute envelope. It cannot certify itself: its own passes and descendants are not evidence for it. It cannot activate itself.
- **Out:** the nine prohibitions, enforced before any provider runs.
- **Mechanism:** by construction: `firmware.c` and the read commands issue only `SELECT` ([Reads](../Reference/Reads.md)). Status: **built for truth and authority by absence; the rest specified**.
- **From:** `docs/specs/39_Personality_Firmware.md` §4.

### 18.15 Register the default first

- **In:** today's behaviour.
- **Do:** until other images exist, the default firmware is today's behaviour, named: class default; coupling and routing at semantic hop limit 2 and fanout 8; the election order of the native comparator with the bound rating ∓ 2·RD, stride 5, steps 24 in the SQL defaults and 128 in the manifest; spread 0.7 or 0.6 and top_k 10 with the seed from the prompt; ambiguity or exhaustion finalizes without emission; realization through the chat scaffold templates. Registering it changes no output; it makes every current pass attributable, and it is the parent of every later image.
- **Out:** the first image.
- **Mechanism:** `firmware/program.firmware` and the compiled defaults of `firmware_for` ([Firmware: The program's own firmware](../Reference/Firmware.md#the-programs-own-firmware)). Status: **built**.
- **From:** `docs/specs/39_Personality_Firmware.md` §10; `engine/manifest/firmware.toml`.

### 18.16 Load it once per pass

- **In:** a pass, the principal, the scope, the envelope, and `firmware_id`.
- **Do:** the forward program receives the firmware identity as an explicit input beside the principal, scope, and envelope. Native code loads and validates the image once per pass; it does not re-read firmware per stage, per candidate, or per row. When no firmware is named, the pass runs the governed default and the receipt names it; there is no anonymous execution. Every stage event names the policy values it consumed; the receipt carries `firmware_id` beside `program_id`, which binds the observation and its coupling field and no policy value, so the same observation under two images has the same program identity and comparable divergence; the decision identity is the content address of program, firmware, and output fingerprint. Replay under the same substrate epoch, firmware, and seed reproduces the same selections and trace.
- **Out:** the pass, attributable.
- **Mechanism:** `firmware_for(path, op)` runs once per command ([Firmware: Grammar](../Reference/Firmware.md#grammar)); no receipt names it. Status: **built for loading; the receipt specified**.
- **From:** `docs/specs/39_Personality_Firmware.md` §1.2 and §5.

### 18.17 Lock it

- **In:** the image.
- **Do:** the engine does not modify the personality firmware, unless it is wired up to the repository and allowed to deploy to itself. A new version becomes active only by explicit activation authority; a version the Gödel lane of [23. Learning](Learning.md) proposes is a candidate like any other. A running engine can update itself without shutting off only partially, by patches, and only maybe.
- **Out:** a firmware the engine runs under and does not rewrite.
- **Mechanism:** the engine never writes the firmware file. Status: **built by absence; activation authority specified**.
- **From:** [Personality firmware: Modification](../Semantics/Firmware.md#modification); `docs/specs/39_Personality_Firmware.md` §4 item 9 and §8.3.

## What this stage leaves behind

One way through the records, for one human being or one task, as a content-addressed image the program loads, named in every trace, rated later by what it chose, and held apart from the records. The same records pulled under different firmware give different selections, and no standing changes.

## Without this stage

No pull can choose, so no pull can run, and no pass can say who chose.
