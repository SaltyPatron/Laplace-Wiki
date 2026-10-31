# Installation acceptance

The [parent issue](https://github.com/SaltyPatron/Laplace-Operations/issues/2) tracks delivery. `criteria.json` owns the
versioned operational outcomes, responsible repositories, dependencies, required evidence and executable check mapping.
The [audit](../docs/2026-10-10-system-audit.md#expanded-installation-delivery-and-resource-audit) explains why they exist.
These operational criteria do not replace Laplace's product specification.

`laplace-ops verify desktop -Installed` and the registered
`desktop-installed-runtime` check verify the serving IIS release without a build
or a second application process. `desktop-runtime` and `desktop-lifecycle`
separately exercise the source-run localhost application and require its build.
`desktop-browser-runtime` renders the two recorded entity/matchup cases in
installed Edge using real API responses, captures screenshots and request/error
evidence, and revokes its temporary verification key. No browser download is run.
API status and verification return their own result without appending client
inventory to JSON output. An older external MCP session does not change the API
check's result; `laplace-ops clients verify` reports its distinct nonzero result
when a reconnect or visibility repair is needed.

List the checks with `laplace-ops test -List`. Run selected checks with
`laplace-ops test -Check <id,...>`. This reuses the registry runner and records
the run under the declared `LAPLACE_WORK/operations/test-*/receipt.json` without
rebuilding or deploying components.

`production-runtime-identity` and `production-resource-settings` execute the
monorepo's canonical verifier in memory over SSH. Resource readback consumes
Operations' selected tuning rules through stdin and checks the existing service,
cluster and settings. Neither audit installs scripts or creates remote work.

The installed-runtime checks are `desktop-source-interpretation` (the selected
`laplace` binary, its packaged recipes and caches, and committed Native readback)
and `desktop-sql-foundation` (the installed `laplace-mono` database configuration
and extension). They use the existing PostgreSQL service and remove their own
verification databases. The runner owns their transient directories and removes
them on success, failure and timeout, retaining receipts and SQL logs separately.
They do not ingest into the operator's corpus.
Interrupted runs carry a scratch lease: `laplace-ops storage` reports it, and
`laplace-ops storage clean` retires it only after its owner and child processes
have exited. Unregistered directories are preserved.
Run every registered check with an explicit new evidence destination:

```powershell
. ./laplace.env.ps1
pwsh -NoProfile -File acceptance/verify.ps1 -Output "$env:LAPLACE_WORK/acceptance/full-20261010.json"
```

This currently returns **2 (incomplete)**. Checks without implementations, checks for another operating system, and
checks not selected are named in the receipt. A missing executable, timeout or failed check cannot return success.
Exit 1 means a check failed. Exit 0 means only the selected checks passed; it does not accept the whole installation.
The receipt distinguishes those outcomes and includes source revision, dirty-worktree flags, registry digest, host,
UTC timestamps, exact commands, exit codes and output. Existing receipts are never overwritten.

For a bounded Windows verification:

```powershell
. ./laplace.env.ps1
pwsh -NoProfile -File acceptance/verify.ps1 -Check storage-windows,resource-refusal-windows,backup-copy-windows -Output "$env:LAPLACE_WORK/acceptance/windows-20261010.json"
```

CI runs the named implemented checks on Windows and Linux and uploads their JSON receipts even on failure. Its green
component jobs are not a green whole-installation acceptance result. Future live probes must identify the target,
installed release, substrate selection and workload identity without logging credentials. Live destructive operations
must not be smuggled into this default verifier; setup/recovery actions prepare the state, and verification reads it.

Work proceeds as: criterion -> failing check -> implementation -> passing check -> install/activate when applicable ->
live evidence -> tracker update. Do not check off a whole-host outcome using a narrower fixture. The two storage fixes
and refusal of planner-declared overcommit have executable regression evidence. Configuration convergence, coherent
release installation, cloud-off serving, identity, network/TLS, recovery and wire-budget criteria remain open.
