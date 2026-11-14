# Laplace-MCP API

Laplace-MCP is the HTTP service in front of Laplace. A caller sends content or an ID it already holds. This process maps tier 0, names the entity, and calls the database functions. The caller is not linked to Postgres and does not send SQL.

The process listens on `127.0.0.1:5188`. nginx `laplace-managed` proxies `POST https://hart-server:8443/mcp` to `http://127.0.0.1:5188/mcp`. The same bodies are served on `/v1/...` directly.

`LAPLACE_CONNINFO` selects the database. Deployment supplies the selected connection and resource closure; callers must not depend on development-machine or libpq defaults.

Nothing about the machine is compiled in but a default. The process reads, from its environment (the unit takes the machine's `/etc/laplace/machine.env` when there is one):

| Name | What | Unset |
|---|---|---|
| `LAPLACE_MCP_HOST`, `LAPLACE_MCP_PORT` | the address and port `lpm serve` listens on; `lpm serve HOST PORT` still wins | `127.0.0.1`, `5188` |
| `LAPLACE_CONNINFO` | the selected database connection | must be supplied by the owning installation |
| `LAPLACE_ENGINE` | the engine program the routes run | `$LAPLACE_BUILD/Laplace-Engine/icx-release/laplace`, or `/repos/build/...` without `LAPLACE_BUILD` |
| `LAPLACE_GRAMMARS` | the directory of compiled tree-sitter grammars | `/repos/build/grammars` |

It is built as the engine is (`CMakeLists.txt`): Laplace-Native as part of it, with icx under the floating-point contract and laplace-math, and the engine's reader (`read.c`, `pg.c`) from `LAPLACE_ENGINE_SRC` (the engine's `src` beside this repository). The defaults in the table are what the build was configured with (`native/config.h.in`): the value in the environment at configure time, else the deployment target's.

One process holds one database connection. `lpm serve` is that process. `laplace_mcp.py` is not.

## Deployed clients

Configured editor clients use the deployed authenticated HTTPS MCP endpoint,
not an editor-launched native process. On the desktop installation:

| Endpoint | Surface |
|---|---|
| `https://dev.hartonomous.com/modular/mcp` | native Laplace-MCP, including code search and substrate code reads |
| `https://dev.hartonomous.com/mcp` | monorepo substrate tools; a different catalog |

VS Code's native code client is:

```json
{
  "laplace-code": {
    "type": "http",
    "url": "https://dev.hartonomous.com/modular/mcp",
    "headers": { "Authorization": "Bearer <enrolled MCP credential>" }
  }
}
```

The placeholder is not a credential. Use the installation's existing MCP
identity; do not put real credentials into repository examples. Other MCP
clients, including Codex, should select the same deployed endpoint using their
HTTP transport configuration. Do not substitute a build-tree executable.

`laplace-ops deploy -Target desktop -Components modular-web` verifies the
installed native tool catalog and a real authenticated code search before
migrating the owned VS Code `laplace-code` entry from stdio to HTTP. It preserves
unrelated client settings and the existing same-origin identity. Setup owns IIS
topology, identities and permissions; ordinary deployment does not provision
another host or CI runner. See the [modular browser and MCP host](../web/README.md).

## Who may call it

`lpm serve` takes a bearer token: `LAPLACE_MCP_TOKEN`, or the `LAPLACE_MCP_TOKEN=` line of the file `LAPLACE_MCP_TOKEN_FILE` names. Without one of at least 32 characters and no whitespace it does not listen; it exits 2. Every request but `GET /health` sends `Authorization: Bearer <token>`; any other gets `401` with `WWW-Authenticate: Bearer` and `{"error":"unauthorized"}`, and nothing is dispatched. On hart-server setup makes the token once, in `/etc/laplace/secrets/modular-mcp.env` (root and `laplace-runner`, 0640), and the unit reads it. `lpm mcp` over stdio takes none: it is the calling user's own process.

## What a caller sends

