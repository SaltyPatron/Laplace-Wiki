# Wordnets

The wordnets attest sense: what each says of a word, of a synset that is the words it lists, and of a sense that is a word in a synset, every value as the wordnet writes it; CILI is the highway's interlingual index, every synset's `ili` read as the concept it points at; the Princeton database files that the WN-LMF editions and the highway already carry are not read; and the manual pages attest nothing.

Four sources read the wordnets, in the order [`recipes/order`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/order) gives: the Collaborative Interlingual Index, Open English WordNet, Open Multilingual Wordnet, then Princeton WordNet 3.0. A wordnet's identifiers (`oewn-02084071-n`, `example-en-10161911-n`, `abandon%2:40:00::`, a synset offset) are its keys: how the file points at its entries, senses and synsets. They resolve to the things they name and are recorded nowhere ([Corpora](README.md#page-shape)).

## Sources

| Source | Witness | Trust class | Lineage | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- | --- |
| `cili` | `Collaborative Interlingual Index` | | | | `ili.ttl`, `ili-map-pwn30.tab` | none: the highway's input ([Types](../Reference/Types.md#perf-caches)) |
| `open-english-wordnet` | what the lexicon writes as `label="..."`: "named as the lexicon names itself" | class `AcademicCurated` | `WordNet` | `cili` | `english-wordnet-*.xml` | [`oewn.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/open-english-wordnet/oewn.recipe), `like wn-lmf` |
| `open-multilingual-wordnet` | what each lexicon writes as `label="..."` | class `AcademicCurated` | none; `omw-en.xml` `WordNet` | `cili` | `omw-*.xml` | [`omw.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/open-multilingual-wordnet/omw.recipe), [`omw-en.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/open-multilingual-wordnet/omw-en.recipe), `like wn-lmf` |
| `princeton-wordnet` | `WordNet 3.0`: "named as the README names the release" | class `AcademicCurated` | `WordNet` | `unicode` | `cntlist`, `cntlist.rev`, `*.exc`, the manual pages | [`recipes/princeton-wordnet`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/princeton-wordnet) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior is the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## WN-LMF

Open English WordNet and every wordnet of Open Multilingual Wordnet are one file each in WN-LMF, the Global WordNet Association's XML for wordnets, [WN-LMF-1.3.dtd](http://globalwordnet.github.io/schemas/WN-LMF-1.3.dtd). Both read like the shared [`wn-lmf.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wn-lmf.recipe), which says what each element is:

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `Lexicon` | `<Lexicon id="..." label="Open English WordNet" language="en" ...>` | the lexicon, named as it names itself (`identity Lexicon label`); its other attributes said of it | `[Open English WordNet, language, en]`, `[Open English WordNet, version, 2024]` | `label CDATA #REQUIRED` |
| `LexicalEntry` | `<LexicalEntry id="..."><Lemma writtenForm="dog" partOfSpeech="n"/>` | the word its Lemma writes (`identity LexicalEntry >Lemma.writtenForm`): the subject of everything inside the entry; its `id` a key | `[Open English WordNet, LexicalEntry, dog]`, `[dog, partOfSpeech, n]` | "writtenForm CDATA #REQUIRED" |
| `Form`, `Pronunciation` | inside the entry | said of the word, each attribute and text under its name | `[dog, writtenForm, dogs]`, `[dog, Pronunciation, dɒɡ]` | |
| `Synset` | `<Synset id="..." ili="i46360" members="oewn-dog-n oewn-domestic_dog-n ..." partOfSpeech="n" lexfile="noun.animal">` | the composition of the words its `members` refer to, in the order listed (`identity Synset members`; `refer members Sense within` and `refer members LexicalEntry`: OMW writes sense ids, OEWN entry ids, and either names the word): every wordnet that lists the same words has the same synset. A member that names nothing is left out, and a synset whose members name nothing is no thing. `ili` is a type of the highway's interlingual index, read as the concept's content (`type ili ili`); `lexfile` is content the highway lists; `id` and `members` are keys | `[Open English WordNet, Synset, [dog, domestic dog, Canis familiaris]]`, `[[dog, …], ili, a member of the genus Canis …]`, `[[dog, …], partOfSpeech, n]`, `[[dog, …], lexfile, noun.animal]` | "members IDREFS", "ili CDATA #REQUIRED" |
| `Definition`, `ILIDefinition`, `Example` | text inside a synset or a sense | said of the synset or the sense under the element's name; an attribute such as `dc:source` under its name | `[[dog, …], Definition, a member of the genus Canis …]` | |
| `Sense` | `<Sense id="..." synset="..." ...>` inside the entry | the word it is inside, with its synset (`identity Sense synset within`, `refer synset Synset`): `[dog, [dog, domestic dog, …]]`; its place in the word; `id` a key | `[dog, Sense, [dog, [dog, …]]]`, `[[dog, [dog, …]], adjposition, a]` | "synset IDREF #REQUIRED" |
| `SenseRelation`, `SynsetRelation` | `<SynsetRelation relType="hypernym" target="..."/>` | the relation of the sense or synset it is inside: its type and the sense or synset its `target` refers to (`link`, `refer`) | `[[dog, …], hypernym, [canine, canid]]`, `[[dog, [dog, …]], antonym, [cat, [cat, …]]]` | "relType enumerated, target IDREF" |
| `SyntacticBehaviour` | `<SyntacticBehaviour id="..." subcategorizationFrame="Somebody %s something" senses="..."/>` | the frame its text writes (`identity SyntacticBehaviour subcategorizationFrame`); `senses` the senses it refers to; `id` a key | `[Somebody %s something, senses, [eat, [eat, …]]]` | |
| `Count` | text inside a sense | said of the sense under `Count` | `[[dog, [dog, …]], Count, 70]` | |
| the `dc:` attributes, `status`, `note`, `confidenceScore` | on the elements that declare them | said of the thing the element is or is inside, under the attribute's name as written | `[[dog, …], dc:source, …]` | |
| `LexicalResource`, `xmlns:dc` | the root, namespaces | structure and XML's own plumbing: nothing | nothing | |
| an `ili` written `in`, or a number the index does not know | `ili="in"` | a key no list knows: nothing | nothing | |

