# Recipes

A source is a directory under `recipes/` holding a `source` file and a recipe for each kind of file the source comes in; a recipe is configuration, the layout or grammar that gives a file its tree and what each named part of that tree is, read by one decomposer; the file `order` lists the sources in the order they go in.

There is one compiled structure reader (`Laplace-Engine/src/structure_compile.c`, `structure_records.c`, `structure_decode.c`) and one compiled statement VM (`recipe_compile.c`, `recipe_says.c`, `say.c`); no code names a format or a source. A line is one directive; `#` where a line begins or after a space begins a comment, outside a name written between double quotes; a name of several words is written between double quotes; `$NAME` in a path is read from the environment (`LAPLACE_DATA`, `LAPLACE_MODELS`); `*` in a root takes the newest of several. A recipe line the engine does not know stops the recipe's load and says which line.

For a curated source, reading is extraction: the recipe takes the raw product, the content and what the source states, out of the packaging, its formats, records and layout, which stay as provenance with their trunks. Every container format is parsed by its compiled Tree-sitter grammar (`tree-sitter-xml`, `tree-sitter-json`, `tree-sitter-turtle`, `tree-sitter-csv`/`tsv`/`psv`, `tree-sitter-conllu`, `tree-sitter-wndb`, `tree-sitter-pgn`, plus 300+ code grammars), chaining into child Tree-sitter grammars via `ts_parser_set_included_ranges` for fields with internal sub-syntax (`FEATS`, `DEPS`, `MISC`, `CxnElt`, `Functor`, embedded JSON, sense keys `drop%2:38:00::`, `mcr:ili-30-01976841-v`) down to UAX #29 text leaves and `tier0.bin` / `highway.bin`. `.format` and `.recipe` rules (including declarative `tier NAME by SEP` layouts compiled by `layout_compile_tiers` into `lp_records`, `lp_paragraphs`, `lp_conllu_records`, `lp_csv`/`lp_tsv`/`lp_psv`, or `wndb`) compile once at load time into $O(1)$ integer `TSSymbol`/`TSFieldId` jump tables and hash-indexed disposition programs; the intermediate `STree`/`SNode` heap DOM (`s_grammar_split` / `copy_around`), hand-rolled `tier_read` byte scanners, and per-node runtime string building (`child_path` / `records_of` heap churn) are retired. Content decomposes to codepoints for its identity; a claim attaches once, at the tier the source asserts it, never spread over the words below; an XML attribute is said of its element; a mapping row is one interchange strand, never a claim per column; and a default the format declares (`default FIELD VALUE`) attests nothing.

## The source file

| Directive | Meaning |
| --- | --- |
| `name NAME` | the source's name, the name `laplace ingest NAME` and `order` use |
| `witness NAME...` | who testifies when this source attests, named as content inside the source record (`[record, file trunks]`); `{dir}`, `{name}`, `{first NAME}` expand per file when needed for sub-record voices |
| `lineage NAME...` | the witness it derives from; copies of one lineage fold into one dependence root per claim while each witness trunk keeps its `attestation` row |
| `class NAME` | the witness's trust class, one that `Laplace-Native/manifest/trust_classes.toml` declares; the class's prior is the trust its claims play at. A class the manifest does not declare, or a trust written as a number (`trust`, `deviation`), stops the load with status 2 |
| `held REASON` | a source not yet supplied on disk: `laplace ingest --plan` reports `REASON` without failing |
| `root PATH` | where the source is kept; several may be given and the first that exists is the source |
| `files PATTERN` | the files it is, when not everything under a root; several may be given |
| `ignore NAME` | ignore-file name (`.gitignore`) respected in gitignore syntax under walked directories |
| `except PATTERN...` | files under its root that are not the source |
| `prefer NAME over NAME` | read a preferred sibling file when present, falling back otherwise |
| `room N` | what it takes in the database, in times what its files hold, as measured; used by the room check |
| `called NAME` | the source's record, where its witness is named file by file: the first part of its trunk |
| `after SOURCE...` | the sources it comes after; `order` is the total order. A source asked for by name is run after every source it comes after, each its own run; one whose prerequisite did not go in is not begun |
| `reads FORMAT...` | its files are ordinary content, read as these formats, the recipes that belong to no source |

A recipe of a source takes the source's witness, lineage, and trust unless it names its own.

## The recipe file

### Which files, and what gives them a tree

