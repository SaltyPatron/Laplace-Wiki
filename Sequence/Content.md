# 8. Content

Content is broken to codepoints and built back up into a Merkle DAG on the client, deduplicated trunk to leaf, and recorded as entities and trajectories.

Ingestion computes content's IDs on the client and deduplicates it trunk to leaf against what is already recorded. Everything this stage records is observation: what the content is and how it lies, with no one yet saying anything about it.

## Before this stage

[5. Tier 0](Tier-0.md): the perf-cache the client maps. [6. Database](Database.md): the tables. [7. Recipes](Recipes.md): the recipe for the file's format.

## Operations, per file

### 8.1 Check the bytes

- **In:** the file.
- **Do:** hash the file's bytes with BLAKE3-256 and ask the database, in one query over all the files of the batch, whether that hash is a recorded source. A file whose bytes are already recorded is passed over entirely.
- **Out:** the files that still need decomposing.
- **Check:** ingesting the 195 Gutenberg texts again took 0.1 s: one query found all 195 recorded, and nothing was decomposed.
- **From:** [Deployment](../Operations/Deployment.md), [Research: Engine Measurements: Ingestion](../Research/Engine.md#ingestion).

### 8.2 Decompose on the client

- **In:** the file and its recipe.
- **Do:** the client breaks content down using the memory-mapped tier 0. Text goes through UAX #29 into sentences, words, graphemes, and codepoints; a grapheme of one codepoint is that codepoint. A composition is an n-ary, recursive sequence of constituents, each of which is a codepoint or another composition. Nothing is dropped: "The cat sat on the mat" is `[The, ' ', cat, ' ', sat, ' ', on, ' ', the, ' ', mat]`, and "Sherlock Holmes" is `[[S,h,e,r,l,o,c,k], ' ', [H,o,l,m,e,s]]`. Text is recorded as it arrives, without normalization: precomposed and decomposed forms are different content. Case is never folded: `King` is not `king`, and `Carlsen, Magnus` is not `MagnusCarlsen`. Every core decomposes.
- **Out:** the file's Merkle DAG, in memory on the client.
- **Check:** on the real implementation, decompose, hash, deduplicate, and recompose ran at 8 MB/s on one thread, 195 of 195 files recomposed byte for byte.
- **From:** [Ingestion: Client-side](../Storage/Ingestion.md#client-side), [Compositions: Constituents](../Storage/Compositions.md#constituents), [Identity: Pure content](../Storage/Identity.md#pure-content), [Research: Engine Measurements: Ingestion](../Research/Engine.md#ingestion).

### 8.3 Assign tiers

- **In:** the DAG of 8.2.
- **Do:** codepoints are tier 0, graphemes tier 1, words tier 2, and so on; tiers are dynamic across modalities. The tier of a composition is always at least one more than the tier of its highest constituent, so the DAG is acyclic by construction and needs no cycle hashing. A word can go straight from tier 0 constituents to tier 2. A node can fill a higher tier, but never a lower one: `[H,e,l,l,o]` is always a tier 2 word, "Hello" on its own is never a separate tier 3 sentence, and "Hello!" is a tier 3 sentence. Tier is an observation, never part of an ID.
- **Out:** a tier on every node.
- **From:** [Compositions: Tiers](../Storage/Compositions.md#tiers), [Research: Prior Art: Content-addressed code and data](../Research/Prior-Art.md#content-addressed-code-and-data).

### 8.4 Hash every node, leaves up

- **In:** the DAG of 8.2.
- **Do:** a leaf's ID is its codepoint's ID from tier 0. A composition's ID is BLAKE3 over its children's 16-byte IDs, in order, repeats included, truncated to 16 bytes. A composition with one child is that child. The hash input is nothing but content: type, tier, source, position within the source, index, and so on are the observation and position of that content, and are never part of the ID. Hashes are never faked: if a hash could be made from a made-up string, that string should instead be a decomposed entity with a trunk node.
- **Out:** the ID of every node, and the trunk's ID for the whole file.
- **Check:** every child ID has the same fixed width, so the input parses in exactly one way and the byte length fixes the child count: `[a,a]` is twice as long as `[a]`. Fixed-width child IDs and one-child collapse keep leaf inputs and composition inputs apart. `[2,5,5]` and `[2,5]` are different inputs and different IDs; there is no padding, sorting, or removal of repeats before hashing, which is the CVE-2012-2459 lesson. The hash covers structure: `[ab,c]` and `[a,bc]` both spell "abc" and have different IDs, so equal text deduplicates across documents only because segmentation is a deterministic function of local content.
- **From:** [Identity: BLAKE3](../Storage/Identity.md#blake3), [Identity: Pure content](../Storage/Identity.md#pure-content), [Research: Hashing: Hash input](../Research/Hashing.md#hash-input), [Research: Hashing: The CVE-2012-2459 lesson](../Research/Hashing.md#the-cve-2012-2459-lesson).

### 8.5 Compute every coordinate, leaves up

- **In:** the DAG of 8.2 and tier 0.
- **Do:** a leaf's coordinate is its codepoint's. A composition's real coordinate is the exact integer average of its children's fixed-point coordinates, `c_j = trunc((Σ m_j) / k)`, truncated toward zero; the sum fits a 128-bit integer for *k* < 2⁷⁴. It falls inward and never outside the wall. Compute its Hilbert value from the coordinate.
- **Out:** a real 4D coordinate and a Hilbert value on every node.
- **Check:** for a pure repeat, Σ = *k*·*p* exactly, so `[n,n,…,n]` lands bit for bit on n's point; 280 of 280 pure repeats in the prototype did. Every composition is at least as deep as its constituents' average. The native centroid runs at 211 M points per second per core.
- **From:** [Physicality: Real coordinates](../Storage/Physicality.md#real-coordinates), [Space: The interior](../Storage/Space.md#the-interior), [Research: Numerics: The fixed-point grid](../Research/Numerics.md#the-fixed-point-grid), [Research: Prototype: Verification](../Research/Prototype.md#verification).

### 8.6 Build every path

- **In:** the DAG and IDs of 8.4.
- **Do:** every entity's physicality is its path, recorded with geometry ZM: a point, a line, a polygon, a multi-line, and more. Each vertex is the ID of a constituent entity, in order. The 128-bit ID is bit-packed into the mantissa bits of the vertex's X, Y, and Z: 43, 43, and 42 bits, with sign 0 and a fixed exponent that keeps these coordinates between 0.25 and 0.5, inside the 4-ball, where every fraction pattern is a normal, finite, nonzero number. The 28 spare bits are dynamic, not hard-coded to one purpose: the entity's type tells how to parse them, and before that they help with indexing and filtering, holding values from known lists; a small tag says which layout they are in. M carries the vertex's metadata: a fixed-length binary field of bits for flags, values, segmentation, run-length encoding, filtering, indexing, and querying. A run of identical children is one vertex with the run length in M. An atom's physicality is a POINT ZM holding its own ID. The same entity ID is placed into every path that uses it, and each path records one use of it.
- **Out:** a path per node, and the visualization centroid of each path, recorded so it is never recomputed.
- **Check:** the packed coordinates have no meaning as positions; they are an artist's rendition, and their bits are what record which constituents, in which order. 1,000,008 IDs round-tripped exactly through packing. Arithmetic destroys the payload, so paths move through EWKB and binary COPY, never through WKT at default precision, which changed 93.5% of coordinates. The native pack and unpack runs at 104 M per second per core.
- **From:** [Physicality: Physicality](../Storage/Physicality.md#physicality), [Identity: The ID in geometry](../Storage/Identity.md#the-id-in-geometry), [Physicality: Centroids](../Storage/Physicality.md#centroids), [Research: Hashing: Packing into IEEE-754 doubles](../Research/Hashing.md#packing-into-ieee-754-doubles), [Research: Geometry: Text output](../Research/Geometry.md#text-output).

### 8.7 Deduplicate trunk to leaf

- **In:** the IDs of 8.4.
- **Do:** an O(tier) check from trunk to leaf. Send the trunk IDs; everything the database already holds is eliminated, together with everything under it, because if a trunk node matches, its children match as well; then send the next tier's IDs for the trunks that did not match; and so on down. The check reduces its own total count as it goes. The checks are set-based operations, one query per tier per round, not per-row conflict handling such as `ON CONFLICT`. Pruning on a trunk match is sound because a node is recorded only when everything under it is recorded; recording bottom up, leaves first, in one transaction maintains it.
- **Out:** the set of nodes that are new.
- **Check:** 2,800,910 IDs deduplicated in 8.2 s. Where the bytes differ but the content tree is known, the check stops at the first tier: 195 IDs checked in 11 ms, and nothing sent. If children do not match under a matching trunk, the ingestion was done wrong; 0 of 3,915,022 mismatched in the prototype.
- **From:** [Ingestion: Deduplication](../Storage/Ingestion.md#deduplication), [Identity: Same content, same hash](../Storage/Identity.md#same-content-same-hash), [Research: Hashing: Sync and deduplication](../Research/Hashing.md#sync-and-deduplication), [Research: Engine Measurements: Ingestion](../Research/Engine.md#ingestion).

### 8.8 Count occurrences and containers

- **In:** the DAG of 8.2.
- **Do:** the number of times a node occurs is the number of paths from document trunks down to it, a sum over its parents' counts, computed in one pass in tier order from the trunk down; a word used twice in one sentence contributes twice. Its containers are its distinct parents. Ingesting a document adds its own counts to every node reachable from its trunk.
- **Out:** each entity's occurrences and distinct containers.
- **Check:** 0.7 s for the Gutenberg texts once counting became linear, from 47.5 s before.
- **From:** [Research: Corpus Search: Occurrence counting](../Research/Corpus-Search.md#occurrence-counting), [Research: Engine Measurements: Ingestion](../Research/Engine.md#ingestion).

### 8.9 Record the new rows

- **In:** the new nodes of 8.7, their coordinates of 8.5, their paths of 8.6, and their counts of 8.8.
- **Do:** stream only new rows, by binary COPY, in a bulk session with `synchronous_commit = off`: entities, then physicalities, then statistics, then the source with its trunk, origin, format, size, content hash, and normalization form recorded as a filter. If the system is operating properly, the counts of entities and physicalities match.
- **Out:** the file recorded.
- **Check:** entity COPY at 954,000 rows per second; physicality COPY at 215,000 rows per second, 2.9 GB. 3,915,022 entities and 3,915,022 physicalities in the prototype. At volume, a Tatoeba sentence of 16.6 vertices cost about 1,117 bytes: path 599, entity row 101, and the rest in indexes and statistics.
- **From:** [Deployment](../Operations/Deployment.md), [Physicality: Entity and physicality](../Storage/Physicality.md#entity-and-physicality), [Research: Engine Measurements: Ingestion](../Research/Engine.md#ingestion), [Research: Engine Measurements: Storage at volume](../Research/Engine.md#storage-at-volume).

### 8.10 Recompose and compare

- **In:** the trunk ID of 8.4.
- **Do:** walk the trunk's paths down to tier 0 and rebuild the file.
- **Out:** proof that the record is lossless.
- **Check:** byte for byte, the same hash as the file. All of Alice in Wonderland recomposed from the database in 828 ms.
- **From:** [Research: Prototype: Verification](../Research/Prototype.md#verification), [Research: Engine Measurements: Queries](../Research/Engine.md#queries).

## What is observed

Normal digital content, such as what users upload during normal usage, does not give attestations. It gives observations: the physicality trajectory alone gives precedes, contains, co-occurrences, and more. The physical trajectory records the order of the constituents, so no ordinal is needed in the metadata. Referencing a trunk node is enough to reach everything under it: from the trunk, the geometry fans out to its constituents and hops along them, down to the atoms. See [Attestations: Observations](../Semantics/Attestations.md#observations), [Physicality: Trajectories](../Storage/Physicality.md#trajectories), and [Physicality: Hop and fanout](../Storage/Physicality.md#hop-and-fanout).

## What this stage leaves behind

Entities, physicalities, sources, and statistics, and every observation the trajectory carries.

## Without this stage

There is nothing for a witness to attest to, because entities get the attestations.