What one element says it says together, as one record: a thing's place in the thing it is inside, its own attributes, its own text; an element that is not a thing speaks of the thing it is inside. Every entry stands on lines of its own (`records`), so a long file is read in parts on every core.

Measured on Open English WordNet 2024 ([Research](../Research/README.md)): 2.70 million compositions and 1.77 million attestations, against 4.49 million when its ids were content.

## CILI

The Collaborative Interlingual Index: "language-independent concept identifiers, their definitions, and their maps to the wordnets. The definitions are Princeton WordNet's." Each concept is a type of the highway's `ili` list (116,698 of them), its content the definition `ili.ttl` gives it (961 concepts share a definition with another and are one type each by content); its number is a key. `ili-map-pwn30.tab` gives the highway the WordNet 3.0 offset of each concept, and WordNet's `index.sense` the sense keys, so a wordnet's `ili`, VerbNet's `wn`, VerbAtlas's `wn:` and `bn:` spellings, PredicateMatrix's offsets and sense keys all resolve to the same slot ([Hops](Hops.md)). The source directory holds a `source` file and no recipe: the Turtle files, the sense mappings and `changes-in-wn31.csv` say nothing that is not a key.

## The Princeton database

WordNet 3.0's `dict` files are the edition `omw-en.xml` carries in WN-LMF, which is read above. The database tables that say the same (`data.*`, `index.*`, `index.sense`, `sentidx.vrb`) and the one the highway lists (`lexnames`) are not read as tables.

| File | Laplace reads it as | Claim recorded |
| --- | --- | --- |
| `cntlist`, `cntlist.rev` | the sense key, read as the ILI concept it resolves to (`type sense_key ili`); its tag count said of it; the sense number a key | `[concept, tag_cnt, 10742]` |
| `noun.exc`, `verb.exc`, `adj.exc`, `adv.exc` | the inflected form, and each base form after it, under the file's category | `[inflected form, noun, base form]` |
| the manual pages, `README`, `LICENSE`, the HTML | text, observed | nothing |
