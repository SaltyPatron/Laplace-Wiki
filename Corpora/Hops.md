# Hops

The lexicons are separate witnesses, and a hop is the curated edge that lets consensus on a claim in one of them pull on a claim in another.

A hop is not a third lexicon. It says that a thing named in one resource is the thing named in another, by the identifiers each resource uses: an edge between highway IDs, highway nodes that are content as their resources write them and on which every source that cites them lands ([Corpora](README.md#page-shape)), the edge attested by the resource that states it. A resource that writes a highway node by a pointer, a WordNet offset or a BabelNet id, has the pointer resolved to the highway node and recorded nowhere. The resource's recipe says it in its `types`, `keyed`, `alias` and `maps` lines, and `laplace highway` reads those lines into the highway perf-cache: an edge between two slots of the highway's lists, an index over those identifiers ([Types](../Reference/Types.md#perf-caches), [Claims](../Semantics/Claims.md#the-linguistic-super-highway)). [Pull](../Semantics/Pull.md#hop-and-fanout) is the pull across it. As built, no recipe reads a mapping file as claims, so an edge stands only in the perf-cache; the highway nodes it joins are content to be recorded, and each edge an attestation of the resource that states it.

| Hop | Joins | On the highway as |
| --- | --- | --- |
| [CILI](Wordnets.md) | a wordnet's synsets and the Collaborative Interlingual Index: WordNet 3.0 offsets and sense keys, resolved to the concept each names | the `ili` list's highway node, `i46360`, and what resolves to it: the pointers `00001740-a`, `wn:00001740v`, `bn:00082138v`, and the sense keys `abandon%2:40:00::` and without `::`, WordNet's internal pointers to lexicalizations, resolved through the highway to the lexicalization strand and recorded nowhere |
| [SemLink](SemLink.md) | PropBank rolesets and VerbNet classes; VerbNet classes and FrameNet frames | edges `pbroleset`→`vnclass`, `vnclass`→`fnframe` |
| [Predicate Matrix](Predicate-Matrix.md) | one predicate role across WordNet, VerbNet, FrameNet and PropBank | edges `ili`→`vnclass`, `ili`→`fnframe`, `ili`→`pbroleset`, `vnclass`→`fnframe`, `pbroleset`→`vnclass`, `pbroleset`→`fnframe` |
| [VerbAtlas](VerbAtlas.md) | BabelNet and WordNet synsets; synsets and VerbAtlas frames; PropBank rolesets and VerbAtlas frames | `bn:` and `wn:` pointers to `ili`; edges `ili`→`vaframe`, `pbroleset`→`vaframe` |
| [PropBank](PropBank.md)'s links | rolesets and VerbNet classes, rolesets and FrameNet frames | edges `pbroleset`→`vnclass`, `pbroleset`→`fnframe` |
| [VerbNet](VerbNet.md)'s members | classes and WordNet senses, classes and FrameNet frames | edges `vnclass`→`ili`, `vnclass`→`fnframe` |
| [FrameNet](FrameNet.md)'s indexes | frame elements and lexical units to their frames | edges `fnlu`→`fnframe`; `fnfe`→`fnframe` is in the recipe (`maps FE ID fnfe to ^frame/ID fnframe`) and yields no edge in the highway built 2026-10-03 |
| [MapNet](MapNet.md) | FrameNet 1.3 frames and lexical units, and WordNet 1.6 synsets | not on it: WordNet 1.6 offsets are pointers into an edition no source here has, so they resolve to nothing |
| [FrameBase](FrameBase.md) | FrameBase frames and WordNet 3.0 synsets | not yet |
| [WordFrameNet](WordFrameNet.md) | a frame, a word, and a synset offset, with no field defined | not yet |

The highway is generated on every deployment ([Operations](../Operations/Deployment.md)) and has a fingerprint every install agrees on; `laplace status` shows it. A mapping's own precision, where its publisher states one, is not yet carried on an edge.
