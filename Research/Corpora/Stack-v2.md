# The Stack v2

The Stack v2, published by the BigCode Project, contains over 3B files in 600+ programming and markup languages, and each row is one source file.

## Files

| Path | Bytes | What the file is | Proof |
| --- | --- | --- | --- |
| `/vault/models/stack-v2` | 72,657,289,286 | 28 parquet files, 230,786,710 rows, eight language directories; not the full 600-language release | `du -sb` on 2026-09-29; pyarrow `num_rows` summed the same day |
| `/vault/models/stack-v2/data/C/train-00000-of-00004.parquet` | 2,634,979,138 | C train shard, 4 of 4 local files, split complete relative to the filename; 8,448,590 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/C/train-00001-of-00004.parquet` | 2,634,895,762 | C train shard, 4 of 4 local files, split complete relative to the filename; 8,448,590 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/C/train-00002-of-00004.parquet` | 2,635,066,917 | C train shard, 4 of 4 local files, split complete relative to the filename; 8,448,590 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/C/train-00003-of-00004.parquet` | 2,635,022,372 | C train shard, 4 of 4 local files, split complete relative to the filename; 8,448,589 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/C++/train-00000-of-00007.parquet` | 2,887,418,190 | C++ train shard, 5 of 7 shards present locally; 9,048,860 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/C++/train-00001-of-00007.parquet` | 2,887,577,152 | C++ train shard, 5 of 7 shards present locally; 9,048,860 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/C++/train-00002-of-00007.parquet` | 2,887,634,028 | C++ train shard, 5 of 7 shards present locally; 9,048,860 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/C++/train-00003-of-00007.parquet` | 2,887,566,944 | C++ train shard, 5 of 7 shards present locally; 9,048,860 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/C++/train-00004-of-00007.parquet` | 2,887,451,832 | C++ train shard, 5 of 7 shards present locally; 9,048,860 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/JavaScript/train-00000-of-00018.parquet` | 2,816,737,638 | JavaScript train shard, 5 of 18 shards present locally; 9,020,045 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/JavaScript/train-00001-of-00018.parquet` | 2,816,739,831 | JavaScript train shard, 5 of 18 shards present locally; 9,020,045 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/JavaScript/train-00002-of-00018.parquet` | 2,816,838,741 | JavaScript train shard, 5 of 18 shards present locally; 9,020,045 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/JavaScript/train-00003-of-00018.parquet` | 2,816,605,899 | JavaScript train shard, 5 of 18 shards present locally; 9,020,045 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/JavaScript/train-00004-of-00018.parquet` | 2,816,725,986 | JavaScript train shard, 5 of 18 shards present locally; 9,020,045 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/Python/train-00000-of-00009.parquet` | 2,822,702,062 | Python train shard, 5 of 9 shards present locally; 8,960,411 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/Python/train-00001-of-00009.parquet` | 2,822,247,616 | Python train shard, 5 of 9 shards present locally; 8,960,411 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/Python/train-00002-of-00009.parquet` | 2,822,696,710 | Python train shard, 5 of 9 shards present locally; 8,960,411 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/Python/train-00003-of-00009.parquet` | 2,822,617,201 | Python train shard, 5 of 9 shards present locally; 8,960,411 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/Python/train-00004-of-00009.parquet` | 2,822,359,224 | Python train shard, 5 of 9 shards present locally; 8,960,411 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/Rust/train-00000-of-00001.parquet` | 1,137,358,014 | Rust train shard, 1 of 1 local files, split complete relative to the filename; 3,726,432 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/SQL/train-00000-of-00001.parquet` | 1,777,667,200 | SQL train shard, 1 of 1 local files, split complete relative to the filename; 5,685,145 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/Shell/train-00000-of-00002.parquet` | 2,344,279,150 | Shell train shard, 2 of 2 local files, split complete relative to the filename; 7,574,780 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/Shell/train-00001-of-00002.parquet` | 2,344,665,536 | Shell train shard, 2 of 2 local files, split complete relative to the filename; 7,574,779 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/TypeScript/train-00000-of-00005.parquet` | 2,375,833,263 | TypeScript train shard, 5 of 5 local files, split complete relative to the filename; 7,456,927 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/TypeScript/train-00001-of-00005.parquet` | 2,375,836,217 | TypeScript train shard, 5 of 5 local files, split complete relative to the filename; 7,456,927 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/TypeScript/train-00002-of-00005.parquet` | 2,375,864,049 | TypeScript train shard, 5 of 5 local files, split complete relative to the filename; 7,456,927 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/TypeScript/train-00003-of-00005.parquet` | 2,376,004,764 | TypeScript train shard, 5 of 5 local files, split complete relative to the filename; 7,456,927 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |
| `/vault/models/stack-v2/data/TypeScript/train-00004-of-00005.parquet` | 2,375,880,932 | TypeScript train shard, 5 of 5 local files, split complete relative to the filename; 7,456,927 rows | `stat` size and pyarrow `ParquetFile.metadata.num_rows` on 2026-09-29 |

