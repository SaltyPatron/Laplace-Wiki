# Laplace-Operations

`sudo ./setup.sh` owns shared infrastructure and the declared modular Laplace runtime.
It does not configure the monorepo API, MCP, browser identities or their credentials.
Run the monorepo's `sudo bash deploy/linux/site-host.sh` from its own checkout for those.
The explicit Operations `site` and `runtime` stages remain compatibility entry points;
they are not part of `all`. Refactor has its own installer in its own repository.

Start with the [installation map](docs/installation-map.md): repositories, environments, executable
locations and known broken entry points. It distinguishes observed installations from intended behavior.

For the current monorepo application's staging-to-production delivery and installed-runtime checks, use
[Operating Laplace](docs/operating-laplace.md). The commands below describe the active modular stack.

The modular MCP is a separate installed service: `laplace-modular-mcp.service`,
with its matching Engine packaged beside it. `sudo ./setup.sh` includes it when
`installation/<hostname>-modular.json` declares that host; `sudo ./setup.sh modular`
runs just that installation. `LAPLACE_MODULAR_MANIFEST` selects an alternate declaration.
The declaration owns its source/build/release/state paths, OS/database identities,
prepared artifacts, listener and resource allocation. Installation grants local peer
access to its selected database and retires the declared old user service only after
candidate verification. It does not ingest sources.

After installation, `python3 installation/modular.py deploy` builds, packages,
activates and verifies it without sudo. The Operations pipeline invokes the same
command with immutable MCP/Native/Engine revisions. Failed activation restores the
previous release and PostgreSQL's exact prior cache settings. PostgreSQL selects
the immutable release's `share/prepared` files; build inputs do not replace those
database bindings. Receipts include the selected paths and go to the declared
`receipts` directory. Inspect the
service with `systemctl status laplace-modular-mcp` and its logs with
`journalctl -u laplace-modular-mcp`. This service is distinct from the monorepo's
`laplace-mcp` and from Refactor; its acceptance does not establish either of those.

The Windows modular CLI is installed separately from `laplace-mono`:

```powershell
./setup.ps1 client -Installation ./installation/hart-desktop-modular-client.json
laplace --where
laplace status
laplace help ingest
```

This non-administrator installation uses the declaration's existing Engine build,
prepared artifacts, compiled grammars, data paths and database identity. It packages
native dependencies, recipes, firmware and artifacts into an immutable release under
the declared prefix, then verifies native composition and the selected database before
publishing the human command. No PostgreSQL instance is created. The command works from
any directory and reads its installed client profile; it does not need a developer shell.
When MCP is selected, Engine and MCP build in the declared MCP profile with one
Native dependency graph. The package selects that graph's Engine executable;
the standalone Engine tree is not rebuilt. Without MCP, the declared standalone
Engine profile remains the build owner.
On HART-DESKTOP, the profile is `E:/Data/Laplace/clients/laplace/client.json` and the command
is in the existing `%LOCALAPPDATA%/Laplace/bin` directory beside `laplace-mono`.
The Linux operator command is a small bootstrap into the selected release's
packaged client controller. It pins that release until the native process exits;
subsequent deployments update the client code with its matching binaries. Run the
normal client installer once to replace an older copied launcher.

`installation/build-grammars.ps1 -Source <grammar-source-directory> -Output <build-directory>`
builds selected Windows grammar sources, including C++ scanners, and fails on any compiler
error. `package-windows-client.py` resolves transitive DLL imports and also packages the
declared dynamically loaded [oneMKL CPU libraries](https://www.intel.com/content/www/us/en/docs/onemkl/developer-guide-windows/2024-2/using-the-single-dynamic-library.html).
The package manifest records file hashes, grammar names and Engine/Native revisions.

The machine Laplace runs on, and Laplace on it, from nothing: one environment file, four scripts, and the agents. The
code is in Laplace-Native, Laplace-postgres and Laplace-Engine, side by side under one source root; this repository
holds what installs, sets up, deploys, repairs and runs them (Operations in the Wiki).

The host deployment scripts explicitly call `laplace deploy --configure-server-cache`
to select the declared server-local cache paths. Ordinary `laplace deploy` from a
client preserves database configuration and upgrades the installed extension in
its own namespace; it does not adopt matching public tables. Index maintenance
uses the server's configured memory and touches only Native relations.

```sh
git clone https://github.com/SaltyPatron/Laplace-Operations /repos/src/Laplace-Operations
cd /repos/src/Laplace-Operations
sudo ./setup.sh           # host configuration plus declared runtime installation and verification
./deploy.sh               # build/install and database infrastructure; requires prepared perf-caches
./ingest.sh               # the sources, in recipes/order, into that database
# Runner setup is included in setup.sh; agents.sh is available for focused runner maintenance.
```

`laplace.env` is the one definition of where everything is; every script here and every build reads it, and every
value in it is `${VAR:-default}`, so another machine sets its own.

## From an empty server to loaded content

```sh
./deploy.sh                                        # the database laplace.env names
LAPLACE_CONNINFO="host=/tmp port=5432 user=laplace dbname=NAME" ./deploy.sh
```

`deploy.sh` requires existing tier 0, flags, highway, layout and keys before making changes, including before an explicit database drop. It tunes PostgreSQL, builds/installs code and missing grammars, reads the highway fingerprint, deploys extensions/schema/settings and reports status. It does not fetch datasets, generate perf-caches or admit content. `deploy.ps1` applies the same artifact boundary on Windows. Linux deployment and direct installation hold an exclusive host lock for their full duration; ingestion holds it shared, so it cannot start between a deployment lock probe and a schema/install change. CI sets `LAPLACE_HOST_LOCK_WAIT_SECONDS=wait` to queue until the real holder releases the lock; numeric values retain an explicit deadline, and ordinary commands default to zero for immediate refusal. The workflow's overall deployment timeout still applies. Per-database locks additionally serialize ingestion. The lock is `$LAPLACE_LOCKS/host-resource.lock`, with descriptor 8 inherited by nested installers. Monorepo site delivery uses the same protocol. Historical entry points and Windows host coordination remain to be reconciled.

Prepare or install perf-caches as an independent operation. The existing generators are `laplace tier0`, `laplace flags`, and `laplace highway -o /path/to/artifact/highway.bin`; they require their declared source data and, for highway generation, compiled grammars. Generate into a separate directory, retain the binary and its `.layout`, `.keys`, `.nodes` sidecars together, and select the installed artifact through `LAPLACE_HIGHWAY`. Source fetching remains explicit through `data.sh`. Deployment does not decide when to regenerate an artifact.

`laplace ingest --highway --no-load` checks an existing sidecar without database access. `laplace ingest --highway` explicitly admits it to the declared database. Neither ordinary deployment nor ordinary source ingestion invokes this admission automatically. Existing content remains in existing databases; a new deployment stays empty until admission is requested. Automated artifact promotion and provenance receipts remain unfinished.

Each source deployment step writes under `$LAPLACE_WORK/logs/deploy`. `./deploy.sh drop` is an explicit destructive operation: it drops the named database through the role (`DROP DATABASE … WITH (FORCE)`, never `postgres` or an empty name), then recreates its infrastructure. On desktop, `laplace-ops seed -Yes` uses `deploy.ps1 -Installed drop`: the installed human client's database, Engine and verified caches, without tuning or rebuilding. Active database clients make the drop fail. Its `modular-database` receipt and log use the bounded operation history; `laplace-ops test -Check desktop-installed-deployment` verifies recreation against a disposable database.

```sh
./data.sh fetch                                    # every data set data.tsv declares, from its publisher, at the latest
./data.sh status                                   # each set present or missing; each recipe's roots, resolved or not
./grammars.sh fetch                                # every grammar grammars.tsv declares, cloned from its origin at the latest
```

A host receives no copy of another host's data. `data.tsv` declares each data set the recipes read: its directory under `$LAPLACE_DATA`, how it is fetched (a mirror of the publisher's directory, a file, a GitHub listing, the latest GitHub release), its origin and where under the set it lands, and `data.sh fetch` pulls it from there at the machine's own network speed, as the publisher serves it. `grammars.tsv` and `grammars.sh` do the same for the tree-sitter grammars. `data.sh record` and `grammars.sh record` are the record of what a machine holds. Fetching the same declarations or origins does not establish identical versions, contents or deployments. Compare selected artifact identities and installed configuration.

