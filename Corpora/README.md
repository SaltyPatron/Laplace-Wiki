# Corpora

Each page specifies one collection's record format and the attestation that format supplies.

The format is the publisher's record. The attestation is what that record assigns, at the composition [Attestations](../Semantics/Attestations.md) allows, under the mask [Claims](../Semantics/Claims.md) names, and across the hop [Pull](../Semantics/Pull.md) already defines.

A page here is the glossary of one source: which piece of which fixed-format file says what, of which entity, and as which claim. It is not a manifest of what was downloaded, and it is not the publisher's documentation retold. The Engine reads each source through its recipe, [`recipes/<source>`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes), and the page is that recipe in words: what the recipe reads, the page states; what the recipe passes over, the page says is not read.

## Page shape

Every page has the same parts, in this order.

1. The summary sentence: what the source attests, and what in it attests nothing.
2. **Sources.** One row per source directory of the Engine: witness (as content, and how it is named when every file or directory is its own witness), trust class, lineage, what it comes after in `recipes/order`, the files matched, and a link to the recipe.
3. **The record.** What one record of the file is, what it is about, and what one attestation witnesses.
4. **Pieces.** One row per field, attribute, element, pointer symbol, or comment key the format has: how it is written, what Laplace reads it as (the subject, a predicate, a pair, a relation, a note, or nothing), the claim tuple recorded, and the publisher's specification of that piece, quoted where it names the piece. A piece the recipe does not read is a row too, saying so and why.

The rules the rows follow:

