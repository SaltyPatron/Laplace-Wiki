# Operating Laplace

For shared infrastructure and modular runtime setup, run `sudo ./setup.sh` from Operations.
For monorepo API/MCP, browser and chess identity setup, run `sudo bash deploy/linux/site-host.sh`
from the Laplace checkout. The latter owns database TLS, scoped runtime credentials and their refresh;
an existing workload enrollment does not require a personal OpenBao login. Operations' default setup
does not install or restart monorepo services.
Refactor has its own installer. See [the monorepo's setup entrypoints](https://github.com/SaltyPatron/Laplace/blob/main/deploy/README.md).
Runtime checks do not establish complete installation of all three implementations.
See [installation configuration and receipts](../installation/README.md#default-setup-and-runtime-identity-installation).

For human pgAdmin administration from Windows, use the installed
[Windows operator access](operator-database-access.md). The declared Linux
instances use the operator's Windows private-key store.
The PostgreSQL operator roles require no password. Service AppRoles and browser
login credentials are not used for these connections.

See the [installation map](installation-map.md) for the current repo/environment layout and the
different CLI implementations. These lifecycle controls are not a globally installed ingestion CLI.

Run these from this Operations checkout on HART-DESKTOP, using your existing GitHub CLI login:

```powershell
./laplace.ps1 status -Target production -Wait
./laplace.ps1 verify -Target staging -Wait
./laplace.ps1 verify -Target production -Wait
./laplace.ps1 prepare -Target desktop
./laplace.ps1 build -Target desktop
./laplace.ps1 deploy -Target staging -Wait
./laplace.ps1 deploy -Target production -Wait
./laplace.ps1 recovery -Target production
```

`staging` selects hart-server; `production` selects hart-prod; `cloud` selects hart-cloud when it is running.
`status` inspects installed revisions, configuration and connectivity; `runs` lists workflow history. `verify` executes the installed application. With `-Wait`, status and verification receipts are downloaded under `$LAPLACE_WORK/operations/<run-id>`.
`deploy -Target staging` builds and runs `main` on hart-server and stops there. This is also the default for `deploy`.
`deploy -Target production` verifies staging, transfers that package to hart-prod, publishes and verifies it.
Normal main delivery does not start hart-cloud or change the selected substrate backend. The monorepo's
`product-operator.yml` exposes `qualify-cloud` for explicitly requested isolated qualification; its lease is
released afterward so the existing idle-stop mechanism can stop the VM. `prepare`, `build` and `test` select desktop by
default and reject remote targets. HART-DESKTOP remains the development and optional GPU machine.

Desktop `build` and `deploy` use the same application component builder and immutable artifacts.
API, CLI, UCI, migrations and web have independent input/output receipts; the managed components
derive their source dependencies from the actual `ProjectReference` graph. CMake checks the native
graph once, and unchanged managed components skip `dotnet publish`. Unchanged compositions reuse
the complete verified package without copying its files. `build` selects that package for development;
`deploy` activates it in IIS and verifies authenticated SQL/native behavior. `start` consumes the
development package, and repeated `start`/`verify` reuse its owned process.

```powershell
laplace-ops deploy desktop -Components web -Plan
laplace-ops deploy desktop -Components web
laplace-ops deploy desktop -Components api,cli
laplace-ops deploy desktop -Components modular
laplace-ops deploy desktop -Components uci -Force
laplace-ops deploy desktop -Package 'E:\path\to\verified-package'
```

The default `all` selects both implementation stacks. API selection includes its generated web
contract; native/PostgreSQL selection includes the application consumers that must match its ABI.
Web-only delivery does not build or install PostgreSQL extensions, run migrations, or package MCP.
Modular-only delivery does not require or publish IIS. `-Force` explicitly rebuilds the selected
closure; normal commands reuse matching artifacts. `prepare` remains the explicit acquisition step.
The shared local artifact store deduplicates identical runtime, grammar and cache files; immutable
package hardlinks have independent lifetimes and never point through another release directory.
Receipts record the selected components and their individual build/reuse decisions.
`-Package` activates an already composed, hash-verified application closure without
requiring a compiler toolchain, rebuilding, installing extensions or running migrations.
Database migration remains a separate operator action when a package requires it.

Windows grammar generation is a declared external dependency. `./setup.ps1 tree-sitter`
builds the CLI from the same pinned checkout as the Engine's Tree-sitter runtime;
`./setup.ps1 tree-sitter -Check` verifies the installed binary against its receipt.
Both `deps` and desktop `prepare` also provision it. The Rust compiler, standard
library and Cargo are checksum-pinned in `toolchain/rust.lock.json` and installed
under `$LAPLACE_DEPS/rust/<version>`. The generator goes under
`$LAPLACE_DEPS/tree-sitter-cli/<version>/bin`; the developer shell adds it to the
current process's PATH. Cargo downloads and build outputs stay under
`$LAPLACE_BUILD/deps`. No Rust installation or configuration is written to the
operator's profile. The build verifies generation, ICX compilation and parsing
before recording success. For an offline build using already cached archives
and crates, invoke `installation/build-tree-sitter.ps1 -Offline`.

Workflow operations return a GitHub run link. `-Wait` follows that run and returns failure if it fails. The GitHub
**Product — maintenance** workflow offers the same controls. `-Revision` selects a published ref; local uncommitted
changes are not uploaded by this command. No repository or build directory is mounted on a deployment target.

`recovery` is an administrator SSH operation using the existing host key. It verifies the newest declared application
backup's SHA-256, restores into a uniquely named disposable database, and runs the installed API on a separate loopback
port with background provider/bootstrap services disabled. It tests authenticated SQL and native operations using the
restored application state, then removes its temporary database, process and credential file. Its JSON receipt is saved
under `$LAPLACE_WORK/operations`. `backup/recovery-installation.json` declares paths, identities and the port. This proves
application-data recovery with the selected substrate still available; substrate and OpenBao recovery are separate checks.

The installed-runtime check requires API/web responses, MCP authentication when installed, authenticated SQL
execution, native decomposition/storage invariants, compatible loaded Tier-0 artifacts, and the configured Stockfish
executable's UCI/search behavior. An empty substrate database is reported separately from failed infrastructure.
The verifier issues a temporary key in the migration-provisioned verification workspace and revokes it afterward.

On a declared Linux host, from the matching Laplace source checkout:

```sh
bash deploy/linux/site.sh smoke
bash deploy/linux/site.sh configure restart smoke
```

Linux uses `/etc/laplace/machine.env`; `LAPLACE_MACHINE_ENV` selects another declaration. Existing nonempty process
values take precedence, including when later declarations reference them. Files contain assignments, optional
`export`, comments, quoted values and quoted multiline values; `$NAME`, `${NAME}` and `%NAME%` resolve previously
declared or process values. Files are read as data: command substitutions and backticks never execute. Duplicate,
malformed, unreadable or explicitly missing declarations stop the operation. Operations' shell entry points and the
application/site installer use the same reader contract; `LAPLACE_CONFIG_SOURCE` records the selected file.

The first command verifies the installed site. The second regenerates its declared runtime configuration and
restarts it. Shared host locks prevent these operations from racing deployment or ingestion.
The component delivery workflow waits for another repository's host operation for up to 3,600 seconds; the
repository variable `LAPLACE_HOST_LOCK_WAIT_SECONDS` configures this deadline. Operations shell commands accept
the same variable and default to zero (immediate refusal). A timeout fails before shared-runtime changes.

Install API operator and existing OAuth provider credentials from OpenBao on an SSH-accessible target:

```powershell
./secrets/configure-site.ps1 -HostName hart-server -InstallPrefix /opt/laplace
```

This uses the existing authenticated Bao session. Values travel over stdin and are not printed. An operator credential
is created once under `kv/hosts/<host>/laplace-api`; provider credentials come from `kv/shared/laplace-auth`.
Conflicting installed credentials stop the operation instead of silently rotating them. Restart the service after
a reported change. This bootstrap does not replace the host's AppRole or establish credential-refresh automation.

The production API's OS and application database identities are declared in
`secrets/application-runtime-installation.json`. Provision and verify its data-only credentials, then activate with:

```powershell
./secrets/application-runtime.ps1 -Phase prepare -Target production
./secrets/application-runtime.ps1 -Phase activate -Target production
./secrets/application-runtime.ps1 -Phase verify -Target production
```

`verify` executes `Laplace/deploy/linux/runtime/application-runtime.py` in memory with `--stdout-only`. It transfers no installer files and creates no remote scratch. Run `laplace-ops test -Check production-runtime-identity` to retain the result in the local bounded acceptance history.

Preparation does not switch the serving process. Activation writes the declared runtime connection, moves writable
API state to its private service home, and restarts under the separate OS account. It runs the installed application
verifier and restores the prior configuration/service identity on failure. Migration credentials stay with the
deployment account; the API's pgpass contains only its two runtime credentials. Preparation enrolls a separate
OpenBao AppRole that can read only the two declared runtime records. Its root-only credential is selected by
`LAPLACE_BAO_RUNTIME_CREDENTIALS`; the existing host AppRole remains available for deployment. Verification exercises
both allowed reads, denies migration/shared credentials, and proves the token stops working after revocation.
The refresh reads selected substrate and `LAPLACE_BAO_APP_RUNTIME_RECORD`; `setup.sh database-client` installs
that timer for `LAPLACE_API_USER`. Changed credentials are authenticated before publication and trigger verified
pool recreation. The two-connection application pool and six-connection role allocation include a concurrent
recovery process and credential checks; these are not an aggregate substrate-cluster resource budget.

Apply the declared application-cluster resource budget with `./secrets/application-runtime.ps1 -Phase resources`.
The installer checks the actual database directory, holds the host operation lock, validates the plan before database
changes, and restores the previous PostgreSQL configuration if tuning or application verification fails. A successful
apply includes the required database restart and authenticated application verification. Repair repeats the same
operation. Application tuning failures now fail setup instead of being printed as a successful installation.
Use `-Phase resources-check` for readback without changing the database or restarting it.

The production declaration allocates eight application client connections: two serving, two recovery, and one each
for credential refresh, backup, migration and operator inspection. PostgreSQL's maintenance/reserved allocation
brings its connection setting to fourteen. A 1 GB reservation leaves room for other host processes; a 256 MB shared
buffer ceiling avoids allocating a quarter of this host to its currently small application database. These are
explicit initial allocations, not measured throughput guarantees. Substrate runs on a different database host.

`LAPLACE_PG_WORK_NODES` estimates simultaneous sort/hash nodes per backend (default two); the planner charges each
against `work_mem` with its declared hash multiplier of one. Increasing the estimate reduces per-node memory, and
plans that exceed the private-memory allocation at minimum settings are refused. This is not an arbitrary-query
memory cap. [PostgreSQL documents the per-operation and parallel-worker multipliers](https://www.postgresql.org/docs/current/runtime-config-resource.html).
The application WAL profile retains `replica` for recovery/base-backup compatibility; this does not itself enable
WAL archiving or prove point-in-time recovery. Application overrides use `LAPLACE_APP_PG_*` in machine.env so they
do not silently change a co-located substrate cluster's plan.

Register an existing Stockfish build using its actual selected source path:

```sh
python3 scripts/install-stockfish.py --configure --source-dir "$LAPLACE_STOCKFISH_SOURCE" --prefix "$LAPLACE_INSTALL_PREFIX"
```

The command validates the official pinned checkout and executes a legal search before saving its paths. It preserves
unrelated service settings and leaves the checkout in place.

Hart-prod is the inexpensive always-on web host. Its substrate database connection can fail over from
hart-cloud to hart-server when hart-cloud is stopped or unavailable. Hart-prod also has its own PostgreSQL
for local fallback, in addition to its billing, account and other application data. A selected hart-server
connection is a failover state; it does not change the hosts' development, staging and production roles.
Inspect the selected target before a database reset, including whether it currently serves production.
`secrets/provision-database.ps1` creates the non-superuser substrate login and the consumer's OpenBao record;
`sudo ./setup.sh database-client` installs the existing host AppRole's credential refresh timer. Selecting a new
database source is explicit; the timer only refreshes the selected credential. It never moves account/session data.

Selection checks the installed Tier-0 receipt before writing configuration. Use the installed helper with
`--select --verification-base https://api.hartonomous.com` and its existing host/AppRole arguments to activate
the selected substrate credential. It verifies authenticated application work afterward and restores the prior
credential and configuration if activation fails. Changing substrate contents does not imply a stale replica.

After the cloud lease has ended and hart-cloud is stopped, verify continued public API/MCP operation with:

```powershell
./acceptance/verify.ps1 -Check cloud-off-serving -Output "$env:LAPLACE_WORK/operations/cloud-off-$(Get-Date -Format yyyyMMdd-HHmmss).json"
```

The acceptance registry declares the installation's actual control host, cloud project, serving host and public URLs.
The check verifies cloud state both before and after execution; it does not start or stop the VM.

When MCP runs on the database host, declare `LAPLACE_MCP_UPSTREAM` in the consumer's machine.env and run the
site host installer. Distribute the existing MCP credential with:

```powershell
./secrets/configure-site.ps1 -HostName hart-prod -InstallPrefix /opt/laplace -UseSudo -McpTokenSource kv/hosts/hart-server/laplace-api
./network/cloudflare-api.ps1 -Zone hartonomous.com -ApiHosts api.hartonomous.com,mcp.hartonomous.com
```

The Cloudflare command checks the host-specific API rule; `-Apply` converges it. Browser Integrity Check was returning
403/error 1010 for legitimate Python clients before they reached Laplace. The rule disables that browser heuristic
only on the two programmatic service hosts, preserving application authentication and other security rules.
[Cloudflare documents this setting for API traffic](https://developers.cloudflare.com/waf/tools/browser-integrity-check/).
The nginx template preserves HTTPS from the trusted local tunnel and the public host header, so OAuth callback URLs
have the correct public origin. [ASP.NET proxy guidance](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/proxy-load-balancer?view=aspnetcore-10.0)
explains why forwarded scheme and host affect redirects.

Repository administrators can read back the declared public-runner approval policy with
`./github/runner-policy.ps1`, or converge it with `-Apply`. It requires approval for every external fork's workflow,
including returning contributors. The saved receipt includes previous and current settings.
[GitHub documents the repository policy API](https://docs.github.com/en/rest/actions/permissions#set-fork-pr-contributor-approval-permissions-for-a-repository).
This does not isolate an approved workflow from a persistent runner's filesystem or network. Privileged promotion
and untrusted builds still need separate execution contexts, as described in
[GitHub's self-hosted runner guidance](https://docs.github.com/en/actions/reference/security/secure-use).

For development on HART-DESKTOP, use the same entry point:

```powershell
./laplace.ps1 prepare
./laplace.ps1 build
./laplace.ps1 test
./laplace.ps1 configure-development
./laplace.ps1 start -Target desktop
./laplace.ps1 status -Target desktop
./laplace.ps1 logs -Target desktop
./laplace.ps1 stop -Target desktop
./laplace.ps1 verify -Target desktop
```

`configure-development` applies `development/installation.json`. HART-DESKTOP selects its local custom PostgreSQL
installation, `laplace-mono` substrate and separate `laplace-desktop-app` database. The declared Windows developer
and IIS account authenticate through SSPI to distinct restricted roles; no database password or human Bao login
is needed. The application schema has a non-login owner, and its runtime role has no DDL or administrator access.
Remote SCRAM declarations retain the existing OpenBao credential contract. See [operator access](operator-database-access.md)
for pgAdmin's local SSPI and remote Windows-certificate connections.

The existing `laplace-hart-desktop-development` workload enrollment supplies the API identity and shared OAuth
record. Local SSPI runs do not fetch the two remote database-password records. Subsequent starts use the enrolled
workload role and revoke the short-lived Bao session; operator token expiry does not prevent a restart. Initial
enrollment on an unconfigured machine is the separate `enroll-development` operation. The workload cannot modify
the records or read another host's credentials. This follows
[OpenBao's application authentication contract](https://openbao.org/docs/auth/approle/).

The enrollment is encrypted with [Windows user-bound DPAPI](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/convertfrom-securestring)
under `%LOCALAPPDATA%/Laplace/credentials/<client>.json`, with access limited to the current Windows user and SYSTEM.
`LAPLACE_DEVELOPMENT_CREDENTIALS` selects an absolute alternate file. It contains the encrypted AppRole enrollment,
not a cached administrator token; do not copy it to another user or computer. Enrollment preserves an existing
file. Its SecretID remains valid until explicitly revoked, while each issued token lasts at most ten minutes.
`development/verify-enrollment.ps1` tests the actual read/deny/revocation boundaries without operator credentials.

`start` starts the application in the background and returns after SQL/native/application verification.
Repeated `start` reports the existing instance. `status` shows its address, source revision, process and log directory;
`logs` prints recent application output. `stop` requests shutdown through the launcher after checking the recorded
process start time and application path. It does not stop another process that happens to use the selected port.
The workload enrollment makes these commands independent of an operator Bao login. No administrator session is needed.

`run` provides the foreground alternative: it verifies the SQL/native/application path, then serves the built web application
and API at `http://localhost:5187` until Ctrl+C. Native artifacts, source and
build paths come from the existing machine configuration. It starts the normal application background services and
loads the existing sign-in provider configuration from the declared OpenBao identity reference. OAuth callback
registration must allow this local origin; an authorization redirect alone does not prove interactive sign-in.
The Google redirect URI for the direct development process is `http://localhost:5187/signin-google`.
This process is separate from the installed IIS site. `verify -Target desktop` reuses an owned running process,
preserving its PID and browser session; when stopped it starts and stops a temporary verification process.
It does not establish that IIS works. The `browser-routes` acceptance check exercises the declared browser origins
in `network/environments.json`, including TLS and the callbacks emitted through IIS/nginx.
[Google requires the callback to match the OAuth client's registered URI](https://developers.google.com/identity/protocols/oauth2/web-server).
[Microsoft documents its localhost callback rules](https://learn.microsoft.com/en-us/entra/identity-platform/reply-url).
`verify -Target desktop` exercises the owned running instance, or starts and stops a temporary instance if none is running.
Use `start` or `run` for ongoing browser use. Run `build` after source
changes. `LAPLACE_API_PORT` selects a different loopback port. `LAPLACE_DEVELOPMENT_INSTALLATION` selects another
development declaration for both configuration and run; declared database pool sizes are per datasource.

`./setup.ps1` prepares this development profile by default. `./setup.ps1 deps` installs dependencies from the
toolchain manifest; `./setup.ps1 all` explicitly includes a local PostgreSQL server and its service/access setup.
Use the default profile for HART-DESKTOP and hart-server for deployment verification.

The source defaults to `LAPLACE_SRC/Laplace`; `-SourcePath <checkout>` selects a worktree. Preparation fetches the
exact grammar commits required by that source and the numbered Unicode release with checked SHA-256 inputs.
Build compiles the CPU native libraries, prepared artifacts, managed solution and web application, then executes
native interop, decomposition and round-trip tests. These commands do not start a GPU service or install a local
PostgreSQL server. Every build/test writes a result under `LAPLACE_WORK/operations`, including failures.

Windows machine settings live in `%ProgramData%/Laplace/machine.env`. `LAPLACE_SRC` contains checkouts;
`LAPLACE_DEPSRC` contains dependency source; `LAPLACE_DEPS` contains versioned installed dependencies;
`LAPLACE_BUILD` contains generated build trees; `LAPLACE_WORK` contains operation receipts and logs.
The normal `LAPLACE_SRC/Laplace` checkout defaults to `LAPLACE_BUILD/Laplace`, consistently in
Operations, PowerShell and MSBuild. An explicitly selected alternate checkout retains an isolated
`LAPLACE_BUILD/worktrees/<checkout-name>-<path-hash>` directory. `LAPLACE_BUILD_ROOT` remains an explicit override.
The installed dependency manifest is copied by preparation and supplies the versioned prefixes used by CMake.
Neither a Windows service account nor a guessed password is used as a database login.

The MSBuild values are resolved during project evaluation, so IDE builds use the same directories as scripted builds.
[Microsoft documents why these output properties must be set before their consumers](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory).
The workspace identifier uses the same SHA-256 function in PowerShell and
[MSBuild's stable hashing implementation](https://github.com/dotnet/msbuild/blob/main/src/Build/Evaluation/IntrinsicFunctions.cs).

The LAN resolver uses the router's `.lan` records through AdGuard. Check or converge the cloud/hosting names from
their actual Tailscale node addresses with:

```powershell
./network/openwrt-private-dns.ps1 -Router hart-router -TailnetHost hart-server -Nodes hart-prod,hart-cloud -LocalDomain lan
# Add -Apply to converge the records, retain the prior DHCP configuration, and verify the result.
```

This supplies `hart-prod.lan` and `hart-cloud.lan` to the existing LAN DNS path. It does not power on the cloud VM.
The router already routes Tailscale's address range through hart-server. A Tailscale client can separately resolve its
fully qualified MagicDNS names using the local Quad100 resolver even with automatic DNS configuration disabled,
as described in [Tailscale's DNS guidance](https://tailscale.com/docs/reference/faq/dns-resolv-conf).
The updater uses OpenWrt's supported domain records, verified against its
[24.10.2 dnsmasq implementation](https://github.com/openwrt/openwrt/blob/v24.10.2/package/network/services/dnsmasq/files/dnsmasq.init).
