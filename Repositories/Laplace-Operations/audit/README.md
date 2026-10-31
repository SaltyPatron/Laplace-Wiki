# Repository configuration audit

This inventories source; it does not install Laplace, select storage, provision hosts, or establish effective runtime configuration.
The collector uses GitHub's repository list and immutable default-branch commits, plus explicitly supplied local roots.
Local discovery has no depth limit. It records skipped dependency/OS directories and unreadable metadata, and includes
family checkouts whose old remotes use another account, Azure DevOps, or no origin. It does not follow directory links.

Requires PowerShell 7, authenticated `gh`, Git, and Node 24 (built-in SQLite). No npm packages are required.

```powershell
# Set these to the audit destination and roots being investigated; no drive or host is assumed.
./audit/run.ps1 -Owner SaltyPatron -Output $auditDirectory -LocalRoots $repositoryRoots
node ./audit/serve-index.mjs --output $auditDirectory
```

The viewer prints a loopback URL and writes it to `viewer.json`. It serves only audit files and read queries. It creates
no Windows service, scheduled task, network route or persistent application installation. Stop that Node process to stop
the viewer. Cached GitHub revisions are reused unless `-Refresh` is supplied. Use a new output directory to retain a
previous complete audit. `--append` on the scanner adds newly discovered checkouts without duplicating previous snapshots.

## Outputs

| File | Purpose |
| --- | --- |
| `configuration.sqlite` | Complete occurrence/glossary database and full-text search index |
| `index.html`, `data.js` | Viewer and coverage metadata |
| `environment-glossary.json` | Names with a direct environment reader, assignment/reference, or declaration |
| `environment-contracts.json`, `environment-contracts.csv` | Source-level definitions and consumers, including credential names, mixed-case names, wrapper flags, shell inputs, GitHub variables/secrets and service declarations; computed-name locations and changed local files are explicit |
| `repository-index.json` | Every repository's environment names, category counts and configuration-file source links |
| `configuration-review.json` | Reviewed precedence, units, capacities, resource equations and cross-repository findings with acceptance checks |
| `reviewed-glossary.json`, `findings.json` | Reviewed meanings and findings, tied to the reviewed source revisions |
| `glossary.json` | Every indexed term, expressions, source comments and locations; unreviewed meanings stay unreviewed |
| `occurrences.jsonl`, `occurrences.csv` | Full lexical results, including compile-time and process-local name candidates |
| `variants.json` | Different definition expressions requiring review; not automatically contradictions |
| `coverage.json`, `acquisition.json` | Revisions, source scopes, timestamps, scanner hashes and failure status |
| `files.json`, `skipped.json` | Every scanned file hash and every excluded tree entry |
| `repository-discovery.json`, `discovery.json` | Local discovery boundaries and scan decisions |
| `scanner-versions/` | Exact collector source bytes used for each generation pass |
| `verification.json` | Tree reconciliation, sampled source/hash/line checks, local drift and search timings |

The lexer covers environment access, configuration files, absolute/derived paths, CMake settings, CLI options, named
numeric assignments/constants, array bounds, SQL settings/query bounds and threshold comparisons. Tests, documentation,
generated code and historical material remain searchable. These are **source occurrences**, not a count of independent
settings. General shell/CMake names and `LAPLACE_*` identifiers are labelled `environment-candidate`; the environment reader catalogue separates
direct evidence from name matching. Numeric assignments can be ordinary implementation variables rather than configurable limits.

Text files have no size cutoff. Binary assets, private keys, LFS payloads and submodule contents are listed as excluded.
Tracked text inside a vendored directory is still scanned. Dynamic names, wrapper APIs and computed values require semantic
review; a lexical inventory cannot prove exhaustiveness for those. Credential-bearing contexts are suppressed, not exported
as secret values. CSV cells that could be interpreted as formulas are escaped.

Manual descriptions are applied only when the relevant pinned source revisions match the reviewed snapshot. A later revision
does not inherit a false “reviewed” result. A captured local checkout can change afterward; verification reports that drift
instead of attributing new bytes to the earlier snapshot.

```powershell
node ./audit/test-configuration-index.mjs
node ./audit/verify-index.mjs --output $auditDirectory
```

The regression fixture checks actual Git snapshots, local edits, multiline environment readers, paths, constants, SQL
settings/bounds, unusual text extensions, credential suppression, binary/LFS exclusions, repeat append behavior, full-text
index coverage, and rejection of compile guards/printf tokens as proven environment readers.

The environment projection re-reads captured source blobs and verifies hashes before extracting definitions and consumers.
This retains credential **names** even when the lexical export suppressed their contexts, and excludes SQL `SET` from
environment definitions. Dotted test-project names are classified as tests. CMD assignments and shell references remain
labelled as process/shell state; their presence does not imply that they are supported operator controls. The source contracts
include comments and exact expressions, while the reviewed cross-repository report explains selected precedence and resource
relationships. No effective values are invented for dynamically computed names or changed local files.
