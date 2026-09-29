# Wordnets

The wordnets attest sense, and CILI is the hop that changes language without becoming a second witness of the Princeton gloss.

The composition is a sense: a lemma in a synset. The mask is sense. The value is the synset, its part-of-speech category, and its pointer relations. The part of speech here is the category of the synset, noun or verb or adjective or adverb. It is not the part-of-speech mask on a token in a sentence. That mask belongs to [Universal Dependencies](Universal-Dependencies.md). A wordnet does not own the word. The word is observed from the wordnet.

Princeton WordNet 3.0 is the witness `WordNet 3.0`, lineage WordNet. The database files in `dict/` and the manual pages in `doc/man` are the release. Root `/vault/Data/Wordnet/WordNet-3.0`. Loaded measure: 2,639,563 compositions from 38 MB. `WordNet-3.0.tar.gz` is that release again. The recipe's deviation is 35, and the recipe says the specification does not give that number.

The Collaborative Interlingual Index attests an interlingual key and the maps from wordnet sense keys onto it. Its definitions are Princeton WordNet's. Lineage is WordNet, so those definitions are not a second witness of the gloss. The key is the hop [Pull](../../Semantics/Pull.md) describes: bubble up to the index, change language, bubble down. The recipe reads the refresh extract. Loaded measure: 6,055,916 compositions from 100 MB. The map `ili-map-pwn30.tab` was measured at 117,659 rows, 117,587 distinct sense keys, no missing keys, no duplicate keys ([Semantics Experiments](../Semantics-Experiments.md#the-identifier-highway)). Deviation 35, the recipe's choice.

Open English WordNet is a later English wordnet, lineage WordNet, witness named by the lexicon's own first label. The recipe reads the refresh `OpenEnglishWordNet-2025-plus` release. There is no live directory. Loaded measure: 4,489,027 compositions from 103 MB. It is the same mask as Princeton WordNet 3.0, not an independent publisher of the 3.0 glosses. Deviation 35.

Open Multilingual Wordnet 2.0 is one witness per language, each named by that lexicon's first label, read from the refresh release after CILI and Open English WordNet. Loaded measure: 29,072,501 compositions from 597 MB. Deviation 90, the recipe's choice. `/vault/Data/omw` and `/vault/Data/OMW` are two checkouts of the build repository. A recursive diff of those trees reports `.git/index` only (measured). The build repository is not the 2.0 release the recipe reads.

Fanout is the number of pointers leaving a synset and the number of languages leaving an interlingual index. [Pull](../../Semantics/Pull.md) caps that fanout. Two senses that share a hypernym are one hop apart when that pointer is in the graph. None of these files attest a dependency role.

## Files, breakdown, and caveats

Taken from the recipe files. A line in a block is a directive. The prose above it is that file's own account of what is read, what is not, and what a row becomes.

### `princeton-wordnet/cntlist-rev.recipe`

cntlist.5: "The cntlist.rev file contains the same fields described above, in the following order:   sense_key  sense_number  tag_cnt"

```text
match cntlist.rev
grammar table
separator space
columns sense_key sense_number tag_cnt
claims
together
subject in sense_key
attest sense_number tag_cnt
```

### `princeton-wordnet/cntlist.recipe`

cntlist.5: "The fields are separated by one space", and   "Each line in cntlist is of the form:   tag_cnt  sense_key  sense_number" Every row says of its sense_key its tag_cnt and its sense_number. The sense_key is recorded whole (see index.sense).

```text
match cntlist
grammar table
separator space
columns tag_cnt sense_key sense_number
claims
together
subject in sense_key
attest tag_cnt sense_number
```

### `princeton-wordnet/data.recipe`

