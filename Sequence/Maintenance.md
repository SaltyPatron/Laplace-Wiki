# 29. Maintenance

An install is kept right by forgetting a source per witness, sweeping what nothing references, regenerating caches whose dependencies changed, reseeding only when semantics change, upgrading the extension in place, and proving after each that the deployed revision is one build.

The rules here run for the life of an install. Each preserves the invariants the chain established: every physicality coordinate inside the bounded domain; every packed constituent id resolving to an entity; ordinal and run expansion matching the declared constituent count; realized curves built from resolved child coordinates and never from carriers; attestation and consensus endpoints resolving; every lane with a reconstructor reconstructing; and coordinate or Hilbert equality never read as identity.

## Before this stage

A running install: everything through [22. Users](Users.md).

## Operations

### 29.1 Forget a source

- **In:** a witness to correct or remove.
- **Do:** correcting a source is per-witness replacement, never a database recreate: remove the source's attestations and its trunk, sweep what nothing references any more, replay the standings it touched, and re-ingest the corrected generation, whose files give it a trunk of its own. The engine's forget removes a source's contributions; observed testimony from other witnesses stays. With provenance by containment, the target, removing the trunk is the whole of the forget, once a working prototype shows containment replays exactly what the attestation table does. Old evidence remains addressable rather than being overwritten. Do not drop or recreate the entire database merely to fix a single source.
- **Out:** the world without that witness's testimony, standings refolded.
- **From:** `docs/plan/ASSIMILATION_ROADMAP.md` workstream C; `docs/specs/06_Engineering_Ruleset.txt` §Operational constraints; `docs/INVENTION.md` §11.

### 29.2 Sweep

