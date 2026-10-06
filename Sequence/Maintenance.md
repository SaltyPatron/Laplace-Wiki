# 29. Maintenance

An install is kept right by forgetting a source per witness, sweeping what nothing references, regenerating caches whose dependencies changed, reseeding only when semantics change, upgrading the extension in place, and proving after each that the deployed revision is one build.

The rules here run for the life of an install. Each preserves the invariants the chain established: every physicality coordinate inside the bounded domain; every packed constituent id resolving to an entity; ordinal and run expansion matching the declared constituent count; realized curves built from resolved child coordinates and never from carriers; attestation and consensus endpoints resolving; every lane with a reconstructor reconstructing; and coordinate or Hilbert equality never read as identity.

## Before this stage

A running install: everything through [22. Users](Users.md).

## Operations

### 29.1 Forget a source

- **In:** a witness to correct or remove.
- **Do:** correcting a source is per-witness replacement, never a database recreate: remove the source's attestations and its trunk, sweep what nothing references any more, replay the standings it touched, and re-ingest the corrected generation, whose files give it a trunk of its own. The engine's forget removes a source's contributions; observed testimony from other witnesses stays. With provenance by containment, the target, removing the trunk is the whole of the forget, once a working prototype shows containment replays exactly what the attestation table does. Old evidence remains addressable rather than being overwritten. Never reset or drop the database without explicit authorization for that action.
- **Out:** the world without that witness's testimony, standings refolded.
- **From:** `docs/plan/ASSIMILATION_ROADMAP.md` workstream C; `docs/specs/06_Engineering_Ruleset.txt` §Operational constraints; `docs/INVENTION.md` §11.

### 29.2 Sweep

- **In:** the store after a forget.
- **Do:** the engine's sweep removes entities and physicalities that no path, claim, or source references any longer, in tier order from the trunk down, set-based. Tier 0 is never swept: it is the fixed list from the Unicode generation.
- **Out:** a store with no orphans.
- **From:** [Ingestion: Deduplication](../Storage/Ingestion.md#deduplication); `docs/INVENTOR_RECORD.md` §Tiers.

### 29.3 Re-ingest idempotently

- **In:** a source already admitted, run again.
- **Do:** unchanged completed files are skipped by the byte check of [11. Content](Content.md) operation 11.2; an edited file admits its changed structure and keeps the previous content; existing attestation identities are excluded from repeated folding, so a retry never multiplies witnessing. Re-ingestion reproduces identities and source testimony exactly.
- **Out:** nothing new, or only what changed.
- **From:** `seeds/operational/README.md`; `docs/specs/08_Record_vs_Calculate_Spec.txt` §Acceptance.

### 29.4 Regenerate the caches that depend on what changed

- **In:** a changed generation: a recipe, a manifest, a lower cache, a hot set.
- **Do:** rebuild the dependents named in each blob's dependency manifest of [7. Perfcaches](Perfcaches.md) operation 7.3 and no others; publish atomically; the loader refuses the stale generation until the new one is in place. A scalar canonicalization recipe change is a new number ROM generation; a relation manifest change is a new highway ROM; a new hot set is a new sparse image or chess generation.
- **Out:** consistent cache generations.
- **From:** `docs/specs/33_Perfcache_Blob_Law.md`; `docs/guides/compositional-perfcache.md` §Cache dependency and invalidation.

### 29.5 Reseed only when semantics change

- **In:** a change to a registry.
- **Do:** adding a relation, a qualifier value, a trust class, or a vocabulary value appends a bit or a code and touches no existing mask; it owes no reseed. A reseed is owed when semantics change, a rank or family edit, or when historical rows must gain a new bit's coverage. The last bit-order reseed is the one that froze the layout, and a retired relation keeps its bit forever. When a reseed runs, the seeds apply the locally materialized rows rather than re-decomposing.
- **Out:** a reseed, or none.
- **From:** `docs/decisions/0001-highway-bit-order.md`; `docs/plan/ASSIMILATION_ROADMAP.md` workstream C.

### 29.6 Upgrade the extension in place

- **In:** a new Laplace-postgres version.
- **Do:** after an engine rebuild, rebuild and install the extensions before verification; then `ALTER EXTENSION laplace UPDATE` through versioned upgrade scripts, never a drop, because dropping the extension drops every index built on its functions. Validate the installed extension, not an edited template. PostgreSQL's lifecycle is service-managed.
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
- **Do:** one ingest at a time; never kill an ingest or backend owned by another task; the CLI is a server workload with server GC, bounded memory, structured progress, and cancellation-safe journals; summary output is not verification; diagnose with independent evidence, wall time, CPU, waits, allocations, plans, lock state, and phase throughput at the layer that owns the claim; never validate a populated-system claim with an empty fixture; preserve unrelated worktree changes.
- **Out:** an install that stays measurable.
- **From:** `docs/specs/06_Engineering_Ruleset.txt` Rules #9, #11 and §Operational constraints.

## What this stage leaves behind

An install whose world can be corrected without being rebuilt, whose caches never lie about their generation, and which can prove at any time that it is one build.

## Without this stage

The first correction is a rebuild, the first stale cache is a wrong answer, and the first registry addition renumbers a billion rows.