```sh
./ingest.sh                                        # every source, in recipes/order
./ingest.sh open-english-wordnet verbnet           # these sources
```

`ingest.sh` holds a lock per database, builds and installs nothing, and needs `laplace`, tier 0 and the highway already deployed. Its steps are `laplace ingest`, the write-ahead log it made by table and index (read each minute with `pg_walinspect` into `wal.tsv`), `laplace status` and `laplace bench`, each kept under `$LAPLACE_WORK/logs/ingest-runs/<time>`. What is recorded is passed over by its trunk, so a run that was cut off is taken up by running it again. A source is not begun when the database's volume has not the room the source was measured to take (`room` in its `source` file); that is said.

## The machine

```sh
sudo ./setup.sh                                    # once per machine: volumes, packages, rights, kernel, dependencies, cluster, settings, access
./tune-pg.sh                                       # the server's settings, as the role: apply the declaration, reload, check
./tune-pg.sh --plan                                # the facts read from this machine and every setting they give; no connection
tests/tune-pg-plan.sh                              # the rules against every host's measured facts, and the invariants they must keep
sudo ./setup.sh settings                           # the same declaration, when a pending restart needs root
sudo ./setup.sh restart-controller                 # validate the running cluster, then converge its bounded restart helper
sudo ./setup.sh machine                            # repair declaration permissions only; no provisioning
./setup.sh repair --check                          # validate this host against installation/<hostname>.json; no sudo
sudo ./setup.sh repair --storage-report            # measure declared existing volumes, protected files and deleted-open files
sudo ./setup.sh repair                             # install/repair that declaration and verify the landed application and secrets backups
sudo ./setup.sh secrets-stack                      # hart-server's existing Vaultwarden/OpenBao services; explicit only
sudo ./setup.sh secrets-backup                     # install only the backup job and run one checked backup
sudo ./setup.sh secrets-client                     # host AppRole -> app DB password files and recurring refresh
sudo LAPLACE_DROP=$LAPLACE_PGDATA ./setup.sh drop all   # the cluster emptied and made again (never part of all)
```

`repair --storage-report` saves metadata under the declared work directory's
`logs/storage`, readable by the sudo caller. It reads no file contents and changes
no services, retention settings or stored data. `storage_report_roots` selects the
existing directories to measure; hart-server selects `/var`, `/logs` and `/hosting`.
The report records failures explicitly, including inaccessible or changing files.

`setup.sh` is the one step that needs root. It is not a sequence of patches: the top of the file declares the machine as sets — the volumes Laplace keeps apart (heap, WAL, temporary files, repositories, data), the packages, the dependencies built from `$LAPLACE_SRC`, the server's settings from Operations: Database, who may connect and how (`postgres` over the socket by peer, and `laplace` by peer through the `laplace` map for the operator and the runners; `laplace` and `postgres` with scram from this host, and from `$LAPLACE_LAN` over TLS only) — and each part compares its set with the machine and makes only what is missing. Run again on a finished machine it changes nothing and reports. What it did is kept under `$LAPLACE_WORK/logs/root`; the role's password is in the operator's `~/.pgpass`. Then `./deploy.sh`.

Every name of the machine's is a variable of `laplace.env` with this installation's value as its default: the paths (`LAPLACE_PREFIX`, `LAPLACE_PG_DIR`, `LAPLACE_PGDATA`, `LAPLACE_PGWAL`, `LAPLACE_PGTEMP`), the users and groups (`LAPLACE_PGUSER`, `LAPLACE_ROLE`, `LAPLACE_GROUP`, `LAPLACE_PG_GROUP`), the service (`LAPLACE_PGSERVICE`), the volumes (`LAPLACE_VOLUMES`), the network (`LAPLACE_LAN`) and the agent. Another machine declares what differs in `/etc/laplace/machine.env`, which `laplace.env` reads first, so its units, runners and tools all see one declaration; the file is every user's to read (`setup.sh` makes it so; a declaration that exists and cannot be read is an error, never hart-server's defaults), and holds no secret: the passwords are `/etc/laplace/pgpass`, root's. The following historical hart-cloud example describes its C3 build/substrate configuration. hart-cloud is the on-demand development and AVX-512 qualification host, normally stopped; hart-prod serves production:

```sh
LAPLACE_LAN=100.64.0.0/10                                    # the tailnet: hart-server and the laptop reach it there
LAPLACE_VOLUMES="file lv-wal 16G xfs /data/pgdata/pg_wal"    # no volume groups: the WAL kept apart as a loop-mounted file
LAPLACE_REPOS="Laplace Laplace-Native"                       # the runners this machine hosts
LAPLACE_AGENT_LABELS=laplace,production                      # its jobs: the monorepo's production delivery, the ISA matrix
```