- **In:** the store after a forget.
- **Do:** the engine's sweep removes entities and physicalities that no path, claim, or source references any longer, in tier order from the trunk down, set-based. Tier 0 is never swept: it is the fixed list from the Unicode generation.
- **Out:** a store with no orphans.
- **From:** [Ingestion: Deduplication](../Storage/Ingestion.md#deduplication); `docs/INVENTOR_RECORD.md` §Tiers.

### 29.3 Re-ingest idempotently

- **In:** a source or repository already admitted, run again.
- **Do:** the ingest journal checks each file's raw byte-hash on disk (bound to the active recipe and grammar generation, [11. Content](Content.md) operation 11.2) to skip re-running Tree-sitter or UAX #29 on unchanged completed files while keeping canonical substrate file identity strictly as the Merkle trunk `lp_id`; modified files decompose and deduplicate `Trunk → Leaf` so unchanged subtrees stay shared; and existing `(claim, witness, lineage)` series update idempotently without multiplying standing. Re-ingestion reproduces canonical identities and source testimony bit-identically.
- **Out:** nothing new, or only what genuinely changed.
- **From:** [11. Content](Content.md) operation 11.2; `docs/specs/08_Record_vs_Calculate_Spec.txt` §Acceptance.

### 29.4 Regenerate the caches that depend on what changed

- **In:** a changed generation: a recipe, a manifest, a lower cache, a hot set.
- **Do:** rebuild the dependents named in each blob's dependency manifest of [7. Perfcaches](Perfcaches.md) operation 7.3 and no others; publish atomically; the loader refuses the stale generation until the new one is in place. A scalar canonicalization recipe change is a new number ROM generation; a `manifest/banks.tsv` or `manifest/slots/` change is a new `highway.bin` ROM; a new hot set is a new sparse image or chess generation.
- **Out:** consistent cache generations.
- **From:** `docs/specs/33_Perfcache_Blob_Law.md`; `docs/guides/compositional-perfcache.md` §Cache dependency and invalidation.

### 29.5 Reseed only when semantics change

- **In:** a change to a governed manifest or recipe.
- **Do:** introducing a new content predicate in a `.recipe` requires zero C manifest edits and zero reseeds ([6. Registries](Registries.md) operation 6.1). Appending a new slot to `manifest/slots/*.tsv` or a new trust class touches no existing `bit(64)` mask and owes no reseed. A reseed (or targeted per-source `laplace forget` + re-ingest under 29.1) is owed only when a recipe's semantic mapping changes or historical rows must populate a newly added `manifest/banks.tsv` bank. Retired slots keep their slot numbers forever so historical masks never decode against the wrong meaning.
- **Out:** a targeted re-ingest/reseed only when semantics change, or none.
- **From:** `Laplace-Native/manifest/banks.tsv`; [6. Registries](Registries.md) operations 6.1 and 6.2.

### 29.6 Upgrade the extension in place

- **In:** a new Laplace-postgres version.
- **Do:** after an engine or extension rebuild, install the module and run `laplace deploy` before verification. Because `Laplace-postgres` hashes persistent storage table DDL (`laplace-storage:<hash>`) separately from replaceable C and SQL routines (`laplace.reconcile.sql`), compatible databases upgrade in place (`ALTER EXTENSION laplace UPDATE TO ...`) with all data and indexes preserved; recreate (`laplace deploy --recreate`) only when persistent table storage layout changes. The extension is never dropped out of a database that is kept, because dropping the extension drops every column and index built on its types and functions. Validate the installed extension, not an edited template. PostgreSQL's lifecycle is service-managed.
- **Out:** the extension at the new version, indexes intact.
- **From:** [Builds: Laplace-postgres](../Operations/Builds.md#laplace-postgres); `docs/specs/06_Engineering_Ruleset.txt` §Operational constraints.

### 29.7 Prove one deployed revision

- **In:** the install after any of the above.
- **Do:** the application, the prefix native libraries, the PostgreSQL execution module, and the tier-0 perf-cache must identify one build; the deployed-revision check probes each served record in the serving process, the tier-0 fingerprint of [5. Tier 0](Tier-0.md) operation 5.7, the vocabulary record, the chess floors, against the canonical function. Then the self-checks of [14. Indexes](Indexes.md) operation 14.10.
- **Out:** an install that knows it is one build.
- **From:** `docs/OPERATING_SEQUENCE.md` §6; `docs/specs/33_Perfcache_Blob_Law.md`.

### 29.8 Prove physical-plan invariance across sources

- **In:** the admitted estate.
- **Do:** run the cross-source matrix of [9. Sources](Sources.md) operation 9.7 whenever the spine changes: the durable semantic fingerprint of every source must be identical under every legal physical plan.
- **Out:** the invariance receipts.
- **From:** `docs/plan/INGEST_BOUNDARY_AND_RECIPE_LAW.md` §Physical-plan invariance.

### 29.9 Adopt a new Unicode version

- **In:** a new Unicode release whose data and segmentation tooling are both final.
- **Do:** [1. Unicode](Unicode.md) through [5. Tier 0](Tier-0.md) again: only the points move, the IDs do not, so a new tier 0 with a new fingerprint is generated, every dependent cache is regenerated under 29.4, and coordinates and Hilbert values above tier 0 are recomputed from the leaves. A new tier-0 generation is a governed foundation change; ordinary numbers and modality values compose above the floor and never allocate unused ranks.
- **Out:** a new generation, fingerprinted.
- **From:** [Atoms: Unicode versions](../Storage/Atoms.md#unicode-versions); `docs/invention/modality-ladder-law.md` §Tier-0.

### 29.10 Keep the operating rules

- **In:** every day.
- **Do:** one ingest at a time per database; never kill an ingest or backend owned by another active run; the CLI is a server workload with server GC, bounded memory, structured progress, and cancellation-safe journals; summary output is not verification; diagnose with independent evidence, wall time, CPU, waits, allocations, plans, lock state, and phase throughput at the layer that owns the claim; never validate a populated-system claim with an empty fixture; evaluate leftover agent worktree changes against the invention rather than stranding broken partial work.
- **Out:** an install that stays measurable.
- **From:** `docs/specs/06_Engineering_Ruleset.txt` Rules #9, #11 and §Operational constraints.

## What this stage leaves behind

An install whose world can be corrected without being rebuilt, whose caches never lie about their generation, and which can prove at any time that it is one build.

## Without this stage

The first correction is a rebuild, the first stale cache is a wrong answer, and the first registry addition renumbers a billion rows.
