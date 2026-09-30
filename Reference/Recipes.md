# Recipes

A source is a directory under `recipes/` holding a `source` file and a recipe for each kind of file the source comes in; a recipe names the grammar a file decomposes by and, for a curated source, the claims it attests; the file `order` lists the sources in the order they go in.

The grammar of both files is the top comment of `Laplace-Engine/src/recipe.c`; this page is that grammar, directive by directive, with what each does in the engine. A line is one directive; `#` begins a comment; a name of several words is written between double quotes; `$NAME` in a path is read from the environment, with `LAPLACE_DATA` and `LAPLACE_MODELS` defaulting when unset; `*` in a root takes the newest of several.

## The source file

| Directive | Meaning |
| --- | --- |
| `name NAME` | the source's name, the name `laplace ingest NAME` and `order` use |
| `witness NAME...` | who testifies when this source attests, named as content: the witness's ID is the ID of that text. `{dir}` is the directory a file is in; `{name}` its own name without what follows its last dot; `{first NAME}` what the file first writes as `NAME="..."` |
| `lineage NAME...` | the witness it derives from; copies of one lineage play one matchup per claim, each copy still a row in the ledger |
| `trust T` or `deviation D` | how far the witness is trusted, −1 to 1, or given as the deviation it plays with, `trust = g(D / 173.7178)` |
| `root PATH` | where the source is kept; several may be given and the first that exists is the source |
| `files PATTERN` | the files it is, when not everything under a root; several may be given |
| `except PATTERN...` | files under its root that are not the source |
| `room N` | what it takes in the database, in times what its files hold, as measured; used by the room check |
| `after SOURCE...` | the sources it comes after; `order` is the total order |
| `reads FORMAT...` | its files are ordinary content, read as these formats, the recipes that belong to no source |

A recipe of a source takes the source's witness, lineage, and trust unless it names its own.

## The recipe file

### Identity and grammar

| Directive | Meaning |
| --- | --- |
| `name NAME` | |
| `match GLOB...` | files it applies to, by file name; a glob with a directory in it, `annotated/train-*`, by the end of the path |
| `grammar text \| vocabulary \| table \| lines \| fields \| NAME` | UAX #29 text; a tokenizer's vocabulary; a table of rows and fields; lines matched by patterns; records of `KEY IS VALUE` lines; or a tree-sitter grammar loaded as `$LAPLACE_GRAMMARS/libtree-sitter-NAME.so` |
| `like RECIPE` | reads as that recipe does, the same grammar and statements, under its own name, witness, lineage, and trust |
| `trust T`, `deviation D`, `witness NAME...`, `lineage NAME...`, `predicate TEXT` | as for the source, for this recipe alone |
| `records` | the file is a flat sequence of line-terminated records: large files are split at line boundaries, parsed on every core, and joined under one root |
| `unit BYTES` | queries run on the parts of the syntax tree no larger than this, default 65536, in reading order, so a pattern matches inside one record and the work is bounded by the record |
| `itself CHAR` | a character the source writes, in an object, for the subject's own codepoint |
| `subject-attribute A [F L]` | for `@subject.attr`: the subject is the codepoint in sibling attribute `A` of the captured node's parent, or the element itself when it carries `F` and `L`, a range attested at its element and never copied to each codepoint |
| `paths CHAR [CHAR]` | a value beginning with the first character is a path, the tuple of its parts, `/c/en/dog` is `[c, en, dog]`; with a second, a part's words are joined by it, `ice_cream` is `[ice, cream]` |

### A table

| Directive | Meaning |
| --- | --- |
| `separator tab \| CHAR` | what parts a row's fields; tab unless said |
| `header` | the first row names the columns |
| `columns NAME...` | the columns, when no row names them |
| `quoted` | a field may stand between double quotes, holding the separator or a line's end, a quote inside written twice |
| `escaped CHAR` | the character after it is itself; `CHAR` and `N` alone in a field is left as written, what the source leaves unknown |
| `skip N` | the first N lines are not rows |
| `comment CHAR` | a line beginning with it is not a row |
| `remark CHAR` | in a row, what follows it is not the row |
| `kind COLUMN KIND` | the column's values name things of a kind, a source's own numbers, each recorded as the path of the kind and the value; `{dir}`, `{name}` the file's |
| `kinds own` | a kind stands within the source: `[Tatoeba, Sentence id, 77]` |
| `voices within-file` | witnesses named by column stand within the file: `[witness, file, column]` |
| `list COLUMN CHAR` or `list COLUMN json` | a field of the column is several values parted by the character, or a JSON list of texts; `*` for every column |
| `empty TEXT` or `empty-matches PATTERN` | what the source writes in a field it leaves empty; an empty field attests nothing |

