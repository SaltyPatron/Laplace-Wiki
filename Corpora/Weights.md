# Weights

Model weights have no recipe yet, so they are not ingested and attest nothing, and Spitball holds the intent to assimilate them.

## Source

No directory under [`recipes/`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes) reads this collection, and `recipes/order` does not name it. Until a recipe exists, nothing in it is decomposed, recorded, or attested; see [Attestations](../Semantics/Attestations.md#observations). The format below is the publisher's, kept so that a recipe can be written from it. [Spitball](../Spitball.md#model-ingestion) holds what assimilating a model is meant to be.

## Format

| Record | Fields in order | What a record is | Specification |
| --- | --- | --- | --- |
| Weight file | No text-field order. Companion files in the same directory are the config and the tokenizer, where the repository ships them | A weight file: safetensors, pytorch `.bin`, GGUF, `.pt`, `.pth`, TorchScript, or `checkpoint.pt` | Each model's card, at its repository |
