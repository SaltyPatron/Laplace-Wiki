# Physicality

Every composition has a full, real 4D coordinate, and its content is stored as a trajectory.

## Real coordinates

Separately from its [ID point](Identity.md#the-id-point), every composition has a full, real 4D coordinate: the centroid of its geometry ZM.

## Indexes

GiST indexes the geometry: real coordinates and ID points. GIN indexes each trajectory's constituents, to find every container of any node, such as every sentence that contains a word.

## Centroids

A centroid is generated and recorded for both the real coordinates and the bit-packed visualization, so it is never recomputed.

Centroids collide in the S³: `[c,a,t]` and `[a,c,t]` have the same centroid. Their Fréchet distances are, mostly, different.

## Trajectories

Content is stored as trajectories on geometry ZM. The physical trajectory records the order of the constituents, so no ordinal is needed in the metadata.

The trajectory alone gives precedes, contains, co-occurrence, and more.

## Hop and fanout

Referencing a trunk node is enough to reach everything under it. From the trunk, the geometry fans out to its constituents and hops along them, down to the [atoms](Atoms.md).
