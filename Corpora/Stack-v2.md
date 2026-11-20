# The Stack v2

The Stack v2 is a repository-indexed source-code metadata Parquet corpus queued for declarative `.recipe` admission (`Batch 3`, `Laplace#894`), whose local Parquet shards carry Software Heritage `blob_id`, `content_id`, repository, revision, language, and SPDX license index records ready to join with fetched source blobs or local `.git` checkouts.

## Source & `Batch 3` admission queue

BigCode's The Stack v2 ([`bigcode/the-stack-v2`](https://huggingface.co/datasets/bigcode/the-stack-v2)) distributes its public Parquet index separately from raw file bytes stored in the Software Heritage (SWH) archive. All 28 locally staged Parquet files (`230,786,710` rows) hold the 26-column metadata and provenance index with **no inline `content` column**.

In `Batch 3` (`Laplace#894`), a declarative `.recipe` over native Parquet admits repository, path, language, and SPDX license provenance—and, where target language slices have their SWH blobs or local `.git` repositories staged on disk (never bulk-downloaded over metered `HART-DESKTOP` links), resolves `blob_id`/`content_id` as archive pointers (`key`/`refer`) onto the Tree-sitter AST trunks of the actual UTF-8 source files while filtering out `is_vendor = true` and `is_generated = true` noise.

## Publisher record format

| Record | Fields in order (26 columns) | Target Laplace semantics | Specification |
| --- | --- | --- | --- |
| Software Heritage file-index row (`*.parquet`) | `blob_id`, `directory_id`, `path`, `content_id`, `detected_licenses`, `license_type`, `repo_name`, `snapshot_id`, `revision_id`, `branch_name`, `visit_date`, `revision_date`, `committer_date`, `github_id`, `star_events_count`, `fork_events_count`, `gha_license_id`, `gha_event_created_at`, `gha_created_at`, `gha_language`, `src_encoding`, `language`, `is_vendor`, `is_generated`, `length_bytes`, `extension` | When paired with staged file bytes, `blob_id` / `content_id` / `directory_id` / `revision_id` / `snapshot_id` resolve (`key`/`refer`) to the canonical file AST, directory tree, and `.git` revision trunk; `repo_name`, `path`, `language`, and SPDX `detected_licenses` (`permissive` authority gating) attest repository provenance; `is_vendor` and `is_generated` gate admission; crawl timestamps (`visit_date`, `gha_event_created_at`) and byte-length counters are packaging metadata (`omit`). Without staged blobs, the Parquet shards hold index metadata only and zero source-code text | [BigCode, The Stack v2 dataset card](https://huggingface.co/datasets/bigcode/the-stack-v2) |
