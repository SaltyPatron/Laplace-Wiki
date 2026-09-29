# Tokenizers

A model tokenizer's vocabulary is observed content and attests nothing.

The composition is a token in a model's vocabulary, read as the text it stands for from `$LAPLACE_MODELS/*/tokenizer.json`. Loaded measure: 191,108 compositions from 9 MB. There is no witness. The recipe says this is ordinary content and attests nothing. A tokenizer that splits a word does not attest the word's sense, its part of speech, or a dependency role. The split is a property of that model, observed from the file.

[Model Ingestion](../Models.md) records tokenizer ingestion as content and treats model testimony as a separate, witnessed act. The vocabulary file is not that testimony. Two tokenizers that contain the same string are not two witnesses of a sense. There is no hop and no fanout until some other witness relates the string to a claim.

## Files, breakdown, and caveats

Taken from the recipe files. A line in a block is a directive. The prose above it is that file's own account of what is read, what is not, and what a row becomes.

### `tokenizers/source`

The vocabularies of the tokenizers of the models kept on this machine: each token as the text it stands for, and the vocabulary as the path of its tokens in the order the tokenizer numbers them. Ordinary content: it attests nothing. Measured when it was loaded: 191,108 compositions from 9 MB, at 750 bytes each with their indexes and standings.

```text
reads vocabulary
```