Jina's embedding API is `POST https://api.jina.ai/v1/embeddings` with a JSON body of `model` and `input` (a string or a list of strings, and for some models an image or a PDF). The response is a list of float vectors. See [Jina embeddings](https://jina.ai/embeddings/).

`POST /v1/embeddings` takes one string in `input` and returns the entity instead of a vector.

```json
{"input":"Sherlock Holmes"}
```

```json
{"object":"list","model":"laplace","data":[{"object":"record","index":0,"id":"d91895c654f33a108a63bb64f10ca69f","tier":3,"coord":[-0.43097229504208512,-0.40779169540644233,-0.30074172951672307,-0.71703307803402827],"hilbert":"05f75fb4b4f82a49","parts":["ee7048d5a4b2e11e5223e57a5bd579a4","00263ca9f57f7177f495e3711f8cdd59","5b7e40e9a23ae55eaccd45646934977d"]}],"ms":{"identity":0.123}}
```

The ID, tier, coordinate, Hilbert value, and parts are computed here from the mapped tier 0 (`lp_text_parts`). Measured identity time on this call was 0.123 ms. A second call on the same process was 0.025 ms. No database is used.

`input` is one string, up to 8192 bytes. A list of inputs, an image, and a PDF are not accepted yet.

## Search

The browser-oriented read extensions are additive:

- `POST /v1/library` discovers stored source/file trunks through the native
  `kind=file` physicality role, regardless of witness registration. `after` is
  an optional canonical-ID cursor; a page returns up to 64 trunks, `has_more`
  and `next`. Source children retain their stored content order.
- `POST /v1/provenance` takes `id` and returns bounded structural ancestry:
  nodes, ordered edges (ordinal, position, run, said, outcome), source/file
  display metadata, and registry metadata separately. Bounds are 16 levels,
  512 nodes and 64 holders per kind and frontier member. `complete=false`
  means more ancestry may exist. Structural containment is not itself an
  assertion; `search.attestations` remains the attestation projection.
- `POST /v1/catalog` returns the connected database, read-only state, exact
  table counts and observation time. `registered_witness_rows` counts registry
  rows only, not all source trunks in the DAG.
- `search` accepts `display:true` for bounded Native-rendered labels and trunk
  metadata. `recorded` reports database recording; canonical cache content can
  be present without a database row. `storage` distinguishes `database`,
  `tier0-cache`, `highway-cache`, `computed` and `unresolved`.
  Physicality rows include their mask string and original vertex annotations
  alongside expanded constituent IDs. Labels are display projections.

These reads are also MCP tools (`library`, `provenance`, `catalog`). JSON-RPC
envelope IDs and `params.arguments.id` are separate. JSON Unicode escapes and
direct UTF-8 resolve to the same canonical identity.

`POST /v1/search` with `{"input":"Sherlock Holmes"}` or `{"id":"d91895c654f33a108a63bb64f10ca69f"}`.

The string is named by Native. Root and first-level member identities are read
through the Engine reader's `holds_above`, `attested`, `paths_of` and `tiers_of`
operations. The response retains root calculation, physicalities, claims,
containing structures, attestations and per-member reads separately.

`discovery` declares `schema: "laplace-discovery/v1"`, `query_kind` (`text` or
`id`), `root_present`, `members_complete`, `scope: "returned-read"` and
`matches`. Only known database or selected canonical-cache content appears in
matches. A calculated root can have an ID, coordinate and decomposition while
being absent from discovery matches. Known members and their recorded relations
remain available even when that complete root has not been recorded.

Each match includes `id`, `tier`, `match` (`exact` or `member`), `recorded`,
`storage` and `stored_tier`. Member matches add `via` (the query root ID) and
zero-based `ordinal`. Repeated equal members retain separate query positions.
These positions describe the query decomposition; they are not stored witness
occurrences, and their count is not a witness count. Canonical ID input is
normalized to lowercase hexadecimal.

Text and cache decomposition return at most 64 first-level parts.
`parts_total`, `parts_complete` and `discovery.members_complete` expose that
bound. An incomplete prefix does not establish that later members are absent.
Stored physicalities and containing paths retain their own returned order.
`fan`, when positive, caps claims and containing structures for each read;
omitting it returns the available rows. This response is not a global ranked
collection, a snapshot cursor or a complete semantic discovery protocol.