What `setup.sh` makes on a fresh Ubuntu 22.04 host, so that nothing is done by hand: the volumes, or file volumes where there are no volume groups (`file` as the group); the distribution's packages, the ones every dependency's build needs included (`sqlite3` for PROJ, the autotools for PostGIS, GMP and MPFR for PostGIS 3.6); CMake from Kitware; ICU 78 fetched from unicode-org's release (it is a release, not a build); the loader told where ICU 78 and the compiler's runtime are (`/etc/ld.so.conf.d`), so the server's user, the agent and a systemd unit, none of which has anyone's environment, run what icx built; every dependency built from source with its own log under `$LAPLACE_WORK/logs/root` and its failure said, the next one still tried; the cluster, its WAL bounded by the device holding it; the settings, derived from the machine (below), list parameters written as lists; the access rules; the site's own packages and sources (nginx, the .NET 10 SDK from Ubuntu's dotnet backports, Node 24 from NodeSource, the GitHub CLI) before the monorepo's host script; the agents. What Intel does not ship as a package the script still only checks: the oneAPI compiler is installed from Intel's apt repository, pinned to the cluster's build (`intel-oneapi-compiler-dpcpp-cpp-2026.1`).

`setup.sh` runs to its end under `sudo` from a shell, or as a transient unit (`systemd-run --same-dir --setenv=HOME=/root --setenv=SUDO_USER=<operator> ./setup.sh ...`) when the shell may go away before the dependencies are built.

### The application database, on a hosting host

Each host selects one PostgreSQL installation with `LAPLACE_PG_DIR` and one local cluster with `LAPLACE_PGDATA`, `LAPLACE_PGSERVICE`, and `LAPLACE_PGPORT`. `setup.sh appdb` creates the declared `LAPLACE_APP_DBNAME` inside that cluster; it does not install a second PostgreSQL or copy operator credentials. Implementation installers own schemas and OpenBao runtime identities. Consolidate existing duplicate software with `sudo ./setup.sh postgres` on Linux, or `./setup.ps1 postgres` in an administrator PowerShell on Windows. Preview the actual host with `./setup.sh postgres --check` or `./setup.ps1 postgres -Check`. The full explicit setup includes consolidation after the custom dependency build. Configured distribution clusters must be adopted before their binaries can be retired; consolidation never drops databases or force-stops PostgreSQL processes.

### Backups

