# Credential agents and log protection

Windows services authenticate with their own OpenBao AppRoles. A person's `bao login`
does not refresh these identities. Their owning application installers declare the
KV records, AppRole policy, rendering and service installation. Operations maintains
the explicitly declared shared OpenBao executable and server protections.

On HART-DESKTOP, administrator PowerShell:

```powershell
& .\setup.ps1 secrets-agents
```

`installation/hart-desktop-secrets-agents.json` selects the executable by version and
SHA256 and names both installed services. Setup checks service commands and identities,
preserves enrollment, replaces the agent executable, and requires a newly authenticated
render. It does not use the operator's Bao login. A failed update remains failed in its
receipt; the defective executable is not automatically restarted. `-Check` performs
only the unprivileged host/binary/service metadata preflight.

On hart-server:

```bash
sudo ./setup.sh secrets-recover
sudo ./setup.sh secrets-protection
```

After a reboot the existing Shamir-sealed OpenBao cannot authenticate users or
agents until its threshold shares are supplied.

On this installation, the October 9 import record places the shares in
`https://vault.hartonomous.com`, folder **Infrastructure**, secure note
**OpenBao unseal keys + init (hart-server, 2026-10-09)**. Its reported readback matched
the original before the plaintext `~/.config/shell/openbao-init-20261009.json` was
shredded. The earlier `/root` copy had already been removed. Local escrow discovery
alone therefore cannot recover this installation. This historical receipt does not
replace verification that the user can currently decrypt the note.

Unlock that note through the existing Vaultwarden account, then run the following
command three times, supplying a different `unseal_keys_b64` share at each hidden
prompt. No sudo or OpenBao login is required. Keep shares out of command arguments,
logs and chat; there is no need to export another plaintext file.

```bash
bao operator unseal
```

Then `sudo ./setup.sh secrets-recover` verifies HTTPS recovery without reading
escrow because Bao is already unsealed. Ordinary setup also follows that path.

For installations retaining an existing local escrow, `secrets-recover` repairs nginx
startup and submits shares from the existing, root-only `/root/openbao-init-*.json`
escrow when exactly one such file exists. It never initializes storage, reads the
root token, replaces authentication, or installs unattended unseal. Keys travel
through stdin to the loopback endpoint, never command arguments or output. If
escrow was moved offline, use `bao operator unseal` with the offline shares; no
replacement keys can decrypt the existing store. Multiple escrow files require
explicit selection with `--unseal-file PATH`. `--check` is read-only.

Ordinary setup performs this recovery before the protection burst check. A sealed
Bao returns HTTP 503 even for unauthenticated renewals; that is a readiness failure,
not evidence that the nginx limiter failed. Protections still require observed
HTTP 403/429 boundaries and healthy HTTPS after recovery. Recovery refuses missing
or insecure escrow without changing initialization, data or identities.

`secrets/protection.json` declares paths and limits. Nginx permits 10 requests/second
per client (burst 30), 1 self-renewal/second per client (burst 10), and 40 requests/second
overall (burst 80). Excess receives HTTP 429 and Retry-After before reaching OpenBao.
These are secrets API limits, not ingestion or application throughput limits. Client
identity for this limit is the actual network peer; requests behind one NAT share it.
Increase the declared values if the installed workload count needs it, based on measured
traffic. The installer exercises a short unauthenticated burst against the real route
and verifies healthy HTTPS afterward.

Audit rotation checks run every minute, at 64 MiB with 16 rotations. Nginx retains its
existing daily policy with an added 32 MiB size threshold and the same minute checks.
Size thresholds can overshoot between checks; they are not filesystem quotas. Audit
rotation signals OpenBao to reopen the file, without copytruncate or discarding records.
The flood incident log is disposable; it is not application data or a required backup.

To discard the closed incident log and the abandoned archive attempt:

```bash
sudo ./setup.sh secrets-protection --discard-flood-log
```

Setup verifies that OpenBao holds the new active audit file and has released the old
file before removing the closed incident log and its matching complete/partial archive.
It creates no backup. It never truncates the active audit log or changes OpenBao data,
policies or initialization. Interrupted setup records failure. The cleanup is repeatable.

Secrets-stack installation includes these controls. After first installation, ordinary
setup reruns reconcile `/etc/laplace/secrets-protection.json` as well. Receipts under the
declared work/log directory distinguish preflight, started, failed and passed results.

The 2026-10-12 incident combined a missing `auth/token/renew-self` permission in the
monorepo IIS enrollment with an OpenBao 2.7.0 retry bug and missing server controls.
The [2.7.0 lifetime watcher](https://github.com/openbao/openbao/blob/v2.7.0/api/lifetime_watcher.go)
left retry sleep at zero; [2.7.1](https://github.com/openbao/openbao/blob/v2.7.1/api/lifetime_watcher.go)
uses the calculated backoff. [OpenBao file auditing](https://openbao.org/docs/audit/file/)
requires external rotation. [Nginx request limiting](https://nginx.org/en/docs/http/ngx_http_limit_req_module.html)
provides the server boundary independently of client behavior.
