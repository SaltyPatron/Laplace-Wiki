# Hops

The lexicons are separate witnesses, and a hop is the curated edge that lets consensus on a claim in one of them pull on a claim in another.

A hop is not a third lexicon. It records that a thing named in one resource is the thing named in another, and [Pull](../Semantics/Pull.md#hop-and-fanout) is the pull across it. [Claims](../Semantics/Claims.md#the-linguistic-super-highway) names the hops that form the Linguistic Super Highway. What each hop's files say, piece by piece, is on the hop's own page; the witness of a hop is the resource that published the mapping, never either lexicon it joins.

| Hop | Joins | Named on the highway |
| --- | --- | --- |
| [SemLink](SemLink.md) | PropBank rolesets and VerbNet classes; VerbNet verb senses and FrameNet frames | yes |
| [Predicate Matrix](Predicate-Matrix.md) | one predicate role across VerbNet, WordNet, FrameNet, and PropBank | yes, as PredicateMatrix |
| [MapNet](MapNet.md) | FrameNet 1.3 frames and lexical units, and WordNet 1.6 synsets | yes |
| [VerbAtlas](VerbAtlas.md) | WordNet synsets and VerbAtlas frames; PropBank predicate senses and VerbAtlas frames; BabelNet and WordNet synsets | no |
| [FrameBase](FrameBase.md) | FrameBase frames and WordNet 3.0 synsets | no |
| [WordFrameNet](WordFrameNet.md) | a frame, a word, and a synset offset, with no field defined | yes |
| [CILI](Wordnets.md) | a wordnet's synsets and the Collaborative Interlingual Index, so a claim changes language without a second witness of the gloss | yes |

A mapping's own precision or confidence, where its publisher states one, is the outcome its rows enter with, as the hop's page says. A mapping that states none enters as a win from its witness, at the trust that witness has.
