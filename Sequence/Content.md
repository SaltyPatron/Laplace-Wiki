# 11. Content

Content runs one ordered ingest spine: unpack, records, working-set deduplication, accumulation, bulk tier descent, apply by COPY, fold completion, and a receipt, with the DAG built and hashed on the client and deduplicated trunk to leaf against what is already recorded.

Ingestion is the learning process. It computes content's IDs on the client and deduplicates it trunk to leaf against what is already recorded. Everything this stage records is observation: what the content is and how it lies, with no one yet saying anything about it. A source adapter recovers its source faithfully and maps fields into declared roles; it does not get a private identity law, scheduler, semantic engine, or persistence model.

## Before this stage

[5. Tier 0](Tier-0.md): the perf-cache the client maps. [7. Perfcaches](Perfcaches.md): the number, separator, and any higher ROMs. [8. Database](Database.md): the tables. [9. Sources](Sources.md): the active source generation. [10. Recipes](Recipes.md): the recipe for the file's format.

## The spine

```text
unpack → records → working-set dedup → accumulation → bulk tier descent → apply/COPY → fold completion
```

Decomposers are pure content-to-change streams with no inline SQL, and they declare every relation they emit. The shared spine owns batching, novelty proof, tier descent, COPY, attestation merge, consensus fold, and completion semantics. The right operation at the wrong stage violates this rule. Parallel producers communicate through bounded channels; per-cell non-commutative folds keep FIFO order, commutative deposits may run concurrently; outer index-build concurrency stays at one unless measured safe. Batch, commit, and working-set sizing derive from source shape and machine capacity, not from environment overrides.

## Operations, per source

### 11.1 Unpack the artifact graph

- **In:** the active source generation, its artifact graph with dispositions.
- **Do:** open each admitted artifact through its provider: decode the container, unpack archive members, stream the feed. Choose the physical plan from actual topology, resources, and source structure: if the admitted plan has memory for a complete artifact plus its composition, parser, and dedup scratch, a whole working set is valid; streaming is valid when the source or the resource plan requires it; streaming partitions are physical only and disappear from canonical results. One generic resource authority admits reader, parser, native, and persistence concurrency; a source never takes all visible CPUs independently, and serviceable work reserves database, product, runner, and control-plane headroom. A file, document, or source object stays one exact semantic object while its internally independent work is scheduled at a finer dependency-aware grain.
- **Out:** the provider's records, spans, fields, errors, and packaging facts, per artifact, with journal and resume accounting.
- **From:** `docs/plan/INGEST_BOUNDARY_AND_RECIPE_LAW.md` §Whole working set versus streaming, §Benchmark lesson, §Resource ownership; `docs/specs/06_Engineering_Ruleset.txt` Rules #10 and #12.

### 11.2 Name the file by its trunk

