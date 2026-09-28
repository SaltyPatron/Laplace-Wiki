# Physicality

Every entity has a full, real 4D coordinate, and every composition's content is stored as a trajectory.

## Entity and physicality

Every entity is its own record, with its [ID](Identity.md) and its real coordinate. Every entity also has a physicality, related to it by foreign key, so the physicality needs nothing special for an ID. If the system is operating properly, the counts of entities and physicalities match.

## Physicality

The physicality is the path recorded with geometry ZM, which can be a point, a line, a polygon, a multi-line, and more. Each vertex is the ID of a constituent entity, in order; M carries that vertex's metadata: a fixed-length binary field of bits for flags, values, segmentation, and anything else, such as run-length encoding, filtering, indexing, and querying. An atom's physicality is a POINT ZM holding its own ID.

The same entity ID is placed into every path that uses it. That is what lets `[2,5,5]` be text, a number, an IP segment, and more: the entity never changes, and each path records one use of it.

## Real coordinates

Every composition has a full, real 4D coordinate, recorded on its entity as a normal POINT ZM, with M as the fourth coordinate. Tier 0 coordinates are generated; every other coordinate is computed up from the codepoint leaves.

Compositions have a Hilbert value too. The Hilbert value maps to coordinates deterministically and mathematically, so it can be used for indexing, filtering, and querying; it is part of the deterministic content, derived from the coordinate and never part of an ID.

## Indexes

Laplace exploits GiST and GIN indexing for novel mechanisms. GiST indexes the geometry. GIN indexes each trajectory's constituents, read from the IDs in its geometry, to find every container of any node, such as every sentence that contains a word.

The coordinates of the bit-packed IDs in a physicality have no meaning as positions; they are an artist's rendition, a visualization of the 4D representation. Their bits are what record which constituents, in which order.

## Partitions

Partitions go by the ID hash, not by Hilbert value: remember the 4-ball against the 4-box. See [Research: Engine Measurements](../Research/Engine.md#partitions).

## Centroids

A centroid is generated and recorded for both the real coordinates and the bit-packed visualization, so it is never recomputed. The real centroid comes from the constituents' real coordinates; the visualization centroid comes from the bit-packed geometry of the path.

Centroids collide in the 4-ball: `[c,a,t]` and `[a,c,t]` have the same centroid. Their Fréchet distances are, mostly, different.

## Trajectories

Content is stored as physicality trajectories on geometry ZM. The physical trajectory records the order of the constituents, so no ordinal is needed in the metadata.

The trajectory alone gives precedes, contains, co-occurrence, and more.

## Hop and fanout

Referencing a trunk node is enough to reach everything under it. From the trunk, the geometry fans out to its constituents and hops along them, down to the [atoms](Atoms.md).
