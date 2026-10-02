# Tree-sitter

Tree-sitter grammars are what the Engine parses files with, named by a recipe's `grammar` line, and they are not a source: nothing in them is attested.

## Source

A recipe's `grammar NAME` line, or the `format NAME` file it names, loads a tree-sitter grammar from `$LAPLACE_GRAMMARS`; the recipe's `node` lines say what each kind of the grammar's nodes is in the file's tree, and its dispositions what each named part of that tree is ([Recipes](../Reference/Recipes.md)). A grammar is a tool of the ingest, not a source in `recipes/order`: no witness is named for it and no claim is recorded from it. Its `node-types.json` is the format below, which is what `laplace tree file` prints the node names of.

## Format

| Record | Fields in order | What a record is | Specification |
| --- | --- | --- | --- |
| node type | type, named, then fields, children, or subtypes when present | One object in the node-types.json array. type and named together identify the node type. fields and children describe child nodes. subtypes lists the nodes a supertype can wrap. | [Static Node Types](https://tree-sitter.github.io/tree-sitter/using-parsers/6-static-node-types.html) |
