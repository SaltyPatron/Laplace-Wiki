# Installed Laplace: repositories, environments and commands

Updated 2026-10-13 from installed commands, actual desktop builds, SSH service/revision
readback and HTTPS requests. Research/historical repository observations below are from
October 11. This records installed surfaces and remaining gaps, not whole-product acceptance.

## Where to run ingestion

The intended workflow is an ordinary, non-admin terminal on hart-desktop, from any working directory.
The CLI reads input on the machine executing it and connects to the selected substrate database.
A remote database does not require mounting source or build trees. A server ingestion API reads
server paths unless its API explicitly uploads the files.

The installed `laplace-mono` and `laplace` commands resolve from the desktop's normal terminal
and hart-server's interactive login. They select different databases and product interfaces.
Monorepo recipe ingestion delegates to the modular Native Engine; that shared ingestion
implementation does not establish parity for the rest of the product:

| Entry point | Current behavior and location |
| --- | --- |
| Monorepo `laplace-mono` | Accepts `ingest document <file-or-directory>`, singular. Desktop launcher selects `E:\Data\Laplace\clients\laplace-mono\client.json` and the CLI in the installed IIS release. Server launcher selects `/home/ahart/.local/share/laplace-mono/client.json` and `/opt/laplace/app/cli/Laplace.Cli`. `--where` prints the resolved executable, profile and database without credentials. |
| Modular `laplace` | Desktop launcher selects `E:\Data\Laplace\clients\laplace\client.json` and the packaged executable under `E:\Data\Laplace\services\laplace\releases`. It includes native libraries, grammar libraries, recipes and firmware. Live `status` reaches HART-DESKTOP and matches both artifact fingerprints. Server launcher selects `/home/ahart/.config/laplace/client.json` and `/hosting/laplace/modular/current/bin/laplace`. |
| Refactor `Laplace-Refactor` | Frozen historical reference repository retained strictly for recipe-driven ingestion design context; not an active runtime or installation target. |
| Operations `laplace.ps1` | Development/build/deployment controller, not the ingestion CLI. |
| Operations `ingest.ps1` / `ingest.sh` | Modular ingestion wrappers still tied to build-tree locations and their environment. |

From any desktop directory:

```powershell
laplace-mono --where
laplace-mono ingest document 'E:\path\to\documents'
laplace --where
laplace status
```

The monorepo desktop development profile selects HART-DESKTOP database `laplace-mono`,
role `laplace_desktop_db`, using SSPI. The modular client selects HART-DESKTOP database
`laplace` as Windows operator `ahart`, also through SSPI and verified TLS. Explicit staging
selection remains available: monorepo profile `staging`, or modular `LAPLACE_CLIENT_CONFIG`
pointing to `E:/Data/Laplace/clients/laplace/client-staging.json`. The background modular MCP
uses its separate service identity. Raw Operations
build/ingest wrappers still have their own environment resolution; do not infer a target from
the word "Laplace" alone. Read the selected client configuration or `--where`.

The modular client profile declares optional `source` and `models` input roots alongside
`data`. The installer accepts `--source` and `--models`; desktop setup captures these from
the host declaration or machine configuration. The launcher exports them as `LAPLACE_SRC`
and `LAPLACE_MODELS` to the Engine and reports them under `inputs` in `--where`. Normal
commands do not require dot-sourcing a developer shell. A missing model directory is an
absent source, not an instruction to download models. Use `ingest --plan <source>` before
loading; a plan that names an absent source still reports failure.
`installation/install-windows-client.ps1 -Installation <host-declaration> -SkipPackage`
reinstalls the command against the existing package, validating Native composition and
both database artifact fingerprints before replacing the launcher.

The modular CLI is not a replacement for all `laplace-mono` capabilities. In particular,
checkpoint testimony (`laplace model`) does not replace Foundry synthesis/export. The
monorepo also owns document adapters, persisted ingestion journals, application APIs,
auth/billing and chess workflows. Their functional SQL schemas and operator contracts
must survive modularization; a successful Engine or perf-cache proof does not verify them.

## Repositories and deployments

