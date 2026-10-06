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
- **From:** [Pull: Hop and fanout](../Semantics/Pull.md#hop-and-fanout), [Research: Semantics Experiments: What was measured on one entity](../Research/Semantics-Experiments.md#what-was-measured-on-one-entity).

### 15.2 Keep the response typed

- **In:** the strands of 15.1.
- **Do:** a response carries its route and its typed force, and the types are not collapsed into one relevance number at this point. The channels: exact identity and composition; containment and parent trajectories; ordered occurrence, continuation, and gap state; the relation's identity and rank; support, draw, or refutation with rating, deviation, volatility, and witness count; source and context dependence; structural and geometric neighbourhood, Hilbert locality, angular separation, Fréchet shape; deterministic calculation and domain providers; prior session and frontier state. Some of these are hard admissibility constraints, some evidence, some contradiction, some search cost, some order the frontier, some remain provenance only; which may be combined and how is declared by the firmware's election order, not here. Two routes converging on one candidate are signal, not duplicate edges, and dependent routes are not independent witnesses. A relation below the salience floor is a filter, not a strand.
- **Out:** the typed response set of the entity.
- **From:** `docs/INVENTION.md` §6, §7, §19; `docs/specs/37_Substrate_Operation_ISA.md` §OP10 COUPLE law; `docs/INVENTIONS.md` #59 to #65.

### 15.3 Read each strand's standing as a confidence

- **In:** the standings of the strands.
- **Do:** the pull does not change a standing. What the pull selects on is a reading of it. The anchor is rating 1500. A claim's confidence is the chance it beats that anchor, taken *k* deviations below its rating, on Glicko-2's scale of 173.7178: *p* = σ((*r* − 1500)/173.7178 − *k* · RD/173.7178). *k* is a restriction on uncertainty: at *k* = 0 the rating is taken as it stands; each step of *k* demands that the rating still hold further down inside its deviation, so a claim few witnesses have touched tugs less than its rating alone says.
- **Out:** a confidence per strand.
- **From:** [Personality firmware: How a standing is read](../Semantics/Firmware.md#how-a-standing-is-read).

### 15.4 Turn the confidence into a cost

- **In:** the confidence of 15.3.
- **Do:** the cost of crossing the claim is −ln *p* + λ, with λ a tax paid once per hop. Costs add, so the cheapest chain is the one whose confidences multiply to the most, shortened by the tax. Costs are non-negative, so Dijkstra and A* are exact, and a heuristic computed under an optimistic cost stays admissible and consistent when ratings change. λ decides whether a longer, stronger chain beats a shorter, weaker one: two hops at 0.90 cost 0.211 + 2λ, one hop at 0.70 costs 0.357 + λ, and they cross at λ = 0.146.
- **Out:** a cost per strand.
- **From:** [Personality firmware: How a standing is read](../Semantics/Firmware.md#how-a-standing-is-read), [Personality firmware: How far a search walks](../Semantics/Firmware.md#how-far-a-search-walks), [Research: Relations Research: Edge cost](../Research/Relations.md#edge-cost).

### 15.5 Refuse what the firmware refuses, then apply the fan

- **In:** the strands of 15.1.
- **Do:** a restriction is applied before the sort: strands of a kind the firmware does not navigate, such as layout, punctuation, a part of speech, a witness, or a language, are dropped. Then the fan: a hop reads at most so many claims that hold the entity, and a search at most so many, and orders that set by confidence. An entity that holds more claims than the fan, a part of speech, a language, is a fan-limited node: reached and not crossed, a lane limit. Past the fan the set is never whatever the index returned first, which differs between two installs of the same content: a node over the fan is a hub, or is read whole and ordered by confidence then ID, and every read of one command sees one snapshot, [30. Conflicts](Conflicts.md) R2.
- **Out:** the ordered set of strands the firmware allows.
- **From:** [Research: Semantics Experiments: What was measured on one entity](../Research/Semantics-Experiments.md#what-was-measured-on-one-entity), [Personality firmware: How far a search walks](../Semantics/Firmware.md#how-far-a-search-walks).

### 15.6 Hop, or bubble up and down

- **In:** the set of 15.5.
- **Do:** follow a strand to the entity at its other end, and repeat from 15.1. A hop that changes the kind of identifier, word to synset, synset to ILI, roleset to VerbNet class to frame, takes an interchange onto another road class, 15.7. For a change of language, bubble up to the ILI, change the language, and bubble down: `[dog, eng, ?]` ordered by observed usages, then the witness's sense order, then standing, gives i46360; `[?, language, i46360]` for eight languages, ordered by standing, gives `Hund`, `chien`, `perro`, `犬`, `cane`, `koira`, `pies`, `كلب`. From `Butler`, Laplace can pull a great deal of information and link it to `butler`; the two are different entities 0.045 apart on the S³, one a surname, the other a noun and a verb, and a witness attests the etymology that joins them.
- **Out:** the next entity, and the chain so far with its accumulated cost.
- **From:** [Semantics](../Semantics/README.md), [Pull: Hop and fanout](../Semantics/Pull.md#hop-and-fanout), [Research: Semantics Experiments: Translation through the ILI](../Research/Semantics-Experiments.md#translation-through-the-ili), [Research: Semantics Experiments: Observation and attestation together](../Research/Semantics-Experiments.md#observation-and-attestation-together).

### 15.7 Measure degrees

- **In:** two entities.
- **Do:** degrees of separation, as in a Bacon number or an Erdős number, measure how far anything is from anything else: an A-star search from one to the other over the costs of 15.4, limited by the search fan, the number of hops a chain may run, and λ. Landmarks and the geodesic distance on the S³ give consistent heuristics; when positions are derived from content rather than from relations, the geometric heuristic is close to zero and A* behaves like Dijkstra, still exact. The trip is route planning. The road classes are the identifier systems, the Engine's highway type lists: words in each language, a wordnet's synsets, the ILI, the interlingual freeway, ISO 639 languages, FrameNet frames, frame elements, and lexical units, VerbNet classes and roles, PropBank rolesets, VerbAtlas frames, and the part-of-speech, dependency, and lexicographer-file inventories. The interchanges are the mapping strands where a route changes class: lexicalizations, word to synset or ILI with its language, CILI's maps, SemLink, the Predicate Matrix, MapNet, VerbAtlas, WordFrameNet, FrameBase. A-star plans trips that change class at interchanges; road speed is confidence, λ the turn penalty per hop, the fan the lanes considered at a node, the envelope the trip's limits, and the firmware the driver's preferences. Because the geometric heuristic is close to zero, landmarks, the highway nodes, give the heuristic, and the Engine's highway ROM, its type lists and mapping edges, is the precomputed freeway network. As built, the Engine's reads run Dijkstra, an estimate of 0, over claims read from the database, and never walk the highway ROM's edges; the acceptance trip is `dog` to its OEWN synset to `i46360` to `[犬, jpn]`, printed leg by leg.
- **Out:** the cheapest chain, or what is nearest. There is no one context-free universal distance: a raw degree counts admitted transitions, a witnessed degree passes every edge through an evidence floor, a typed degree uses selected relation families only, a temporal degree a historical world boundary, a source degree restricted providers, a cross-domain degree required modal transitions.
- **From:** [Pull: The web](../Semantics/Pull.md#the-web), `docs/guides/knowledge-arena.md` §Laplace Degree, [Research: Relations Research: Heuristics](../Research/Relations.md#heuristics).

### 15.8 Read a distribution only when asked

- **In:** a subject and a relation.
- **Do:** the normalized distribution over a subject's objects under one relation comes from the Glicko-2 log-odds of the cells, not from a dot product, and it returns the empty set when the subject couples to nothing, the answer a softmax cannot give. With collections in place it is a distribution over attested analyses, not over individually attested tags. It is a read for a caller that asked for a distribution; the forward program itself keeps the typed set.
- **Out:** the distribution, or nothing.
- **From:** `docs/specs/38_Collections_Are_Compositions.md` (belief distribution).

## What this stage leaves behind

Hop and fanout from anything to anything, each strand read as a confidence and a cost, each step O(log N) + O(K): an index lookup and the ordering of what it returned.

## Without this stage

An entity is a record with a standing and no neighbors.
