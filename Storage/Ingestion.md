# Ingestion

Ingestion computes content's IDs on the client and deduplicates it trunk to leaf against what is already recorded.

## Client-side

The client breaks content down and computes its IDs and coordinates itself, using the memory-mapped [tier 0](Atoms.md#generation).

## Recipes

Literally any standardized or fixed-format file is a modality to Laplace, and Laplace treats them all exactly the same: a generic decomposer uses a recipe to tell it how to extract the content.

Encrypted content has no value to Laplace: it is random binary blob storage. The database itself can be encrypted.

The decomposer and the ingestion pipeline are optimized to the limit and powered by recipes that denote how to decompose content into Laplace records: how content is recorded, what content is recorded, what gets reproducibility, and what does not matter.

## Deduplication

Deduplication is an O(tier) check from trunk to leaf. Everything it finds already recorded is eliminated, so the check reduces its own total count as it goes.

The client has decomposed the content and holds a deterministic trunk ID for every tier, with the records, their coordinates, and their physicality trajectories already made and deduplicated on the client. The check is the client saying "I have these IDs: which do you already have?" and omitting those from what it writes. It goes by the IDs: the file trunk, the trunks of the file's metadata and of its content tree, then their children, whichever tree the recipe made. It never searches the tiers.

Asking first is what removes conflict handling and reduces the WAL: only new records are written. The check should take next to nothing, even for gigabytes.

The checks are set-based operations, not per-row conflict handling such as `ON CONFLICT`. See [Research: Engine Measurements](../Research/Engine.md#ingestion).

Same content means the same hash. If a trunk node matches, its children match as well; if they do not, the ingestion was done wrong. See [Research: Hashing](../Research/Hashing.md) and [Research: Prototype](../Research/Prototype.md#verification).
