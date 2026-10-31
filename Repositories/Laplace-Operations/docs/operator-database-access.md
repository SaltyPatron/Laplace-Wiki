# Windows operator access to Laplace databases

HART-DESKTOP is the isolated development environment. Its one custom PostgreSQL
18.6 installation is `D:/Libraries/postgresql/18.6`, service `laplace-postgres`,
data `E:/Data/Laplace/pgdata`, WAL `D:/Data/Laplace/pg_wal`. The service listens on
localhost and HART-DESKTOP's owned LAN/Tailscale addresses. The existing cluster
was activated in place without initdb or a data reset; its system identifier is
`7696004236835714020`. These directories now hold active development data.

The installed IIS application and `laplace-mono` development profile use local
`laplace-mono` and `laplace-desktop-app`, with distinct restricted runtime roles.
The installed modular `laplace` command uses local database `laplace` as the human
operator. Its Tier-0 and highway fingerprints match the installed Engine. Source,
builds, installed artifacts and database state remain in their declared locations.
Hart-server remains staging and an intentional production fallback; hart-prod
keeps its application/fallback databases. Hart-cloud remains off. Selecting local
development did not migrate, reset or delete any remote database.

The `HART-DESKTOP Laplace` pgAdmin registration authenticates the exact Windows
account `HART-DESKTOP\ahart` using SSPI, maps it to database administrator `ahart`,
and verifies the HART-DESKTOP server certificate. No PostgreSQL password is stored.
`windows-operator-access.ps1` maintains this mapping; `development/configure.ps1`
maps the declared developer and IIS virtual account to the two restricted runtime
roles. Windows administrator status alone does not create a PostgreSQL identity;
these explicit mappings implement the intended access.

For hart-server and hart-prod, the human operator connects from pgAdmin as `ahart`, using PostgreSQL
certificate authentication. The RSA private key is non-exportable in that Windows
user's Personal certificate store. PostgreSQL maps the certificate's exact subject,
which contains the enrolled Windows SID, to the operator role. No PostgreSQL password,
OpenBao token, password helper, or workload AppRole is used by these connections.
The database role is an administrator on both remote clusters.

`installation/hart-desktop-operator.json` declares the Windows identity, target
clusters, individual client addresses, public trust certificates, installed OpenSSL
engine and pgAdmin paths. The certificate is provisioned through existing operator
SSH/database administration; it does not turn an unverified email or arbitrary
Windows account into a PostgreSQL administrator. The monorepo's Google/Microsoft
browser identities and workload enrollments retain their separate responsibilities.

From the declared Windows account, run `installation/Install-OperatorAccess.ps1`
for enrollment or repair, then reopen pgAdmin. The installer verifies all three clusters
and the pgAdmin connection manager before reporting success. Its server setup holds
the existing host lock, backs up public authentication files, validates HBA/identity
maps, and reloads configuration without restarting PostgreSQL or applications.
Repeat installation preserves the key and does not reload an unchanged cluster.

pgAdmin uses native libpq service definitions because its file picker treats an
OpenSSL engine identifier as a filename. Its normal `config_local.py` scopes the
installed CryptoAPI engine and OpenSSL configuration to the desktop app. No pgAdmin
driver or authentication code is patched. The installed CryptoAPI engine supports
PKCS#1 SHA-2 signatures; these connections therefore use TLS 1.2, authenticated
ECDHE/AES-GCM encryption, and full server certificate verification. The private key
never becomes a PEM key file. The remote logins use Windows key ownership; the
local login uses Windows SSPI. Neither requires a browser OAuth exchange or a
personal OpenBao login.

Verify with `installation/Verify-OperatorAccess.ps1`. It checks Windows SID, key
export restrictions, certificate lifetime, password-free PostgreSQL roles, the exact
`system_user` authentication identity, and actual saved pgAdmin connections. It also
requires denial without a certificate, with a missing Windows key, and for a different
database role. The `desktop-operator-certificate` acceptance check records this evidence
under IDENTITY-001. `desktop-installed-databases` additionally verifies one custom
service, storage identity, every HART-DESKTOP DNS address, both installed clients
and IIS readiness. `desktop-runtime` verifies the separate source development API.
These checks do not close the wider identity criterion or
[the installation tracker](https://github.com/SaltyPatron/Laplace-Operations/issues/2).

The enrolled certificate expires after one year; verification fails with 30 days
remaining. Renewal requires replacing the public certificate trust through this
administrator enrollment, preserving the preceding certificate until the replacement
is verified. Automatic renewal is not installed. Revoke access immediately with
`ALTER ROLE ahart NOLOGIN` on each selected cluster; remove the corresponding trust
and Windows certificate during de-enrollment. Existing authenticated sessions require
explicit termination for immediate revocation. Installer receipts name the original
HBA/identity backup files; restoring them and the recorded prior `ssl_ca_file`, then
reloading, reverses enrollment without changing application credentials or data.

Live verification on HART-DESKTOP at 11:28 UTC on 2026-10-13 passed both
`desktop-operator-certificate` and `desktop-database-identities`. The receipt is
`E:/Data/Laplace/work/laplace-mono/operator-access/desktop-access-20261013T112836Z.json`.
The saved pgAdmin connections authenticated as `ahart` on HART-DESKTOP, hart-server
and hart-prod. Local unmapped-role and wrong-certificate-name denial checks passed;
all three certificate denial cases passed on both remote hosts. Repeated remote enrollment in
`enrollment-20261013T041504Z.json` reported `changed: false` for both clusters.
The enrolled certificate expires on 2027-10-12. Both deployed Operations setup
scripts preserve the operator HBA and identity-map includes. This evidence covers
operator access and the checked desktop workload boundaries, not whole-installation
acceptance.

At 05:02:12 UTC, the installed pgAdmin connection manager also opened `laplace`,
`laplace-desktop-app`, and `laplace-mono` on hart-server, and `laplace-app` on
hart-prod using the saved registrations. Every connection authenticated as `ahart`
with the enrolled Windows certificate, TLS enabled, administrator access, and no
saved password. The receipt is
`E:/Data/Laplace/work/laplace-mono/operator-access/pgadmin-laplace-databases-20261013T050212Z.json`.
This exercised pgAdmin's saved connection backend; GUI interaction was not verified.
