# Physicality

Every composition has a full, real 4D coordinate, and its content is stored as a trajectory.

## Entity and physicality

Every entity is its own record, with its [ID](Identity.md) and its real coordinate. Every entity also has a physicality, related to it by foreign key, so the physicality needs nothing special for an ID. If the system is operating properly, the counts of entities and physicalities match.

## Physicality

The physicality is the path recorded with geometry ZM. Each vertex is the ID of a constituent entity, in order; M carries metadata for that vertex, such as run-length encoding.

The same entity ID is placed into every path that uses it. That is what lets `[2,5,5]` be text, a number, an IP segment, and more: the entity never changes, and each path records one use of it.

## Real coordinates

Every composition has a full, real 4D coordinate, recorded on its entity. Tier 0 coordinates are generated; every other coordinate is computed up from the codepoint leaves.

## Indexes

GiST indexes the geometry: real coordinates and ID points. GIN indexes each trajectory's constituents, to find every container of any node, such as every sentence that contains a word.

## Centroids

A centroid is generated and recorded for both the real coordinates and the bit-packed visualization, so it is never recomputed. The real centroid comes from the constituents' real coordinates; the visualization centroid comes from the bit-packed geometry of the path.

Centroids collide in the S³: `[c,a,t]` and `[a,c,t]` have the same centroid. Their Fréchet distances are, mostly, different.

## Trajectories

Content is stored as physicality trajectories on geometry ZM. The physical trajectory records the order of the constituents, so no ordinal is needed in the metadata.

The trajectory alone gives precedes, contains, co-occurrence, and more.

## Hop and fanout

Referencing a trunk node is enough to reach everything under it. From the trunk, the geometry fans out to its constituents and hops along them, down to the [atoms](Atoms.md).
