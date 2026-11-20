# 9. Sources

A source is admitted as one release, staged and qualified together, with every artifact given a disposition and none silently skipped; its identity is its trunk, `[source record, its files' trunks]`, so a release is its files and no name, version, or recipe is ever part of an ID.

A logical source has many releases, files, and sidecars. Laplace does not ingest a directory and it does not ingest a parser; it ingests a selected source generation, and the dataset refresh and the recipe work are one dependency chain, not sequential projects. A source is the trunk over its files, `[source record, its files' trunks in path order]`, and a release is its files: a new release has different files and so a different source trunk, and no name, version suffix, or recipe is ever part of an ID. The same sentence seen in two releases is one entity with two parents, one under each release's trunk.

## Before this stage

[8. Database](Database.md): the store the generation will be admitted into. [6. Registries](Registries.md): the trust class the witness is declared under.

## Operations, per source generation

### 9.1 Select the release

- **In:** the source's authority and its published releases.
- **Do:** choose the current release, not a legacy, old, broken, or deprecated one. The main files of a standard are the source of truth; the additional files are used where they carry information the main files lack: the UCD XML first, then the UAX #29 tests, the confusables, the security data. Stage the release outside the active tree; `staged` means not yet activated into the selected world generation, and it does not mean ignore the staged release while designing semantics against the superseded active one.
- **Out:** a staged release.
- **From:** `docs/plan/INGEST_BOUNDARY_AND_RECIPE_LAW.md` §Source-generation dependency law and §Concrete source-estate evidence; `docs/INVENTOR_RECORD.md` §Decomposition.

### 9.2 Enumerate the artifact graph with dispositions

- **In:** the staged release.
- **Do:** enumerate every physical artifact: file, archive member, sidecar, object. Each gets an explicit disposition: admitted, equivalent packaging, superseded, excluded with reason, or unsupported with why not. Silent non-enumeration is invalid. An artifact owns its identity, provenance, journal and resume accounting, and complete-coverage disposition; it can contain zero, one, or many source-format objects.
- **Out:** the exact artifact graph, every member dispositioned.
- **From:** `docs/OPERATING_SEQUENCE.md` §1; `docs/plan/INGEST_BOUNDARY_AND_RECIPE_LAW.md` §Artifact boundary.

### 9.3 Recover the native schema with a qualified provider

- **In:** the artifact graph.
- **Do:** run the format's provider, [10. Recipes](Recipes.md) operation 10.2, over the staged artifacts to recover the source's own schema: its fields, records, spans, ordinals, and the errors and ambiguities the provider reports. The provider is the irreducible parser, codec, or standards reader; it owns exact decode and container unpacking, grammar parsing, field and span extraction, the source-specific academic mapping declarations, its own identity and version, and exact inverse or declared loss. It does not own an identity rule, a Unicode ladder, a Merkle law, a scheduler, a persistence protocol, batch cardinality as identity, a search engine, or a silent fallback from unknown field meaning to content.
- **Out:** the native schema the recipe must disposition completely.
- **From:** `docs/plan/INGEST_BOUNDARY_AND_RECIPE_LAW.md` §Source-provider ownership.

### 9.4 Name the witness

