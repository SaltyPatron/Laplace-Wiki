# 12. Attestations

Curated corpora are recorded as witnesses and claims, n-ary compositions of content IDs attached at the tier the source asserts them, with enumerated values as mask bits, sets as collections, and calculations marked as such.

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
- **Do:** entities are witnessed. WordNet does not own `dog`: we observe `dog` from WordNet. Every witness observes the same entity. The witness is the source trunk, `[source record, its files' trunks]`, from [9. Sources](Sources.md) operation 9.4; the source's own name is content inside its source record, never the witness's ID. Witnessing is not attribution, and both are containment. That an entity was witnessed means it was recorded in some tree; it is calculated, never stored: a walk up through the GIN gives every trunk that holds the entity, and its occurrence counts follow. Attribution is of a claim: a source asserted this strand, with an outcome. In the target the strand sits in a record path under the source's trunk, so attribution is a walk up too; until a working prototype proves that against the attestation table, attribution is the table's row. Attestations come from seeded corpora and from Laplace's own calculations and outcomes at their trust; ordinary content, a prompt among it, gives observations. If a witness is derived from another witness, record that lineage, keyed by the trunk ID, so copies do not count as independent consensus: Open English WordNet is derived from Princeton WordNet, so the two form one lineage, and a claim both attest gets one matchup with both witnesses in its witness set. The witnessing is mechanistic interpretability, auditability, and provenance. A witness may be a standards source, lexicon, corpus, document, user, tool, game, deterministic calculation provider, conventional model, or Laplace itself; the source and context remain attributable.
- **Out:** the witness record, with its lineage.
- **From:** [Attestations: Witnesses](../Semantics/Attestations.md#witnesses); `docs/INVENTION.md` §5; [Research: Semantics Experiments: Witnessed claims](../Research/Semantics-Experiments.md#witnessed-claims).

### 12.3 Set the witness's trust from its class

- **In:** the witness of 12.2.
- **Do:** the witness's trust class from [6. Registries](Registries.md) operation 6.5 is the only statement of its trust, and the class's prior seeds the standing of every claim it makes. Trust runs from MANDATE, 1.0, down through standards, academically curated datasets, user-curated corpora, models, user prompts, and responses, to 0 for the adversarial and to −1 for the reliably wrong. A witness entering for the first time starts from the stock default for its level: the source's trust, stability, and uncertainty. Trust is played as the opponent's deviation in [13. Consensus](Consensus.md), so it is fixed here, before the first matchup. Relation rank is not trust and does not enter here.
- **Out:** the trust every claim from this witness will play at.
- **From:** [Consensus: Trust](../Semantics/Consensus.md#trust); [Consensus: Entry](../Semantics/Consensus.md#entry); `docs/plan/ASSIMILATION_ROADMAP.md` law 8 and workstream A.

### 12.4 Ingest the corpus's files as content

- **In:** the corpus's files and their recipe.
- **Do:** [11. Content](Content.md), operations 11.1 to 11.14. Every label the corpus uses, `dog`, `noun`, `i46360`, `eng`, `hypernym`, is content and gets its entity here, and so is the source's own name, inside its source record. A corpus's annotation layers are content too: each sentence's part-of-speech sequence and dependency sequence hashed like compositions, so that small sub-structures share almost entirely while whole-sentence layers rarely repeat. A highway ID the corpus cites, a shared vocabulary other sources cite too, an ILI, a roleset, a VerbNet class, a FrameNet frame, a language code, is content like any other text, `i46360` is `[i,4,6,3,6,0]` exactly as `3.14159` is `[3,.,1,4,1,5,9]`, and every source that cites it lands on the same node; what kind of identifier it is, an ILI, is attested by the source that says so. An internal pointer, how the corpus addresses its own records, a WordNet offset, a synset or sense id, a FrameNet number, a token number or `sent_id`, a sentence number, a row or line number, is decomposed by the source's own notation only for the facts it carries, `06975898-n` an offset and the part of speech `n`, resolved to the ID of what it points at, and not recorded, [10. Recipes](Recipes.md) operation 10.11.
- **Out:** every entity the corpus's claims will name.
- **From:** [Claims: Tuples](../Semantics/Claims.md#tuples); `docs/plan/ASSIMILATION_ROADMAP.md` law 6; [Research: Semantics Experiments: Annotation layers as content](../Research/Semantics-Experiments.md#annotation-layers-as-content).

### 12.5 Form each claim as a composition of entities

- **In:** the entities of 12.4 and the recipe.
- **Do:** a claim is a tuple of entities with referential integrity: every part of a claim is an entity. `noun` is `[n,o,u,n]`, the same entity as the word "noun" anywhere else. Any tier's entity can be a predicate. A claim is a composition of content IDs of any arity and any tier; the `(subject, relation, object)` triple is one shape among many. A lexicalization is `[lemma, language, ILI]`, with the language a part of it and not a context column; a concept's part of speech is `[ILI, POS, n]`, with WordNet's `n` as written; a concept relation is `[ILI, hypernym, ILI]`; a role sits inside its roleset; a valence pattern is one claim. A relation, where a claim has one, is the content its source writes, indexed by the bit of [6. Registries](Registries.md) operation 6.1. Every source speaking about the same claim lands on the same cell. Each fact lands where the source asserts it, and "dog is a noun" exists in several shapes at once: WordNet says the concept is a noun and `dog` lexicalizes it, `[dog, eng, i46360]`, `[chien, fra, i46360]`; a treebank records one layer claim per sentence per layer, `[sentence, UPOS, layer]`, and what it says of the word by itself is the standing of `[dog, NOUN]`, one claim per pair, every tagging act a game; FrameNet's `dog.n` has the part of speech as a part; Wiktionary's English entry is a noun; and the bit on `dog`'s row is the filter. Nothing is blanketed across tiers it was not asserted at. Facts about the concept, `[i46360, hypernym, …]`, are language-neutral, so one consensus over every witness is correct; a cross-language homograph lexicalizes different concepts. An entity with a physicality can be the subject or object of any number of claims; that is the intended pattern. Relations are tied together by types and tiers: an ILI synset is a type, just like an IP segment is. An order, containment, or co-occurrence fact is never a claim; it is read from the trajectory.
- **Out:** the claims, as paths of entity IDs.
- **From:** [Claims: Tuples](../Semantics/Claims.md#tuples); `docs/specs/05_Substrate_Invariants.txt` Rules #3, #6; `docs/plan/ASSIMILATION_ROADMAP.md` workstream B; [Research: Semantics Experiments: Witnessed claims](../Research/Semantics-Experiments.md#witnessed-claims).

### 12.6 Hash each claim twice

- **In:** the claims of 12.5.
- **Do:** deterministic content determines a claim's ID. A claim is a limited path trajectory, so its hash is computed the same way as a composition's: from the IDs along its path. Witnessing and consensus are two different beasts: for witnessing, the hash covers the claim's specifics, the witness, context, and qualifiers; for consensus, the hash covers only the main components that make the claim unique, its composition, never a fixed subject, type, and object with a missing object filled with zeros. So each claim gets a witnessing ID and a consensus ID, and two witnesses attesting the same claim land on the same consensus ID.
- **Out:** the claim IDs.
- **From:** [Claims: IDs](../Semantics/Claims.md#ids); [Consensus: Deduplication](../Semantics/Consensus.md#deduplication).

### 12.7 Set the qualifier mask and the entity masks

- **In:** the claims of 12.5.
- **Do:** the attestation's 256-bit qualifier mask says which variants the source asserts, from the families of [6. Registries](Registries.md) operation 6.4: `eng HAS_EXTERNAL_ID eng {iso639-2b, iso639-2t, iso639-3}` is one claim with three bits; a case mapping carries `lower` or `upper`, `simple` or `full`; a name carries `primary` or `alias`. Qualifiers are OR-merged under aggregation. Calculated evidence carries the derivation/calculation qualifier. Bits are set where a source asserts them, at the tier it asserts them, and codes that mean the same set the same bit, whether a source wrote `n` or `NOUN`. Each entity carries OR-masks derived from those as a prefilter: `dog`'s part-of-speech mask is `NOUN|VERB`, and its highway mask has the bit of every relation it participates in. A mask is a filter; the actual score is a consensus read, and a mask miss is never authoritative absence. The mappings between curated resources, SemLink, PredicateMatrix, MapNet, WordFrameNet, and CILI, which link PropBank, VerbNet, FrameNet, WordNet, and ILIs to one another, are the Linguistic Super Highway, and the highway is part of the foundation behind the masks, the basis for which source codes mean the same bit: bubble up to the numerical identifier, and back down into any language.
- **Out:** the qualifier mask of each attestation and the masks of each entity.
- **From:** [Claims: Masks](../Semantics/Claims.md#masks); [Claims: The Linguistic Super Highway](../Semantics/Claims.md#the-linguistic-super-highway); `docs/plan/ASSIMILATION_ROADMAP.md` laws 5 and 7; `docs/INVENTOR_RECORD.md` §Relations.

### 12.8 Record each set-valued fact as one collection

- **In:** each set-valued field the recipe declared under [10. Recipes](Recipes.md) operation 10.12.
- **Do:** sort the members ascending by id and deduplicate, so the identity is order-independent; the bundle id is the Merkle hash over the sorted members; add the bundle as an entity of type Collection; add its physicality as a set trajectory over the sorted members, with its own physicality type and its own partial GIN, never widening the text-trajectory indexes; and add one attestation `(subject, relation, bundle)`. Canonical order for a set is ascending by member id, and that order is the deduplication mechanism, not a policy choice: every later form carrying `{nom, sg, masc}` re-stages the same id and writes nothing new. A collection is an entity with a Merkle id, a coordinate, and typed edges; not a CSV column, not a `text[]`, not JSON, not a bitmask, and a representation that cannot carry a rating is not a collection.
- **Out:** one entity and one edge per distinct member set.
- **From:** `docs/specs/38_Collections_Are_Compositions.md` §3, §4.

### 12.9 Record each attestation with its outcome

- **In:** the claims of 12.6 and the witness of 12.2.
- **Do:** attestations are a win, draw, or loss, and/or a score in [0, 1] with a draw at 0.5, so there are positive and negative attestations. Confirmation, draw, and refutation remain distinct; the absence of a row is unknown, never refutation. A denial is a refute outcome on the positive relation. Record each one as a row of the attestation table, with its qualifier mask. The target records each one by containment: the record is a path over the claims it asserts, inside its file's content tree under the source trunk, with each claim's run length and its outcome or score in its vertex's M, and many source trunks can hold the same strand, each found through the GIN. The standing of [13. Consensus](Consensus.md) is one metadata table keyed by the strand ID, beside the path, never on the GIN-indexed path row, where a non-HOT update would re-insert GIN entries for every vertex. Trust and lineage are keyed by the trunk ID. Containment is the target, proven side by side with the table first: the per-claim-and-witness attestation table stays until a working prototype on real data shows that containment answers everything the table answers today, who said a claim, its games, score, and position, its qualifiers, forgetting and replay, with nothing lost. As built, the Engine emits claims as events only, `say.c` `claim()` and `together()`, no entity made of the claims together, and keeps provenance only in `attestation`, a row of claim, witness, score, and position. Observed testimony is append-only; a correction adds new testimony and never erases the earlier witness. A witness that asserts the same claim n times, a corpus tagging the same word the same way in a thousand sentences, asserts it with run length n, read off the tree as the strand occurring in n records under its trunk, and plays one matchup on it per ingestion with n carried as the certainty of its assertion, never n games, [13. Consensus](Consensus.md) operation 13.4. Packaging is not repetition: a cross-product table layout, the Predicate Matrix's rows, or an automatic tagger's per-token output, FrameNet's BNC and PENN layers or Universal Dependencies EWT's mostly automatic UPOS, repeating one fact is not the source saying it again. A number the source states beside a claim, such as a witness's sense order or a usage count it writes, WordNet's `tag_cnt 10742`, is content, recorded as given beside the claim as an observation and not as games: merging a stated frequency into a standing loses it, because a standing measures whether a claim holds and saturates as its deviation shrinks. Ingest completion is operational state, never an attestation.
- **Out:** the attestations, rows of the attestation table, and in the target record paths under the source trunk, in the order the corpus gave them; [Corpora: Universal Dependencies](../Corpora/Universal-Dependencies.md) works a record through from the trunk to its strands.
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

Witnesses, each a source trunk, with their lineage and trust class keyed by the trunk, claims as compositions with their two IDs and their qualifier masks, collections for every set, and every attestation, a row of the attestation table and in the target a strand in a record path under its trunk, with its outcome, its dependence root, and whether it was recorded or calculated, in order.

## Without this stage

There are no semantics, no way to link concepts and languages, and nothing for a strand to tug back with.