The database's data files, a synset on every line. wndb.5: "All fields, unless otherwise noted, are separated by one space character", and, of the lines that begin each file, "These lines all begin with two spaces and the line number": a line that begins with a space is not a row. The format wndb.5 gives:   "synset_offset  lex_filenum  ss_type  w_cnt  word  lex_id  [word  lex_id...]  p_cnt  [ptr...]  [frames...]  |  gloss"  READ: the fields that begin every line, and the first word, each said of the line's synset under the field's own name, together, as one record. The synset is the path of its synset_offset and its ss_type; wndb.5: "Each synset in the database can be uniquely identified by combining the synset_offset for the synset with a code for the syntactic category (since it is possible for synsets in different data.pos files to have the same synset_offset)." In data.adj a line's ss_type is a or s, and the pointers that point to a synset whose line says s write a for it ("& 00003553 a 0000", where the line of 00003553 says s): the path recorded here is the one the synset's own line writes.  NOT READ, because the table reader cannot say it (every line of these files holds parts that are not read):   lex_id                    of the first word: it is said of the word within the synset, not of the synset   [word lex_id...]          the second word to the last: w_cnt of them, so nothing after the first stands at a                             fixed place in the line   p_cnt  [ptr...]           the pointers, each "pointer_symbol  synset_offset  pos  source/target"   [frames...]               in data.verb, "f_cnt  +  f_num  w_num  [ +  f_num  w_num...]"   |  gloss                  the text after the vertical bar, to the end of the line   the syntactic marker      in data.adj wndb.5 says a marker "is appended, in parentheses, onto word without any                             intervening spaces": the first word is recorded as written, marker and all

```text
match data.noun data.verb data.adj data.adv
grammar table
separator space
comment   # the character after "comment " is a space
columns synset_offset lex_filenum ss_type w_cnt word lex_id
claims
together
subject in synset_offset ss_type
attest lex_filenum w_cnt word
```

### `princeton-wordnet/exceptions.recipe`

The exception lists. wndb.5: "The first field of each line is an inflected form, followed by a space separated list of one or more base forms of the word. There is one exception list file for each syntactic category." wndb.5 gives these fields no names. Each claim is the inflected form, the syntactic category the file's name gives (noun.exc: noun), and a base form; a line that lists several base forms says each. The name after "columns" is this recipe's handle for the first field; it is never recorded.

```text
match noun.exc verb.exc adj.exc adv.exc
grammar table
separator space
columns inflected
claims
predicate-in-name ^ .
subject in inflected
rest values
```

### `princeton-wordnet/html.recipe`

