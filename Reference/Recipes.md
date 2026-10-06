# Recipes

A source is a directory under `recipes/` holding a `source` file and a recipe for each kind of file the source comes in; a recipe is configuration, the layout or grammar that gives a file its tree and what each named part of that tree is, read by one decomposer; the file `order` lists the sources in the order they go in.

There is one decomposer (`Laplace-Engine/src/structure.c`) and one reading of what a file's parts are (`say.c`); no code names a format or a source. A line is one directive; `#` where a line begins or after a space begins a comment, outside a name written between double quotes; a name of several words is written between double quotes; `$NAME` in a path is read from the environment, with `LAPLACE_DATA` and `LAPLACE_MODELS` defaulting when unset; `*` in a root takes the newest of several. A recipe line the engine does not know stops the recipe's load and says which line.

## The source file

| Directive | Meaning |
| --- | --- |
| `name NAME` | the source's name, the name `laplace ingest NAME` and `order` use |
| `witness NAME...` | who testifies when this source attests, named as content: as built, the witness's ID is the ID of that text; the law makes the witness the source trunk and that name content inside its source record. `{dir}` is the directory a file is in; `{name}` its own name without what follows its last dot; `{first NAME}` what the file first writes as `NAME="..."`. With these, as built, every directory or file is a witness of its own, a treebank, a lexicon, a dataset; the law makes the corpus one source trunk and one witness, and a treebank, a lexicon or a dataset files under it, with their paths |
| `lineage NAME...` | the witness it derives from; copies of one lineage play one matchup per claim, each copy still a row in `attestation` |
| `class NAME` | the witness's trust class, one that `Laplace-Native/manifest/trust_classes.toml` declares; the class's prior is the trust its claims play at. A class the manifest does not declare, or a trust written as a number (`trust`, `deviation`), stops the load with status 2 |
| `root PATH` | where the source is kept; several may be given and the first that exists is the source |
| `files PATTERN` | the files it is, when not everything under a root; several may be given |
| `except PATTERN...` | files under its root that are not the source |
| `room N` | what it takes in the database, in times what its files hold, as measured; used by the room check |
| `called NAME` | the source's record, where its witness is named file by file: the first part of its trunk |
| `after SOURCE...` | the sources it comes after; `order` is the total order. A source asked for by name is run after every source it comes after, each its own run; one whose prerequisite did not go in is not begun |
| `reads FORMAT...` | its files are ordinary content, read as these formats, the recipes that belong to no source |

A recipe of a source takes the source's witness, lineage, and trust unless it names its own.

## The recipe file

### Which files, and what gives them a tree

| Directive | Meaning |
| --- | --- |
| `name NAME` | |
| `match GLOB...` | files it applies to, by file name; a glob with a directory in it, `annotated/train-*`, by the end of the path; the most specific pattern wins |
| `grammar text \| NAME` | UAX #29 text, or a tree-sitter grammar loaded as `$LAPLACE_GRAMMARS/libtree-sitter-NAME.so` |
| `format NAME` | the grammar and what each kind of its nodes is, kept once for every recipe of that format in `recipes/formats/NAME.format` (`xml`, `json`, `turtle`) |
| `like RECIPE` | reads as that recipe does, its layout and dispositions, under its own name, witness, lineage, and trust |
| `class NAME`, `witness NAME...`, `lineage NAME...` | as for the source, for this recipe alone |

