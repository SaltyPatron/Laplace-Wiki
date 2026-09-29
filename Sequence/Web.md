# 12. Web

With standings on every claim, a pull reads a standing as a confidence and a cost, and hops and fans out over the web at O(log N) + O(K) a step.

When entities and physicalities are recorded, additional records and relations are added to form a spider colony web: N spiders, all with interwoven webs, where pulling on one strand makes everything else tug back. Consensus tells how hard it tugs back.

## Before this stage

[10. Consensus](Consensus.md): a standing on every claim. [11. Indexes](Indexes.md): the lookups a hop is made of.

## Operations, per hop

### 12.1 Find the strands that hold an entity

- **In:** an entity's ID.
- **Do:** look up every claim that holds the entity in any of its places, through the semantics indexes of [11. Indexes](Indexes.md) operation 11.6, and every container that holds it, through the GIN of operation 11.4.
- **Out:** the set of strands leaving the entity. Fanout is the number of them: the number of properties recorded of a codepoint, of senses and translations leaving an entry, of edges leaving a concept, of dependents of a head.
- **Check:** `dog` in the engine database returns 612 claims, 131 matched at least once and 481 untouched stock.
- **From:** [Pull: Hop and fanout](../Semantics/Pull.md#hop-and-fanout), [Personality firmware: What was measured on one entity](../Semantics/Firmware.md#what-was-measured-on-one-entity).

### 12.2 Read each strand's standing as a confidence

- **In:** the standings of the strands.
- **Do:** the pull does not change a standing. What the pull selects on is a reading of it. The anchor is rating 1500. A claim's confidence is the chance it beats that anchor, taken *k* deviations below its rating, on Glicko-2's scale of 173.7178: *p* = σ((*r* − 1500)/173.7178 − *k* · RD/173.7178). *k* is a restriction on uncertainty: at *k* = 0 the rating is taken as it stands; each step of *k* demands that the rating still hold further down inside its deviation, so a claim few witnesses have touched tugs less than its rating alone says.
- **Out:** a confidence per strand.
- **Check:** a standing of 1774.3 with deviation 93.3 reads as 0.829 at *k* = 0 and 0.624 at *k* = 2. Untouched stock at deviation 250 reads 0.500 at *k* = 0 and 0.053 at *k* = 2; at deviation 350, 0.018. Two standings, 1700 at deviation 300 and 1600 at deviation 40, cross at *k* = 0.38: below it the louder rating is selected, above it the tighter deviation. Nothing in the two standings changed.
- **From:** [Personality firmware: How a standing is read](../Semantics/Firmware.md#how-a-standing-is-read).

### 12.3 Turn the confidence into a cost

- **In:** the confidence of 12.2.
- **Do:** the cost of crossing the claim is −ln *p* + λ, with λ a tax paid once per hop. Costs add, so the cheapest chain is the one whose confidences multiply to the most, shortened by the tax. Costs are non-negative, so Dijkstra and A* are exact, and a heuristic computed under an optimistic cost stays admissible and consistent when ratings change. λ decides whether a longer, stronger chain beats a shorter, weaker one: two hops at 0.90 cost 0.211 + 2λ, one hop at 0.70 costs 0.357 + λ, and they cross at λ = 0.146.
- **Out:** a cost per strand.
- **From:** [Personality firmware: How a standing is read](../Semantics/Firmware.md#how-a-standing-is-read), [Personality firmware: How far a search walks](../Semantics/Firmware.md#how-far-a-search-walks), [Research: Relations Research: Edge cost](../Research/Relations.md#edge-cost).

### 12.4 Refuse what the firmware refuses, then apply the fan

- **In:** the strands of 12.1.
- **Do:** a restriction is applied before the sort: strands of a kind the firmware does not navigate, such as layout, punctuation, a part of speech, a witness, or a language, are dropped. Then the fan: a hop reads at most so many claims that hold the entity, and a search at most so many, and orders that set by confidence. An entity that holds more claims than the fan, a part of speech, a language, is a hub: reached and not crossed. The limit is applied before the ordering, so past the fan the set is whatever the index returned.
- **Out:** the ordered set of strands the firmware allows.
- **Check:** on `dog` at *k* = 2, always taking the top: `[dog, LEMMA, dog]` 0.972, `[dog, UPOS, NOUN]` 0.969, `[dog, XPOS, NN]` 0.966, `[dog, SpaceAfter, No]` 0.943, `[犬, Gloss, dog]` 0.902. The fourth is a typesetting observation, and determiners and a punctuation mark sit in the same tenth as the gloss. The top three are 0.003 apart.
- **From:** [Personality firmware: What was measured on one entity](../Semantics/Firmware.md#what-was-measured-on-one-entity), [Personality firmware: How far a search walks](../Semantics/Firmware.md#how-far-a-search-walks).

### 12.5 Hop, or bubble up and down

- **In:** the set of 12.4.
- **Do:** follow a strand to the entity at its other end, and repeat from 12.1. For a change of language, bubble up to the ILI, change the language, and bubble down: `[dog, eng, ?]` ordered by observed usages, then the witness's sense order, then standing, gives i46360; `[?, language, i46360]` for eight languages, ordered by standing, gives `Hund`, `chien`, `perro`, `犬`, `cane`, `koira`, `pies`, `كلب`. From `Butler`, Laplace can pull a great deal of information and link it to `butler`; the two are different entities 0.045 apart on the S³, one a surname, the other a noun and a verb, and a witness attests the etymology that joins them.
- **Out:** the next entity, and the chain so far with its accumulated cost.
- **Check:** the two translation lookups took 3.3 ms and 1.2 ms.
- **From:** [Semantics](../Semantics/README.md), [Pull: Hop and fanout](../Semantics/Pull.md#hop-and-fanout), [Research: Semantics Experiments: Translation through the ILI](../Research/Semantics-Experiments.md#translation-through-the-ili), [Research: Semantics Experiments: Observation and attestation together](../Research/Semantics-Experiments.md#observation-and-attestation-together).

### 12.6 Measure degrees

- **In:** two entities.
- **Do:** degrees of separation, as in a Bacon number or an Erdős number, measure how far anything is from anything else: an A-star search from one to the other over the costs of 12.3, limited by the search fan, the number of hops a chain may run, and λ. Landmarks and the geodesic distance on the S³ give consistent heuristics; when positions are derived from content rather than from relations, the geometric heuristic is close to zero and A* behaves like Dijkstra, still exact.
- **Out:** the cheapest chain, or what is nearest.
- **From:** [Pull: The web](../Semantics/Pull.md#the-web), [Research: Relations Research: Heuristics](../Research/Relations.md#heuristics).

## What this stage leaves behind

Hop and fanout from anything to anything, each strand read as a confidence and a cost, each step O(log N) + O(K): an index lookup and the ordering of what it returned.

## Without this stage

An entity is a record with a standing and no neighbors.
