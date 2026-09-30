# Tiny codes

Tiny Codes has no recipe yet, so its rows are not ingested and attest nothing.

## Source

No directory under [`recipes/`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes) reads this collection, and `recipes/order` does not name it. Until a recipe exists, nothing in it is decomposed, recorded, or attested; see [Attestations](../Semantics/Attestations.md#observations). The format below is the publisher's, kept so that a recipe can be written from it.

## Format

| Record | Fields in order | What a record is | Specification |
| --- | --- | --- | --- |
| One code snippet | `prompt` (large_string), `main_topic` (large_string), `subtopic` (large_string), `adjective` (large_string), `action_verb` (large_string), `scenario` (large_string), `target_audience` (large_string), `programming_language` (large_string), `common_sense_topic` (large_string), `idx` (int64), `response` (large_string). The card does not name these columns. One row of `part_9_1632520.parquet` (`idx` 1255011) has a Julia instruction in `prompt` and the code snippet in `response`; the other strings are the slots named in that instruction. | One synthetic snippet. All 9 parquet files share this schema. | [nampdn-ai, Tiny Codes dataset card](https://huggingface.co/datasets/nampdn-ai/tiny-codes); pyarrow schema and `num_rows` on 2026-09-29 |
