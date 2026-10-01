# 7. Perfcaches

Above tier 0, every deterministic reusable layer that earns it is emitted as a fingerprinted, rebuildable, memory-mapped ROM whose dependencies follow composition, from number roots and vocabularies up to pixels, positions, and images.

Tier 0 is the anchor cache, what everything boils down to in all cases, but it is not the only perf-cache. A perf-cache is a deterministic, versioned, one-way acceleration of canonical structure or of a deterministic calculation over it. PostgreSQL is the system of record; a blob is never independent truth, never the only copy of testimony, never a manual data store, and a miss falls back to the canonical path and never redefines identity.

## Before this stage

[5. Tier 0](Tier-0.md): the anchor every higher record composes from. [6. Registries](Registries.md): the manifests the highway and vocabulary ROMs are generated from.

## Operations, per blob

### 7.1 Declare the blob's format

- **In:** the class of record to cache.
- **Do:** every blob format defines its magic, version, byte order, record layout, and bounds; the source database generation or fingerprint it derives from; its relation, manifest, and recipe compatibility inputs; a complete-file checksum and, where needed, section checksums; deterministic ordering and duplicate handling; its writer, loader, validation, and stale-file behaviour; and the canonical PostgreSQL operation that rebuilds or verifies it. Cache contents preserve typed meaning: a point cache stores point facts, a trajectory cache stores ordered manifests, a model-factor cache stores versioned factor records. Packing values into one binary format does not erase their semantic classes.
- **Out:** the format contract.
- **From:** `docs/specs/33_Perfcache_Blob_Law.md`.

### 7.2 Choose dense or sparse

- **In:** the legal state space of the layer.
- **Do:** when a recipe's legal state space is finite, directly enumerable, and serviceable in the machine's resource envelope, precompute the entire domain and use direct addressing, `record = records[address(value)]`, true O(1) with no hash table: the Unicode generation, the relation and highway manifest, small numeric domains, finite piece-and-square vocabularies, a pixel domain when its format makes full enumeration practical. When the possible universe is huge, patches, regions, frames, images, AST subtrees, chess positions, cache the finite admitted, selected, or hot canonical estate with a declared deterministic lookup, a minimal perfect hash, an open-addressed fixed table, a sorted key table, and state its big-O and collision semantics honestly. Not exhaustive does not mean not a perf-cache.
- **Out:** the lookup law of the blob.
- **From:** `docs/guides/compositional-perfcache.md` §Dense finite versus sparse/admitted caches.

### 7.3 Bind the dependency generations

- **In:** the lower caches and recipes this blob composes from.
- **Do:** every higher cache records the generations and fingerprints it depends on. The pixel ROM depends on the tier-0 generation, the scalar recipe, the channel order and precision recipe, and the placement recipe; the patch ROM on the pixel ROM and the patch shape recipe; the video structure ROM on the image and audio cache generations and the timing recipe. A lower change invalidates and rebuilds the affected dependents; unrelated caches stay usable.
- **Out:** the dependency manifest of the blob.
- **From:** `docs/specs/33_Perfcache_Blob_Law.md` §Compositional cache lattice; `docs/guides/compositional-perfcache.md` §Cache dependency and invalidation.

### 7.4 Declare the selector and profile