| Directive | Meaning |
| --- | --- |
| `name NAME` | the recipe's name (also referenced by `@RECIPE/FIELD` in `.firmware`) |
| `match GLOB...` | files it applies to, by file name; a glob with a directory in it, `annotated/train-*`, by the end of the path; the most specific pattern wins |
| `interpreter NAME...` | shebang interpreters (`sh`, `bash`, `python3`, `node`) that match extensionless executable scripts |
| `grammar text \| NAME` | UAX #29 text, a compiled Tree-sitter grammar loaded from `$LAPLACE_GRAMMARS`, or a native Engine grammar (`pgn`, `fen`) |
| `format NAME` | loads `recipes/formats/NAME.format` (`xml`, `json`, `turtle`, `conllu`, `wndb`, `csv`, `tsv`, `psv`), declaring the Tree-sitter grammar, record boundaries, column bindings, and `node` rules once for every recipe of that format |
| `product-format NAME` | composes outer framing records around an inner product format |
| `input decode NAME` | decodes binary container input (`syzygy` in `src/chess_syzygy.c`) before the grammar parses it ([Syzygy](../Corpora/Syzygy.md)) |
| `like RECIPE` | reads as that recipe does, its layout and dispositions, under its own name, witness, lineage, and trust |
| `class NAME`, `witness NAME...`, `lineage NAME...` | as for the source, for this recipe alone |

A recipe that names only a grammar records each file as its syntax tree, byte for byte. A recipe that lays a file out (`.format` node/column rules or compiled `tier` packaging) and says what its parts are is a curated source.

### Formats, grammar nodes, and compiled tier layouts

Format files (`recipes/formats/NAME.format`, with `include OTHER`) and recipes map compiled Tree-sitter CST nodes, tabular columns, and sentence layers directly into `SemanticRecord` values:

