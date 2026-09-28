# Identity

Every node's ID is the BLAKE3 hash of its constituents, so the same content always has the same ID.

## BLAKE3

BLAKE3 is simply a unique identifier. It gives enough bits to avoid collisions.

## Pure content

The hash is purely content. Type, source, position within the source, index, and so on are not the content; they are the observation and position of that content, and they are never part of the ID. Hashes are never faked: if a hash could be made from a made-up string, that string should instead be a decomposed entity with a trunk node.

For text, the same codepoint sequence is the same content; the tree matters when it is rendered.

## Same content, same hash

Because IDs are deterministic, ingesting the same Merkle DAG again lands on the same nodes: it is the same content, so it overlaps.

A trunk node's ID stands for the whole tree under it. Referencing the trunk node is enough: the geometry fans out and hops to everything below it. See [Physicality](Physicality.md#hop-and-fanout).

## The ID point

Every entity is its own record, with its ID. The 128-bit BLAKE3 hash is bit-packed into the mantissas of the X, Y, and Z coordinates of a geometry ZM point, and that is how the entity's ID is placed into every [physicality](Physicality.md#physicality) trajectory that uses it. The hash does not need more than three of the four mantissas: a 128-bit hash leaves 28 of the three mantissas' bits spare, to use as needed. M is metadata for the physicality trajectory: a bitmask for filtering, indexing, and querying, such as run-length encoding. Type or tier belong in it only if they genuinely speed up queries.

Bit-packing the mantissas is what makes the database searchable by ID. It also enables a 3D visualization of the 4D representation.

## Client-side computation

The client computes IDs itself. With tier 0 [memory-mapped](Atoms.md#generation), the client deterministically produces the ID and coordinates of any content without a database call.
