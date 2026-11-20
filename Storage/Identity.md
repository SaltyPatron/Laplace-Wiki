# Identity

Every node's ID is the BLAKE3 hash of its constituents, so the same content always has the same ID.

## BLAKE3

BLAKE3 is simply a unique identifier. It gives enough bits to avoid collisions. See [Research: Hashing](../Research/Hashing.md).

A codepoint's ID is the BLAKE3 hash of its UTF-8 bytes. UTF-8 handles every Unicode scalar value; surrogates are a UTF-16 mechanism and never appear alone in valid text, so they take UTF-8's generalized 3-byte form, which no valid character uses.

## Pure content

The hash is purely content. Type, tier, source, position within the source, index, and so on are not the content; they are the observation and position of that content, and they are never part of the ID. Hashes are never faked: if a hash could be made from a made-up string, that string should instead be a decomposed entity with a trunk node.

A composition's ID is BLAKE3 over its children's 16-byte IDs, in order, repeats included, truncated to 16 bytes, and nothing else: no domain byte, tier, type, recipe name, version, source, position, index, or role label. A composition with one child is that child. None of these is needed to keep a node from colliding with a leaf: a leaf hashes the 1 to 4 bytes of one codepoint's UTF-8, and a node at least 32. A recipe decides how content decomposes into a tree, so the same bytes under a different decomposition can give a different trunk, but a recipe never salts a hash: the same content has the same ID.

For text, the same codepoint sequence is the same content; the tree matters when it is rendered.

Text is recorded byte-for-byte as it arrives, without Unicode normalization: precomposed (`é`, one codepoint) and decomposed (`e` + U+0301, two codepoints) forms are different content with different IDs, and there is no normalization-form filter column. Case is never folded: `King` is not `king`, and `Carlsen, Magnus` is not `MagnusCarlsen` (case and lexical variants link through `tier0.flags` and attested claims, never by mutating IDs).

## Same content, same hash

Because IDs are deterministic, ingesting the same Merkle DAG again lands on the same nodes: it is the same content, so it overlaps.

A trunk node's ID stands for the whole tree under it. Referencing the trunk node is enough: the geometry fans out and hops to everything below it. See [Physicality](Physicality.md#hop-and-fanout).

## The ID in geometry

Every entity is its own record, and its ID is that record's key. The only other place the ID is written is inside geometry: the 128-bit BLAKE3 hash is bit-packed into the mantissa bits of the X, Y, and Z coordinates of a geometry ZM point, and that is how the entity's ID is placed into every [physicality](Physicality.md#physicality) that uses it. Nothing else is derived from it or hashed from it.

The hash does not need more than three of the four mantissas: across the IEEE-754 `binary64` X, Y, and Z components at fixed biased exponent 1021 (values in `[0.25, 0.5)`), the low `43 + 43 + 42 = 128` mantissa bits hold the constituent's 16-byte `lp_id`, leaving the upper `9 + 9 + 10 = 28` bits spare (`4-bit tag + 24-bit payload`, such as `LP_SPARE_SCORE`). `M` is an exact 53-bit integer-valued double carrying per-vertex metadata (`run` bits `0..29`, `said` role bits `30..32`, `outcome` bits `33..34`, and `position` bits `35..52`), while enumerated grammatical and row-role banks live in the table's 64-bit `mask` (`manifest/banks.tsv`).

Bit-packing IDs and vertex metadata into binary EWKB `POINT ZM` / `LINESTRING ZM` mantissas in `[0.25, 0.5)` exists strictly to exploit PostgreSQL and PostGIS storage, TOAST compression, and GIN/GiST indexing (`laplace_path_ops`) without edge tables. Carrier doubles are never spatial coordinates and are never plotted directly: Glome rendering and 4D shape metrics (`laplace_curves`, `laplace_frechet4d`, `laplace_dtw4d`, `laplace_edr4d`) always unpack the constituent IDs and resolve their real 4D `entity.coord` positions.

## Client-side computation

The client computes IDs itself. With tier 0 [memory-mapped](Atoms.md#generation), the client deterministically produces the ID and coordinates of any content without a database call.
