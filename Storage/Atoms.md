# Atoms

Codepoints are tier 0, the absolute floor: every Unicode codepoint has a deterministic ID and a deterministic coordinate on the S³.

## The codespace

Every codepoint in the Unicode codespace has a point: all 1,114,112 of them in Unicode 17. The scope is never reduced to the codepoints in use.

## Placement

Codepoints are placed across the S³ with Marc Alexa's Super-Fibonacci spirals and the Hopf fibration, sequenced by DUCET, with reverse-ordinal ordering. Only about 150,000 of the 1,114,112 codepoints are in use, and this placement still distributes them evenly, giving a perfect distribution across the S³.

Every codepoint also has a Hilbert curve value: the actual Hilbert value from the S4, filtered to the S³. It is for locality, partitioning, and ordering, to optimize performance and reduce random thrashing.

## Unicode data

Tier 0 is built from the Unicode data, in full:

- the UCD XML, flat or grouped, which carries `UnicodeData`, `Scripts`, and the other UCD files;
- `allkeys.txt` from the UCA, for sequencing;
- the bidi, CJK, and emoji data;
- the ISO and other flags that go with them.

## Generation

Tier 0 is generated native C that is marshalled into PostgreSQL. It is memory-mapped as a perf-cache, so the client can look up any codepoint in O(1), in microseconds.

Tier 0 is still recorded to the database, but function calls never need to read it from there. That eliminates at least half of the database calls and round trips.

## Unicode versions

The codespace will not change for a very long time. A new Unicode version changes only the points.