The manual pages as HTML (each says it was generated from the manual page's source by PolyglotMan). Recorded as the file's syntax tree, every byte as written; nothing is attested from them.

```text
match *.html
grammar html
```

### `princeton-wordnet/index-sense.recipe`

The sense index. senseidx.5: "fields are separated by one space", and   "Each line is of the form:   sense_key  synset_offset  sense_number  tag_cnt" Every row says of its sense_key what each other field holds, under the field's own name. Not read: the parts of the sense_key itself. senseidx.5 writes it lemma%lex_sense, and lex_sense ss_type:lex_filenum:lex_id:head_word:head_id; the table reader has no way to part a field at % and : and name the parts by their position. The sense_key is recorded whole, as written.

```text
match index.sense
grammar table
separator space
columns sense_key synset_offset sense_number tag_cnt
claims
together
subject in sense_key
attest synset_offset sense_number tag_cnt
```

### `princeton-wordnet/index.recipe`

The database's index files, a word on every line. wndb.5: "All fields, unless otherwise noted, are separated by one space character"; the lines that begin each file "all begin with two spaces and the line number": a line that begins with a space is not a row. The format wndb.5 gives:   "lemma  pos  synset_cnt  p_cnt  [ptr_symbol...]  sense_cnt  tagsense_cnt   synset_offset  [synset_offset...]"  READ: synset_cnt and p_cnt, each said under its own name, together, as one record, of the path of the lemma and its pos; wndb.5: "All remaining fields are with respect to senses of lemma in pos."  NOT READ, because the table reader cannot say it (every line of these files holds parts that are not read):   [ptr_symbol...]                     p_cnt of them, so nothing after p_cnt stands at a fixed place in the line   sense_cnt  tagsense_cnt   synset_offset  [synset_offset...]   synset_cnt of them, in the order of the lemma's senses

```text
match index.noun index.verb index.adj index.adv
grammar table
separator space
comment   # the character after "comment " is a space
columns lemma pos synset_cnt p_cnt
claims
together
subject in lemma pos
attest synset_cnt p_cnt
```

### `princeton-wordnet/lexnames.recipe`

lexnames.5: "Each line in lexnames contains 3 tab separated fields ... The first field is the two digit decimal integer file number. ... The second field is the name of the lexicographer file that is represented by that number, and the third field is an integer that indicates the syntactic category of the synsets contained in the file." lexnames.5 gives these fields no names: each line is recorded as the tuple of its three fields, in its own order.

```text
match lexnames
grammar table
claims
row tuple
```

### `princeton-wordnet/man.recipe`

The manual pages, which document every file of the database and say what each pointer_symbol, ss_type, lex_filenum and frame number stands for; the release's own README, licence, authors, change log and installation instructions; the log grind wrote when it built the database (dict/log.grind.3.0); and the texts the browser shows (lib/wnres). Read as text, every byte as written (the manual pages are written in troff, and their markup is part of what is recorded). Nothing is attested from them.

```text
match *.1 *.3 *.5 *.7 *.man README LICENSE COPYING AUTHORS ChangeLog INSTALL license.txt log.grind.3.0
grammar text
```

### `princeton-wordnet/sentidx.recipe`

wndb.5: "Each line of the file sentidx.vrb contains a sense_key followed by a space and a comma separated list of example sentence template numbers, in decimal." wndb.5 names the first field sense_key and gives the list no name: each claim is a pair, the sense_key and a template number. One line (pet%2:35:00::) lists none. The sense_key is recorded whole (see index.sense). The names after "columns" are this recipe's handles for the fields; they are never recorded.

```text
match sentidx.vrb
grammar table
separator space
columns sense_key templates
claims
pair
subject in sense_key
object in templates
```

### `princeton-wordnet/source`

WordNet 3.0: Princeton University's database files (dict/) and the manual pages that document every one of them (doc/man). The witness is named as the README names the release: "This is the README file for WordNet 3.0"; the licence lines at the head of the database files say "WordNet 3.0 Copyright 2006 by Princeton University". The deviation is this recipe's choice (the one the other wordnets of this lineage were given); the specification does not give one. Measured when it was loaded: 2,639,563 compositions from 38 MB, at 750 bytes each with their indexes and standings.

```text
witness WordNet 3.0
lineage WordNet
deviation 35
root $LAPLACE_DATA/Wordnet/WordNet-3.0
```

### `open-english-wordnet/oewn.recipe`

```text
match english-wordnet-*.xml
like wn-lmf
```

### `open-english-wordnet/source`

Open English WordNet. The witness is named as the lexicon names itself. Measured when it was loaded: 4,489,027 compositions from 103 MB, at 750 bytes each with their indexes and standings.

```text
witness {first label}
lineage WordNet
deviation 35
root $LAPLACE_DATA/.refresh-*/OpenEnglishWordNet-2025-plus
```

### `open-multilingual-wordnet/omw-en.recipe`

The English wordnet of Open Multilingual Wordnet is Princeton WordNet 3.0.

```text
match omw-en.xml
lineage WordNet
deviation 40
like wn-lmf
```

### `open-multilingual-wordnet/omw.recipe`

```text
match omw-*.xml
like wn-lmf
```

### `open-multilingual-wordnet/source`

Open Multilingual Wordnet 2.0: wordnets of many languages, each its own witness, named as its lexicon names itself. Measured when it was loaded: 29,072,501 compositions from 597 MB, at 750 bytes each with their indexes and standings.

```text
witness {first label}
deviation 90
root $LAPLACE_DATA/.refresh-*/OMW-2.0/extracted/omw-*
```

### `cili/changes.recipe`

What changed between WordNet 3.0 and 3.1: every row says of its WordNet 3.1 synset what each column holds.

```text
match changes-in-wn31.csv
grammar table
separator ,
header
claims
subject in WN31
attest *
```

### `cili/ili.recipe`

The index and its maps, in Turtle.

```text
match *.ttl
like turtle
```

### `cili/maps.recipe`

The index's maps to the wordnets, as tables: a concept, and the synset it is in the wordnet the file's name gives. The older maps were constructed automatically, and give each row a score.

```text
match ili-map-pwn*.tab
grammar table
columns ili synset score
claims
predicate-in-name - .
subject in ili
object in synset
score in score
```

### `cili/senses.recipe`

Sense mappings: a synset, and a sense key it holds, in the wordnet the file's name gives.

```text
match pwn*.tab
grammar table
columns synset sense
claims
predicate-in-name ^ .
subject in synset
object in sense
```

### `cili/source`

The Collaborative Interlingual Index: language-independent concept identifiers, their definitions, and their maps to the wordnets. The definitions are Princeton WordNet's. Measured when it was loaded: 6,055,916 compositions from 100 MB, at 750 bytes each with their indexes and standings.

```text
witness Collaborative Interlingual Index
lineage WordNet
deviation 35
root $LAPLACE_DATA/.refresh-*/CILI/extracted
```
