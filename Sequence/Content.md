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
- **Check:** a benchmark dominated by one 41.6 MB document measured the scheduler's grain, not the composer's ceiling; independent streams measure aggregate headroom.
- **Mechanism:** files walked with `nftw`, hidden and empty skipped; a `.gz` file read through zlib; a source's files under its first existing `root` or by `files`; with nothing named, one process per source in `order` after the room check ([Ingest: Enumerate](../Reference/Ingest.md#1-enumerate)). Archives are not unpacked; no journal is kept beyond the per-source log. In the monorepo: `IngestInventory`, `IngestParallelism`, `IngestTopology`, `PostgresResourcePlan`, `WorkingSetMode`; the journals `ingest_run_journal`, `ingest_file_journal`, `ingest_flush_journal` ([Monorepo: Ingest](../Reference/Monorepo.md#ingest)). Status: **built; monorepo for dispositions and the journal**.
- **From:** `docs/plan/INGEST_BOUNDARY_AND_RECIPE_LAW.md` §Whole working set versus streaming, §Benchmark lesson, §Resource ownership; `docs/specs/06_Engineering_Ruleset.txt` Rules #10 and #12.

### 11.2 Check the bytes

- **In:** each artifact.
- **Do:** hash the artifact's bytes with BLAKE3-256 and ask the database, in one query over all the artifacts of the batch, whether that hash is a recorded source. An artifact whose bytes are already recorded and complete is passed over entirely; the file journal accounts for it as admitted and complete. File timestamps do not define semantic file identity. An edited artifact retains the previous content while admitting the changed structure.
- **Out:** the artifacts that still need decomposing.
- **Check:** ingesting the 195 Gutenberg texts again took 0.1 s: one query found all 195 recorded, and nothing was decomposed.
- **Mechanism:** no byte hash and no source table: a file is passed over when its trunk `[metadata, content]` is recorded, probed first in the load ([Ingest: Trunk to leaf](../Reference/Ingest.md#trunk-to-leaf)); a long file's trunk is probed with `SELECT 1 FROM entity WHERE id = ANY($1::blake3[])` before it is read again ([Ingest: The statements](../Reference/Ingest.md#the-statements)). In the monorepo: `ingest_file_journal.resume_fingerprint`, BLAKE3 of the raw bytes; `ingest_unit_completion` and `ingest_layer_completion` ([Monorepo: Ingest](../Reference/Monorepo.md#ingest)). Status: **built, by trunk; monorepo by byte fingerprint**.
- **From:** [Deployment](../Operations/Deployment.md); `seeds/operational/README.md`; [Research: Engine Measurements: Ingestion](../Research/Engine.md#ingestion).

### 11.3 Decompose on the client

- **In:** the artifact and its recipe.
- **Do:** the client breaks content down using the memory-mapped tier 0 and the ROMs of [7. Perfcaches](Perfcaches.md), in native code over a working set or batch, never one call per scalar, token, node, or record. Text goes through UAX #29 into sentences, words, graphemes, and codepoints; a grapheme of one codepoint is that codepoint. A composition is an n-ary, recursive sequence of constituents, each of which is a codepoint or another composition. Nothing is dropped: "The cat sat on the mat" is `[The, ' ', cat, ' ', sat, ' ', on, ' ', the, ' ', mat]`, and "Sherlock Holmes" is `[[S,h,e,r,l,o,c,k], ' ', [H,o,l,m,e,s]]`. Text is recorded as it arrives, without normalization: precomposed and decomposed forms are different content. Case is never folded: `King` is not `king`, and attestations link them. A number decomposes to its digit codepoints under the scalar recipe and composes to one reusable root; a pixel's channels reference number roots; a sample references a scalar root; a code file's syntax subtrees compose bottom-up with the gaps as text constituents; an image composes pixels into patches, regions, and the image, with every contiguous square substructure an occurrence of a global root; a checkpoint's tokenizer composes as one ordered vocabulary. Every core decomposes.
- **Out:** the artifact's Merkle DAG, in memory on the client, under a source trunk, a file trunk, a metadata tree, and a content tree.
- **Check:** on the real implementation, decompose, hash, deduplicate, and recompose ran at 8 MB/s on one thread, 195 of 195 files recomposed byte for byte.
- **Mechanism:** one OpenMP task per file into the 256-shard node table, one `lp_text` per thread ([Ingest: Batch and decompose](../Reference/Ingest.md#3-batch-and-decompose), [Formats: The engine's node table](../Reference/Formats.md#the-engines-node-table)); `lp_text_decompose` for text, the parsers and `attest_*` for the rest. In the monorepo: `text_decomposer.c` into the native `IntentStage`, `content_witness_batch`. Status: **built for text, code, tables, XML, JSON, vocabularies; images, audio, video, checkpoints specified**.
- **From:** [Ingestion: Client-side](../Storage/Ingestion.md#client-side); [Compositions: Constituents](../Storage/Compositions.md#constituents); [Identity: Pure content](../Storage/Identity.md#pure-content); `docs/INVENTION.md` §3; `docs/invention/modality-ladder-law.md`; [Research: Engine Measurements: Ingestion](../Research/Engine.md#ingestion).

### 11.4 Assign tiers

- **In:** the DAG of 11.3.
- **Do:** codepoints are tier 0, graphemes tier 1, words tier 2, and so on; tiers are dynamic across modalities and are compositional altitude within the selected recipe, not a global ontology. The tier of a composition is always at least one more than the tier of its highest constituent, so the DAG is acyclic by construction and needs no cycle hashing. A word can go straight from tier 0 constituents to tier 2. A node can fill a higher tier, but never a lower one: `[H,e,l,l,o]` is always a tier 2 word, "Hello" on its own is never a separate tier 3 sentence, and "Hello!" is a tier 3 sentence. Tier is an observation, never part of an ID, and never a proxy for role, source, or modality.
- **Out:** a tier on every node.
- **Mechanism:** `lp_ref_compose(children, n, tier)`, the caller passing one above the highest child ([Native: Composition](../Reference/Native.md#composition-composec)); `tier` in every row ([Schema: Content](../Reference/Schema.md#content-schemasql)). In the monorepo: `tier_tree.c`; `entities.tier` 0 to 255; `hash128_merkle` discards its `tier` argument. Status: **built**.
- **From:** [Compositions: Tiers](../Storage/Compositions.md#tiers); `docs/specs/05_Substrate_Invariants.txt` Rule #1b; [Research: Prior Art: Content-addressed code and data](../Research/Prior-Art.md#content-addressed-code-and-data).

### 11.5 Hash every node, leaves up

- **In:** the DAG of 11.3.
- **Do:** a leaf's ID is its codepoint's ID from tier 0. A composition's ID is BLAKE3 over its children's 16-byte IDs, in order, repeats included, truncated to 16 bytes. A composition with one child is that child. The hash input is nothing but content: type, tier, source, parent, position within the source, occurrence ordinal, role label, modality, cache profile, physicality, and provenance are the observation and position of that content and are never salt. `[k,i,n,g]` is one entity wherever that composition occurs, as a word, a name, a label, a title, or a token, and a 2×2 pixel composition is one entity inside every 8×8 region, image, and frame that contains it. Hashes are never faked: if a hash could be made from a made-up string, that string should instead be a decomposed entity with a trunk node; a special record is an entity referenced by trajectory or referential integrity, not a canonical-name hack.
- **Out:** the ID of every node, and the trunk's ID for the whole artifact.
- **Check:** every child ID has the same fixed width, so the input parses in exactly one way and the byte length fixes the child count: `[a,a]` is twice as long as `[a]`. Fixed-width child IDs and one-child collapse keep leaf inputs and composition inputs apart. `[2,5,5]` and `[2,5]` are different inputs and different IDs; there is no padding, sorting, or removal of repeats before hashing, which is the CVE-2012-2459 lesson. The hash covers structure: `[ab,c]` and `[a,bc]` both spell "abc" and have different IDs, so equal text deduplicates across documents only because segmentation is a deterministic function of local content. Normal convergence of equal content is content-address convergence; a true cryptographic collision is a distinct event that is detected, never the word for two sources admitting the same content.
- **Mechanism:** `lp_id_compose` over the children's contiguous 16-byte IDs, one child collapsing ([Native: Identity](../Reference/Native.md#identity-identityc-utf8c), [Formats: The ID](../Reference/Formats.md#the-id)). In the monorepo: `hash128_merkle`: BLAKE3 over a domain byte `0x01` and the child ids, so the same composition has a different ID than in the split repositories ([Monorepo: Identity and placement](../Reference/Monorepo.md#identity-placement-and-the-carrier)). Status: **built**.
- **From:** [Identity: BLAKE3](../Storage/Identity.md#blake3); [Identity: Pure content](../Storage/Identity.md#pure-content); `docs/specs/05_Substrate_Invariants.txt` Rules #1 and #1d; `docs/INVENTOR_RECORD.md` §Entities; [Research: Hashing: Hash input](../Research/Hashing.md#hash-input); [Research: Hashing: The CVE-2012-2459 lesson](../Research/Hashing.md#the-cve-2012-2459-lesson).

### 11.6 Compute every coordinate, leaves up

- **In:** the DAG of 11.3 and tier 0.
- **Do:** a leaf's coordinate is its codepoint's. A composition's real coordinate is the exact integer average of its children's fixed-point coordinates, `c_j = trunc((Σ m_j) / k)`, truncated toward zero; the sum fits a 128-bit integer for *k* < 2⁷⁴. It falls inward and never outside the wall. Compute its Hilbert value from the coordinate. The coordinate is one property of the object, not a container for it: two different orderings of the same constituents may share a coordinate and remain different entities with different trajectories, and a dense region can hold many distinct structures. Coordinate or Hilbert equality is a locality signal, never identity.
- **Out:** a real 4D coordinate and a Hilbert value on every node.
- **Check:** for a pure repeat, Σ = *k*·*p* exactly, so `[n,n,…,n]` lands bit for bit on n's point; 280 of 280 pure repeats in the prototype did. Every composition is at least as deep as its constituents' average. The native centroid runs at 211 M points per second per core. The monorepo's managed model and chess paths place by Karcher mean instead; that divergence is recorded in [30. Conflicts](Conflicts.md).
- **Mechanism:** `lp_ref_compose` averages with `lp_coord_centroid` in 128-bit, truncated toward zero; `lp_hilbert4` ([Native: Coordinates](../Reference/Native.md#coordinates-coordc)). In the monorepo: `math4d_centroid` in doubles; the managed chess and model paths use `math4d_karcher_mean`, [Conflicts P3](Conflicts.md); `hilbert4d_encode` 128-bit. Status: **built**.
- **From:** [Physicality: Real coordinates](../Storage/Physicality.md#real-coordinates); [Space: The interior](../Storage/Space.md#the-interior); `docs/INVENTION.md` §2 and §4; [Research: Numerics: The fixed-point grid](../Research/Numerics.md#the-fixed-point-grid); [Research: Prototype: Verification](../Research/Prototype.md#verification).

### 11.7 Build every path

- **In:** the DAG and IDs of 11.5.
- **Do:** every entity's physicality is its path, recorded with geometry ZM: a point, a line, a polygon, a multi-line, and more. Each vertex is the ID of a constituent entity, in order. The 128-bit ID is bit-packed into the mantissa bits of the vertex's X, Y, and Z: 43, 43, and 42 bits, with sign 0 and a fixed exponent that keeps these coordinates between 0.25 and 0.5, inside the 4-ball, where every fraction pattern is a normal, finite, nonzero number. The 28 spare bits are dynamic, not hard-coded to one purpose: the entity's type tells how to parse them, and before that they help with indexing and filtering, holding values from known lists; a small tag says which layout they are in. M carries the vertex's metadata: a fixed-length binary field of bits for flags, values, segmentation, run-length encoding, filtering, indexing, and querying. A run of identical children is one vertex with the run length in M. An atom's physicality is a POINT ZM holding its own ID. The same entity ID is placed into every path that uses it, and each path records one use of it. A path is the bit-perfect Merkle DAG container from trunk to leaf: exact structure, sequence, occurrences, and tiers. Physicalities are typed: a text trajectory, a set, a projection, a structural declaration, a board each carry their own type value, and partial indexes are built per type.
- **Out:** a path per node, and the visualization centroid of each path, recorded so it is never recomputed.
- **Check:** the packed coordinates have no meaning as positions; they are an artist's rendition, and their bits are what record which constituents, in which order. 1,000,008 IDs round-tripped exactly through packing. Arithmetic destroys the payload, so paths move through EWKB and binary COPY, never through WKT at default precision, which changed 93.5% of coordinates. The native pack and unpack runs at 104 M per second per core. The monorepo's carrier packs 212 bits per vertex as 128 id, 16 ordinal, 16 run, 52 flags; that difference from 43/43/42 is recorded in [30. Conflicts](Conflicts.md).
- **Mechanism:** `lp_id_to_xyz`, 43 + 43 + 42 bits at exponent −2; M = run | said; `lp_ewkb_runs` ([Formats: The packed path vertex](../Reference/Formats.md#the-packed-path-vertex), [Formats: EWKB](../Reference/Formats.md#ewkb)). The 28 spare mantissa bits are unused and no layout tag exists; no visualization centroid is stored. In the monorepo: the 212-bit carrier: 128-bit id, 16-bit ordinal, 16-bit run, 52 flag bits, with vertex classes content, atom, testimony, factor, and parse, [Conflicts P2](Conflicts.md) ([Monorepo: Identity and placement](../Reference/Monorepo.md#identity-placement-and-the-carrier)). Status: **built**.
- **From:** [Physicality: Physicality](../Storage/Physicality.md#physicality); [Identity: The ID in geometry](../Storage/Identity.md#the-id-in-geometry); `docs/specs/05_Substrate_Invariants.txt` Rules #2 and #4; `docs/specs/38_Collections_Are_Compositions.md` §4; [Research: Hashing: Packing into IEEE-754 doubles](../Research/Hashing.md#packing-into-ieee-754-doubles); [Research: Geometry: Text output](../Research/Geometry.md#text-output).

### 11.8 Deduplicate in the working set, then trunk to leaf

- **In:** the IDs of 11.5.
- **Do:** first within the working set: repeated identical canonical rows coalesce before crossing any boundary, while distinct interpretations, occurrences, and attributed testimony keep their semantics. Then against the database, an O(tier) check from trunk to leaf: send the trunk IDs; everything the database already holds is eliminated, together with everything under it, because if a trunk node matches, its children match as well; then send the next tier's IDs for the trunks that did not match; and so on down. The check reduces its own total count as it goes. The checks are set-based operations, one query per tier per round, not per-row conflict handling such as `ON CONFLICT` and not one existence query per entity. Pruning on a trunk match is sound because a node is recorded only when everything under it is recorded; recording bottom up, leaves first, in one transaction maintains it. Probing the perf-caches trunk first is the same law in memory. If John 3:16 is already recorded, the check catches the already-ingested parts, overlaps, and adds a witness or an occurrence.
- **Out:** the set of nodes that are new, and for every known node, the occurrence to add.
- **Check:** 2,800,910 IDs deduplicated in 8.2 s. Where the bytes differ but the content tree is known, the check stops at the first tier: 195 IDs checked in 11 ms, and nothing sent. If children do not match under a matching trunk, the ingestion was done wrong; 0 of 3,915,022 mismatched in the prototype. The OMW seed that probed existence row by row made 434 round trips at about 8.4k rows per second against about 300k rows per second for a local materialization.
- **Mechanism:** within the batch, the node table finds or adds every composition once (`hits`); against the database, `recorded()` per round, one `EXISTS` chain per hex digit over the partitions that hold anything, 50,000 IDs per chunk on every connection, `keep` 1 or 2 ([Ingest: Trunk to leaf](../Reference/Ingest.md#trunk-to-leaf), [Formats: The engine's node table](../Reference/Formats.md#the-engines-node-table)). In the monorepo: `IngestExistenceGate`, the probes `entities_exist_bitmap`, `content_descent_bitmap`, `tier_batch_existence_probe`, and `merkle_dedup` ([Monorepo: Ingest](../Reference/Monorepo.md#ingest)). Status: **built**.
- **From:** [Ingestion: Deduplication](../Storage/Ingestion.md#deduplication); [Identity: Same content, same hash](../Storage/Identity.md#same-content-same-hash); `docs/plan/INGEST_BOUNDARY_AND_RECIPE_LAW.md` §Source-provider ownership; `docs/plan/ASSIMILATION_ROADMAP.md` workstream C; `docs/INVENTOR_RECORD.md` §O(tier); [Research: Hashing: Sync and deduplication](../Research/Hashing.md#sync-and-deduplication).

### 11.9 Count occurrences and containers

- **In:** the DAG of 11.3.
- **Do:** the number of times a node occurs is the number of paths from document trunks down to it, a sum over its parents' counts, computed in one pass in tier order from the trunk down; a word used twice in one sentence contributes twice. Its containers are its distinct parents. Ingesting a document adds its own counts to every node reachable from its trunk. Content novelty and occurrence volume are different axes: as a corpus matures, structural novelty tapers while occurrence volume keeps growing, and later observations add occurrence, provenance, evidence, and standing without minting the structure again.
- **Out:** each entity's occurrences and distinct containers.
- **Check:** 0.7 s for the Gutenberg texts once counting became linear, from 47.5 s before.
- **Mechanism:** not stored: `laplace fills` computes occurrences at read time, leaf to trunk and back, from the paths ([Reads: laplace fills](../Reference/Reads.md#laplace-fills)). The prototype's `entity_stats` table is not in the built schema ([Schema: What the prototype had](../Reference/Schema.md#what-the-prototype-had)). In the monorepo: `n_constituents` per physicality, `observation_count` per attestation, `ops.entity_evidence_count`; no occurrence count per entity either. Status: **built at read time; stored counts prototype**.
- **From:** [Research: Corpus Search: Occurrence counting](../Research/Corpus-Search.md#occurrence-counting); `docs/INVENTION.md` §3 "Content novelty and observation volume are different"; [Research: Engine Measurements: Ingestion](../Research/Engine.md#ingestion).

### 11.10 Accumulate and stage

- **In:** the new nodes of 11.8, their coordinates of 11.6, their paths of 11.7, and their counts of 11.9, plus every claim the recipe declared.
- **Do:** decompose and stage all the records the whole source converts into, deduplicated, and stop there: entities, physicalities, occurrences, references, and the claims of [12. Attestations](Attestations.md), as sorted streams routed to their partitions. Staging is where records collide and self-deduplicate. Reduce claims by attestation identity, merging games and scores and OR-ing qualifier masks; fold each witness's rating period per cell in memory; emit consensus deltas and entity masks beside the rows. Native code does this per source; C# selects artifacts, orders dependencies, and handles commit epochs, progress, and retries, holding no per-row objects; SQL orchestrates at set level only. A native COPY buffer is transport into the shared writer, not delivered knowledge.
- **Out:** the staged, partition-routed streams of one source.
- **Mechanism:** the node table is the stage: new nodes bucketed by `part_of(id, tier)`; the standings map in memory holds every claim of the batch with its entry standing ([Ingest: COPY](../Reference/Ingest.md#copy), [Ingest: Semantics](../Reference/Ingest.md#semantics)). In the monorepo: `staged_load.cpp`: claims merged by attestation id, games and scores summed, qualifiers OR-ed; `IngestDescentFlush`; `partition_route` ([Monorepo: Ingest](../Reference/Monorepo.md#ingest)). Status: **built**.
- **From:** `docs/plan/ASSIMILATION_ROADMAP.md` workstream C, target order; `docs/INVENTOR_RECORD.md` §Decomposition; `docs/specs/06_Engineering_Ruleset.txt` Rules #1, #5, #8.

### 11.11 Apply by COPY

- **In:** the streams of 11.10.
- **Do:** stream only new rows, by binary COPY, in a bulk session with `synchronous_commit = off`, in tier order, leaves first: entities, then physicalities, then statistics, then the source with its trunk, origin, format, size, content hash, and normalization form recorded as a filter, then the attestation rows of [12. Attestations](Attestations.md). PostgreSQL stores the rows and resolves key conflicts as set merges; it reads prior standing once per cell per source. Gigabytes should take seconds. If the system is operating properly, the counts of entities and physicalities match.
- **Out:** the source recorded.
- **Check:** entity COPY at 954,000 rows per second; physicality COPY at 215,000 rows per second, 2.9 GB. 3,915,022 entities and 3,915,022 physicalities in the prototype. At volume, a Tatoeba sentence of 16.6 vertices cost about 1,117 bytes: path 599, entity row 101, and the rest in indexes and statistics.
- **Mechanism:** `COPY entity_t… FROM STDIN (FORMAT binary)` then `COPY physicality_t…`, one connection per leaf partition, a tier at a time from the lowest, `synchronous_commit = off` ([Ingest: COPY](../Reference/Ingest.md#copy), [Formats: Binary wire formats](../Reference/Formats.md#binary-wire-formats)). No statistics rows, no source row; the file trunks are written last of all. In the monorepo: binary COPY streams produced by `laplace_staged_claims` and `laplace_staged_score`; `ingest.physicalities_merge`; `apply_write_epoch`. Status: **built**.
- **From:** [Deployment](../Operations/Deployment.md); [Physicality: Entity and physicality](../Storage/Physicality.md#entity-and-physicality); [Research: Engine Measurements: Ingestion](../Research/Engine.md#ingestion); [Research: Engine Measurements: Storage at volume](../Research/Engine.md#storage-at-volume).

### 11.12 Fold and complete

- **In:** the applied rows.
- **Do:** [13. Consensus](Consensus.md) plays the staged matchups as they arrive, set-sized, not per record. Then record completion as operational state, per unit and per layer, never as an attestation. Existing attestation identities are excluded from repeated folding by the shared atomic writer, so a retried job does not multiply the same witnessing: re-ingestion is not another epoch.
- **Out:** the source complete, with its completion state.
- **Mechanism:** the standings played in memory and written in the one semantics transaction, the file trunks last, so a recorded trunk is the completion mark ([Ingest: Semantics](../Reference/Ingest.md#semantics)). No separate completion state or epoch exists. In the monorepo: `ingest_unit_completion`, `ingest_layer_completion`, `ingest_flush_journal.receipt_kind`, `ops.ingest_run_close` ([Monorepo: Ingest](../Reference/Monorepo.md#ingest)). Status: **built; monorepo for completion state**.
- **From:** `docs/plan/ASSIMILATION_ROADMAP.md` commit `eeecf3207`; `docs/INVENTION.md` §11; `docs/specs/34_Conversational_Provenance.md` §Turn contract.

### 11.13 Recompose and compare

- **In:** the trunk ID of 11.5.
- **Do:** walk the trunk's paths down to tier 0 and rebuild the artifact, where the recipe declared reconstruction. Curated sources are mined, not reproduced; user content is reproduced.
- **Out:** proof that the record is lossless, or the declared loss.
- **Check:** byte for byte, the same hash as the file. All of Alice in Wonderland recomposed from the database in 828 ms.
- **Mechanism:** `expand` rebuilds every non-curated file from the node table and tier 0 and compares ([Ingest: Recompose and compare](../Reference/Ingest.md#4-recompose-and-compare)); `laplace_text(blake3)` recomposes from the database ([SQL: Paths](../Reference/SQL.md#paths)). In the monorepo: `ContentRoundtrip.cs`, `/v1/explore/storage-proof`, `prove-live-recursive-substrate.py`. Status: **built**.
- **From:** `docs/INVENTION.md` §17.4; [Research: Prototype: Verification](../Research/Prototype.md#verification); [Research: Engine Measurements: Queries](../Research/Engine.md#queries).

### 11.14 Write the receipt

- **In:** every operation of this source.
- **Do:** report physical files and semantic units separately: artifacts, records, and scalars decoded; entities and trajectories reused against newly admitted; claims and evidence cells derived; native kernel invocations and batch widths; managed, native, SPI, and SQL boundary crossings; CPU, memory, I/O, WAL, and database work; provider, precision, and recipe identity; result fingerprints. Summary output is not verification; each command has an independent acceptance read, and a result is reported after looking at the substrate, the entity census by type and tier, not only claim counts.
- **Out:** the ingest receipt, and a journal that lets the run resume.
- **Mechanism:** the summary on stdout and the per-source log under `$LAPLACE_WORK/logs/ingest/` ([Ingest: After the load](../Reference/Ingest.md#after-the-load)); a cut-off run is taken up by running again ([Build: deploy.sh](../Reference/Build.md#deploysh)). In the monorepo: `ingest_run_journal` with units, entities, physicalities, attestations, fold and writer times, throughput against baseline; `ops.ingest_runs`, `ops.ingest_files`; resume by `resume_fingerprint` ([Monorepo: Ingest](../Reference/Monorepo.md#ingest)). Status: **built in part; monorepo for the receipt and the journal**.
- **From:** `docs/OPERATING_SEQUENCE.md` §1; `docs/plan/MODEL_INGESTION_DESIGN.md` §12; `docs/specs/06_Engineering_Ruleset.txt` Rule #9; `docs/plan/ASSIMILATION_ROADMAP.md` workstream J.

## What is observed

Normal digital content, such as what users upload during normal usage, does not give attestations. It gives observations: the physicality trajectory alone gives precedes, contains, co-occurrences, completes-to, and more, so none of those is ever recorded as testimony. The physical trajectory records the order of the constituents, so no ordinal is needed in the metadata. Referencing a trunk node is enough to reach everything under it: from the trunk, the geometry fans out to its constituents and hops along them, down to the atoms. `Captain Ahab` is a precedes with a gap of one, and that gap is searchable. See [Attestations: Observations](../Semantics/Attestations.md#observations), [Physicality: Trajectories](../Storage/Physicality.md#trajectories), [Physicality: Hop and fanout](../Storage/Physicality.md#hop-and-fanout), and `docs/specs/05_Substrate_Invariants.txt` Rule #3.

## What is not the spine

These are architecture smells in repeated ingest work, and each is a defect even when the semantic output is right: one P/Invoke per scalar, token, node, or record; one existence query per entity; per-row SPI prepare and execute; one transaction or COPY per semantic object; a batch API implemented by looping a scalar write; source-private thread pools competing with the common scheduler; source-private caches compensating for a missing working set; per-record consensus calls when a set-sized fold is possible; evidence round-tripping through the database to be refolded from neutral. See `docs/plan/INGEST_BOUNDARY_AND_RECIPE_LAW.md` §Universal execution-grain law and `docs/plan/ASSIMILATION_ROADMAP.md` workstream C.

## What this stage leaves behind

Entities, physicalities, sources, and statistics, and every observation the trajectory carries, with a receipt and a resumable journal, admitted by a plan that provably does not change what exists.

## Without this stage

There is nothing for a witness to attest to, because entities get the attestations.
