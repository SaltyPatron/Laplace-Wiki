# Wordnets

The wordnets attest sense, each of its own synsets and senses under its own names, and CILI is the hop between them that carries a sense across languages without becoming a second witness of the Princeton gloss; the manual pages attest nothing.

Four sources read the wordnets, in the order [`recipes/order`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/order) gives: the Collaborative Interlingual Index, Open English WordNet, Open Multilingual Wordnet, then Princeton WordNet 3.0. Three of them derive from one lineage, `WordNet`: copies of one lineage play one matchup per claim, and each copy is still a row in the ledger. The wordnets of Open Multilingual Wordnet are each a witness of their own, except its English one, which is Princeton WordNet 3.0 and takes the lineage.

## Sources

| Source | Witness | Uncertainty | Lineage | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- | --- |
| `cili` | `Collaborative Interlingual Index` | deviation 35 | `WordNet`: "The definitions are Princeton WordNet's." | `unicode`, `iso-639` | `*.ttl`, `ili-map-pwn*.tab`, `pwn*.tab`, `changes-in-wn31.csv` | [`recipes/cili`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/cili) |
| `open-english-wordnet` | what the lexicon first writes as `label="..."`: "named as the lexicon names itself" | deviation 35 | `WordNet` | `cili` | `english-wordnet-*.xml` | [`oewn.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/open-english-wordnet/oewn.recipe) |
| `open-multilingual-wordnet` | what each lexicon first writes as `label="..."`: "wordnets of many languages, each its own witness, named as its lexicon names itself" | deviation 90; `omw-en.xml` deviation 40 | none; `omw-en.xml` `WordNet`: "The English wordnet of Open Multilingual Wordnet is Princeton WordNet 3.0." | `cili`, `iso-639`, `open-english-wordnet` | `omw-*.xml` | [`omw.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/open-multilingual-wordnet/omw.recipe), [`omw-en.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/open-multilingual-wordnet/omw-en.recipe) |
| `princeton-wordnet` | `WordNet 3.0`: "named as the README names the release" | deviation 35: "this recipe's choice (the one the other wordnets of this lineage were given); the specification does not give one" | `WordNet` | `unicode` | `dict/` and `doc/man`, by the recipes below | [`recipes/princeton-wordnet`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/princeton-wordnet), one per file |

The uncertainty is the deviation the witness's attestations enter at, as [Consensus](../Semantics/Consensus.md#entry) describes. Only the Princeton source says of its number that it is the recipe's choice; [Corpora](README.md#not-settled) lists the number among what stays missing.

## WN-LMF

Open English WordNet and every wordnet of Open Multilingual Wordnet are one file each in WN-LMF, the Global WordNet Association's XML for wordnets, [WN-LMF-1.3.dtd](http://globalwordnet.github.io/schemas/WN-LMF-1.3.dtd). Both read like the shared [`wn-lmf.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wn-lmf.recipe), each under its own name, witness, lineage and trust: XML read as what it says. "A lexical entry is the word its Lemma writes: a wordnet does not own a word, it says things of it. Everything else that carries an id (the lexicon, a sense, a synset, a syntactic behaviour) is the thing that id names, and what is inside a thing is said of it." Every name and value is as the wordnet writes it. Every entry stands on lines of its own, so a long file is read in parts, on every core.

