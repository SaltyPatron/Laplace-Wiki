# Ingestion

Ingestion computes content's IDs on the client and deduplicates it trunk to leaf against what is already recorded.

## Client-side

The client breaks content down and computes its IDs and coordinates itself, using the memory-mapped [tier 0](Atoms.md#generation).

## Recipes

Literally any standardized or fixed-format file is a modality to Laplace, and Laplace treats them all exactly the same: a generic decomposer uses a recipe to tell it how to extract the content.

The decomposer and the ingestion pipeline are optimized to the limit and powered by recipes that denote how to decompose content into Laplace records: how content is recorded, what content is recorded, what gets reproducibility, and what does not matter.

## Deduplication

Deduplication is an O(tier) check from trunk to leaf. Everything it finds already recorded is eliminated, so the check reduces its own total count as it goes.

Same content means the same hash. If a trunk node matches, its children match as well; if they do not, the ingestion was done wrong. See [Research: Hashing](../Research/Hashing.md) and [Research: Prototype](../Research/Prototype.md#verification).
