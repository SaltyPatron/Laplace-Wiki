# Corpora

Each page specifies one collection's record format and the attestation that format supplies.

The format is the publisher's record. The attestation is what that record assigns, at the composition [Attestations](../Semantics/Attestations.md) allows, under the mask [Claims](../Semantics/Claims.md) names, and across the hop [Pull](../Semantics/Pull.md) already defines.

A page here specifies what one source attests under the Recording Law ([INVENTOR_RECORD](../Repositories/Laplace/docs/INVENTOR_RECORD.md)): which piece of each fixed-format file supplies canonical content, which internal file pointers resolve at ingest via `key` and `refer` and are recorded nowhere, which shared identifiers land on highway nodes, and which annotations supply n-ary claims or scored outcomes across the `BELIEF` and `RISK` planes. It is not a manifest of what was downloaded, and it is not the publisher's documentation retold. The Engine admits each source through its declarative recipe under [`recipes/<source>`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes). Where an active recipe does not yet extract a gold label, crosswalk, multi-turn trajectory, or score—or where a corpus awaits its `.recipe`—the page states the target corpus semantics first and distinguishes remaining recipe gaps to close in `Batch 2` and `Batch 3`, never excusing dropped fields, crosswalks, or scores as permanent specification exclusions.

## Page shape

Every page has the same parts, in this order.

1. The summary sentence: what the source attests under the Recording Law, and where a queued source or piece awaits recipe wiring.
2. **Sources.** One row per source directory of the Engine: witness (its name, content inside the source record, the witness itself being the source trunk, one per corpus, whose treebanks, lexicons, and datasets are files under it with their paths—one organization's corpus set being one source, as Universal Dependencies' treebanks, documentation pages, and validator data are, while each ISO 639 authority is a corpus of its own; and, where the Engine as built names a witness per file or directory, how it does alongside the single-trunk target), trust class, lineage, what it comes after in `recipes/order`, the files matched, and a link to the recipe.
3. **The record.** What one record of the file is, what it is about, and what one attestation witnesses.
4. **Pieces.** One row per field, attribute, element, pointer symbol, or comment key the format has: how it is written, what Laplace reads it as (the subject, a predicate, a pair, a relation, a scored risk/standing signal, a note, or file bookkeeping), the target claim tuple or scored attestation, and the publisher's specification of that piece, quoted where it names the piece. Where an active recipe leaves a piece unextracted or unscored, the row states both the target semantics and the current recipe gap.
5. **Relations.** Where the page records claims: for each claim shape, whether its relation as built is still a field or markup name and what semantic relation or road class is the target.

The rules the rows follow:

