# Ingestion

Ingestion computes content's IDs on the client and deduplicates it trunk to leaf against what is already recorded.

## Client-side

The client breaks content down and computes its IDs and coordinates itself, using the memory-mapped [tier 0](Atoms.md#generation).

## Deduplication

Deduplication is an O(tier) check from trunk to leaf. Everything it finds already recorded is eliminated, so the check reduces its own total count as it goes.

Same content means the same hash. If a trunk node matches, its children match as well; if they do not, the ingestion was done wrong.
