# Tokenizers

A model tokenizer's file is observed content, recorded as the JSON document it is, every member and token as the file writes it and byte for byte, and attests nothing.

The source is the `tokenizer.json` of every model kept on this machine. It has no recipe of its own: its source file says the files are ordinary content, read as `json`, and observed, as [Attestations](../Semantics/Attestations.md#observations) says of ordinary content. [Research: Models](../Research/Models.md#vocabularies-as-content) records what was measured when they were loaded by the reader that came before.

## Source

| Source | Witness | Trust | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `tokenizers` | none: observed content has no witness | none | `unicode` | `tokenizer.json` in each model's directory | [`source`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/tokenizers/source), `reads json` |

## The file

`tokenizer.json` is the Hugging Face tokenizers file; its `model.vocab` maps each token to its id, and `added_tokens` adds tokens with a `content` and an `id` of their own ([tokenizers: models](https://huggingface.co/docs/tokenizers/api/models), [added tokens](https://huggingface.co/docs/tokenizers/api/added-tokens)).

| Piece | Written as | Laplace reads it as | Claim recorded |
| --- | --- | --- | --- |
| a token of `model.vocab` | `"king": id` | a member of the JSON syntax tree: the token as the tokenizer writes it and its number, each a text decomposed like any text | none |
| an added token | an object of `added_tokens` with `content` and `id` | an object of the syntax tree, its members as written | none |
| `model.type`, `merges`, the normalizer, the pre-tokenizer, and the rest of the file | | the rest of the syntax tree, as written | none |
| the file | | its syntax tree, each node the composition of its children with the bytes between them kept as text, so it recomposes byte for byte; files that are the same are one composition | none |