| Directive | Meaning |
| --- | --- |
| `records SYMBOL...` | top-level Tree-sitter node types streamed as independent records in a single pass across batches |
| `columns ID FIELD under ROW tier N fields A B ...` | maps fixed positional child nodes (such as CoNLL-U's 10 tab-separated columns under `word_line`) to field names in $O(1)$ |
| `node TYPE group [as NAME] [name PATH...] [list] [kind]` | a composite CST node (`as record`, `as row`, or named by `PATH` / `kind`) |
| `node TYPE note name FIELD text FIELD` | a comment/note CST node (`# key = value` in CoNLL-U) |
| `node TYPE value name PATH text PATH` | a named attribute or key/value CST node |
| `node TYPE text [raw] [join] [kind] [field NAME grammar SUBGRAMMAR]` | a text leaf; `field NAME grammar SUBGRAMMAR` chains an inner Tree-sitter grammar (`kv_pipe`, `ud_relation`, `deps`, `ud_misc`) over that field's byte range |
| `node TYPE member name FIELD value FIELD` | an object member naming its value child |
| `node TYPE skip` | skips the CST subtree |
| `resolve xml \| json \| turtle \| lines` | unescapes format-level character/entity encodings |
| `trim`, `levels NAME...`, `split ELEMENT...` | whitespace trimming, nested JSON object levels, and multi-core record partitioning |
| `surface TIER ROW ID FORM [separator SEP] [unless FIELD VALUE] [verify text spacing]` | reconstructs or verifies a sentence record's untokenized surface text (including CoNLL-U multiword tokens and `SpaceAfter=No`) against its `# text = ...` note |
| `layers TIER ROW FIELD...` | aligns per-token annotation columns (`FORM`, `LEMMA`, `UPOS`, `XPOS`, `FEATS`, `DEPREL`, `DEPS`, `MISC`) as compact sentence-level layers |
| `tree TIER ROW HEAD DEPREL` | composes the sentence's syntactic dependency tree over row ordinals and `DEPREL` slots |
| `part PATH grammar SUBGRAMMAR` / `part PATH by SEP [is IS] [pieces N] [space CHAR]` | parses an embedded field (`CxnElt`, `Functor`, `fen`, `json`, `object`, or `lp_parts` separators) through its compiled child grammar |
| `empty TEXT...` | sentinel token (`_` in CoNLL-U) denoting an absent field that attests nothing |
| `tier NAME by SEP`, `names ...`, `header`, `skip N`, `note`, `comment`, `remark`, `quoted`, `padded`, `is SEP`, `continued`, `escaped CHAR` | declarative flat-file layout directives, compiled at recipe load by `layout_compile_tiers` into the matching compiled Tree-sitter packaging grammar (`lp_records`, `lp_paragraphs`, `lp_conllu_records`, `lp_csv`/`lp_tsv`/`lp_psv`, `wndb`) |

### What each named part is

| Directive | Meaning |
| --- | --- |
| `content NAME...` | the part is content, the text it is, the same entity wherever that text stands |
| `key TIER NAME [within SCOPE]` | the part is the file's or record's internal pointer (`key row ID within record`): it resolves to the TIER's thing, preserving occurrence ordinals within `SCOPE`, and is written nowhere. A highway ID is never a `key`: it is content |
| `refer NAME TIER [within] [TIER...]` | the part's text is a pointer to a TIER, here or in another recipe of the source: it is read as that thing; unresolved pointers say nothing and are counted |
| `index FIELD in LIST [matching PATTERN] [base 0\|1]` | resolves a record-local numeric index into a parsed list; invalid or out-of-range indices reject admission rather than fabricating content |
| `type NAME LIST... [matching PATTERN] [as TEMPLATE...] [node]` | resolves the part through the highway's `LIST` (`lp_highway_resolve` / `lp_highway_key`); with `node`, the key is the canonical highway identifier text itself (`abandon.01`, `NOUN`, `nsubj`) |
| `type NAME upos crosswalk TAGSET` / `vocabulary NAME` | maps a source tagset (`brown`, `ptb`, `wordnet-pos`, `webster-pos`, or `recipes/vocabularies/NAME.tsv`) to its highway slot and crosswalks it to `upos` |
| `value LIST NAME...` | declares what `NAME` means when attested: a value from highway road class `LIST` (or `-` for the source's own inventory), emitting `[thing, value]` (or `[thing, [KEY, VALUE]]` for `Name=Value` features) with zero markup column names in the claim |
| `relation "TEXT" NAME...` | declares in the source's own documented words (`"TEXT"`, never the raw column/attribute identifier) the relation `[thing, TEXT, value]` that `NAME` states (also referenced by `@RECIPE/NAME` in `.firmware`) |
| `dependence TIER CLASS` | marks observations emitted in `TIER` (including under `when`/`always`) with `LP_SAID_DEPENDENCE` (`7`) bound to `CLASS` in `manifest/trust_classes.toml` (such as `DerivedCalculation`), while keeping the corpus trunk as witness |
| `default FIELD VALUE` / `unless_equal FIELD OTHER` | suppresses redundant testimony when a field equals its format-declared default or duplicates a sibling scalar |
| `admit references NAME...` | admits only records whose external keys belong to the exported provider domain |
| `metadata NAME...` | the part is said of the file itself: it goes in the file's metadata tree |
| `omit NAME...` | the part is the file's bookkeeping, read by nothing, nor anything inside it |
| `perfcache` | properties already present in `tier0.flags` are read from the flags ROM and not re-attested |
| `own NAME...`, `codepoints NAME...`, `range NAME...` | source-scoped values and hexadecimal codepoint / `FIRST..LAST` notations |

Names are written as the file writes them. `ELEMENT.NAME` scopes `NAME` to `ELEMENT` (`MISC.Translit`); `NAME*` matches by prefix; `note:NAME` matches a comment/note key. Any named part left without a disposition—or attested without a `value` or `relation` meaning—is counted and reported as an explicit unresolved obligation (`say_obligations`), never silently dropped or polluted with raw markup names.

### Paths

Wherever a line names a part, it may name it by a path from the part being read: `A/B` the B in its A; `^` what it is inside; `^NAME` the nearest part of that name it is inside; `N` its Nth part, counted from 1 (`start/3` is `ice_cream` in `/c/en/ice_cream/n`); `NAME[CHILD=VALUE]` a part of that name whose CHILD is written VALUE (`property[predicate=skos:definition]`); `.` the part itself.

### What a part is the thing of

| Directive | Meaning |
| --- | --- |
| `thing TIER NAME... [resolved]` | a TIER is the thing its part `NAME` names, or the path of several parts (`resolved` keeps the non-empty resolved parts in recipe order); supports `NAME matching PATTERN`, `NAME space CHAR`, and `literal "TEXT"` |
| `thing TIER NAME... within` / `within-file` | scopes a local name within its enclosing thing or file |
| `thing TIER span START END TEXT [inclusive]` | the codepoint span `START..END` of `TEXT` |
| `thing TIER NAME... of [CHILD]` | the path of the things of its named child parts in file order (`thing DEPS of edge`) |
| `thing TIER .` | the part itself, whole |
| `thing TIER NAME product PRODUCT` | the product a native grammar reads off the part (`position` for `pgn`; [Chess](../Sequence/Chess.md)) |

### What a file attests

| Directive | Meaning |
| --- | --- |
| `attest TIER NAME... [of PATH] [by PATH]` | emits `[thing, value]` (for `value`-typed fields) or `[thing, TEXT, value]` (for `relation "TEXT"` fields) on `TIER`'s thing (or `of PATH`) |
| `relate TIER NAME to NAME [of PATH] [alone] [by PATH]` | emits `[thing, relation, other]` where the first `NAME` has a `value` declaration (`[thing, relation]` when `alone` and the target is omitted, such as CoNLL-U `HEAD = 0`) |
| `pair TIER NAME... [of PATH]` | emits `[thing, value]` directly (`pair row MISC.CopyOf`) |
| `holds TIER NAME... [via]` | relates `TIER` to inner things declared with `value` |
| `itself TIER [by PATH]` | `TIER`'s thing is itself the n-ary claim tuple |
| `voices TIER NAME... [within-file]`, `voice TIER NAME` | records speaker/annotator qualifiers (`LP_SAID_VOICE`) inside the judgment record while keeping the corpus trunk as witness |
| `together TIER` | groups a record's claims with 1-based ordinal positions in vertex `M` |
| `games TIER NAME` | sets the observation repeat count (`run` / `games`) from an integer count column |
| `score TIER NAME [from A to B]` | maps a numeric rating on `[A, B]` into `[0, 1]` (`WIN`, `DRAW`, `LOSS`, or `LP_SPARE_SCORE`) |
| `strict TIER` | refuses any record of `TIER` that attests nothing or has an out-of-range/non-numeric `score`, exiting 1 before registering a witness (`statement.recipe`) |
| `where NAME is \| is-not \| matches ...` | filters outermost records that speak |
| `when NAME is \| is-not \| matches ...`, `always` | conditional block over `attest`, `pair`, `relate`, `omit`, `refer`, and `dependence` |
| `stem [FROM] TO`, `itself-mark CHAR`, `about PATTERN`, `line PATTERN` | filename stem extraction, UCD self-codepoint marker, and page-pattern extraction |

Nothing is renamed: every entity and documented relation text is decomposed as written.

### The highway

A resource's recipe says which of its things are types and what it maps between them; `laplace highway` reads every source that says any, in order, by the same decomposer, so a type's ID is the very thing its recipe composes for it when the source is ingested ([Types](Types.md)).

| Directive | Meaning |
| --- | --- |
| `types LIST "SAY" TIER` | each thing of TIER is a type of the highway's LIST, in the order the files write them (a text of a list is a type by itself) |
| `keyed LIST TIER PATH [matching PATTERN] [as TEMPLATE]` | the value at PATH is a resource's identifier of that type, as those who point at it write it |
| `alias LIST TIER PATH [matching ...] to PATH [matching ...]` | an identifier that names the type another identifier names |
| `maps TIER PATH LIST [matching ...] to PATH LIST [matching ...]` | an edge between the type one identifier names and the type another names |

A pattern is POSIX extended; a template writes `\0` the whole match and `\1` to `\9` its parts; with no template, the first part, or the whole. What names no type of its list is left out and said, by lists, with an example.

## How a file is recorded

A file's trunk is `[metadata, content]`. The metadata tree is the OS's record of the file, its parts as the OS names them (`pathname`, a composition of its filenames; `filename`; and what `statx` returns, `stx_mode` to `stx_mtime`), each `[name, value]` and each disposed of by the file's recipe or, where that says nothing of it, by the stock recipe `file` (`metadata` or `omit`); then what the recipe says is said of the file itself. A part neither disposes of is said once and not recorded. The content tree is the file's own tree. A file a recipe records only by its grammar is its syntax tree, each node the composition of its children with the bytes between them kept as text, so it recomposes byte for byte; leaves are text, decomposed by UAX #29. A curated file's content is the whole of each of its outermost parts as its recipe reads them, in the file's order, each the claim it is where it is one; a few thousand are one path, and more are factored into blocks from the content alone: a block ends after a part whose own ID says so, never at a count or a position, and the blocks are composed the same way, level by level, until one holds them all. A file's tier is one above its highest constituent. The trunk is written last of everything the file is and attests, so a recorded trunk means all of it is recorded.

A source's trunk is `[record, content]`: the record is the witness its `source` file names, or its `called` line where the witness is named file by file; the content is its files' trunks in the order of their paths. It is written after the last of its files, in a load of its own, and found recorded like any other trunk, by its ID. This source trunk is the witness ID in `public.attestation` (`(claim, witness, lineage, games, tokens, score, "position", trust)`), while record-, file-, and voice-level provenance is containment (`LP_SAID_RECORD`, `LP_SAID_CLAIM`, `LP_SAID_HOLDS`, `LP_SAID_VOICE`, and `LP_SAID_DEPENDENCE` vertices under each file's content tree, walked by `laplace_attested` and `laplace_attribution`), replacing the retired `witness` table with nothing lost.

## The stock recipes

Format recipes that belong to no source, which any source's `reads` may name and which `laplace ingest FILE` uses by extension, shebang `interpreter`, or structural content sniffing (`detect_structure_recipe` in `Laplace-Engine/src/recipe.c` when an extension is absent or unrecognized):

| Recipe | Matches | Reads |
| --- | --- | --- |
| `text` | `*.txt *.md` | UAX #29 codepoint, grapheme, word segment (a separator separates at the word tier, [Types](Types.md#segmentation)), sentence, paragraph, file |
| `markdown` | `*.md *.markdown` | compiled paragraph/line packaging (`lp_paragraphs`), leaves text |
| `xml` | `*.xml` | `format xml`: compiled `tree-sitter-xml` syntax tree, leaves text |
| `json` | `*.json` | `format json`: compiled `tree-sitter-json` syntax tree; a tokenizer's `tokenizer.json` is read so |
| `jsonl` | `*.jsonl *.ndjson` | line-delimited records (`lp_records`) chaining into `format json` |
| `tsv` / `csv` | `*.tsv *.tab` / `*.csv` | compiled tabular grammars (`lp_tsv`, `lp_csv_quoted`) |
| `turtle` | `*.ttl *.nt *.n3` | `format turtle`: subject statements, predicate relations, language tags and datatypes |
| `wn-lmf` | | `format xml`: lexical entries, synsets, lexicalizations (`[lemma, language, ILI]`), and highway `ili` nodes |
| `statement` | `*.statement` | runtime witness statements (`laplace witness`): `[subject, relation, object]` (or `[subject, relation]`) with tab-separated `[0, 1]` score, `omit pathname filename`, `strict row` |
| `file` | | OS `statx` file metadata dispositions (`metadata pathname filename stx_mode ... stx_mtime`, `omit stx_atime`) |

A worked example from `universal-dependencies/conllu.recipe` (paired with `recipes/formats/conllu.format`, which binds `grammar conllu`, `records sentence`, `columns ... fields ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC`, and sub-grammars `kv_pipe`, `ud_relation`, `deps`, `ud_misc`):

```text
name conllu
match *.conllu
format conllu
empty _

surface record row ID FORM separator " " unless MISC.SpaceAfter No verify text spacing
thing row FORM
layers record row FORM LEMMA UPOS XPOS FEATS DEPREL DEPS MISC
tree record row HEAD DEPREL
content text FORM LEMMA XPOS FEATS MISC
type UPOS upos
content DEPREL relation
type base deprel node
content subtype
value deprel base
when subtype matches .
dependence DEPREL DerivedCalculation
dependence relation DerivedCalculation
always
attest DEPREL base of ^
attest relation base of ^/^/^

key row ID within record
when HEAD is 0
omit HEAD
always
refer HEAD row

omit "newdoc id" "newpar id" sent_id MISC.SpaceAfter
metadata note:newdoc* note:newpar* note:doc_* note:meta::* note:title note:author note:url
content note:*

value upos UPOS
value - FEATS
relation "Language-specific part-of-speech tag" XPOS
relation "Lemma or stem of word form" LEMMA
value - DEPREL

attest row LEMMA UPOS XPOS FEATS
attest row MISC
attest record note:*
relate row DEPREL to HEAD alone
```

`format conllu` parses each sentence and its 10 token columns through compiled `tree-sitter-conllu` and its sub-grammars (`FEATS`, `DEPREL`, `DEPS`, `MISC`) without byte-splitting scanners; `surface` verifies exact untokenized spacing against `# text = ...`; `layers` and `tree` record aligned token layers and syntactic subtrees; `ID` and `HEAD` resolve sentence-locally via `key row ID within record` and `refer HEAD row` and are written nowhere; `UPOS` and `DEPREL` bind to highway slots via `type` and `value` (marking subtype family membership with `dependence ... DerivedCalculation`); and `LEMMA`, `XPOS`, and documented `MISC` attributes state their UD-documented `relation "..."` wording rather than raw column names.

## Where recipes are checked

`laplace structure LAYOUT FILE` shows a file's tree as a layout parts it. `laplace tree FILE` shows a file's syntax tree as its grammar reads it. `laplace ingest --plan` shows which recipe takes which file; `--claims` prints every claim as text and loads nothing; `--no-load` decomposes and checks recomposition without writing, and says every named part left open and every identifier no list of the highway holds. A recipe that does not load stops its own source and no other.
