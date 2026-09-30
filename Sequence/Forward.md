# 20. Forward

One stateful, typed program answers every request: RESOLVE, COUPLE, ORIENT, ROUTE, SCAN, COMPOSE, PROPOSE, STEER, SELECT, REALIZE, WITNESS, each emitted constituent changing the state before the next, over one shared witnessed substrate, under the firmware, the authority, and the envelope.

Laplace uses one forward program for conversation, code, games, model-scoped queries, analysis, and export. Every surface binds requests to it; none implements a rival cognition path. The stages are semantic contracts, not eleven round trips: a conforming implementation fuses them inside one coarse native operator as long as the trace preserves the state transitions and evidence boundaries. Opcodes are stable names, not execution-order numbers, so `OP10 COUPLE` runs between `OP0 RESOLVE` and `OP1 ORIENT`. A program may omit an operation only when its precondition is already established by the caller and the trace says so; a natural-language request asking Laplace to determine meaning may never skip COUPLE or ORIENT because a convenient default relation mask exists.

## Before this stage

[19. Pull](Pull.md): the operators. [18. Firmware](Firmware.md): the image loaded once per pass. [16. Authority](Authority.md): the effective scope. [17. Envelope](Envelope.md): the ceiling.

## As built

None: `pull.c` states that `laplace pull` is the lookups the forward pass is made of and not yet the forward pass ([Reads: laplace pull](../Reference/Reads.md#laplace-pull)); the operators it calls are [19. Pull](Pull.md). In the monorepo: `generation.forward_program(...)`, one C entry `pg_laplace_forward_trace`, with `p_hops` 2 and `p_fanout` 8 by default, `p_seed`, `p_prior_frontier` as discourse; `converse.respond` is COUPLE; `cognition_program.h` compiles the observation into obligations from its occurrence ordinals and mints `program_id`, `semantic_act_id`, `output_fingerprint`; `steer_candidates.c`, `prompt_intent.h`, `intent_stage`; `generation.forward_text` realizes a completed act; `converse.forward_turn` and `converse.chat`; the web `ForwardProofView`; `bench-forward-program.py` ([Monorepo: Firmware and the forward program](../Reference/Monorepo.md#firmware-and-the-forward-program)). `docs/read-path.md` §11 lists what is still open: complete typed coupling coverage, remaining row-at-a-time paths, and the centroid against Karcher reconciliation.

Status: **monorepo**. Every operation below is from the invention documents; [Reference: Traceability](../Reference/Traceability.md#20-forward) indexes it.

## Operations, per pass

### 20.1 RESOLVE (OP0)

- **In:** the surface's request, the principal, the session.
- **Do:** admit the exact current observation as content, [11. Content](Content.md) on the client: the prompt is one exact observation, a trunk with ordered constituents, and UAX #29 is the tokenizer and the trunk ID is the token index. Resolve its constituent occurrences, the session and context identities, prior discourse bindings from the session trajectory of [21. Sessions](Sessions.md), the world, time, and source boundary, open obligations, and the requested output contract. Resolve the principal and tenant, the role and relationship authority, the granted packages and capabilities, the active caller-selected scope, and kernel governance into the effective boundary of [16. Authority](Authority.md) operation 16.4, and load the firmware of [18. Firmware](Firmware.md) operation 18.16. Decomposition and tier ascent and descent recover structure; they do not privilege one token, noun, regex, topic word, or renderable label as the interpretation root. Firmware owns nothing semantic here.
- **Out:** the resolved root, occurrence ids, scope, hard caller constraints, authority roots, obligations, and `firmware_id`.
- **From:** `docs/specs/36_Laplace_Forward_Pass.md` §RESOLVE; `docs/specs/37_Substrate_Operation_ISA.md` OP0; `docs/INVENTIONS.md` #62, #104.

### 20.2 COUPLE (OP10)

- **In:** the resolved state of 20.1.
- **Do:** compute the query-relative coupling field of the whole admitted observation against every eligible indexed plane under the hard authority, scope, and resource boundary: the current root and trajectory, constituent occurrences with order and gaps, prior discourse bindings, open obligations, world, time, and source context, and explicit caller constraints all perturb the web at once, through the channels of [15. Web](Web.md) operation 15.2. A plane, entity, or source outside the effective COUPLE capability never influences cognition to be hidden later. The response is typed state, not one scalar: relation identity, role compatibility, ordinal and gap state, containment, support or refutation, rating, deviation, volatility, witness count, source dependence, geometry, and provenance stay distinguishable. Routes converging on one candidate stay visible; dependent routes are not independent witnesses. Firmware owns only how many coupling rounds to spend, up to the envelope; it never owns eligibility of a plane and never supplies a relation or provider mask before ORIENT. For `test` in a prompt, the medical, software, and examination senses each activate different roles, containers, definitions, and operations, and the other constituents tug those candidates differently.
- **Out:** the typed response field: what responds, by which route, with what force.
- **From:** `docs/INVENTION.md` §7; `docs/specs/36_Laplace_Forward_Pass.md` §COUPLE; `docs/specs/37_Substrate_Operation_ISA.md` §OP10 COUPLE law; `docs/specs/39_Personality_Firmware.md` §3.

### 20.3 ORIENT (OP1)

- **In:** the field of 20.2 and the discourse and task state.
- **Do:** construct the joint interpretation: candidate senses, roles, bindings, topics, operations, and obligations constrain one another through the complete observation, and a winning interpretation is a jointly compatible subgraph, not the definition with the largest global score. The result is one of: unique enough to execute; multiple surviving interpretations, ambiguity; inconsistent or impossible under current evidence; resource-bounded, more compute required. Ambiguity is a valid state; certainty is never manufactured to obtain one route. A caller may impose hard scope or request a constrained operation, but a default mask never substitutes for ORIENT. Content obligations come from an occurrence's own evidence: with no supported parse every occurrence is an obligation, and "What", "is", "the", and "of" stay obligations until a treebank supplies their part-of-speech standing. Firmware owns the active goal, objective, success conditions, acceptable uncertainty, termination, and the response to an ambiguous, impossible, or exhausted orientation; it never owns the detection of ambiguity or which interpretation is true.
- **Out:** the interpretation, or the ambiguity disposition.
- **From:** `docs/specs/36_Laplace_Forward_Pass.md` §ORIENT; `docs/INVENTION.md` §7 "Joint interpretation before policy"; `docs/plan/ASSIMILATION_ROADMAP.md` §0 live status.

### 20.4 ROUTE (OP2)

- **In:** the orientation of 20.3 and the hard constraints.
- **Do:** compile the oriented state into an executable cognition program: eligible relation, provider, and operator families, salience bands, modalities, circuit and domain planes, hop, fanout, and frontier limits, required calculations, and output obligations. Policy follows interpretation, and surviving alternatives are preserved where the operation requires them. The route exposes the same dimensions execution will consume, so it is the preflight plan of [17. Envelope](Envelope.md) operation 17.2. Firmware owns hop and fanout spend, extra routing rounds toward unresolved obligations, and routing refutation readers; it never owns the caller's hard scope, the output contract, or authority.
- **Out:** the program and its envelope.
- **From:** `docs/specs/36_Laplace_Forward_Pass.md` §ROUTE; `docs/specs/37_Substrate_Operation_ISA.md` OP2.

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
- **Do:** produce legal, grammatical, typed next constituents, semantic acts, or actions. A proposal may combine physical continuation, graph evidence, model-circuit testimony, code grammar, tool results, or domain operators without committing to an answer. Routing state and output eligibility are separate: reaching a frame, sense, or category does not license emitting its label merely because it is renderable; an output operation must first establish the result-bearing relation, ordered observation, or semantic act. Conversely, a selected typed result does not require a text physicality. A step can return any segment of any branch, or a combination: the word together with a gloss attested of it, the remainder of the sentence, the letters, or all three. Firmware owns the semantic-act preference: answer, ask, explain, abstain, act; it never owns grammar or type legality.
- **Out:** the proposal set.
- **From:** `docs/specs/36_Laplace_Forward_Pass.md` §PROPOSE; [Pull: The forward pass](../Semantics/Pull.md#the-forward-pass).

### 20.8 STEER (OP6)

- **In:** the proposals of 20.7.
- **Do:** apply the oriented task, discourse state, source and world scope, principal authority and capabilities, kernel governance, hop, fanout, and resource limits, ordinal continuity, standing and uncertainty, observed outcomes, obligations, and the current residual and frontier state to the proposal set, under the firmware's election order of [18. Firmware](Firmware.md) operation 18.9: relation rank as read-time salience floor, election by grounded obligations, the conservative bound, ordinal continuity, the least-shared meeting first. While no candidate grounds every remaining obligation, route to the joint meeting of the constituents instead of emitting partial-coverage candidates; glue hubs such as `HAS_POS NOUN` and `HAS_LANGUAGE eng` do not win election. STEER is query-relative and never reintroduces a global popularity score or an interpretation COUPLE and ORIENT discarded. Firmware owns the election order, the sufficiency bound, the ordinal-continuity window, and the emission budget; never a cross-family scalar or the claims' standing.
- **Out:** the ranked, admitted proposals.
- **From:** `docs/specs/36_Laplace_Forward_Pass.md` §STEER; `docs/plan/ASSIMILATION_ROADMAP.md` §0 and commit `0be08b414`.

### 20.9 SELECT (OP7)

- **In:** the admitted proposals of 20.8.
- **Do:** select under the declared policy of [18. Firmware](Firmware.md) operation 18.10, and retain enough receipt state to explain which routes, standing, and obligations determined eligibility. The selected item must be supported by the admitted evidence and constraints. Authority is checked again at the requested act: permission to inspect or couple does not grant DERIVE, REALIZE, PERSIST, EXPORT, EXECUTE, or DELEGATE. Pooled model consensus is consumed as witnessed standing; N external answers are not adjudicated by a hidden judge. Nothing is brute-forced, no softmax reduces the set to a scalar, and no standing changes. The dot product of "the capital of France is" points exactly at `Paris` because the attestations are the facts, not at empty space to be resolved by nearest neighbour.
- **Out:** the selected identity, semantic act, or action, with its decision identity.
- **From:** `docs/specs/36_Laplace_Forward_Pass.md` §SELECT; `docs/INVENTOR_RECORD.md` §The forward pass.

### 20.10 REALIZE (OP8)

- **In:** the selection of 20.9.
- **Do:** render the selected act, entity, or action into the requested surface, text in the query's language, SAN or UCI, JSON, a file, without using rendering to reclassify it, through [19. Pull](Pull.md) operation 19.10 in bulk. REALIZE is an authority boundary: an operation may know that relevant knowledge exists and honestly abstain from revealing operational detail when the principal lacks realization authority, and even disclosure that a restricted scope exists may require DISCOVER. Only a completed semantic act is realized; an exhausted or unresolved frontier is never promoted into answer text. The disposition, open, complete, unresolved, budget exhausted, ambiguous, is named. Firmware owns the voice and the wording of an abstention or partial result.
- **Out:** the surface, and its realization fingerprint.
- **From:** `docs/specs/36_Laplace_Forward_Pass.md` §REALIZE; `docs/read-path.md` §4 and §8.

### 20.11 WITNESS (OP9)

- **In:** the outcome of 20.10 and any effect.
- **Do:** append the observation, turn, action, tool call, and result with its receipt through the governed write lane of [21. Sessions](Sessions.md), when the operation contract calls for witnessing. Calculated outcomes identify analyzer, tool, version, and recipe. Reads alone do not witness: a read is never silently testimony merely because it executed, and replaying a read manufactures nothing. Retrying the same write uses an idempotency key so transport retries do not multiply observation count. New evidence or emitted content changes the active state and therefore the next coupling field. Firmware owns nothing about whether the governed lane runs; whether Laplace's own response attests, and at what class, is conflict C1 in [30. Conflicts](Conflicts.md).
- **Out:** the durable turn, and the changed world.
- **From:** `docs/specs/36_Laplace_Forward_Pass.md` §WITNESS; `docs/specs/34_Conversational_Provenance.md` §Turn contract.

### 20.12 Loop

- **In:** the state after 20.11.
- **Do:** every emitted constituent or semantic act updates the active trajectory, discourse bindings, obligations, residual and frontier state, and query-relative coupling before the next constituent is selected: `state_t → couple/orient → sparse hop/fanout → select/realize/witness → state_t+1 → recompute affected coupling`. Building one frontier and draining it without feedback is not a conforming pass. The result is content, so it has a trunk, a tree, observations, and attestations, and the next step works from those. The pass ends when the firmware's termination policy is met, when obligations close, or when the envelope is exhausted, and a WHY_NOT then distinguishes unknown, unsupported, ambiguous, resource-exhausted, and known-but-not-authorized. The pass may hold a bounded frontier, residual state, candidate set, or operator-local cache in memory as a working projection over the shared substrate; it retains the canonical ids and routes needed to rejoin durable state and never becomes a second semantic authority.
- **Out:** the completed pass.
- **From:** `docs/specs/36_Laplace_Forward_Pass.md` §Stateful emission and §Persistent execution state; `docs/INVENTIONS.md` #70, #73.

## The trace

Each pass exposes a bounded typed trace sufficient to audit: resolved root and occurrence ids; active scope and hard caller constraints; authority roots, capability grants, and governance disposition; coupling channels and responding route families; surviving interpretations and ambiguity disposition; the compiled provider and operator program; hop, fanout, frontier, and candidate counts; ordered, context, and occurrence coverage; evidence cells with contradiction and standing and uncertainty; dependence and provenance roots; obligation state; the selected semantic act; the realization fingerprint; state transitions and writes; `program_id`, `firmware_id`, and the decision identity; estimated and reserved work; and actual resource and work counters. MCP, HTTP, CLI, SQL, streaming, and export adapters agree at this level; equivalent requests execute equivalent programs. See `docs/specs/36_Laplace_Forward_Pass.md` §Trace contract and `docs/specs/37_Substrate_Operation_ISA.md` §Receipts.

## The correspondence

The transformer roles correspond only functionally. Q is the active admitted observation with its bindings and obligations. K is every indexed typed address and plane able to respond. QK is COUPLE, the typed query-relative response field, never one relevance score. V is the responding physicalities, facts, evidence, and calculations with standing as rating, deviation, volatility, and witnesses. O is the receipted fold into updated bindings, orientation, frontier, and obligations. Heads are the independent relation, provider, tier, and context planes, named. Position is exact trajectory ordinal, gap, and containment. The residual stream is the surviving typed frontier carried between rounds. A layer is one routed processing and fold round over the enabled planes, not a fixed block. The KV cache is the persistent substrate plus the witnessed session and frontier projection plus rebuildable perf-caches. The loss is witnessed outcomes and the uncertainty-bearing fold. Those fetches, attention, convolution, diffusion, the feed-forward network, are the lookup; the weights they would have shifted are the attestations, the observations, and the witnessing; what remains after the lookup returns the set is the choice, and the choice is the firmware. See `docs/INVENTION.md` §8, `docs/invention/transformer-slot-map.md`, and [Personality firmware: Instruction sets](../Semantics/Firmware.md#instruction-sets).

## What this stage leaves behind

An answer: a set, a segment of a branch, a combination, a single fact, an action, or an honest abstention, with a trace that says how, under which firmware, within which authority and envelope, and a witnessed turn that has already changed the next pass.

## Without this stage

Nothing answers.
