# Tree-sitter

Tree-sitter grammars are what the Engine parses files with, named by a recipe's `grammar` line, and they are not a source: nothing in them is attested.

## Source

A recipe's `grammar NAME` line, or the `format NAME` file it names, loads a tree-sitter grammar from `$LAPLACE_GRAMMARS`; the recipe's `node` lines say what each kind of the grammar's nodes is in the file's tree, and its dispositions what each named part of that tree is ([Recipes](../Reference/Recipes.md)). A grammar is a tool of the ingest, not a source in `recipes/order`: no witness is named for it and no claim is recorded from it. Its `node-types.json` is the format below, which is what `laplace tree file` prints the node names of.

## Format

| Record | Fields in order | What a record is | Specification |
| --- | --- | --- | --- |
| node type | type, named, then fields, children, or subtypes when present | One object in the node-types.json array. type and named together identify the node type. fields and children describe child nodes. subtypes lists the nodes a supertype can wrap. | [Static Node Types](https://tree-sitter.github.io/tree-sitter/using-parsers/6-static-node-types.html) |

## What is compiled on this machine

`/vault/Data/TreeSitter` holds 303 grammar checkouts and 325 `grammar.js` files. `Laplace-Engine/tools/build_grammars.sh` compiles every `src/parser.c` there into `$LAPLACE_GRAMMARS/libtree-sitter-<name>.so`. 316 of those libraries are built. One checkout can export more than one language (`csv` and `tsv` from `tree-sitter-csv`).

The monorepo's `engine/core/grammars` wires 35 of them into `grammar_registry.c` and describes the rest as dormant until someone writes a decomposer. That wait is the wrong gate. A recipe that names a grammar and nothing else already admits the file.

## Where UAX #29 applies

UAX #29 is the rule for text. It applies in two places, and both of them are normal.

- The whole file, when nothing else names its parts. A Gutenberg book is this case: no book recipe has been written, so the file is basic text.
- Every span another recipe has already decided is text. A TSV field, an XML text node, a PDF text run, a Word text run, a source leaf. The container recipe does not replace UAX #29. It decides which spans are text, and those spans are decomposed by it.

A `.tsv` is not one text. IANA `text/tab-separated-values` says a header line, then one record per line, fields separated by a tab, no tab inside a field, the same count on every record. RFC 4180 is the CSV memo. The row is the composition of its fields. The file is the composition of its rows. The field is the text.

XML has a grammar here: `libtree-sitter-xml.so`, and the stock recipe is `grammar xml` with the note that leaves are text. HTML and Markdown are the same shape. The element tree is the grammar. The character data in a leaf is UAX #29.

A language or format that has a built `libtree-sitter-*.so` and no record standard uses that grammar for the tree, and UAX #29 for the leaves. Sending the whole file through `grammar text` drops the tree.

## A recipe is Laplace's grammar of a format

The question a recipe answers is: how is this file parsed, whatever the standardized format is. One decomposer reads every recipe (`Laplace-Engine/src/structure.c`). No code names a format. The recipe does.

A tree-sitter library is one way a recipe gets a tree: `grammar NAME`. A separator layout is another: `tier` lines, as `conllu.recipe` does for a record standard. `grammar text` is the third, and it means the whole file is text because no format recipe exists yet.

PDF and Word have no tree-sitter grammar in the vault, and they have no recipe either. That is a missing recipe, not a reason to admit them as basic text. ISO 32000 names PDF's objects and content streams. ECMA-376 names a `.docx` as a package of XML parts, of which `word/document.xml` is XML the XML grammar already reads. Each of those needs a recipe that says those parts, and UAX #29 on the text the parts hold. The decomposer today opens gzip before the recipe sees the bytes. It does not yet open a PDF or an OOXML package. The recipe is still what has to be written.

## What the grammar contributes, and what records the file

Tree-sitter is a parser generator. It builds a concrete syntax tree: every token, a grammar-rule name, and a byte span ([Introduction](https://tree-sitter.github.io/)). That tree is the cut list. It is not the record, and it is not a vector.

The record is the composition the engine already performs for a grammar-only recipe ([Recipes](../Reference/Recipes.md)): each node is the composition of its children, the bytes between children stay as text, and a leaf is UAX #29 text, so the file recomposes byte for byte. The trunk is one entity id. The coordinates are the physicality on the record you fetch with that id. The caller keeps the id.

```text
name ada
match *.adb *.ads
grammar ada
```

`grammar ada` loads `/repos/build/grammars/libtree-sitter-ada.so`. No `node` lines. That is a complete admission.

A curated recipe comes after, when a node kind is a key, a skip, or a reference: `node` lines, or a `format` file. Write those when you know them. Do not hold the file in basic text until the `node` lines exist, and do not hold the grammar unwired until a decomposer is designed.

`laplace tree FILE` prints the cuts before you trust them. A grammar that does not recompose the file, or that errors across the corpus, is not yet usable. Repair the grammar or write the record reader. Falling back to `grammar text` hides the miss and mints the wrong trunk.
