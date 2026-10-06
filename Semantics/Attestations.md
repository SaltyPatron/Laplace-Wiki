# Attestations

Curated corpora attest to entities, ordinary digital content is observed, and every attestation is a win, draw, or loss and/or a score from a witness.

## Observations

Normal digital content, such as what users upload during normal usage, does not give attestations. It gives observations: the physicality trajectory alone gives precedes, contains, co-occurrences, and more. See [Physicality](../Storage/Physicality.md#trajectories).

## Attestations

Curated corpora give attestations, observations, witnessing, usage, examples, and more. A treebank, a dictionary, a thesaurus, or an encyclopedia is a different type of corpus from normal digital content: it states things about content.

Entities get the attestations, because an entity is the complete structure being attested to. Codepoints get attestations, such as a stroke count; words get attestations; sentences get attestations; and so on at every tier. A sentence from OpenSubtitles, for example, is attested to be English, or whichever language it is.

Attestations are recorded at the highest tier possible for a given corpus. OpenSubtitles gives the language of sentences, not of words.

## Strands

The spider web connects entities, and Glicko-2 sets the tension. An attestation is a link between IDs: the strand, which is the claim, and the witness that pulls on it, with the outcome. It is not a row that copies what it links.

A strand is a composition of the entities it connects, and its physicality is geometry ZM like any other: a point, a line, a polygon, a multi-line, and more. It does not have to be a line.

A claim is a game series: games plus a score. Another file of the same source that attests the same thing adds to the games already played; it does not add a second record.

## Seeded corpora

A seeded corpus is mined for what it teaches: its semantic knowledge, observations, and attestations. Laplace does not export UD Treebanks; it records what UD Treebanks teaches. WordNet, PropBank, SemLink, and every other seed are the same: they happen to be standardized files and formats that can be parsed and decomposed. What a source observed is attested in its own terms; the index a source gives a sentence is not, because Laplace never exports the source. The highway IDs a source cites, an ILI, a roleset, a frame, a language code, are content, and every source that cites one lands on the same node; the pointers by which a source addresses its own records, an offset, a synset id, a sentence number, are resolved to what they point at and not recorded.

A source is a trunk entity above its files, each file is a trunk under it, and each record of each file sits under that. If the file's trunk node is recorded and its metadata matches, everything in that file is already recorded.

## Witnesses

Entities are witnessed. WordNet does not own `dog`: we observe `dog` from WordNet. Every witness observes the same entity.

The witness is the source trunk, `[source record, its files' trunks]`. Provenance is containment: a record is a path over the strands it asserts, inside its file's content tree, with each strand's run length and outcome in its vertex's M, and many source trunks can hold the same strand. The source's own name is content inside its source record. Its trust and lineage are keyed by the trunk; the standing of a strand is one row keyed by the strand's ID, beside the path. Forgetting a source removes its trunk, sweeps what nothing references, and replays the standings it touched.

Witnessing is not attribution, and both are containment. Witnessing is of any entity: it was recorded in some tree. It is calculated, never stored: a walk up through the GIN gives every trunk that holds the entity, and its occurrence counts follow. Normal user content only adds observations: new trees that contain existing nodes. Attribution is of a claim: a source asserted this strand, with an outcome. The strand sits in a record path under the source's trunk, so attribution is a walk up too. Attestations come from seeded corpora and from Laplace's own calculations and outcomes at their trust; ordinary prompts give observations. What is stored per claim is the strand's entity and path, and its standing where that is not a pure function of one witness's series.

A witness derived from another witness records that lineage, so copies do not count as independent consensus.

The witnessing is mechanistic interpretability, auditability, and provenance.

## Outcomes

Attestations are a win, draw, or loss, and/or a score, so there are positive and negative attestations. When Laplace can code, and it compiles something that fails, that failure is an attestation: Laplace just trained itself.
