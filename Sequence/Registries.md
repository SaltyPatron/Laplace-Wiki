# 6. Registries

Before any source is admitted, the 64-bit mask banks, highway vocabularies, trust classes, model operator templates, and firmware policy kinds are enumerated as governed, append-only perf-caches: every member is a content-derived entity (`noun` is `[n,o,u,n]`), its stable bit or slot is only an acceleration index over it, any content entity may serve as a claim predicate without registration, and no registry is a table of made-up IDs.

Laplace separates open-ended semantic claims from fixed-width hardware acceleration. Any content entity at any tier (`capital`, `hypernym`, `P36`, `abandon.01`, `NOUN`) may serve immediately as a predicate, role, or argument in an n-ary claim (`[France, capital, Paris]`, `[Q142, P36, Q90]`, `[dog, eng, i46360]`, `[dog, NOUN]`) without editing a C manifest or rebuilding the engine. Governed registries exist strictly for the fixed bit fields, ROM slot tables, trust priors, operator shapes, and firmware parameters whose binary layout must remain append-only and identical across installs. Every member in every governed list is an ordinary content-derived entity (`noun` is the same `[n,o,u,n]` as the word anywhere else), and its bit or slot is a perf-cache acceleration index over that entity, never a lookup table of fabricated IDs. Developer handles in manifests and C headers are conveniences only; no runtime path tests English strings for meaning.

## Before this stage

[5. Tier 0](Tier-0.md): every label and identifier in every manifest is text, and its identity is the canonical Tier-0 composition of that text, so tier 0 must exist before a registry or `highway.bin` can name anything. [3. Builds](Builds.md): the generator that compiles the manifests into C headers and perf-cache ROMs.

## Operations

### 6.1 Keep claim predicates open content; freeze only acceleration slots