- A witness provides content and attestations about it; a page records those. A file's bookkeeping about its own records (dates an entry was made, colours, versions, licences, usage notes, who edited a row) is not testimony and is read by nothing (`omit`, or a column not named). Every name and value that is recorded is as the source writes it: nothing is renamed, reordered, or filled in.
- A claim is a tuple, as [Claims](../Semantics/Claims.md#tuples) defines it, written `[subject, predicate, object]` or `[subject, object]` for a pair. Its tier is one above its highest part, as [Compositions](../Storage/Compositions.md#tiers) requires.
- An empty field attests nothing. What the source writes for empty, such as `_`, is named on the page.
- The specification cited is the publisher's, at its URL. A path on a local disk is not a citation.
- Counts, sizes, and what was measured when a source was loaded belong under [Research](../Research/README.md), not here.
- A source with no recipe says so in its summary: its files are observed content and attest nothing until a recipe exists.
- **A source's identifiers are keys, not content.** How a resource points at its own things (a synset id, a sense key, an ILI number, a sentence id, a geonameid, a case id, a roleset id, a frame element's number, an entry's etymology number, a dialogue's numbering, `sent_id`) is plumbing: it resolves to the thing it names and is recorded nowhere ([Identity](../Storage/Identity.md): the hash is purely content). The recipe says which attributes, members or columns are keys (`key`), which point at things defined elsewhere in the same file or set (`refer`), and which are a resource's keys of types (`type`). The page names them as such and shows no claim with a key in it.
- **A thing is its content.** A word is what the lemma writes; a synset is the composition of the words it lists; a sentence is its text or the path of its words; a place is its name, latitude and longitude; a case, a post, a comment is its text; a frame is its name, a frame element its frame and name, a roleset its predicate's lemma and the name the resource writes for it. Two witnesses that write the same content say it of the same thing.
- **Types are the highway's.** What a curated resource enumerates (parts of speech, dependency relations, lexicographer files, ILI concepts, VerbNet classes and roles, FrameNet frames, frame elements and lexical units, PropBank rolesets, VerbAtlas frames) is a type: one record each in the highway perf-cache, its content as the resource writes it, its slot a mask bit where the list is small ([Types](../Reference/Types.md), [Claims](../Semantics/Claims.md#masks)). A key of a type (`i46360`, `va:0001f`, `abandon.01`, `leave-51.2`, an FE's `ID`) is read as the type. The mappings between the resources (CILI's maps, SemLink, PredicateMatrix, VerbAtlas's bridges, PropBank's links, VerbNet's members, FrameNet's indexes) are the highway's edges: each resource's recipe says them in its `types`, `keyed`, `alias` and `maps` lines, and `laplace highway` reads those lines. The recipes of CILI, SemLink and the Predicate Matrix also attest what their rows say.

## Not settled

Two things every page needs are not on any page yet, because the words for them do not exist. A missing section stays missing until they do.

- **Tier.** [Attestations](../Semantics/Attestations.md#attestations) says attestations are recorded at the highest tier possible for a corpus. Which tier that is for each source's subject is stated nowhere.
- **Mask.** [Claims](../Semantics/Claims.md#masks) says separate columns hold bitmasks for part of speech, sense, dependency relation, and so on. The banks are Laplace-Native's `manifest/banks.tsv`, copied into the highway's layout: `kind` (8 bits, a row's own, no list), `upos` (32), `lexfile` (64), `deprel` (64), `vnrole` (64), each width the room kept for values still to come, a value's bit its frozen slot ([Types](../Reference/Types.md#masks)). Only `kind` is written so far. A sense mask, sense 1 to 256 of a lemma, is specified and has no bank.

## Recipes

Every source in `recipes/order`, in that order, and the page that is its glossary. A page not in this table documents a collection no recipe reads yet, and says so.

| Source | Page |
| --- | --- |
| `unicode` | [Unicode Character Database](Unicode.md) |
| `iso-639` | [ISO 639](ISO-639.md) |
| `cili` | [Wordnets](Wordnets.md) |
| `open-english-wordnet` | [Wordnets](Wordnets.md) |
| `open-multilingual-wordnet` | [Wordnets](Wordnets.md) |
| `princeton-wordnet` | [Wordnets](Wordnets.md) |
| `propbank` | [PropBank](PropBank.md) |
| `verbnet` | [VerbNet](VerbNet.md) |
| `framenet` | [FrameNet](FrameNet.md) |
| `semlink` | [SemLink](SemLink.md) |
| `predicate-matrix` | [Predicate Matrix](Predicate-Matrix.md) |
| `mapnet` | [MapNet](MapNet.md) |
| `verbatlas` | [VerbAtlas](VerbAtlas.md) |
| `wordframenet` | [WordFrameNet](WordFrameNet.md) |
| `universal-dependencies-tools` | [Universal Dependencies](Universal-Dependencies.md) |
| `universal-dependencies-documentation` | [Universal Dependencies](Universal-Dependencies.md) |
| `universal-dependencies` | [Universal Dependencies](Universal-Dependencies.md) |
| `wsd-evaluation-framework` | [Word sense disambiguation](Word-Sense-Disambiguation.md) |
| `wiktionary-kaikki` | [Wiktionary](Wiktionary.md) |
| `wiktionary` | [Wiktionary](Wiktionary.md) |
| `conceptnet` | [ConceptNet](ConceptNet.md) |
| `atomic-2020` | [ATOMIC](ATOMIC.md) |
| `framebase` | [FrameBase](FrameBase.md) |
| `atomic-10x` | [ATOMIC](ATOMIC.md) |
| `tatoeba` | [Tatoeba](Tatoeba.md) |
| `opensubtitles` | [OpenSubtitles](OpenSubtitles.md) |
| `project-gutenberg` | [Project Gutenberg](Project-Gutenberg.md) |
| `tokenizers` | [Tokenizers](Tokenizers.md) |
| `geonames` | [GeoNames](GeoNames.md) |
| `hatecheck` | [HateCheck](HateCheck.md) |
| `sghatecheck` | [HateCheck](HateCheck.md) |
| `xstest` | [XSTest](XSTest.md) |
| `social-bias-frames` | [Social Bias Frames](Social-Bias-Frames.md) |
| `social-chemistry-101` | [Social Chemistry](Social-Chemistry.md) |
| `prosocial-dialog` | [ProsocialDialog](Prosocial-Dialog.md) |
| `real-toxicity-prompts` | [RealToxicityPrompts](RealToxicityPrompts.md) |
| `toxigen` | [ToxiGen](ToxiGen.md) |
| `measuring-hate-speech` | [Measuring Hate Speech](Measuring-Hate-Speech.md) |
| `civil-comments` | [Civil Comments](Civil-Comments.md) |

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