### A table whose rows come in records

For a treebank: a sentence, and a row for each word.

| Directive | Meaning |
| --- | --- |
| `record blank` or `record LINE` | rows up to an empty line, or up to that line, are one record |
| `note IS` | a comment line `KEY IS VALUE` says `VALUE` of the record under `KEY` |
| `about KEY` | the note that holds what the record is about |
| `word COLUMN` | each row is about the word in this column, within what the record is about |
| `number COLUMN [SPAN]` | the column that numbers the rows; `A SPAN B` is a row spanning rows A to B |
| `attest COLUMN...` | said of the word, under the column's name |
| `pairs COLUMN PART IS [LIST]` | the field holds `KEY IS VALUE` parts: each value said of the word under its key |
| `relation COLUMN to COLUMN` | the word's relation to the word the second column numbers |
| `relations COLUMN PART IS` | the field holds `HEAD IS RELATION` parts: further relations |

What is recorded (`records.c`): `[word, COLUMN, value]`, `[word, KEY, VALUE]`, `[word, relation, head word]`, `[token, [word, word…]]` for a spanning row, `[sentence, KEY, VALUE]` for a note. The rows form a tree by their heads; a word's node is the path of its dependents' nodes and its own in row order, each dependent's node after the claim that relates it, so a phrase analysed the same way is the same node wherever it occurs. The record is the path of what it is about, its notes, its spans, and its trees; it is what was witnessed, one ledger row, and every claim in it plays.

### XML read as what it says

| Directive | Meaning |
| --- | --- |
| `identity ELEMENT ATTRIBUTE` | an element is the thing its attribute names; `*` for any element carrying it; `.cp` a codepoint in hex, `.cps` several |
| `identity ELEMENT FIRST..LAST` | a range of codepoints, the path of its first and last |
| `identity ELEMENT >CHILD` | the thing the text of the child element names; `>CHILD.ATTRIBUTE` that element's attribute |
| `identity ELEMENT NAME within` | the name stands only within the thing the element is inside: the path of that thing and the name |
| `identity ELEMENT NAME kind [KIND]` | the name stands only among things of its kind: the path of the kind and the name; `.` is the element's own text |
| `refer [ELEMENT.]ATTRIBUTE KIND` | the attribute's value names a thing of that kind and is recorded as it |
| `words RECORD WORD...` | the element is a record of words: each word element's text is a word, its attributes said of the word within the record; what the record is about is the path of its words |
| `span ELEMENT START END TEXT [inclusive]` | the element speaks of a stretch of the text element between two characters |
| `list ATTRIBUTE CHAR` | an attribute of several values |
| `link ELEMENT A B [KIND]` | an element is a relation of the thing it is inside: `[thing, value of A, value of B]`; `>CHILD` for B is the text of each child |
| `codepoints ATTRIBUTE...` | attributes whose values are codepoints in hex, recorded as the text they are |

`{dir}` as a kind is the file's directory: a name that stands only within its data set.

### JSON read as what it says

| Directive | Meaning |
| --- | --- |
| `identity * KEY` or `identity UNDER KEY` | an object is the thing the first of these members it holds names, a text, a number, or a list of texts naming it together; `UNDER` restricts to objects under that key |
| `named KEY by KEY...` | an object holding the key is the thing those members name together, in order: `named word by lang_code word pos` is `[en, free, noun]` |
| `linkage` | what a thing inside another says, it says of being there: the claim `[thing, key..., thing inside]` |
| `specifics [claims under KEY...]` | what is held with a claim is its specifics, pairs of key and value, recorded together with the claim as what is witnessed and no claim of their own; under the named keys, claims of their own |
| `tuples` | a list of plain values inside a list is one tuple |
| `keys things` | the keys of an object inside nothing are things, each one's value speaking of it |
| `records` | a value on every line |

