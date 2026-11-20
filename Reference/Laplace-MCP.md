# Laplace-MCP

Laplace-MCP (`SaltyPatron/Laplace-MCP`) builds `lpm` and `Laplace.Modular.Web`, exposing the modular C core, the `laplace` database, and `Laplace-Engine` over authenticated HTTP (`/v1/*`, `/mcp`) and stdio MCP without adding commands to `laplace`.

`lpm` links `Laplace-Native` (`find_package(LaplaceNative CONFIG REQUIRED)`), memory-maps `tier0.bin` and `highway.bin`, decomposes text locally with `lp_text_parts` / `lpm_identify`, queries PostgreSQL through `Laplace-postgres` set functions (`laplace_held_files`, `laplace_holders`, `laplace_containers`, `laplace_claims*`, `laplace_forward`, `laplace_frechet4d`, `laplace_attested`, `laplace_paths`), and invokes `laplace` for full-pipeline CLI operations (`ingest`, `hop`, `translate`, `degrees`, `pull`, `turn`).

## Modes and authentication

- `lpm check`: verifies `tier0.bin` mapping, `Holmes` (`5b7e40e9a23ae55eaccd45646934977d`) and `A` (`32684bfa28c0c84d6f210511aace0efc`) golden IDs, and wall bounds.
- `lpm id STRING` and `lpm text STRING`: offline client-side entity identification and UAX #29 tree inspection.
- `lpm mcp`: JSON-RPC 2.0 MCP server (`initialize`, `ping`, `tools/list`, `tools/call`) over standard input/output for local process callers.
- `lpm serve [HOST [PORT]]`: HTTP listener (`LAPLACE_MCP_HOST`, `LAPLACE_MCP_PORT`). Fails closed at startup unless `LAPLACE_MCP_TOKEN` or `LAPLACE_MCP_TOKEN_FILE` supplies a secret of at least 32 non-whitespace characters; every request except `GET /health` requires constant-time `Authorization: Bearer <token>`.

## HTTP routes and 25 MCP tools

`POST /mcp` accepts both standard JSON-RPC 2.0 MCP envelopes (`tools/list`, `tools/call`) and `{ "op": "<name>", ... }` dispatch onto the `/v1/*` handlers; `GET /v1/surface` and `GET /v1/schema` report the live endpoint, 64-bit mask-bank, vertex-role, and tool schemas, while `GET /health` (liveness) and `GET /health/ready` (DB + `laplace` extension readiness) serve probes.

| Group | Tools / `/v1/<name>` routes | Contract |
| --- | --- | --- |
| Substrate & catalog | `library`, `catalog`, `provenance`, `sources`, `ingest_status`, `recipe_plan`, `recipe_catalog`, `ingest`, `reindex` | Cursor-paginated source/file trunks via `kind` mask (`library`), exact table counts and read-only status (`catalog`), bounded containment DAG ancestry (`provenance`), witness trunks and trust (`sources`, `ingest_status`), `laplace ingest --plan` / `--catalog` (`recipe_plan`, `recipe_catalog`), and live file/workspace admission (`ingest`, `reindex`) |
| Code intelligence | `code_search`, `code_where`, `code_callers`, `code_callees`, `file_outline` | Supersedes the legacy `code-search` service over the `laplace` database alone: UAX #29 + AST LCA search with IDF/BM25 and 4D Fréchet ranking (`code_search`), exact span/symbol containment and enclosing declarations (`code_where`), caller/callee graphs (`code_callers`, `code_callees`), and ordered declaration outlines (`file_outline`) |
| Geometry & ranking | `text`, `embeddings`, `shape`, `rerank` | Offline entity ID/4D coordinate/constituents (`text`, OpenAI-compatible 4D `embeddings`), stored-constituent 4D discrete Fréchet (`shape`), and deterministic containment-IDF + Fréchet document reranking (`rerank`) |
| Web & forward pass | `search`, `forward`, `hop`, `translate`, `degrees`, `pull`, `turn` | Entity discovery, containers, and claims (`search`, `hop`), trajectory continuations (`forward`), concept-bridged translation (`translate`), rated shortest-path distance (`degrees`), single-pass pull (`pull`), and the 11-stage stateful forward program (`turn`, defaulting to `--read` when `session` is omitted) |

Measured on the reference database: `Sherlock Holmes` (`d91895c654f33a108a63bb64f10ca69f`) is named in under a millisecond from mapped `tier0.bin`; `laplace_containers` executed in 3.96 ms; Fréchet against itself was `0` and against `Holmes` `0.221`; ingesting a 43-byte file exited 0 in 0.2 s and returned the file trunk as an exact container.
