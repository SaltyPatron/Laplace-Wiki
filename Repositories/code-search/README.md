# code-search

Semantic search over the Laplace repositories for coding agents: an MCP server (stdio) with two tools, backed by
Qdrant and local llama.cpp embedding and reranking servers.

## How a search works

Files are cut into chunks of up to 60 lines (6 lines overlap, at most 900 tokens by the embedding model's own
tokenizer). Code goes to one collection, prose (`.md`, `.txt`, `.rst`) to another, because the two models' vectors
differ in size. A search embeds the query with both models, takes `3k` nearest chunks from each collection (and from
the `CODESEARCH_ALSO_*` collections), reranks the union with the cross-encoder, and returns the best `k`.

| Role | Model | Port on HART-DESKTOP | Collection |
|---|---|---|---|
| code embedding | jina-code-embeddings-1.5b Q8_0, 1536-d | 8711 `/v1/embeddings`, `/tokenize` | `laplace-desktop-code` (desktop), `laplace-code` (hart-server) |
| reranker | Qwen3-Reranker-0.6B Q8_0 | 8712 `/v1/rerank` | |
| prose embedding | Qwen3-Embedding-0.6B Q8_0, 1024-d | 8713 `/v1/embeddings`, `/tokenize` | `laplace-desktop-text` (desktop), `laplace-text` (hart-server) |

Qdrant is on hart-server, `http://192.168.1.2:6333` (LAN) or `http://localhost:6333` on the host. The llama.cpp
servers are installed on HART-DESKTOP as Windows services by `install-gpu-services.ps1` (run once from an elevated
PowerShell; models from `E:\Models\Active`, llama.cpp from `D:\Libraries\llama.cpp-dist`). hart-server reaches them
at `http://192.168.1.3:871x`.

## Tools

| Tool | Arguments | Returns |
|---|---|---|
| `search` | `query` (string, required); `k` (1-50, default 10); `scope` (`all`, `code`, `prose`; default `all`); `repo` (one repository label, such as `Laplace` or `Laplace-Engine`) | list of `{score, repo, path, start, end, text}`; `path` begins with the repository label, lines are 1-based and inclusive |
| `reindex` | `paths` (list of absolute file paths, optional) | a summary line; without `paths`, every file whose size, time or content changed since the last index |

## Running it

| Host | Server | Index / search from a shell |
|---|---|---|
| HART-DESKTOP | `run.cmd` | `run.cmd index`, `run.cmd watch`, `run.cmd search QUERY...` |
| hart-server | `run` | `uv run python codesearch.py index` (or the `code-search-watch` user unit, `systemd/`) |

`run.cmd` indexes the desktop's Laplace checkouts (whatever branch each is on) into the desktop collections and also
searches hart-server's collections, so one search covers both.

Environment (`run.cmd` sets the desktop values; every name but `CODESEARCH_KEY` is optional):

| Name | What | Default |
|---|---|---|
| `CODESEARCH_ROOTS` | roots separated by the OS path separator, each `PATH` or `LABEL=PATH` | hart-server's `/repos/src` repositories |
| `CODESEARCH_EMBED_HOST` | scheme and host of the llama.cpp servers | `http://192.168.1.3` |
| `CODESEARCH_KEY` | bearer key for the llama.cpp servers and `api-key` for Qdrant (the one `install-gpu-services.ps1` configures) | none: required. hart-server: `~/.config/code-search/env`; HART-DESKTOP: a user environment variable |
| `CODESEARCH_QDRANT` | Qdrant URL | `http://localhost:6333` |
| `CODESEARCH_CODE_COLLECTION`, `CODESEARCH_TEXT_COLLECTION` | collections this host writes | `laplace-code`, `laplace-text` |
| `CODESEARCH_ALSO_CODE`, `CODESEARCH_ALSO_TEXT` | other collections of the same models a search also reads, comma-separated | none |
| `CODESEARCH_STATE` | file of size/mtime/sha per indexed file | `state.json` beside `codesearch.py` |

## Registering with an agent

Codex (`~/.codex/config.toml`) on HART-DESKTOP:

```toml
[mcp_servers.code-search]
command = "cmd"
args = ["/c", "E:/Repositories/Laplace/code-search/run.cmd"]
```

Claude Code:

```
claude mcp add --scope user code-search -- cmd /c E:/Repositories/Laplace/code-search/run.cmd   # HART-DESKTOP
claude mcp add --scope user code-search -- /home/ahart/tools/code-search/run                    # hart-server
```

VS Code (`mcp.json`):

```json
"code-search": { "type": "stdio", "command": "cmd", "args": ["/c", "E:/Repositories/Laplace/code-search/run.cmd"] }
```

Check the services before blaming the index: `curl -H "Authorization: Bearer $KEY" http://127.0.0.1:8711/health`
(likewise 8712, 8713) and `curl http://192.168.1.2:6333/collections`.
