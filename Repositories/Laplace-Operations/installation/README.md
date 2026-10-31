# Existing host repair

The desktop modular browser has its own IIS publication declaration:
`hart-desktop-modular-web.json`. From an elevated desktop operator shell, run
`pwsh -File installation/Publish-ModularWeb.ps1` to build, activate and verify
`https://dev.hartonomous.com/modular/` without switching the mono release.
Receipts live under `E:/Data/Laplace/work/operations/modular-web`. The application
uses the installed same-origin identity service; its current substrate screens
are explicitly labelled captured data. See `Laplace-MCP/web/README.md`.

From the updated Operations checkout on hart-server:

```sh
./setup.sh repair --check
sudo ./setup.sh repair
```

`hart-server.json` declares this installation's observed paths and services. Another installation uses
`--installation /absolute/path/to/installation.json`. Preflight rejects the wrong host, missing mounts,
unavailable services and conflicting existing machine settings before changing configuration. It does not
create volumes or build mounts. Existing additional settings remain intact.

Repair acquires the deployment/ingestion host lock, installs the public `/etc/laplace/machine.env`, checks the
latest production application backup on the backup landing volume, restores it into a new private database,
reads its application tables, and removes that scratch database. It repairs the existing secrets backup job,
runs a checked backup, extracts the backed-up Vaultwarden SQLite database and performs an integrity check.
It does not stop serving databases, restart application services, change runtime identities or modify source
checkouts. When this host declares a modular runtime, repair also converges the listener credential that
`sudo ./setup.sh` installs: the token file is made once, the installed unit names that file, and root's
credential helper is installed. The listener process is left running; deployment's existing restart is what
loads the named file. Sudo is used for this installation operation; ordinary deployment and verification
remain unprivileged.

Every attempted repair after preflight saves a public, secret-free receipt under
`/var/lib/laplace/installation/receipts`. A failure returns nonzero and restores the previous machine declaration.
The secrets backup job may already have been repaired and new archives retained when a later check fails;
rerunning repair repeats its checks. A failed restore still removes its own newly created scratch database.