What one element says it says together, as one record: a thing's place in the thing it is inside, its own attributes, and its own text; an element that is not a thing speaks of the thing it is inside, and is one record of its own. An empty attribute value attests nothing.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `Lexicon` | `<Lexicon id="..." label="..." language="..." ...>` | the lexicon its `id` names; its other attributes said of it under their own names | `[lexicon, label, value]`, `[lexicon, language, value]`, `[lexicon, version, value]` | `id ID #REQUIRED`, `label CDATA #REQUIRED`, `language CDATA #REQUIRED`, `email`, `license`, `version`, `url`, `citation`, `logo` [WN-LMF-1.3.dtd](http://globalwordnet.github.io/schemas/WN-LMF-1.3.dtd) |
| `LexicalEntry` | `<LexicalEntry id="..."><Lemma writtenForm="..." partOfSpeech="..."/>` | the word its Lemma's `writtenForm` writes: the subject of everything inside the entry; the entry's `id` said of the word | `[lexicon, LexicalEntry, word]`, `[word, id, value]` | `writtenForm CDATA #REQUIRED` [WN-LMF-1.3.dtd](http://globalwordnet.github.io/schemas/WN-LMF-1.3.dtd) |
| `Lemma` | the element inside the entry | not a thing: its attributes said of the word, together | `[word, writtenForm, value]`, `[word, partOfSpeech, n]`, `[word, script, value]` | `partOfSpeech (n\|v\|a\|r\|s\|t\|c\|p\|x\|u) #REQUIRED` [WN-LMF-1.3.dtd](http://globalwordnet.github.io/schemas/WN-LMF-1.3.dtd) |
| `Form` | `<Form writtenForm="..."/>` inside the entry | its attributes said of the word; one that carries an `id` is instead the thing that id names, inside the word | `[word, writtenForm, value]`; `[word, Form, form id]`, `[form id, writtenForm, value]` | `writtenForm CDATA #REQUIRED`, `id ID #IMPLIED` [WN-LMF-1.3.dtd](http://globalwordnet.github.io/schemas/WN-LMF-1.3.dtd) |
| `Pronunciation` | text with `variety`, `notation`, `phonemic`, `audio` | its text said of the word under `Pronunciation`; its attributes under their own names | `[word, Pronunciation, text]`, `[word, variety, value]` | `#PCDATA`, `variety CDATA #IMPLIED` [WN-LMF-1.3.dtd](http://globalwordnet.github.io/schemas/WN-LMF-1.3.dtd) |
| `Sense` | `<Sense id="..." synset="..." ...>` inside the entry | the sense its `id` names, inside the word; its other attributes said of it as written, `subcat`'s several ids as one text | `[word, Sense, sense]`, `[sense, synset, synset]`, `[sense, adjposition, a]`, `[sense, subcat, value]`, `[sense, lexicalized, false]` | `synset IDREF #REQUIRED`, `adjposition (a\|ip\|p) #IMPLIED`, `subcat IDREFS #IMPLIED`, `lexicalized (true\|false) "true"` [WN-LMF-1.3.dtd](http://globalwordnet.github.io/schemas/WN-LMF-1.3.dtd) |
| `SenseRelation` | `<SenseRelation relType="..." target="..."/>` inside a sense | the sense's relation: its `relType` to what `target` names; its other attributes, such as `dc:type`, are not read | `[sense, antonym, target sense]` | `relType` enumerated, `target IDREF #REQUIRED` [WN-LMF-1.3.dtd](http://globalwordnet.github.io/schemas/WN-LMF-1.3.dtd) |
| `Synset` | `<Synset id="..." ili="..." partOfSpeech="..." ...>` | the synset its `id` names, inside the lexicon; its other attributes said of it, `members`' several ids as one text | `[lexicon, Synset, synset]`, `[synset, ili, i46360]`, `[synset, partOfSpeech, n]`, `[synset, members, value]`, `[synset, lexfile, value]`, `[synset, dc:source, value]` | `ili CDATA #REQUIRED`, `members IDREFS #IMPLIED`, `lexfile CDATA #IMPLIED` [WN-LMF-1.3.dtd](http://globalwordnet.github.io/schemas/WN-LMF-1.3.dtd) |
| `Definition`, `ILIDefinition`, `Example` | text inside a synset, or an example inside a sense | the text said of the synset, or the sense, under the element's name; an attribute the element carries, such as an example's `dc:source`, is said of the same thing under the attribute's name | `[synset, Definition, text]`, `[synset, ILIDefinition, text]`, `[synset, Example, text]`, `[sense, Example, text]` | `#PCDATA` [WN-LMF-1.3.dtd](http://globalwordnet.github.io/schemas/WN-LMF-1.3.dtd) |
| `SynsetRelation` | `<SynsetRelation relType="..." target="..."/>` inside a synset | the synset's relation: its `relType` to what `target` names | `[synset, hypernym, target synset]` | `relType` enumerated, `target IDREF #REQUIRED` [WN-LMF-1.3.dtd](http://globalwordnet.github.io/schemas/WN-LMF-1.3.dtd) |
| `SyntacticBehaviour` | `<SyntacticBehaviour id="..." subcategorizationFrame="..." senses="..."/>` | the thing its `id` names, inside the lexicon; one without an `id`, inside an entry, speaks of the word | `[lexicon, SyntacticBehaviour, id]`, `[id, subcategorizationFrame, text]`; `[word, subcategorizationFrame, text]` | `id ID #IMPLIED`, `subcategorizationFrame CDATA #REQUIRED` [WN-LMF-1.3.dtd](http://globalwordnet.github.io/schemas/WN-LMF-1.3.dtd) |
| `Count` | text inside a sense | said of the sense under `Count`, its attributes under their names | `[sense, Count, value]` | [WN-LMF-1.3.dtd](http://globalwordnet.github.io/schemas/WN-LMF-1.3.dtd) |
| the `dc:` attributes, `status`, `note`, `confidenceScore` | on the elements that declare them | said of the thing the element is, or is inside, under the attribute's name as written, prefix and all | `[synset, dc:source, value]` | `dc:contributor` ... `dc:type`, `status`, `note`, `confidenceScore` [WN-LMF-1.3.dtd](http://globalwordnet.github.io/schemas/WN-LMF-1.3.dtd) |
| `LexicalResource`, the `xmlns:dc` declaration | the root | structure, inside no thing: speaks of nothing | nothing | |
| an `ili` written `in` | `ili="in"` | recorded as written; the DTD does not define `in` | `[synset, ili, in]` | `ili CDATA #REQUIRED` [WN-LMF-1.3.dtd](http://globalwordnet.github.io/schemas/WN-LMF-1.3.dtd) |

A synset's `ili` is the hop: it names the concept CILI keeps, and CILI names the synset back.

## The Princeton database

WordNet 3.0 is "Princeton University's database files (dict/) and the manual pages that document every one of them (doc/man)". The licence lines at the head of the database files say "WordNet 3.0 Copyright 2006 by Princeton University". Each database file is a table whose fields are parted by one space; the numbers the recipes give a field are where it stands, and a name a recipe gives an unnamed field is its handle, never recorded.

### `data.noun`, `data.verb`, `data.adj`, `data.adv`

A synset on every line, read by [`data.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/princeton-wordnet/data.recipe). wndb.5: "All fields, unless otherwise noted, are separated by one space character", and, of the lines that begin each file, "These lines all begin with two spaces and the line number": a line that begins with a space is not a row. The format wndb.5 gives is "synset_offset  lex_filenum  ss_type  w_cnt  word  lex_id  [word  lex_id...]  p_cnt  [ptr...]  [frames...]  |  gloss". [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn)

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| `synset_offset` and `ss_type` | the synset: the path of the two, as the synset's own line writes them; a pointer that writes `a` for a synset whose line says `s` is not read, so the path recorded is the line's own | the subject | "Each synset in the database can be uniquely identified by combining the synset_offset for the synset with a code for the syntactic category (since it is possible for synsets in different data.pos files to have the same synset_offset)." [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn) |
| `lex_filenum` | said of the synset under the field's name | `[[synset_offset, ss_type], lex_filenum, value]` | "Two digit decimal integer corresponding to the lexicographer file name containing the synset." [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn) |
| `w_cnt` | said of the synset | `[[synset_offset, ss_type], w_cnt, value]` | "Two digit hexadecimal integer indicating the number of words in the synset." [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn) |
| the first `word` | said of the synset under `word`, recorded as written, syntactic marker and all | `[[synset_offset, ss_type], word, galore(ip)]` | "ASCII form of a word as entered in the synset by the lexicographer, with spaces replaced by underscore characters (_)."; in data.adj a marker "is appended, in parentheses, onto word without any intervening spaces" [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn) |
| `lex_id` of the first word | not read: it is said of the word within the synset, not of the synset | nothing | "One digit hexadecimal integer that, when appended onto lemma, uniquely identifies a sense within a lexicographer file." [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn) |
| `[word lex_id...]`, the second word to the last | not read: `w_cnt` of them, so nothing after the first stands at a fixed place in the line | nothing | [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn) |
| `p_cnt [ptr...]` | not read: the pointers, each "pointer_symbol  synset_offset  pos  source/target" | nothing | "The source/target field distinguishes lexical and semantic pointers." [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn) |
| `[frames...]` | not read: in data.verb, "f_cnt  +  f_num  w_num  [ +  f_num  w_num...]" | nothing | [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn) |
| `\| gloss` | not read: the text after the vertical bar, to the end of the line | nothing | "The gloss may contain a definition, one or more example sentences, or both." [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn) |

What a line says it says together: the line is one record, witnessed once, and its three claims within it. The parts not read are not read because the table reader cannot say them: every line of these files holds parts that stand at no fixed place.

### `index.noun`, `index.verb`, `index.adj`, `index.adv`

A word on every line, read by [`index.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/princeton-wordnet/index.recipe); a line that begins with a space is not a row. The format wndb.5 gives is "lemma  pos  synset_cnt  p_cnt  [ptr_symbol...]  sense_cnt  tagsense_cnt   synset_offset  [synset_offset...]". [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn)

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| `lemma` and `pos` | the path of the two | the subject | "All remaining fields are with respect to senses of lemma in pos." [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn) |
| `synset_cnt` | said of the path under its own name | `[[lemma, pos], synset_cnt, value]` | "Number of synsets that lemma is in. This is the number of senses of the word in WordNet." [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn) |
| `p_cnt` | said of the path | `[[lemma, pos], p_cnt, value]` | "Number of different pointers that lemma has in all synsets containing it." [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn) |
| `[ptr_symbol...]` | not read: `p_cnt` of them, so nothing after `p_cnt` stands at a fixed place in the line | nothing | [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn) |
| `sense_cnt`, `tagsense_cnt` | not read, for the same reason | nothing | [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn) |
| `synset_offset [synset_offset...]` | not read: `synset_cnt` of them, in the order of the lemma's senses | nothing | "When the index.pos files are generated, the synset_offsets are output in sense number order, with sense 1 first in the list." [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn) |

The line is one record, witnessed once, and its two claims within it.

### `index.sense`, `cntlist`, `cntlist.rev`

Three tables of a sense key and its numbers, read by [`index-sense.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/princeton-wordnet/index-sense.recipe), [`cntlist.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/princeton-wordnet/cntlist.recipe) and [`cntlist-rev.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/princeton-wordnet/cntlist-rev.recipe). senseidx.5: "fields are separated by one space", and "Each line is of the form:   sense_key  synset_offset  sense_number  tag_cnt". cntlist.5: "Each line in cntlist is of the form:   tag_cnt  sense_key  sense_number", and "The cntlist.rev file contains the same fields described above, in the following order: sense_key  sense_number  tag_cnt". [senseidx(5WN)](https://wordnet.princeton.edu/documentation/senseidx5wn), [cntlist(5WN)](https://wordnet.princeton.edu/documentation/cntlist5wn)

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| `sense_key` | the subject, recorded whole, as written | the subject | senseidx.5 writes it `lemma%lex_sense`, and `lex_sense` `ss_type:lex_filenum:lex_id:head_word:head_id` [senseidx(5WN)](https://wordnet.princeton.edu/documentation/senseidx5wn) |
| the parts of the `sense_key` | not read: the table reader has no way to part a field at `%` and `:` and name the parts by their position | nothing | [senseidx(5WN)](https://wordnet.princeton.edu/documentation/senseidx5wn) |
| `synset_offset`, `sense_number`, `tag_cnt` in `index.sense` | each said of the sense key under the field's own name | `[sense_key, synset_offset, value]`, `[sense_key, sense_number, value]`, `[sense_key, tag_cnt, value]` | [senseidx(5WN)](https://wordnet.princeton.edu/documentation/senseidx5wn) |
| `tag_cnt`, `sense_number` in `cntlist` and `cntlist.rev` | each said of the sense key under its own name, whichever order the file writes them in | `[sense_key, tag_cnt, value]`, `[sense_key, sense_number, value]` | "The fields are separated by one space" [cntlist(5WN)](https://wordnet.princeton.edu/documentation/cntlist5wn) |

Each line is one record, witnessed once, and its claims within it.

### `noun.exc`, `verb.exc`, `adj.exc`, `adv.exc`

The exception lists, read by [`exceptions.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/princeton-wordnet/exceptions.recipe). wndb.5: "The first field of each line is an inflected form, followed by a space separated list of one or more base forms of the word. There is one exception list file for each syntactic category." wndb.5 gives these fields no names. [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn)

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| the first field | the inflected form: the subject; the recipe's handle for the field, `inflected`, is never recorded | the subject | "an inflected form" [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn) |
| the file's name before its `.` | the predicate: the syntactic category, `noun`, `verb`, `adj` or `adv` | the predicate | "one exception list file for each syntactic category" [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn) |
| each further field | a base form; a line that lists several says each | `[inflected form, noun, base form]` | "a space separated list of one or more base forms of the word" [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn) |

Each claim stands alone.

### `sentidx.vrb`

Read by [`sentidx.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/princeton-wordnet/sentidx.recipe). wndb.5: "Each line of the file sentidx.vrb contains a sense_key followed by a space and a comma separated list of example sentence template numbers, in decimal." wndb.5 names the first field `sense_key` and gives the list no name. [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn)

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| `sense_key` | the subject, recorded whole | the subject | [senseidx(5WN)](https://wordnet.princeton.edu/documentation/senseidx5wn) |
| the list, parted by `,` | each number a pair with the sense key; the recipe's handle for the field, `templates`, is never recorded | `[sense_key, template number]` | "a comma separated list of example sentence template numbers, in decimal" [wndb(5WN)](https://wordnet.princeton.edu/documentation/wndb5wn) |
| a line that lists none | one line, `pet%2:35:00::` | nothing | |

Each pair stands alone.

### `lexnames`

Read by [`lexnames.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/princeton-wordnet/lexnames.recipe). lexnames.5: "Each line in lexnames contains 3 tab separated fields ... The first field is the two digit decimal integer file number. ... The second field is the name of the lexicographer file that is represented by that number, and the third field is an integer that indicates the syntactic category of the synsets contained in the file." lexnames.5 gives these fields no names. [lexnames(5WN)](https://wordnet.princeton.edu/documentation/lexnames5wn)

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| the line | the row itself is the claim: the tuple of its three fields, in its own order | `[file number, lexicographer file name, syntactic category]` | [lexnames(5WN)](https://wordnet.princeton.edu/documentation/lexnames5wn) |

### The manual pages and the rest of the release

[`man.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/princeton-wordnet/man.recipe) reads the manual pages, "which document every file of the database and say what each pointer_symbol, ss_type, lex_filenum and frame number stands for"; the release's own README, licence, authors, change log and installation instructions; the log grind wrote when it built the database; and the texts the browser shows. They are read as text, every byte as written: the manual pages are written in troff, and their markup is part of what is recorded. [`html.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/princeton-wordnet/html.recipe) reads the manual pages as HTML, each of which says it was generated from the manual page's source by PolyglotMan, as the file's syntax tree. Nothing is attested from either: what they say of a pointer symbol or a frame number is observed content, as [Attestations](../Semantics/Attestations.md#observations) says of ordinary text, and the pointers and frames of the data files are not read.

## CILI

The Collaborative Interlingual Index: "language-independent concept identifiers, their definitions, and their maps to the wordnets. The definitions are Princeton WordNet's." Four recipes read it. The witness is `Collaborative Interlingual Index`, of lineage `WordNet`.

### The index and its maps in Turtle

`ili.ttl`, `ili-map.ttl`, `ili-map-wn30.ttl`, `ili-map-wn31.ttl` and `ili-map-odwn13.ttl` read like the shared [`turtle.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/turtle.recipe), through [`ili.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/cili/ili.recipe): every statement is recorded as written. An identifier between angle brackets is recorded without them, in whichever of the three places it stands; a quoted text without its quotes and with its escapes resolved; a name written with a prefix keeps it; `a` is recorded as the `a` the file writes.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| a statement | `<i1> a <Concept> .` | the triple as written | `[i1, a, Concept]` | the index holds "a definition and a source for each identifier" [CILI](https://github.com/globalwordnet/cili) |
| `skos:definition` | `<i1> skos:definition "..." .` | the text, said of the concept | `[i1, skos:definition, text]` | |
| `dc:source` | `<i1> dc:source pwn30:00001740-a .` | the prefixed name, kept as written | `[i1, dc:source, pwn30:00001740-a]` | |
| `owl:sameAs` | `<i1> owl:sameAs pwn30:00001740-a .`; `ili:i1 owl:sameAs pwn31:300001740-a .`; `ili:i69801 owl:sameAs odwn13:06341431-n .` | the map: the concept's synset in that wordnet, subject and object each as the file spells them | `[i1, owl:sameAs, pwn30:00001740-a]`, `[ili:i1, owl:sameAs, pwn31:300001740-a]` | "mapping from Princeton WordNet 3.0 to the ILI in Turtle"; "The mappings from Princeton WordNet 3.1 to the ILI"; "The mapping from Open Dutch WordNet 1.3 to the ILI" [CILI](https://github.com/globalwordnet/cili) |
| a text with a language tag or a datatype | `"..."@en`, `"..."^^type` | the text says so | `[text, en]`, `[text, datatype]` | |
| `# able` | a comment after the statement | not read | nothing | |
| a blank node, a collection | | not read: a statement of a node the file does not name | nothing | |

Each statement stands alone. The README says of `ili-map.ttl` and `ili-map-wn30.ttl` that "These files are identical"; both are read.

### The maps as tables

`ili-map-pwn*.tab` are the index's maps to the wordnets as tables, read by [`maps.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/cili/maps.recipe): "a concept, and the synset it is in the wordnet the file's name gives. The older maps were constructed automatically, and give each row a score." The recipe's handles for the three fields, `ili`, `synset` and `score`, are never recorded.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| the first field | the concept | the subject | "ILI WNX.X CONFIDENCE" [CILI](https://github.com/globalwordnet/cili) |
| the file's name, between its last `-` and the `.` after it | the predicate: the wordnet, `pwn30` from `ili-map-pwn30.tab` | the predicate | |
| the second field | the synset in that wordnet | `[i1, pwn30, 00001740-a]` | |
| the third field | the score the row gives its claim; a row that gives none is a win | the claim's score, as the file writes it | "These are automatic mappings." [CILI](https://github.com/globalwordnet/cili) |

Each claim stands alone.

### The sense mappings

`pwn*.tab` are the sense mappings, read by [`senses.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/cili/senses.recipe): "a synset, and a sense key it holds, in the wordnet the file's name gives."

| Piece | Laplace reads it as | Claim recorded |
| --- | --- | --- |
| the first field | the synset | the subject |
| the file's name before its first `.` | the predicate: the wordnet | the predicate |
| the second field | the sense key | `[synset, wordnet, sense key]` |

Each claim stands alone.

### `changes-in-wn31.csv`

Read by [`changes.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/cili/changes.recipe): "What changed between WordNet 3.0 and 3.1: every row says of its WordNet 3.1 synset what each column holds." The table is parted by `,` and its first row names the columns.

| Piece | Laplace reads it as | Claim recorded |
| --- | --- | --- |
| `WN31` | the WordNet 3.1 synset | the subject |
| every other column | said of it under the column's name, as the header writes it | `[WN31, column, value]` |
| an empty field | what the table leaves empty | nothing |

Each claim stands alone. The CILI README and every file the four recipes do not match are not read.