| Repository | Desktop | hart-server | Production / other deployment |
| --- | --- | --- | --- |
| Laplace | Named IIS site and installed `laplace-mono`; separate source development API | API/UI, separate monorepo MCP and CLI installed | API/UI on hart-prod; nginx `/mcp` forwards to hart-server:8080 |
| Laplace-Native | Included in installed modular client; source checkout is separate | Included in modular package | No separate modular installation identified |
| Laplace-postgres | Modular extension 1.12 in the one custom PostgreSQL 18.6 installation; local `laplace` database | Modular extension files installed; `laplace` database exists | Distinct from monorepo substrate; equivalent modular deployment not established |
| Laplace-Engine | CLI installed with native/resource closure | CLI in modular release | Modular installation location absent on hart-prod |
| Laplace-MCP | Source; expected Windows executable absent | Separate modular MCP service active | Modular installation location absent on hart-prod |
| Laplace-Operations | Shared/modular setup; existing mono build/deployment controller delegates CLI publication to Laplace | Default setup owns shared/modular services; explicit mono compatibility stages forward to the monorepo installer | Shared configuration; monorepo owns its own application delivery |
| Laplace-UCI | IIS connector and its credential agent installed; chess selection remains a separate application capability | Chess controller/client configuration installed | Environment selection belongs to the existing chess controller; complete play/ingest acceptance remains open |
| Laplace-Refactor | Frozen reference checkout (recipe-driven ingestion context) | Frozen reference checkout | Frozen reference only; not deployed |
| Laplace-Conventional | Python/GPU evaluation checkout | Source/runner present | No verified deployment |
| Laplace-Wiki | Source | Source | Documentation publication workflow, not an application runtime |
| Laplace-Research | Not in canonical source root | Research checkout | No application deployment established |
| Laplace-Prototype | Not in canonical source root | Experimental storage checkout; documented DB port 5439 gives no response | Separate experiment |
| Laplace-Patreon | Not in canonical source root | Publication drafts | README states nothing published |
| Laplace-Scratch | Not in canonical source root | Preserved session scripts; originals copied, not moved | Not an application installation |
| Laplace_Hartonomous-Old | Historical copies require separate identification | Earlier implementation checkout | No current runtime established |
| Laplace_Hartonomous-Old- | Historical copies require separate identification | Earlier implementation checkout | No current runtime established |

hart-cloud is deliberately `TERMINATED` (`c3-standard-8`), for on-demand AVX-512 qualification,
development and benchmarks. Its stored runtime was not reverified by starting it. hart-server is
the local verification deployment; hart-desktop owns development and optional GPU work. OpenBao
and Vaultwarden already live on hart-server. hart-router supplies network/DNS infrastructure.

## Paths and serving state

| Purpose | Desktop | hart-server |
| --- | --- | --- |
| Source | `E:\Repositories\Laplace` | `/repos/src` |
| Builds | `D:\Libraries\build\Laplace` | `/repos/build` |
| Dependencies | `D:\Libraries` | `/repos/deps` plus installed toolchains/libraries |
| Input data | `E:\Data\Ingest` | `/vault/Data` |
| Work/logs | `E:\Data\Laplace\work` | `/repos/work` |
| Machine declaration | `C:\ProgramData\Laplace\machine.env` | `/etc/laplace/machine.env` |
| Installed payload | Monorepo `E:\Data\Laplace\services\laplace-mono-api`; modular `E:\Data\Laplace\services\laplace` | Monorepo `/opt/laplace/app`; modular `/hosting/laplace/modular/current` |

These are these hosts' configured locations, not required mount names on other installations.
Source checkouts, configured build directories and installed releases serve different purposes.
The installed clients run from a normal home directory without mounting source/build trees.

| HTTP surface | Observed result |
| --- | --- |
| Desktop development `http://localhost:5187/health` | 200 |
| Desktop IIS `https://dev.hartonomous.com/health` | 200 |
| Server `http://hart-server:8080/health` | 200 |
| Staging `https://staging.hartonomous.com/health` | 200 |
| Production `https://api.hartonomous.com/health` | 200 |

The October 12 desktop source build at `d3cb42fb4` passed native, managed and web builds,
published its configured ReadyToRun CLI, executed CLI help/native decomposition without
developer environment variables, and passed 23 native/runtime tests. The source API started
at localhost:5187 with that revision. This development build does not replace the installed
IIS release. On October 13 the corrected Windows database/launcher source reached
local main; a fresh desktop build passed all 23 selected native/runtime tests and
the running source API passed authenticated SQL/native checks against HART-DESKTOP.
The installed IIS release observed at 11:33 UTC is `a9385bedcab51` and independently
uses the local SSPI roles. See `operator-database-access.md` for current verification.
Production's installed source revision is `d3cb42fb4`; API and nginx are active.
The server modular package selects Engine `64f6184`, Native `8022bbd`, MCP `4299eec`
and Operations `59ba23e`. Use `--where` for the current resolved installation after upgrades.

OpenBao's desktop agents now run 2.7.1 with renewal permission; independent workload
credentials do not require a human login to renew. Request limiting and audit rotation are
installed on hart-server. The closed flood log and abandoned partial archive were deleted:
the verified cleanup receipt is `/repos/work/logs/secrets-protection/20261012T192725Z-b5d536be.json`.
`/var` has 82 GiB free (32% used) at that observation. These are incident/installation results,
not evidence that every Laplace feature works.

## What remains unfinished

The [acceptance register](https://github.com/SaltyPatron/Laplace-Operations/blob/66b925e19c2936f36813563f1b56147ff317c888/acceptance/criteria.json) and
[open parent issue](https://github.com/SaltyPatron/Laplace-Operations/issues/2) already require:

- CONFIG-001: consistent selection of named installation, paths and identities.
- INSTALL-001: a complete usable installed runtime and repair/upgrade process.
- RELEASE-001: compatible executable, native libraries, schemas and prepared artifacts.
- INGEST-001: explicit release/substrate selection and usable ingestion of real input.
- NETWORK-001: correct deployed origins, routing, TLS and authentication.

Installed CLI location, native closure and database selection have been checked on desktop
and server. Refactor installation, modular higher-environment delivery, remaining build-path
assumptions and end-to-end feature failures still require implementation and live verification.
The parent issue remains open across all three implementations.