This proves landed database restoration and extracted SQLite integrity. It does not establish application
behavior on the restored database, a complete Vaultwarden recovery, OpenBao unseal/recovery, or runner/runtime
identity isolation. Those remain separate acceptance requirements. The database restore uses PostgreSQL's
[documented transactional restore options](https://www.postgresql.org/docs/18/app-pgrestore.html).

## Default setup and runtime identity installation

Operations configures shared infrastructure and the declared modular runtime:

```sh
sudo ./setup.sh
```

The monorepo's `sudo bash deploy/linux/site-host.sh`, run from its own checkout, owns API/MCP behavior,
database permissions, OpenBao boundaries and credential refresh. Operations `all` never invokes that setup.
A failed monorepo runtime stage fails its installer. A stopped API/MCP can be repaired as
long as the service units and application release are installed. A missing release fails explicitly; setup
does not build or ingest an application implicitly.

Runtime selection uses `LAPLACE_RUNTIME_MANIFEST` from the machine declaration (or process override), otherwise
`deploy/linux/runtime/<hostname>-runtime.json` in the monorepo checkout. Explicit paths must be absolute. The declaration is
validated against the actual host and effective machine configuration before provisioning. Conflicting database
names, ports or cluster paths fail. The declared local runtime uses its configured PostgreSQL cluster;
`LAPLACE_APP_DBNAME` alone does not request a second packaged cluster on that host. Hosts without a runtime
declaration receive infrastructure/modular setup only.

The old explicit stage forwards to the configured monorepo for compatibility:

```sh
./setup.sh runtime --check
sudo ./setup.sh runtime
```

The monorepo's `hart-server-runtime.json` declares the current hart-server installation; `--manifest /absolute/path.json` selects another
declaration. The preflight checks the actual machine, mounts, services and installed paths. A non-root
check reports `workload_authentication=requires_privileged_check` when the private enrollment exists;
it does not claim authentication was tested. A root check also authenticates the installed AppRole.
The privileged operation creates separate API and MCP OS accounts and restricted database roles, enrolls
an API AppRole with read-only access to two host runtime records, verifies authentication, and activates
the services. Existing Bao records must match the declared target; rerunning preserves their passwords
and the host's enrollment. Only first enrollment needs the operator's Bao login. Both repeated setup and
runtime refresh authenticate through the root-private AppRole. Rejected existing enrollment fails without
falling back to an operator token, rewriting policy or generating replacement credentials.

This step preserves application data in `laplace-mono.app` and pins its application connection separately
from substrate selection. It does not move application data to a separate physical database. MCP uses
local PostgreSQL peer authentication; the API uses distinct TLS application and substrate logins.
Mutable state is declared under `/hosting/laplace/runtime`; no build mount is created.

API readiness/native operations, database privilege refusals, Bao policy/refusal/revocation and an
authenticated MCP substrate-counts tool call must pass. Failed activation restores prior service
configuration and restarts the previous services. Prepared accounts, grants and Bao records remain for
retry. A subsequent credential-timer installation failure leaves the verified services running and marks
setup failed, so rerun the same operation. Secret-free receipts are saved alongside repair receipts.
Fixture/CI success and `--check` are not proof that privileged installation has run.

Modular setup repairs the installed package or resumes the last completed package whose installation
selection matches. It verifies artifact and dependency hashes before reuse, then checks the runtime
identity and candidate before changing services. `modular.py deploy` selects a new source revision;
it requires completed OS/service installation before building. Repeated setup does not implicitly
upgrade an installed modular release.

The modular listener takes a bearer token. `sudo ./setup.sh` with no arguments runs the whole installation,
including the modular runtime. That installation converges the token as declared state:
`LAPLACE_MCP_TOKEN` in `secrets/modular-mcp.env` beside the declared environment file (64 hex, root and
the deployment group, 0640), made once and never replaced. The unit names that file. A host installed
before the token existed gets the file and the unit line the next time setup runs. Recurring deployment
does not run as root and does not create the file. It asks the helper that setup installs, aimed at that
host's `installed_config`, the same way a PostgreSQL restart is asked, and waits until the file and the
unit line are in place. `lpm serve` refuses to listen without a token, and deployment verification reads
it through the deployment group. A caller sends `Authorization: Bearer <token>`.

Runtime setup also converges the declared local PostgreSQL certificate before changing service identities.
Its subject is distinct from the OS default server certificate, its SANs cover the declared database endpoints,
and both API connections and credential refresh use full certificate verification against
`tls.root_certificate`. The original private key is retained; replaced public certificates are backed up in
the receipt directory. Invalid certificate activation restores the previous certificate and trust file.
A successful certificate repair remains installed if a later identity step fails. The `valid_days` and
`renew_before_days` policy is evaluated when setup runs; automatic certificate renewal remains separate work.
Existing CA-issued certificates are refused rather than replaced by a local self-signed certificate.

If service activation fails, the receipt points to root-private diagnostics containing the verifier failure
and the API journal for that attempt. Password inputs and process environments are not logged. Public
receipts contain no diagnostic output. The root-private AppRole enrollment is long-lived and may issue five-minute tokens with
read access to the two named host runtime records. It is not a user authentication bypass or a secret-reading
HTTP endpoint. Existing serving identities remain unchanged until activation passes.

The TLS regression runs a disposable PostgreSQL cluster with the installed Npgsql assembly:
build `tests/runtime-db-probe/runtime-db-probe.csproj` with `-p:NpgsqlAssembly=/path/to/Npgsql.dll`, then run
`python3 tests/runtime-tls.py --pgbin /path/to/postgresql/bin --probe /path/to/runtime-db-probe.dll`.
It reproduces the same-name certificate collision, verifies the repaired connection with `VerifyFull`,
rejects the wrong CA, and checks key preservation, idempotence and failed-rotation rollback.