- **In:** the meanings curated sources and recipes assert, and the closed standards vocabularies used as index filters.
- **Do:** do not force open-ended world predicates into a closed C enum. Any content entity may stand in the predicate or role slot of an n-ary claim ([12. Attestations](Attestations.md) operation 12.5), so admitting GeoNames `capital`, Wikidata `P*` properties, domain lexicons, or user-authored `.recipe` files in Recipe Studio requires zero C rebuilds. At the same time, enforce the structural laws that prevent relation proliferation: a negation is never a `NOT_*` string relation ("hot is not cold" or ConceptNet `NotDesires` lowers to a refute outcome on the positive claim, `outcome = LOSS` / score `< 0.5`); an inverse is the same relation read from the other end; and constituent order, adjacency, gaps, and containment live in `physicality.path` trajectories, never in `precedes` or `contains` rows. Only the bounded grammatical, lexical, and row-role enumerations that drive bitmask prefiltering and highway crosswalks are frozen into append-only slot lists (`Laplace-Native/manifest/slots/*.tsv`).
- **Out:** open-ended content predicates for claims, plus frozen append-only slot lists for mask banks and highway road classes.
- **From:** [Claims: Tuples](../Semantics/Claims.md#tuples); [Reference: Types, masks and the highway](../Reference/Types.md); [30. Conflicts](Conflicts.md) S3.

### 6.2 Fix the 64-bit `mask` banks

- **In:** `Laplace-Native/manifest/banks.tsv` and the frozen slot lists in `manifest/slots/`.
- **Do:** partition the single 64-bit carrier (`uint64_t` in C, `bit(64)` on `entity.mask` and `physicality.mask` in PostgreSQL) into disjoint, append-only bit fields whose offsets never move:
  - `kind` (8-bit flag set at offset `0` on row carriers): row roles (`CLAIM`, `RECORD`, `TUPLE`, `FILE`), distinguishing assertions and records from ordinary prose or media trajectories inside the composite GIN index;
  - `upos` (5-bit enum at offset `8`): Universal Dependencies universal parts of speech;
  - `lexfile` (6-bit enum at offset `13`): WordNet lexicographer semantic files;
  - `deprel` (6-bit enum at offset `19`): Universal Dependencies syntactic dependency relations;
  - `vnrole` (6-bit enum at offset `25`): VerbNet thematic roles;
  - `wnframe` (6-bit enum at offset `31`): WordNet syntactic verb frames.

  Each enum field stores `slot + 1` (`0` = absent) from its append-only `manifest/slots/LIST.tsv`, leaving upper bits of the 64-bit carrier free for future governed banks. Slots are only ever appended or tombstoned, never renumbered or reused, so stored `bit(64)` masks never silently change meaning across versions. (Codepoint-level Unicode properties stay in their dedicated 256-bit `tier0.flags` ROM rather than consuming `entity.mask` bits.)
- **Out:** the 64-bit `mask` layout (`LP_MASK_BITS` and `laplace_mask_*`), shared identically by `Laplace-Native`, `Laplace-postgres`, and `Laplace-Engine`.
- **From:** `Laplace-Native/manifest/banks.tsv`; [Reference: Schema](../Reference/Schema.md#the-mask); [Reference: Types, masks and the highway](../Reference/Types.md#masks).

### 6.3 Separate witness certainty from firmware salience

- **In:** claims in `consensus` and predicates weighed at read time.
- **Do:** keep epistemic certainty and read-time salience strictly orthogonal. Certainty comes from witness trust and corroborated game series in [13. Consensus](Consensus.md): a `HAS_SCRIPT` claim from Unicode is near-certain in `consensus` even when irrelevant to an open conversational prompt. Salience—which predicates, road classes, and parts of speech pull hardest for the active task—is decided at read time by the active `.firmware` profile (`weigh`, `role`, [18. Firmware](Firmware.md) operations 18.7 and 18.8) and by empirical container specificity, never by a hardcoded global float table that buries numeric or structural claims (such as assigning scalar values a magic `0.12` multiplier).
- **Out:** pure epistemic standing in `consensus`, and explicit task-relative weighing in `.firmware`.
- **From:** [Consensus: Trust](../Semantics/Consensus.md#trust); [18. Firmware](Firmware.md) operations 18.7 and 18.8; [30. Conflicts](Conflicts.md) S3.

### 6.4 Represent qualifiers and claim specifics without closed bit-table bottlenecks

- **In:** claim variants such as language codes, mapping modes, name roles, and calculation provenance.
- **Do:** carry open or relational qualifiers directly as content constituents in the n-ary claim composition (`[dog, eng, i46360]` carries ISO 639 `eng` in the strand itself; a case or normalization mapping names its target mode as content) or in the asserting record trajectory under the witness trunk, while vertex `M` (`said` roles `CLAIM`, `RECORD`, `TUPLE`, `METADATA`, `HOLDS`, `VOICE`, `DEPENDENCE`, `outcome`, and `position`) and the `kind` mask bank carry structural row roles. Calculated evidence records its analyzer and recipe provenance explicitly ([12. Attestations](Attestations.md) operation 12.10). No source waits on a 256-bit qualifier manifest edit to express its nuances.
- **Out:** n-ary claim compositions and vertex `M` / `kind` role encodings.
- **From:** [Claims: Tuples](../Semantics/Claims.md#tuples); [Reference: Formats](../Reference/Formats.md); [12. Attestations](Attestations.md) operations 12.5 and 12.9.

### 6.5 Declare the trust classes

- **In:** the kinds of witness Laplace hears from.
- **Do:** a witness's trust class seeds its initial trust prior in `[0, 1]` (or negative for reliably adversarial/inverted witnesses), bounding what any single witness's game series can move in [13. Consensus](Consensus.md) operation 13.2. Classes are append-only; a class's meaning never changes once declared. The governed hierarchy: `SubstrateMandate` 1.00 (mandated structural laws); `StandardsDerived` 0.95 (Unicode, ISO 639, FIDE rules, endgame tablebases, deterministic compiler/test toolchains); `AcademicCurated` 0.85 (OEWN, OMW, CILI, UD, FrameNet, VerbNet, PropBank, SemLink, curated opening theory); `AcademicCuratedWithUserInput` 0.78; `StructuredCorpus` 0.70, `DerivedCalculation` 0.70; `UserCuratedResource` 0.60 (Wiktionary, Wikidata, Tatoeba); `AIModelProbe` 0.50 (an assimilated model checkpoint); `AppDerived` 0.40, `AgentTranscript` 0.40, `ToolResultContent` 0.40; `UserPromptContent` 0.30; `ResponseContent` 0.20 (Laplace's own generated responses); `AdversarialUntrusted` 0.00. Standards outrank academic curations, which outrank community wikis and parallel corpora; an assimilated model outranks raw prompts and sits below curated datasets; Laplace's own output sits below user prompts by design. Sharing a trust class never collapses independent witnesses into a single dependence root ([13. Consensus](Consensus.md) operation 13.3).
- **Out:** the trust-class priors, each class a content-derived entity whose English code name is a developer handle only.
- **From:** [Consensus: Trust](../Semantics/Consensus.md#trust); [30. Conflicts](Conflicts.md) C4.

### 6.6 Declare row kinds and highway road classes

- **In:** the structural row roles (`kind`) and cross-resource identifier systems (`manifest/slots/`).
- **Do:** distinguish row-role flags (`CLAIM`, `RECORD`, `TUPLE`, `FILE` in `banks.tsv`) and highway road classes (`ili`, `Synset`, `upos`, `deprel`, `lexfile`, `vnclass`, `vnrole`, `fnframe`, `fnfe`, `fnlu`, `pbroleset`, `vaframe`, ISO 639 language codes) from content identity. An entity is never salted with a type label such as `WordNet_Synset`, `Byte`, or `Channel`: a value gets its domain role strictly from the higher-tier compositions and claims that hold it, so the exact same `['2','5','5']` entity serves as a pixel channel intensity, a raw byte value, an IPv4 octet, a code literal, and a prose numeral.
- **Out:** the row-kind and highway road-class manifests.
- **From:** [Compositions: Types](../Storage/Compositions.md#types); [Reference: Types, masks and the highway](../Reference/Types.md).

### 6.7 Declare the governed vocabularies and tagset crosswalks

- **In:** the authorities' published lists: UD tools' `upos.json`, `deprels.json`, and `feats.json`; WordNet `lexnames` and verb frames; VerbNet roles; Brown, Penn Treebank, WordNet, and Webster POS tagsets; CILI, PropBank, VerbNet, FrameNet, and VerbAtlas identifier lists.
- **Do:** generate append-only slot tables in `Laplace-Native/manifest/slots/` and crosswalk edges (`edges-tagsets.tsv` and inter-resource mappings). Source text is recorded literally as written: WordNet's `n` stays `[n]`, Penn Treebank's `nns` stays `[n,n,s]`, and UD's `NOUN` stays `[N,O,U,N]`. Crosswalks link tagset slots to shared `upos` slots (and set the corresponding `upos` field in `mask`) by governed authority without rewriting the source's text. Languages are never stored in a mask bank: ISO 639 codes (`eng`, `en`, `jpn`) are highway nodes inside lexicalization claims (`[dog, eng, i46360]`), linked across 2-letter and 3-letter standards by attested ISO/CLDR claims.
- **Out:** `manifest/banks.tsv`, `manifest/slots/*.tsv`, and tagset/highway crosswalk tables.
- **From:** [Claims: Masks](../Semantics/Claims.md#masks); [Reference: Types, masks and the highway](../Reference/Types.md#perf-caches).

### 6.8 Declare the model operator templates

- **In:** the operator tensor shapes conventional checkpoints contain.
- **Do:** declare the structural templates that [24. Models](Models.md) matches tensors against by shape: vocabulary projection, position and segment embeddings, norms, grouped-query self-attention, fused QKV in either orientation, multi-head latent attention, gated/fused-gated/plain MLP, MoE router, stacked experts, and low-rank factor pairs. Tensor names break ties only between equal shapes; roles remain source-scoped structural coordinates rather than Laplace's native ontology.
- **Out:** the model operator shape declarations.
- **From:** [24. Models](Models.md) operation 24.5.

### 6.9 Declare the firmware policy kinds

- **In:** every parameter and decision rule [18. Firmware](Firmware.md) may bind.
- **Do:** enumerate the governed `.firmware` directive vocabulary (`hop`, `search`, `translate`, `follows`, `pull`, `weigh`, `role`, domain/plane scope, conservative `k`, hop tax `lambda`, fanout, frontier bounds, near-tie spread/temperature, seed policy, shape metric, and ambiguity/realization disposition). An unknown directive in a `.firmware` file fails validation loudly rather than being silently ignored. Ship `program.firmware` and task profiles (`deductive`, `inductive`, `abductive`, `constructive`, `adversarial`, `chess`) as clean text definitions outside the database records.
- **Out:** the `.firmware` directive grammar and shipped baseline profiles.
- **From:** [Reference: Firmware](../Reference/Firmware.md); [18. Firmware](Firmware.md).

### 6.10 Generate the C headers and `highway.bin` from the manifests

- **In:** `tier0.bin` from [5. Tier 0](Tier-0.md) and the manifests of 6.1 to 6.9.
- **Do:** emit the `Laplace-Native` mask/slot headers and build `highway.bin` directly from `manifest/` plus `tier0.bin`, requiring zero raw external corpora on disk at build time. Every slot's `lp_id`, 4D fixed-point coordinate, and Hilbert key is computed by ordinary Tier-0 composition (`i46360` -> `['i','4','6','3','6','0']`), indexed by O(1) `(list, slot)` arrays, open-addressed `(list, id)` tables, and CSR crosswalk edges. Nothing is seeded as fabricated lookup rows.
- **Out:** generated C tables and the fingerprinted `highway.bin` ROM mapped by client and server.
- **From:** [7. Perfcaches](Perfcaches.md); [Reference: Types, masks and the highway](../Reference/Types.md#perf-caches).

## What this stage leaves behind

Frozen 64-bit `mask` banks (`manifest/banks.tsv`), `highway.bin` vocabulary slots and crosswalks, witness trust classes, model operator templates, and `.firmware` directives—every member a content-derived entity indexed in ROM—while claim predicates remain completely open content requiring zero C rebuilds for new domains or recipes.

## Without this stage

Mask bits would drift across builds, tagsets and lexical resources would lack O(1) highway crosswalks, and witness trust priors would have no shared scale.