- **In:** each artifact.
- **Do:** a file is a trunk, `[metadata, content]`, in the DAG, and its ID is the hash of its constituents like any other node's. A file's bytes are never hashed to name it or to mark it, and file timestamps do not define file identity. Whether a file is already recorded is not known here: it is asked in 11.8, by the trunk's ID, once the client has decomposed the file and has that ID from 11.5.
- **Out:** every artifact goes on to 11.3; none is passed over before its trunk ID exists.
- **From:** [Compositions: Files](../Storage/Compositions.md#files); [Identity: Pure content](../Storage/Identity.md#pure-content); [Ingestion: Deduplication](../Storage/Ingestion.md#deduplication).

### 11.3 Decompose on the client

- **In:** the artifact and its recipe.
- **Do:** the client breaks content down using the memory-mapped tier 0 and the ROMs of [7. Perfcaches](Perfcaches.md), in native code over a working set or batch, never one call per scalar, token, node, or record. Text goes through UAX #29 into sentences, words, graphemes, and codepoints; a grapheme of one codepoint is that codepoint. A composition is an n-ary, recursive sequence of constituents, each of which is a codepoint or another composition. Nothing is dropped: "The cat sat on the mat" is `[The, ' ', cat, ' ', sat, ' ', on, ' ', the, ' ', mat]`, and "Sherlock Holmes" is `[[S,h,e,r,l,o,c,k], ' ', [H,o,l,m,e,s]]`. Text is recorded as it arrives, without normalization: precomposed and decomposed forms are different content. Case is never folded: `King` is not `king`, and attestations link them. A number decomposes to its digit codepoints under the scalar recipe and composes to one reusable root; a pixel's channels reference number roots; a sample references a scalar root; a code file's syntax subtrees compose bottom-up with the gaps as text constituents; an image composes pixels into patches, regions, and the image, with every contiguous square substructure an occurrence of a global root; a checkpoint's tokenizer composes as one ordered vocabulary. Every core decomposes.
- **Out:** the artifact's Merkle DAG, in memory on the client, under a source trunk, a file trunk, a metadata tree, and a content tree. [Corpora: Universal Dependencies](../Corpora/Universal-Dependencies.md) works the chain through from the corpus's one trunk to the codepoints.
- **From:** [Ingestion: Client-side](../Storage/Ingestion.md#client-side); [Compositions: Constituents](../Storage/Compositions.md#constituents); [Identity: Pure content](../Storage/Identity.md#pure-content); `docs/INVENTION.md` §3; `docs/invention/modality-ladder-law.md`; [Research: Engine Measurements: Ingestion](../Research/Engine.md#ingestion).

### 11.4 Assign tiers

- **In:** the DAG of 11.3.
- **Do:** codepoints are tier 0, graphemes tier 1, words tier 2, and so on; tiers are dynamic across modalities and are compositional altitude within the selected recipe, not a global ontology. The tier of a composition is always at least one more than the tier of its highest constituent, so the DAG is acyclic by construction and needs no cycle hashing. A word can go straight from tier 0 constituents to tier 2. A node can fill a higher tier, but never a lower one: `[H,e,l,l,o]` is always a tier 2 word, "Hello" on its own is never a separate tier 3 sentence, and "Hello!" is a tier 3 sentence. Tier is an observation, never part of an ID, and never a proxy for role, source, or modality.
- **Out:** a tier on every node.
- **From:** [Compositions: Tiers](../Storage/Compositions.md#tiers); `docs/specs/05_Substrate_Invariants.txt` Rule #1b; [Research: Prior Art: Content-addressed code and data](../Research/Prior-Art.md#content-addressed-code-and-data).

### 11.5 Hash every node, leaves up

- **In:** the DAG of 11.3.
- **Do:** a leaf's ID is its codepoint's ID from tier 0. A composition's ID is BLAKE3 over its children's 16-byte IDs, in order, repeats included, truncated to 16 bytes. A composition with one child is that child. The hash input is nothing but content: type, tier, source, parent, position within the source, occurrence ordinal, role label, modality, cache profile, physicality, and provenance are the observation and position of that content and are never salt. `[k,i,n,g]` is one entity wherever that composition occurs, as a word, a name, a label, a title, or a token, and a 2×2 pixel composition is one entity inside every 8×8 region, image, and frame that contains it. Hashes are never faked: if a hash could be made from a made-up string, that string should instead be a decomposed entity with a trunk node; a special record is an entity referenced by trajectory or referential integrity, not a canonical-name hack.
- **Out:** the ID of every node, and the trunk's ID for the whole artifact.
- **From:** [Identity: BLAKE3](../Storage/Identity.md#blake3); [Identity: Pure content](../Storage/Identity.md#pure-content); `docs/specs/05_Substrate_Invariants.txt` Rules #1 and #1d; `docs/INVENTOR_RECORD.md` §Entities; [Research: Hashing: Hash input](../Research/Hashing.md#hash-input); [Research: Hashing: The CVE-2012-2459 lesson](../Research/Hashing.md#the-cve-2012-2459-lesson).

### 11.6 Compute every coordinate, leaves up

- **In:** the DAG of 11.3 and tier 0.
- **Do:** a leaf's coordinate is its codepoint's. A composition's real coordinate is the exact integer average of its children's fixed-point coordinates, `c_j = trunc((Σ m_j) / k)`, truncated toward zero; the sum fits a 128-bit integer for *k* < 2⁷⁴. It falls inward and never outside the wall. Compute its Hilbert value from the coordinate. The coordinate is one property of the object, not a container for it: two different orderings of the same constituents may share a coordinate and remain different entities with different trajectories, and a dense region can hold many distinct structures. Coordinate or Hilbert equality is a locality signal, never identity.
- **Out:** a real 4D coordinate and a Hilbert value on every node.
- **From:** [Physicality: Real coordinates](../Storage/Physicality.md#real-coordinates); [Space: The interior](../Storage/Space.md#the-interior); `docs/INVENTION.md` §2 and §4; [Research: Numerics: The fixed-point grid](../Research/Numerics.md#the-fixed-point-grid); [Research: Prototype: Verification](../Research/Prototype.md#verification).

### 11.7 Build every path

- **In:** the DAG and IDs of 11.5.
- **Do:** every entity's physicality is its path, recorded with geometry ZM: a point, a line, a polygon, a multi-line, and more. Each vertex is the ID of a constituent entity, in order. The 128-bit ID is bit-packed into the mantissa bits of the vertex's X, Y, and Z: 43, 43, and 42 bits, with sign 0 and a fixed exponent that keeps these coordinates between 0.25 and 0.5, inside the 4-ball, where every fraction pattern is a normal, finite, nonzero number. The 28 spare bits are dynamic, not hard-coded to one purpose: the entity's type tells how to parse them, and before that they help with indexing and filtering, holding values from known lists; a small tag says which layout they are in. M carries the vertex's metadata: a fixed-length binary field of bits for flags, values, segmentation, run-length encoding, filtering, indexing, and querying. A run of identical children is one vertex with the run length in M. An atom's physicality is a POINT ZM holding its own ID. The same entity ID is placed into every path that uses it, and each path records one use of it. A path is the bit-perfect Merkle DAG container from trunk to leaf: exact structure, sequence, occurrences, and tiers. Physicalities are typed: a text trajectory, a set, a projection, a structural declaration, a board each carry their own type value, and partial indexes are built per type.
- **Out:** a path per node, and the visualization centroid of each path, recorded so it is never recomputed.
- **From:** [Physicality: Physicality](../Storage/Physicality.md#physicality); [Identity: The ID in geometry](../Storage/Identity.md#the-id-in-geometry); `docs/specs/05_Substrate_Invariants.txt` Rules #2 and #4; `docs/specs/38_Collections_Are_Compositions.md` §4; [Research: Hashing: Packing into IEEE-754 doubles](../Research/Hashing.md#packing-into-ieee-754-doubles); [Research: Geometry: Text output](../Research/Geometry.md#text-output).

### 11.8 Deduplicate in the working set, then trunk to leaf

- **In:** the IDs of 11.5.
- **Do:** first within the working set: repeated identical canonical rows coalesce before crossing any boundary, while distinct interpretations, occurrences, and attributed testimony keep their semantics. Then against the database, an O(tier) check from trunk to leaf: send the trunk IDs; everything the database already holds is eliminated, together with everything under it, because if a trunk node matches, its children match as well; then send the next tier's IDs for the trunks that did not match; and so on down. The check reduces its own total count as it goes. The checks are set-based operations, one query per tier per round, not per-row conflict handling such as `ON CONFLICT` and not one existence query per entity. Pruning on a trunk match is sound because a node is recorded only when everything under it is recorded; recording bottom up, leaves first, in one transaction maintains it. Probing the perf-caches trunk first is the same law in memory. If John 3:16 is already recorded, the check catches the already-ingested parts, overlaps, and adds a witness or an occurrence.
- **Out:** the set of nodes that are new, and for every known node, the occurrence to add.
- **From:** [Ingestion: Deduplication](../Storage/Ingestion.md#deduplication); [Identity: Same content, same hash](../Storage/Identity.md#same-content-same-hash); `docs/plan/INGEST_BOUNDARY_AND_RECIPE_LAW.md` §Source-provider ownership; `docs/plan/ASSIMILATION_ROADMAP.md` workstream C; `docs/INVENTOR_RECORD.md` §O(tier); [Research: Hashing: Sync and deduplication](../Research/Hashing.md#sync-and-deduplication).

### 11.9 Count occurrences and containers

- **In:** the DAG of 11.3.
- **Do:** the number of times a node occurs is the number of paths from document trunks down to it, a sum over its parents' counts, computed in one pass in tier order from the trunk down; a word used twice in one sentence contributes twice. Its containers are its distinct parents. Ingesting a document adds its own counts to every node reachable from its trunk. Content novelty and occurrence volume are different axes: as a corpus matures, structural novelty tapers while occurrence volume keeps growing, and later observations add occurrence, provenance, evidence, and standing without minting the structure again.
- **Out:** each entity's occurrences and distinct containers.
- **From:** [Research: Corpus Search: Occurrence counting](../Research/Corpus-Search.md#occurrence-counting); `docs/INVENTION.md` §3 "Content novelty and observation volume are different"; [Research: Engine Measurements: Ingestion](../Research/Engine.md#ingestion).

### 11.10 Accumulate and stage

- **In:** the new nodes of 11.8, their coordinates of 11.6, their paths of 11.7, and their counts of 11.9, plus every claim the recipe declared.
- **Do:** for a seeded corpus this is extraction, the raw product out of its packaging, a bulk client-side extract folded per strand before the database sees it; "no ETL" in [13. Consensus](Consensus.md) means no delayed folding of standing, not this. Decompose and stage all the records the whole source converts into, deduplicated, and stop there: entities, physicalities, occurrences, references, and the claims of [12. Attestations](Attestations.md), as sorted streams routed to their partitions. Staging is where records collide and self-deduplicate. Reduce claims by attestation identity, merging games and scores and OR-ing qualifier masks; fold each witness's repeats per strand into its one matchup in memory; emit consensus deltas and entity masks beside the rows. Native code does this per source; C# selects artifacts, orders dependencies, and handles commit epochs, progress, and retries, holding no per-row objects; SQL orchestrates at set level only. A native COPY buffer is transport into the shared writer, not delivered knowledge.
- **Out:** the staged, partition-routed streams of one source.
- **From:** `docs/plan/ASSIMILATION_ROADMAP.md` workstream C, target order; `docs/INVENTOR_RECORD.md` §Decomposition; `docs/specs/06_Engineering_Ruleset.txt` Rules #1, #5, #8.

### 11.11 Apply by COPY

- **In:** the streams of 11.10.
- **Do:** stream only new rows, by binary COPY, in a bulk session with `synchronous_commit = off`, in tier order, leaves first: entities, then physicalities, then statistics, then the source with its trunk, origin, format, size, content hash, and normalization form recorded as a filter, then the attestation rows of [12. Attestations](Attestations.md). PostgreSQL stores the rows and resolves key conflicts as set merges; it reads prior standing once per cell per source. Gigabytes should take seconds. If the system is operating properly, the counts of entities and physicalities match.
- **Out:** the source recorded.
- **From:** [Deployment](../Operations/Deployment.md); [Physicality: Entity and physicality](../Storage/Physicality.md#entity-and-physicality); [Research: Engine Measurements: Ingestion](../Research/Engine.md#ingestion); [Research: Engine Measurements: Storage at volume](../Research/Engine.md#storage-at-volume).

### 11.12 Fold and complete

- **In:** the applied rows.
- **Do:** [13. Consensus](Consensus.md) plays the staged matchups as they arrive, set-sized, not per record. Then record completion as operational state, per unit and per layer, never as an attestation. Existing attestation identities are excluded from repeated folding by the shared atomic writer, so a retried job does not multiply the same witnessing: re-ingestion is not another epoch.
- **Out:** the source complete, with its completion state.
- **From:** `docs/plan/ASSIMILATION_ROADMAP.md` commit `eeecf3207`; `docs/INVENTION.md` §11; `docs/specs/34_Conversational_Provenance.md` §Turn contract.

### 11.13 Recompose and compare

- **In:** the trunk ID of 11.5.
- **Do:** walk the trunk's paths down to tier 0 and rebuild the artifact, where the recipe declared reconstruction. Curated sources are mined, not reproduced; user content is reproduced.
- **Out:** proof that the record is lossless, or the declared loss.
- **From:** `docs/INVENTION.md` §17.4; [Research: Prototype: Verification](../Research/Prototype.md#verification); [Research: Engine Measurements: Queries](../Research/Engine.md#queries).

### 11.14 Write the receipt

- **In:** every operation of this source.
- **Do:** report physical files and semantic units separately: artifacts, records, and scalars decoded; entities and trajectories reused against newly admitted; claims and evidence cells derived; native kernel invocations and batch widths; managed, native, SPI, and SQL boundary crossings; CPU, memory, I/O, WAL, and database work; provider, precision, and recipe identity; result fingerprints. Summary output is not verification; each command has an independent acceptance read, and a result is reported after looking at the substrate, the entity census by type and tier, not only claim counts.
- **Out:** the ingest receipt, and a journal that lets the run resume.
- **From:** `docs/OPERATING_SEQUENCE.md` §1; `docs/plan/MODEL_INGESTION_DESIGN.md` §12; `docs/specs/06_Engineering_Ruleset.txt` Rule #9; `docs/plan/ASSIMILATION_ROADMAP.md` workstream J.

## What is observed

Normal digital content, such as what users upload during normal usage, does not give attestations. It gives observations: the physicality trajectory alone gives precedes, contains, co-occurrences, completes-to, and more, so none of those is ever recorded as testimony. The physical trajectory records the order of the constituents, so no ordinal is needed in the metadata. Referencing a trunk node is enough to reach everything under it: from the trunk, the geometry fans out to its constituents and hops along them, down to the atoms. `Captain Ahab` is a precedes with a gap of one, and that gap is searchable. See [Attestations: Observations](../Semantics/Attestations.md#observations), [Physicality: Trajectories](../Storage/Physicality.md#trajectories), [Physicality: Hop and fanout](../Storage/Physicality.md#hop-and-fanout), and `docs/specs/05_Substrate_Invariants.txt` Rule #3.

## What is not the spine

These are architecture smells in repeated ingest work, and each is a defect even when the semantic output is right: one P/Invoke per scalar, token, node, or record; one existence query per entity; per-row SPI prepare and execute; one transaction or COPY per semantic object; a batch API implemented by looping a scalar write; source-private thread pools competing with the common scheduler; source-private caches compensating for a missing working set; per-record consensus calls when a set-sized fold is possible; evidence round-tripping through the database to be refolded from neutral. See `docs/plan/INGEST_BOUNDARY_AND_RECIPE_LAW.md` §Universal execution-grain law and `docs/plan/ASSIMILATION_ROADMAP.md` workstream C.

## What this stage leaves behind

Entities, physicalities, sources, and statistics, and every observation the trajectory carries, with a receipt and a resumable journal, admitted by a plan that provably does not change what exists.

## Without this stage

There is nothing for a witness to attest to, because entities get the attestations.
