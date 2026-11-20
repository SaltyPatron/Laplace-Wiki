# 12. Attestations

Curated corpora are recorded as witnesses and claims, n-ary compositions of content IDs attached at the tier the source asserts them, with enumerated values as mask bits, sets as collections, and calculations marked as such.

Semantics are the relations Laplace records about entities, so that it can link concepts and languages and hop and fan out from anything to anything with integrity. Curated corpora give attestations; dozens of them are required, and this stage records what each one says, in order. A claim is "this source says X is, or is not, Y": the witness, the outcome, and the games.

## Before this stage

[11. Content](Content.md): every entity a claim will name. [8. Database](Database.md): the semantics tables. [6. Registries](Registries.md): the relations, qualifiers, trust classes, and vocabularies. [9. Sources](Sources.md) and [10. Recipes](Recipes.md): the witness and the claim declarations for each corpus.

## Operations, per corpus

### 12.1 Decide what the corpus attests

- **In:** the corpus.
- **Do:** a treebank, a dictionary, a thesaurus, or an encyclopedia is a different type of corpus from normal digital content: it states things about content. Curated corpora give attestations, observations, witnessing, usage, examples, and more. Decide what this corpus states, and at what tier: attestations are recorded at the exact compositional object the source asserts, never sprayed downward across sub-constituents. OpenSubtitles gives the language of whole sentences, not of individual words. Because Laplace's composition law collapses singletons (`n == 1 → child itself`), **every single-codepoint grapheme, word, symbol, or tag**—English `"a"` and `"I"`, Spanish `"y"`, CJK single-character words `"犬"` (dog) and `"水"` (water), single digits `"0"`..`"9"`, WordNet's POS code `"n"`—**is its Tier-0 codepoint entity**. While only Unicode attests universal character-encoding properties (`gc`, `sc`, `ccc`, case and decomposition mappings), lexicons, CILI mappings (`[犬, jpn, i46360]`), and treebanks (`[a, DET]`, `[I, PRON]`) naturally and lawfully attest lexical, sense, and part-of-speech claims directly on Tier-0 codepoint entities; no reader or writer may exclude `tier = 0` from lexical or grammatical claims. A corpus that states nothing, such as a novel or a tokenizer's vocabulary, is observed content under [11. Content](Content.md), not a semantic witness.
- **Out:** what this corpus's claims are about, and at which tier each attaches.
- **From:** [Attestations: Attestations](../Semantics/Attestations.md#attestations); `docs/INVENTIONS.md` #27; `docs/INVENTOR_RECORD.md` §Attestations.

### 12.2 Name the witness and its lineage

- **In:** the corpus.
- **Do:** entities are witnessed. WordNet does not own `dog`: we observe `dog` from WordNet. Every witness observes the same entity. The witness is the source trunk, `[source record, its files' trunks]`, from [9. Sources](Sources.md) operation 9.4; the source's own name is content inside its source record, never a salted witness ID. Multi-author umbrella collections (such as Universal Dependencies' 353 treebanks or Open Multilingual Wordnet's 32 language lexicons) may admit independently curated treebanks or lexicons as replaceable sub-source trunks under the parent collection trunk, corroborating shared claims unless they share a causal `lineage`. Witnessing is not attribution, and both are containment: walking up through the GIN finds every trunk that holds an entity, while claim attribution is recorded both as containment inside the asserting record path under the witness trunk and as a folded row per `(claim, witness, lineage)` in `attestation`. If a witness derives from another witness (Open English WordNet from Princeton WordNet, or a ConceptNet edge imported from Wiktionary), record that causal `lineage` so copies do not double-count as independent consensus ([13. Consensus](Consensus.md) operation 13.3). A witness may be a standards source, lexicon, treebank, corpus, user, deterministic calculation provider, assimilated model, or Laplace itself; provenance remains attributable end to end.
- **Out:** the witness trunk and its causal `lineage`.
- **From:** [Attestations: Witnesses](../Semantics/Attestations.md#witnesses); `docs/INVENTION.md` §5; [Research: Semantics Experiments: Witnessed claims](../Research/Semantics-Experiments.md#witnessed-claims).

### 12.3 Set the witness's trust from its class

- **In:** the witness of 12.2.
- **Do:** the witness's trust class from [6. Registries](Registries.md) operation 6.5 is the only statement of its trust, and the class's prior seeds the standing of every claim it makes. Trust runs from MANDATE, 1.0, down through standards, academically curated datasets, user-curated corpora, models, user prompts, and responses, to 0 for the adversarial and to −1 for the reliably wrong. A witness entering for the first time starts from the stock default for its level: the source's trust, stability, and uncertainty. The class's default is where the witness's own trust starts: its trust is its own rating, earned only through agreement or disagreement with independent witnesses and verified outcomes, never by repeating itself, and it bounds each of its votes in [13. Consensus](Consensus.md) operation 13.2. Relation rank is not trust and does not enter here.
- **Out:** the trust every claim from this witness will play at.
- **From:** [Consensus: Trust](../Semantics/Consensus.md#trust); [Consensus: Entry](../Semantics/Consensus.md#entry); `docs/plan/ASSIMILATION_ROADMAP.md` law 8 and workstream A.

### 12.4 Ingest the corpus's files as content

- **In:** the corpus's files and their recipe.
- **Do:** [11. Content](Content.md), operations 11.1 to 11.14. Every label the corpus uses, `dog`, `noun`, `i46360`, `eng`, `hypernym`, is content and gets its entity here, and so is the source's own name, inside its source record. A corpus's annotation layers are content too: each sentence's part-of-speech sequence and dependency sequence hashed like compositions, so that small sub-structures share almost entirely while whole-sentence layers rarely repeat. A highway ID the corpus cites, a shared vocabulary other sources cite too, an ILI, a roleset, a VerbNet class, a FrameNet frame, a language code, is content like any other text, `i46360` is `[i,4,6,3,6,0]` exactly as `3.14159` is `[3,.,1,4,1,5,9]`, and every source that cites it lands on the same node; what kind of identifier it is, an ILI, is attested by the source that says so. An internal pointer, how the corpus addresses its own records, a WordNet offset, a synset or sense id, a FrameNet number, a token number or `sent_id`, a sentence number, a row or line number, is decomposed by the source's own notation only for the facts it carries, `06975898-n` an offset and the part of speech `n`, resolved to the ID of what it points at, and not recorded, [10. Recipes](Recipes.md) operation 10.11.
- **Out:** every entity the corpus's claims will name.
- **From:** [Claims: Tuples](../Semantics/Claims.md#tuples); `docs/plan/ASSIMILATION_ROADMAP.md` law 6; [Research: Semantics Experiments: Annotation layers as content](../Research/Semantics-Experiments.md#annotation-layers-as-content).

### 12.5 Form each claim as a composition of entities

- **In:** the entities of 12.4 and the recipe.
- **Do:** a claim is a tuple of entities with referential integrity: every part of a claim is an entity. `noun` is `[n,o,u,n]`, the same entity as the word "noun" anywhere else. **Any content entity at any tier may serve as a predicate**—including GeoNames `capital`, Wikidata `P*` properties (`P36`), domain verbs, or user-authored recipe predicates—without requiring a C manifest edit or engine rebuild ([6. Registries](Registries.md) operation 6.1). A claim is a composition of content IDs of any arity and any tier; the `(subject, relation, object)` triple is one shape among many. A lexicalization is `[lemma, language, concept]`, with the ISO 639 language node a part of the composition (`[dog, eng, i46360]`, or `oewn-*` when `ili="in"`); a concept's part of speech is `[concept, POS, n]`; a concept relation is `[i46360, hypernym, …]`; a role sits inside its roleset; a valence pattern is one claim. Every source speaking about the same claim composition lands on the exact same `claim` `lp_id`. Each fact lands where the source asserts it: WordNet links `[dog, eng, i46360]` and `[chien, fra, i46360]`; a UD treebank records hierarchical sentence layers (`[sentence, UPOS, layer]`) and word-level POS claims (`[dog, NOUN]`, `[a, DET]`) carrying full empirical token counts; Wiktionary attests entries per language and POS; and the `upos` slot in `entity.mask` serves as an O(1) prefilter. Order, adjacency, gaps, and containment are never claims; they are read directly from `physicality.path`.
- **Out:** the claims, as ordered compositions of entity IDs.
- **From:** [Claims: Tuples](../Semantics/Claims.md#tuples); `docs/specs/05_Substrate_Invariants.txt` Rules #3, #6; [Research: Semantics Experiments: Witnessed claims](../Research/Semantics-Experiments.md#witnessed-claims).

### 12.6 Key consensus by claim `lp_id` and attestation by `(claim, witness, lineage)`

- **In:** the claims of 12.5.
- **Do:** deterministic content alone determines a claim's `lp_id`: it is composed and hashed identically to any other composition over its ordered constituent IDs, never `BLAKE3(subject || type || object)` with zero-padded missing slots. Two witnesses asserting the exact same proposition therefore produce the exact same `claim` `lp_id` and fold into the same row of `consensus(claim)`, while per-witness attribution, series counts, score, position, and trust are keyed on `(claim, witness, lineage)` in `attestation` alongside containment in the witness's record trajectories.
- **Out:** the canonical `claim` `lp_id` and `(claim, witness, lineage)` series key.
- **From:** [Claims: IDs](../Semantics/Claims.md#ids); [Reference: Schema](../Reference/Schema.md#the-four-tables); [30. Conflicts](Conflicts.md) T2.

### 12.7 Set the 64-bit `mask` banks

- **In:** the claims of 12.5 and `Laplace-Native/manifest/banks.tsv`.
- **Do:** set the 64-bit `bit(64)` acceleration fields on `physicality.mask` and `entity.mask` ([6. Registries](Registries.md) operation 6.2): `kind` row-role flags (`CLAIM`, `RECORD`, `TUPLE`, `FILE`) at offset 0, and governed enum slots (`upos`, `lexfile`, `deprel`, `vnrole`, `wnframe`, storing `slot + 1`) where a source asserts them at that tier, resolving source-specific tagsets (WordNet `n`, PTB `nns`, Brown `NN-TL`) through `highway.bin` crosswalks to the shared `upos` slot without altering the literal claim text. Masks are indexed alongside path constituents in the composite GIN (`physicality_paths`), turning filtered probes such as "claims holding `dog` with `kind = CLAIM`" into a single posting-list intersection; a mask is strictly an acceleration prefilter, never authoritative absence, and actual strength is always read from `consensus` and `attestation`.
- **Out:** `entity.mask` and `physicality.mask` (`bit(64)`).
- **From:** [Claims: Masks](../Semantics/Claims.md#masks); [Reference: Schema](../Reference/Schema.md#the-mask); [Reference: Types, masks and the highway](../Reference/Types.md#masks).

### 12.8 Record each set-valued fact as one collection

- **In:** each set-valued field the recipe declared under [10. Recipes](Recipes.md) operation 10.12.
- **Do:** sort the members ascending by id and deduplicate, so the identity is order-independent; the bundle id is the Merkle hash over the sorted members; add the bundle as an entity of type Collection; add its physicality as a set trajectory over the sorted members, with its own physicality type and its own partial GIN, never widening the text-trajectory indexes; and add one attestation `(subject, relation, bundle)`. Canonical order for a set is ascending by member id, and that order is the deduplication mechanism, not a policy choice: every later form carrying `{nom, sg, masc}` re-stages the same id and writes nothing new. A collection is an entity with a Merkle id, a coordinate, and typed edges; not a CSV column, not a `text[]`, not JSON, not a bitmask, and a representation that cannot carry a rating is not a collection.
- **Out:** one entity and one edge per distinct member set.
- **From:** `docs/specs/38_Collections_Are_Compositions.md` §3, §4.

### 12.9 Record each attestation with its outcome and empirical counts

- **In:** the claims of 12.6 and the witness of 12.2.
- **Do:** attestations carry an outcome—win (`1.0`), draw (`0.5`), or loss (`0.0`)—or a continuous score in `[0, 1]`, so positive and negative testimony remain distinct and the absence of a row means unknown, never refutation. A denial (`"hot is not cold"`, ConceptNet `NotDesires`) is a refute outcome on the positive claim, never a `NOT_*` predicate. Record each assertion both by containment—a record path over the claims it asserts inside its file's content tree under the source trunk, with `run`, `said` role, `outcome`, and `position` packed in each vertex's `M`—and as a folded series row `(claim, witness, lineage, games, tokens, score, "position", trust)` in `attestation`, while `consensus(claim)` sits off the GIN-indexed `physicality` heap for HOT in-place updates. **Preserve genuine empirical corpus counts rather than flattening 800 occurrences to 1 game:** when a UD treebank tags `dog` as `NOUN` across 800 sentence tokens or SemCor / WordNet records empirical sense-tagged occurrences (`tag_cnt`), those real corpus counts are preserved in `games` / `tokens` (and any explicit sense-frequency / sense-order claims) so `lp_attest_series` folds the series up to the witness's trust ceiling while [18. Firmware](Firmware.md) and [20. Forward](Forward.md) retain empirical token frequency to disambiguate common versus rare senses and parts of speech. Only artificial Cartesian join repeats inside a denormalized mapping file (such as a single lexical fact repeated across 20 unrelated join rows of PredicateMatrix) are deduplicated per logical assertion. Ingest completion is operational state, never an attestation.
- **Out:** record assertion paths under the source trunk plus folded `(claim, witness, lineage)` rows in `attestation` preserving `games` and `tokens`.
- **From:** [Attestations: Outcomes](../Semantics/Attestations.md#outcomes); [Reference: Ingest](../Reference/Ingest.md#records-and-the-series); `docs/specs/05_Substrate_Invariants.txt` Rule #5; `docs/INVENTIONS.md` #24.

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

1. **Referential integrity.** Every part of a claim is an entity, so every entity a claim names is recorded before the claim. There is no record ballooning: Laplace does not record that `dog` translates to `Hund`, that `dog` translates to `chien`, and so on for every pair; the word `dog` has an ILI, and you bubble up to it, change the language, and bubble down. Every entity is content-derived, so the source that names an identifier records it as the content it is, and what two sources say of one thing links by entity collision whichever is ingested first: identity is not order-dependent, and no placeholder node waits for another source. The estate still places the identifiers other corpora point at, the ISO codes and the ILIs, before the corpora that point at them; a lexicon before the mapping that joins it to another lexicon; a tag set before the treebank annotated with it; a sense inventory before the corpus whose tokens are tagged with its senses. That order is in [9. Sources](Sources.md) operation 9.9.
2. **First in, first out.** As content is observed, first in, first out, the matchups are played, and a witness or claim entering for the first time starts from stock. So the order corpora arrive in changes standings, most trusted witness first, and a snapshot is reproducible only if attestations are applied in a deterministic order. Measured on 11,311 claims replayed in nine orders, the median spread of rating across orders was 0 and the 95th percentile 8.1.

Which corpus comes in which position follows from those two rules and from what each corpus references: [9. Sources](Sources.md) §The estate, and why each source is in it, gives every source, the reason it is ingested, what it must follow, and what waits for it.

See [Semantics](../Semantics/README.md), [Claims: Tuples](../Semantics/Claims.md#tuples), [Consensus: Matchups](../Semantics/Consensus.md#matchups), and [Research: Trust: Order of attestations](../Research/Trust.md#order-of-attestations).

## What this stage leaves behind

Witnesses, each a source trunk, with their lineage and trust class keyed by the trunk, claims as open-ended content compositions with their canonical claim IDs and 64-bit masks, collections for every set, and every attestation—recorded both as a strand in a record path under its trunk and as a folded `(claim, witness, lineage)` series preserving empirical `games` and `tokens`—with its outcome, its causal dependence root, and whether it was recorded or calculated, in order.

## Without this stage

There are no semantics, no way to link concepts and languages, and nothing for a strand to tug back with.