`GET /v1/schema` returns each selected Highway bank's layout and its canonical
`values: [{slot, id, label}]`. Slot and identity come from that frozen Highway
generation. This enumerates governed mask values; it does not declare global
search predicates, facet counts or operators that the endpoint does not implement.

`tests/deployed/read-snapshot.py` verifies this contract against the deployed database,
including unrecorded phrase roots, recorded repeated members, cache-only
content, bounded prefixes and HTTP/MCP parity.

## Shape

`POST /v1/shape` with `{"input":"...","other":"..."}`.

Both strings are decomposed here. `laplace_frechet4d` is called on two linestrings built with `ST_MakeLine` of the stored `entity.coord` of those constituents, in constituent order. The comparison is the database function.

| Pair | Fréchet | Time |
|---|---|---|
| Sherlock Holmes against itself | 0 | 15.3 ms |
| Sherlock Holmes against Holmes (`5b7e40e9a23ae55eaccd45646934977d`) | 0.22124873411843002 | 25.9 ms |

`laplace_frechet4d(geometry, geometry, integer)` (up to 8 skipped vertices), `laplace_dtw4d`, and `laplace_edr4d` are installed and are not separate endpoints yet.

## Forward

`POST /v1/forward` with `{"input":"..."}` calls `laplace_forward` on the constituent IDs.

For `Sherlock Holmes` the service returned, in 16.4 ms, the span of the two words held by 2 paths as a run twice, followed by Holmes (`5b7e40e9a23ae55eaccd45646934977d`, times 2), and the word Holmes held by 6 paths.

## Ingest

`POST /v1/ingest` with `{"path":"/absolute/path"}` runs the engine (`LAPLACE_ENGINE`) as `laplace ingest` on that path. That is the engine pipeline: decompose, deduplicate trunk to leaf, record, attest. The body must be an absolute path that exists. The call blocks until ingest exits.

A proof file `/tmp/lpm-api-proof.txt`, one line `Sherlock Holmes kept his pipe on the mantel.` plus a newline, exited 0 in 0.2 s: 1 file, 15 compositions, 4 new entities, 11 subtrees already recorded, 0 attestations. Searching the exact bytes, ID `f27bdacd15c996339ccee43dd4153450`, returned one container, `221c6d0ef03f1be62c3625e9625f32db`, tier 4, whose text is the filename and that line.

## Surface

`GET /v1/surface` lists the routes this process serves, the database functions those routes call, the engine's twenty-one commands, and the reads that are specified and not yet a route.

`GET /health` answers without the database.

Served now: library, catalog, provenance, schema, embeddings, rerank, code_search, reindex, code_where, code_callers, code_callees, sources, ingest_status, file_outline, recipe_plan, recipe_catalog, search, forward, shape, ingest, hop, text, translate, pull, degrees, surface, health. `hop`, `text`, `translate`, `pull` and `degrees` run the engine command of that name on `input` (`translate` also takes `from` and `to`; `degrees` takes `other`) and return its exit code and log. HTTP routes and MCP tools are separate catalogs; `/v1/surface` and `tools/list` describe their respective installed surfaces.

Engine commands that are not a route here: tier0, flags, highway, deploy, forget, sweep, index, structure, tree, turn, fills, status, bench, model; `sources` is read from the database rather than run. `hop` is the engine's program over the same container and claim reads search calls. `fills` in the engine is containers, then `lp_follows` for the exact run, then a parent walk through `laplace_fills`. `laplace_fills` by itself is that parent walk, so this service does not expose it as "what follows."

Specified past these routes, and not built as their own endpoints: turn, gaps, file metadata as its own read, DTW, EDR, Fréchet with skipped vertices, and the forward stages RESOLVE, COUPLE, ORIENT, ROUTE, SCAN, PROPOSE, STEER, SELECT, REALIZE, WITNESS. `laplace_couple` is the installed operator that returns strands, containment, and shape in one call. Search calls containers and claims as two reads inside one statement. It does not call `laplace_couple`.

