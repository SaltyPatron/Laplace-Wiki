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

### 9.9 Order the sources by dependency

- **In:** every active generation.
- **Do:** every part of a claim is an entity, so the identifiers other sources point at come first. The dependency order: Unicode, then ISO 639, then CILI, then OEWN and OMW, then Wiktionary, then frames and roles, VerbNet, PropBank, FrameNet, SemLink, VerbAtlas, FrameBase, then commonsense, ConceptNet, ATOMIC, then usage corpora, UD, Tatoeba, OpenSubtitles, then the operational seed, the invention documents themselves under SubstrateMandate, then models and chess. A lexicon comes before the mapping that joins it to another; a tag set before the treebank annotated with it; a sense inventory before the corpus tagged with its senses. First in, first out then fixes standings, so the order is part of the record.
- **Out:** the admission order.
- **From:** `docs/plan/ASSIMILATION_ROADMAP.md` workstream H; `seeds/operational/README.md`; [12. Attestations](Attestations.md) §The order of corpora.

### 9.10 Run the common admission machine

- **In:** the active generation, in its turn.
- **Do:** [11. Content](Content.md) and [12. Attestations](Attestations.md). Source-specific code remains only the irreducible recovery kernel; the common spine owns everything after it. One ingest at a time.
- **Out:** the source admitted.
- **From:** `docs/specs/06_Engineering_Ruleset.txt` Rule #8 and §Operational constraints.

## What this stage leaves behind

An estate of activated source generations, each a bound tuple of authority, release, artifact graph, provider, and recipe, with a witness, a trust class, a lineage, and receipts proving that its admission does not depend on how it was physically run.

## Without this stage

Ingestion is fixed one corpus at a time forever, a batch size can change what exists, a superseded directory keeps being extended, and nothing says which files were skipped.
