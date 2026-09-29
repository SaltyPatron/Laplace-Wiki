# 5. Tier 0

Every codepoint's ID, fixed-point coordinate, Hilbert value, and flags are written once into a fingerprinted file that the client and the database map.

Codepoints are tier 0, the absolute floor: every Unicode codepoint has a deterministic ID and a deterministic coordinate on the S³.

## Before this stage

[4. Projection](Projection.md): the point and the rank of every codepoint. [1. Unicode](Unicode.md): the flags. [3. Builds](Builds.md): the generator.

## Operations

### 5.1 Hash every codepoint

- **In:** each codepoint.
- **Do:** encode the codepoint as UTF-8. UTF-8 handles every Unicode scalar value; surrogates are a UTF-16 mechanism and never appear alone in valid text, so they take UTF-8's generalized 3-byte form, which no valid character uses. Hash the bytes with BLAKE3 and keep the first 16 bytes. BLAKE3 is an extendable-output function and shorter outputs are prefixes of longer ones, so the 128-bit ID is exactly the first 16 bytes of the standard 256-bit hash: `digest(16) == digest(32)[:16]`.
- **Out:** the 128-bit ID of every codepoint.
- **Check:** every one of the 1,114,112 IDs is unique. At 128 bits, generic collision work is about 2⁶⁴ hash evaluations, preimage and second preimage about 2¹²⁸, and the probability of any accidental collision among 10¹⁵ nodes is 1.47 × 10⁻⁹. The native kernel hashes 8–12 M codepoints per second per core.
- **From:** [Identity: BLAKE3](../Storage/Identity.md#blake3), [Research: Hashing: BLAKE3](../Research/Hashing.md#blake3), [Research: Hashing: Truncation to 128 bits](../Research/Hashing.md#truncation-to-128-bits).

### 5.2 Convert every point to fixed point

- **In:** the point of every codepoint from [4. Projection](Projection.md).
- **Do:** store every coordinate as *m* · 2⁻⁵³ with integer |*m*| ≤ 2⁵³. Such values are exact doubles, so the columns stay `float8`, while all arithmetic on them is integer arithmetic. Truncate each generated coordinate toward zero to the grid.
- **Out:** four integers per codepoint.
- **From:** [Research: Numerics: The fixed-point grid](../Research/Numerics.md#the-fixed-point-grid).

### 5.3 Move every point inside the wall

- **In:** the fixed-point coordinates of 5.2.
- **Do:** the generated points are correctly rounded doubles, and rounding can push a norm above 1: in exact arithmetic 557,263 of the generated points, half of them, lay outside the unit ball by at most 4.4 × 10⁻¹⁶, and none exactly on it. While Σ*m*² > 2¹⁰⁶, which is exact in 128-bit integers, decrement the largest |*m*| by one.
- **Out:** every point with *m*·*m* ≤ 2¹⁰⁶ exactly.
- **Check:** 0 steps for 556,849 points, 1 for 501,210, 2 for 55,477, 3 for 574, 4 for 2; 624,971 ulp steps in total; no coordinate moved more than 4.44 × 10⁻¹⁶. After this, the wall is a theorem about the stored numbers: the exact centroid of points of norm at most 1 has norm at most 1 by convexity, rounding toward zero never increases a norm, and for a pure repeat Σ = *k*·*p* exactly so `[n,n,…,n]` lands bit for bit on n's point. The native wall check runs at 296 M points per second per core.
- **From:** [Space: The wall](../Storage/Space.md#the-wall), [Research: Numerics: Norm at most one](../Research/Numerics.md#norm-at-most-one), [Research: Numerics: The fixed-point grid](../Research/Numerics.md#the-fixed-point-grid), [Research: Prototype: Tier 0](../Research/Prototype.md#tier-0).

### 5.4 Record the Hilbert value

- **In:** the Hilbert value of each point from [4. Projection](Projection.md) operation 4.5.
- **Do:** record it beside the coordinate. The Hilbert value is for locality, partitioning, and ordering, to optimize performance and reduce random thrashing. It maps to coordinates deterministically and mathematically, so it can be used for indexing, filtering, and querying; it is derived from the coordinate and never part of an ID.
- **Out:** one Hilbert value per codepoint.
- **From:** [Atoms: Placement](../Storage/Atoms.md#placement), [Physicality: Real coordinates](../Storage/Physicality.md#real-coordinates).

### 5.5 Record the rank and the flags

- **In:** the DUCET rank of [4. Projection](Projection.md) operation 4.3 and the flags read in [1. Unicode](Unicode.md).
- **Do:** record the rank, and generate the flags that go with tier 0 from the standard's own lists: the bidi, CJK, and emoji data, and the ISO and other flags.
- **Out:** the rank and flags of every codepoint.
- **From:** [Atoms: Unicode data](../Storage/Atoms.md#unicode-data).

### 5.6 Write the table

- **In:** everything from 5.1 to 5.5.
- **Do:** write all 1,114,112 records into one file. The prototype's record is 64 bytes: BLAKE3-128 ID, fixed-point coordinate, Hilbert value, DUCET rank; the whole table is 68 MiB. Tier 0 is generated native C that is marshalled into PostgreSQL.
- **Out:** the tier-0 file, and the flags file that goes with it.
- **From:** [Atoms: Generation](../Storage/Atoms.md#generation), [Research: Prototype: Tier 0](../Research/Prototype.md#tier-0).

### 5.7 Fingerprint it

- **In:** the file of 5.6.
- **Do:** hash the whole table. Every build has a checksum, a fingerprint, so an install knows which tier 0 it has. Two installs with the same fingerprint produce the same coordinates for the same content, so they sync perfectly.
- **Out:** the fingerprint. The prototype's, the SHA-256 of its table, is `1710d2d9899ce403c73513642250b80a0827cf77819fbd79a8ae93c5aae482a5`.
- **Check:** the `icx` and `gcc` builds of Laplace-Native both reproduce the prototype's tier-0 IDs and Hilbert values bit for bit.
- **From:** [Atoms: Generation](../Storage/Atoms.md#generation), [Research: Engine Measurements: Native operations](../Research/Engine.md#native-operations).

### 5.8 Map it as the perf-cache

- **In:** the file of 5.6.
- **Do:** memory-map it, read-only and shared, in the client and in every database backend on first use, outside PostgreSQL's memory contexts, with a setting that holds the file path. Backends are forked processes, and the page cache shares the physical memory among them; read-only data needs no locking, and parallel workers map the file as well. The client can then look up any codepoint in O(1), in microseconds. Tier 0 is still recorded to the database, but function calls never need to read it from there; that eliminates at least half of the database calls and round trips.
- **Out:** O(1) lookup of any codepoint's ID, coordinate, Hilbert value, and flags, on the client and inside the database.
- **From:** [Atoms: Generation](../Storage/Atoms.md#generation), [Identity: Client-side computation](../Storage/Identity.md#client-side-computation), [Research: Geometry: C extensions](../Research/Geometry.md#c-extensions).

### 5.9 Make it modular

- **In:** the table of 5.6.
- **Do:** the perf-cache is modular: ASCII, UTF, CJK, emoji, and so on. The same applies to other modalities, such as 8-bit, 16-bit, and 32-bit color for images. That enables deployment to lesser hardware; the full tier 0 is small enough for a Raspberry Pi.
- **Out:** the modules an install can choose to map.
- **From:** [Atoms: Generation](../Storage/Atoms.md#generation).

## What this stage leaves behind

The ID, coordinate, Hilbert value, rank, and flags of every codepoint, in one fingerprinted file that the client and every database backend map.

## Without this stage

Nothing above tier 0 can have an ID or a coordinate, because every composition's ID is hashed from its constituents' IDs and every coordinate is computed up from the codepoint leaves. The client can compute nothing, and every lookup would need a database round trip.
