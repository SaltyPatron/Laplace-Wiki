# 20. Forward

One stateful, typed program answers every request: RESOLVE, COUPLE, ORIENT, ROUTE, SCAN, COMPOSE, PROPOSE, STEER, SELECT, REALIZE, WITNESS, each emitted constituent changing the state before the next, over one shared witnessed substrate, under the firmware, the authority, and the envelope.

Laplace uses one forward program for conversation, code, games, model-scoped queries, analysis, and export. Every surface binds requests to it; none implements a rival cognition path. The stages are semantic contracts, not eleven round trips: a conforming implementation fuses them inside one coarse native operator as long as the trace preserves the state transitions and evidence boundaries. Opcodes are stable names, not execution-order numbers, so `OP10 COUPLE` runs between `OP0 RESOLVE` and `OP1 ORIENT`. A program may omit an operation only when its precondition is already established by the caller and the trace says so; a natural-language request asking Laplace to determine meaning may never skip COUPLE or ORIENT because a convenient default relation mask exists.

## Before this stage

[19. Pull](Pull.md): the operators. [18. Firmware](Firmware.md): the image loaded once per pass. [16. Authority](Authority.md): the effective scope. [17. Envelope](Envelope.md): the ceiling.

## Operations, per pass

### 20.1 RESOLVE (OP0)

