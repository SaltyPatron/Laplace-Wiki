# Atoms

Codepoints are tier 0, the absolute floor: every Unicode codepoint has a deterministic ID and a deterministic coordinate on the S³.

## The codespace

Every codepoint in the Unicode codespace has a point: all 1,114,112 of them in Unicode 17. The scope is never reduced to the codepoints in use.

## Placement

Codepoints are placed across the S³ at Marc Alexa's Super-Fibonacci points, which relate to the Hopf fibration and distribute evenly across the S³. The points are taken in the order of their Hilbert value: the actual Hilbert value from the S4, filtered to the S³. The codepoints are sequenced by DUCET, and DUCET rank *r* takes the *r*-th point.

Collation neighbors are therefore spatial neighbors: `King` falls by `king`, by `ding`, by `dong`, by `kong`. The placement is not exact, but it is predictable and recordable.

The Hilbert value is also for locality, partitioning, and ordering, to optimize performance and reduce random thrashing.

## Unicode data

Tier 0 is built from the Unicode data, in full:

- the UCD XML, flat or grouped, which carries `UnicodeData`, `Scripts`, and the other UCD files;
- `allkeys.txt` from the UCA, for sequencing;
- the bidi, CJK, and emoji data;
- the ISO and other flags that go with them.

## Generation

Tier 0 is generated native C that is marshalled into PostgreSQL. It is memory-mapped as a perf-cache, so the client can look up any codepoint in O(1), in microseconds.

Tier 0 is still recorded to the database, but function calls never need to read it from there. That eliminates at least half of the database calls and round trips.

The perf-cache is modular: ASCII, UTF, CJK, emoji, and so on. The same applies to other modalities, such as 8-bit, 16-bit, and 32-bit color for images. That enables deployment to lesser hardware; the full tier 0 is small enough for a Raspberry Pi.

Every build has a checksum, a fingerprint, so an install knows which tier 0 it has. Two installs with the same fingerprint produce the same coordinates for the same content, so they sync perfectly.

## Unicode versions

The codespace will not change for a very long time. A new Unicode version changes only the points.