- **In:** the source's record and its files.
- **Do:** a source is the witness of its observations: WordNet did not invent `dog`, it observed that `dog` is a noun. The witness is the source trunk, `[source record, its files' trunks in path order]`, the same trunk that is the source's identity. Provenance, where content came from, is containment under the trunk: each record the source asserts is a path over its claims inside its file's content tree, so the trunks that hold a claim are found by walking up from it, and the trunk is complete once the last file is decomposed, however early the claims stream. Attestations are what the source claims (WordNet says `dog` is a noun), and they are recorded per claim, witness, and lineage in the `attestation` table, with `games`, `tokens`, `score`, `position`, and `trust`; there is no separate witness table, the witness is the trunk ID, and a witness is known when it has attestations. The source's own name, `Open Multilingual Wordnet` or `omw-fr`, and its release are content inside its source record, never a salted witness ID. Multi-author umbrella collections such as Universal Dependencies (353 treebanks across 186 languages) and Open Multilingual Wordnet (32 language lexicons) group independently curated sub-corpora under a parent collection: individual UD treebanks (`UD_English-EWT`, `UD_Japanese-GSD`) and individual OMW lexicons (`omw-fr`, `omw-ja`) may be admitted as independently replaceable and corroborating sub-source trunks under the parent collection trunk, sharing a `lineage` root only when one actually derives from another (such as OEWN and Princeton WordNet sharing `WordNet` lineage), so `laplace forget` can replace a single updated treebank or lexicon without dropping the entire collection and independent treebanks corroborate shared grammatical claims. By contrast, individual annotators, crowd workers, speakers, and game players named inside a single dataset (such as ToxiGen, Social Bias Frames, or a PGN archive) are participant entities recorded inside each record—as White and Black are in a chess game—never separate witnesses: the corpus trunk witnesses that those participants rated or played the record so, never that an unsafe statement is true. A file's trunk is its content alone: its relative pathname within the source, its filename, and its bytes' tree, with no host path, OS record, timestamp, or binary digest (`src/file_metadata.c`, `recipes/file.recipe`), so the same source produces the exact same witness trunk on every machine. Record causal `lineage` where one witness derives from another so copied datasets do not double-count as independent consensus, while keeping independent witnesses in the same trust class distinct ([13. Consensus](Consensus.md) operation 13.3). Assign the trust class from [6. Registries](Registries.md) operation 6.5: Unicode and ISO 639-3 are `StandardsDerived`; OEWN, OMW, CILI, and UD are `AcademicCurated`; Wiktionary is `UserCuratedResource`; OpenSubtitles is `StructuredCorpus`. ISO 639 is each authority's own corpus and witness: the Library of Congress's ISO 639-2, SIL's ISO 639-3, IANA's language subtag registry, Unicode's CLDR supplemental data, and Glottolog.
- **Out:** the witness trunk (and any sub-source trunks under a collection), with its causal `lineage` and trust class carried on its attestation rows.
- **From:** `docs/plan/ASSIMILATION_ROADMAP.md` laws 1 and 8 and workstream H; [Attestations: Witnesses](../Semantics/Attestations.md#witnesses); [12. Attestations](Attestations.md) operations 12.2 and 12.3.

### 9.5 Declare the source profile

- **In:** the schema of 9.3 and the witness of 9.4.
- **Do:** before activation, the generation declares at least: artifact and release authority; provider, grammar, or codec identity; artifact and source-object framing; canonical composition and occurrence grain; the disposition of every field and structural role; ordering and multiplicity semantics; reference namespaces; provenance and testimony rules; normalization and canonicalization rules; inverse reconstruction or declared loss; the legal physical-plan dimensions; qualification fixtures; a physical-plan invariance receipt; and a coverage and amplification receipt. This is the semantic profile; a resource-sizing record is not it.
- **Out:** the source profile, bound to this exact staged release.
- **From:** `docs/plan/INGEST_BOUNDARY_AND_RECIPE_LAW.md` §Required source-profile fields.

### 9.6 Write the recipe against the staged release

- **In:** the profile of 9.5.
- **Do:** [10. Recipes](Recipes.md), for this source, against this release. Do not extend a bespoke decomposer against a superseded source merely because that directory is still the active path, and do not switch the active path to a release whose provider and recipe cannot yet account for its native fields.
- **Out:** a recipe qualified against these artifacts.
- **From:** `docs/plan/INGEST_BOUNDARY_AND_RECIPE_LAW.md` §Source-generation dependency law.

### 9.7 Qualify: disposition, reconstruction, invariance

- **In:** the recipe and the fixtures.
- **Do:** prove complete field and role disposition, with no field silently dropped or coerced to content; prove reconstruction or the declared loss; and prove physical-plan invariance: for the same artifact, provider, and recipe, vary the read buffer size, the parser feed chunk, the record batch, the native batch, the probe batch, the worker count and affinity, the scheduling order where source order is preserved, the COPY and apply batch, and the cache warm or cold state, and require that canonical ids, Merkle composition, trajectories with their ordinals, gaps, and multiplicity, occurrences, references, testimony ids and observation cardinality, provenance coordinates, deterministic calculation results, and reconstruction output are identical. Only time, CPU, RSS, I/O, WAL, cache behaviour, batch sizes, temporary staging, and worker scheduling may differ.
- **Out:** the invariance and coverage receipts.
- **From:** `docs/plan/INGEST_BOUNDARY_AND_RECIPE_LAW.md` §Physical-plan invariance and §Measured counterexample.

### 9.8 Activate release and recipe together

- **In:** the receipts of 9.7.
- **Do:** activate the release and the recipe as one selected source generation. Runtime source selection binds the entire artifact graph to authority, release, provider configuration, semantic recipes, and exact artifact identities; a single field map is one artifact recipe and cannot stand in for a complete logical source.
- **Out:** the active source generation.
- **From:** `docs/plan/INGEST_BOUNDARY_AND_RECIPE_LAW.md` §Source-provider ownership.

### 9.9 Derive the order from what each source references

- **In:** every active generation.
- **Do:** the order is not a list anyone supplies; it is read off the claims, and nothing depends on it for identity. Every node is content-derived, so what two sources say of one thing links by entity collision whichever is ingested first: a source that names a language code, a concept identifier, a sense, a frame, a role set, a part of speech, or a dependency label records that identifier as the content it is, and lands on the same node that the source that is its witness records, before or after. No placeholder node waits for another source, and no stand-in identity is ever replaced. Walk the references all the same: what each source's claims point at, and what points at this source, place it in the estate. The result, and the reason each source is in the estate at all, is [the estate](#the-estate-and-why-each-source-is-in-it) below. First in, first out then fixes standings, so within a tier the higher trust class goes first.
- **Out:** the admission order, derived.
- **From:** [Claims: Tuples](../Semantics/Claims.md#tuples); [12. Attestations](Attestations.md) §The order of corpora; `docs/plan/ASSIMILATION_ROADMAP.md` workstream H.

### 9.10 Run the common admission machine

- **In:** the active generation, in its turn.
- **Do:** [11. Content](Content.md) and [12. Attestations](Attestations.md). Source-specific code remains only the irreducible recovery kernel; the common spine owns everything after it. One ingest at a time.
- **Out:** the source admitted.
- **From:** `docs/specs/06_Engineering_Ruleset.txt` Rule #8 and §Operational constraints.

## The estate, and why each source is in it

Each row is one source generation: what the forward program cannot do without it, the predicates and tier it attests, what it references, and what references it. The tiers are the order the estate is admitted in, read off those references; within a tier the higher trust class is admitted first. Identity depends on no order: every node is content-derived, and sources link by entity collision whichever comes first ([9.9](#99-derive-the-order-from-what-each-source-references)). Any content entity may serve as a claim predicate without C manifest edits ([6. Registries](Registries.md) operation 6.1), while enumerated grammatical and lexical codes set their 64-bit `mask` slots (`manifest/banks.tsv`) and `highway.bin` crosswalks. Developer handles below name the semantic propositions and trust classes each source contributes; none is a fabricated ID.

### Tier 0. The floor

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| Unicode Character Database 17.0 | Every codepoint's properties, the segmentation classes UAX #29 breaks all text with, the collation the S³ order is built from, the case mappings that link `King` to `king`, the decompositions and normalization forms. Nothing composes without it. | at tier 0: `HAS_GENERAL_CATEGORY`, `HAS_SCRIPT`, `USES_SCRIPT_EXTENSION`, `HAS_BLOCK`, `HAS_AGE`, `HAS_NAME`, `HAS_BIDI_CLASS`, `HAS_MIRROR`, `HAS_LINE_BREAK`, `HAS_EAST_ASIAN_WIDTH`, `HAS_JOINING_TYPE`, `HAS_COMBINING_CLASS`, `HAS_NUMERIC_TYPE`, `HAS_NUMERIC_VALUE`, `HAS_EMOJI_PROPERTY`, `HAS_CHARACTER_PROPERTY`, `CONFUSABLE_WITH`, `HAS_CASE_MAPPING`, `DECOMPOSES_TO`, `NORMALIZES_TO`, `HAS_NORMALIZATION_FORM`, each variant a qualifier | nothing | everything | StandardsDerived, named in the registry |

### Tier 1. Identifiers other sources point at

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| SIL's ISO 639-3 | The identity of a language. Every lexicalization is `[lemma, language, concept]`, every treebank names its language, every subtitle pair names two; without language identities there is no language filter, no bubbling from `[dog, eng, ?]` up and `[?, deu, ?]` down, and `gift` in English and `Gift` in German would be one claim. Each authority in this tier is a corpus of its own. No code is normalized: each is recorded as its corpus writes it, a highway node of the language road class, and `en` and `eng` are joined by the 2↔3-letter link a corpus attests. | `IS_LANGUAGE_CODE`; `HAS_NAME`; `HAS_LANGUAGE_SCOPE`; `HAS_LANGUAGE_TYPE`; `MEMBER_OF_MACROLANGUAGE`; `SUPERSEDED_BY` with its retirement reason; the equivalent 639-2 and 639-1 codes as attested links | Unicode | every source that names a language | StandardsDerived, named in the registry |
| The Library of Congress's ISO 639-2, with the 2-letter codes of 639-1 and the families and groups of 639-5 | The bibliographic and terminology codes, the 2-letter codes and their 3-letter equivalents, and the English and French names, from the registration authority. | the 2↔3-letter links and the bibliographic and terminology equivalences as attested relations, `HAS_EXTERNAL_ID` with qualifiers iso639-1, iso639-2b, iso639-2t; `HAS_NAME` | Unicode | every source that writes a 2-letter or a 639-2 code | StandardsDerived, named in the registry |
| IANA's language subtag registry | The BCP 47 subtags that tags such as `en-GB` and `zh-Hant` are built from, with their preferred values, deprecations, and macrolanguages. | `HAS_EXTERNAL_ID` with qualifier bcp47; the macrolanguage and preferred-value relations as attested relations | Unicode | every source that writes a language tag | StandardsDerived, named in the registry |
| Unicode's CLDR supplemental data | The 2↔3-letter language aliases, the likely subtags, and the languages of each territory. | the aliases and likely subtags as attested relations | Unicode | language tags, places | StandardsDerived, named in the registry |
| Glottolog | Languages, dialects, and families as Glottolog classifies them, with their ISO 639-3 codes. | the classification and its links to ISO 639-3 codes as attested relations | Unicode | language families, languages ISO 639 does not code | not yet named; no recipe reads it yet |
| CILI | The interlingual index: one language-neutral concept identifier per meaning, `i46360` for the dog, which is content, `[i,4,6,3,6,0]`, the same entity wherever that text occurs; that it is an ILI is what CILI attests. It is the highway: bubble up from a word in one language to the ILI, change the language, bubble down, in two indexed lookups. Facts about the concept are language-neutral, so every lexicon's evidence on one claim lands in one cell. | that each identifier, `i46360`, is an ILI, said of that highway node and never as an external key of something else; `HAS_DEFINITION`, which is Princeton's; `HAS_BASE_CONCEPT_STATUS`; the maps to WordNet 3.0 and 3.1 offsets, those releases' internal pointers, by which each release's synsets resolve to their ILI; the offsets are not recorded | Unicode, ISO 639 | every wordnet, Wiktionary's translations, word-sense evaluation, the predicate mappings | AcademicCurated, named in the registry, lineage WordNet |

### Tier 2. Lexicons: what words mean

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| Open English WordNet 2025+ | The current English sense inventory: which senses a word has, the definition and examples of each, part of speech, hypernymy, meronymy, antonymy, the relations a hop follows. `[dog, eng, i46360]` and `[dog, NOUN]` are read from it; synsets not yet assigned a CILI `i*` number (`ili="in"`) keep their stable `oewn-*` synset ID as their concept node until CILI maps them ([10. Recipes](Recipes.md) operation 10.11). | sense bindings (`[lemma, eng, concept]`), parts of speech, definitions, examples, hypernymy, instance-of, meronymy (`part`, `member`, `substance`), antonymy, synonymy, similarity, `also_see`, attributes, derivational relations, pertainyms, entailment, causation, participles, domain qualifiers, verb groups, and verb frames on words and concept nodes | CILI, ISO 639 | OMW, Wiktionary, ConceptNet, the sense-tagged corpora, every read that asks what a word means | AcademicCurated, named in the registry, lineage WordNet |
| Open Multilingual Wordnet 2.0, 32 lexicons | The same senses lexicalized in 32 languages (`chien`, `犬`, `perro`, `cane` all binding to `i46360`), making translation an indexed read. Admitted under the OMW collection with individual language lexicons (`omw-fr`, `omw-ja`, …) replaceable and independently corroborating unless sharing causal lineage. | sense lexicalizations and parts of speech per language, definitions and examples where a lexicon carries them, explicit lexical gaps | CILI, ISO 639, OEWN for shared synsets | translation, cross-language reads | AcademicCurated, named in the registry |
| Princeton WordNet 3.0 | The compatibility coordinate older mappings write against: sense keys and 3.0 offsets that PredicateMatrix, MapNet, SemCor, VerbNet, and CILI's maps still use, plus empirical `cntlist` (`tag_cnt`) sense frequencies. Shares `WordNet` lineage with OEWN so shared lexical claims are not double-counted as independent witnesses. | 3.0 byte offsets and sense keys resolved through `highway.bin` to the concepts and lexicalizations they address; empirical sense frequency (`tag_cnt`) preserved as frequency/token evidence for sense disambiguation | CILI | the mapping resources and the sense-tagged corpora | AcademicCurated; shared `WordNet` lineage with OEWN |

### Tier 3. Predicates and their arguments

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| PropBank 3.4 frames | Every predicate's role sets, `bite.01`, and its numbered arguments: who did what to whom, the shape a sentence's verb imposes on its dependents. | each role as an n-ary claim inside its roleset, the roleset `bite.01` as PropBank writes it, with each differently named attribute of the role one edge; `ROLE_CORRESPONDS_TO` for the links to VerbNet and FrameNet; `HAS_EXAMPLE` | Unicode, ISO 639, the wordnets for sense links | SemLink, VerbAtlas, PredicateMatrix, semantic role reads | AcademicCurated, named in the registry |
| VerbNet 3.4 | Verb classes with their thematic roles, Agent, Patient, and syntactic frames; the class a verb belongs to constrains what its arguments can be. | `MEMBER_OF_VERBNET_CLASS`, `HAS_THEMATIC_ROLE`, `HAS_VERB_FRAME`, `INHERITS_FROM` for subclasses; members' WordNet sense keys, internal pointers resolved through the highway perf-cache to the lexicalizations they address and not recorded | PropBank, the wordnets | SemLink, PredicateMatrix | AcademicCurated, named in the registry |
| FrameNet 1.7 | Frames, `Cause_harm`, and their elements: the situation a word evokes and the roles in it, with frame-to-frame relations, Inheritance, Using, Precedes, Causative_of, that a hop can follow between situations. | `EVOKES_FRAME`, `HAS_FRAME_ELEMENT`, `HAS_SEMANTIC_TYPE`, `HAS_VALENCE_PATTERN`, `INHERITS_FROM`, `FRAME_USES`, `PERSPECTIVE_ON`, `PRECEDES`, `CAUSATIVE_OF`, `INCHOATIVE_OF`, `ALSO_SEE`, `HAS_SUBEVENT`; the annotated full-text as content with its annotation layers | Unicode, ISO 639, the wordnets | SemLink, MapNet, FrameBase, WordFrameNet | AcademicCurated, named in the registry |

### Tier 4. The Linguistic Super Highway: the mappings between resources

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| SemLink 2 | The curated joins PropBank to VerbNet and VerbNet to FrameNet, plus annotated instances, so a role set, a class, and a frame that mean the same are one claim across three witnesses rather than three disconnected nodes. | `CORRESPONDS_TO` between role sets, classes, and frames; `ROLE_CORRESPONDS_TO` between their roles | PropBank, VerbNet, FrameNet | reads that cross from one predicate resource to another | AcademicCurated, named in the registry |
| PredicateMatrix 1.3 | 426,696 rows tying each predicate to VerbNet, FrameNet, PropBank, WordNet, and MCR identifiers, with Catalan and Spanish lexicalizations on the same rows: one hop from `bite%2:35:00` to `i28957`, `18.2`, `Taking`, `bite.01`. Superseded in coverage, retained until its distinct fields are covered elsewhere. | the row as a claim across the identifiers, one witness; its errors, `bite` to `Arriving`, stay one witness's | the wordnets, PropBank, VerbNet, FrameNet | reads that need the older join | AcademicCurated |
| MapNet 0.1 | FrameNet frames and lexical units mapped to WordNet synsets, 5,162 lines, against FrameNet 1.3 and WordNet 1.6; retained only until FrameBase and SemLink cover it. | frame-to-synset, lexical-unit-to-synset | FrameNet, Princeton WordNet | none once superseded | AcademicCurated |
| VerbAtlas 1.1 | Verb frames over BabelNet synsets with a PropBank mapping: another witness of which verbs share a frame. | synset-to-frame, PropBank-to-VerbAtlas | the wordnets, PropBank | reads over verb frames | AcademicCurated |
| WordFrameNet | Word-to-frame files against older releases; retained until covered. | word-to-frame | FrameNet, the wordnets | none once superseded | AcademicCurated, provenance unknown |
| FrameBase 2.0 | FrameNet's frames as a schema graph with instances, the modern coverage that retires MapNet and WordFrameNet. | frame schema and instance claims | FrameNet, the wordnets | frame reads at scale | AcademicCurated |

### Tier 5. Annotated text: what a treebank says of each word

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| Universal Dependencies 2.18, 353 treebanks, with its documentation pages and its validator's data | Standing and empirical token counts across 353 treebanks in 186 languages (`[word, NOUN]`, `[word, lemma]`, dependency and feature layers), plus UD's validator lists (`upos.json`, `deprels.json`, `feats.json`) and documentation definitions. Individual treebanks (`UD_English-EWT`, `UD_Japanese-GSD`, …) can be updated, forgotten, and corroborated as independent sub-source trunks under the UD collection, and every annotated token occurrence preserves its real empirical count (`games` / `tokens`, never flattening 800 occurrences to 1) so [18. Firmware](Firmware.md) operation 18.8 weights content words over stop-words both in context and via word-level POS fallback. | word-level `upos` (`[dog, NOUN]`, including single-codepoint Tier-0 words like `[a, DET]` and `[I, PRON]`) with full empirical token counts; lemma claims; sentence-level `UPOS`, `DEPREL`, and feature annotation layers composed hierarchically; `SpaceAfter` carried natively in the sentence trajectory; documentation definitions for every UPOS, dependency relation, and feature value | Unicode, ISO 639 | contextual and fallback POS role weights, the fillers filter, grammatical relation coupling, word-sense evaluation, Wiktionary's parts of speech | AcademicCurated, named in the registry |
| WSD evaluation framework: SemCor and the five test sets | Sense-tagged usage: 226,036 instances whose gold sense keys map through CILI/`highway.bin` to concept nodes, preserving empirical sense-tag occurrence counts (`games` / `tokens` and `tag_cnt`) alongside sentence co-occurrence trajectories and held-out evaluation benchmarks. | sense-tagged occurrences and empirical sense counts on lexicalizations, plus sentence trajectories; ephemeral instance pointers (`d000.s000.t000`) resolve at ingest and are recorded nowhere | the wordnets, CILI, UD | sense disambiguation and empirical sense priors in [18. Firmware](Firmware.md) and [20. Forward](Forward.md) | AcademicCurated |

### Tier 6. The user-curated lexicon

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| Wiktionary, the 2026-08-28 raw Wiktextract | Every word in every language with its parts of speech, senses, glosses, forms, pronunciations, etymologies, and translations: the breadth the academic lexicons lack, `Butler` the surname whose etymology leads to `butler`, German bindings that OMW does not carry, morphological analyses as collections. Witness is the extraction program, lineage Wiktionary. | `HAS_POS`, `HAS_DEFINITION`, `HAS_EXAMPLE`, `FORM_OF`, `HAS_FEATURE` as a collection, `TRANSCRIBES_AS` as a collection, `HAS_USAGE_REGISTER` as a collection, `HAS_ETYMOLOGY`, `BORROWED_FROM`, `INHERITED_FROM`, `IS_TRANSLATION_OF`, `HAS_SENSE` where a key exists | Unicode, ISO 639, the UD vocabularies, CILI where a sense has a key | ConceptNet, whose lineage it is; the fillers filter; translation coverage | UserCuratedResource, named in the registry |

### Tier 7. Commonsense: what is said between terms

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| ConceptNet 5.7 | 34 million edges in 50 relations, `IsA`, `AtLocation`, `UsedFor`, `Causes`, `CapableOf`, with each edge carrying its sources and a weight: the test bed for witness and consensus modelling, including explicit negative assertions (`NotDesires`, `NotCapableOf`, `NotHasProperty`, `NotUsedFor`). Every edge folds under its upstream source `lineage` (Wiktionary, DBpedia, contributors), so a copied edge is not counted as an independent second witness. | positive content predicates (`is a`, `at location`, `causes`, `used for`, `capable of`, `has part`, `has property`, `antonym`, …), with negative ConceptNet relations (`NotDesires`, `NotCapableOf`, `NotHasProperty`, `NotUsedFor`) lowered to **refutation outcomes (`LOSS` / score `< 0.5`) on the positive predicate**—never `NOT_*` string relations ([6. Registries](Registries.md) operation 6.1) | Unicode, ISO 639, Wiktionary, the wordnets it imports | usage reads that need commonsense relations no lexicon states | UserCuratedResource, named in the registry |
| ATOMIC 2020 | 1.2 million human-authored if-then tuples, `xWant`, `xEffect`, `HinderedBy`, about events and people: what follows from what, the natural witness-count test, since 64,569 tuples appear more than once. | event-consequence predicates (`xWant`, `xEffect`, `xNeed`, `xAttr`, `xIntent`, `xReact`, `xReason`, `oWant`, `oEffect`, `oReact`, `ObjectUse`, `xFilledBy`, `isBefore`, `isAfter`, `HinderedBy`, `Desires`, `Causes`), with `NotDesires` lowered to a refutation outcome on `Desires` rather than a `NOT_*` predicate | Unicode, ISO 639 | reads about consequences and intent | AcademicCurated, named in the registry's examples by kind |
| ATOMIC10x | The machine-generated ten-times set, admitted as a separate witness at a model's trust, never as a transparent replacement for the human set. | the same relations, under its own witness | ATOMIC 2020's vocabulary | none | AIModelProbe, by the registry's rule for machine-generated testimony |

### Tier 8. Usage: whole sentences and texts

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| Tatoeba 2026-08-29 | Millions of sentences in hundreds of languages with which sentences translate which: sentence-level usage, precedes, gaps, and continuations across languages, and translation pairs as claims of whole sentences. It says nothing of a sentence's words one by one, so it attests at the sentence tier only. | `HAS_LANGUAGE` and `IS_TRANSLATION_OF` at the sentence; `HAS_RECORDING` for audio; author, tags, and lists as observations | ISO 639, and the lexicons whose words its sentences land on | continuation and gap reads across languages | UserCuratedResource, by the registry's rule for user-written sentences |
| OpenSubtitles v2024 | Parallel subtitle sentences per language pair, the largest conversational usage corpus: what is said, in what order, in speech. The language of sentences, not of words. | `HAS_LANGUAGE` at the sentence; the parallel alignment as `IS_TRANSLATION_OF` | ISO 639 | conversational continuation reads | StructuredCorpus, the registry's class for parallel text, which the roadmap ranks below Wiktionary |
| Project Gutenberg, 195 texts | Whole books as content: the corpus the prototype proved lossless recomposition, deduplication, occurrence counting, and gap and continuation reads on. Content, not a witness: it attests nothing, and its trajectories give `[Captain, ' ', ?]` in Moby Dick. | nothing; observations only | Unicode | container and gap reads, informativeness from container counts | none: content |

### Tier 9. Vocabularies of models

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| The tokenizers of the model farm | Each vocabulary as the path of its tokens in index order, each token as the text it stands for, so that a model's pieces resolve to shared content before the model is read: 2,700,090 tokens across 24 files deduplicated to 240,450 compositions and 11 distinct vocabularies. Ordinary content; it attests nothing. | nothing | Unicode | [24. Models](Models.md) | none: content |

### Tier 10. Places

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| GeoNames, the 2026-09-03 dump | Every place with its names in every language, its hierarchy, its feature class, and the country table with each country's capital: what answers "the capital of France", what a name in a sentence resolves to, and the alternate names that bind a place across languages. | multilingual names, administrative hierarchy, coordinates, feature and admin codes through their code tables, `[country, capital, city]` directly as a content-predicate claim requiring zero C manifest changes ([6. Registries](Registries.md) operation 6.1), and `geonameid` cross-dataset links where cited by external authorities such as Wikidata `P1566` or Natural Earth | ISO 639, Unicode | capital and geographic queries, place resolution across languages | UserCuratedResource / StructuredCorpus |
| Natural Earth 5.1 | Country and populated-place geometry with public-domain provenance: the shapes and points the names of GeoNames sit on. | geometry per place | GeoNames | map reads | StandardsDerived by kind, pending provenance verification |

### Tier 11. Harm

These are ingested last because they reference everything above and because of what they are for: Laplace knows what bad words are, what racism is, and that it is bad, so that it scores negatively, gets avoided, and reduces standing, rather than being ignorant of it. Governance is not deletion of knowledge.

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| HateCheck, and its multilingual and Singapore variants when pinned | Functional test cases with the labels ten annotators gave: hateful or not, by construction, per target and per functionality. | the case as content; the label as a claim of HateCheck, the witness, `IS_TYPED_AS` against the governed harm types, and which annotator gave which label as a relation HateCheck attests | Unicode, ISO 639 | the harm reads, and the refusal policy of firmware | AcademicCurated |
| Civil Comments | Two million comments with continuous toxicity labels and identity fields. | toxicity and identity labels as claims of the set, the witness | Unicode | harm standing at the sentence | AcademicCuratedWithUserInput |
| ToxiGen | Generated and human-annotated statements: one corpus witnessing its records, as a PGN is. The generator, a model and its prompt, and the annotators are participants recorded in each record, as White and Black are in a game. | that these annotators rated this statement so, and that this model generated it from this prompt, as relations of the one witness; never that a statement is true | Unicode | harm standing | AcademicCurated, the class of the one corpus that witnesses its records, [30. Conflicts](Conflicts.md) I9 |
| Measuring Hate Speech | Comments with annotator metadata and a continuous hate-speech measure. | the measure as a claim of the set, the witness, and each annotator's rating as a relation the set attests of that annotator | Unicode | harm standing | AcademicCurated |
| Social Bias Frames | Posts with the implied bias, the target group, and the offensiveness, as frames. | the frame's fields as claims | Unicode | harm reads that need the implication, not only the label | AcademicCurated |
| Social Chemistry 101 | Rules of thumb about social situations with their judgments: what people think is acceptable. | rules of thumb and judgments as claims | Unicode | the disposition policy of firmware | AcademicCurated |
| ProsocialDialog | Unsafe utterances with their reasons and the prosocial responses to them. | reasons and responses as claims | Unicode | realization under a refusal | AcademicCurated |
| RealToxicityPrompts | Prompts scored by a model for toxicity: admitted as model-scored evaluation evidence, never as human ground truth. | scores under the scoring model as a calculated witness | Unicode | evaluation only | AIModelProbe, the registry's class for a model's probed outputs |
| XSTest | Prompts that look unsafe and are safe: the test that a refusal policy does not over-refuse. | safe and unsafe labels | Unicode | the firmware's disposition policy | AcademicCurated |

### After the chain: the lanes

| Source | Why it is ingested | Stage |
| --- | --- | --- |
| The operational seed: `docs/INVENTION.md`, `docs/INVENTIONS.md`, and the canonical architecture documentation | The invention's own text as content under `SubstrateMandate` | [19. Pull](Pull.md) operation 19.8 |
| The model farm, Safetensors and GGUF | Circuits as source-scoped entities and graded claims under each model's witness (`raw_weight_bytes_retained = 0`) | [24. Models](Models.md) |
| TWIC through 1660, Lichess openings, Syzygy 3–5 men | Games as trajectories, openings as starting sequences, and tablebases as endings; `StructuredCorpus` for game collections, `StandardsDerived` for FIDE data and tablebases | [27. Chess](Chess.md) |
| Stockfish, pinned | Position and transition evaluations under a versioned provider, `DerivedCalculation` | [27. Chess](Chess.md) operation 27.4 |
| The tree-sitter grammar estate, The Stack v2, tiny-codes, and `.git` repositories | Grammars as parse providers, code and commit DAGs as content and compiler/LSP symbol witnesses | [26. Code](Code.md) |
| Wikidata, Wikipedia, and Natural Earth | Admitted via declarative `.recipe` files: Wikidata `Q*` items as shared cross-dataset highway entities (`Q937`, `Q142`) and `P*` properties (`P36` capital, `P1566` GeoNames ID) as open content predicates, Wikipedia for encyclopedic prose and links, and Natural Earth for public-domain geographic geometry | [9. Sources](Sources.md) operation 9.1, [10. Recipes](Recipes.md) |

The estate's physical state, which artifact is active, staged, superseded, or excluded and why, is `docs/source-estate.tsv` in the monorepo, and the current recipe headers in Laplace-Engine record the same order as this table.

## What this stage leaves behind

An estate of activated source generations, each a source trunk over its files, bound with its artifact graph, provider, and recipe, that trunk its witness, with a trust class and a lineage keyed by the trunk, and receipts proving that its admission does not depend on how it was physically run.

## Without this stage

Ingestion is fixed one corpus at a time forever, a batch size can change what exists, a superseded directory keeps being extended, and nothing says which files were skipped.