- **In:** the deployment the blob is for.
- **Do:** a cache generation may materialize only a declared subset of a canonical tier while preserving the same identities, coordinates, and recipes as the full world. Lawful selectors: a range, `U+0000..U+007F`; an explicit set or palette, `#000000 #FFFFFF #FF0000`; a generated finite set, every legal value under a declared bit depth; a band, selected frequency bins or filter-bank bands under one analyzer recipe; a predicate over deterministic typed fields; the hot or admitted set; the dependency closure of selected higher structures. The manifest binds the profile id, cache class, canonical recipe and generation, selector kind and payload hash, dependency modules, local lookup layout, record layout version, generator identity, output hashes and sizes, fallback policy, and publication generation. A local slot number is an acceleration address only: slot 0 may be U+0020, slot 17 may be `#FF0000`, and the loader returns the global canonical record; a subset never renumbers its members into a new semantic universe. Several modules compose into one runtime profile, such as an ASCII segment, a common scalar segment, and a Bash grammar segment for a terminal, or a selected script segment, a sample segment, a speech-band segment, and hot audio windows for speech. Overlap is verified by canonical record parity. Fallback is one of canonical-fallback, remote-fetch, profile-miss, or deny-by-authority, and the last comes only from the authority layer, never from a miss.
- **Out:** the profile manifest.
- **From:** `docs/specs/33_Perfcache_Blob_Law.md` §Segmented / profile-scoped ROMs; [Atoms: Generation](../Storage/Atoms.md#generation); [5. Tier 0](Tier-0.md) operation 5.9.

### 7.5 Emit, checksum, publish atomically

- **In:** the generator and its inputs.
- **Do:** the same decomposer that populates the database emits the blob, so the two are bit-identical by construction. Write to a temporary file, flush, checksum, and atomically replace. Readers map immutable files and never mutate their source. A blob never seeds PostgreSQL: the path is one way, from the canonical generator or the database to the file.
- **Out:** the published generation.
- **From:** `docs/specs/33_Perfcache_Blob_Law.md`; [Atoms: Generation](../Storage/Atoms.md#generation).

### 7.6 Load strictly

- **In:** the blob at its configured path.
- **Do:** the loader rejects a missing, truncated, corrupt, incompatible, or stale blob explicitly, and refuses unknown versions; it does not partially load and continue. A process-local native loader, the PostgreSQL module binding, and the prefix library must identify the same build. A green CI job, a file on disk, or a setting pointing at a path is not proof the serving process can load the blob; the deployed-revision check probes the served record.
- **Out:** a mapped generation, or a refusal.
- **From:** `docs/specs/33_Perfcache_Blob_Law.md`; `docs/OPERATING_SEQUENCE.md` §6.

### 7.7 Prove parity

- **In:** the blob and the canonical path.
- **Do:** perf-cache usage preserves parity with the canonical database and native reference path in ids, ordering, scores, unknown behaviour, and source scope. Performance tests do not replace semantic parity tests. A cache record must equal ordinary canonical composition for the same input; a missing entry falls back to canonical composition; changing a canonicalization recipe requires a new generation.
- **Out:** the parity receipt of the generation.
- **From:** `docs/specs/33_Perfcache_Blob_Law.md`; `docs/invention/modality-number-perfcache.md` §Correctness.

### 7.8 Look up trunk first, and resolve keys before the index

- **In:** a request value.
- **Do:** probe the highest lawful reusable composition before rebuilding its descendants: for a decoded image, the complete image key first; on a miss the region keys, then patch keys, then pixel or direct-domain lookup. A hit owns the already-verified descendant composition for that generation; only missed branches descend, so work is proportional to the novel branches. A deterministic materialization fingerprint may serve as the lookup key before the canonical root is known, provided the record binds shape, recipe, and dependency generation and a collision cannot return an unrelated object; that fingerprint is not identity. Then transform the request into canonical keys, id, coordinate, Hilbert value, range, before any indexed SQL or SPI probe, and feed them as parameters. Never wrap an indexed column in a per-row cache function, and never claim `IMMUTABLE` for a cache-backed function unless its mapped generation makes that promise valid for the lifetime of the index.
- **Out:** the canonical key, and an index probe on it.
- **From:** `docs/specs/33_Perfcache_Blob_Law.md` §Trunk-first lookup and §Index-friendly lookup law; [Query: Functions in queries](../Query.md#functions-in-queries).

## The roster

| Blob | Role | Lookup | Rebuilt from | Stage that needs it |
| --- | --- | --- | --- | --- |
| Tier-0 codepoint ROM | U+0000..U+10FFFF: id, UCA order, PointZM, Hilbert value, UAX flags, NFC compose and decomposition; format v4 `LPRF`, the only format the loader accepts | `records[cp]` | the UCD emit, [5. Tier 0](Tier-0.md) | every stage after 5 |
| Highway ROM | the relation-law bit plane: canonical name, band, bit, rank | bit test, 256-bit mask | the relation manifest, [6. Registries](Registries.md) | [12. Attestations](Attestations.md) |
| Number ROM | canonical integer roots 0..255, `0 → ['0']`, `42 → ['4','2']`, `255 → ['2','5','5']` | `records[value]` | tier 0 through the scalar recipe | [11. Content](Content.md) for images, audio, bytes |
| Vocabulary ROM | UPOS, dependency relations and subtypes, features, feature values: content id, coordinate, Hilbert value, tier, code, parent code, label | `(vocabulary, code)` direct index; `(vocabulary, id)` open-addressed | tier 0 plus the vocabulary manifests | [12. Attestations](Attestations.md) |
| Separator-id ROM | alphabet-bounded separator atoms and clusters | compiled set | tier 0 plus the grapheme law | [11. Content](Content.md) |
| Chess position ROM | piece-and-square vocabulary and catalog boards | id → coordinate, Hilbert value, tier | recorded-floor export | [27. Chess](Chess.md) |
| Chess transition ROM | deterministic `(from, move) → to` | mmap search | recorded-floor export | [27. Chess](Chess.md) |
| Pixel, patch, region, image ROMs | deterministic image compositions at successive tiers; an 8×8 region exposes its 204 square occurrences as references to global roots | direct where dense, sparse where admitted or hot | the image recipe plus lower generations | [11. Content](Content.md) for images and video |
| Audio sample, window, segment, track ROMs | deterministic audio tiers | direct where dense, sparse where hot | the audio recipe plus lower generations | [11. Content](Content.md) for audio and video |
| Factor ROM | versioned model-factor trajectories | pointer arithmetic | deposited factor physicalities | [24. Models](Models.md), [25. Export](Export.md) |
| Generation-corpus ROM | the cold generation lane | mmap | the generation corpus | [20. Forward](Forward.md) |

The number ROM is an acceleration of canonical composition, not the numeric domain: `0.34567` is `['0','.','3','4','5','6','7']` through the ordinary content path, and a million digits of π compose as one word without a ROM entry. Glicko-2 standing is not a perf-cache. Attestation ids are not codepoint ids. A new blob lands only with a row in this roster, a one-way rebuild path, determinism and staleness gates, a loader that refuses unknown versions, and a serving-process probe the deployed-revision check runs.

The dense ROMs, tier 0, highway, number, vocabulary, separator, are built here, before the database. The hot and admitted ROMs, pixels through images, audio, chess floors, factors, are generated after the content that fills them, under [14. Indexes](Indexes.md) operation 14.12, and regenerated under [29. Maintenance](Maintenance.md).

## What this stage leaves behind

A lattice of fingerprinted, rebuildable ROMs, each binding the generations it depends on, mapped by the client and by every backend, so that a known structure is a bounded lookup and only a new one is composed.

## Without this stage

Every codepoint, number, vocabulary value, and known image would be recomposed and looked up through the database on every use, and the O(1) that the trunk-to-leaf and leaf-to-trunk operations rely on would not exist.