A claim is the path from a thing to a value, every key and value as written; an array says each value under the same path; `null` and an empty text say nothing. Everything a top-level value says it says together: one record, witnessed once.

### Lines and fields

| Grammar | Directive | Meaning |
| --- | --- | --- |
| `lines` | `about PATTERN` | the first matching line names what the file is about, its first part |
| `lines` | `line PATTERN` in a claims block | a matching line says its parenthesized parts: two are said of what the file is about, three are the claim; with `pair`, two are the pair; with `predicate NAME`, `[1, NAME, 2]` |
| `fields` | `record LINE`, `field IS`, `about KEY...` | records of `KEY IS VALUE` lines, a line beginning with a space continuing the one before; the record is about the first of the keys it holds, every other field said of it under its key |

### Maps and claims

| Directive | Meaning |
| --- | --- |
| `map NAME [from FILE GRAMMAR]` … `end` | patterns read over the whole file, or over another file by its grammar or as a `table`, before anything is attested; each match binds `@key` to `@value`, so a part written as one identifier can be recorded as what it stands for |
| `claims` | a kind of statement the source makes; what follows applies to it |
| `predicate TEXT` | the claims' predicate, when the source states it by position |
| `predicate-in-name A B` | the predicate is in the file's name, between its last `A` and the `B` after; `^` for `A` |
| `enter RATING DEVIATION` | the stock default a claim of this kind enters at; otherwise the rating of the unrated with the deviation its witness's trust plays with |
| `ordered` | each claim's position among its kind's claims in its record is recorded |
| `distinct` | a claim whose subject is its object is not one |
| `pair` | the claims are pairs `[subject, object]`; with no object, of the subject and what the file's name says |
| `together` | in a table: what a row says it says together, the row one record witnessed once and its claims within it |
| `itself` | what the row attests is its subject itself, a review of a sentence |
| `json COLUMN` | the field is a JSON object speaking of the row's claim; `witnesses KEY...` the path of keys to who witnessed it, each a witness of its own |
| `witness in COLUMN` | who says the row; each is a witness of its own |
| `score in COLUMN [from A to B]` | the score the row gives, on the source's scale, `A` a loss, `B` a win, halfway a draw; a win when it gives none |
| `subject in COLUMN[.resolver...]`, `predicate in COLUMN`, `object in COLUMN`, `key in`, `value in` | the parts by column; several columns for the subject make it the path of them all |
| `subject-kind KIND` | the subject's name stands only among things of its kind |
| `rest pairs \| values` | the fields after the named columns come in predicate-object pairs, or are each an object |
| `voices COLUMN... \| NAME*` | each column a witness named by the source and the column, its field what that witness says of the subject |
| `row tuple` | the row itself is the claim, the path of its fields |
| `fields pairs CHAR` | every field is `A CHAR B`, the pair `[A, B]`, said together |
| `where COLUMN is \| is-not \| matches VALUE` | the rows it speaks of |
| `attest COLUMN... \| * \| NAME*` | each column a predicate by its name, its field the object |
| `query` … `end` | tree-sitter query patterns; every match attests one claim from `@subject`, `@predicate`, `@object`, each with resolvers after a dot |

Resolvers: `.cp` a codepoint in hex; `.text` the node's text, quotes and surrounding spaces stripped; `.head` the text before its first colon; `.iri` an identifier without its angle brackets; `.tag` a tag after `@`; `.term` a Turtle term as what it stands for; `.cps` codepoints in hex as text; `.range` a codepoint, a sequence, or `FIRST..LAST` as the path of its ends; `.xml` with references resolved; `.node` the node itself as recorded; `.NAME` then looked up in map `NAME`, a part no map holds attesting nothing. Predicates: `#eq?`, `#not-eq?`, `#any-of?`, `#not-any-of?`, `#match?`, `#not-match?`.

Nothing is renamed: every name and value is recorded as the source writes it.

## How a file is recorded

