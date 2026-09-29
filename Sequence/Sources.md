# 9. Sources

A source is admitted only as one bound generation: authority, release, exact artifact graph, provider, and recipe, staged and qualified together, with every artifact given a disposition and none silently skipped.

A logical source has many releases, files, and sidecars. Laplace does not ingest a directory and it does not ingest a parser; it ingests a selected source generation, and the dataset refresh and the recipe work are one dependency chain, not sequential projects. Release and version participate in provenance identity, never in content identity: the same sentence seen in two releases is one entity with two release-attributable occurrences.

## Before this stage

[8. Database](Database.md): the store the generation will be admitted into. [6. Registries](Registries.md): the trust class the witness is declared under.

## Operations, per source generation

### 9.1 Select the release

- **In:** the source's authority and its published releases.
- **Do:** choose the current release, not a legacy, old, broken, or deprecated one. The main files of a standard are the source of truth; the additional files are used where they carry information the main files lack: the UCD XML first, then the UAX #29 tests, the confusables, the security data. Stage the release outside the active tree; `staged` means not yet activated into the selected world generation, and it does not mean ignore the staged release while designing semantics against the superseded active one.
- **Out:** a staged release.
- **Check:** the estate at 2026-09-19 had UD v2.17 active with 686 `.conllu` files and v2.18 staged with 712; OMW active as duplicated legacy trees of 1,455 files each and OMW 2.0 staged as 32 WN-LMF lexicons; recipe work targets the staged generation.
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

- **In:** the source's authority and release.
- **Do:** a source is the witness of its observations: WordNet did not invent `dog`, it observed that `dog` is a noun. The witness identity is the content composition `[authority, release]`; a curated source has one witness per lexicon, `[omw-fr, 2.0]`. Record the lineage where one witness is derived from another, so copies do not count as independent consensus. Assign the trust class from [6. Registries](Registries.md) operation 6.5: Unicode and ISO 639-3 are StandardsDerived; OEWN, OMW, CILI, and UD are AcademicCurated; Wiktionary is UserCuratedResource; OpenSubtitles is lower. A separate feed within a source, ISO 639-2 French names, CLDR, ISO 639-5, is its own witness.
- **Out:** the witness, its lineage, and its class.
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
- **Do:** prove complete field and role disposition, with no field silently dropped or coerced to content; prove reconstruction or the declared loss; and prove physical-plan invariance: for the same artifact, provider, and recipe, vary the read buffer size, the parser feed chunk, the record batch, the native batch, the probe batch, the worker count and affinity, the scheduling order where source order is preserved, the COPY and apply batch, and the cache warm or cold state, and require that canonical ids, Merkle composition, trajectories with their ordinals, gaps, and multiplicity, occurrences, typed references, testimony ids and observation cardinality, provenance coordinates, deterministic calculation results, and reconstruction output are identical. Only time, CPU, RSS, I/O, WAL, cache behaviour, batch sizes, temporary staging, and worker scheduling may differ.
- **Out:** the invariance and coverage receipts.
- **Check:** the OpenSubtitles defect is the counterexample: an arbitrary 512-pair batch participated in durable content-object construction, so changing the physical batch changed which identities existed.
- **From:** `docs/plan/INGEST_BOUNDARY_AND_RECIPE_LAW.md` §Physical-plan invariance and §Measured counterexample.

### 9.8 Activate release and recipe together

- **In:** the receipts of 9.7.
- **Do:** activate the release and the recipe as one selected source generation. Runtime source selection binds the entire artifact graph to authority, release, provider configuration, semantic recipes, and exact artifact identities; a single field map is one artifact recipe and cannot stand in for a complete logical source.
- **Out:** the active source generation.
- **From:** `docs/plan/INGEST_BOUNDARY_AND_RECIPE_LAW.md` §Source-provider ownership.

### 9.9 Derive the order from what each source references

