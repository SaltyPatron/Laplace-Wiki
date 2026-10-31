# Laplace system audit — 2026-10-10

This is an ongoing infrastructure and deployment audit. The user explicitly clarified that the coding agent is not being asked to prove the invention. Findings below are evidence, not a replacement specification or a claim that the whole system has been audited.

## Latest operational observations — approximately 18:50 UTC

- Operations #64 merged at `d6286e3` after hosted CI 38076782084 passed. Push run 38076898323 passed staging deployment, readback and required reads; ingestion and production were skipped. Stack maintenance now lives under `secrets/`. Local root installation of the updated secrets backup script has not yet been verified.
- Operations #65 merged at `42b5e8e` after CI 38077156900 passed. Candidate source bundle `aac8d85` was deployed on hart-prod: `setup.sh secrets-client` authenticated the Bao appdb password against PostgreSQL, refreshed four existing consumers, and installed a 15-minute refresh timer. The systemd refresh returned status 0. A fresh `psql` connection as the runner using its password file returned `laplace|laplace-app`; its credential file is runner-owned mode600. Canonical password and AppRole files are root-owned mode600. API health is HTTP200, service active, NRestarts=0. This does not migrate knowledge DB credentials or shared OAuth/payment secrets.
- Authenticated Bao inventory confirms roles `hart-desktop`, `hart-laptop`, `hart-prod`, `hart-server`; no `hart-cloud` role returned. The `host-` prefix belongs to policies, not role names. A real Raft snapshot was downloaded into protected build scratch; both archive payload checksums passed. Decryption and restored service were not tested.
- Cloudflare API confirms unproxied `openbao` and `vault` CNAMEs to `hart-server.hartonomous.com`, whose A record is `192.168.1.2`. Proxied `api` and `mcp` records target the production tunnel; both ingress rules target hart-prod port8080. No Cloudflare configuration was changed. Certificate renewal remains unverified.
- Public API `/health` returns JSON200. Public MCP GET `/` and `/mcp` return HTML200; MCP initialize POST `/mcp` returns405. Live hart-prod nginx only proxies `/` to the API on5187; it does not have the current source template's MCP route. The host setup intentionally omits local MCP when the knowledge DB is remote. This is an unresolved deployment/route defect, not a healthy MCP endpoint.
- VM query: hart-cloud TERMINATED; hart-prod RUNNING. Actual billing spend/trial balance remain unknown. No cloud VM was started for these checks.
- The user repaired `/etc/laplace` mode755 on hart-server; its `machine.env` is absent, not an unreadable unknown override. Setup permission repair merged in Operations #63 and Laplace #1770.
- Archive inventory: 3144 session-shaped JSONL files, 2,236,510,861 bytes, 823,838 records, 457,633 user/assistant events, 141 duplicate-file groups, 33,737 exact duplicate message events, five parse errors and no read errors. Parsed timestamps span December 29, 2025 through October 9, 2026 for this candidate set. This is structural inventory, not semantic review or complete nineteen-month coverage. Protected details remain outside Git.

Earlier observations below retain their original context; the dated updates above and below supersede their unresolved status where explicitly stated.

## Scope and authority

The active acceptance criteria are operational: correct dependencies and sequence, prepared artifacts, migrations before service activation, installed-version evidence, failure propagation, recovery and declared host roles. Design documents constrain these changes; research or semantic benchmarks are not substitutes for deployment acceptance.

The user's objective is to recover a professional, dependable development environment and make progress on Laplace as a whole. Pipeline changes, cloud setup, documentation, research, implementation, and agent-history reconstruction belong to that same task. Subsequent corrections refine this scope; they do not discard earlier work.

The user identifies the Laplace monorepo as the furthest implementation. Laplace-Refactor was an attempt at a properly engineered implementation. The modular repositories were intended to enforce reuse, generics, organization and coding standards. Repository existence, agent-written descriptions, and green checks do not establish that these aims were achieved.

Evidence order: current direct instructions; original user messages and invention documents; research artifacts with their stated experimental limits; implementation and runtime observations. Agent explanations and commit messages establish what was claimed or attempted, not what the user intended. Wiki reference pages describing existing code are not automatically design authority.

Code search is unavailable: the user states the embedding service was disabled or broken. Direct repository and transcript searches are being used. No attempt to restore embeddings is authorized by that observation alone.

## Machines and operating purpose

| Machine | User-declared role | Relevant constraint |
| --- | --- | --- |
| hart-laptop | Ubuntu local development | Verify tooling and deployment portability against its actual configuration. |
| hart-desktop | Windows local development | RTX 4060 Ti; Windows behavior requires Windows evidence. |
| hart-server | Ubuntu Server development, integration and deployment staging | GTX 1080 Ti has broken cooling and is off limits. |
| hart-router | OpenWrt router | Network infrastructure, not another development host. |
| hart-cloud | On-demand AVX-512 development, proof and benchmarking; existing delivery also assigns a knowledge/build role | The user explicitly says it is stopped by design to conserve the 90-day Google Cloud trial. Do not infer failure from `TERMINATED` or start it as an audit step. |
| hart-prod | Production hosting surface | VM running does not establish application health. |

## Windows workspace and lifecycle observations

The desktop session inspected the machine and fetched repository refs on October 10. Fetching did not update the
operator's working branches. Both D: and E: are approximately 2 TB NTFS volumes labelled EVO 990; D: has approximately
8.6 GB used and E: approximately 1.4 GB used. Capacity is not the demonstrated cause of the current fragmentation.

| Observed boundary | Evidence | Consequence |
| --- | --- | --- |
| Machine declaration governs only some entry points | Operations `laplace.env.ps1` reads `%ProgramData%\Laplace\machine.env`; that file puts repositories/work/ingest/PGDATA on E: and WAL on D: | Changing those paths does not reconfigure consumers that do not read this declaration. |
| Monorepo Windows configuration independently chooses another installation | Laplace `5abe41bbe`, `scripts/win/env.cmd`, defaults builds and dependencies beneath `D:\Data\Laplace`, PGDATA to `D:\Data\Postgres`, ingest to `D:\Data\Ingest`, and repositories to `D:\Repositories` | The modular and monorepo entry points can select different installations, inputs and database identities on the same machine. |
| IDE/MSBuild has a third route into the output tree | Same revision, `app/Directory.Build.props` and `Directory.Build.targets`, default directly to `D:\Data\Laplace` | Opening the solution does not establish that it shares Operations' declared build paths; separate worktrees can share these defaults. |
| One environment variable has different identity meanings | Operations uses `LAPLACE_PGUSER` for the Windows PostgreSQL service account; monorepo `env.cmd` uses it as the database login, defaults `PGPASSWORD=postgres`, and constructs `LAPLACE_DB` | Simply sourcing both environments is unsafe. The shared configuration must distinguish OS identity, database identity and credentials. |
| The local operational checkout is not remote main | `E:\Repositories\Laplace\Laplace-Operations` is at `8b00424` on `windows-devshell`, with modified `laplace.env.ps1` and untracked `build.ps1`; two additional Operations worktrees are present | The untracked build script exists in this old checkout, while current remote main already tracks a different build implementation. Preserve operator changes and reconcile revisions before choosing an authoritative entry point. |
| Build graphs and deployment graphs differ | Native is compiled into postgres/Engine/MCP; MCP also compiles Engine reader sources. Operations builds postgres and Engine. The monorepo builds its own native modules, extensions, .NET endpoints and SPA | A single product release cannot be inferred from independently successful repository builds. Record the complete dependency revisions, prepared artifacts and the consumers actually deployed. |
| Public delivery currently depends on the optional cloud host | Monorepo `5abe41bbe`, `.github/workflows/laplace.yml`, progresses from hart-server through starting/building on hart-cloud to publishing on hart-prod | An intentional cloud-off operating arrangement is not represented by selecting another compatible knowledge target alone. The release-building and runtime-host decisions also need explicit configuration. |