## MCP

`POST /mcp` also speaks MCP JSON-RPC when the body contains `"jsonrpc"`. The native catalog exposes 24 tools: `library`, `catalog`, `provenance`, `code_search`, `code_where`, `code_callers`, `code_callees`, `ingest_status`, `sources`, `file_outline`, `recipe_plan`, `recipe_catalog`, `reindex`, `rerank`, `search`, `embeddings`, `shape`, `forward`, `ingest`, `hop`, `text`, `translate`, `degrees` and `pull`. `tools/list` is authoritative for each installed release's catalog and arguments. Database grants and installed resource access still constrain what a tool may execute.

The following loopback configuration and handshake are historical direct-listener
examples, not the current desktop editor configuration:

```toml
[mcp_servers.laplace]
url = "http://127.0.0.1:5188/mcp"
headers = { Authorization = "Bearer ${LAPLACE_MODULAR_MCP_TOKEN}" }
```

An earlier `grok mcp doctor laplace` run reported handshake OK, protocol 2025-11-25, and 5 tools in that release. A Grok process restricted to `laplace__search` called `search` on `Sherlock Holmes` and received the six containers and three claims. These observations are not the current tool count or protocol contract. A session that was already open before `grok mcp add` does not gain the tool; `use_tool` in that session returns tool not found until a new session loads the config.

## nginx

```
curl -skS --resolve hart-server:8443:127.0.0.1 \
  -X POST https://hart-server:8443/mcp \
  -H 'Content-Type: application/json' -H "Authorization: Bearer $LAPLACE_MODULAR_MCP_TOKEN" \
  -d '{"op":"search","input":"Sherlock Holmes"}'
```

`op` is any route by its name (`search`, `code_where`, `file_outline`, ...), `embed` for `embeddings`, `frechet` for `shape`, or `surface`.

## Code search

`code_search`, `rerank` and `reindex` answer from the database (`LAPLACE_CONNINFO`), as the other code tools do: nothing is indexed by the process and nothing is read from a working tree. They read what a recipe source ingested, by default the `workspace-code` source of Laplace-Engine, whose witness is `Laplace Workspace`.

