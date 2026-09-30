# Corpora

Each page specifies one collection's record format and the attestation that format supplies.

The format is the publisher's record. The attestation is what that record assigns, at the composition [Attestations](../Semantics/Attestations.md) allows, under the mask [Claims](../Semantics/Claims.md) names, and across the hop [Pull](../Semantics/Pull.md) already defines.

A page here is the glossary of one source: which piece of which fixed-format file says what, of which entity, and as which claim. It is not a manifest of what was downloaded, and it is not the publisher's documentation retold. The Engine reads each source through its recipe, [`recipes/<source>`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes), and the page is that recipe in words: what the recipe reads, the page states; what the recipe passes over, the page says is not read.

## Page shape

Every page has the same parts, in this order.

1. The summary sentence: what the source attests, and what in it attests nothing.
2. **Sources.** One row per source directory of the Engine: witness (as content, and how it is named when every file or directory is its own witness), trust or deviation, lineage, what it comes after in `recipes/order`, the files matched, and a link to the recipe.
3. **The record.** What one record of the file is, what it is about, and what one ledger row witnesses.
4. **Pieces.** One row per field, attribute, element, pointer symbol, or comment key the format has: how it is written, what Laplace reads it as (the subject, a predicate, a pair, a relation, a note, or nothing), the claim tuple recorded, and the publisher's specification of that piece, quoted where it names the piece. A piece the recipe does not read is a row too, saying so and why.

The rules the rows follow:

- Every name and value is recorded as the source writes it. The predicate is the column's or attribute's name; nothing is renamed, reordered, or filled in.
- A claim is a tuple, as [Claims](../Semantics/Claims.md#tuples) defines it, written `[subject, predicate, object]` or `[subject, object]` for a pair. Its tier is one above its highest part, as [Compositions](../Storage/Compositions.md#tiers) requires.
- An empty field attests nothing. What the source writes for empty, such as `_`, is named on the page.
- The specification cited is the publisher's, at its URL. A path on a local disk is not a citation.
- Counts, sizes, and what was measured when a source was loaded belong under [Research](../Research/README.md), not here.
- A source with no recipe says so in its summary: its files are observed content and attest nothing until a recipe exists.

## Not settled

Three things every page needs are not on any page yet, because the words for them do not exist. A missing section stays missing until they do.

- **Tier.** [Attestations](../Semantics/Attestations.md#attestations) says attestations are recorded at the highest tier possible for a corpus. Which tier that is for each source's subject is stated nowhere.
- **Mask.** [Claims](../Semantics/Claims.md#masks) says separate columns hold bitmasks for part of speech, sense, dependency relation, and so on. Which bit each predicate sets is defined nowhere.
- **Trust.** [Consensus](../Semantics/Consensus.md#trust) gives the order of trust, from MANDATE down. The number each source enters at is the recipe writer's choice, and each recipe says so.

## Pages

- [Unicode Character Database](Unicode.md)
- [ISO 639](ISO-639.md)
- [Wordnets](Wordnets.md)
- [Word sense disambiguation](Word-Sense-Disambiguation.md)
- [Universal Dependencies](Universal-Dependencies.md)
- [Hops](Hops.md)
- [FrameNet](FrameNet.md)
- [VerbNet](VerbNet.md)
- [PropBank](PropBank.md)
- [SemLink](SemLink.md)
- [Predicate Matrix](Predicate-Matrix.md)
- [MapNet](MapNet.md)
- [VerbAtlas](VerbAtlas.md)
- [FrameBase](FrameBase.md)
- [WordFrameNet](WordFrameNet.md)
- [Wiktionary](Wiktionary.md)
- [ConceptNet](ConceptNet.md)
- [ATOMIC](ATOMIC.md)
- [Tatoeba](Tatoeba.md)
- [OpenSubtitles](OpenSubtitles.md)
- [Project Gutenberg](Project-Gutenberg.md)
- [Tokenizers](Tokenizers.md)
- [GeoNames](GeoNames.md)
- [Civil Comments](Civil-Comments.md)
- [Measuring Hate Speech](Measuring-Hate-Speech.md)
- [HateCheck](HateCheck.md)
- [ProsocialDialog](Prosocial-Dialog.md)
- [RealToxicityPrompts](RealToxicityPrompts.md)
- [Social Bias Frames](Social-Bias-Frames.md)
- [Social Chemistry](Social-Chemistry.md)
- [ToxiGen](ToxiGen.md)
- [XSTest](XSTest.md)
- [COCO](COCO.md)
- [Code authority](Code-Authority.md)
- [Code corpus](Code-Corpus.md)
- [Games](Games.md)
- [NLTK](NLTK.md)
- [Natural Earth](Natural-Earth.md)
- [The Stack v2](Stack-v2.md)
- [Tiny codes](Tiny-Codes.md)
- [Tree-sitter](TreeSitter.md)
- [Weights](Weights.md)
