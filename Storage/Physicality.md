# Physicality

Every entity has a full, real 4D coordinate, and every composition's content is stored as a trajectory.

## Entity and physicality

Every entity is its own record, with its [ID](Identity.md) and its real coordinate. Every entity also has a physicality, related to it by foreign key, so the physicality needs nothing special for an ID. If the system is operating properly, the counts of entities and physicalities match.

## Physicality

The physicality is the path recorded with geometry ZM, which can be a point, a line, a polygon, a multi-line, and more. Each vertex is the ID of a constituent entity, in order; M carries that vertex's metadata: a fixed-length binary field of bits for flags, values, segmentation, and anything else, such as run-length encoding, filtering, indexing, and querying. An atom's physicality is a POINT ZM holding its own ID.

As built (Laplace-Native, `lp_m_full`), M is an integer a double holds exactly, 53 bits: the low 30 are the run, how many times the vertex repeats; the next 3 say what the vertex is within the path: a claim, a record, a tuple, the metadata of what the path is, a part of a content tree that holds records below it, or who in a record says the claim after it. Above them, a claim's vertex in a record carries how the record said it: the outcome in 2 bits (a win, the default and every vertex that is no claim; a draw; a loss; a score) and its position among the claims said together in 18 bits (0, none). A score other than a win, a draw or a loss is carried in the vertex's spare bits ([Identity](Identity.md)), tag 1, the score times 2^24: exact for every single-precision score at or above one half, within 2^-25 below. None of it is part of any ID; provenance is read from it ([Attestations: Witnesses](../Semantics/Attestations.md#witnesses)).

The same entity ID is placed into every path that uses it. That is what lets `[2,5,5]` be text, a number, an IP segment, and more: the entity never changes, and each path records one use of it.

## Real coordinates

Every composition has a full, real 4D coordinate, recorded on its entity as a normal POINT ZM, with M as the fourth coordinate. Tier 0 coordinates are generated; every other coordinate is computed up from the codepoint leaves.

Compositions have a Hilbert value too. The Hilbert value maps to coordinates deterministically and mathematically, so it can be used for indexing, filtering, and querying; it is part of the deterministic content, derived from the coordinate and never part of an ID.

## Indexes

Laplace exploits GiST and GIN indexing for novel mechanisms. GiST indexes the geometry. GIN indexes each trajectory's constituents, read from the IDs in its geometry, to find every container of any node, such as every sentence that contains a word.

The X, Y, Z, and M doubles of a `physicality.path` vertex have no meaning as spatial positions and are never rendered or passed directly into distance functions: X, Y, and Z pack `43 + 43 + 42 = 128` constituent ID bits plus `28` tagged spare bits in `[0.25, 0.5)`, and M packs `53` integer metadata bits, strictly so PostGIS `geometry` storage, TOAST, and GIN (`laplace_path_ops`) index exact constituent order, runs, roles, and containment without edge tables.

## Partitions

`entity` and `physicality` are range-partitioned by `tier` (`PARTITION BY RANGE (tier)` in `Laplace-postgres/sql/laplace.sql.in`: nine partitions `t0`..`t7` and `t8plus` on both tables, with composite primary keys `(tier, id)` and `(tier, entity)` and per-partition `UNIQUE (id)` / `UNIQUE (entity)` indexes) so upward containment and tier-bounded probes prune lower tiers cleanly; `attestation` and `consensus` are range-partitioned by `claim` into 16 hex-nibble partitions (`attestation_0`..`attestation_f` and `consensus_0`..`consensus_f`, `fillfactor = 80`). See [Reference: Schema](../Reference/Schema.md) and [30. Conflicts](../Sequence/Conflicts.md) P4. Partitions never go by Hilbert value — remember the 4-ball inside the 4-cube: the 64-bit `hilbert` key covers the 4-ball and is used for locality ordering and spatial B-tree pruning (`entity_hilbert`, `entity_tier_hilbert`, `laplace_hilbert_ball_ranges`) within partitions. See [Research: Engine Measurements](../Research/Engine.md#partitions).

## Centroids

One exact real 4D centroid (`entity.coord`, computed via `__int128` fixed-point average of the constituents' real coordinates truncated toward zero) is generated and stored once on `entity`, so it is never recomputed; no centroid is ever computed or stored over packed `physicality.path` carrier doubles. When trajectory shape (`laplace_frechet4d`, `laplace_dtw4d`, `laplace_edr4d`, `laplace_hausdorff4d`) or Glome curves (`laplace_curves`, `laplace_couple`) are evaluated, Laplace unpacks the constituent IDs from `physicality.path` and resolves each constituent's real 4D `entity.coord` (`laplace_project_path`).

Centroids collide in the 4-ball: `[c,a,t]` and `[a,c,t]` have the same centroid. Their Fréchet distances are, mostly, different. The shape being compared is the tree, not the centroid of its text. A close Fréchet distance across trees is a semantic relation the ID does not record. See [Query: Shape](../Query.md#shape).

## Trajectories

Content is stored as physicality trajectories on geometry ZM. The physical trajectory records the order of the constituents, so no ordinal is needed in the metadata.

The trajectory alone gives precedes, contains, co-occurrence, and more.

## Hop and fanout

Referencing a trunk node is enough to reach everything under it. From the trunk, the geometry fans out to its constituents and hops along them, down to the [atoms](Atoms.md).
