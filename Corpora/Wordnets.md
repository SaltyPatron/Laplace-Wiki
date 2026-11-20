# Wordnets

The wordnets attest lexical senses and concept relations across languages: synsets anchor on CILI's `ILI` (`i46360`) where assigned and on their lexicon-scoped synset identifier (`oewn-*`) where `ili="in"`—never collapsing homonymous word-list synsets onto bare member lists or CILI gloss strings—while senses form `[lemma, language, ILI]` lexicalization strands and SemCor `Count`/`tag_cnt` usage frequencies are preserved as empirical observations.

Four sources in [`recipes/order`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/order) read the wordnet family: the Collaborative Interlingual Index (`cili`), Open English WordNet (`open-english-wordnet`), Open Multilingual Wordnet (`open-multilingual-wordnet`), and Princeton WordNet 3.0 (`princeton-wordnet`).

Under the Recording Law and [30. Conflicts](../Sequence/Conflicts.md) S1, I5, I7, I8:

- **Synset concept identity (`ILI` vs. `ili="in"`)**: 19,619 of WordNet 3.0's 117,659 synsets share their exact member word list with another synset (eleven verb synsets are simply `drop`), and 961 CILI concepts share an identical English definition string. A synset therefore **never** takes its identity from its member word list or its CILI gloss string: it anchors on its shared `ILI` highway node (`i46360`, content `[i, 4, 6, 3, 6, 0]`) where assigned, and on its lexicon-scoped synset node (`oewn-*`) where `ili="in"` (a new concept not yet assigned an `ILI`), linking by entity collision as soon as CILI assigns an `ILI`.
- **Lexicalization strands (`[lemma, language, ILI]`)**: Every word sense in a language is the 3-part lexicalization composition `[lemma, language, ILI]` (`[dog, en, i46360]`, or `[lemma, language, synset]` when `ili="in"`), with the ISO 639 language node directly inside the strand so cross-lingual translation is an exact GIN intersection on `ILI` + target language (`wn-lmf.recipe` lines 31–34).
- **Internal pointers vs. empirical observations**: Entry IDs (`oewn-dog-n`), sense IDs, WordNet byte offsets (`01976841-v`), and sense keys (`abandon%2:40:00::`) are internal pointers decomposed for their POS/lexfile facts, resolved via `key`/`refer`/`highway.bin`, and recorded nowhere ([Corpora](README.md#page-shape)). By contrast, WN-LMF `<Count>` and Princeton SemCor `cntlist` `tag_cnt` and `sense_number` are empirical corpus usage and sense-rank observations preserved on the lexicalization strand (`[sense, count of usages, 70]`), never confused with witness matchup counts.
- **Single trunk per corpus**: Open Multilingual Wordnet is one corpus trunk and one witness (`Open Multilingual Wordnet`), with each `omw-*.xml` lexicon a file under that trunk (`Batch 2` closes `witness {first label}` per-file witness splitting).

## Sources

| Source | Witness | Trust class | Lineage | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- | --- |
| `cili` | `Collaborative Interlingual Index` source trunk | class `AcademicCurated` | `WordNet` | `unicode`, `iso-639` | `ili.ttl`, `ili-map-pwn30.tab`, `ili-map-pwn31.tab`, `ili-map-odwn13.tab` | [`ili.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/cili/ili.recipe), [`ili-map-pwn30.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/cili/ili-map-pwn30.recipe), [`ili-map-pwn31.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/cili/ili-map-pwn31.recipe), [`ili-map-odwn13.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/cili/ili-map-odwn13.recipe) |
| `open-english-wordnet` | `Open English WordNet` source trunk | class `AcademicCurated` | `WordNet` | `cili` | `english-wordnet-*.xml` | [`oewn.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/open-english-wordnet/oewn.recipe) (`like wn-lmf`) |
| `open-multilingual-wordnet` | `Open Multilingual Wordnet` source trunk (as built, `witness {first label}` per lexicon file) | class `AcademicCurated` | none (`omw-en.xml`: `WordNet`) | `cili` | `omw-*.xml` | [`omw.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/open-multilingual-wordnet/omw.recipe), [`omw-en.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/open-multilingual-wordnet/omw-en.recipe) (`like wn-lmf`) |
| `princeton-wordnet` | `WordNet 3.0` source trunk | class `AcademicCurated` | `WordNet` | `unicode` | `lexnames`, `index.sense`, `cntlist`, `cntlist.rev`, `sents.vrb`, `sentidx.vrb`, `frames.vrb`, `*.exc`, `data.*`, `index.*`, docs | [`recipes/princeton-wordnet/`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/princeton-wordnet) |

## WN-LMF (`wn-lmf.recipe`)

Open English WordNet and Open Multilingual Wordnet share [`wn-lmf.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wn-lmf.recipe) ([WN-LMF-1.3.dtd](http://globalwordnet.github.io/schemas/WN-LMF-1.3.dtd)):

| Piece | Written as | Laplace reads it as | Attestation recorded | Specification |
| --- | --- | --- | --- | --- |
| `Lexicon` | `<Lexicon id="..." label="Open English WordNet" language="en" ...>` | lexicon container (`thing Lexicon label`); `language` supplies the ISO 639 highway node inside every `Sense` lexicalization (`type language language`) | `Requires` dependencies (`[lexicon, requires wordnet, [ref, version]]`); packaging attributes (`version`, `license`, `url`, `email`) omitted | `WN-LMF-1.3.dtd` |
| `LexicalEntry` | `<LexicalEntry id="..."><Lemma writtenForm="dog" partOfSpeech="n"/>` | canonical lemma text (`thing LexicalEntry Lemma/writtenForm`, `together LexicalEntry`); `id` is a `key`; `partOfSpeech` crosswalks `wordnet-pos` → `upos` (`NOUN`) while setting the `upos` bank | `[dog, n]` + `upos` slot, `script`, held `Sense` and `Form` records | `Lemma/writtenForm` |
| `Form`, `Pronunciation`, `Tag` | `<Form writtenForm="dogs">`, `<Pronunciation variety="US">dɒɡ</Pronunciation>` | inflected forms (`thing Form writtenForm`), IPA strings, language varieties, and grammatical tags | `[dog, other form, dogs]`, `[dog_or_form, pronunciation of a form, dɒɡ]`, `variety of language`, grammatical `Tag` | OntoLex `otherForm`, `wn:pronunciation` |
| `Synset` | `<Synset id="oewn-02084071-n" ili="i46360" members="..." partOfSpeech="n" lexfile="noun.animal">` | concept node anchored on `ILI` (`i46360`) and source synset node (`thing Synset id`, `type Synset.id Synset node`) so `ili="in"` synsets stay distinct and never collapse onto member word lists; `lexfile` sets the `lexfile` bank (`6` bits at offset `13`) | `[synset, i46360]`, `[synset, noun.animal]`, `[synset, partOfSpeech]`, `[synset, definition of the synset, …]`, `standard definition of the synset in the ILI`, `is lexicalized`, member lemmas | `WN-LMF-1.3.dtd`, `wn-lemon-1.3.ttl` |
| `Sense` | `<Sense id="..." synset="..." adjposition="a" subcat="...">` | lexicalization `[lemma, language, ILI]` (`thing Sense ^LexicalEntry/Lemma/writtenForm ^Lexicon/language >synset/ili`), falling back to `[lemma, language, synset]` when `ili="in"` | `[entry, lexical sense, [lemma, lang, ILI]]`, `[sense, reference, synset]`, `syntactic behaviour`, `adjposition`, `is lexicalized` | OntoLex `LexicalSense` |
| `Count` | `<Count>70</Count>` | empirical SemCor/corpus sense frequency observation (`content Count`) | `[sense, count of usages, 70]` (observation, never matchup games) | `wn:count` |
| `SenseRelation`, `SynsetRelation` | `<SynsetRelation relType="hypernym" target="..."/>` | typed semantic or lexical relation (`hypernym`, `antonym`, `meronym_part`, `entails`, `derivational`, ...) resolved via `refer` | `[synset, hypernym, target_synset]`, `[sense, antonym, target_sense]` | `WN-LMF` `relType` inventory |
| `SyntacticBehaviour` | `<SyntacticBehaviour id="..." subcategorizationFrame="Somebody %s something" senses="..."/>` | verb subcategorization frame (`wnframe` bank, `6` bits at offset `31`) | `[frame, applies to, sense]` | `wn:senseSubcat` |
| `Example`, `dc:source` | `<Example dc:source="...">...</Example>` | usage example text and cited author/work (`content dc:source`, never an extra witness) | `[synset_or_sense, example usage, text]` | `wn:example` |

## CILI (`cili`)

`ili.recipe` reads `ili.ttl` anchoring each concept strictly on its canonical `i<N>` subject identifier (`thing triple subject`, `where triple/subject matches ^i[0-9]+$`), never on its English definition text, while preserving `[i<N>, a, Concept]`, `[i<N>, skos:definition, [gloss, @en]]`, and `pwn30:` offset keys for `highway.bin`. `ili-map-pwn30.recipe`, `ili-map-pwn31.recipe`, and `ili-map-odwn13.recipe` register edition-specific WordNet offsets onto `ili` slots in `highway.bin` without recording byte offsets as semantic claims.

## Princeton WordNet 3.0 (`princeton-wordnet`)

[`recipes/princeton-wordnet/`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/princeton-wordnet) supplies:

- `lexnames.recipe`: the 45 lexicographer files (`noun.animal`, `verb.motion`, ...), populating the `lexfile` highway list and `bit(64)` mask bank (`6` bits at offset `13`).
- `frames.recipe`, `sents.recipe`, `sentidx.recipe`: Princeton's 35 generic verb frames (`wnframe` bank, `6` bits at offset `31`) and sense-specific verb sentence templates.
- `index-sense.recipe`: sense-key (`abandon%2:40:00::`) resolution mappings for `highway.bin` (targeting `[lemma, eng, ILI]` lexicalization strands in `Batch 2`).
- `cntlist.recipe`, `cntlist-rev.recipe`: SemCor empirical `tag_cnt` frequency counts and `sense_number` rank observations on each resolved sense.
- `exceptions*.recipe`: morphological exception mappings (`*.exc`: `[inflected_form, base_form]` per POS).

## Relations

`wn-lmf.recipe` and `cili/ili.recipe` already map WN-LMF elements and attributes onto OntoLex-Lemon and Global WordNet RDF (`wn-lemon-1.3.ttl`) semantic relations (`lexical sense`, `other form`, `definition of the synset`, `count of usages`, `applies to`) rather than XML tag names. Remaining `Batch 2` items unify `open-multilingual-wordnet` onto a single corpus witness trunk (`omw-*` files under one trunk) and complete sense-key → `[lemma, eng, ILI]` resolution in `highway.bin` alongside `Pronunciation.variety` and `Tag.category` qualifiers.
