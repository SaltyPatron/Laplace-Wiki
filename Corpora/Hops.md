# Hops

The lexicons are separate witnesses, and a hop is the curated edge that lets consensus on a claim in one of them pull on a claim in another.

A hop is not a third lexicon and not a record in the DAG. It says that a thing named in one resource is the thing named in another, by the keys each resource uses; those keys are plumbing ([Corpora](README.md#page-shape)), so a hop is said by the resource's recipe in its `types`, `keyed`, `alias` and `maps` lines and read by `laplace highway` into the highway perf-cache: an edge between two slots of the highway's lists ([Types](../Reference/Types.md#perf-caches), [Claims](../Semantics/Claims.md#the-linguistic-super-highway)). [Pull](../Semantics/Pull.md#hop-and-fanout) is the pull across it. No recipe reads a mapping file, and no claim holds a mapping's key.

| Hop | Joins | On the highway as |
| --- | --- | --- |
| [CILI](Wordnets.md) | a wordnet's synsets and the Collaborative Interlingual Index: WordNet 3.0 offsets and sense keys, resolved to the concept each names | the `ili` list's keys: `i46360`, `00001740-a`, `wn:00001740v`, `bn:00082138v`, `abandon%2:40:00::` and without `::` |
| [SemLink](SemLink.md) | PropBank rolesets and VerbNet classes; VerbNet classes and FrameNet frames | edges `pbroleset`→`vnclass`, `vnclass`→`fnframe` |
| [Predicate Matrix](Predicate-Matrix.md) | one predicate role across WordNet, VerbNet, FrameNet and PropBank | edges `ili`→`vnclass`, `ili`→`fnframe`, `ili`→`pbroleset`, `vnclass`→`fnframe`, `pbroleset`→`vnclass`, `pbroleset`→`fnframe` |
| [VerbAtlas](VerbAtlas.md) | BabelNet and WordNet synsets; synsets and VerbAtlas frames; PropBank rolesets and VerbAtlas frames | `bn:` and `wn:` keys of `ili`; edges `ili`→`vaframe`, `pbroleset`→`vaframe` |
| [PropBank](PropBank.md)'s links | rolesets and VerbNet classes, rolesets and FrameNet frames | edges `pbroleset`→`vnclass`, `pbroleset`→`fnframe` |
| [VerbNet](VerbNet.md)'s members | classes and WordNet senses, classes and FrameNet frames | edges `vnclass`→`ili`, `vnclass`→`fnframe` |
| [FrameNet](FrameNet.md)'s indexes | frame elements and lexical units to their frames | edges `fnlu`→`fnframe`; `fnfe`→`fnframe` is in the recipe (`maps FE ID fnfe to ^frame/ID fnframe`) and yields no edge in the highway built 2026-10-03 |
| [MapNet](MapNet.md) | FrameNet 1.3 frames and lexical units, and WordNet 1.6 synsets | not on it: WordNet 1.6 offsets are keys of an edition no source here has |
| [FrameBase](FrameBase.md) | FrameBase frames and WordNet 3.0 synsets | not yet |
| [WordFrameNet](WordFrameNet.md) | a frame, a word, and a synset offset, with no field defined | not yet |

The highway is generated on every deployment ([Operations](../Operations/Deployment.md)) and has a fingerprint every install agrees on; `laplace status` shows it. A mapping's own precision, where its publisher states one, is not yet carried on an edge.