A recipe that names only a grammar records each file as its syntax tree, byte for byte. A recipe that lays a file out (tiers, or a grammar's node rules) and says what its parts are is a curated source.

### The layout: tiers

A file is laid out in tiers, outermost first, each parted from the next by what the recipe writes. What follows a `tier` line is said of that tier.

| Directive | Meaning |
| --- | --- |
| `tier NAME by SEP` | the file, or the tier above, is NAMEs parted by SEP: `\n`, `\n\n`, `\t`, a character, a word, or `space`, `tab`, `hash` by name |
| `names A B C ...` | the parts of the tier below have these names, by position |
| `header` | the first part of the file names the positions of the tier below, and is no part itself |
| `skip N` | the first N parts are not parts |
| `note PREFIX [IS]` | a part that begins with PREFIX is a note: `KEY IS VALUE` when IS is written in it |
| `comment PREFIX` | a part that begins with PREFIX is not read |
| `remark CHAR` | in a part, what follows CHAR is not read |
| `quoted` | a part of the tier below may stand between double quotes, a quote in it written twice |
| `padded` | the parts of the tier below are written with spaces around them that are not theirs |
| `is SEP` | each part of this tier is written `KEY SEP VALUE`: the part is named KEY |
| `continued` | a part that begins with white space goes on with the one before it |
| `escaped CHAR` | the character after CHAR is itself, a tier's separator included |
| `part PATH by SEP [is IS] [pieces N] [space CHAR]` | a named part is itself parts, parted by SEP; with `is`, each is `KEY IS VALUE`; with `pieces`, at most N, the last the rest as written; with `space`, CHAR in it stands for a space. `by json`: a JSON list of texts; `by object`: a JSON value read into the tree, each member under its key. `PATH*` is every part whose name begins so |
| `empty TEXT...` | what the file writes where it leaves a part empty; an empty part says nothing |

A file laid out in tiers whose outermost parts are lines or end at an empty line, and whose parts point at no other part of the file, is read a stretch at a time when it is longer than a batch, provided its recipe is curated and has no header, no quoted outermost tier and no `split`.

### The layout: a grammar's nodes

A grammar gives the tree; the recipe, or the format file it names, says what each kind of node is in it.

| Directive | Meaning |
| --- | --- |
| `node TYPE group [name PATH...] [list] [kind]` | it holds nodes; its name is the text at the first PATH there is (`A/B`: the B in its A); in a `list`, its values and groups are named by it; with `kind`, it is named by its type |
| `node TYPE value name PATH text PATH` | a name and its text |
| `node TYPE text [raw] [join] [kind]` | a text, under the name of what holds it; with `join`, texts side by side are one text; `raw`, as written |
| `node TYPE member name FIELD value FIELD` | it names what its other part is: that part, read as its own kind, under the name |
| `node TYPE skip` | it and what is inside it are not of the tree |
| `resolve xml \| json \| turtle` | how the grammar's texts write what they cannot write plainly |
| `trim` | the white space a text begins and ends with is the file's layout, not the text's |
| `levels NAME...` | an object's members at each depth, whose keys are what the file says (a roleset, a class number), are parts of that name, each holding its `key` and its `value` |
| `split ELEMENT...` | a long file of records each an element on lines of its own is parted before each line that begins one, each part parsed on every core |

A tree-sitter field names a child that has no name of its own; a group named by its rule keeps its own name. A group that holds nothing named holds its own text. A kind the recipe says nothing of is passed through: what is inside it stands where it stands.

### What each named part is

| Directive | Meaning |
| --- | --- |
| `content NAME...` | the part is content, the text it is, the same entity wherever that text stands |
| `key TIER NAME` | the part is the file's internal pointer for a TIER: it resolves to the TIER's thing, and is written nowhere; the source's other files may refer to it. A highway ID is never a `key`: it is content ([Corpora](../Corpora/README.md#page-shape)) |
| `refer NAME TIER [within] [TIER...]` | the part's text is a pointer to a TIER, here or in another recipe of the source: it is read as that thing (`within`: as the thing that TIER is inside); several targets, the first that holds the pointer; a pointer nothing holds says nothing and is counted |
| `type NAME LIST... [matching PATTERN] [as TEMPLATE]` | the part's text is a resource's identifier of a type in the highway's LIST, read as that type; several lists, the first that knows it; with a pattern, the identifier as those lists write it (`vn:51.2` read as `51.2`), and a text the pattern does not match is no identifier of theirs; an identifier no list knows is counted and said, never taken for text. For a pointer to a type, a WordNet offset, a BabelNet id, an FE's number, that is the law: resolved and written nowhere. For a highway ID, `i46360`, `abandon.01`, `leave-51.2`, the claim as built holds the type's content and not the ID's text; the law keeps the hub as content, as written, the type's slot only an index over it |
| `metadata NAME...` | the part is said of the file itself: it goes in the file's metadata tree |
| `omit NAME...` | the part is the file's bookkeeping, read by nothing, nor anything inside it |
| `perfcache` | after the layout (`format`, `tier`): a part named as a property the flags perf-cache holds (`tier0.flags`, by its name or its long name, matched loosely) is read from the flags for every codepoint and not attested again; the flags must be generated |
| `own NAME...` | the part's value stands only within the source: `[witness, NAME, value]`. As built, that path is a witness of its own, an annotator, a worker, a speaker or a member named inside the corpus; the law makes it content, the corpus the witness, and what the corpus reports of it, this annotator labelled this case, a relation the corpus attests |
| `codepoints NAME...`, `range NAME...` | code points written in hex, as the text they are; `FIRST..LAST` the path of the two |

Names are written as the file writes them. `ELEMENT.NAME` is that part of that element only; `NAME*` is every name that begins so; `note:NAME` is a note of that name, and `note:*` every note. A named part the recipe gives no disposition is an obligation left open: it is counted and its name said, never taken for content and never dropped in silence.

### Paths

Wherever a line names a part, it may name it by a path from the part being read: `A/B` the B in its A; `^` what it is inside; `^NAME` the nearest part of that name it is inside; `N` its Nth part, counted from 1 (`start/3` is `ice_cream` in `/c/en/ice_cream/n`); `NAME[CHILD=VALUE]` a part of that name whose CHILD is written VALUE (`property[predicate=skos:definition]`); `.` the part itself.

### What a part is the thing of

| Directive | Meaning |
| --- | --- |
| `thing TIER NAME...` | a TIER is the thing its part NAME names; named by several parts together, it is the path of them; several `thing` lines for one TIER are tried in turn |
| `thing TIER NAME... within` | its name stands only within the thing it is inside: the pair of that thing and it |
| `thing TIER NAME... within-file` | its name stands only within the file: `[the file's name, it]` |
| `thing TIER span START END TEXT [inclusive]` | the stretch of the text TEXT between the characters START and END, counted as code points |
| `thing TIER NAME... of` | the path of the things of its parts of these names, in the file's order (a sentence of its words) |
| `thing TIER .` | the part itself, whole |

### What a file attests

| Directive | Meaning |
| --- | --- |
| `attest TIER NAME... [of PATH] [by PATH]` | of a TIER's thing, what each part NAME says, under the part's own name: `[thing, NAME, value]`; a part of `KEY IS VALUE` parts says each VALUE under its KEY; `.` its own text; `*/` each element inside it that is a value; `of`: said of another of its parts; `by`: said by the witness each part at the path names, every one of them, as built; the law keeps the corpus the witness and makes what each one named said a relation the corpus attests, and by the source where none is named |
| `relate TIER NAME to NAME [alone] [by PATH]` | of a TIER's thing, its relation (the first part's value) to what the second part is: `[thing, relation, other]`; several parts of that name, the relation to each; `...` each part the file gives no name; `{file}` the relation the file's own name gives; with `alone`, where the second names nothing, `[thing, relation]` |
| `pair TIER NAME... [of PATH]` | what the file writes beside the thing with nothing between: `[thing, value]`; a list, the pair with each; `{file}` what the file's name says |
| `holds TIER NAME... [via]` | the nearest things of these names inside it: `[thing, name, inner thing]`; `via`: under the name of the element between the two |
| `itself TIER [by PATH]` | the TIER's thing is itself the claim (a tuple that is a statement), said by the witness each part at the path names |
| `voices TIER NAME... [within-file]` | each part is a witness of its own, saying its value of the thing: `[witness, NAME]`, or within the file `[witness, file, NAME]`. That is as built; the law makes each annotator content and the corpus the witness, and what each part says a relation the corpus attests |
| `voice TIER NAME` | who says everything the part says |
| `together TIER` | what the part and everything inside it say is one record, the thing first, witnessed once, its claims within it |
| `score TIER NAME [from A to B]` | the score the part gives what it attests, on the scale the source writes it on: A a loss, B a win, halfway a draw |
| `where NAME is VALUE \| is-not VALUE \| matches PATTERN` | the outermost parts the recipe speaks of; another is in the file's tree and attests nothing |
| `when NAME is \| is-not \| matches ...`, `always` | the lines after it are said only of the parts that meet it, several met together, up to `always` |
| `stem [FROM] TO` | what `{file}` stands for: the file's name after its last FROM, up to the TO after it |
| `itself-mark CHAR` | what the source writes, in a value, for the code point the part is |
| `about PATTERN` | of a page: the first line that matches names what the page is about |
| `line PATTERN [:: pair \| claim \| predicate NAME]` | a line that matches says its parenthesized parts: two of what the page is about, the pair, the claim itself, or `[1, NAME, 2]` |

