# 6. Registries

Before any claim is written, the relations, qualifiers, trust classes, entity types, vocabularies, and firmware policy kinds are enumerated as governed, append-only perf-caches: every member is a content-derived entity (`noun` is `[n,o,u,n]`), its stable bit or slot is only an index over it, and no registry is a table of made-up IDs.

Everything a claim can say is drawn from a fixed, governed list: which relation, under which qualifiers, by a witness of which trust class, about an entity of which type, using which part of speech or dependency label. Those lists are enumerated as completely as possible once, frozen, and only ever appended to, because at millions and billions of records a renumbering is not a maintenance operation. Each registry's members are content entities like everything else, `noun` the same `[n,o,u,n]` as the word anywhere, and a stable bit or slot is a perf-cache index over them, never the identity of a meaning: the registry is knowledge the substrate already has, not a lookup table of made-up IDs. A member's meaning is attested and realizable in any language; the English names in the manifests and the code are developer handles only, and no code path tests for an English value.

## Before this stage

[5. Tier 0](Tier-0.md): every label in every registry is text, and its identity is the content identity of that text, so tier 0 must exist before a registry can name anything. [3. Builds](Builds.md): the code generator that reads the manifests.

## Operations

### 6.1 Enumerate the relations completely, then freeze

- **In:** the meanings a claim can carry.
- **Do:** one relation per meaning. Ask how many different options human communication really has: `HAS_PART`, synonymy, antonymy, hypernymy, definition, example, external identifier, name, case mapping, decomposition, and the rest. A variant of a meaning is not a new relation; it is a qualifier on the claim (6.2). A direction is not a new relation; an inverse is an alias that resolves to the same relation read the other way. A negation is not a new relation; "hot is not cold" is a refute outcome on the positive relation, never a `NOT_` relation. An order or containment fact is not a relation at all; it lives in physicality trajectories and not in testimony. Before the freeze, do a deliberate completeness pass so that the families known to be coming, the modality ladders, the code and repository lane, the governance and credit bands, get their bits reserved now rather than appended piecemeal later. Reserved-but-unused bits are cheap; renumbering is not.
- **Out:** the relation inventory, one element per meaning, each a content entity whose meaning is attested; its English name in the manifest, `HAS_PART` or `IS_A`, is a developer handle and never its identity.
- **From:** [Claims: Tuples](../Semantics/Claims.md#tuples); `docs/decisions/0001-highway-bit-order.md`; `engine/manifest/relation_types.toml`; `docs/plan/ASSIMILATION_ROADMAP.md` law 5.

### 6.2 Assign every relation an explicit, append-only bit

- **In:** the inventory of 6.1.
- **Do:** each relation declares `bit = N` explicitly in the manifest. The code generator validates, unique, in range, no reuse of a retired bit; it never assigns. A new relation takes the next free bit; existing bits never move. A retired relation leaves a tombstone: it keeps its bit and its type identity so that evidence already admitted under it stays readable, names its successor plus the qualifiers that now carry its meaning, or its successor read in the other direction, or `TRAJECTORY` when the fact belongs to physicality, and resolving it for emission fails closed. A reused bit would make an old stored mask decode as a different relation, which is silent corruption, exactly the failure this rule exists to end.
- **Out:** the 256-bit highway mask layout, which every entity and every attestation carries.
- **From:** `docs/decisions/0001-highway-bit-order.md` §Decision; `docs/specs/05_Substrate_Invariants.txt` Rule #7.

### 6.3 Declare each relation's rank, symmetry, parent, and family root

- **In:** each relation of 6.1.
- **Do:** each relation declares a rank tier, a symmetry, a parent, and a family root. Rank is read-time salience, applied in coupling and not in the fold: mandate 1.0, definitional 0.97, taxonomic 0.90, equivalence 0.82, partitive 0.73, causal 0.64, oppositional 0.45, associative 0.36, tensor calculation 0.27, lexical glue 0.18, scalar valued 0.12, standards structural 0.08, probationary 0.05. Content relations are on top; grammatical glue and standards metadata are at the floor. A relation such as `HAS_SCRIPT` is certain and merely low-salience; certainty comes from the witness's trust, salience from the rank, and the two never become one number. Symmetry says whether the claim reads the same both ways. Family roots let subtype relations such as dependency and feature relations collapse to one root for capacity.
- **Out:** the `[ranks]` ladder and one rank per relation.
- **From:** `engine/manifest/relation_types.toml` `[ranks]`; `docs/plan/ASSIMILATION_ROADMAP.md` workstream A, decided 2026-09-25; [Consensus: Trust](../Semantics/Consensus.md#trust).

### 6.4 Enumerate the qualifier families

- **In:** every variant that 6.1 refused to make a relation.
- **Do:** a qualifier is a multi-select flag carried on an attestation's 256-bit mask, the sister of the entity highway mask. Each family owns up to 32 bits from a declared base; values are append-only within a family, and a value's bit never changes meaning. A family that declares `relations` applies to those relations only, so families whose relation sets are disjoint may share bit positions; a family without `relations` applies to every relation and owns its bits outright. `eng HAS_EXTERNAL_ID eng {iso639-2b, iso639-2t, iso639-3}` is one claim with three qualifier bits, not three relations. Families in the manifest: identifier under `HAS_EXTERNAL_ID` (iso639-1, iso639-2b, iso639-2t, iso639-3, bcp47, ili, the WordNet offsets and keys); name under `HAS_NAME` (primary, alias, reference, print, inverted, abbreviation, correction, control, alternate, figment, unicode-1); mapping under `HAS_CASE_MAPPING` and `NORMALIZES_TO` (lower, upper, title, fold, simple, full, nfkc, nfc, nfd, nfkd, and the UTS #46 operations); decomposition under `DECOMPOSES_TO` (the Decomposition_Type long names plus the DUCET's own tags); retirement under `SUPERSEDED_BY` (change, duplicate, non-existent, split, merge); membership under `HAS_PART`; and the derivation/calculation qualifier that marks calculated evidence.
- **Out:** the qualifier mask layout, and the value aliases recipes resolve source codes through.
- **From:** `engine/manifest/qualifiers.toml`; `docs/plan/ASSIMILATION_ROADMAP.md` law 5; [12. Attestations](Attestations.md) operation 12.7.

### 6.5 Declare the trust classes

- **In:** the kinds of witness Laplace will ever hear from.
- **Do:** a witness's class is the only statement of its trust, and the class's prior in [0, 1] seeds the standing of every claim that witness makes. Classes are append-only; a class's label and meaning never change once declared. The registry: SubstrateMandate 1.00, the substrate's own mandated structure, the governed laws and operational records; StandardsDerived 0.95, a standards body's published data, Unicode, ISO 639, FIDE, endgame tablebases, a toolchain's specified behaviour; AcademicCurated 0.85, OEWN, OMW, CILI, UD, FrameNet, VerbNet, PropBank, SemLink, opening theory; AcademicCuratedWithUserInput 0.78; StructuredCorpus 0.70; UserCuratedResource 0.60, Wiktionary; AIModelProbe 0.50, an ingested model; AppDerived 0.40; UserPromptContent 0.30; ResponseContent 0.20, Laplace's own responses; AdversarialUntrusted 0.00; DerivedCalculation 0.70; AgentTranscript 0.40; ToolResultContent 0.40. A standards body ranks above an academic curation, which ranks above a user-curated wiki, which ranks above subtitles; a model ranks above a user prompt and below a curated dataset; Laplace's own output ranks below a user prompt, by design.
- **Out:** the trust-class law; each class is a content entity whose meaning is attested, and `AcademicCurated` and the other names are developer handles, never identities.
- **From:** `engine/manifest/trust_classes.toml`; `docs/plan/ASSIMILATION_ROADMAP.md` law 8 and workstream A; [Consensus: Trust](../Semantics/Consensus.md#trust).

### 6.6 Declare the entity types

- **In:** the kinds of thing a recipe will mark.
- **Do:** a type is a filter on entity rows, never testimony and never seeded into the substrate. A type is a content entity like any other, its meaning attested, and its bit is a perf-cache index over it. The manifest's names for the types recipes disposition recovered objects into, `Word`, `Scalar`, `Byte`, `Channel`, `Collection`, `CILI_Concept`, `WordNet_Synset`, `Architecture`, `Agent_Model`, `Bidi_Resolution`, and so on, are developer handles, and no identity is derived from an invented label such as `WordNet_Synset` as if that label were the meaning. A value gets a type only when it is put into a composition; the same `[2,5,5]` serves as a pixel channel intensity, a raw byte value, and an IP segment.
- **Out:** the entity-type law.
- **From:** `engine/manifest/entity_types.toml`; [Compositions: Types](../Storage/Compositions.md#types).

### 6.7 Declare the governed vocabularies

- **In:** the authorities' own lists: UD tools' `upos.json`, the dependency relations and subtypes, the features and feature values.
- **Do:** refresh each vocabulary manifest from its authority file, recording the authority path and its SHA-256, and assign each value an append-only code with a parent code. Source text is recorded as it arrives and never rewritten: WordNet's `n` stays `[n]` and UD's `NOUN` stays `[N,O,U,N]`. Things that mean the same set the same bit: that `n` and `NOUN` are one part of speech, or that a two-letter code and an ISO 639-3 code name one language, is attested by the mapping source or the governed alias, each mapping justified by a governed authority, and both codes set the same mask bit; never by fabricating a record. A feature value is the ordered composition `[feature, value]`, so vocabulary records equal the ordinary content path.
- **Out:** `upos.tsv`, `deprel.tsv`, `deprel_subtype.tsv`, `feature.tsv`, `feature_value.tsv`, `pos_alias.tsv`, each generated, never hand-edited.
- **From:** `engine/manifest/vocabulary/`; `docs/plan/ASSIMILATION_ROADMAP.md` laws 3 and 4; [Claims: Masks](../Semantics/Claims.md#masks).

### 6.8 Declare the model operator templates

- **In:** the operator shapes a checkpoint can contain.
- **Do:** declare the templates that [24. Models](Models.md) recognizes tensors against by shape: vocabulary projection, position and segment embeddings, norms, grouped-query self-attention, fused QKV in either orientation, latent attention, gated, fused-gated and plain MLP, router, stacked experts, low-rank factor pairs. The name of a tensor is a hint; the shape constrains the role; roles are source-scoped coordinates, not native ontology.
- **Out:** `model_operators.toml`.
- **From:** `engine/manifest/model_operators.toml`; `docs/plan/ASSIMILATION_ROADMAP.md` law 14.

### 6.9 Declare the firmware policy kinds

- **In:** every decision [18. Firmware](Firmware.md) may bind.
- **Do:** policy kinds, the parameter names and their value types, are a governed registry with stable bits like relations and qualifiers. A firmware image may bind only registered kinds; an unregistered kind is a rejected image, not an ignored field. The first image, `default`, names today's behaviour: salience floor 0.3, semantic hops 2, fanout 8, meeting hops 2, meeting fanout 256, meeting frontier 4,096, sharing window 32, sharing cap 4,096, spread 0.6, top_k 10, steps 128, max stride 5.
- **Out:** the firmware policy registry and its first image.
- **From:** `engine/manifest/firmware.toml`; `docs/specs/39_Personality_Firmware.md` §1.1 and §10.

### 6.10 Generate the code and the ROMs from the manifests

- **In:** the manifests of 6.1 to 6.9.
- **Do:** the code generator emits the relation law, the qualifier law, the trust-class law, the entity-type law, the firmware law, and the vocabulary and highway perf-caches of [7. Perfcaches](Perfcaches.md). The TOML is the single input; the registry is the TOML; nothing becomes hidden state. Governed vocabularies are perf-cache ROM registries whose stable bits index content entities; they are never seeded as rows, because a registry is not a lookup table of made-up IDs: its members are content like everything else.
- **Out:** generated native code and the manifest-derived blobs.
- **From:** `docs/decisions/0001-highway-bit-order.md`; `docs/plan/ASSIMILATION_ROADMAP.md` law 4.

## What this stage leaves behind

The complete, frozen, append-only lists of what a claim can say, who can say it and at what trust, what an entity can be typed as, which bit each source's codes set, and which decisions a firmware can make: every member a content entity whose meaning is attested, every bit a perf-cache index over it, and none of them a lookup table of made-up IDs.

## Without this stage

Every source would mint its own relations and codes, bits would move on every addition, stored masks would decode against the wrong layout, and no two witnesses could ever attest the same claim.