The user explicitly rejected treating this as drive-letter cleanup. The required correction covers source ownership,
worktree/build isolation, dependency sequencing, prepared artifacts, ingestion, runtime releases, credentials and CI/CD
as one lifecycle. A proposed directory tree or an added launcher alone does not establish that these consumers agree.
The monorepo and modular schemas must not be silently treated as interchangeable during that correction.

Supporting desktop repairs are separately evidenced: explicit LAN share names and Tailscale DNS were applied; direct
Tailscale transport to hart-prod was observed after the UDP firewall correction; a repository copy of 4,947 files was
verified by destination SHA-256. These checks do not establish full product delivery or database recovery. The desktop
backup task currently references the separate Operations repair checkout under the operator's C: profile; that live
dependency must be accounted for when consolidating the workspace.

The desktop session's proposed additional OpenBao agent/policy files were never deployed and were removed after the
existing secrets integration landed on Operations main. Existing OpenBao and Vaultwarden placement remains unchanged.

## Expanded installation, delivery and resource audit

Execution is now tracked in [acceptance/criteria.json](https://github.com/SaltyPatron/Laplace-Operations/blob/66b925e19c2936f36813563f1b56147ff317c888/acceptance/criteria.json) and
[Operations issue #2](https://github.com/SaltyPatron/Laplace-Operations/issues/2). The
[acceptance runner](../acceptance/README.md) records named commands, source revision, host, timestamps and outcomes.
The whole-system criteria are not completed by this document. CI produces scoped component receipts; missing checks
remain incomplete. RESOURCE-REFUSAL-001 adds an executable failure boundary: the known overcommitted desktop plan was
accepted by both old apply implementations, and is now rejected before database access on both platforms. This does not
establish a full host budget or reconcile the desktop's old resident-memory declaration.

This addition inspects Operations main `75fd1de`, Laplace main `58cab06ee`, Native main `1b9367c`,
the desktop, hart-server, hart-prod, and GitHub's registered runners on October 10. Older observations elsewhere
in this running record are historical evidence, not assertions that later repairs never happened. No cloud instance
was started for this audit. No live PostgreSQL tuning was applied. The two storage-detector repairs below are code
changes in the desktop repair branch; the server's installed Operations checkout is still separate.

The central defect is **incomplete ownership of an installation across its lifecycle**. There is substantial implementation,
including CPU topology, prepared database operations, pinned dependencies, host locks and deployment receipts. Calling
everything fake would conceal those assets. However, independently sophisticated pieces do not establish one reproducible,
operable product. A person currently supplies missing configuration, ordering, compatibility and recovery decisions from memory.

### YAML and the human operating model

| Finding and current evidence | Human or deployment consequence | Required correction |
| --- | --- | --- |
| **Environment names disagree.** Operations `laplace.yml` describes its production target as hart-cloud; its production runner actually is `hart-cloud-Laplace-Operations`, currently offline. Monorepo delivery calls hart-cloud `knowledge` and hart-prod `production`; GitHub's registrations agree with that second vocabulary. | A person cannot safely interpret “production” across repositories. Operations' ingest workflow requests `[self-hosted, laplace, Laplace-Operations]` without a tier; either eligible host can run it when online. | Separate deployment tier, machine, installed role and knowledge target. Resolve all four before an operation starts and include them in its receipt. |
| **Dispatch reports one revision but consumes moving dependencies.** Native sends its tested SHA; Operations staging checks out all three dependency repositories at `main`. | A later merge can enter the staging combination even though it was not the revision named in the dispatch. The trigger is a notification, not a dependency lock. | Resolve one release manifest containing every repository SHA and build contract; test that resolved combination. Recent production SHA pinning is a real repair, but does not turn the original trigger into a pin. |
| **Ingest depends on previous runner state.** Operations `ingest.yml` checks out only Operations and relies on dependencies/build outputs left in the runner workspace. Its comments claim no code is checked out, but the workflow does perform a checkout. | A replaced runner or a manually selected Operations branch can combine new scripts with old binaries and recipes. Retrying is not demonstrably retrying the same installation. | Run ingestion against an explicit installed release and knowledge target; record source selection and checkpoints separately. A deployment must not implicitly ingest or erase knowledge. |
| **The maintenance front door still uses a retired installation.** `product-operator.yml` invokes `product-stage.yml`; `full-qualification.yml` explicitly disables scheduling because this chain assumes a decommissioned layout. The forward-chat job still names `/build/laplace/work`, `laplace_admin`, and database `laplace`. | The obvious “verify”, “deploy” and “qualification” controls do not operate on the same installation as normal delivery. This is a direct DX failure, not merely too many YAML files. | Port maintenance onto the same installation engine and target resolver before presenting it as the ordinary control surface. Keep product-specific seed/proof operations as named operations behind it. |
| **Concurrency is only partly modeled.** Operations and monorepo use different GitHub groups. Recent host locks now share `/run/lock/laplace/host-resource.lock`; the legacy proof workflow locks `/build/laplace/work/host-resource.lock`. | Repository queues do not coordinate shared host resources. Some modern paths correctly refuse a collision, while legacy paths participate in another lock namespace. “Queued” and “refused” are also different retry experiences. | One resolved host/resource lock contract used by every installation/ingest entry point, plus deliberate queue/supersession policy. Preserve the existing host-lock repair. |
| **`cancel-in-progress: false` is not a durable operation queue.** The reviewed workflows do not specify the newer `queue` option. | A later request can replace a pending manual ingest or deployment. Comments promising all operations simply queue are stronger than the platform behavior. | Choose which builds may be superseded; operations with distinct inputs need durable queuing and visible disposition. Do not blindly queue every obsolete build. |
| **Cloud-on-demand is not consistently part of the operation contract.** Monorepo delivery starts and leases hart-cloud. Native's unconditional AVX-512 job targets its offline runner without that mechanism; Native's deploy job depends on `native`, not `isa`. | A run can have ordinary build evidence and a queued ISA check while staging delivery proceeds. The UI does not clearly distinguish baseline acceptance from paid AVX-512 qualification. | Declare required evidence by target CPU and operation. Share the cloud lease mechanism where AVX-512 evidence is requested; preserve intentional offline operation. |
| **Green delivery proves less than the product promise.** Current `site.sh` verifies application/web revision receipts and some endpoint status codes, but explicitly reports `/health/ready` without requiring it. Its build phase uses `BUILD_TESTING=OFF`. | Installed files and an answering web process can pass while the selected substrate is unreachable. Separate CI may provide tests, but this chain alone does not prove qualification or useful service. | Distinguish installation acceptance from serving acceptance. Promotion of a serving role needs authenticated representative work against the selected compatible knowledge target, without requiring every optional corpus/capability to be seeded. |
| **Public PR builds and installed infrastructure share a trust boundary.** Native runs `pull_request` jobs on the persistent staging runner and checks out private Operations using a repository secret. Operations runtime/deployment also uses a superuser database role. | Restricted fork tokens alone do not isolate the runner's filesystem, reachable services or resident credentials. No compromise is alleged; the configured execution boundary is the finding. | Isolate untrusted build execution from privileged installation credentials and long-lived service state; give trusted promotion a separate identity. This is the user's RBAC concern expressed operationally. |

GitHub documents concurrency groups within a repository and the default replacement of a pending run; current documentation
also provides `queue: max`. This does not replace a cross-repository host lock or an application operation journal.
[GitHub concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency).
GitHub also explicitly describes the risks of persistent self-hosted runners handling untrusted contributions.
[GitHub runner security](https://docs.github.com/en/actions/concepts/security/compromised-runners).

The monorepo's 19 workflows are not inherently excessive. The defect is that a human must know which generation of
deployment they belong to, what runner state they inherit, which database they select, and which green result proves what.
Consolidating filenames without consolidating those contracts would repeat the superficial drive-letter cleanup.

### Paths, installation and repair

The existing `%ProgramData%\Laplace\machine.env` is a useful starting point. It currently directs repositories, ingest,
work and PGDATA to E:, and WAL to D:. It does not govern monorepo `scripts/win/env.cmd` or every MSBuild default. Those
still describe another D: installation. `LAPLACE_PGUSER` means the OS service account in Operations and a database login in
the monorepo. At **current** Laplace `58cab06ee`, `scripts/win/env.cmd` still supplies `PGPASSWORD=postgres` when absent;
the recent administrator-credential preservation fixes in setup scripts did not remove this other default. Defaults and
credentials must not be conflated when bridging these scripts.

Other concrete lifecycle gaps:

- Native presets and Windows Operations builds use a repository/preset output path without a worktree identity. Monorepo
  MSBuild outputs similarly share a default root. Opening a second worktree does not establish build isolation. Build
  roots need a stable workspace identity plus configuration/toolchain identity; installed releases need their own identity.
  CMake provides preset `binaryDir`, environment expansion and local user presets for this purpose.
  [CMake presets](https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html).
- Windows `build.ps1 install` assumes drive-letter staging through `DESTDIR`; CMake documents that mechanism as unsuitable
  for Windows drive-letter prefixes. Treat that path as requiring a real Windows installation test or a supported staging
  mechanism, not as validated by a successful compile. This audit did not execute extension installation.
  [CMake DESTDIR](https://cmake.org/cmake/help/latest/envvar/DESTDIR.html).
- Linux `site.sh` stages native files but activates them file by file, then mirrors application/perf-cache directories.
  Windows `deploy-api.cmd` stops IIS, mirrors with `robocopy /MIR`, and restarts the pool even on its failure path.
  These checks have value, but neither file mirroring nor individual renames make the **whole release** atomic. No complete
  previous-release restoration was demonstrated for a partial publication or incompatible database migration.
- Source/dependency acquisition, builds, prepared artifacts, persistent knowledge, installed binaries, secrets and logs
  have different lifetimes. A clean-build command must not own the latter five indiscriminately. A product uninstall
  must remove owned services/binaries without silently removing databases, corpora, shared dependencies or credentials.
- Existing secret setup now preserves OpenBao/Vaultwarden data and supports an independent backup-maintenance action.
  Those are correct lifecycle distinctions to extend, not reasons to replace or move the established services.

The InstallShield/WiX analogy is appropriate at the **installation lifecycle** level. WiX Burn separates detection,
planning and application, and can plan installation, repair and removal. Windows Installer provides rollback mechanics;
custom actions still need deliberate recovery behavior. A new GUI or an MSI around today's scripts would not create those
semantics automatically. [WiX bootstrapper lifecycle](https://docs.firegiant.com/wix3/bundle/ba/bootstrapper_application_interface/),
[Windows Installer rollback](https://learn.microsoft.com/en-us/windows/win32/msi/rollback-installation).

### Actual resource configuration and competing planners

| Machine / evidence | Observed configuration | Interpretation |
| --- | --- | --- |
| HART-DESKTOP, live inspection and `tune-pg.ps1 -Plan` | i9-14900KS, 24 physical/32 logical processors; about 47.72 GiB visible RAM. Planner reserves 34 GiB, caps shared buffers at 1 GiB, chooses 195 connections, 24 parallel workers and 12 autovacuum workers; reports roughly 435 MiB overcommit under its own arithmetic. No matching llama-server or Laplace PostgreSQL Windows service was found. | An October 5 workload measurement became a general default. Its current applicability is unproved. Operations counts all physical cores while the monorepo also has P/E-core-aware policies. This was a plan, not an installed PostgreSQL configuration. |
| hart-server, live PostgreSQL settings | 6 physical/12 logical cores; about 125.7 GiB RAM. Shared buffers about 31.42 GiB; work_mem 158 MiB; maintenance about 3.93 GiB; autovacuum about 1.31 GiB per worker, 3 workers; 70 connections; 6 parallel workers, 3 per gather; `huge_pages=try` but status `off`; WAL target 32 GiB, `wal_level=minimal`. | Hardware-sized settings exist. They do not demonstrate a safe aggregate budget or optimal throughput. About 2.26 GiB swap was in use at the snapshot; that alone does not establish current memory pressure. |
| hart-prod, live PostgreSQL 18 app cluster on port 5432 | `/data/postgresql/app`, database `laplace-app`; 2 vCPUs, about 3.82 GiB RAM. Shared buffers 128 MiB, work_mem 4 MiB, maintenance 64 MiB, 100 connections, 8 parallel workers, WAL target 1 GiB, `wal_level=replica`, archiving off. | These are not the Operations-generated app-profile values (fixture proposes 22 connections). The installation's declared tuning and live tuning have not converged. Defaults are not automatically wrong, and higher values are not automatically better. |
| hart-cloud | GCP reports c3-standard-8, `TERMINATED`; Operations' stored fixture models 8 threads/4 cores and roughly 32 GiB RAM. | Intentionally offline. Fixture values are not fresh live tuning evidence. CPU qualification and benchmarking should explicitly acquire/release this resource. |

Operations `tune-pg.sh`, Operations `tune-pg.ps1`, monorepo `scripts/pg-machine-tuning.sh`, and managed
`PostgresResourcePlan` are separately implemented planners. They disagree today: Operations derives serving connections
as four per logical thread for knowledge; managed code uses one per logical processor per serving datasource. Managed
ingest includes two fold-headroom owners absent from the older monorepo shell equation. Parallel-maintenance policies
and memory partitioning also differ. Statements that these are one identical equation are not established by their comments.

Specific remaining defects and limits:

1. **Arithmetic is presented as a memory guarantee.** The Operations private-budget check includes one work_mem and one
   temp_buffers allocation per modeled backend. A query can have several simultaneous memory-consuming plan nodes and
   parallel workers. The test proves that formula, not a bound on actual PostgreSQL memory. Effective cache size is a
   planner estimate, not another reservation. PostgreSQL documents both per-operation memory and the distinction between
   requested and actual huge-page use. [PostgreSQL resource settings](https://www.postgresql.org/docs/18/runtime-config-resource.html).
2. **The client and server do not necessarily share hardware.** `PostgresResourcePlan.Current` uses the calling process's
   machine. That may be the desktop or hart-prod while its DB is hart-server. Server tuning must use server limits;
   a client's pool must respect its allocation from that server's connection budget. This is especially important for the
   user's intended remote native-client arrangement.
3. **A pool limit is not a host-wide limit.** `SubstrateClient` creates two serving datasources; admin services create
   serving and ingest datasources; application/billing code has a separate datasource. Their actual activation depends on
   enabled services, but each can own a pool. API, MCP, CLI, ingestion, deployment and operator connections must be summed
   by target cluster and identity. Npgsql documents the datasource/pool relationship.
   [Npgsql datasources](https://www.npgsql.org/doc/basic-usage.html).
4. **Detected capacity is not assigned capacity.** Managed `MemoryTopology` normally uses physical RAM; its GC/container
   limit is only a fallback. The monorepo shell reads MemTotal. Operations has a cgroup memory check, but its core count
   reads system topology and can raise a smaller detected thread count back to the physical-core count. Linux service
   snapshots showed no MemoryMax or CPUQuota bounds on API/MCP/PG; this is not proof that all services fit simultaneously.
   cgroup memory ceilings and CPU quotas are distinct from installed hardware.
   [Linux cgroup resource controls](https://docs.kernel.org/admin-guide/cgroup-v2.html).
5. **Every layer can claim the same cores.** CMake/Ninja jobs, test workers, native/OpenMP/MKL/TBB work, managed work and
   PostgreSQL parallelism need operation-specific budgets. A set of individually reasonable thread counts can multiply
   under nested work or concurrent services. Intel documents coordinating threading runtimes and nested parallelism.
   [Intel oneMKL threading](https://www.intel.com/content/www/us/en/docs/onemkl/developer-guide-linux/2023-1/improving-performance-with-threading.html).
6. **Recovery policy must precede WAL tuning.** Both Operations tuning profiles currently declare minimal WAL and zero
   senders, including the app profile. That can be intentional for reconstructible knowledge, but accounts and billing
   need an explicitly chosen recovery point. Minimal WAL cannot support PITR/streaming recovery; logical dumps still
   provide their own recovery point. The live prod app cluster currently uses replica WAL, not that declaration.
   [PostgreSQL WAL modes](https://www.postgresql.org/docs/18/runtime-config-wal.html).
7. **Deployment-triggered retuning is service maintenance.** `deploy.sh` invokes tuning; pending changes may request a PG
   restart. Ingest locks protect one class of activity, but a serving workload also has availability requirements. An
   installation plan must disclose reload/restart effects and verify current sessions/maintenance policy before activation.

The actionable storage defects reproduced and repaired in this branch are narrower:

- Linux `mount_of` overwrote its requested path with mount-table fields, then returned the chosen device paired with the
  final row's unrelated mountpoint. On hart-server it returned root device `253:8` and a Docker namespace path for both
  data and WAL. Corrected code returns `253:2 /data/pgdata` and `253:3 /data/pgdata/pg_wal`; actual WAL volume is 64 GiB.
  It was evaluated against the live mount table from a temporary audit copy, without applying settings.
- Windows inferred a dedicated WAL volume solely from different drive letters. With the real E:/D: declaration it
  proposed **953856 MB** max_wal_size on the shared D: drive. It now defaults to shared storage, producing **32768 MB**
  under the existing sizing policy. A dedicated separate drive requires `LAPLACE_PG_WAL_DEDICATED=1`; same-drive or invalid
  declarations are rejected. This is a corrected input classification, not a claim that 32 GiB is the optimal target.
- New tests exercise nested mounts, path boundaries, escaped spaces, unrelated later mounts, real Windows path parsing,
  separate-but-shared drives and explicit dedication. Earlier arithmetic fixtures supplied the storage facts, so they
  could not detect these failures. Both detector tests and the existing plan fixtures pass locally and are added to CI.

### Networking, identities, knowledge selection and continuity

The topology is an integrated system: router/DNS -> LAN and Tailscale reachability -> TLS and service identity ->
configured database and installed native/schema compatibility -> API/MCP operation -> public Cloudflare ingress.
OpenBao and Vaultwarden already live on hart-server. Their existence is not the missing architecture; the missing
contract is which human/workload/deployment identity may retrieve which credentials, for which service and environment,
and how enrollment, refresh, revocation and recovery work. The appdb-sync work is a useful existing part of that contract.

Current evidence still requires these distinctions:

- Tailscale provides a route; it does not supply PostgreSQL grants, HBA authorization, TLS hostname validation or schema
  compatibility. The earlier narrow hart-prod HBA repair proved a connection boundary, not a completed target switch.
- hart-prod's machine declaration still points knowledge to `100.103.255.122` (hart-cloud). Its API service was active,
  but `/health/ready` timed out after eight seconds while cloud remained intentionally stopped. The hosting surface and
  durable local app database therefore do not yet establish usable cloud-off operation.
- Selecting the compatible hart-server knowledge substrate should be explicit configuration, analogous to selecting
  the intended knowledge/model. Record schema/extension ABI, prepared-artifact identity and admitted source state; do
  not invent a replica-freshness requirement for two intentionally different knowledge substrates. This exercise does
  not by itself prove restoration or consistency of accounts, sessions and billing.
- Direct Tailscale transport, public tunnel health, private DNS resolution, certificate validity and application readiness
  are separate observations. Prior checks found a working wildcard certificate; ownership of its renewal/distribution
  still needs confirmation. No cert/acme system timer appeared in the server's unprivileged timer inventory; that does
  not rule out cron or another renewal host. Public MCP behavior also needs end-to-end verification through its tunnel.
- Repository copy verification, secrets restore checks, database backups and off-site continuity have different coverage.
  The earlier 4,947-file copy check did not back up a running PostgreSQL cluster or prove a production restore. The live
  desktop copy-off task also still depends on this repair checkout's path, which must be migrated deliberately.

For the user's network objective, measure **external client/DB round trips and bytes per useful operation**, including
connection establishment, result payloads, retries and cold/warm prepared-artifact behavior. The code already uses batching
and prepared operations in places; Npgsql documents batching specifically to reduce round trips.
[Npgsql performance](https://www.npgsql.org/doc/performance.html).
SQL statements executed internally through PostgreSQL SPI are not each a network round trip. Likewise, client-side CPU
work alone does not establish low wire volume, and more connections do not remove a serial chain of dependent requests.
No new wire benchmark was run in this audit, so low network usage remains an objective rather than a measured conclusion.

### Coherent installation contract and implementation sequence

This is a proposed repair direction grounded in the user's existing roles, not a new product specification:

| Responsibility | One declared contract should answer |
| --- | --- |
| Machine | OS, hardware facts, usable resource allocation, configured roots/volumes and which roles are installed. D:/E: describe this host, not every consumer's defaults. |
| Release | Exact source/dependency revisions, compiler/numerical contract, CPU baseline/dispatch variants, PostgreSQL ABI/schema compatibility, prepared artifacts and runtime dependency closure. |
| Environment | Tier, endpoint names, knowledge target, separate application database, configuration precedence, allowed identities, enabled capabilities and recovery objectives. |
| Installation engine | Detect -> validate/plan -> prepare -> install/migrate -> activate -> verify -> record; explicit repair/upgrade/remove semantics and recoverable failure boundaries. |
| Operation | Selected installed release, target knowledge identity, ingestion/proof/benchmark inputs, locks, resource budget, checkpoint/resume state and measurable acceptance. |
| Front ends | Local shell, IDE and GitHub Actions invoke the same operations and show the same resolved plan. YAML schedules and transports work rather than defining a second installation. |

Implement in dependency order:

1. Reconcile the non-secret machine schema and variable meanings, preserve current paths/user changes, and make every
   entry point print where its resolved values came from. Inventory installed state before moving files.
2. Separate isolated source/build workspaces from versioned runtime releases and persistent data. Package one compatible
   release closure; install the same closure locally and through CI, with platform-specific service adapters.
3. Make ordinary delivery and maintenance share the installer. Retire incompatible controls only after their useful
   operations have been ported; replace runner-leftover assumptions with release receipts.
4. Reconcile resource plans and service identities across the whole host. Verify PG settings, pools, native dispatch and
   actual resource use on desktop/server/prod; reserve cloud AVX-512 evidence for explicit cloud operations.
5. Complete the configured hart-server knowledge selection on prod while cloud stays off, then exercise authenticated
   API/MCP work and record wire cost. Separately rehearse release rollback, application-data restore, secret recovery and
   certificate renewal. These are different forms of continuity and need distinct evidence.

Completion means a human can configure a host once, install a named compatible release, choose a knowledge target, run
or resume an operation, see what is actually running, and recover a failed change without reconstructing the system from
chat history. The storage fixes improve that path; they do not complete this lifecycle consolidation.

## Documentation, research and implementation map

| Source | What has been located | What it can establish |
| --- | --- | --- |
| Laplace | `docs/INVENTION.md`, `INVENTIONS.md`, `INVENTOR_RECORD.md`, binding specs, `engine/manifest/` | Invention laws, recorded direct corrections, and existing implementation; distinguish them. |
| Laplace-Wiki | `Semantics/Claims.md`, `Sequence/Perfcaches.md`, `Reference/Types.md`, `Sequence/Conflicts.md`, research pages | Cross-repository explanations and known conflicts. The pages disagree in places; selecting one silently is not reconciliation. |
| Laplace-Refactor | `contracts/authority-stack.json`, `docs/audits/DIRECT_REQUIREMENT_EVIDENCE.md`, `requirements/product.yaml` | Locators for original requirements and explicit separation of product law, executable contracts and observed state. They do not prove the implementation satisfies those contracts. |
| Laplace-Research | Semantics, relations, learning, numerics, placement, hashing, corpus-search, recipes and prior-art work | Experimental and literature evidence. Recorded results must retain their datasets, conditions and limitations. |
| Laplace-Prototype | Storage, semantics, translation/WSD, chess, code and recipe experiments | Prior behavior and counterexamples; not proof that the modular product retained those capabilities. |
| Laplace-Native / Laplace-postgres / Laplace-Engine | Shared native code, PostgreSQL integration and executable behavior | Current call paths and storage behavior; not authority for interpreting the invention. |
| Laplace-Operations / Laplace-MCP | Deployment, checks, services and public access | Whether the intended operations actually reach a compatible installed system. |
| Other discovered roots | Laplace-Conventional, Laplace-Patreon, Laplace-Scratch, two Laplace_Hartonomous-Old roots | Present in the inventory; review and linkage remain unfinished. |

## Highway: evidence and causal history

The original Claude conversation on October 3 is preserved in local session `8200b5a3-c852-4c36-9a97-634eaad52cbd`. Its direct messages include:

- `2026-10-03T05:53:41.887Z`: the user explains POS/sense/dependency relations across sources, asking what each source says about an entity.
- `2026-10-03T05:54:14.403Z`, UUID `d441a4bd-250f-4b9e-a376-896bfc77797e`: the message names ILI, synsets, frames, POS, sense and dependency relations. The transcript also contains a duplicate event at this timestamp under UUID `8c21ba50-9704-48b0-94c8-b51cf20b394a`; these are not two independent requirements.
- `2026-10-03T07:51:45.245Z`, UUID `315b73b3-cb63-4c01-ae98-658df5ad3528`: pregenerated relations/types/kinds acting as perf-caches or flagged enums are permitted; arbitrary hardcoding and an English semantic pivot are not.

The surrounding assistant messages repeatedly reinterpret the highway first as type lists, then solely as a relation registry, then as category masks. These are documented interpretation changes, not user-approved architecture. The complete exchange must be used; quoting one of those assistant explanations as the requirement would repeat the error.

Related documentation makes distinctions that the audit must preserve:

- Wiki `Semantics/Claims.md` distinguishes flagged enum masks, identifiers without mask bits, and mappings between resources. It explicitly distinguishes relation types from POS/sense/dependency groups.
- Wiki `Reference/Types.md` describes the current type ROM and reports that only the kind bank is written; entity and occurrence carriers are not built. This is a documented implementation limit, pending fresh runtime verification.
- Refactor `requirements/product.yaml`, `LP-PERFCACHE-002`, specifies independent lifecycle and canonical parity. `LP-HIGHWAY-001` describes shared typed coordinates across languages, modalities and operations; it is broader than a POS bitmap.
- Research and Prototype include translation through witnessed ILI claims and WSD experiments. Their results distinguish standing, prevalence, POS filtering and context; a structural hash comparison alone does not establish those behaviors.

The deployment coupling has a traceable implementation history:

1. Engine commit `4b2a9f505623768339fa7c7abb75103c5bc64578` (October 1), titled as a keyed-parent repair, also added deployment of highway text contents into the database. Its code comment says the contents are needed for claims to render and pull through.
2. Engine commit `8eaa30d8350aca7747d9af7359acc04ae782f94f` (October 2) changed the sidecar from texts to compositions alongside a large decomposer change.
3. Current `src/table.c:highway_typed` returns an ID, coordinate and tier from the ROM; it does not itself construct the node's children in the ingest table. This helps explain why removing deployment's sidecar load alone may expose missing composition content. It does not justify that lifecycle.
4. Operations `deploy.sh` regenerates the highway unconditionally; Engine `cmd_deploy` reads `.nodes`, calls `load`, and calls `merge`.

Repair therefore needs to trace both source admission and consumers, preserve canonical composition and referential integrity, and provide an independently generated/installable artifact. Merely deleting the deploy call or renaming the artifact would not establish correctness. No highway implementation change has been made in this audit yet.

## Observed pipeline and verification defects

[Operations run 38069889646](https://github.com/SaltyPatron/Laplace-Operations/actions/runs/38069889646), triggered by the merge of PR #54, completed successfully on October 10.

| Observation | Evidence | Consequence |
| --- | --- | --- |
| Highway generation ran for 418.5 seconds | Runner `logs/deploy/20261010T165941Z/highway.log` | Routine deployment regenerated a persistent artifact. The comment describing this as taking seconds understates the observed cost. |
| Deploy loaded/merged highway content | Same directory, `deploy.log`: 155,362 types, 228,209 compositions, zero new entities | The separate ingest job was skipped, but deployment still executed a data-loading path. Zero new rows does not mean no load was attempted. |
| No other machine's matching record existed | `logs/verify/20261010T170700Z-build/compare.txt` | The green cross-machine check established no cross-machine comparison. |
| Local repeated decomposition matched | Same directory, `determinism.txt` | Evidence of local repeatability for two selected sources only. |
| Production checkout uses moving `main` references | `.github/workflows/laplace.yml`, production checkouts | Comments claiming the same tested revisions are not enforced by the workflow. Production was skipped in this run. |

The first implemented repair makes missing peer records and retrieval failure return exit 2 from the comparison command; mismatches remain exit 1. `verify.sh` reports incomplete evidence as incomplete, rather than as equality or a fabricated mismatch. The shell comparator also rejects a renamed local record and records for different commits. This is a bounded correction; it does not turn fingerprint comparison into deployment, integration or semantic acceptance.

## MCP and deployment ownership

Two different MCP services exist on hart-server:

- System `laplace-mcp.service`: `/usr/bin/dotnet /opt/laplace/app/mcp-runtime/Laplace.Endpoints.Mcp.dll --http`.
- User `laplace-mcp.service`: `/repos/src/Laplace-MCP/native/lpm serve 127.0.0.1 5188`.

On October 10, the native service's `tools/list` returned tools, but a `search` for `highway mask` returned `isError: true`: `physicality_t3_c` does not exist. The source had already been corrected in commit `e86961f` and merged at `d7fbc1d`; run `38019824734` built it successfully. The user service still ran an October 5 binary from the source directory. The failure was stale deployment, not an absent source fix. A successful MCP handshake is not evidence that repository search works.

An earlier probe received an empty reply and the user service restarted. Its journal reports database connections terminated by an administrator command, followed by process exit 1. That journal does not establish which operator caused the database event. A subsequent probe produced the missing-table error above.

At 17:22 UTC the native user service was repaired locally. The CI-built executable and library were installed with CMake's runtime-path relocation into `/home/ahart/.local/lib/laplace-mcp/d7fbc1d89035c1e51e59153f5ca3fa9561e7a6ab`; the user service has an `installed-runtime.conf` drop-in pointing there. The old binary was preserved. The system .NET service was not changed.

The installed pair uses Engine `7459129e79c894f2d4166b683feb4c7ee81301b0` and Native `1b9367c8055cdbd79beb1a8ba4c2d1aa322e4678`. The original install attempt copied and relocated the files but could not write the runner-owned install manifest; rerunning the generated install script with only its manifest destination redirected into the release completed successfully. The release contains `revisions.txt` and the install manifest.

Validation: `lpm check` passed; dynamic-library resolution uses the installed `liblpm.so`, not the runner copy. A candidate on port 5198 was checked before replacement and stopped afterward. The installed service on 5188 returned a successful search for `Sherlock Holmes`, with the expected ID, four containers and two claims; `highway mask` returned a valid response with no rows rather than a missing-table error. These checks demonstrate the repaired schema path only. They do not establish that repository documents are ingested, that search replaces code-search, or that the complete MCP/product contract works. Automatic delivery to this user service remains missing from CI.

## Other outstanding operational work

GPU scheduling correction: the Conventional runner `hart-server-Laplace-Conventional`
(GitHub runner 22) was online and idle but advertised `gpu`, `pascal`, and `1080ti`,
contrary to the user's damaged-GPU restriction. Removed those custom labels through
the GitHub runner API; retained its CPU-capable labels. The registration default now
omits GPU labels. No GPU probe or workload was executed. Registration defaults do
not overwrite an explicit machine override; root-owned machine configuration still
requires inspection where access is unavailable.

- Production API: earlier live inspection found `/etc/laplace` mode 700, an unreadable machine declaration for the runner, repeated restarts and no health response. The deployed revision receipt was absent. Configuration and artifact-delivery repair remains outstanding.
- Google: the working account is `thesaltypatron@gmail.com`, project `project-f5812b96-f924-41a4-94c`. Earlier audit records confirm the nightly stop at approximately 02:06 Central, a later start, and a later guest shutdown. Recheck VM state before operational decisions.
- Billing: project linkage and an open billing account were verified. Actual spend, credit remaining and expiry were not obtained; do not infer them from VM runtime or enabled billing.
- Azure: installation and cached tenant-only account were observed; usable subscription/resource access remains unverified.
- GitHub: authenticated access and PR #54 merge are verified. The tuning fixtures and focused PowerShell checks do not prove Windows execution or safe live tuning on every machine.
- Agent history: selected recent Claude exchanges and historical evidence indexes have been read. Full archive review, deduplication and correction chronology remain unfinished. No full-history audit claim is justified.

## Continuation

### Open pull requests reviewed

The October 10 inventory found three open draft PRs under SaltyPatron: Operations #57 and Engine #38/#44.

- Engine #38 is a superseded prototype. Its highway string fix has the same stable patch ID as main's `55861e9`; `src/provenance.c` and all `tools/containment-prototype` files at its head `602f56e` are byte-identical to main-history commit `99bced5`. Main subsequently merged containment work in #47 and extracted the shared walks in #52. Closing the old draft does not delete the branch or erase its recorded measurements. This does not certify the later implementation's semantic completeness.
- Engine #44 is genuinely unfinished: its own description reports incorrect sense selection, missing POS standings, recipe labels used as FrameNet strings, and 40–75-second turns. Its prerequisite #43 is merged. Passing its build does not resolve these functional defects; it must remain a tracked implementation task rather than be marked ready cosmetically.
- Operations #57's bounded verification correction has seven passing regression cases and a PowerShell parse check. Its broader audit records unfinished work; that does not make the tested correction itself unready. Land the correction without running the known defective automatic deployment chain, and continue the lifecycle repair separately within this same task.

Continue the same system-wide task after user corrections. Track fixes against their original requirement, affected consumers, actual checks and deployment state. Do not replace unfinished implementation with a completion statement, and do not require the user to re-list repositories or restart the work.

## Engineering and operations research — initial evidence, October 10

The user's request covers the whole engineering and operating system. Research must inform concrete corrections across requirements, repository boundaries, environments, builds, tests, artifact generation, ingestion, migrations, deployment, recovery, cloud lifecycle, costs, and continuity. A source list is not completion. External guidance does not define Laplace semantics or override the inventor's requirements. This section records preliminary findings; full-paper methodological review and implementation remain unfinished.

### Evidence and its limits

| Source | Evidence type and relevant finding | Limit |
| --- | --- | --- |
| [Soares et al., Effects of CI](https://arxiv.org/html/2103.05451v3) | Systematic review: 101 empirical studies selected from 479 candidates across six digital libraries; reports benefits and technical/process challenges. | Introduction, selected results/discussion and threats to validity inspected. It is an interpretive synthesis, not a meta-analysis; study definitions and contexts vary. Publication, selection and interpretation biases remain. This does not establish that any particular Laplace check is useful. |
| [Shahin, Babar and Zhu, CI/CD systematic review](https://arxiv.org/abs/1703.07019) | Review of 69 selected papers covering 2004–June 2016; identifies testing cost, transparency, design, domain and infrastructure as adoption factors. | Historical evidence, not current tool documentation or a universal pipeline prescription. Reviews may overlap in included studies; do not count them as independent experiments. |
| [NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) and [practice text](https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-218.pdf) | Published security-development recommendations; PS.3.1 addresses retaining release files and supporting integrity/provenance information. | Security framework, not evidence that compliance proves product correctness or a required certification for Laplace. |
| [Microsoft operational excellence](https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/principles) | Institutional guidance connects ownership, documented operations, observability, repeatable deployment and recovery; recommends infrastructure layers aligned with lifecycle. | Recommendations require adaptation to this initial setup and hardware. Multiple Microsoft pages are not independent empirical studies. |
| [GitLab deployment safety](https://docs.gitlab.com/ci/environments/deployment_safety/) | Documents serialization of deployments and prevention of outdated deployment jobs. | Establishes platform mechanisms and concrete failure modes; does not require migrating from GitHub. |
| [GitHub deployment environments](https://docs.github.com/en/actions/concepts/workflows-and-actions/deployment-environments) | Documents target-specific protections, secrets and deployment history. | An environment label does not provision isolation or establish service health. Approval features are optional mechanisms, not a reason to add user approval gates. |
| [DORA deployment automation](https://dora.dev/capabilities/deployment-automation/) | Guidance separates deployable packages, deployment scripts and environment configuration, and recommends exercising the deployment process before production. | One research programme; its multiple pages are not multiple independent authorities. |
| [Twelve-Factor build/release/run](https://12factor.net/build-release-run) | Practitioner methodology distinguishes executable construction, configuration and execution. | Useful separation of responsibilities; not a specification for Laplace's native engine or canonical data. |

### Application to the observed system

The following are engineering recommendations derived from the observed failures and user requirements, not claims that the sources prescribe Laplace's architecture.

| Area | Required investigation or correction | Evidence needed before calling it complete |
| --- | --- | --- |
| Requirements and history | Link behavior to original invention requirements and direct corrections; reconcile research and implementations across repositories. | Traceable requirement, implementation and counterexample records; explicit gaps in archive coverage. |
| Environments | Preserve laptop/desktop development, server staging and cloud production roles. Define credentials, configuration, service placement and database boundaries explicitly. Keep the server's damaged GPU off limits. | Installed state and deployment rehearsal on declared targets; Windows evidence for Windows claims. A host name alone proves nothing. |
| Build and release | Resolve all repository inputs to exact revisions; retain compatible artifacts and their dependencies. Promotion must identify the artifact tested. | Artifact digest, source revisions, toolchain/CPU target, deployment record and installed readback. Platform-specific binaries may differ; do not require one binary across incompatible targets. |
| Highway and ingestion | Implement the user's independent highway generation lifecycle while tracing consumers and canonical content dependencies. | Independent generation and installation; compatibility checks; explicit admission operations; tests showing ordinary deployment does not silently regenerate or ingest. |
| Tests | State each check's requirement, fixture, expected outcome and scope. Distinguish repeatability, portability, integration, deployment and semantic acceptance. | Actual assertions and failure cases. Missing peer evidence remains incomplete. Identical wrong results do not establish semantics. |
| Database changes | Assign each existing migration to its actual database and service; ship the exact scripts with the compatible release. | Migration history on the target, startup acceptance and recovery evidence. Reverting binaries alone does not reverse data changes. |
| Deployment workflow | Reuse deployment mechanics across staging and production; serialize changes to each target; prevent stale jobs overwriting newer releases. | Failure and retry behavior, exact deployed versions and endpoint checks. Audit locks across repositories as well as within a workflow. |
| Runtime and recovery | Verify API/MCP operations, restart behavior, dependencies, backups and restoration. Record manual repairs in the durable deployment mechanism. | Functional requests, observed errors, restore verification and bounded recovery behavior; process-active status is insufficient. |
| Cloud lifecycle and costs | Reconcile scheduled shutdown, job leases, starts and actual billing. Separate service availability expectations from build scheduling. | Timestamped cloud/guest events and billing observations. Current spend and trial balance remain unknown. |
| Agent continuity | Maintain one evidence-backed work record across corrections and interruptions. | Completed fixes, deployed state, failed checks and remaining work clearly separated; no invented completion or repeated requests to restate scope. |

These recommendations add neither a Kubernetes migration nor new approval bureaucracy. Choice of tooling, number of environments, rollout strategy and test cost must follow the actual workload. The immediate known defects remain the deployment/data coupling, incomplete release identity, missing service delivery and misleading verification already documented above.

### Applied finding: preserve the staging source revisions

The Operations workflow now records the three dependency commits after staging checkout and passes those job outputs into production checkout. A production preflight rejects missing or malformed commits rather than allowing checkout to fall back to a default branch. This resolves the independently moving dependency branches within a run. It does not promote an immutable binary: production still builds for its own CPU target, and generated resource versions and installed artifact digests require further work.

Local validation parsed the workflow YAML and executed its actual capture/preflight scripts against three temporary Git repositories. Valid commits passed; empty, branch-name, short and nonhex values failed. Advancing the Engine fixture branch and checking out the captured commit recovered the original staging revision. No production deployment was performed by this validation.

### Additional workflow coordination finding

Operations uses workflow group `hart-server-laplace` and deployment/ingestion file locks. The monorepo uses `laplace-site-hart-server`, `laplace-site-knowledge` and `laplace-site-hart-prod`; inspected `site.sh` uses the lock directory for restart triggers but has no corresponding deployment `flock`. Those mechanisms do not establish coordination between the repositories. This is a source-level finding, not an observed collision. Before introducing a common lock, trace shared binaries, PostgreSQL extension/schema changes and the full duration of ingestion so a partial lock does not leave the conflicting operation exposed.

The research does not support treating additional checks as automatic improvement. Soares et al. report contradictory findings for PR lifetime and confidence, with differences in how CI adoption is measured. For Laplace, evaluate checks by the defects they detect, their duration, and whether they verify the declared behavior. Microsoft's [deployment guidance](https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/safe-deployments) separately distinguishes contract compatibility from behavioral correctness and highlights the complexity of stateful rollback. These support evaluating the existing checks individually; they do not supply Laplace's semantic acceptance criteria.

## Follow-up — 2026-10-10 18:00 UTC and later

- Monorepo #1768 merged as `35a7bda40290cdf953e6ef58d881205b443dfa5d` after full CI policy run 38073878207 passed. Hidden receipts are retained, app/browser migrations are packaged and run before hosting publication, caches are staged before publication, unreadable declarations fail, and the cloud lease waits for hosting. Merged with `[skip ci]`; a full deployment is not claimed.
- The existing hart-prod API was repaired using its declared database configuration and nine existing application migrations, after retaining a database dump. `/health`, `/health/live`, `/openapi/v1.json` and `/v1/models` returned 200. Knowledge readiness timed out while hart-cloud was stopped. Installed source revision remains unknown.
- hart-prod has no system MCP unit. `site-host.sh` deliberately omits that unit on hosts using a remote knowledge database. Do not describe the absent unit as a crashed service or blindly install it. Public MCP routing and the knowledge-host endpoint still need verification.
- Engine #54 separates `.nodes` admission from deployment and adds a read-only highway fingerprint. Local clean icx build and six admission/artifact checks passed. Actual deployment into a newly created isolated database left zero entity rows with the real highway present; that test database was removed. The serving database was not loaded. PR CI and coordinated Operations rollout are tracked separately.
- Operations scripts now consume prepared artifacts. Six shell boundary cases passed, including missing artifacts before an explicit drop; seven existing comparison regressions passed. Fingerprints read installed artifacts instead of old generation logs. Generation input provenance is unknown until a receipt binds the artifact to its sources. Windows execution and automated artifact promotion remain unverified.

### Deployment gates and extension CI — 18:12 UTC follow-up

Engine #54 and Operations #60 are merged (bde37b9 and 92af13a), with no automatic deployment run. The original clean main checkouts of Engine, Operations and Laplace were fast-forwarded to the merged fixes; local source files no longer retain the older generation path or GPU runner defaults. This does not update installed services by itself.

Postgres #16 qualifies its candidate in a private package directory and temporary database instead of replacing shared extension files during PR checks. Local clean icx build, candidate-function module bindings, actual extension execution and cleanup passed; shared library/control/SQL hashes remained unchanged. GitHub run 38074637704 also passed. PostgreSQL 18's documented extension search paths support the isolated package selection.

Operations deployment checks now read extension version/tables and compare the Engine's existing tier-0/highway fingerprints with PostgreSQL's. They capture observed binary/artifact hashes without claiming missing provenance. Live readback on hart-server passed using the freshly built candidate Engine against extension 1.12; seven negative/positive boundary cases and three workflow cases (17 assertions) passed. Production depends on successful staging reads as well as deployment/readback. Cross-machine build qualification remains explicitly callable and still reports absent peers as incomplete; it is not the infrastructure gate. These changes do not validate invention semantics or replace pending full deployment/recovery rehearsal.

Linux Operations deployment and direct installation now hold an exclusive host-resource lock; ingestion holds it shared for its complete lifetime. The lock is never unlinked, and nested installs reuse descriptor 8. Background WAL samplers close their copy so they cannot retain the lock after ingestion ends. Four actual flock contention/lifetime cases passed. The monorepo site entry point is being updated to the same file/protocol with four passing contention cases. Legacy entry points and Windows host locking are not yet covered by this result.

### Completed staging rehearsal — 2026-10-10 18:19 UTC

Run [38075199422](https://github.com/SaltyPatron/Laplace-Operations/actions/runs/38075199422) deployed main `f639a786c5da1021cec5404008572d90ac7b4f2d` to hart-server with production/drop/reseed explicitly false. Deployment and infrastructure readback passed; ingestion and every production job were skipped. The deployment log contains `highway-fingerprint`, not generation or sidecar admission. Tier0/highway/layout/keys hashes match the pre-run readback.

The required CLI reads passed. The optional `fills` diagnostic spent 60 seconds and timed out; the old script explicitly ignored that result. It is being removed from ordinary deployment reads. This run is evidence of modular staging delivery and required command execution, not successful translation semantics (the translation output said no concept was attested for the sample), not full monorepo deployment and not production qualification.

At approximately 18:21 UTC, a fresh `laplace-app` dump on hart-prod restored into an isolated database with all 17 tables and nine migration journal records. The temporary database and protected dump were removed after verification. This checks local logical restoration, not off-host backup delivery or disaster recovery. The API remained active with NRestarts=0 and health 200; the backup timer was active with next run October 11 03:32 UTC.
