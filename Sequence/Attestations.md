# 12. Attestations

Curated corpora are recorded as witnesses and typed claims, one cell per subject, relation, and object, qualified by mask, with sets as collections and calculations marked as such, in an order fixed by referential integrity and by the first-in-first-out matchups that follow.

Semantics are the relations Laplace records about entities, so that it can link concepts and languages and hop and fan out from anything to anything with integrity. Curated corpora give attestations; dozens of them are required, and this stage records what each one says, in order. A claim is "this source says X is, or is not, Y": the witness, the outcome, and the games.

## Before this stage

[11. Content](Content.md): every entity a claim will name. [8. Database](Database.md): the semantics tables. [6. Registries](Registries.md): the relations, qualifiers, trust classes, and vocabularies. [9. Sources](Sources.md) and [10. Recipes](Recipes.md): the witness and the claim declarations for each corpus.

## Operations, per corpus

### 12.1 Decide what the corpus attests

- **In:** the corpus.
- **Do:** a treebank, a dictionary, a thesaurus, or an encyclopedia is a different type of corpus from normal digital content: it states things about content. Curated corpora give attestations, observations, witnessing, usage, examples, and more. Decide what this corpus states, and at what tier: attestations are recorded at the highest tier possible for a given corpus, on the compositional object the source actually asserts. OpenSubtitles gives the language of sentences, not of words. Codepoints get attestations, such as a stroke count; words get attestations; sentences get attestations; and so on at every tier. A corpus that states nothing, such as a novel or a tokenizer's vocabulary, is content under [11. Content](Content.md), not a witness. What other source could attest at tier 0 than Unicode itself.
- **Out:** what this corpus's claims will be about, and at which tier.
- **From:** [Attestations: Attestations](../Semantics/Attestations.md#attestations); `docs/INVENTIONS.md` #27; `docs/INVENTOR_RECORD.md` §Attestations.

### 12.2 Name the witness and its lineage

- **In:** the corpus.
- **Do:** entities are witnessed. WordNet does not own `dog`: we observe `dog` from WordNet. Every witness observes the same entity. The witness is `[authority, release]`, one per lexicon, from [9. Sources](Sources.md) operation 9.4. If it is derived from another witness, record that lineage, so copies do not count as independent consensus: Open English WordNet is derived from Princeton WordNet, so the two form one lineage, and a claim both attest gets one matchup with both witnesses in its witness set. The witnessing is mechanistic interpretability, auditability, and provenance. A witness may be a standards source, lexicon, corpus, document, user, tool, game, deterministic calculation provider, conventional model, or Laplace itself; the source and context remain attributable.
- **Out:** the witness record, with its lineage.
- **From:** [Attestations: Witnesses](../Semantics/Attestations.md#witnesses); `docs/INVENTION.md` §5; [Research: Semantics Experiments: Witnessed claims](../Research/Semantics-Experiments.md#witnessed-claims).

### 12.3 Set the witness's trust from its class

- **In:** the witness of 12.2.
- **Do:** the witness's trust class from [6. Registries](Registries.md) operation 6.5 is the only statement of its trust, and the class's prior seeds the standing of every claim it makes. Trust runs from MANDATE, 1.0, down through standards, academically curated datasets, user-curated corpora, models, user prompts, and responses, to 0 for the adversarial and to −1 for the reliably wrong. A witness entering for the first time starts from the stock default for its level: the source's trust, stability, and uncertainty. Trust is played as the opponent's deviation in [13. Consensus](Consensus.md), so it is fixed here, before the first matchup. Relation rank is not trust and does not enter here.
- **Out:** the trust every claim from this witness will play at.
- **From:** [Consensus: Trust](../Semantics/Consensus.md#trust); [Consensus: Entry](../Semantics/Consensus.md#entry); `docs/plan/ASSIMILATION_ROADMAP.md` law 8 and workstream A.

### 12.4 Ingest the corpus's files as content

- **In:** the corpus's files and their recipe.
- **Do:** [11. Content](Content.md), operations 11.1 to 11.14. Every label the corpus uses, `dog`, `noun`, `i46360`, `eng`, `hypernym`, and the witness's own name, is content and gets its entity here. A corpus's annotation layers are content too: each sentence's part-of-speech sequence and dependency sequence hashed like compositions, so that small sub-structures share almost entirely while whole-sentence layers rarely repeat. An external identifier is a typed reference bound to content by a claim, not a node to render.
- **Out:** every entity the corpus's claims will name.
- **From:** [Claims: Tuples](../Semantics/Claims.md#tuples); `docs/plan/ASSIMILATION_ROADMAP.md` law 6; [Research: Semantics Experiments: Annotation layers as content](../Research/Semantics-Experiments.md#annotation-layers-as-content).

### 12.5 Form each claim as a typed cell of entities

- **In:** the entities of 12.4 and the recipe.
- **Do:** a claim is a tuple of entities with referential integrity: every part of a claim is an entity. `noun` is `[n,o,u,n]`, the same entity as the word "noun" anywhere else. Any tier's entity can be a predicate. The canonical consensus address is the typed `(subject, relation, object)` triple, with the relation drawn from [6. Registries](Registries.md) operation 6.1; every source speaking about that triple folds into the same cell. A lexicalization is `[lemma, language, ILI]`, a concept's part of speech `[ILI, POS, n]`, a relation `[ILI, hypernym, ILI]`. A word binds to a language-neutral key, `dog HAS_SENSE i46360 @eng`, `chien HAS_SENSE i46360 @fra`; facts about the key, `i46360 IS_A …`, are language-neutral, so one consensus over every witness is correct; a cross-language homograph binds to different keys. An entity with a physicality can be the subject or object of any number of claims; that is the intended pattern. Relations are tied together by types and tiers: an ILI synset is a type, just like an IP segment is. An order, containment, or co-occurrence fact is never a claim; it is read from the trajectory.
- **Out:** the claims, as paths of entity IDs.
- **From:** [Claims: Tuples](../Semantics/Claims.md#tuples); `docs/specs/05_Substrate_Invariants.txt` Rules #3, #6; `docs/plan/ASSIMILATION_ROADMAP.md` workstream B; [Research: Semantics Experiments: Witnessed claims](../Research/Semantics-Experiments.md#witnessed-claims).

### 12.6 Hash each claim twice

- **In:** the claims of 12.5.
- **Do:** deterministic content determines a claim's ID. A claim is a limited path trajectory, so its hash is computed the same way as a composition's: from the IDs along its path. Witnessing and consensus are two different beasts: for witnessing, the hash covers the claim's specifics, the witness, context, and qualifiers; for consensus, the hash covers only the main components that make the claim unique, the typed cell. So each claim gets a witnessing ID and a consensus ID, and two witnesses attesting the same claim land on the same consensus ID.
- **Out:** the claim IDs.
- **From:** [Claims: IDs](../Semantics/Claims.md#ids); [Consensus: Deduplication](../Semantics/Consensus.md#deduplication).

### 12.7 Set the qualifier mask and the entity masks

- **In:** the claims of 12.5.
- **Do:** the attestation's 256-bit qualifier mask says which variants the source asserts, from the families of [6. Registries](Registries.md) operation 6.4: `eng HAS_EXTERNAL_ID eng {iso639-2b, iso639-2t, iso639-3}` is one claim with three bits; a case mapping carries `lower` or `upper`, `simple` or `full`; a name carries `primary` or `alias`. Qualifiers are OR-merged under aggregation. Calculated evidence carries the derivation/calculation qualifier. Each entity carries OR-masks for filtering: `dog`'s part-of-speech mask is `NOUN|VERB`, and its highway mask has the bit of every relation it participates in. A mask is a filter; the actual score is a consensus read, and a mask miss is never authoritative absence. The mappings between curated resources, SemLink, PredicateMatrix, MapNet, WordFrameNet, and CILI, which link PropBank, VerbNet, FrameNet, WordNet, and ILIs to one another, are the Linguistic Super Highway, and the highway is part of the foundation behind the masks: bubble up to the numerical identifier, and back down into any language.
- **Out:** the qualifier mask of each attestation and the masks of each entity.
- **From:** [Claims: Masks](../Semantics/Claims.md#masks); [Claims: The Linguistic Super Highway](../Semantics/Claims.md#the-linguistic-super-highway); `docs/plan/ASSIMILATION_ROADMAP.md` laws 5 and 7; `docs/INVENTOR_RECORD.md` §Relations.

### 12.8 Record each set-valued fact as one collection

- **In:** each set-valued field the recipe declared under [10. Recipes](Recipes.md) operation 10.12.
- **Do:** sort the members ascending by id and deduplicate, so the identity is order-independent; the bundle id is the Merkle hash over the sorted members; add the bundle as an entity of type Collection; add its physicality as a set trajectory over the sorted members, with its own physicality type and its own partial GIN, never widening the text-trajectory indexes; and add one attestation `(subject, relation, bundle)`. Canonical order for a set is ascending by member id, and that order is the deduplication mechanism, not a policy choice: every later form carrying `{nom, sg, masc}` re-stages the same id and writes nothing new. A collection is an entity with a Merkle id, a coordinate, and typed edges; not a CSV column, not a `text[]`, not JSON, not a bitmask, and a representation that cannot carry a rating is not a collection.
- **Out:** one entity and one edge per distinct member set.
- **From:** `docs/specs/38_Collections_Are_Compositions.md` §3, §4.

### 12.9 Record each attestation with its outcome

- **In:** the claims of 12.6 and the witness of 12.2.
- **Do:** attestations are a win, draw, or loss, and/or a score in [0, 1] with a draw at 0.5, so there are positive and negative attestations. Confirmation, draw, and refutation remain distinct; the absence of a row is unknown, never refutation. A denial is a refute outcome on the positive relation. Record each one in `attestation` with its witness, its lineage, its context, its qualifier mask, and its outcome; an attestation records subject, relation, optional object, source, optional context, outcome, score, uncertainty inputs, and observation count. Observed testimony is append-only; a correction adds new testimony and never erases the earlier witness. What the corpus records beside a claim that is not an attestation, such as a witness's sense order or a tagged corpus's usage counts, is recorded as given, beside the claim, as an observation: merging a frequency into a standing loses it, because a standing measures whether a claim holds and saturates as its deviation shrinks. Ingest completion is operational state, never an attestation.
- **Out:** the attestations, in the order the corpus gave them.
- **From:** [Attestations: Outcomes](../Semantics/Attestations.md#outcomes); `docs/specs/05_Substrate_Invariants.txt` Rule #5; `docs/INVENTIONS.md` #24; [Research: Engine Measurements: Consensus writes](../Research/Engine.md#consensus-writes).

### 12.10 Keep recorded and calculated apart

- **In:** the attestations of 12.9.
- **Do:** a recorded row is deterministic transcription of what the source states. A calculated row, a parse, a classification, an engine evaluation, a circuit correlation, an inferred relation, names its analyzer identity and version, inputs, recipe, output relation and score domain, and execution receipt, and carries the calculation qualifier. Recorded and calculated sources may fold into a shared cell when they make the same proposition, but source trust and uncertainty remain available and they are never collapsed into one indistinguishable source. A calculated proxy never overwrites the literal outcome it estimates. Calculated testimony may be superseded or recomputed without deleting recorded evidence, and a newer analyzer competes as another witness unless a version policy scopes it out.
- **Out:** every row marked recorded or calculated, with its analyzer where calculated.
- **From:** `docs/specs/08_Record_vs_Calculate_Spec.txt`.

### 12.11 Keep dependence visible

- **In:** the attestations and their witnesses.
- **Do:** multiple paths and witnesses count only to the degree their evidence roots are independent. Lineage from 12.2, the shared source behind two mappings, and a calculation triggered by ten thousand games that produces one result under one generation are each one root. Provenance stays available so that duplicate dependence never masquerades as independent confirmation; a copied source pointed at by several paths is one witness.
- **Out:** the dependence roots each attestation folds under.
- **From:** `docs/INVENTIONS.md` #30; `docs/guides/chess-forward-pass-proof.md` §Dedup calculation, preserve occurrences.

### 12.12 Play the matchups

- **In:** the attestations of 12.9.
- **Do:** [13. Consensus](Consensus.md), as the rows arrive.

## The order of corpora

Two rules of the specification fix the order the corpora go in, and the order is part of the record.

1. **Referential integrity.** Every part of a claim is an entity, so every entity a claim names is recorded before the claim. There is no record ballooning: Laplace does not record that `dog` translates to `Hund`, that `dog` translates to `chien`, and so on for every pair; the word `dog` has an ILI, and you bubble up to it, change the language, and bubble down. So the identifiers other corpora point at, the ISO codes and the ILIs, come before the corpora that point at them; a lexicon comes before the mapping that joins it to another lexicon; a tag set comes before the treebank annotated with it; a sense inventory comes before the corpus whose tokens are tagged with its senses. The dependency order in force is in [9. Sources](Sources.md) operation 9.9.
2. **First in, first out.** As content is observed, first in, first out, the matchups are played, and a witness or claim entering for the first time starts from stock. So the order corpora arrive in changes standings, most trusted witness first, and a snapshot is reproducible only if attestations are applied in a deterministic order. Measured on 11,311 claims replayed in nine orders, the median spread of rating across orders was 0 and the 95th percentile 8.1.

Which corpus comes in which position follows from those two rules and from what each corpus references: [9. Sources](Sources.md) §The estate, and why each source is in it, gives every source, the reason it is ingested, what it must follow, and what waits for it.

See [Semantics](../Semantics/README.md), [Claims: Tuples](../Semantics/Claims.md#tuples), [Consensus: Matchups](../Semantics/Consensus.md#matchups), and [Research: Trust: Order of attestations](../Research/Trust.md#order-of-attestations).

## What this stage leaves behind

Witnesses with their lineage and trust class, claims as typed cells with their two IDs and their qualifier masks, collections for every set, and every attestation with its outcome, its dependence root, and whether it was recorded or calculated, in order.

## Without this stage

There are no semantics, no way to link concepts and languages, and nothing for a strand to tug back with.