A query is decomposed as all text is (Native UAX #29). Its terms are its word segments that hold a letter or digit and each run of segments with no space between them (an identifier such as `lp_ref_compose`, a dotted or hyphenated name), each once, at most 64; each is the entity that content is wherever it was recorded. How common a term is comes from one capped read of the container index: the paths that hold it directly. A term held directly by more than `LAPLACE_CODE_HUB` paths of a kind is a hub and is not walked. Every other term is walked up the container index to the files of the source's witness in one call inside PostgreSQL (`laplace_held_files`), and each file comes back with its unit, the lowest node of its content that holds the terms it holds (their common ancestor, else the node holding the most of them), the unit's tier and each term's occurrences below it.

Each file's unit is scored by BM25 over the terms' occurrences (IDF `log(1 + (N - df + 0.5) / (df + 0.5))` with N 64 times the hub cap, `k1 = 1.2`, `b = 0.75`), the unit's tier standing for its length against the mean of the units'. Over `scope` `all`, documentation and data files weigh 0.35, tests 0.25 and C headers 0.85. Text is read only for the hits returned: each unit's lines in its file's recorded text, and its first 60 lines.

`code_search` takes `query` (required), `limit` (1 to 64, default 15), `path` (a substring the file's path must contain), `source` (the witness whose files are searched; default `LAPLACE_CODE_SOURCE`, else `Laplace Workspace`), `scope` (`all`, `code` or `docs`), `bridge` and `explain` (every candidate, not only the first `limit`). Each hit has `rank`, `path`, `line0`..`line1` (1-based, of the unit in the file's recorded text), `id` (the unit) and its `hilbert`, `shared` (terms the unit holds), `rerank` (the score as a share of what the query's terms could give, with the scope's weight) and `bm25` (the raw score), and `snippet`. The answer also has `docs` (the witness's files), `witnesses` (how many witnesses have that name), `entities` (files the walk reached), each term with its `holders`, `idf`, `hub` and `walked`, `candidates` (`reached`, `kept`), `levels`, `cut` (the walk stopped at `LAPLACE_CODE_NODES` nodes) and `phases_ms`.

`bridge: true` (or `LAPLACE_CODE_BRIDGE=1`) adds words reached through the Engine's attested translation relations to the query. Engine execution failures are reported as errors. The added words are expansion candidates; they do not establish that a query's sense has been resolved.

The [invention's query-relative coupling field](https://github.com/SaltyPatron/Laplace/blob/main/docs/INVENTION.md#7-the-query-relative-coupling-field) requires joint interpretation across the whole observation and permits ambiguity among surviving alternatives. Global usage frequency or a single overlap score does not establish a unique sense. Search expansion must retain that distinction; it cannot substitute for the required joint interpretation.

`rerank` takes `query`, `documents` (up to 256 texts) and `top_n` (1 to the number of documents). Each document scores the IDF, over the database's containment, of the query's terms it holds, as a share of all the query's terms: a document holding none of them scores 0, one holding all scores 1. Ties go to the shorter document. Each result has `index`, `relevance_score` and `shared`.

`reindex` runs `laplace ingest` of the code source again (`LAPLACE_CODE_INGEST`, default `workspace-code`, whose recipe supersedes what changed), or of one absolute file or directory given as `path`, and returns the engine's exit code and log.

| Name | What |
|---|---|
| `LAPLACE_CODE_SOURCE` | the witness `code_search` reads when a call names none (default `Laplace Workspace`) |
| `LAPLACE_CODE_HUB` | paths of a kind holding a term directly past which it is a hub (default 4096) |
| `LAPLACE_CODE_NODES` | nodes the walk up the container index reads before it stops (default 400000) |
| `LAPLACE_CODE_INGEST` | the source `reindex` ingests (default `workspace-code`) |
| `LAPLACE_CODE_BRIDGE`, `LAPLACE_CODE_BRIDGE_LANGUAGE`, `LAPLACE_CODE_BRIDGE_CONCEPTS` | `bridge` by default; the language it translates from (default `en`); concepts per word, 1 to 99 (default 2; any other value is an error) |

`LAPLACE_CODE_HUB` and `LAPLACE_CODE_NODES` are positive whole numbers; any other value is an error, not the default.

`tests/code-search-eval.py LPM [--scope all,code] [--min-mrr X]` asks ten questions about the Laplace repositories through `lpm mcp` and reports where each scope puts the file that answers each (hit@1, @5, @10, mean reciprocal rank at 10, median latency). Run it against a database holding the `workspace-code` ingest; it fails where `LAPLACE_CONNINFO` names none or the witness is absent.

### Optional local stdio

`lpm mcp` remains available for an explicitly selected local CLI or test process,
with one JSON-RPC message per line. It is not the configured editor integration
and does not verify the deployed HTTP endpoint. The following Codex example
illustrates that optional local mode only; configured editor clients use
[deployed HTTP](#deployed-clients):

```toml
[mcp_servers.laplace-code]
command = "D:/Libraries/build/Laplace/Laplace-MCP/icx-release/lpm.exe"
args = ["mcp"]
env = { LAPLACE_CONNINFO = "host=HART-DESKTOP dbname=laplace" }
```

## Code from the database

`code_where`, `code_callers`, `code_callees`, `sources`, `ingest_status` and `file_outline` read the database (`LAPLACE_CONNINFO`) too: they answer for code a recipe source ingested, such as Laplace-Engine's `workspace-code`. Nothing is read from a working tree.

`code_where` takes `query` (required: a name, or any exact span of code), `path` (a substring the file's path must contain), `defines` (true: only files that define it), `limit` (files, default 20), `occurrences` (per file, default 3, at most 16) and `context` (bytes, default 120). It walks up the container index from the query's entity through every path that holds it to the files: a file is a trunk over its metadata and its content, and the walk stops there. Each hit has `path` (the file's pathname record), `file` (its trunk ID), `defines` (the declaration kinds the code recipe said of the name in that file, such as `function_definition` or `class_declaration`; files that define it come first), `occurrences` (how many places in its syntax tree hold it) and `at`: for each place, `line`, `context` (the innermost enclosing node of at least `context` bytes), `enclosing` (the first line of the outermost enclosing node under 8 KiB below the file, usually the declaration) with its span `line0`..`line1`, and `depth`. Lines are counted in the file's recorded content. The answer also has `files`, `nodes` and `levels` walked, and `cut` when the walk reached 400,000 nodes and stopped (a name as common as `return`).

`sources` returns each witness in the database: `id`, `name` (the first part of its trunk) and `trust`.

`file_outline` takes `path` (the end of a file's pathname, matched at a `/` boundary) or `file` (the file's ID, as `code_where` returns it). For each matching file (up to 16) it returns `path`, `file`, `bytes`, and `declarations`: the claims `[kind, name]` its code recipe said of it, in the order said, each with `line`, the first line at or after the previous declaration where `name` stands as a whole word. A C recipe says parameters as well as functions, so a C function's parameters follow it.

`code_callers` takes `query` (required: a declared name), `path` (a substring the file's path must contain) and `limit` (callers, default 50). Each place `code_where` finds the name (a path up from it that is not a claim) is a chain of nodes below its file, each found where it stands in the file's recorded content. A node that starts on the line of a declaration in the file's outline, and holds that declaration's name in its first line before the place, is that declaration's node; the innermost one holds the place. `callers` lists those declarations: `name`, `kind`, `path`, `file`, `line` (the declaration's) and `at` (the lines of its uses). A place that no declaration holds is listed in `top_level` (`path`, `file`, `at`). A declaration's own name, its head, is not a use of it. Same-named declarations in different files are not told apart. The answer also has `files` and `cut`, as `code_where` has.

`code_callees` takes `query` (required: a declared name) and `path` (a substring the defining file's path must contain). For each definition of the name (a file that defines it, at a line its outline gives), its code is the outermost node of the place's chain that starts on that line. `definitions` lists `path`, `file`, `kind`, `line0`..`line1` and `callees`: each name in that code followed by `(` that a code recipe declared, meaning a claim `[kind, name]` said by a file's record of claims, or, when that record would hold only the one claim, the claim said in its place as the record (the engine says a record of one claim as that claim). Each callee has `name`, `kind`, `declared_in` (how many files) and up to 4 `files` (`path`, `file`). `outside` lists the names it calls that nothing in the database declares, such as a library's or the language's.

`ingest_status` takes `source` (optional: one source's name) and reads only. `sources` lists each witness with `id`, `name` (the first 200 bytes of its record), `trust`, `parts` (how many parts its trunk holds after its record) and `readings` (how many witnesses begin with the same record). More than one reading is a source read again without superseding its earlier reading (Laplace-Engine `supersede`). `activity` lists the database's sessions that are not idle, as `pg_stat_activity` shows them to this role: `pid`, `user`, `state`, `seconds` and `query` (200 bytes). `logs` lists the engine's per-source ingest logs from `LAPLACE_INGEST_LOGS`, else `$LAPLACE_WORK/logs/ingest`, newest first, at most 20: `source`, `modified` (UTC), `bytes` and `last` (the last line). It is `null` when neither directory is set or readable.

`recipe_plan` takes `input` (optional: a source name or a path) and returns `exit` and `log` from `laplace ingest --plan`: which recipe reads which files, with nothing read into the database. Without `input` it plans every source in order.

`recipe_catalog` takes no arguments and returns `exit` and `log` from `laplace ingest --catalog`. Parse `log` as JSON for the complete available source and decomposer catalog: canonical names, short aliases, witnesses, content roots and filename patterns, recipes, file formats, and prerequisite sources. It lists definitions without opening a database or requiring corpus files. The same operation is available over HTTP at `POST /v1/recipe_catalog`.
