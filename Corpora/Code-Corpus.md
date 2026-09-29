# Code corpus

`/vault/models/code-corpus` holds 397,004 files in the old project trees `archive-001-Deleted-Solutions`, `archive-002-projects`, `archive-BACKUP`, `github-canonical`, and `vault-E-Repositories`, 40,190,205,104 bytes by `du -sb` on 2026-09-29.

## Value

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| Old project tree | A directory of project source and its companion files, not a published columnar dataset | Each file under `archive-001-Deleted-Solutions` | The file bytes | The local archive directory | `du -sb` and `find` on 2026-09-29 |
| Old project tree | A directory of project source and its companion files, not a published columnar dataset | Each file under `archive-002-projects` | The file bytes | The local archive directory | `du -sb` and `find` on 2026-09-29 |
| Old project tree | A directory of project source and its companion files, not a published columnar dataset | Each file under `archive-BACKUP` | The file bytes | The local archive directory | `du -sb` and `find` on 2026-09-29 |
| Old project tree | A directory of project source and its companion files, not a published columnar dataset | Each file under `github-canonical` | The file bytes | The local archive directory | `du -sb` and `find` on 2026-09-29 |
| Old project tree | A directory of project source and its companion files, not a published columnar dataset | Each file under `vault-E-Repositories` | The file bytes | The local archive directory | `du -sb` and `find` on 2026-09-29 |

## Format

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| File in an old project tree | No fixed column order; the trees are project directories, not a parquet schema | One of the 397,004 files under `/vault/models/code-corpus` | `find -type f` on 2026-09-29 |