Nothing is renamed: every name and value is recorded as the source writes it.

### The highway

A resource's recipe says which of its things are types and what it maps between them; `laplace highway` reads every source that says any, in order, by the same decomposer, so a type's ID is the very thing its recipe composes for it when the source is ingested ([Types](Types.md)).

| Directive | Meaning |
| --- | --- |
| `types LIST "SAY" TIER` | each thing of TIER is a type of the highway's LIST, in the order the files write them (a text of a list is a type by itself) |
| `keyed LIST TIER PATH [matching PATTERN] [as TEMPLATE]` | the value at PATH is a resource's identifier of that type, as those who point at it write it |
| `alias LIST TIER PATH [matching ...] to PATH [matching ...]` | an identifier that names the type another identifier names (a sense key and its synset's offset) |
| `maps TIER PATH LIST [matching ...] to PATH LIST [matching ...]` | an edge between the type one identifier names and the type another names |

A pattern is POSIX extended; a template writes `\0` the whole match and `\1` to `\9` its parts; with no template, the first part, or the whole. What names no type of its list is left out and said, by lists, with an example.

## How a file is recorded

A file's trunk is `[metadata, content]`. The metadata tree is the OS's record of the file, its parts as the OS names them (`pathname`, a composition of its filenames; `filename`; and what `statx` returns, `stx_mode` to `stx_mtime`), each `[name, value]` and each disposed of by the file's recipe or, where that says nothing of it, by the stock recipe `file` (`metadata` or `omit`); then what the recipe says is said of the file itself. A part neither disposes of is said once and not recorded. The content tree is the file's own tree. A file a recipe records only by its grammar is its syntax tree, each node the composition of its children with the bytes between them kept as text, so it recomposes byte for byte; leaves are text, decomposed by UAX #29. A curated file's content is the whole of each of its outermost parts as its recipe reads them, in the file's order, each the claim it is where it is one; a few thousand are one path, and more are factored into blocks from the content alone: a block ends after a part whose own ID says so, never at a count or a position, and the blocks are composed the same way, level by level, until one holds them all. A file's tier is one above its highest constituent. The trunk is written last of everything the file is and attests, so a recorded trunk means all of it is recorded.

A source's trunk is `[record, content]`: the record is the witness its `source` file names, or its `called` line where the witness is named file by file; the content is its files' trunks in the order of their paths. It is written after the last of its files, in a load of its own, and found recorded like any other trunk, by its ID. By the law this trunk is the witness, and the trust and lineage are keyed by the trunk; as built the witness is the named record. Provenance is the `attestation` table, a row per claim and witness, and it stays: provenance by containment, a record a path over the claims it asserts under its file's content tree, is the target, and replaces the table only once a working prototype on real data shows, side by side with it, that containment answers everything the table answers, who said a claim, its games, score and position, its qualifiers, forgetting and replay, with nothing lost.

## The stock recipes

Format recipes that belong to no source, which any source's `reads` may name and which `laplace ingest FILE` uses by extension:

| Recipe | Matches | Reads |
| --- | --- | --- |
| `text` | `*.txt *.md` | UAX #29 codepoint, grapheme, word segment (a separator separates at the word tier, [Types](Types.md#segmentation)), sentence, paragraph, file |
| `xml` | `*.xml` | its syntax tree, leaves text |
| `json` | `*.json` | its syntax tree; a tokenizer's `tokenizer.json` is read so, its vocabulary the members that name each token and give its number |
| `turtle` | | `format turtle`: a statement is its subject; its property is the relation to its objects; a literal says its language tag or datatype |
| `wn-lmf` | | `format xml`: a lexical entry is the word its `Lemma` writes; a synset is the composition of the words its `members` are; a sense is the word with its synset; `ili` a type of the highway's interlingual index |
| `file` | | no layout: what the OS keeps of every file, `metadata pathname filename stx_mode stx_uid stx_gid stx_nlink stx_ino stx_size stx_blocks stx_blksize stx_attributes stx_dev_major stx_dev_minor stx_rdev_major stx_rdev_minor stx_btime stx_ctime stx_mtime`, `omit stx_atime` (reading the file changes it) |

A worked example, `universal-dependencies/conllu.recipe`:

```text
name conllu
match *.conllu
tier record by \n\n
tier row by \n
note hash =
names ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC
tier field by \t
empty _
part FEATS by | is =
part MISC by | is =
part DEPS by | is :

thing record text
thing row FORM
content text FORM LEMMA XPOS DEPREL DEPS FEATS MISC
type UPOS upos
key row ID
refer HEAD row
metadata "newdoc id" "newpar id" sent_id note:newdoc* note:meta::* ...
content note:*

attest row LEMMA UPOS XPOS FEATS MISC
attest record note:*
relate row DEPREL to HEAD alone
```

A record is the sentence its `# text = ...` note writes; a row is the word its `FORM` writes; `ID` numbers the rows of one record and `HEAD` points at a row by it, positions within the sentence, never part of an ID; `UPOS` is a type of the highway; what the file writes about its documents is its metadata tree; every other note is what the treebank says of the sentence under the note's name; `DEPREL` relates the word to the row `HEAD` numbers, and to nothing, alone, for the root.

## Where recipes are checked

`laplace structure LAYOUT FILE` shows a file's tree as a layout parts it. `laplace tree FILE` shows a file's syntax tree as its grammar reads it. `laplace ingest --plan` shows which recipe takes which file; `--claims` prints every claim as text and loads nothing; `--no-load` decomposes and checks recomposition without writing, and says every named part left open and every identifier no list of the highway holds. A recipe that does not load stops its own source and no other.