- **In:** the surface's request (or an internal monologue / self-prompt step), the principal, the session or task trajectory.
- **Do:** decompose the exact current observation **in C memory from mapped `tier0.bin`, `tier0.flags`, and `highway.bin` in microseconds**—requiring zero synchronous database `COPY` writes before answering: Laplace has **tiers of entities rather than fixed BPE tokens**, so any granularity of `entity` (`tier 0` codepoints, `tier 1` graphemes/compositional scalars like `"255"`, `tier 2` UAX #29 words, `tier 3+` multi-word idioms, clauses, AST statements, functions, or repository subtrees) is a first-class 16-byte `lp_id` handle at a deterministic point in the 4-ball. Resolve multi-tier constituent occurrences, session/task identities, resolved prior-turn discourse referents and open obligations from [21. Sessions](Sessions.md), turn-level `system`/`developer`/user or `InternalMonologue` framing ([18. Firmware](Firmware.md) operation 18.3), the effective authority boundary ([16. Authority](Authority.md) operation 16.4), and the active `.firmware` image ([18. Firmware](Firmware.md) operation 18.16).
- **Out:** the in-memory decomposed multi-tier DAG and root `lp_id`, multi-tier occurrence handles, prior discourse referents, effective authority scope, obligations, turn-level channel/framing, and `firmware_id`.
- **From:** `docs/specs/36_Laplace_Forward_Pass.md` §RESOLVE; `docs/specs/37_Substrate_Operation_ISA.md` OP0; `docs/INVENTIONS.md` #62, #104.

### 20.2 COUPLE (OP10)

- **In:** the resolved state of 20.1.
- **Do:** compute **microsecond trajectory salience** (`laplace_salience`, [19. Pull](Pull.md) operation 19.11: continuous GIN self-information $I(e)$, joint span contraction, and `M`-outcome `WIN`/`LOSS` differential) alongside the query-relative coupling field against the eligible indexed planes within the effective authority and `.firmware` scope in **2–3 batched binary database probes** (`<100–200ms` total pass latency on populated data, never ~45 per-word round trips): query centroids ($\sum w_i x_i / \sum w_i$) and directed curve nominations (`frechet4d`/`dtw4d`/`edr4d`) weight constituents by salience rather than flat `1/N` averaging over spaces and question glue, and high-frequency hubs retain their exact GIN `df` rather than vanishing behind a binary `hub` cliff. Current constituents with order and gaps, resolved prior-turn discourse entities (`"Where was he born?"`, `"Why?"`), open obligations, and prior internal OODA outcomes perturb the web together through [15. Web](Web.md) operation 15.2. A plane, entity, or source outside `COUPLE` authority never enters cognition.
- **Out:** the salience-weighted typed response field: what responds, with what intrinsic/contextual/causal salience, by which route, and with what standing.
- **From:** `docs/INVENTION.md` §7; `docs/specs/36_Laplace_Forward_Pass.md` §COUPLE; [19. Pull](Pull.md) operation 19.11; [18. Firmware](Firmware.md) operation 18.7.

### 20.3 ORIENT (OP1)

- **In:** the salience-weighted field of 20.2 and the discourse and task state.
- **Do:** construct the joint interpretation across candidate senses, multi-tier spans, grammatical roles, relation intents ([19. Pull](Pull.md) operation 19.8), discourse referents, and obligations. Combine microsecond trajectory salience (`laplace_salience`: continuous $I(e)$ + leave-one-out constraint bits) with [18. Firmware](Firmware.md) operation 18.8's two-tier POS law—**contextual parse alignment plus word-level lexical/UD POS fallback (`[lightning, NOUN]`, `[does, AUX]`, `[What, PRON]`, `[the, DET]`)**—so high-salience content anchors (`lightning`, `France`, `capital`, divergent AST symbols) command the obligation budget while high-frequency pragmatic frames (`How does ... ?`, `What is the ... ?`) act strictly as speech-act framing instead of matching unrelated stop-word sentences (`"How does this shirt fit?"`). Promote tight high-PMI, high-$I$ spans to their higher-tier `entity` handles, and **never mute emission (`budget = 0`) when multiple senses survive**: `ORIENT` hands ranked/grouped interpretations to `ROUTE`..`REALIZE` to answer from the strongest/shared attested structure, surface genuinely contested perspectives, or ask a concise clarifying question ([18. Firmware](Firmware.md) operation 18.12).
- **Out:** salience-weighted content obligations, promoted multi-tier handles, and ranked joint interpretation(s).
- **From:** `docs/specs/36_Laplace_Forward_Pass.md` §ORIENT; `docs/INVENTION.md` §7; [19. Pull](Pull.md) operation 19.11; [18. Firmware](Firmware.md) operations 18.8 and 18.12.

### 20.4 ROUTE (OP2)

- **In:** the orientation of 20.3 and the hard constraints.
- **Do:** compile the oriented state into an executable cognition plan within the preflight bounds of [17. Envelope](Envelope.md) operation 17.2: eligible domain planes, `mask` bank filters, calculation providers, hop, fanout, and frontier ceilings, Highway A* route planning over mapped `highway.bin` landmarks and crosswalks ([15. Web](Web.md) operation 15.7), and n-ary (`np >= 4`) claim and trajectory traversal. Firmware governs hop/fanout spend, domain-plane focus, extra rounds toward open content obligations, and refutation probing without ever widening caller authority.
- **Out:** the bounded execution plan.
- **From:** `docs/specs/36_Laplace_Forward_Pass.md` §ROUTE; `docs/specs/37_Substrate_Operation_ISA.md` OP2; [15. Web](Web.md) operation 15.7.

### 20.5 SCAN (OP3)

- **In:** the program of 20.4.
- **Do:** discover the bounded responding frontier through exact identity, containment, indexes, perf-cache, Hilbert and PostGIS locality, source and context filters, typed graph operations, and declared calculation providers, the operators of [19. Pull](Pull.md). The work shape is an indexed star expansion around the active root or frontier: `q → {x_1 … x_k}`, each admitted spoke becoming the next center, to the hop and resource boundary. Canonical identities make separately reached routes collapse onto the same structures without losing their receipts. Approximate geometry nominates candidates and never establishes identity or truth. A*, Dijkstra, strongest-first walk, containment, trajectory continuation, and geometric search are operators inside this stage; none is the cognition. Firmware owns operator choice inside the routed program, beam and depth spend, and whether optional geometry or ordinal-continuity operators run; a default intent mask standing in for ORIENT is a caller hard constraint only.
- **Out:** the candidates, with their routes.
- **From:** `docs/INVENTION.md` §9; `docs/specs/36_Laplace_Forward_Pass.md` §SCAN; `docs/specs/37_Substrate_Operation_ISA.md` §Sparse execution law.

### 20.6 COMPOSE (OP4)

- **In:** the candidates of 20.5.
- **Do:** build and fold the active typed frontier from the responding routes, trajectories, factors, tiers, relation bands, standing, contradiction, and uncertainty. Corroborating and conflicting witnesses remain visible. Different evidence dimensions remain typed until the operation contract declares a gate, cost, ranking dimension, or fold. Convergent routes strengthen a candidate only under the declared dependence and provenance law. Firmware owns nothing here: the fold, the dependence law, and standing itself are not policy.
- **Out:** the composed frontier.
- **From:** `docs/specs/36_Laplace_Forward_Pass.md` §COMPOSE; `docs/specs/39_Personality_Firmware.md` §3.

### 20.7 PROPOSE (OP5)

- **In:** the frontier of 20.6.
- **Do:** produce legal, grammatical, typed next constituents, semantic acts, internal deliberation links, or actions **at any entity tier** (`tier 0` codepoints for novel spelling/identifiers, `tier 2` words, `tier 3` idioms/C statements/clauses, or `tier 4+` whole AST blocks, definitions, or reused subtrees)—never forcing known multi-tier structures to be spelled out subword-by-subword. A proposal may combine physical continuation, graph evidence, model-circuit testimony, code grammar, prior `WIN`/`LOSS` repair trajectories, or domain operators without committing to an answer. Routing state and output eligibility stay separate: reaching a frame, sense, or category does not license emitting its bare label unless a result-bearing relation, ordered observation, or semantic act is established. Firmware owns semantic-act preference (`answer`, `think`/`monologue`, `act`/`verify`, `ask`, `explain`, `abstain`); it never owns grammar or type legality.
- **Out:** the multi-tier proposal set.
- **From:** `docs/specs/36_Laplace_Forward_Pass.md` §PROPOSE; [Pull: The forward pass](../Semantics/Pull.md#the-forward-pass).

### 20.8 STEER (OP6)

- **In:** the proposals of 20.7.
- **Do:** rank and assemble proposals under the oriented task, discourse state, principal authority, envelope limits, and `.firmware` election order ([18. Firmware](Firmware.md) operation 18.9): weighted content-obligation coverage, conservative standing (`rating − k·RD`), empirical usage specificity (`tokens`/`tag_cnt` and container rarity), and trajectory/clause coherence. Joint meetings that ground multiple content obligations rank above isolated single-word hits, **and when an explanation or multi-part prompt spans complementary attested claims and trajectories, `STEER` composes a coherent multi-clause plan covering the grounded obligations in sequence rather than discarding valid partial-coverage clauses or returning empty output**. Unconstrained enum nodes (`NOUN`, `eng`) act only as filters and never win election as answers, while high-degree content hubs (`Paris`, `lightning`) are crossed cleanly via top-standing scans ([15. Web](Web.md) operation 15.5).
- **Out:** the ranked, admitted single-clause or multi-clause answer/action plan.
- **From:** `docs/specs/36_Laplace_Forward_Pass.md` §STEER; [18. Firmware](Firmware.md) operations 18.9 and 18.12.

### 20.9 SELECT (OP7)

- **In:** the admitted proposals of 20.8.
- **Do:** select under the declared policy of [18. Firmware](Firmware.md) operation 18.10, and retain enough receipt state to explain which routes, standing, and obligations determined eligibility. The selected item must be supported by the admitted evidence and constraints. Authority is checked again at the requested act: permission to inspect or couple does not grant DERIVE, REALIZE, PERSIST, EXPORT, EXECUTE, or DELEGATE. Pooled model consensus is consumed as witnessed standing; N external answers are not adjudicated by a hidden judge. Nothing is brute-forced, no softmax reduces the set to a scalar, and no standing changes. The dot product of "the capital of France is" points exactly at `Paris` because the attestations are the facts, not at empty space to be resolved by nearest neighbour.
- **Out:** the selected identity, semantic act, or action, with its decision identity.
- **From:** `docs/specs/36_Laplace_Forward_Pass.md` §SELECT; `docs/INVENTOR_RECORD.md` §The forward pass.

### 20.10 REALIZE (OP8)

- **In:** the selection of 20.9.
- **Do:** render the selected act, composed clauses, entity, or action into the requested surface—natural language in the target language, Markdown, JSON, code, SAN or UCI, or media—through `lp_realize` in bulk ([19. Pull](Pull.md) operation 19.10), honoring turn-level format, verbosity, persona, and `stop` sequences. `REALIZE` enforces disclosure authority ([16. Authority](Authority.md) operation 16.5). When senses tie or witnesses disagree, realize from the leading/shared attested structure, surface the contested perspectives with provenance, or ask a concise clarifying question; **emit `ABSTAIN` strictly when zero relevant witnessed evidence exists in the authorized scope (or when disclosure is denied by authority)**, never on a sense tie or partial coverage.
- **Out:** the realized surface, disposition, and realization fingerprint.
- **From:** `docs/specs/36_Laplace_Forward_Pass.md` §REALIZE; [18. Firmware](Firmware.md) operations 18.12 and 18.13.

### 20.11 WITNESS (OP9)

- **In:** the completed turn outcome of 20.10, any internal monologue / deliberation trajectories, and any executed tool, compile, test, or game effect.
- **Do:** talking, internal monologue/reasoning, and coding share **one universal 4-table substrate**, distinguished by trajectory vertex metadata (`said`, `outcome`, `position`, spare bits on `physicality.path`—never `entity.mask`) and witness trust class ([6. Registries](Registries.md) operation 6.5): external user turns commit under `UserPromptContent` (`0.30`), Laplace external responses under `ResponseContent` (`0.20`), Laplace internal reasoning/hypothesis steps under `InternalMonologue` (`0.10`, preserving full deliberation links and provenance without bootstrapping self-talk into truth), and compiler/test/verifier consequences under `ToolchainVerification` (`0.90`, attaching `WIN`/`LOSS` outcomes directly to the salient divergent AST/action constituents). Commit through the governed write lane of [21. Sessions](Sessions.md) operation 21.5 at turn or verifier completion (skipped on stateless `--read` calls), deduplicating identical `[prompt, response]` turns by content identity.
- **Out:** the durable episodic, deliberation, and consequence records when witnessing is active.
- **From:** `docs/specs/36_Laplace_Forward_Pass.md` §WITNESS; `docs/specs/34_Conversational_Provenance.md` §Turn contract; [23. Learning](Learning.md) operations 23.1 and 23.5.

### 20.12 Update active state across clauses, internal monologue, and OODA steps

- **In:** the in-memory working frontier as multi-tier clauses compose, internal reasoning steps link candidate hypotheses, or compiler/test/game verifiers return consequences.
- **Do:** as each multi-tier constituent, clause, internal thought, or AST delta (`R0 + Δ → R1`) is selected inside the pass, update the active trajectory, covered salience-weighted obligations, entity bindings, and anti-repetition residual state **in C memory** over the already-probed working frontier—never issuing per-word database `COPY` writes or per-word SQL round-trip storms. When an OODA step acts on code or a verifier ([26. Code](Code.md)), Laplace realizes the candidate, runs the toolchain, decomposes diagnostics, computes outcome-differential salience (`LOSS` vs `WIN`) to isolate failing constituents (*"every time this datatype enters this function, compile fails"*), witnesses the consequence, and self-corrects on the next round before finalizing. The pass finishes when content obligations and verification close, a `stop` or output cap is reached, or the envelope closes, recording an explicit disposition (`complete`, `clarification_requested`, `contested_perspectives`, `abstain_no_evidence`, `unauthorized`, or `envelope_exhausted`).
- **Out:** the completed pass and its audit receipt.
- **From:** `docs/specs/36_Laplace_Forward_Pass.md` §Stateful emission and §Persistent execution state; `docs/INVENTIONS.md` #70, #73, #116.

## The trace

Each pass exposes a bounded typed trace sufficient to audit: resolved root and occurrence ids; active scope and hard caller constraints; authority roots, capability grants, and governance disposition; coupling channels and responding route families; surviving interpretations and ambiguity disposition; the compiled provider and operator program; hop, fanout, frontier, and candidate counts; ordered, context, and occurrence coverage; evidence cells with contradiction and standing and uncertainty; dependence and provenance roots; obligation state; the selected semantic act; the realization fingerprint; state transitions and writes; `program_id`, `firmware_id`, and the decision identity; estimated and reserved work; and actual resource and work counters. MCP, HTTP, CLI, SQL, streaming, and export adapters agree at this level; equivalent requests execute equivalent programs. See `docs/specs/36_Laplace_Forward_Pass.md` §Trace contract and `docs/specs/37_Substrate_Operation_ISA.md` §Receipts.

## The correspondence

The transformer roles correspond only functionally. Q is the active admitted observation with its bindings and obligations. K is every indexed typed address and plane able to respond. QK is COUPLE, the typed query-relative response field, never one relevance score. V is the responding physicalities, facts, evidence, and calculations with standing as rating, deviation, volatility, and witnesses. O is the receipted fold into updated bindings, orientation, frontier, and obligations. Heads are the independent relation, provider, tier, and context planes, named. Position is exact trajectory ordinal, gap, and containment. The residual stream is the surviving typed frontier carried between rounds. A layer is one routed processing and fold round over the enabled planes, not a fixed block. The KV cache is the persistent substrate plus the witnessed session and frontier projection plus rebuildable perf-caches. The loss is witnessed outcomes and the uncertainty-bearing fold. Those fetches, attention, convolution, diffusion, the feed-forward network, are the lookup; the weights they would have shifted are the attestations, the observations, and the witnessing; what remains after the lookup returns the set is the choice, and the choice is the firmware. See `docs/INVENTION.md` §8, `docs/invention/transformer-slot-map.md`, and [Personality firmware: Instruction sets](../Semantics/Firmware.md#instruction-sets).

## What this stage leaves behind

An answer: a set, a segment of a branch, a combination, a single fact, an action, or an honest abstention, with a trace that says how, under which firmware, within which authority and envelope, and a witnessed turn that has already changed the next pass.

## Without this stage

Nothing answers.