With a grammar, a file is recorded as its syntax tree: each node the composition of its children with the bytes between them kept as text, so it recomposes byte for byte; leaves are text, decomposed by UAX #29. A file's trunk is `[metadata, content]` (`file.c`): the metadata vertex, marked `LP_SAID_METADATA`, is the file's name as written, its path under its source's root or its own name when given by itself, never where the source is kept on this machine; the content is the text, the syntax tree, or the vocabulary; for a curated file, what it witnessed in the order it was read, each record or claim marked `LP_SAID_RECORD` or `LP_SAID_CLAIM`, composed as one record when there are several. A curated file that witnessed nothing has nothing of it to record. A file's tier is one above its highest constituent; every composition's tier is one above its highest child's. The trunk is written last of everything the file is and attests, so a recorded trunk means all of it is recorded.

A tokenizer vocabulary (`vocab.c`): each token is the text it stands for, byte-level BPE characters mapped back to bytes by GPT-2's table, SentencePiece's `▁` a space, WordPiece's `##` continuing a word, a byte token or one that is not valid UTF-8 by itself the notation `<0xAB>` of each byte; the vocabulary is the path of its tokens in index order; the token list itself is kept as the model wrote it.

## The stock recipes

Format recipes that belong to no source, which any source's `reads` may name and which `laplace ingest FILE` uses by extension:

| Recipe | Matches | Grammar |
| --- | --- | --- |
| `text` | `*.txt *.md` | `text`: UAX #29 codepoint, grapheme, word segment, sentence, paragraph, file |
| `xml` | `*.xml` | `xml` as its syntax tree, leaves text |
| `json` | `*.json` | `json` as its syntax tree |
| `turtle` | | `turtle`: every statement `[subject, predicate, object]` as written; a literal with a language tag or datatype also `[text, tag]` or `[text, datatype]`; blank nodes and collections not read |
| `vocabulary` | `tokenizer.json` | `vocabulary` |
| `wn-lmf` | | `xml` with `records`, `identity LexicalEntry >Lemma.writtenForm`, `identity * id`, `link SenseRelation relType target`, `link SynsetRelation relType target`: a lexical entry is the word its lemma writes, everything else with an id is what that id names, and what is inside a thing is said of it |

Source directories in the estate: `unicode` (23 recipes), `iso-639` (10), `cili`, `open-english-wordnet`, `open-multilingual-wordnet`, `princeton-wordnet`, `propbank`, `verbnet`, `framenet`, `semlink`, `predicate-matrix`, `mapnet`, `verbatlas`, `wordframenet`, `universal-dependencies-tools`, `universal-dependencies-documentation`, `universal-dependencies`, `wsd-evaluation-framework`, `wiktionary-kaikki`, `wiktionary`, `conceptnet`, `atomic-2020`, `framebase`, `atomic-10x`, `tatoeba`, `opensubtitles`, `project-gutenberg`, `tokenizers`, `geonames`, `hatecheck`, `sghatecheck`, `xstest`, `social-bias-frames`, `social-chemistry-101`, `prosocial-dialog`, `real-toxicity-prompts`, `toxigen`, `measuring-hate-speech`, `civil-comments`: the order of `order`.

A worked example, `universal-dependencies/conllu.recipe`:

```text
name conllu
match *.conllu
grammar table
columns ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC
comment #
record blank
empty _
note =
about text
word FORM
number ID -
attest LEMMA UPOS XPOS
pairs FEATS | = ,
pairs MISC | =
relation DEPREL to HEAD
relations DEPS | :
```

A sentence is a record whose `# text = …` note is what it is about; every row is about its `FORM` within that sentence; `LEMMA`, `UPOS`, and `XPOS` are attested under those names; `FEATS` and `MISC` are `KEY=VALUE` parts split on `|`; `DEPREL` relates the word to the row `HEAD` numbers; `DEPS` holds further `HEAD:RELATION` parts; `_` is empty; a row `A-B` spans rows.

## Where recipes are checked

`laplace tree FILE` shows a file's syntax tree as its grammar reads it. `laplace ingest --plan` shows which recipe takes which file; `--claims` prints every claim as text and loads nothing; `--no-load` decomposes and checks recomposition without writing. A recipe that does not load stops its own source and no other. When a unit holds more partial matches than a query keeps, ingestion says so.
