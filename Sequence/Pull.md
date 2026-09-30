# 19. Pull

A lookup computes the ID on the client and hits the indexes, and every operator the forward program can call, containment, gap, continuation, shape, relation read, and batch realization, is an indexed set access followed by one native operation.

Laplace finds content by computing its ID and coordinates on the client and looking them up with spatial indexes. These are the operators a routed program calls inside SCAN, COMPOSE, and REALIZE; A*, Dijkstra, strongest-first walk, containment, trajectory continuation, and geometry are operators inside the program, and none alone is the cognition. Each obeys the execution-grain law: bounded set-sized PostgreSQL access through prepared SPI, one coarse native C program, loops and recursion and reductions inside it, a bounded result and a receipt.

## Before this stage

[14. Indexes](Indexes.md), [15. Web](Web.md), [17. Envelope](Envelope.md), and [18. Firmware](Firmware.md).

## Operations: lookups

### 19.1 Compute the ID on the client

- **In:** any content, and the memory-mapped tier 0.
- **Do:** [11. Content](Content.md) operations 11.2 to 11.5, on the client, with no database call: the UAX #29 decomposition of "Sherlock Holmes" is `[[S,h,e,r,l,o,c,k], ' ', [H,o,l,m,e,s]]`, and that trunk has one deterministic ID for all of it, and one coordinate. Inside the database the same computation is a native function, evaluated once when the query is planned, so the query becomes an index lookup on the result.
- **Out:** the ID and coordinates of the real Merkle DAG of the content.
- **Mechanism:** `entity_named` → `lp_text_parts` over the mapped tier 0, no database call ([Reads: Naming an entity](../Reference/Reads.md#naming-an-entity)); `laplace text` prints it ([CLI: laplace text](../Reference/CLI.md#laplace-text)); inside the database `laplace_id(text)` and `laplace_parts(text)` ([SQL: Identity](../Reference/SQL.md#identity)). Status: **built**.
- **From:** [Query: Lookup by ID](../Query.md#lookup-by-id), [Query: Functions in queries](../Query.md#functions-in-queries), [Identity: Client-side computation](../Storage/Identity.md#client-side-computation).

### 19.2 Look up by ID

- **In:** the ID of 19.1.
- **Do:** the B-tree of [14. Indexes](Indexes.md) operation 14.1, pruned to one partition by the ID's first hex digit; then the entity's stored counts.
- **Out:** the entity, its coordinate, its containers, and its occurrences, or not found.
- **Check:** "Holmes": 527 containers, 574 occurrences, 0.02 ms. A word never recorded: 0.01 ms.
- **Mechanism:** the `entity_id` index per partition; the engine's `SELECT 1 FROM entity WHERE id = ANY(…)` ([Ingest: The statements](../Reference/Ingest.md#the-statements)). Stored counts do not exist. In the monorepo: `n_constituents` and `entities.type_id`; `ops.entity_record`. Status: **built; stored counts prototype**.
- **From:** [Query: Lookup by ID](../Query.md#lookup-by-id), [Research: Engine Measurements: Queries](../Research/Engine.md#queries).

### 19.3 Find every container

- **In:** the ID of 19.1.
- **Do:** the GIN of [14. Indexes](Indexes.md) operation 14.4 finds every container of that ID, such as every sentence that contains a word. File metadata trees are searchable the same way as content: "Show me all ISO 100 images."
- **Out:** every path that holds the entity.
- **Check:** every container of `Holmes`, 527 records, 0.80 ms; every container of the hub `the`, 864,949, 309 ms.
- **Mechanism:** `physicality WHERE path @> ARRAY[id]` through `physicality_paths` ([Reads: laplace hop](../Reference/Reads.md#laplace-hop), [SQL: Containment and the GIN](../Reference/SQL.md#containment-and-the-gin)). In the monorepo: `structural.containers_of` over `containers_of.c`. Status: **built**.
- **From:** [Query: Containers and occurrences](../Query.md#containers-and-occurrences), [Query: Files](../Query.md#files), [Research: Engine Measurements: Storage at volume](../Research/Engine.md#storage-at-volume).

### 19.4 Match a run inside containers

- **In:** a phrase, as its own path from 19.1.
- **Do:** a phrase is a trajectory, like every stored path: "the capital of " is `[the, ' ', capital, ' ', of, ' ']`. One GIN lookup finds the containers holding every constituent. Then the phrase is encoded once into vertex bytes and compared with the raw stored vertices of each container, 16 bytes per SIMD compare, at the vertex scan rate of one core's memory bandwidth; a match is a window of the container's path equal to the phrase's path, at Fréchet distance 0. Only matches are decoded.
- **Out:** every container holding the run, and where.
- **Check:** the run `[Sherlock, ' ', Holmes]`, 92 sentences, 1.76 ms. The native compare took 30 ms where decoding every candidate in Python took 4,558 ms and PostGIS's 2D `ST_Covers` 6.4 s.
- **Mechanism:** `lp_follows`: the phrase encoded once, a SIMD scan of the container's raw vertices ([Native: Trajectory matching](../Reference/Native.md#trajectory-matching-followsc)); `laplace_follows(geometry, blake3[])` in SQL ([SQL: Paths](../Reference/SQL.md#paths)). In the monorepo: `trajectory_continuations.c`, `generation.trajectory_continuations`, `corpus.corpus_trajectory_probe`. Status: **built**.
- **From:** [Query: Gaps](../Query.md#gaps), [Research: Prototype: Continuation as geometry](../Research/Prototype.md#continuation-as-geometry), [Research: Corpus Search: How Laplace finds the containers](../Research/Corpus-Search.md#how-laplace-finds-the-containers).

### 19.5 Read a gap or a continuation

- **In:** a phrase with a gap, or a phrase to continue.
- **Do:** containers can be searched with gaps: every "Captain ␣ Name" in Moby Dick, reading what fills the gap. A continuation is the vertex that follows each matching window. Each result is counted by occurrence across every source.
- **Out:** what fills the gap, or what follows, with counts.
- **Check:** `[Captain, ' ', ?]` in Moby Dick: Ahab 105, Peleg 52, Bildad 27, and ordinary words such as "in" and "of", 9.2 ms; filtering the fillers by their part-of-speech attestations from the treebanks and Wiktionary and dropping function words, verbs, pronouns, and adverbs leaves the nine captains. What follows "the capital of ": the 456, a 82, an 15, his 12, one 7, Italy 6, Armenia 3, 24.7 ms. Against a language model interviewed with 285 such templates, the model's first choice was the continuation Laplace observed most often 43.9% of the time, in 2,217 ms against 84 ms.
- **Mechanism:** `laplace fills`: containers, `lp_follows` for the run, `laplace_path_times` leaf to trunk, occurrences trunk to leaf ([Reads: laplace fills](../Reference/Reads.md#laplace-fills)); a gap is the bench's `[Captain, ' ', ?]` query. In the monorepo: `generation.continuation_conditional_plane`, `realize.render_gaps`. Status: **built**.
- **From:** [Query: Gaps](../Query.md#gaps), [Research: Engine Measurements: Queries](../Research/Engine.md#queries), [Research: Semantics Experiments: Observation and attestation together](../Research/Semantics-Experiments.md#observation-and-attestation-together), [Research: Model Ingestion: Interviewing a model with templates](../Research/Models.md#interviewing-a-model-with-templates).

### 19.6 Compare shapes

- **In:** an entity's tree, and the measure the firmware set in [18. Firmware](Firmware.md) operation 18.8.
- **Do:** shape is the tree. A composition is a tree of constituents across tiers, and its trajectory is that tree recorded in order. Fréchet distance, Fréchet distance tolerant of *k* outliers, DTW, and EDR compare those trees, each answering a different kind of difference, on the real coordinates of the entities, never the packed mantissas. Discrete Fréchet is a dynamic program over the two vertex sequences with the 4D chord as ground distance, O(*pq*), a metric, invariant to duplicated vertices; the 4D GiST and the endpoint lower bounds form the candidate stage ahead of the exact recheck in C. Nearest neighbors in 4D come from the GiST on the real coordinates: the nearest word segments to `king` are `king`, then its anagrams, because order is carried by the path, not the centroid.
- **Out:** matching shapes, and the content that has that shape.
- **Check:** the comparison adds a semantic relation the ID does not: two logs with different timestamps are different content with different IDs, and their trees can still be the same pattern, so one log's shape can lie very close to 50,000 others across 1,000 clients and 10,000 repositories, and finding the pattern once is finding all of them. Discrete Fréchet on 1,000 × 1,000 vertices, 3.8 ms; 16 nearest to `king`, 7.7 ms.
- **Mechanism:** `lp_frechet4`, `lp_frechet4_outliers`, `lp_dtw4`, `lp_edr4` ([Native: Shape measures](../Reference/Native.md#shape-measures-geom4dc)); `laplace_frechet4d`, `laplace_dtw4d`, `laplace_edr4d` ([SQL: Shape measures](../Reference/SQL.md#shape-measures)); nearest by `coord <<->> laplace_coord('king')` on the GiST ([Schema: Indexes](../Reference/Schema.md#indexes)). No read command runs a shape search. In the monorepo: `structural.nearest_neighbors_4d`, `structural.word_shape_distance`, `structural.entity_curve`, `math4d_frechet`, `math4d_hausdorff` ([Monorepo: The native engine](../Reference/Monorepo.md#the-native-engine)). Status: **built as functions; monorepo with the shape search**.
- **From:** [Query: Shape](../Query.md#shape), [Physicality: Centroids](../Storage/Physicality.md#centroids), `docs/specs/05_Substrate_Invariants.txt` Rule #2, [Research: Geometry: Fréchet distance](../Research/Geometry.md#fréchet-distance), [Research: Numerics: Trajectory measures](../Research/Numerics.md#trajectory-measures), [Research: Engine Measurements: Native operations](../Research/Engine.md#native-operations).

### 19.7 Realize the curve, never the carrier

- **In:** a packed trajectory.
- **Do:** unpack each vertex to its constituent id and metadata, resolve each child's physicality, read the child's real coordinate, order by logical ordinal, expanding split runs, and build the realized curve. Every geometric operator of 19.6 runs on that curve. Packed vertex values are not child coordinates, a point cannot answer an order question, and a packed trajectory cannot be passed to a distance operator as if its mantissas were spatial coordinates.
- **Out:** the realized child-coordinate curve, inside the ball by convexity.
- **Mechanism:** the shape functions take real-coordinate POINT ZM or LINESTRING ZM only ([SQL: Shape measures](../Reference/SQL.md#shape-measures)); no built function turns a packed path into its children's coordinate curve. In the monorepo: `sql/functions/structural/entity_curve.sql.in` unpacks each vertex, resolves the child's physicality, reads its coordinate, and orders by ordinal ([Monorepo: Identity and placement](../Reference/Monorepo.md#identity-placement-and-the-carrier)). Status: **monorepo; the primitives built**.
- **From:** `docs/INVENTION.md` §4 "Packed trajectory is not realized geometry"; `docs/specs/05_Substrate_Invariants.txt` Rules #2, #4.

### 19.8 Read a relation through a declared task shape

- **In:** a request's ordered surface and the declared relation-read shapes of the operational seed.
- **Do:** a task shape is an authored, admitted declaration: an exemplar parse, a predicate, and token slots each with an accepted entity type and a binding mode, recorded as a type-8 structural trajectory `[schema, exemplar_parse, predicate, (slot, token_ref, accepted_type, binding_mode)*, slots_end]` under one source-file context, with `exemplar_parse IS_EXAMPLE_OF shape`, `shape CALLS predicate`, and `shape HAS_INPUT slot`. The matcher retains dependency topology, features, language, order, punctuation, and all undeclared lexical structure; only the declared slots may vary, and their current bindings must satisfy the declared type; additional unmatched content prevents a match. A new request need not have an observed parse: its complete ordered surface instantiates the declared substitutions as an inference with its own recipe identity, never recorded as a new parse. The program binds the current input ids and reads the actual predicate results; no expected answer is stored, competing complete interpretations remain ambiguous, and the receipt commits the shape, the parse identities, and the applicability witnesses. `define justice` and `The opposite of empty is` are the two bundled shapes; the runtime holds no English keyword dispatch.
- **Out:** the predicate's actual results for the bound slots, or unresolved.
- **Check:** a missing relation result stays unresolved even when two positively witnessed lemma alternatives have their own results; changing the witnessed result on the current word changes the emitted identity while every byte of the task stays unchanged.
- **Mechanism:** none: the nearest built read is `laplace hop SUBJECT PREDICATE OBJECT` with `?` ([CLI: laplace hop](../Reference/CLI.md#laplace-hop)). In the monorepo: `task_shape.c`, `converse.query_shapes`, the seeds `seeds/operational/tasks/en_define.json` and `en_antonym.json`, `tests/sql/task_shapes.sql` ([Monorepo: Firmware and the forward program](../Reference/Monorepo.md#firmware-and-the-forward-program)). Status: **monorepo; not in the split repositories**.
- **From:** `seeds/operational/README.md` §Declared relation-read task shapes.

### 19.9 Look up a bundle's members and its subjects

- **In:** a subject and a relation, or a relation and a member set.
- **Do:** the members of a subject's collection under one relation are the bundle's constituents in canonical order, read through the trajectory; the subjects that carry a given member set are a GIN containment probe on the bundle followed by the reverse edge, resolving the bundle first so the partition prunes.
- **Out:** members, or subjects.
- **Mechanism:** none: no collections ([Conflicts T2](Conflicts.md)). In the monorepo: set trajectories and their GIN; the member and subject reads of spec 38 §5 were not verified. Status: **monorepo in part**.
- **From:** `docs/specs/38_Collections_Are_Compositions.md` §5.

### 19.10 Realize in batch, at the edge

- **In:** a set of selected ids.
- **Do:** display labels are a final operation, not during the recursion and heavy lifting: Laplace speaks Unicode and renders language, so nothing cares about output characters until rendering. A human- or UI-facing serving operation returns the content id and its display label in the same row; a machine-hop, fold, or internal set-returning operation returns ids and lets the caller batch realization at the edge. Never realize or render once per row when a batch form exists. A selected identity does not need a precomputed text label to be valid; an unresolved entity or a bare hash is not proper output; identifiers realize through their bindings in the query's language. Realization is bulk and native, one selected structure never becoming thousands of per-constituent crossings.
- **Out:** the requested surface, for the whole set.
- **Mechanism:** the `Reader` fetches paths one level at a time for every entity at once and expands in the engine ([Reads: laplace hop](../Reference/Reads.md#laplace-hop)); `laplace_text(blake3)` is the per-row form ([SQL: Paths](../Reference/SQL.md#paths)). In the monorepo: `realize.realize_batch`, `readback.render_text_batch`, `converse.label_batch`. Status: **built**.
- **From:** `docs/specs/06_Engineering_Ruleset.txt` Rule #14; `docs/read-path.md` §8; `docs/INVENTOR_RECORD.md` §The forward pass.

## The rules every operator obeys

Reduce before expanding: apply indexed identity, relation, source, context, and band constraints before fan-out; never create cartesian candidates and repair them with a final `LIMIT`; a result limit requires a ranking produced by the evidence model. Preserve planner-visible SQL: comparison points reach the planner as bound parameters, and every CTE declares `MATERIALIZED` or `NOT MATERIALIZED`. Fence expensive stable calls deliberately, because a stable function in a filter can run once per candidate row. Supply the relation, type, subject, direction, and scope the physical schema prunes on. One implementation per fact: a native replacement declares its name, input domain, output order, null and unknown behaviour, score equation, and parity test, and a `_fast` suffix excuses no drift. See `docs/specs/06_Engineering_Ruleset.txt` Rules #2, #3, #6, #7, #13, #15 and `docs/read-path.md` §7.

## What this stage leaves behind

Every operator a program can route, each an indexed probe and one native operation, each with its cost named by its actual provider and algorithm rather than a blanket O(K).

## Without this stage

The forward program has nothing to call.