## Attestations

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| Source file | Each row is one source file; the published parquet stores Software Heritage file IDs and metadata, and the card says the file bytes are downloaded separately by `blob_id` | The source file identified by `blob_id`, `content_id`, and `path` | The file identifier, not a text span stored in the parquet | BigCode | [BigCode, The Stack v2 dataset card](https://huggingface.co/datasets/bigcode/the-stack-v2) |
| `language` | Programming language of the file, detected by go-enry / linguist | That same source file | The `language` string | BigCode | [BigCode, The Stack v2 dataset card](https://huggingface.co/datasets/bigcode/the-stack-v2) |
| `detected_licenses` | SPDX licenses detected by ScanCode | That same source file | The license list | BigCode | [BigCode, The Stack v2 dataset card](https://huggingface.co/datasets/bigcode/the-stack-v2) |
| `license_type` | Inferred license type, `permissive` or `no_license` | That same source file | The `license_type` string | BigCode | [BigCode, The Stack v2 dataset card](https://huggingface.co/datasets/bigcode/the-stack-v2) |
| `is_vendor` | Vendor-file indicator, detected by go-enry | That same source file | The boolean | BigCode | [BigCode, The Stack v2 dataset card](https://huggingface.co/datasets/bigcode/the-stack-v2) |
| `is_generated` | Generated-file indicator, detected by go-enry | That same source file | The boolean | BigCode | [BigCode, The Stack v2 dataset card](https://huggingface.co/datasets/bigcode/the-stack-v2) |

## Records

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| One source file | `blob_id` (string): Software Heritage ID of the file on AWS S3. `directory_id` (string): Software Heritage ID of the root directory of the repository. `path` (string): file path within the repository. `content_id` (string): Software Heritage content ID. `detected_licenses` (list of string): SPDX licenses detected by ScanCode. `license_type` (string): inferred license type, `permissive` or `no_license`. `repo_name` (string): repository name on GitHub. `snapshot_id` (string): Software Heritage snapshot ID. `revision_id` (string): Software Heritage revision ID. `branch_name` (string): repository branch name. `visit_date` (timestamp[ns]): Software Heritage crawl timestamp. `revision_date` (timestamp[ns]): Software Heritage revision timestamp. `committer_date` (timestamp[ns]): revision timestamp reported by the committer. `github_id` (int64): GitHub identifier for the repository. `star_events_count` (int64): stars calculated from GHArchive events. `fork_events_count` (int64): forks calculated from GHArchive events. `gha_license_id` (string): GHArchive SPDX license identifier, empty if the repo is missing. `gha_event_created_at` (timestamp[ns]): timestamp of the latest GHArchive event for this repository. `gha_created_at` (timestamp[ns]): timestamp of repository creation on GitHub, empty if the repo is missing. `gha_language` (string): repository primary language on GitHub, empty if the repo is missing. `src_encoding` (string): original encoding of the file content before conversion to UTF-8. `language` (string): programming language of the file, detected by go-enry / linguist. `is_vendor` (bool): vendor-file indicator, detected by go-enry. `is_generated` (bool): generated-file indicator, detected by go-enry. `length_bytes` (int64): length of the file content in UTF-8 bytes. `extension` (string): file extension. | A file-level row of `bigcode/the-stack-v2`. Pyarrow read the same 26 columns on all 28 local files, and there is no `content` column. The local files hold 230,786,710 rows | [BigCode, The Stack v2 dataset card](https://huggingface.co/datasets/bigcode/the-stack-v2); pyarrow schema read on 2026-09-29 |

## Lineage

| Paths | What is shared | Proof |
| --- | --- | --- |
| `/vault/models/stack-v2/data/{C,C++,JavaScript,Python,Rust,SQL,Shell,TypeScript}` | The card's per-language train split, one data directory per language. Local files are C 4 of 4, C++ 5 of 7, JavaScript 5 of 18, Python 5 of 9, Rust 1 of 1, SQL 1 of 1, Shell 2 of 2, and TypeScript 5 of 5 | [BigCode, The Stack v2 dataset card](https://huggingface.co/datasets/bigcode/the-stack-v2); directory listing on 2026-09-29 |
| `blob_id` and `src_encoding` | The card's download path for the file bytes in the Software Heritage S3 bucket. Those bytes are not a column in the local parquet | [BigCode, The Stack v2 dataset card](https://huggingface.co/datasets/bigcode/the-stack-v2), section "Downloading the file contents" |