A host that holds databases declares `LAPLACE_BACKUP_DATABASES` (e.g. `laplace laplace-mono` on the database host, `laplace-app` on the hosting host) and `LAPLACE_BACKUP_TARGET` (`user@host:/path`, the landing on hart-server's backup array) in its `/etc/laplace/machine.env`; `sudo ./setup.sh backup` makes the host's own key (`/etc/laplace/backup.key`; its public half `/etc/laplace/backup.pub` is declared in `backup/landing.keys`, which `setup.sh landing` on hart-server authorizes, write-only into the host's own directory) and a nightly timer at 03:30 UTC that dumps each database with `pg_dump -Fc`, proves the dump readable with `pg_restore --list`, writes its SHA-256, ships both by rsync over the tailnet, and keeps `LAPLACE_BACKUP_KEEP_DAYS` (30) locally; the landing keeps its own retention. `LAPLACE_BACKUP_PGBIN` and `LAPLACE_BACKUP_PGPORT` name the server's binaries and port when they are not the substrate cluster's. A restore is proven by restoring into a scratch database on another host; that is an operation to run, not a part. Hosts without the declaration skip the part.

### The server's settings

`tune-pg.sh` (and `tune-pg.ps1`, the same rules) derives every setting from the machine that runs the server, so hart-server, hart-cloud, hart-prod and HART-DESKTOP each get their own numbers from one rule set. The facts are read, never typed: the memory (a cgroup's limit when lower), the logical processors and the physical cores they sit on (a sibling thread is not another core), the volume holding the write-ahead log and whether it is the log's own, whether the data's device rotates. What a machine cannot say is declared in its `machine.env` with the measurement that set it: `LAPLACE_PG_RESERVED` (memory its other residents keep: HART-DESKTOP's llama-servers), `LAPLACE_PG_BUFFERS_MAX` (the largest shared memory a build maps: Windows), `LAPLACE_PG_PROFILE` (`substrate`, the default: the server shares the host with the ingest client, the build and the agent; `app`: with the API and the MCP, the hosting host's application cluster, which `setup.sh appdb` tunes with it). The memory is one equation in four domains, the monorepo's `PostgresResourcePlan`: of what the server may use, a quarter is the shared cache, a quarter the backends' private memory, a quarter the client's and a quarter the page cache; the private quarter is divided by the backends the connection plan allows (every connection and every parallel worker), so `work_mem` is what each may hold. The connection plan is the ingest's fan (one coordinator, two a core, three observers), the serving pools and the maintenance workers; the serving pools are the host's services' (the API, the MCP, the runners' checks, psql), which the machine cannot say: `LAPLACE_PG_SERVING` declares them with the measurement, and undeclared they are four a thread (`app`: eight a thread, sixteen at least). Parallel query runs on the cores, asynchronous reads on the threads, the log is bounded by its volume. `./tune-pg.sh --plan` prints the facts and the settings they give without connecting; `tests/tune-pg-plan.sh` runs the rules over every host's measured facts and the invariants each plan must keep (nothing promised twice: the backends' memory within the private quarter, the buffers within PostgreSQL's 40%, the log's buffers within its target). A server is tuned on the host that runs it: run from a client (hart-prod's `LAPLACE_CONNINFO` names hart-cloud's server) it refuses.

Automatic query-plan dumps are disabled in every `LAPLACE_PG_TRACE` mode. Query statistics and I/O timing still follow the selected tracing mode; plan capture can be enabled in a specific diagnostic session. Array constants inside plans can repeat across partitions and are not bounded by parameter logging limits.

`sudo ./setup.sh logging` installs syslog rotation at a 64 MiB threshold, with seven rotated files and a check every five minutes. The threshold is checked periodically, not a filesystem quota. `sudo ./setup.sh locks` repairs shared lock permissions and declares both host lock files at boot without replacing their inodes. These are focused setup stages; no database recreation is involved.

### A host that stops itself

A host that is started for a job and pays by the minute (hart-cloud) declares `LAPLACE_IDLE_STOP_MINUTES` in its `/etc/laplace/machine.env`, and `sudo ./setup.sh idlestop` installs a five-minute timer that powers the host off once nothing has run on it for that long: no runner job, no ingest, deploy or build, no login session, and no lease. The lease is the delivery's: the monorepo's cloud-host job, having started the instance, writes `laplace-lease` (`<run id> <expiry>`) into its metadata, and its release job removes it once the build job has run, so a job queued behind a concurrency group or waiting for a runner does not find the host gone under it (2026-10-10 05:04Z, run 38023100147: thirty idle minutes while its job waited). On Compute Engine that is a stop; the disk stays and the cloud-host job starts the instance again through workload identity when the next delivery needs it. Hosts without the declaration skip the part.

### The shares

```sh
sudo ./setup.sh shares                             # the SMB shares for the development machine; not part of all
```

`shares` serves `LAPLACE_SHARES` (vault, archive, backup, inbox) to `LAPLACE_SHARE_USER` alone. It uses plain SMB 3,
smbd only (nmbd is disabled), and admits only the LAN: `hosts allow` and `interfaces` cover `LAPLACE_LAN`,
`LAPLACE_SHARE_LAN6`, and link-local on `LAPLACE_SHARE_IF`, and ufw allows 445/tcp from the same sources. It
declares the whole `smb.conf` and keeps the distribution's original as `smb.conf.orig`. A change is reloaded and
never restarted, so a copy in flight is not cut. A user without an SMB password is asked for one (`smbpasswd`); it
is never written down. HART-DESKTOP checks the shares with `setup.ps1 shares`.

### The agents

```sh
sudo ./agents.sh                                   # one GitHub Actions runner per repository of $LAPLACE_REPOS, as laplace-runner
sudo ./agents.sh status                            # each, as this machine and as GitHub see it
sudo ./agents.sh remove Laplace-Wiki               # unregister and remove one (or all)
```

`agents.sh` gives every repository its own runner on this machine, all as `$LAPLACE_AGENT_USER` (default `laplace-runner`) with programs under `$LAPLACE_AGENT_HOME/<repo>/runner`, workspaces under `$LAPLACE_WORK/agents/<repo>` and builds under `$LAPLACE_BUILD/agents/<repo>`: its own environment (`runner/.env`; the machine's dependencies, data and database), registration (named `<host>-<repo>`, labelled `laplace,<repo>`), and service. No runner has root or any sudo rule: `agents.sh` grants none and `setup.sh rights` removes any that names one; each has the shared group and nothing more. Registration takes a token per repository: `gh` logged in as an administrator, or `LAPLACE_AGENT_TOKEN_<REPO>`. Laplace-postgres, Laplace-Engine and Laplace-Operations check out the repositories they build beside themselves; they are private and a workflow's own token reads only its repository, so `agents.sh` puts the operator's `gh` credential (or `LAPLACE_CHECKOUT_TOKEN`) in those as the secret `LAPLACE_CHECKOUT`. Each repository's `.github/workflows/laplace.yml` is its job on its runner: Native builds with icx and gcc and runs its tests under both; postgres builds, installs into the extension directories by rename (no root: the group's right) and updates the extension in the database; Engine builds and runs its checks; Wiki builds the site; Operations runs `deploy.sh` on a push, or `deploy.sh drop` when dispatched with `drop`. `ingest.yml` runs `ingest.sh` when dispatched, with the sources to ingest as its input. The operator and the agent share `$LAPLACE_GROUP`: every shared tree is that group's, set-group-id and group-writable, so neither meets a permission.

When an idle registered runner still uses work/build directories under its home, `agents.sh` stops its service, moves those directories onto the declared work/build roots, updates its local workspace registration and starts it again. Existing absolute cache paths remain symlinks to the moved files. An active job or conflicting destination refuses migration.

### The deployment target: every merge to main

hart-server is the staging target for deployment rehearsal: build/install, schema changes, service operation and failure handling before production. A push to
this repository's main, and a `repository_dispatch` (`main-merged`) that Laplace-Native, Laplace-postgres and
Laplace-Engine send from their own `laplace.yml` once their CI passes on main, run `laplace.yml` here with a frozen
component revision set. A component dispatch retains its exact triggering commit;
other components select main. Engine CI and the verified Native cache artifact
must qualify that selection. Deployments run one at a time (the concurrency group
`hart-server-laplace`, which `ingest.yml` shares).

Manual dispatch accepts `engine_revision` to retain an already qualified Engine
while delivering an independent infrastructure repair. It requires a full commit
in Engine's main history and the same real CI qualification as automatic delivery.
An empty input selects latest main. `rebuild_runtime` remains an explicit request
to discard reusable build outputs; ordinary delivery reuses them.

| job | what |
|---|---|
| deploy | `seed-stamp.sh decide`, then `deploy.sh`, or `deploy.sh drop` when the database is reseeded |
| checks | `verify.sh deployment`: extension version/tables and Engine/PostgreSQL artifact compatibility, with observed binary/artifact hashes |
| ingest | only for an explicit reseed request: `ingest.sh` (every source of `LAPLACE_SOURCES`), then `seed-stamp.sh seeded` |
| reads | `verify.sh reads`, followed by modular packaging, activation and real authenticated MCP/Engine database verification |

The modular workflow targets staging and optional cloud qualification. Production
application promotion belongs to the monorepo delivery workflow.

Each job writes what it found to the run's summary.

**The reseed policy** (`seed-stamp.sh`). A database carries, as its comment, the stamp of the code it was seeded from: a
hash of the trees of Laplace-Native, Laplace-Engine (its source and recipes), Laplace-postgres and Operations'
floating-point contract (`toolchain/`, `math/`, `patches/`, `dependencies.tsv`). Documentation, workflows, tests and the
firmware do not count in that stamp. Since 2026-10-09 the policy only reports: a push or main-merged dispatch does not authorize dropping or ingesting the database. Explicit `drop` recreates infrastructure without ingestion; explicit `reseed` drops and then ingests the configured sources. A pending stamp records interrupted ingestion; it does not authorize an ordinary deployment to resume it.
By hand, in one click: `laplace.yml` with `drop` (empty, no ingest) or `reseed` (drop, then every source), or
`ingest.yml` with `reseed`.

**Separate build qualification** (`verify.sh build`, `fingerprint.sh`, `fingerprint.ps1`). An explicitly requested qualification writes the record of its build: the commits, tier 0 and its flags made afresh, the highway, and, for each source of
`LAPLACE_DETERMINISM`, the claims its recipes make, counted and hashed as a sorted set. Each source is decomposed twice,
and the two runs must agree. The record is published on the branch `fingerprints` of this repository, at
`<native>-<engine>/<machine>.txt`, and compared with every other machine's record for the same commits. On
HART-DESKTOP, `pwsh -File fingerprint.ps1`, run after `build.ps1` at the commits a deployment names, writes the
Windows record beside it, and either side reports any field that differs.

No peer record means cross-machine verification is incomplete, not successful. The scripts return exit 2 when no
other machine's record is available; the shell comparator also distinguishes retrieval failure from a mismatch.
`verify.sh build` reports incomplete evidence as a non-passing check. Record comparison does not establish that an
application starts, an installation works, or a semantic operation is correct on another machine.

The record also says what its results are made from, so that two records which differ are told apart by their inputs
before their arithmetic: the Unicode data (`ucd`: its version, as `DerivedAge.txt` names it, and its files but the
charts), the ICU and the Unicode version it is of (`icu`), the resources the highway was generated from (`resources`,
as the highway's log names them), and the directory each of those and each source of `LAPLACE_DETERMINISM` is read from
(`data`: its files and one hash of their paths, sizes and SHA-256). A result that differs is then said to follow from
inputs that differ, or to come from the same inputs. The current comparison fails output mismatches when inputs
match or are unknown, and ICU or Unicode-version mismatches. Differences attributed to different data are reported
without failing; this does not establish equivalent results. `verify.sh build` also fails when the Unicode
data is not of the Unicode version the ICU is of. `fingerprint.sh inputs` (`fingerprint.ps1 -Inputs`) prints those lines
alone, in about a minute and without the engine; `fingerprint.sh compare FILE DIR` (`-Against DIR`) compares with the
records in a directory in place of the branch's.

The [ongoing system audit](docs/2026-10-10-system-audit.md) records confirmed lifecycle, verification and service
defects, their evidence, and outstanding work. It is not a system-completion report.

The modular command uses the installed release and its packaged recipes/firmware, not a runner's build tree.
The declared `operator_client` is installed by modular setup. It can also be installed without sudo:

```sh
python3 installation/install-client.py --installation /etc/laplace/modular.json \
  --role laplace --work /repos/work/clients/ahart/laplace --data /vault/Data \
  --command "$HOME/.local/bin/laplace"
laplace --where
laplace status
laplace help ingest
```

These are hart-server's declared paths and existing human database identity, not requirements for another host.
`LAPLACE_CLIENT_CONFIG` selects another client declaration. `laplace.sh` is a checkout convenience for the same
installed client; do not copy it onto PATH. Prepared tier/grammar inputs still use the installation's declared
paths. `laplace-mono` is the separate monorepo client; `laplace-refactor` is not installed by this operation.

On Windows, `laplace-ops sources desktop` reads that installed client's recipe catalog.
`laplace-ops ingest desktop <sources...>` and `ingest.ps1` forward to the same installed
`laplace ingest` operation. They do not use a build-tree executable, reset statement
statistics, install diagnostic extensions or run a full benchmark after ingestion.
Run `laplace bench` separately when measurements are wanted.

When the declared desktop UCI service is installed, development configuration and
UCI delivery bind its `mono-development` profile to the API's local SSPI substrate.
UCI delivery incrementally builds and publishes the separate connector, then checks
a real search through its authenticated HTTPS endpoint. Web-only delivery leaves it
alone. One-time UCI setup owns its service, certificate and operator ACLs.

The shared/modular root steps are `sudo ./setup.sh`. Its explicit compatibility part `site` runs the monorepo's `deploy/linux/site-host.sh` (the API and SPA
over `laplace-mono` behind nginx). Its part `agents` runs `agents.sh`, which gives every repository of `LAPLACE_REPOS` its
runner. `agents.sh status` fails when any repository of the owner with a self-hosted workflow has no runner here, or is
missing from `LAPLACE_REPOS`. A runner carries `LAPLACE_AGENT_LABELS`, its repository's name, and the repository's own
labels from `LAPLACE_AGENT_LABELS_<repo>`. GPU labels require an explicit usable-host
declaration. hart-server's GTX 1080 Ti has broken cooling and is off limits; do not
register it with GPU labels or run GPU probes/workloads. hart-desktop's RTX 4060 Ti
is the user-declared development GPU.

## Build

```sh
./build.sh                # the extension and the engine, each with Laplace-Native built as part of it
./build.sh install        # also installs the extension into PostgreSQL's directories; CREATE EXTENSION laplace then makes the schema
```

The three code repositories sit side by side under one source root, `$LAPLACE_SRC`; the dependencies' sources under
`$LAPLACE_DEPSRC` (the same root, unless an agent's); build trees under `$LAPLACE_BUILD`; generated data, logs and
tier 0 under `$LAPLACE_WORK`; installed dependencies under `$LAPLACE_DEPS`; the data sets under `$LAPLACE_DATA`.

## Windows (the development machine)

`setup.ps1 network` reconciles Windows' LAN search domains and Tailscale DNS; `network.ps1 -Check` verifies
resolution without changing it. Windows Tailscale writes bare peer names into its managed hosts-file section.
LAN-only consumers use the explicit LAN name (`LAPLACE_SHARE_HOST=hart-server.lan`); remote consumers use the
tailnet name. The check resolves all registered peers and internet DNS without starting offline machines. It
does not establish that a peer's application is healthy or that the transport is direct.

For Google Cloud's existing VM tags, `LAPLACE_GCP_PROJECT=PROJECT ./network-gcp.sh apply` declares only the
encrypted Tailscale UDP 41641 ingress rule; `check` verifies it. Network, target tags and source ranges have
`LAPLACE_GCP_NETWORK`, `LAPLACE_GCP_TAILSCALE_TAGS`, and `LAPLACE_GCP_TAILSCALE_SOURCES` overrides.
Verify actual direct connectivity with `tailscale ping`; a firewall rule alone is not that evidence.

Substrate-cluster access also requires PostgreSQL authorization. `setup.sh access` preserves the optional
`$LAPLACE_PGDATA/pg_hba.remote.conf` include for explicit remote database/role/client rules, independently of
`LAPLACE_LAN` (which also controls LAN shares). For example, `hostssl laplace-mono laplace 100.124.95.17/32
scram-sha-256` admits hart-prod to hart-server's monorepo substrate over TLS. Validate `pg_hba_file_rules`
for errors and reload PostgreSQL after changing it. Do not substitute the modular `laplace` database for
`laplace-mono`: their schemas and installed native interfaces differ. Selecting another content substrate
does not move the hosting application's separate `LAPLACE_APP_DB` accounts and billing database.

The backup's `Laplace` set takes its repositories, generated work, and corpus inventory from the machine's
`LAPLACE_SRC`, `LAPLACE_WORK`, and `LAPLACE_DATA`, including when they are on E:. `backup/copyoff.ps1 -Set Laplace
-Plan` lists the resolved paths without copying. Required sources cannot silently disappear. Every copy uses a
fresh manifest, Robocopy's incremental transfer, and destination SHA-256 verification; an old receipt never skips
later source changes. Failures reach the scheduled task. `setup.ps1 backup` registers the current implementation;
the task is invoked on demand, with no recurring trigger. Ingest is **inventory only**, and this copy-off is not a
PostgreSQL backup or a versioned/offsite backup. Database recovery needs its own supported backup and restore path.
Run `pwsh -File tests/backup-continuity.ps1` for local copy, corruption, unreadable-file and failure-propagation checks.

```powershell
pwsh -File setup.ps1                  # prepare locked development inputs and register laplace-ops
pwsh -File setup.ps1 all              # explicit elevated host provisioning, when the host needs it
pwsh -File setup.ps1 deps report      # one part, or several
pwsh -File tune-pg.ps1 -Check         # the server's settings against their declaration; without -Check: apply, restart when allowed, check
laplace-ops deploy -Target desktop -Plan # show the delivery stages without changing the installation
laplace-ops deploy -Target desktop    # package modular CLI/MCP, publish IIS, migrate and verify
laplace-ops clients                   # installed/running modular versions, owning clients and protected releases
laplace-ops clients verify -Json      # verify running client versions without rebuilding or cold-starting the API
laplace-ops storage -Json             # audit local output ownership and retention without deleting
laplace-ops clean                     # collect unused local releases, packages, blobs and abandoned generated output
pwsh -File setup.ps1 clean            # the same collector through setup; cleanup is also an alias for clean
```

Desktop deployment uses the enrolled Windows operator and the declared developer shell.
Modular packages include their frozen Native manifests and verify that Native can
reproduce the selected Highway from them. Prepared inputs and compiled grammar
roots are build inputs; installed processes read their release's copies. Shared
immutable files use hardlinks, while grammar generator sources stay out of the
runtime recipe tree. `laplace-ops test -Check desktop-native-roundtrip` runs the
maintained Prototype Gates A/B against the installed client and the existing
cluster, using a disposable database. Native ingestion keeps prepared transactions
disabled (`max_prepared_transactions=0`).

It runs the maintained tuner in apply mode before building: changed settings are
written, reloaded and verified. A required service restart follows the tuner's
existing permission and active-ingestion checks; unresolved changes fail the stage.
It reports each stage, retains its full output, and writes a combined receipt under
`$LAPLACE_WORK/operations/desktop-deploy-*/receipt.json`. It also builds and packages the
declared modular Native/Engine/MCP stack using the same installer as `components desktop`
and `setup.ps1 client`. Before selecting a modular release, acceptance exercises native
composition, database/cache agreement, recipe discovery, MCP initialization, tool discovery
and actual MCP `text` and `ingest_status` calls. MCP readback must report the selected
database; connection, schema and tool errors fail acceptance. This read-only probe
does not require a populated corpus or establish code-search coverage. Success is printed after these checks,
both database migrations, publication and desktop verification pass. Migrations use
the staged package's runtime before IIS selects its new application binary. A failed stage
returns a nonzero exit code with its log path; compiler/npm warnings remain visible
and are also listed in the receipt. Initial provisioning remains owned by `setup.ps1`
and `Install-IisRuntime.ps1`; deployment does not reset databases or silently repair ACLs.

An existing stdio MCP session remains pinned to its executable until its calling application
reconnects. Setup and deployment inventory those sessions and report their PID, parent client,
running release and installed release. They never terminate the client application.
When older sessions remain, the deployment receipt says `installed_pending_reconnect`
and the command exits **2**: the packages are installed, runtime acceptance is pending,
and no rollback or rebuild is implied. Reconnect the reported MCP clients, then run
`laplace-ops clients verify`; it exits 0 when the inventory is current, 2 for older clients,
or 1 for incomplete process visibility. `status desktop` and `verify desktop` include this
same inventory; the latter also preserves its application acceptance checks.

The inventory marks selected releases and releases with running processes as protected.
Missing process visibility protects every release. An unselected release without a process
still requires a reference audit (including database cache settings and rollback references);
`laplace-ops clean` performs that audit and collection. Linux `setup.sh` owns the separate systemd MCP
service and does not control Windows user stdio connections.

Desktop builds, modular installation (`setup.ps1 client` included), IIS publication and
deployment share one operation lock and collect in their outer `finally` block. Each
publisher also removes its own private assembly directory after success or failure.
Standalone Python publishers call the same collector after releasing the component lock.
Cleanup does not start a build, select a release, recycle IIS, or terminate an MCP client.
It retains installed selections, paths referenced by PostgreSQL cache settings, live
processes, one additional rollback release, and two reusable component/package outputs.
Unreferenced blobs are removed only when their Windows hardlink count is one. This is a
bounded local cache; version hashes identify immutable bytes needed by running processes.
They do not define a historical package repository.

`clean` also removes obsolete generated worktree builds and abandoned publisher scratch.
Declared incremental profiles and builds belonging to registered Git worktrees are kept;
source checkouts, canonical database content, corpora, perf-caches and indexes
are outside its deletion policy. Paths with junctions are rejected. Incomplete process
visibility keeps affected releases. Concurrent publishers prevent collection. Receipts
under `$LAPLACE_WORK/operations/storage-*.json` list removed paths and drive free space
before and after; logical hardlink lengths are never reported as reclaimed disk space.

`LAPLACE_WORK` is disposable working data. Installed PostgreSQL extensions and
their selected perf-caches use `LAPLACE_DEPLOY` (by default
`$LAPLACE_DATA_ROOT/deploy`); PostgreSQL's own logs use `$LAPLACE_PGDATA/log`.
Development and IIS share the installation's persistent `state/keys` key ring.
Development setup/start preserves legacy `work/development/keys` XML, including
revocations, by a verified merge that refuses conflicting key IDs. Source recovery
archives belong outside the work tree as well. Recreating work directories must
not require restoring application secrets or source history.

Completed desktop deployment, component, development build/run/verification, database and named-test histories are bounded:
three successful runs and one failed run per operation and target (database operations
are grouped by host, database and command). Storage receipts rotate through the same
collector. Active owners, running processes, runs completed in the last five minutes,
explicit receipt links from retained runs, and directories containing `.retain` are
protected. Unfinished or unrecognized output is preserved for ownership review.
Named tests and database commands collect completed histories on exit; deployment and
installation collect them through their existing `finally` cleanup. A busy publisher
defers automatic history collection until the next operation. Cleanup failures are
reported and fail an otherwise successful command. `laplace-ops clean` uses this same
policy without rebuilding anything.

Linux CI end-of-job collection uses `clean --if-idle`. A busy host produces a
`deferred` receipt with zero removals; the next idle collection reclaims the
retained outputs. Foreground cleanup retains its full host reservation. Cleanup
never upgrades or releases an inherited reader reservation.

Cleanup also invokes the installed Native load-retirement API using the declared
local database identity. Private staging relations are reclaimed after their
owning session disconnects; an idle live ingest retains its lease. The same
operation runs after desktop and native deployment and at the next ingest
startup. Unmarked staging tables and canonical content are preserved. Database
results, including retired relation counts and allocations, appear in the
cleanup receipt alongside the filesystem results.

On the Ubuntu laptop, `bash setup.sh operator` registers `~/.local/bin/laplace-ops`.
`laplace-ops clean` and `bash setup.sh clean` use its declared Linux work/build roots;
`laplace-ops storage` audits without deletion. Native setup/deployment collects under
its existing host lock, and extension installation removes its private staging even
after failure. No IIS or Windows host declaration is required.

Hosted maintenance uses GitHub Actions: `laplace-ops clean -Target staging -Wait` on
Windows, or `laplace-ops clean --target staging --wait` on Linux, dispatches the
existing **Product — maintenance** workflow. Select `production` or `cloud` in place
of `staging` for those hosts. `storage` selects
its audit operation. There is no SSH publication or production compilation. The
staging and production delivery jobs collect after package upload and consumption;
cloud qualification collects before releasing its lease. Cleanup receipts are retained
as Actions artifacts for fourteen days. Cloud maintenance leaves a stopped VM off and
defers to an active qualification lease's own cleanup.

Delivery work is owned by repository/run ID across CI steps. A different active run,
an unavailable run-status API, or unresolved rollback state preserves that staging.
Native releases retain their current selection, live process/cache references and one
rollback; managed applications retain their existing runtime-lease/rollback owner.
Canonical incremental profiles, source, corpora, archives, databases and shared
infrastructure are outside collection. Linux jobs share the same host-resource lock
as deployment and ingestion. End-of-job cleanup runs on success, failure and cancellation;
the next explicit cleanup can retire residue after a hard runner interruption.

Native Linux packages hold a shared `.runtime-lease` lock for each client's whole
lifetime. Collection takes the exclusive lock through deletion, so service accounts
do not need permission to inspect each other's executables. Normal collection keeps
the selected release, live leases/cache references and one rollback.

To replace old unleased staging packages, run
`laplace-ops components -Target staging -Force -Wait` (Windows) or
`laplace-ops components --target staging --force --wait` (Linux).
This explicitly recompiles the native runtime, activates and verifies it, then retires
unselected old packages. Failed build/activation keeps normal retention. Database
resets are separate inputs, defaulting to false. Reconnect existing stdio clients
after this replacement because their old package paths are retired.

Windows modular builds preserve Ninja's outputs. Grammar generation and compilation
reuse receipts that bind source/import/header contents, toolchain/options and output
checksums; unchanged timestamps alone do not invalidate them. Missing or corrupted
outputs rebuild. Packaging reuses an intact selected release when its current binaries,
recipes, firmware, caches, grammar DLLs and runtime dependencies still match, without
copying another package. Packaging does not deploy a database schema.
Run `pwsh -File tests/grammar-incrementality.ps1 -Output <receipt.json>` on the configured
Windows toolchain for the real generation/compilation acceptance, including changed
imports, scanner headers and damaged/missing outputs.

`setup.ps1` is `setup.sh`'s counterpart: the same parts, each a declaration compared with the machine, logged under
`$LAPLACE_WORK\logs\root`; the parts that touch the service, its rights, its settings and its access need an elevated
PowerShell and refuse otherwise, so the rest runs as the developer. `laplace.env.ps1` is `laplace.env`'s: every name of
the machine's (the roots, the cluster and its log, the service and its account, the role, the network, the locks) and
what the settings' rules cannot read from the machine (what its other residents keep, the shared memory this Windows
build maps, the log's room on a shared drive), each with the measurement that set it. `tune-pg.ps1` is `tune-pg.sh`'s:
the settings derived from the machine the same way (the same plan, line for line: `pwsh -File tune-pg.ps1 -Plan` shows it) and checked by the same statement, so the Linux server and the
Windows one each get their own numbers from one set of rules.

A Windows machine declares what differs from HART-DESKTOP's defaults in `%ProgramData%\Laplace\machine.env`
(`LAPLACE_MACHINE_ENV` names another file): the counterpart of `/etc/laplace/machine.env` and the same format, one
`NAME=value` per line, `#` for a comment, `%NAME%` expanded. `laplace.env.ps1` reads it first, so every script and
service on the machine sees one declaration; a value set in the environment still wins. The server's address and
port are names too (`LAPLACE_PGHOST`, `LAPLACE_PGPORT`): the settings, the access rules, the firewall rule and the
role's pgpass line follow them.

```
LAPLACE_SRC=E:\Repositories\Laplace
LAPLACE_PGDATA=E:\Data\Laplace\pgdata
LAPLACE_PGWAL=D:\Data\Laplace\pg_wal
LAPLACE_PGPORT=5432
```

What differs is only what Windows forces. No volume is made: `volumes` reports each root's drive and makes its
directory. The toolchain is installed by hand (Visual Studio, oneAPI, CMake, Git, uv) or by the manifest: `packages`
says what is missing and installs MSYS2's packages. There is no kernel part (huge pages stay off until the backends'
shared-memory mapping is measured to bear them). The server is a Windows service under `NT AUTHORITY\NetworkService`;
there is no socket, so every local connection is scram on loopback. `deps` reads the same `dependencies.tsv`: every row
for `windows` checked out at its commit, or downloaded, verified by SHA-256 and unpacked; then every row with a `build`
whose `proof` is missing, built and installed into its own prefix. The builds use icx under the floating-point contract
in `toolchain/determinism.tsv`: laplace-math first (`math/`), CMake builds through `-DCMAKE_TOOLCHAIN_FILE=toolchain/laplace.cmake
-DLAPLACE_MATH=<laplace-math.lib>`, PostgreSQL's Meson build through the native file `toolchain/meson-native.py msvc
<laplace-math.lib>` writes, with `patches/postgresql`, and PostGIS by `toolchain/windows/postgis.sh` in MSYS2's shell
(from the oneAPI dev shell, `MSYSTEM=MSYS MSYS2_PATH_TYPE=inherit`, `LAPLACE_MATH` set), which applies `patches/postgis`,
configures, builds and installs into that PostgreSQL. On Windows every link ends with laplace-math and then libmmd,
Intel's libm, kept for the exact operations only; no transcendental function in any installed binary comes from it.

The Windows machine is one leg of the cross-OS check: a database the Linux machine's clients reach over `$LAPLACE_LAN`
with TLS, and a client of the Linux machine's database (`LAPLACE_CONNINFO`); `report` tries both. The role has one
password across the installation, the deployment target's: `access` reads it from `LAPLACE_PEER`'s operator pgpass over
the operator's SSH key and gives it to the role here, so one pgpass line reaches both databases; the operator's pgpass
lines for other hosts are kept. HART-DESKTOP's one-time cleanup of what earlier set-ups left is
`toolchain/windows/retire.ps1`, not part of setup.

### The desktop's own parts

Three parts of `setup.ps1` declare what HART-DESKTOP is besides a Laplace host. None is part of `all`; each is named to
be run, says what it changed, changes nothing on a second run, and with `status` (`setup.ps1 backup status`; alone,
`setup.ps1 status`, all three) only reports. Their names are variables of `laplace.env.ps1`.

```powershell
pwsh -File setup.ps1 shares           # hart-server's shares answer by UNC path, with a credential
pwsh -File setup.ps1 services         # elevated: the operator may start, stop and query the GPU services
pwsh -File setup.ps1 firewall         # elevated: the inbound rules this machine's endpoints need
pwsh -File setup.ps1 backup           # the copy-off task, registered or updated; then its state
pwsh -File setup.ps1 status           # all four, reporting only
```

**shares** checks, and makes nothing: the Credential Manager entry for `LAPLACE_SHARE_HOST` (never printed), that
445/tcp answers, and that each `\\<host>\<share>` of `LAPLACE_SHARES` answers. No drive letter is mapped and the
operator's Explorer locations are left alone. A failed check says what to do: `cmdkey /add:hart-server /user:ahart
/pass` (it asks for the password), or `sudo ./setup.sh shares` on hart-server.

**services** appends one allow ACE for the operator's own SID (`LCRPWPLO`: query, start, stop, interrogate) to each
service of `LAPLACE_GPU_SERVICES`, so `chess\chess-gpu.ps1` switches the card without elevation. Already granted is
known by the SID, never by the ACE's text (Windows reorders the rights). A change prints the SDDL before and after;
`sc.exe sdset <service> "<before>"` undoes it.

**firewall** makes the inbound rules of `LAPLACE_FIREWALL` (`name=port@client;…`; today `engines=5190@192.168.1.2`, the
engine endpoint for hart-server): one named rule each, TCP, from that one client, on private networks. A missing rule
is created and one whose port, client or profile differs is corrected; a second run changes nothing.

**backup** is the copy-off of HART-DESKTOP's drives to hart-server, in `backup\`. `jobs.psd1` is the job list: each
set (D:, then C:'s `source`) with its inbox, and each job's source, destination, robocopy exclusions, manifest
destination and whether it is only hashed. The `Models-*` jobs are on hold and run only with `-Models`. `copyoff.ps1
-Set D` writes each job's SHA-256 manifest first (`hash-manifest.ps1`: compiled C#, 8 workers, rows streamed to
`.part`; `# path<TAB>size<TAB>sha256   source=ROOT`, the rows, `# total files=N bytes=B`). It then checks for room on
hart-server over SSH (what is left to copy, plus 5 GiB, or exit 3 and nothing more is copied) and copies with
`robocopy /E /COPY:DAT /DCOPY:DAT /XJ /FFT /R:2 /W:5 /MT:8 /NP /UNILOG+`. It never uses `/MIR`, `/PURGE` or `/MOV`.
The D: set also keeps the uncommitted edits in `LAPLACE_DEPSRC`'s checkouts as patches. `run.ps1` runs every set.
The part registers it as the scheduled task `LAPLACE_BACKUP_TASK`, which runs as the operator, interactive and not
elevated, with no time limit and no trigger, in a headless console. The part never changes the task while it runs.
Start it with `Start-ScheduledTask -TaskName copyoff`; logs and manifests are under `LAPLACE_BACKUP_LOGS`.

## The chess lab's conventional reference

Stockfish, fastchess, Ordo, Lc0, Lc0's networks and the opening suites are rows of `dependencies.tsv`, each pinned by
commit or by SHA-256 (a `data` row is a file the lab reads, fetched into `$LAPLACE_DATA`). fastchess conducts matches,
SPRT and the ladder; cutechess stays for the GUI (Laplace-Wiki, Sequence/Conflicts.md K1). Syzygy tables are not
provisioned here: an engine probes them as a provider, and they are not content Laplace depends on.

```sh
sudo ./setup.sh chess                 # Linux: chess/provision.sh as the operator (2 cores, niced), then the links in /usr/local/bin
chess/provision.sh report             # what is installed: each program by SHA-256, Stockfish's bench, the data rows
```

On Linux Stockfish is built with `make profile-build ARCH=$LAPLACE_STOCKFISH_ARCH` (default `x86-64-bmi2`) and
`$LAPLACE_STOCKFISH_CXX` (default `g++-12`), and is installed only when its bench prints the generation's node count
(2497913 for sf_19); Linux Lc0 is built from its tag with the plain CUDA backend only when `LAPLACE_GPU_HOST`
explicitly matches that machine's short hostname. The default is empty: no GPU probe or CUDA build. Keep it empty
on hart-server; its GTX 1080 Ti is prohibited. HART-DESKTOP is the designated GPU host. On Windows `setup.ps1 deps` unpacks fastchess, Ordo and Lc0's CUDA 12 package and
fetches the data rows; Stockfish there is the monorepo's `install-stockfish.py`.

The RTX 4060 Ti on HART-DESKTOP is shared with the llama.cpp embedders code search depends on, so it has two modes,
switched explicitly and without elevation (the operator holds start, stop and query on the three services):

```powershell
pwsh -File chess\chess-gpu.ps1 status     # the services, their /health, the card's free memory, any Lc0
pwsh -File chess\chess-gpu.ps1 on         # chess-GPU mode: the embedders stopped, the card free for Lc0
pwsh -File chess\chess-gpu.ps1 off        # index mode, the default and what a reboot returns to
```

Each switch is journaled in `$LAPLACE_WORK\logs\chess-gpu.tsv` for the match generation's receipt. Lc0 is never a
service: the conductor starts it per match, only in chess-GPU mode.

## Repair

Operational completion is tracked in [the acceptance register](acceptance/README.md) and [issue #2](https://github.com/SaltyPatron/Laplace-Operations/issues/2).
Named checks save revision- and host-specific receipts in CI; unimplemented outcomes stay incomplete.

These component repair commands do not yet constitute a transactional product installer or a complete rollback.
The [system audit](docs/2026-10-10-system-audit.md#expanded-installation-delivery-and-resource-audit) records the
remaining differences between entry points, machine configuration and live services.

Use the relevant component operation: `sudo ./setup.sh` after a
volume, package or access rule went missing; `./tune-pg.sh` after a server setting drifted (`deploy.sh` runs it, and
the job fails when the live server does not match); `sudo ./setup.sh settings` when a pending restart needs root;
`./deploy.sh` after a build or a database was cut off; `./ingest.sh` after a load was; `sudo ./agents.sh` after a runner was lost (its unit restarts on failure and survives a job's out-of-memory kill), or
`sudo ./agents.sh remove REPO` and again to re-register one. What each did is under `$LAPLACE_WORK/logs`.

Inspect PostgreSQL sizing with `./tune-pg.sh --plan` or `pwsh -File tune-pg.ps1 -Plan` before applying it.
On Windows, a separate WAL drive is still treated as shared unless the machine declaration explicitly sets
`LAPLACE_PG_WAL_DEDICATED=1`. Set that only for a drive reserved for WAL; the desktop's D: also holds dependencies
and builds. The planner's arithmetic checks do not establish a bound on all simultaneous query operators or
other processes' memory use.
When that arithmetic already reports overcommit, plan/check/apply now fail; apply refuses before contacting
PostgreSQL. This catches a known-invalid plan without claiming that a fitting plan has passed a workload test.
