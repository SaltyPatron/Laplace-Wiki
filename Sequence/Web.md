# 15. Web

With standings on every claim, a pull reads a standing as a confidence and a cost, and hops and fans out over the web at O(log N) + O(K) a step.

When entities and physicalities are recorded, additional records and relations are added to form a spider colony web: N spiders, all with interwoven webs, where pulling on one strand makes everything else tug back. Consensus tells how hard it tugs back. Laplace is not a flat graph of node, edge, node pairs: one canonical entity is at once a child in many compositions, a vertex in many trajectories, contained by many structures, a subject or object of many typed relations, witnessed by many sources, and near or structurally similar to other physicalities, and those structures overlap because they share identities. The primitive is: tug a strand; enumerate what tugs back, through which indexed route, and with what typed response.

## Before this stage

[13. Consensus](Consensus.md): a standing on every claim. [14. Indexes](Indexes.md): the lookups a hop is made of.

## Operations, per hop

### 15.1 Find the strands that hold an entity

- **In:** an entity's ID.
- **Do:** look up every claim that holds the entity in any of its places, through the semantics indexes of [14. Indexes](Indexes.md) operation 14.6, and every container that holds it, through the GIN of operation 14.4.
- **Out:** the set of strands leaving the entity. Fanout is the number of them: the number of properties recorded of a codepoint, of senses and translations leaving an entry, of edges leaving a concept, of dependents of a head.
- **Check:** `dog` in the engine database returns 612 claims, 131 matched at least once and 481 untouched stock.
- **Mechanism:** `claims_of` and `claims_like`: `physicality p JOIN consensus s ON s.claim = p.entity WHERE p.path @> $1::blake3[] LIMIT fan + 1` ([Reads: The claims that hold an entity](../Reference/Reads.md#the-claims-that-hold-an-entity)); containers by `path @> ARRAY[id]` through the GIN ([Reads: laplace hop](../Reference/Reads.md#laplace-hop)). In the monorepo: `consensus_neighbors.c`, `explore_web.c`, `containers_of.c`; `consensus.consensus_out` and `consensus_in`; `/v1/explore/entities/{id}/graph`, `containers`, `neighbors` ([Monorepo: Firmware and the forward program](../Reference/Monorepo.md#firmware-and-the-forward-program)). Status: **built**.
- **From:** [Pull: Hop and fanout](../Semantics/Pull.md#hop-and-fanout), [Personality firmware: What was measured on one entity](../Semantics/Firmware.md#what-was-measured-on-one-entity).

### 15.2 Keep the response typed

- **In:** the strands of 15.1.
- **Do:** a response carries its route and its typed force, and the types are not collapsed into one relevance number at this point. The channels: exact identity and composition; containment and parent trajectories; ordered occurrence, continuation, and gap state; the relation's identity and rank; support, draw, or refutation with rating, deviation, volatility, and witness count; source and context dependence; structural and geometric neighbourhood, Hilbert locality, angular separation, Fréchet shape; deterministic calculation and domain providers; prior session and frontier state. Some of these are hard admissibility constraints, some evidence, some contradiction, some search cost, some order the frontier, some remain provenance only; which may be combined and how is declared by the firmware's election order, not here. Two routes converging on one candidate are signal, not duplicate edges, and dependent routes are not independent witnesses. A relation below the salience floor is a filter, not a strand.
- **Out:** the typed response set of the entity.
- **Mechanism:** each strand carries rating, deviation, volatility, matches, and the witness's position, and the sort collapses them to one confidence ([Reads: The claims that hold an entity](../Reference/Reads.md#the-claims-that-hold-an-entity)); the typed channels are [Conflicts R1](Conflicts.md). In the monorepo: `converse.respond` (`forward_respond.c`) keeps every route typed per term: relation, hops, predecessor, rating, deviation, volatility, witnesses, minimum salience, minimum conservative standing, and returns routes per term, never one score: the other side of [Conflicts R1](Conflicts.md) ([Monorepo: Firmware and the forward program](../Reference/Monorepo.md#firmware-and-the-forward-program)). Status: **monorepo; not in the split repositories**.
- **From:** `docs/INVENTION.md` §6, §7, §19; `docs/specs/37_Substrate_Operation_ISA.md` §OP10 COUPLE law; `docs/INVENTIONS.md` #59 to #65.

### 15.3 Read each strand's standing as a confidence

- **In:** the standings of the strands.
- **Do:** the pull does not change a standing. What the pull selects on is a reading of it. The anchor is rating 1500. A claim's confidence is the chance it beats that anchor, taken *k* deviations below its rating, on Glicko-2's scale of 173.7178: *p* = σ((*r* − 1500)/173.7178 − *k* · RD/173.7178). *k* is a restriction on uncertainty: at *k* = 0 the rating is taken as it stands; each step of *k* demands that the rating still hold further down inside its deviation, so a claim few witnesses have touched tugs less than its rating alone says.
- **Out:** a confidence per strand.
- **Check:** a standing of 1774.3 with deviation 93.3 reads as 0.829 at *k* = 0 and 0.624 at *k* = 2. Untouched stock at deviation 250 reads 0.500 at *k* = 0 and 0.053 at *k* = 2; at deviation 350, 0.018. Two standings, 1700 at deviation 300 and 1600 at deviation 40, cross at *k* = 0.38: below it the louder rating is selected, above it the tighter deviation. Nothing in the two standings changed.
- **Mechanism:** `lp_confidence(r, k)` ([Native: Consensus](../Reference/Native.md#consensus-consensusc)); `laplace_confidence(rating, deviation, k)` in SQL ([SQL: Consensus](../Reference/SQL.md#consensus)). In the monorepo: `laplace_effective_mu_fp = rating − 2·rd` (`mu.eff_mu`), `laplace_glicko2_expected_score`, `mu.belief_logit`: *k* is fixed at 2 ([Monorepo: Consensus](../Reference/Monorepo.md#consensus)). Status: **built**.
- **From:** [Personality firmware: How a standing is read](../Semantics/Firmware.md#how-a-standing-is-read).

### 15.4 Turn the confidence into a cost

- **In:** the confidence of 15.3.
- **Do:** the cost of crossing the claim is −ln *p* + λ, with λ a tax paid once per hop. Costs add, so the cheapest chain is the one whose confidences multiply to the most, shortened by the tax. Costs are non-negative, so Dijkstra and A* are exact, and a heuristic computed under an optimistic cost stays admissible and consistent when ratings change. λ decides whether a longer, stronger chain beats a shorter, weaker one: two hops at 0.90 cost 0.211 + 2λ, one hop at 0.70 costs 0.357 + λ, and they cross at λ = 0.146.
- **Out:** a cost per strand.
- **Mechanism:** `lp_cost(r, k, per_hop)`, computed as `log1p(e^−x) + λ` ([Native: Consensus](../Reference/Native.md#consensus-consensusc)). In the monorepo: `mu.weight`, `mu.walk_edge_weight`, and the costs of `astar_path.c`. Status: **built**.
- **From:** [Personality firmware: How a standing is read](../Semantics/Firmware.md#how-a-standing-is-read), [Personality firmware: How far a search walks](../Semantics/Firmware.md#how-far-a-search-walks), [Research: Relations Research: Edge cost](../Research/Relations.md#edge-cost).

### 15.5 Refuse what the firmware refuses, then apply the fan

- **In:** the strands of 15.1.
- **Do:** a restriction is applied before the sort: strands of a kind the firmware does not navigate, such as layout, punctuation, a part of speech, a witness, or a language, are dropped. Then the fan: a hop reads at most so many claims that hold the entity, and a search at most so many, and orders that set by confidence. An entity that holds more claims than the fan, a part of speech, a language, is a hub: reached and not crossed. The limit is applied before the ordering, so past the fan the set is whatever the index returned.
- **Out:** the ordered set of strands the firmware allows.
- **Check:** on `dog` at *k* = 2, always taking the top: `[dog, LEMMA, dog]` 0.972, `[dog, UPOS, NOUN]` 0.969, `[dog, XPOS, NN]` 0.966, `[dog, SpaceAfter, No]` 0.943, `[犬, Gloss, dog]` 0.902. The fourth is a typesetting observation, and determiners and a punctuation mark sit in the same tenth as the gloss. The top three are 0.003 apart.
- **Mechanism:** `refused()` drops strands by predicate or witness; the `LIMIT fan + 1` is applied by the database before the engine sorts by `claim_by_conf` ([Reads: The claims that hold an entity](../Reference/Reads.md#the-claims-that-hold-an-entity), [Firmware: Where each decision acts](../Reference/Firmware.md#where-each-decision-acts)). In the monorepo: `salience_floor` from the firmware; `NON_SALIENT_STRUCTURAL` relations never traversed; `fanout` and a frontier cap in `converse.respond`. Status: **built**.
- **From:** [Personality firmware: What was measured on one entity](../Semantics/Firmware.md#what-was-measured-on-one-entity), [Personality firmware: How far a search walks](../Semantics/Firmware.md#how-far-a-search-walks).

### 15.6 Hop, or bubble up and down

- **In:** the set of 15.5.
- **Do:** follow a strand to the entity at its other end, and repeat from 15.1. For a change of language, bubble up to the ILI, change the language, and bubble down: `[dog, eng, ?]` ordered by observed usages, then the witness's sense order, then standing, gives i46360; `[?, language, i46360]` for eight languages, ordered by standing, gives `Hund`, `chien`, `perro`, `犬`, `cane`, `koira`, `pies`, `كلب`. From `Butler`, Laplace can pull a great deal of information and link it to `butler`; the two are different entities 0.045 apart on the S³, one a surname, the other a noun and a verb, and a witness attests the etymology that joins them.
- **Out:** the next entity, and the chain so far with its accumulated cost.
- **Check:** the two translation lookups took 3.3 ms and 1.2 ms.
- **Mechanism:** `laplace hop` for one entity; `laplace translate` for the two lookups through the concept ([Reads: laplace hop](../Reference/Reads.md#laplace-hop), [Reads: laplace translate](../Reference/Reads.md#laplace-translate)). In the monorepo: `taxonomy.bubble_up`, `inference.translate_to`, `inference.translations`, `lexical.define`, `converse.hypernyms`. Status: **built**.
- **From:** [Semantics](../Semantics/README.md), [Pull: Hop and fanout](../Semantics/Pull.md#hop-and-fanout), [Research: Semantics Experiments: Translation through the ILI](../Research/Semantics-Experiments.md#translation-through-the-ili), [Research: Semantics Experiments: Observation and attestation together](../Research/Semantics-Experiments.md#observation-and-attestation-together).

### 15.7 Measure degrees

- **In:** two entities.
- **Do:** degrees of separation, as in a Bacon number or an Erdős number, measure how far anything is from anything else: an A-star search from one to the other over the costs of 15.4, limited by the search fan, the number of hops a chain may run, and λ. Landmarks and the geodesic distance on the S³ give consistent heuristics; when positions are derived from content rather than from relations, the geometric heuristic is close to zero and A* behaves like Dijkstra, still exact.
- **Out:** the cheapest chain, or what is nearest. There is no one context-free universal distance: a raw degree counts admitted transitions, a witnessed degree passes every edge through an evidence floor, a typed degree uses selected relation families only, a temporal degree a historical world boundary, a source degree restricted providers, a cross-domain degree required modal transitions.
- **Mechanism:** `laplace degrees` over `lp_frontier` with estimate 0, so Dijkstra ([Reads: laplace degrees](../Reference/Reads.md#laplace-degrees), [Native: The pull's frontier](../Reference/Native.md#the-pulls-frontier-pullc)). In the monorepo: `cascade.astar_path` and `inference.laplace_astar_path` over `astar.cpp`, Dijkstra with an opt-in admissible geometric A* ([Monorepo: Firmware and the forward program](../Reference/Monorepo.md#firmware-and-the-forward-program)). Status: **built as Dijkstra; monorepo with the geometric heuristic**.
- **From:** [Pull: The web](../Semantics/Pull.md#the-web), `docs/guides/knowledge-arena.md` §Laplace Degree, [Research: Relations Research: Heuristics](../Research/Relations.md#heuristics).

### 15.8 Read a distribution only when asked

- **In:** a subject and a relation.
- **Do:** the normalized distribution over a subject's objects under one relation comes from the Glicko-2 log-odds of the cells, not from a dot product, and it returns the empty set when the subject couples to nothing, the answer a softmax cannot give. With collections in place it is a distribution over attested analyses, not over individually attested tags. It is a read for a caller that asked for a distribution; the forward program itself keeps the typed set.
- **Out:** the distribution, or nothing.
- **Mechanism:** none. In the monorepo: `mu.belief_logit`, checked by `tests/sql/belief_distribution.sql`. Status: **monorepo; not in the split repositories**.
- **From:** `docs/specs/38_Collections_Are_Compositions.md` (belief distribution).

## What this stage leaves behind

Hop and fanout from anything to anything, each strand read as a confidence and a cost, each step O(log N) + O(K): an index lookup and the ordering of what it returned.

## Without this stage

An entity is a record with a standing and no neighbors.
