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

Ordinary content (plain text, source code, `.git` trees, JSON documents, PGN games, PNG/WAV media) is decomposed losslessly so original bytes round-trip verbatim through `lp_realize`. Seeded lexical and annotation corpora (UD Treebanks, WordNet, PropBank, SemLink) are instead mined for what they teach — their semantic knowledge, observations, and attestations — rather than re-exported in their archive markup. What a curated source observed is attested in its own terms; the shared highway IDs it cites (`i46360`, `abandon.01`, `va:0001f`, `Q937`, `eng`) are content nodes on which every citing source collides, whereas release-local internal pointers (`oewn-...`, byte offsets, `sent_id`, FrameNet numbers, `geonameid`) are resolved at ingest to the entities they address and recorded nowhere.

A source is a trunk entity above its files, each file is a trunk under it, and each record of each file sits under that. If the file's trunk node is recorded and its metadata matches, everything in that file is already recorded.

## Witnesses

Entities are witnessed. WordNet does not own `dog`: we observe `dog` from WordNet. Every witness observes the same entity.

The witness is the source trunk, `[source record, its files' trunks]`. The corpus is the trunk: a corpus is one source trunk and one witness, and a treebank, a lexicon, or a dataset under it is files under that trunk, never a witness of its own. Annotators, workers, speakers, and members a corpus names are content: the corpus is the witness, and what it reports of them, this annotator labelled this case, this speaker said this sentence, are relations it attests. Provenance is containment: a record is a path over the strands it asserts, inside its file's content tree, with each strand's outcome and position in its vertex's M, and many source trunks can hold the same strand. Containment answers provenance, where content came from; it does not replace attestations. A source's claims are recorded per claim, witness and lineage in the `attestation` table (games, tokens, score, position, trust); the witness is the trunk ID, with no registry, and is known when it has attestations. The source's own name is content inside its source record. Its declared trust class and lineage are carried on each of its attestation rows; the standing of a strand is one row keyed by the strand's ID, beside the path. Forgetting a source removes its attestations and its trunk, sweeps what nothing references, and replays the standings it touched.

Occurrence witnessing and claim attribution are distinct operations over the four canonical substrate tables (`entity`, `physicality`, `attestation`, `consensus`). Occurrence witnessing of any entity — which files and source trunks observed it — requires no separate lookup table: walking upward through the GIN container index (`laplace_holders`, `laplace_held_files`) finds every trunk holding the entity and its occurrence counts, and ordinary user content adds new observation trees over existing nodes. Claim attestation and attribution operate on asserted strands: a strand's composition and path live in `entity` and `physicality` (and appear inside asserting record paths under the source's trunk with `said`, `outcome`, and `position` in `M`), its per-witness game series (`claim`, `witness`, `lineage`, `games`, `tokens`, `score`, `position`, `trust`) is stored in `attestation`, and its folded Glicko-2 standing (`rating`, `deviation`, `volatility`, `matches`) is stored in `consensus`, with rooted Fisher information royalty shares (`share_bp = 10000`) computed across contributing witnesses by `laplace_attribution` and `laplace_source_attribution`.

A witness derived from another witness records that lineage, so copies do not count as independent consensus.

The witnessing is mechanistic interpretability, auditability, and provenance.

## Outcomes

Attestations are a win, draw, or loss, and/or a score, so there are positive and negative attestations. When Laplace can code, and it compiles something that fails, that failure is an attestation: Laplace just trained itself.
