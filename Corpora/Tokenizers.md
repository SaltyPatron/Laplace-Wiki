# Tokenizers

A model tokenizer's vocabulary is observed content, each token as the text it stands for and the vocabulary as the path of its tokens in index order, and attests nothing.

The source is the `tokenizer.json` of every model kept on this machine. It has no recipe of its own: its source file says the files are ordinary content, read as `vocabulary`, and observed, as [Attestations](../Semantics/Attestations.md#observations) says of ordinary content. [Research: Models](../Research/Models.md#vocabularies-as-content) records what was measured when they were loaded.

## Source

| Source | Witness | Trust | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `tokenizers` | none: observed content has no witness | none | `unicode` | `tokenizer.json` in each model's directory | [`source`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/tokenizers/source), `reads vocabulary` |

## The vocabulary

`tokenizer.json` is the Hugging Face tokenizers file; its `model.vocab` maps each token to its id, and `added_tokens` adds tokens with a `content` and an `id` of their own ([tokenizers: models](https://huggingface.co/docs/tokenizers/api/models), [added tokens](https://huggingface.co/docs/tokenizers/api/added-tokens)).

| Piece | Written as | Laplace reads it as | Claim recorded |
| --- | --- | --- | --- |
| a token of `model.vocab` | `"king": id` | the text the token stands for, decomposed like any text: a byte-level BPE character is the byte it maps back to, SentencePiece's `▁` is a space, WordPiece's `##` continues a word, and a byte token, or a byte-level token that is not valid UTF-8 by itself, is the notation `<0xAB>` of each byte | none |
| the id | the token's number | where the token stands: the vocabulary is the path of its tokens in index order | none |
| an added token | an object of `added_tokens` with `content` and `id` | its `content`, at its `id`, like any other token | none |
| the vocabulary | | the path of its tokens, in index order; files with the same tokens in the same order are one composition | none |
| `model.type`, `merges`, the normalizer, the pre-tokenizer, and the rest of the file | | not read as statements: the file is content too, and the token list is kept as the model wrote it | none |
