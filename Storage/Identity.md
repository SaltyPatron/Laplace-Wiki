# Identity

Every node's ID is the BLAKE3 hash of its constituents, so the same content always has the same ID.

## BLAKE3

BLAKE3 is simply a unique identifier. It gives enough bits to avoid collisions.

## Same content, same hash

Because IDs are deterministic, ingesting the same Merkle DAG again lands on the same nodes: it is the same content, so it overlaps.

A trunk node's ID stands for the whole tree under it. Referencing the trunk node is enough: the geometry fans out and hops to everything below it. See [Physicality](Physicality.md#hop-and-fanout).

## The ID point

Every node's 128-bit BLAKE3 hash is bit-packed into the mantissas of the X, Y, and Z coordinates of a geometry ZM point. The hash does not need more than three of the four mantissas, which leaves M for metadata.

Bit-packing the mantissas is what makes the database searchable by ID. It also enables a 3D visualization of the 4D representation.

## Client-side computation

The client computes IDs itself. With tier 0 [memory-mapped](Atoms.md#generation), the client deterministically produces the ID and coordinates of any content without a database call.
