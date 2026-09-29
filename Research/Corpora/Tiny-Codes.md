# Tiny codes

This synthetic dataset, published by nampdn-ai as Tiny Codes, is a collection of 1.6 millions short and clear code snippets that can help LLM models learn how to reason with both natural and programming languages.

## Files

| Path | Bytes | What the file is | Proof |
| --- | --- | --- | --- |
| `/vault/models/tiny-codes` | 981,403,859 | 19 files: 9 parquet parts and 10 Hugging Face download-metadata files under `.cache/huggingface`; 1,632,309 parquet rows | `du -sb` and pyarrow `num_rows` on 2026-09-29 |
| `/vault/models/tiny-codes/part_1_200000.parquet` | 120,240,865 | Parquet part, 199,972 rows | `stat` size and pyarrow `num_rows` on 2026-09-29 |
| `/vault/models/tiny-codes/part_2_400000.parquet` | 120,181,361 | Parquet part, 199,970 rows | `stat` size and pyarrow `num_rows` on 2026-09-29 |
| `/vault/models/tiny-codes/part_3_600000.parquet` | 120,140,572 | Parquet part, 199,974 rows | `stat` size and pyarrow `num_rows` on 2026-09-29 |
| `/vault/models/tiny-codes/part_4_800000.parquet` | 120,109,996 | Parquet part, 199,978 rows | `stat` size and pyarrow `num_rows` on 2026-09-29 |
| `/vault/models/tiny-codes/part_5_1000000.parquet` | 120,211,926 | Parquet part, 199,974 rows | `stat` size and pyarrow `num_rows` on 2026-09-29 |
| `/vault/models/tiny-codes/part_6_1200000.parquet` | 120,347,549 | Parquet part, 199,977 rows | `stat` size and pyarrow `num_rows` on 2026-09-29 |
| `/vault/models/tiny-codes/part_7_1400000.parquet` | 120,140,121 | Parquet part, 199,978 rows | `stat` size and pyarrow `num_rows` on 2026-09-29 |
| `/vault/models/tiny-codes/part_8_1600000.parquet` | 120,447,788 | Parquet part, 199,970 rows | `stat` size and pyarrow `num_rows` on 2026-09-29 |
| `/vault/models/tiny-codes/part_9_1632520.parquet` | 19,574,261 | Parquet part, 32,516 rows | `stat` size and pyarrow `num_rows` on 2026-09-29 |
| `/vault/models/tiny-codes/.cache/huggingface` | 1,151 | Ten download-metadata files: `.gitignore` and one `.metadata` file per parquet part. Not a second copy of the parquet | `stat` sizes on 2026-09-29 |

## Attestations

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| Code snippet | A short synthetic snippet for reasoning with natural language and a programming language | The `response` string in the row | The snippet text | nampdn-ai | [nampdn-ai, Tiny Codes dataset card](https://huggingface.co/datasets/nampdn-ai/tiny-codes) |
| Instruction | The prompt the snippet answers | The `prompt` string in the row | The instruction text | nampdn-ai | [nampdn-ai, Tiny Codes dataset card](https://huggingface.co/datasets/nampdn-ai/tiny-codes); one local row read on 2026-09-29 |
| Programming language | The language named for that snippet | The `programming_language` string in the row | The language name | nampdn-ai | Local pyarrow schema and one row, 2026-09-29. The card lists the languages the collection covers and does not name this column |

## Records

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| One code snippet | `prompt` (large_string), `main_topic` (large_string), `subtopic` (large_string), `adjective` (large_string), `action_verb` (large_string), `scenario` (large_string), `target_audience` (large_string), `programming_language` (large_string), `common_sense_topic` (large_string), `idx` (int64), `response` (large_string). The card does not name these columns. One row of `part_9_1632520.parquet` (`idx` 1255011) has a Julia instruction in `prompt` and the code snippet in `response`; the other strings are the slots named in that instruction. | One synthetic snippet. All 9 parquet files share this schema. The local row count is 1,632,309 | [nampdn-ai, Tiny Codes dataset card](https://huggingface.co/datasets/nampdn-ai/tiny-codes); pyarrow schema and `num_rows` on 2026-09-29 |

## Lineage

| Paths | What is shared | Proof |
| --- | --- | --- |
| `/vault/models/tiny-codes/part_1_200000.parquet` through `part_9_1632520.parquet` | The nine parquet siblings of `nampdn-ai/tiny-codes` at commit `9aebe5ee8b406356d5f5f2d603bc0a1684ee8ce7`. That commit is the dataset API `sha` and the first line of each local `.metadata` file | [nampdn-ai, Tiny Codes dataset card](https://huggingface.co/datasets/nampdn-ai/tiny-codes); Hugging Face dataset API; local `.cache/huggingface/download/*.metadata` |
| `/vault/models/tiny-codes/.cache/huggingface/download/*.metadata` | Download etag records for those parquet files, about 128 bytes each, not a second copy of the parquet bytes | `stat` sizes on 2026-09-29 |
