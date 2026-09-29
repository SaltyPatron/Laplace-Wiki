# Code corpus

`/vault/models/code-corpus` holds 397,004 files in the old project trees `archive-001-Deleted-Solutions`, `archive-002-projects`, `archive-BACKUP`, `github-canonical`, and `vault-E-Repositories`, 40,190,205,104 bytes by `du -sb` on 2026-09-29.

## Files

| Path | Bytes | What the file is | Proof |
| --- | --- | --- | --- |
| `/vault/models/code-corpus` | 40,190,205,104 | The five old project trees below, 397,004 files | `du -sb` and `find -type f` on 2026-09-29 |
| `/vault/models/code-corpus/archive-001-Deleted-Solutions` | 1,490,809,876 | 35,744 files in 146 numbered snapshot directories of old projects | `du -sb` and `find -type f` on 2026-09-29 |
| `/vault/models/code-corpus/archive-002-projects` | 1,721,317,666 | 24,538 files in project trees, including Hartonomous, AI-Agents, dnd-ai, and my_ai_project | `du -sb` and `find -type f` on 2026-09-29 |
| `/vault/models/code-corpus/archive-BACKUP` | 18,049,512,021 | 110,135 files in backups, including Hartonomous, HART-SERVER, and HART-MCP | `du -sb` and `find -type f` on 2026-09-29 |
| `/vault/models/code-corpus/github-canonical` | 8,085,174,837 | 12,975 files in older project checkouts, including Hartonomous-001, ADUserInfo, and dotnet_iot | `du -sb` and `find -type f` on 2026-09-29 |
| `/vault/models/code-corpus/vault-E-Repositories` | 10,843,390,535 | 213,612 files in project trees, including LotteryAI, Hartonomous, and HART-MCP | `du -sb` and `find -type f` on 2026-09-29 |

## Attestations

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| Old project tree | A directory of project source and its companion files, not a published columnar dataset | Each file under `archive-001-Deleted-Solutions` | The file bytes | The local archive directory | `du -sb` and `find` on 2026-09-29 |
| Old project tree | A directory of project source and its companion files, not a published columnar dataset | Each file under `archive-002-projects` | The file bytes | The local archive directory | `du -sb` and `find` on 2026-09-29 |
| Old project tree | A directory of project source and its companion files, not a published columnar dataset | Each file under `archive-BACKUP` | The file bytes | The local archive directory | `du -sb` and `find` on 2026-09-29 |
| Old project tree | A directory of project source and its companion files, not a published columnar dataset | Each file under `github-canonical` | The file bytes | The local archive directory | `du -sb` and `find` on 2026-09-29 |
| Old project tree | A directory of project source and its companion files, not a published columnar dataset | Each file under `vault-E-Repositories` | The file bytes | The local archive directory | `du -sb` and `find` on 2026-09-29 |

## Records

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| File in an old project tree | No fixed column order; the trees are project directories, not a parquet schema | One of the 397,004 files under `/vault/models/code-corpus` | `find -type f` on 2026-09-29 |

## Lineage

| Paths | What is shared | Proof |
| --- | --- | --- |
| `/vault/models/code-corpus/archive-002-projects` and `/vault/models/code-corpus/vault-E-Repositories` | Twelve shared directory names. `Hartonomous - Progress 001`, `Hartonomous - Progress 002`, `Hartonomous - Progress 003`, `Hartonomous - Progress 004`, `Hartonomous - Starting Point`, `boneyard`, `dns-recovery`, `my_ai_project`, and `server-scripts` have the same relative paths and the same file sizes, and no shared inode. `AI-Agents`, `Hartonomous`, and `dnd-ai` differ in path and size. No file under `code-corpus` has a link count above 1 | Directory walk of relative path, size, and inode on 2026-09-29; `find -type f -links +1` returned 0 |