- A witness provides content and attestations about it; a page records those. A file's pure bookkeeping about its own packaging (timestamps an entry was modified, map-coloring numbers, zoom hints, export split labels) is not testimony and is omitted (`omit`). Every canonical text and identifier that is recorded is decoded to clean UTF-8 content so identical content collides on the same `lp_id` across every source and modality.
- **A relation is meaning, never a field name.** A claim's relation, like every other part of it, is what the source means, resolved through the road classes, never the name of the field, column, attribute, or layer the source's markup happens to use. A tagset value is a value of that tagset, a road class, with its attested equivalence to the shared vocabulary: FrameNet's BNC layer writes `NN1`, a CLAWS C5 singular common noun, and its PENN layer `nns`, a Penn Treebank plural common noun, each reaching `NOUN` through `manifest/slots/edges-tagsets.tsv`. A per-span label—a frame element, a grammatical function, a phrase type—belongs in the sentence's aligned annotation layer ([Types: Layers](../Reference/Types.md#layers)), not globally on the bare word. A pointer's attribute name (`feID`, `ID`) is in no claim. Where an active recipe still emits a markup name (`[dog, BNC, NN1]`, `[pred, role, 10_VN_ROLE, vn:Theme]`), the Relations section states both the built tuple and the target meaning. Where a source does not document what a field means, the field remains an explicit unresolved obligation until its publisher meaning is established.
- **Toxicity, hate, bias, and moral annotations are scored risk testimony, never blind `WIN` literals.** Safety, hate-speech, toxicity, social-bias, and moral-judgment corpora (`-2..+2` moral scales, `[0, 1]` annotator fractions and model probabilities, continuous Rasch hate measures, gold hate/refusal verdicts) supply **scored negative/harm/risk attestations** feeding the `RISK` and `consensus` planes (`BELIEF ≠ RISK ≠ ACTION`, [INVENTOR_RECORD](../Repositories/Laplace/docs/INVENTOR_RECORD.md), [20. Forward](../Sequence/Forward.md)). Recording a toxicity float or hateful verdict as an uncalibrated `WIN` string literal or leaving it unattested in the row violates the Recording Law; any recipe that still does so is an explicit `Batch 2` recipe gap.
- A claim is a tuple of content, of whatever arity the source asserts it in, as [Claims](../Semantics/Claims.md#tuples) defines it: written `[subject, predicate, object]` or `[subject, object]` for a pair where that is its shape, and as its own shape where it is not, such as a lexicalization `[lemma, language, ILI]`, a bitext translation `[lang1, sent1, lang2, sent2]`, or a role inside a roleset. Its tier is one above its highest part, as [Compositions](../Storage/Compositions.md#tiers) requires.
- An empty field attests nothing. Explicit absence tokens defined by a publisher (such as `_` in CoNLL-U, `char-none` in Social Chemistry, or `none` in ATOMIC tails) are handled as absence or schema-defined nullity, never conflated with ordinary English words.
- The specification cited is the publisher's, at its URL. A path on a local disk is not a citation.
- Counts, sizes, and what was measured when a source was loaded belong under [Research](../Research/README.md), not here.
- A source queued for a declarative `.recipe` (`Batch 2` or `Batch 3`) documents its publisher record layout and target semantic attestations while stating clearly that admission awaits its recipe.
- **Highway IDs are content; a source's internal pointers are not.** A highway ID is an identifier from a shared vocabulary that other sources cite too: an ILI (`i46360`), a Wikidata QID (`Q23622`, `Q937`), a PropBank roleset (`abandon.01`), a VerbNet class (`leave-51.2`), a FrameNet frame, frame element, or lexical unit, a VerbAtlas frame (`va:0001f`), an ISO 639 language code (`eng`), or a FIDE player ID. It is content like any other text ([Identity](../Storage/Identity.md): the hash is purely content), `i46360` is `[i, 4, 6, 3, 6, 0]` and `Q23622` is `[Q, 2, 3, 6, 2, 2]`, and every source that cites it lands on the exact same node ([30. Conflicts](../Sequence/Conflicts.md) S1, I5). An internal pointer is how a resource addresses its own records or a specific edition's layout: a WordNet byte offset, a local sense or entry id (`oewn-dog-n`, `en-dictionary-en-noun-hIt8uVcE`), a FrameNet numeric ID, a WSD instance id (`d000.s000.t000`), a Tatoeba sentence or audio id, a `geonameid`, a case or row id, a dialogue's turn index, a token's number, `sent_id`, or a line number. It is plumbing: decomposed by the source's own notation only to extract the facts it carries (`06975898-n` an offset and part of speech `n`), resolved via `key`, `refer`, or `type` to the entity it points at, and recorded nowhere ([Recipes](../Reference/Recipes.md#what-each-named-part-is)). A sense key (`abandon%2:40:00::`) is WordNet's internal pointer to a lexicalization: decomposed for its lemma, part of speech, and lexicographer file, resolved through the highway perf-cache to `[lemma, language, ILI]`, and recorded nowhere ([30. Conflicts](../Sequence/Conflicts.md) I7).
- **A thing is its content.** A word is what the lemma writes; a sentence is its text or the path of its words; a place is its `[name, latitude, longitude]`; a case, a post, or a comment is its decoded UTF-8 text. A concept is its highway node: a synset anchors on its `ILI` (`i46360`) where assigned and on its lexicon-scoped synset identifier (`oewn-*`) where `ili="in"`—never collapsing the 19,619 WordNet synsets that share member word lists onto bare word lists or CILI gloss strings—and links by collision when CILI states its ILI. A PropBank roleset, a VerbNet class, a FrameNet frame, frame element, or lexical unit, a VerbAtlas frame, a Wikidata item (`Q...`), and a FIDE-identified chess player are highway nodes in the same way, with labels and multilingual names attested of them for realization.
- **Types are the highway's.** What a curated resource enumerates (parts of speech, dependency relations, lexicographer files, subcategorization frames, ILI concepts, VerbNet classes and roles, FrameNet frames, frame elements, and lexical units, PropBank rolesets, VerbAtlas frames) is a type: one record each in `highway.bin`, its content as the resource writes it, and a slot in the `bit(64)` mask where the inventory fits a mask bank ([Types](../Reference/Types.md), [Claims](../Semantics/Claims.md#masks)). The mappings between the resources (CILI's maps, SemLink, Predicate Matrix, MapNet, WordFrameNet, FrameBase, VerbAtlas's bridges, PropBank's links, VerbNet's members, FrameNet's indexes, Wiktionary and ConceptNet external links) are the highway's edges: each resource's recipe declares them in its `types`, `keyed`, `alias`, and `maps` directives, and `laplace highway` compiles them into `highway.bin`.

## Not settled

Two things every page needs are not uniform across all pages yet:

- **Tier.** [Attestations](../Semantics/Attestations.md#attestations) states that attestations attach once at the exact tier the source asserts them (atom, word, phrase, sentence, dialogue, work, or concept), never blanket-copied down to constituent words.
- **Mask.** `entity.mask` and `physicality.mask` carry one `uint64` / SQL `bit(64)` defined by [`Laplace-Native/manifest/banks.tsv`](https://github.com/SaltyPatron/Laplace-Native/blob/main/manifest/banks.tsv): `kind` (`8` bits at offset `0`, row-role flags `CLAIM`, `RECORD`, `TUPLE`, `FILE`), `upos` (`5` bits at offset `8`, entity enum), `lexfile` (`6` bits at offset `13`, entity enum), `deprel` (`6` bits at offset `19`, occurrence enum), `vnrole` (`6` bits at offset `25`, occurrence enum), and `wnframe` (`6` bits at offset `31`, entity enum), where each enum bank stores `slot + 1` (`0` = absent) from frozen `manifest/slots/*.tsv` indices ([Types](../Reference/Types.md#masks)). The number a wordnet gives a sense among a lemma's senses (`sense_number`) is an empirical rank observation, not a mask bank.

## Recipes

Every corpus source in the Engine's [`recipes/order`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/order), in admission order, and the page that specifies it (alongside operational seed and session sources `laplace-operational` and `agent-transcripts`). Recipe presence in `recipes/` does not by itself imply that every dataset is admitted on a given host or that remaining `Batch 2`/`Batch 3` recipe gaps are closed. The three Universal Dependencies entries share one corpus trunk; directories and source-management entries do not mint extra witnesses.

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
| `verbnet-gl` | [VerbNet](VerbNet.md) |
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
| `webster-1913` | [Project Gutenberg](Project-Gutenberg.md) |
| `roget-thesaurus` | [Project Gutenberg](Project-Gutenberg.md) |
| `britannica-1911` | [Project Gutenberg](Project-Gutenberg.md) |
| `sloane-electrical` | [Project Gutenberg](Project-Gutenberg.md) |
| `tokenizers` | [Tokenizers](Tokenizers.md) |
| `brown` | [NLTK](NLTK.md) |
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
| `chess-com` | [Games](Games.md) |
| `twic` | [Games](Games.md) |
| `lumbras-gigabase` | [Games](Games.md) |
| `laplace-chess` | [Games](Games.md) |
| `openings` | [Games](Games.md) |
| `syzygy` | [Syzygy](Syzygy.md) |
| `workspace-code` | [Code corpus](Code-Corpus.md) |

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
- [Syzygy](Syzygy.md)
- [NLTK](NLTK.md)
- [Natural Earth](Natural-Earth.md)
- [The Stack v2](Stack-v2.md)
- [Tiny codes](Tiny-Codes.md)
- [Tree-sitter](TreeSitter.md)
- [Weights](Weights.md)