- **In:** every active generation.
- **Do:** the order is not a list anyone supplies; it is read off the claims. Every part of a claim is an entity, so a source that names a language code, a concept identifier, a sense, a frame, a role set, a part of speech, or a dependency label cannot be admitted before the source that is the witness of that identifier. Walk the references: what each source's claims point at must already exist, and what points at this source waits for it. The result, and the reason each source is in the estate at all, is [the estate](#the-estate-and-why-each-source-is-in-it) below. First in, first out then fixes standings, so within a tier the higher trust class goes first.
- **Out:** the admission order, derived.
- **From:** [Claims: Tuples](../Semantics/Claims.md#tuples); [12. Attestations](Attestations.md) §The order of corpora; `docs/plan/ASSIMILATION_ROADMAP.md` workstream H.

### 9.10 Run the common admission machine

- **In:** the active generation, in its turn.
- **Do:** [11. Content](Content.md) and [12. Attestations](Attestations.md). Source-specific code remains only the irreducible recovery kernel; the common spine owns everything after it. One ingest at a time.
- **Out:** the source admitted.
- **From:** `docs/specs/06_Engineering_Ruleset.txt` Rule #8 and §Operational constraints.

## The estate, and why each source is in it

Each row is one source generation: what the forward program cannot do without it, the relations and tier it attests, what it references and therefore what it must follow, and what waits for it. The tiers are the dependency order; within a tier the higher trust class is admitted first. Trust classes are the registry's of [6. Registries](Registries.md) operation 6.5, and where the registry names the class the row says so.

### Tier 0. The floor

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| Unicode Character Database 17.0 | Every codepoint's properties, the segmentation classes UAX #29 breaks all text with, the collation the S³ order is built from, the case mappings that link `King` to `king`, the decompositions and normalization forms. Nothing composes without it. | at tier 0: general category, script, block, age, name, bidi, line break, segmentation classes, `HAS_CASE_MAPPING`, `DECOMPOSES_TO`, `NORMALIZES_TO`, each variant a qualifier | nothing | everything | StandardsDerived, named in the registry |

### Tier 1. Identifiers other sources point at

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| ISO 639-3, 639-2, 639-5, the IANA subtag registry | The identity of a language. Every lexicalization is `[lemma, language, concept]`, every treebank names its language, every subtitle pair names two; without one language identity there is no language filter, no bubbling from `[dog, eng, ?]` up and `[?, deu, ?]` down, and `gift` in English and `Gift` in German would be one claim. All codes normalize to 639-3 at ingest. | `HAS_EXTERNAL_ID` with qualifiers iso639-1, iso639-2b, iso639-2t, iso639-3, bcp47; `HAS_NAME`; `HAS_PART` for macrolanguages; `SUPERSEDED_BY` with its retirement reason | Unicode | every source that names a language | StandardsDerived, named in the registry |
| CILI | The interlingual index: one language-neutral concept identifier per meaning, `i46360` for the dog, bound to content only by witnessed claims. It is the highway: bubble up from a word in one language to the ILI, change the language, bubble down, in two indexed lookups. Facts about the key are language-neutral, so every lexicon's evidence folds into one cell. | `HAS_EXTERNAL_ID` with qualifier ili; the concept's definition, which is Princeton's; the maps to WordNet 3.0 and 3.1 offsets | Unicode, ISO 639 | every wordnet, Wiktionary's translations, word-sense evaluation, the predicate mappings | AcademicCurated, named in the registry, lineage WordNet |

### Tier 2. Lexicons: what words mean

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| Open English WordNet 2025+ | The current English sense inventory: which senses a word has, the definition and examples of each, part of speech, hypernymy, meronymy, antonymy, the relations a hop follows. `[dog, LEMMA, dog]`, `[dog, UPOS, NOUN]`, and `[dog, HAS_SENSE, i46360]` are read from it. | `HAS_SENSE`, `HAS_POS`, `HAS_DEFINITION`, `HAS_EXAMPLE`, `IS_A`, `HAS_PART`, `IS_ANTONYM_OF`, `IS_SYNONYM_OF`, and the rest of the wordnet pointer set, on words and on ILIs | CILI, ISO 639 | OMW, Wiktionary, ConceptNet, the sense-tagged corpora, every read that asks what a word means | AcademicCurated, named in the registry, lineage WordNet |
| Open Multilingual Wordnet 2.0, 32 lexicons | The same senses lexicalized in 32 languages, one witness per lexicon, so that `chien`, `犬`, `perro`, and `cane` all bind to `i46360` and consensus on the animal has several independent witnesses. It is what makes translation a read. | `HAS_SENSE` and `HAS_POS` per language, definitions and examples where a lexicon has them, explicit lexical gaps | CILI, ISO 639, OEWN for the shared synsets | translation, cross-language reads | AcademicCurated, named in the registry, one witness per lexicon |
| Princeton WordNet 3.0 | The compatibility coordinate every older mapping is written against: sense keys and 3.0 offsets that PredicateMatrix, MapNet, SemCor, VerbNet, and CILI's maps still use. Retained to bridge those, distinguished from OEWN, and never double-counted with it. | the 3.0 sense keys and offsets as `HAS_EXTERNAL_ID` with the pwn30 qualifiers; sense-tagged frequencies as observations, not attestations | CILI | the mapping resources and the sense-tagged corpora | AcademicCurated; one lineage with OEWN, so a claim both make plays once |

### Tier 3. Predicates and their arguments

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| PropBank 3.4 frames | Every predicate's role sets, `bite.01`, and its numbered arguments: who did what to whom, the shape a sentence's verb imposes on its dependents. | role sets and their roles, one typed edge per role attribute; role links to VerbNet and FrameNet | Unicode, ISO 639, the wordnets for sense links | SemLink, VerbAtlas, PredicateMatrix, semantic role reads | AcademicCurated, named in the registry |
| VerbNet 3.4 | Verb classes with their thematic roles, Agent, Patient, and syntactic frames; the class a verb belongs to constrains what its arguments can be. | class membership, thematic roles, syntactic frames, semantic predicates; members' WordNet sense keys | PropBank, the wordnets | SemLink, PredicateMatrix | AcademicCurated, named in the registry |
| FrameNet 1.7 | Frames, `Cause_harm`, and their elements: the situation a word evokes and the roles in it, with frame-to-frame relations, Inheritance, Using, Precedes, Causative_of, that a hop can follow between situations. | frames, frame elements, lexical units, the frame relations, the annotated full-text as content with its annotation layers | Unicode, ISO 639, the wordnets | SemLink, MapNet, FrameBase, WordFrameNet | AcademicCurated, named in the registry |

### Tier 4. The Linguistic Super Highway: the mappings between resources

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| SemLink 2 | The curated joins PropBank to VerbNet and VerbNet to FrameNet, plus annotated instances, so a role set, a class, and a frame that mean the same are one claim across three witnesses rather than three disconnected nodes. | `pb-vn` and `vn-fn` mappings as claims between the identifiers | PropBank, VerbNet, FrameNet | reads that cross from one predicate resource to another | AcademicCurated, named in the registry |
| PredicateMatrix 1.3 | 426,696 rows tying each predicate to VerbNet, FrameNet, PropBank, WordNet, and MCR identifiers, with Catalan and Spanish lexicalizations on the same rows: one hop from `bite%2:35:00` to `i28957`, `18.2`, `Taking`, `bite.01`. Superseded in coverage, retained until its distinct fields are covered elsewhere. | the row as a claim across the identifiers, one witness; its errors, `bite` to `Arriving`, stay one witness's | the wordnets, PropBank, VerbNet, FrameNet | reads that need the older join | AcademicCurated |
| MapNet 0.1 | FrameNet frames and lexical units mapped to WordNet synsets, 5,162 lines, against FrameNet 1.3 and WordNet 1.6; retained only until FrameBase and SemLink cover it. | frame-to-synset, lexical-unit-to-synset | FrameNet, Princeton WordNet | none once superseded | AcademicCurated |
| VerbAtlas 1.1 | Verb frames over BabelNet synsets with a PropBank mapping: another witness of which verbs share a frame. | synset-to-frame, PropBank-to-VerbAtlas | the wordnets, PropBank | reads over verb frames | AcademicCurated |
| WordFrameNet | Word-to-frame files against older releases; retained until covered. | word-to-frame | FrameNet, the wordnets | none once superseded | AcademicCurated, provenance unknown |
| FrameBase 2.0 | FrameNet's frames as a schema graph with instances, the modern coverage that retires MapNet and WordFrameNet. | frame schema and instance claims | FrameNet, the wordnets | frame reads at scale | AcademicCurated |

### Tier 5. Annotated text: what a treebank says of each word

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| UD tools and documentation | The governed vocabularies themselves, `upos.json` and the relation and feature lists, the authorities the manifests of [6. Registries](Registries.md) operation 6.7 are generated from, and the documentation that defines each value. | the definition of every UPOS, dependency relation, and feature value | Unicode | the treebanks, Wiktionary's parts of speech, every source normalized to UPOS | StandardsDerived |
| Universal Dependencies 2.18, 712 treebanks | Standing for `[word, UPOS, NOUN]`, `[word, LEMMA, lemma]`, `[a, det, dog]`, features, in 186 languages: what lets "What is the capital of France" close the obligations on "What", "is", "the", and "of", what filters the fillers of `[Captain, ' ', ?]` down to the names, what gives role trust its information per part of speech and relation, and what the relation-read task shapes are exemplified by. Every treebank is its own witness. The sentences are content; each sentence's part-of-speech and dependency layers are content too, hashed like compositions. | `HAS_POS`, `HAS_LEMMA`, one relation per dependency label, one relation per feature against a `Name=Value` entity, `SpaceAfter`, all at the word in its sentence | Unicode, ISO 639, the UD vocabularies | role trust, the fillers filter, task shapes, word-sense evaluation, the operational seed | AcademicCurated, named in the registry |
| WSD evaluation framework: SemCor and the five test sets | Sense-tagged usage: 226,036 instances whose gold sense keys map through CILI to ILIs. The co-occurrence observations that gave nearly all of the word-sense gain, and the held-out sets a pull is scored on. | sense-tagged occurrences as observations; the gold labels as claims of the annotators | the wordnets, CILI, UD | the disambiguation measure of [18. Firmware](Firmware.md) operation 18.8 | AcademicCurated |

### Tier 6. The user-curated lexicon

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| Wiktionary, the 2026-08-28 raw Wiktextract | Every word in every language with its parts of speech, senses, glosses, forms, pronunciations, etymologies, and translations: the breadth the academic lexicons lack, `Butler` the surname whose etymology leads to `butler`, German bindings that OMW does not carry, morphological analyses as collections. Witness is the extraction program, lineage Wiktionary. | `HAS_POS`, `HAS_DEFINITION`, `HAS_FORM`, `HAS_FEATURE` as a collection, `TRANSCRIBES_AS` as a collection, `HAS_USAGE_REGISTER` as a collection, `HAS_ETYMOLOGY`, translations as `HAS_SENSE` bindings where a key exists | Unicode, ISO 639, the UD vocabularies, CILI where a sense has a key | ConceptNet, whose lineage it is; the fillers filter; translation coverage | UserCuratedResource, named in the registry |

### Tier 7. Commonsense: what is said between terms

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| ConceptNet 5.7 | 34 million edges in 50 relations, `IsA`, `AtLocation`, `UsedFor`, `Causes`, `CapableOf`, with each edge carrying its sources and a weight: the test bed for witness and consensus modelling, and the only large source with explicit negative evidence, `NotDesires`, `NotCapableOf`. Every edge folds under its own sources' lineage, Wiktionary, DBpedia, contributors, so a copied edge is not a second witness. | one governed relation per ConceptNet relation, each row already a triple | Unicode, ISO 639, Wiktionary, the wordnets it imports | usage reads that need relations no lexicon states | AcademicCuratedWithUserInput, by the registry's rule |
| ATOMIC 2020 | 1.2 million human-authored if-then tuples, `xWant`, `xEffect`, `HinderedBy`, about events and people: what follows from what, the natural witness-count test, since 64,569 tuples appear more than once. | one relation per ATOMIC relation, head to tail | Unicode, ISO 639 | reads about consequences and intent | AcademicCurated, named in the registry's examples by kind |
| ATOMIC10x | The machine-generated ten-times set, admitted as a separate witness at a model's trust, never as a transparent replacement for the human set. | the same relations, under its own witness | ATOMIC 2020's vocabulary | none | AIModelProbe, by the registry's rule for machine-generated testimony |

### Tier 8. Usage: whole sentences and texts

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| Tatoeba 2026-08-29 | Millions of sentences in hundreds of languages with which sentences translate which: sentence-level usage, precedes, gaps, and continuations across languages, and translation pairs as claims of whole sentences. It says nothing of a sentence's words one by one, so it attests at the sentence tier only. | `HAS_LANGUAGE` and `TRANSLATES` at the sentence; author, tags, lists, audio as observations | ISO 639, and the lexicons whose words its sentences land on | continuation and gap reads across languages | UserCuratedResource, by the registry's rule for user-written sentences |
| OpenSubtitles v2024 | Parallel subtitle sentences per language pair, the largest conversational usage corpus: what is said, in what order, in speech. The language of sentences, not of words. | `HAS_LANGUAGE` at the sentence; the parallel alignment as a claim | ISO 639 | conversational continuation reads | lower than Wiktionary, by the roadmap; StructuredCorpus by the registry's rule |
| Project Gutenberg, 195 texts | Whole books as content: the corpus the prototype proved lossless recomposition, deduplication, occurrence counting, and gap and continuation reads on. Content, not a witness: it attests nothing, and its trajectories give `[Captain, ' ', ?]` in Moby Dick. | nothing; observations only | Unicode | container and gap reads, informativeness from container counts | none: content |

### Tier 9. Vocabularies of models

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| The tokenizers of the model farm | Each vocabulary as the path of its tokens in index order, each token as the text it stands for, so that a model's pieces resolve to shared content before the model is read: 2,700,090 tokens across 24 files deduplicated to 240,450 compositions and 11 distinct vocabularies. Ordinary content; it attests nothing. | nothing | Unicode | [24. Models](Models.md) | none: content |

### Tier 10. Places

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| GeoNames, the 2026-09-03 dump | Every place with its names in every language, its hierarchy, its feature class, and the country table with each country's capital: what answers "the capital of France", what a name in a sentence resolves to, and the alternate names that bind a place across languages. | `HAS_NAME` with qualifiers, `HAS_PART` for the hierarchy, `HAS_CAPITAL`, `LOCATED_IN`, feature and admin codes through their code tables | ISO 639, Unicode | the capital read of the acceptance slice, place reads | UserCuratedResource, by the registry's rule, since the gazetteer is wiki-edited |
| Natural Earth 5.1 | Country and populated-place geometry with public-domain provenance: the shapes and points the names of GeoNames sit on. | geometry per place | GeoNames | map reads | StandardsDerived by kind, pending provenance verification |

### Tier 11. Harm

These are ingested last because they reference everything above and because of what they are for: Laplace knows what bad words are, what racism is, and that it is bad, so that it scores negatively, gets avoided, and reduces standing, rather than being ignorant of it. Governance is not deletion of knowledge.

| Source | Why it is ingested | Attests | References | Waited for by | Class |
| --- | --- | --- | --- | --- | --- |
| HateCheck, and its multilingual and Singapore variants when pinned | Functional test cases with the labels ten annotators gave: hateful or not, by construction, per target and per functionality. | the case as content; the label as a claim of the annotators | Unicode, ISO 639 | the harm reads, and the refusal policy of firmware | AcademicCurated |
| Civil Comments | Two million comments with continuous toxicity labels and identity fields. | toxicity and identity labels as claims of the annotators | Unicode | harm standing at the sentence | AcademicCuratedWithUserInput |
| ToxiGen | Generated and human-annotated statements, admitted with generated and human provenance kept separate. | labels under two witnesses | Unicode | harm standing | AcademicCurated for the human annotations; AIModelProbe for the generated text |
| Measuring Hate Speech | Comments with annotator metadata and a continuous hate-speech measure. | the measure as a claim per annotator | Unicode | harm standing | AcademicCurated |
| Social Bias Frames | Posts with the implied bias, the target group, and the offensiveness, as frames. | the frame's fields as claims | Unicode | harm reads that need the implication, not only the label | AcademicCurated |
| Social Chemistry 101 | Rules of thumb about social situations with their judgments: what people think is acceptable. | rules of thumb and judgments as claims | Unicode | the disposition policy of firmware | AcademicCurated |
| ProsocialDialog | Unsafe utterances with their reasons and the prosocial responses to them. | reasons and responses as claims | Unicode | realization under a refusal | AcademicCurated |
| RealToxicityPrompts | Prompts scored by a model for toxicity: admitted as model-scored evaluation evidence, never as human ground truth. | scores under the scoring model as a calculated witness | Unicode | evaluation only | DerivedCalculation, model-scored |
| XSTest | Prompts that look unsafe and are safe: the test that a refusal policy does not over-refuse. | safe and unsafe labels | Unicode | the firmware's disposition policy | AcademicCurated |

### After the chain: the lanes

| Source | Why it is ingested | Stage |
| --- | --- | --- |
| The operational seed: `docs/INVENTION.md`, `docs/INVENTIONS.md`, the binding specs, the authored exemplars and task-shape declarations | The invention's own text as content under SubstrateMandate, and the two relation-read shapes that give the program its first declared capabilities | [19. Pull](Pull.md) operation 19.8 |
| The model farm, safetensors | Circuits as source-scoped entities and graded claims under each model's witness | [24. Models](Models.md) |
| TWIC through 1660, Lichess openings, Syzygy 3–5 men | Games as trajectories, openings as starting sequences, tablebases as endings, at StandardsDerived for FIDE data and tablebases | [27. Chess](Chess.md) |
| Stockfish, pinned | Calculated testimony under a versioned provider, DerivedCalculation | [27. Chess](Chess.md) operation 27.4 |
| The tree-sitter grammar estate, The Stack v2, tiny-codes, and the repositories | Grammars as knowledge, code as content, so that Laplace can learn from it and construct with it | [26. Code](Code.md) |
| Wikipedia and Wikidata | Absent from the estate; to be acquired as pinned full dumps for offline prose and qualified statements | [9. Sources](Sources.md) operation 9.1 |

The estate's physical state, which artifact is active, staged, superseded, or excluded and why, is `docs/source-estate.tsv` in the monorepo, and the current recipe headers in Laplace-Engine record the same order as this table.

## What this stage leaves behind

An estate of activated source generations, each a bound tuple of authority, release, artifact graph, provider, and recipe, with a witness, a trust class, a lineage, and receipts proving that its admission does not depend on how it was physically run.

## Without this stage

Ingestion is fixed one corpus at a time forever, a batch size can change what exists, a superseded directory keeps being extended, and nothing says which files were skipped.
