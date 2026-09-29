# 14. Pull

A lookup computes the ID on the client and hits the indexes, and the forward pass pulls segments and strands under the firmware.

Laplace finds content by computing its ID and coordinates on the client and looking them up with spatial indexes. Its forward pass is native C recursive operations with A* and indexed lookups, pulling on the interwoven web under the firmware. Everything before this stage exists so that this stage can answer.

## Before this stage

[11. Indexes](Indexes.md), [12. Web](Web.md), and [13. Firmware](Firmware.md).

## Operations: lookups

### 14.1 Compute the ID on the client

- **In:** any content, and the memory-mapped tier 0.
- **Do:** [8. Content](Content.md) operations 8.2 to 8.5, on the client, with no database call: the UAX #29 decomposition of "Sherlock Holmes" is `[[S,h,e,r,l,o,c,k], ' ', [H,o,l,m,e,s]]`, and that trunk has one deterministic ID for all of it, and one coordinate. Inside the database the same computation is a native function, evaluated once when the query is planned, so the query becomes an index lookup on the result.
- **Out:** the ID and coordinates of the real Merkle DAG of the content.
- **From:** [Query: Lookup by ID](../Query.md#lookup-by-id), [Query: Functions in queries](../Query.md#functions-in-queries), [Identity: Client-side computation](../Storage/Identity.md#client-side-computation).

### 14.2 Look up by ID

- **In:** the ID of 14.1.
- **Do:** the B-tree of [11. Indexes](Indexes.md) operation 11.1, pruned to one partition by the ID's first hex digit; then the entity's stored counts.
- **Out:** the entity, its coordinate, its containers, and its occurrences, or not found.
- **Check:** "Holmes": 527 containers, 574 occurrences, 0.02 ms. A word never recorded: 0.01 ms.
- **From:** [Query: Lookup by ID](../Query.md#lookup-by-id), [Research: Engine Measurements: Queries](../Research/Engine.md#queries).

### 14.3 Find every container

- **In:** the ID of 14.1.
- **Do:** the GIN of [11. Indexes](Indexes.md) operation 11.4 finds every container of that ID, such as every sentence that contains a word. File metadata trees are searchable the same way as content: "Show me all ISO 100 images."
- **Out:** every path that holds the entity.
- **Check:** every container of `Holmes`, 527 records, 0.80 ms; every container of the hub `the`, 864,949, 309 ms.
- **From:** [Query: Containers and occurrences](../Query.md#containers-and-occurrences), [Query: Files](../Query.md#files), [Research: Engine Measurements: Storage at volume](../Research/Engine.md#storage-at-volume).

### 14.4 Match a run inside containers

- **In:** a phrase, as its own path from 14.1.
- **Do:** a phrase is a trajectory, like every stored path: "the capital of " is `[the, ' ', capital, ' ', of, ' ']`. One GIN lookup finds the containers holding every constituent. Then the phrase is encoded once into vertex bytes and compared with the raw stored vertices of each container, 16 bytes per SIMD compare, at the vertex scan rate of one core's memory bandwidth; a match is a window of the container's path equal to the phrase's path, at Fréchet distance 0. Only matches are decoded.
- **Out:** every container holding the run, and where.
- **Check:** the run `[Sherlock, ' ', Holmes]`, 92 sentences, 1.76 ms. The native compare took 30 ms where decoding every candidate in Python took 4,558 ms and PostGIS's 2D `ST_Covers` 6.4 s.
- **From:** [Query: Gaps](../Query.md#gaps), [Research: Prototype: Continuation as geometry](../Research/Prototype.md#continuation-as-geometry), [Research: Corpus Search: How Laplace finds the containers](../Research/Corpus-Search.md#how-laplace-finds-the-containers).

### 14.5 Read a gap or a continuation

- **In:** a phrase with a gap, or a phrase to continue.
- **Do:** containers can be searched with gaps: every "Captain ␣ Name" in Moby Dick, reading what fills the gap. A continuation is the vertex that follows each matching window. Each result is counted by occurrence across every source.
- **Out:** what fills the gap, or what follows, with counts.
- **Check:** `[Captain, ' ', ?]` in Moby Dick: Ahab 105, Peleg 52, Bildad 27, and ordinary words such as "in" and "of", 9.2 ms; filtering the fillers by their part-of-speech attestations from the treebanks and Wiktionary and dropping function words, verbs, pronouns, and adverbs leaves the nine captains. What follows "the capital of ": the 456, a 82, an 15, his 12, one 7, Italy 6, Armenia 3, 24.7 ms. Against a language model interviewed with 285 such templates, the model's first choice was the continuation Laplace observed most often 43.9% of the time, in 2,217 ms against 84 ms.
- **From:** [Query: Gaps](../Query.md#gaps), [Research: Engine Measurements: Queries](../Research/Engine.md#queries), [Research: Semantics Experiments: Observation and attestation together](../Research/Semantics-Experiments.md#observation-and-attestation-together), [Research: Model Ingestion: Interviewing a model with templates](../Research/Models.md#interviewing-a-model-with-templates).

### 14.6 Compare shapes

- **In:** an entity's tree, and the measure the firmware set in [13. Firmware](Firmware.md) operation 13.8.
- **Do:** shape is the tree. A composition is a tree of constituents across tiers, and its trajectory is that tree recorded in order. Fréchet distance, Fréchet distance tolerant of *k* outliers, DTW, and EDR compare those trees, each answering a different kind of difference, on the real coordinates of the entities, never the packed mantissas. Discrete Fréchet is a dynamic program over the two vertex sequences with the 4D chord as ground distance, O(*pq*), a metric, invariant to duplicated vertices; the 4D GiST and the endpoint lower bounds form the candidate stage ahead of the exact recheck in C. Nearest neighbors in 4D come from the GiST on the real coordinates: the nearest word segments to `king` are `king`, then its anagrams, because order is carried by the path, not the centroid.
- **Out:** matching shapes, and the content that has that shape.
- **Check:** the comparison adds a semantic relation the ID does not: two logs with different timestamps are different content with different IDs, and their trees can still be the same pattern, so one log's shape can lie very close to 50,000 others across 1,000 clients and 10,000 repositories, and finding the pattern once is finding all of them. Discrete Fréchet on 1,000 × 1,000 vertices, 3.8 ms; 16 nearest to `king`, 7.7 ms.
- **From:** [Query: Shape](../Query.md#shape), [Physicality: Centroids](../Storage/Physicality.md#centroids), [Research: Geometry: Fréchet distance](../Research/Geometry.md#fréchet-distance), [Research: Numerics: Trajectory measures](../Research/Numerics.md#trajectory-measures), [Research: Engine Measurements: Native operations](../Research/Engine.md#native-operations).

## Operations: the forward pass

### 14.7 Ingest the prompt

- **In:** a prompt.
- **Do:** a prompt is ingested as text, broken down, and given a trunk node ID: [8. Content](Content.md), in full. UAX #29 is the tokenizer and the trunk ID is the token index. There is no context window: the prompt is content, and any portion of the database, of any size, can be treated as a prompt against itself.
- **Out:** the prompt's trunk, its tree across tiers, and every observation its trajectory carries.
- **From:** [Pull: The forward pass](../Semantics/Pull.md#the-forward-pass), [Personality firmware: Instruction sets](../Semantics/Firmware.md#instruction-sets).

### 14.8 Gather the observation, the attestations, and the tree

- **In:** the trunk of 14.7.
- **Do:** what a step has to work from is the observation, the attestations on that observation, and the observation's whole tree across tiers. The observation is the trajectory: precedes, contains, co-occurrence, and the shape of the path, from 14.3 to 14.6. The attestations are the claims witnessed of that same content, from [12. Web](Web.md) operation 12.1. The tree is the composition, from tier 0 up through every constituent and every container: "The cat sat on the mat" is one tier-3 node of eleven constituents; `cat` is one segment of that branch; `sat on the` is another; the letters of `cat` are the tier-0 branch under the word.
- **Out:** the set. None of it is a probability.
- **From:** [Pull: The forward pass](../Semantics/Pull.md#the-forward-pass), [Personality firmware: The decision tree](../Semantics/Firmware.md#the-decision-tree).

### 14.9 Step, under the firmware

- **In:** the set of 14.8 and the firmware.
- **Do:** a step is native C: A* and indexed lookup, O(log N) + O(K), with no softmax and no context window. Which operation runs, which segment it lifts, how far it hops and fans out, what it refuses, how it weighs context words, whether it takes the top, and whether one high-trust attestation is returned as a fact, are the firmware's, [13. Firmware](Firmware.md) operations 13.2 to 13.9. A step can return any segment of the branch, or a combination: the word together with a gloss attested of it, the remainder of the sentence, the letters, or all three. Nothing is brute-forced.
- **Out:** a segment, a set, a combination, or a fact.
- **From:** [Pull: The forward pass](../Semantics/Pull.md#the-forward-pass), [Pull: The choice](../Semantics/Pull.md#the-choice).

### 14.10 Repeat, recursively

- **In:** the result of 14.9.
- **Do:** the forward pass is recursive: the result is content, so it has a trunk, a tree, observations, and attestations, and the next step works from those. Each step is a lookup and a choice, and no step changes a standing.
- **Out:** the answer, when the firmware stops.
- **From:** [Pull: The forward pass](../Semantics/Pull.md#the-forward-pass).

## What this stage leaves behind

An answer: a set, a segment of a branch, a combination, or a single fact.

## Without this stage

Nothing answers.
