# Tiny codes

This synthetic dataset, published by nampdn-ai as Tiny Codes, is a collection of 1.6 millions short and clear code snippets that can help LLM models learn how to reason with both natural and programming languages.

## Value

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| Code snippet | A short synthetic snippet for reasoning with natural language and a programming language | The `response` string in the row | The snippet text | nampdn-ai | [nampdn-ai, Tiny Codes dataset card](https://huggingface.co/datasets/nampdn-ai/tiny-codes) |
| Instruction | The prompt the snippet answers | The `prompt` string in the row | The instruction text | nampdn-ai | [nampdn-ai, Tiny Codes dataset card](https://huggingface.co/datasets/nampdn-ai/tiny-codes); one local row read on 2026-09-29 |
| Programming language | The language named for that snippet | The `programming_language` string in the row | The language name | nampdn-ai | Local pyarrow schema and one row, 2026-09-29. The card lists the languages the collection covers and does not name this column |

## Format

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| One code snippet | `prompt` (large_string), `main_topic` (large_string), `subtopic` (large_string), `adjective` (large_string), `action_verb` (large_string), `scenario` (large_string), `target_audience` (large_string), `programming_language` (large_string), `common_sense_topic` (large_string), `idx` (int64), `response` (large_string). The card does not name these columns. One row of `part_9_1632520.parquet` (`idx` 1255011) has a Julia instruction in `prompt` and the code snippet in `response`; the other strings are the slots named in that instruction. | One synthetic snippet. All 9 parquet files share this schema. The local row count is 1,632,309 | [nampdn-ai, Tiny Codes dataset card](https://huggingface.co/datasets/nampdn-ai/tiny-codes); pyarrow schema and `num_rows` on 2026-09-29 |
