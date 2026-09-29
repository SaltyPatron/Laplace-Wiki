# 9. Attestations

Curated corpora are recorded as witnesses and claims, in an order fixed by referential integrity and by the first-in-first-out matchups that follow.

Semantics are the relations Laplace records about entities, so that it can link concepts and languages and hop and fan out from anything to anything with integrity. Curated corpora give attestations; dozens of them are required, and this stage records what each one says, in order.

## Before this stage

[8. Content](Content.md): every entity a claim will name. [6. Database](Database.md): the semantics tables. [7. Recipes](Recipes.md): a recipe for each corpus's format.

## Operations, per corpus

### 9.1 Decide what the corpus attests

- **In:** the corpus.
- **Do:** a treebank, a dictionary, a thesaurus, or an encyclopedia is a different type of corpus from normal digital content: it states things about content. Curated corpora give attestations, observations, witnessing, usage, examples, and more. Decide what this corpus states, and at what tier: attestations are recorded at the highest tier possible for a given corpus. OpenSubtitles gives the language of sentences, not of words. Codepoints get attestations, such as a stroke count; words get attestations; sentences get attestations; and so on at every tier. A corpus that states nothing, such as a novel or a tokenizer's vocabulary, is content under [8. Content](Content.md), not a witness.
- **Out:** what this corpus's claims will be about, and at which tier.
- **From:** [Attestations: Attestations](../Semantics/Attestations.md#attestations).

### 9.2 Name the witness and its lineage

- **In:** the corpus.
- **Do:** entities are witnessed. WordNet does not own `dog`: we observe `dog` from WordNet. Every witness observes the same entity. Name the witness, and if it is derived from another witness, record that lineage, so copies do not count as independent consensus: Open English WordNet is derived from Princeton WordNet, so the two form one lineage, and a claim both attest gets one matchup with both witnesses in its witness set. The witnessing is mechanistic interpretability, auditability, and provenance.
- **Out:** the witness record, with its lineage.
- **From:** [Attestations: Witnesses](../Semantics/Attestations.md#witnesses), [Research: Semantics Experiments: Witnessed claims](../Research/Semantics-Experiments.md#witnessed-claims).

### 9.3 Set the witness's trust and entry defaults

- **In:** the witness of 9.2.
- **Do:** trust runs from MANDATE, 1.0, down through mathematical results, academically curated datasets, user-curated corpora, user prompts, and social media posts, to 0, or to −1. AI models rank above user prompts, around user-curated sources, and below academically curated datasets. A witness entering for the first time starts from a stock default for its level of attestation: the source's trust, stability, and uncertainty, and whether synonyms matter more or less than meronyms, nouns than verbs, proper nouns than stopwords. Trust is played as the opponent's deviation in [10. Consensus](Consensus.md), so it is fixed here, before the first matchup.
- **Out:** the trust and entry defaults every claim from this witness will play at.
- **From:** [Consensus: Trust](../Semantics/Consensus.md#trust), [Consensus: Entry](../Semantics/Consensus.md#entry).

### 9.4 Ingest the corpus's files as content

- **In:** the corpus's files and their recipe.
- **Do:** [8. Content](Content.md), operations 8.1 to 8.10. Every label the corpus uses, `dog`, `noun`, `i46360`, `eng`, `hypernym`, and the witness's own name, is content and gets its entity here. A corpus's annotation layers are content too: each sentence's part-of-speech sequence and dependency sequence hashed like compositions, so that small sub-structures share almost entirely while whole-sentence layers rarely repeat.
- **Out:** every entity the corpus's claims will name.
- **Check:** all 686 files of one treebank collection, 2,313,529 sentences, gave 1,776,263 distinct part-of-speech sequences; two-token dependency subtrees were 0.4% new and 17-token subtrees 98.9% new.
- **From:** [Claims: Tuples](../Semantics/Claims.md#tuples), [Research: Semantics Experiments: Annotation layers as content](../Research/Semantics-Experiments.md#annotation-layers-as-content).

### 9.5 Form each claim as a tuple of entities

- **In:** the entities of 9.4 and the recipe.
- **Do:** a claim is a tuple of entities with referential integrity: every part of a claim is an entity. `noun` is `[n,o,u,n]`, the same entity as the word "noun" anywhere else. Any tier's entity can be a predicate. A lexicalization is `[lemma, language, ILI]`, a concept's part of speech `[ILI, POS, n]`, a relation `[ILI, hypernym, ILI]`. Relations are tied together by types and tiers: an ILI synset is a type, just like an IP segment is.
- **Out:** the claims, as paths of entity IDs.
- **From:** [Claims: Tuples](../Semantics/Claims.md#tuples), [Research: Semantics Experiments: Witnessed claims](../Research/Semantics-Experiments.md#witnessed-claims).

### 9.6 Hash each claim twice

- **In:** the claims of 9.5.
- **Do:** deterministic content determines a claim's ID. A claim is a limited path trajectory, so its hash is computed the same way as a composition's: from the IDs along its path. Witnessing and consensus are two different beasts: for witnessing, the hash covers the claim's specifics; for consensus, the hash covers only the main components that make the claim unique. So each claim gets a witnessing ID and a consensus ID, and two witnesses attesting the same claim land on the same consensus ID.
- **Out:** the claim IDs.
- **From:** [Claims: IDs](../Semantics/Claims.md#ids), [Consensus: Deduplication](../Semantics/Consensus.md#deduplication).

### 9.7 Set the masks

- **In:** the claims of 9.5.
- **Do:** separate columns hold bitmasks, such as 256-bit masks, that denote which part of speech, sense, dependency relation, and so on apply. These are enums: fixed in scope, and perf-cachable. The mappings between curated resources, such as SemLink, PredicateMatrix, MapNet, WordFrameNet, and CILI, which link PropBank, VerbNet, FrameNet, WordNet, and ILIs to one another, are the Linguistic Super Highway, and the highway is part of the foundation behind the masks.
- **Out:** the mask columns of each claim.
- **From:** [Claims: Masks](../Semantics/Claims.md#masks), [Claims: The Linguistic Super Highway](../Semantics/Claims.md#the-linguistic-super-highway).

### 9.8 Record each attestation with its outcome

- **In:** the claims of 9.6 and the witness of 9.2.
- **Do:** attestations are a win, draw, or loss, and/or a score, so there are positive and negative attestations. Record each one in the ledger with its witness, its lineage, and its outcome. What the corpus records beside a claim that is not an attestation, such as a witness's sense order or a tagged corpus's usage counts, is recorded as given, beside the claim, as an observation: merging a frequency into a standing loses it, because a standing measures whether a claim holds and saturates as its deviation shrinks.
- **Out:** the ledger rows, in the order the corpus gave them.
- **Check:** 5 million attestations appended at about 245,000 rows per second.
- **From:** [Attestations: Outcomes](../Semantics/Attestations.md#outcomes), [Research: Semantics Experiments: Through witnessed claims](../Research/Semantics-Experiments.md#through-witnessed-claims), [Research: Engine Measurements: Consensus writes](../Research/Engine.md#consensus-writes).

### 9.9 Play the matchups

- **In:** the ledger rows of 9.8.
- **Do:** [10. Consensus](Consensus.md), as the rows arrive.

## The order of corpora

Two rules of the specification fix the order the corpora go in, and the order is part of the record.

1. **Referential integrity.** Every part of a claim is an entity, so every entity a claim names is recorded before the claim. There is no record ballooning: Laplace does not record that `dog` translates to `Hund`, that `dog` translates to `chien`, and so on for every pair; the word `dog` has an ILI, and you bubble up to it, change the language, and bubble down. So the identifiers other corpora point at, the ISO codes and the ILIs, come before the corpora that point at them; a lexicon comes before the mapping that joins it to another lexicon; a tag set comes before the treebank annotated with it; a sense inventory comes before the corpus whose tokens are tagged with its senses.
2. **First in, first out.** As content is observed, first in, first out, the matchups are played, and a witness or claim entering for the first time starts from stock. So the order corpora arrive in changes standings, most trusted witness first, and a snapshot is reproducible only if attestations are applied in a deterministic order. Measured on 11,311 claims replayed in nine orders, the median spread of rating across orders was 0 and the 95th percentile 8.1.

Which corpus comes in which position, and at what priority, is the inventor's list; this page states the rules the list obeys.

See [Semantics](../Semantics/README.md), [Claims: Tuples](../Semantics/Claims.md#tuples), [Consensus: Matchups](../Semantics/Consensus.md#matchups), and [Research: Trust: Order of attestations](../Research/Trust.md#order-of-attestations).

## What this stage leaves behind

Witnesses with their lineage and trust, claims with their two IDs and their masks, and a ledger of every attestation with its outcome, in order.

## Without this stage

There are no semantics, no way to link concepts and languages, and nothing for a strand to tug back with.
