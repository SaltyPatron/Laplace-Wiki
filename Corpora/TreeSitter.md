# Tree-sitter

Tree-sitter grammars are what the Engine parses files with, named by a recipe's `grammar` line, and they are not a source: nothing in them is attested.

## Source

A recipe's `grammar NAME` directive, or the shared `format NAME` file it includes (`recipes/formats/NAME.format`), loads a compiled Tree-sitter shared library from `$LAPLACE_GRAMMARS` (`Laplace-Engine/src/grammars.c`); the recipe's `node` rules specify what each syntax node kind represents in the file's tree, and its semantic directives specify what each recovered part attests ([Recipes](../Reference/Recipes.md)). A grammar is a parser used during ingest and realization, not a corpus in `recipes/order`: zero witnesses or claims are minted from the grammar library itself. Its `node-types.json` defines the grammar's static symbol and field inventory inspected by `laplace tree FILE`.

## Format (`node-types.json`)

| Record | Fields in order | What a record is | Specification |
| --- | --- | --- | --- |
| `node-types.json` entry | `type`, `named`, plus `fields`, `children`, or `subtypes` when present | Static grammar node specification: `(type, named)` identifies the symbol, `fields` and `children` constrain child slots, and `subtypes` enumerates wrapped supertypes | [Tree-sitter Static Node Types](https://tree-sitter.github.io/tree-sitter/using-parsers/6-static-node-types.html) |

## Compiled grammar estate (`$LAPLACE_GRAMMARS`)

`Laplace-Engine` compiles both upstream grammars from `/vault/Data/TreeSitter` (300+ languages and data formats) and Laplace-authored grammars under [`Laplace-Engine/recipes/formats/grammars/`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/formats/grammars) (`conllu`, `wndb`, `pgn`, `turtle`, `concept_uri`, `emoji_palette`, `brown_tagged`, `webster`, `britannica`, `c_laplace`, `cpp_laplace`, `sql_laplace`, plus parameterized CSV/TSV/PSV scanners) directly into `$LAPLACE_GRAMMARS` shared libraries. No per-language C or C# decomposer registration exists: naming `grammar <name>` in a declarative `.recipe` immediately admits any language or container format through the one generic C pipeline.

## Where UAX #29 applies

UAX #29 (with Laplace's word-tier separator rule, [Types](../Reference/Types.md#segmentation)) is the universal leaf segmentation law. It applies in two places:

- **Plain-text prose spans or files** when the content itself is natural-language prose (such as the body of a novel after wrapper metadata is separated, or a plain `.txt` note).
- **Every text leaf inside a structured grammar tree:** a TSV/CSV cell, an XML character-data span, a JSON string literal, a source-code comment or docstring, or an XHTML/OOXML/PDF text run. The outer container grammar never replaces UAX #29—it isolates exact structural nodes so leaf text spans decompose cleanly down to Tier-0 codepoints without mixing markup delimiters into words.

Sending a structured `.tsv`, `.xml`, `.json`, or source-code file blindly through `grammar text` destroys its AST hierarchy and is forbidden.

## A recipe is Laplace's grammar of a format

Every file is **packaging** opened to extract canonical **product** (content entities and source-attested claims) while retaining the packaging hierarchy as `[metadata, content]` provenance trunks. Because Laplace's Merkle DAG *is* an AST, Tree-sitter and `.recipe` files form one bidirectional grammar pipeline (`Bytes → Chained Tree-sitter AST → Laplace Merkle DAG + Claims` on ingest, and `Laplace Merkle DAG → AST → Formatted Bytes` on realization):

1. **Multi-level grammar chaining (`ts_parser_set_included_ranges`):**
   - **Outer packaging grammar:** Standardized containers parse through their compiled Tree-sitter grammar (`tree-sitter-xml` for WN-LMF, FrameNet, PropBank, and UCD; `tree-sitter-json` for Wiktextract, Tokenizers, and JSONL; `tree-sitter-turtle` for CILI and FrameBase; compiled CSV/TSV/PSV grammars for Tatoeba, ATOMIC, safety datasets, GeoNames, and ConceptNet; `tree-sitter-conllu` for Universal Dependencies; `tree-sitter-wndb` for Princeton WordNet; `tree-sitter-pgn` for chess; `webster` and `britannica` for structured Gutenberg reference works; plus 300+ programming-language grammars).
   - **Inner injected sub-grammars:** Whenever an outer field carries internal structured syntax (CoNLL-U `FEATS` `Key=Val|Key=Val`, `DEPS`, `MISC`, ConceptNet `/c/en/ice_cream/n` URIs, PGN moves inside TSV cells, or structured sense keys `drop%2:38:00::` / `mcr:ili-30-01976841-v`), the child grammar runs directly over the parent `TSNode` byte range via `ts_parser_set_included_ranges`, chaining down to UAX #29 text leaves and `tier0.bin` / `highway.bin`.
2. **Compiled integer symbol dispatch (`structure_compile.c`):**
   - `.format` and `.recipe` rules compile once at recipe load time against `ts_language_symbol_for_name()` and `ts_language_field_id_for_name()` into flat $O(1)$ integer jump tables (`TSSymbol` / `TSFieldId` → disposition and composition instructions). Worker threads stream the `TSTree` directly over input buffers with `TSTreeCursor` and thread-local arenas—with zero intermediate heap DOM materialization.

Binary container formats (`.gz` already decoded transparently before parsing; `.epub`/OOXML ZIP packages, Parquet columnar pages, PDF object streams, and PNG/WAV/video containers in `Batch 2`) unpack through generic format decoders before handing structured streams and text spans to declarative recipes and Tree-sitter grammars.

## Grammar-only vs. curated semantic recipes

Tree-sitter produces the concrete syntax tree—every token, rule symbol, and byte span ([Tree-sitter Introduction](https://tree-sitter.github.io/)). For a grammar-only recipe:

```text
name ada
match *.adb *.ads
grammar ada
```

`Laplace-Engine` loads `ada` from `$LAPLACE_GRAMMARS`, composes every AST node from its children while retaining inter-token trivia so the file recomposes byte for byte, and segments leaves by UAX #29. Adding curated `node`, `key`, `refer`, `type`, and `attest` directives upgrades a syntax-tree recipe to extract semantic declarations and cross-file attestations without writing a single line of format-specific C code. `laplace tree FILE` and `laplace ingest --no-load` verify lossless recomposition before admission.
