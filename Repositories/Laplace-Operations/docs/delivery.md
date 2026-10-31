# Laplace delivery and host roles

Use [Operating Laplace](operating-laplace.md) for commands. The implemented application delivery is:

`HART-DESKTOP development → hart-server deployment and runtime verification → hart-cloud release build → hart-prod publication and runtime verification`.

| Host | Responsibility | What successful execution establishes |
| --- | --- | --- |
| HART-DESKTOP | Windows development, CPU-native/managed/web builds, optional GPU workloads | The selected checkout builds and its executed runtime tests pass. A GPU is not a core Laplace dependency. |
| hart-server | Independent local deployment target and selectable database host | The Linux installation, migrations, authentication, native calls and application reads work on another machine. Its damaged GPU is ineligible. |
| hart-cloud | On-demand Google Cloud compute for release builds, native AVX-512 testing and benchmarks | Only the checks actually executed by the selected job. The delivery job builds a bundle; it does not automatically establish every ISA or performance claim. |
| hart-prod | Public application hosting and local application database | The received bundle serves authenticated requests through public ingress against the selected compatible database source. |
| hart-router | LAN routing and DNS, including existing AdGuard configuration | Client-to-service probes must establish the actual route and resolution. Router reachability alone is not application readiness. |

Build host, serving host, deployment tier and selected database source are separate settings. hart-cloud is intentionally
stopped when unused. Production currently selects hart-server substrate while keeping accounts, sessions, API keys and
billing in its local application database. OpenBao and Vaultwarden remain on hart-server. Tailscale provides private
connectivity; it does not create database grants, synchronize substrate, or provide application failover by itself.

Substrate selection chooses an admitted substrate/artifact estate. It is not a replica-freshness test. Selection checks
the installed Tier-0 contract before changing configuration and verifies authenticated application work afterward.
The desktop and deployed Linux Tier-0 artifact now have identical bytes for the same pinned Unicode inputs and sources;
source line endings are normalized before computing the generator fingerprint.
[CMake documents the file and string hashing operations](https://cmake.org/cmake/help/latest/command/file.html).

## Delivery behavior

The monorepo's `laplace.yml` installs and verifies on hart-server, starts hart-cloud through existing GCP workload
identity federation, holds its lease while building/publishing, and releases the lease after hosting verification.
The existing idle-stop timer can then stop the VM. Publication receives the bundle built by that run. Runtime checks
include authenticated SQL execution, native decomposition/storage invariants, artifact compatibility and configured
external calculators. A missing optional Stockfish installation does not prevent CPU Laplace deployment.

Complete application promotions share one queue so different revisions cannot interleave prepared output or cloud
leases. Host jobs and explicit maintenance also queue. `queue: max` retains up to 100 pending operations instead of
replacing the previous pending request; the limit is finite.
[GitHub documents queuing and its limits](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).
GitHub concurrency is repository-scoped. The common host-resource file lock coordinates Operations and monorepo
processes that actually share installation/database resources.

The separate Native/Engine/Postgres deployment remains an active, distinct installation path. Operations resolves
immutable dependency commits before checkout and preserves a component dispatch's exact commit after checking that
it belongs to main history. Normal deployment does not drop databases or ingest content. Explicit ingestion has its
own operation. `./laplace.ps1 components -Target cloud -Wait` verifies staging, acquires an independent cloud
lease, starts the declared worker, and deploys the same component revisions there. Required compatibility checks
precede final SQL readback. Cleanup releases only that run's lease; the installed idle timer stops the worker after
all leases and active work end. This component path is separate from public application publication.

Cloud installation uses `cloud/configure-ci.ps1` to publish the declared project, worker, zone and identity variables.
`cloud/configure-identity.ps1 -Repository <owner/repository>` reads GitHub's actual OIDC subject format and binds only
the named branch (main by default). `-ControlHost` and `-Gcloud` select an existing authenticated control installation.
Newer repositories include immutable owner/repository IDs in their subjects; constructing an old name-only subject
would grant an identity the workflow never presents.
[GitHub documents the subject formats](https://docs.github.com/en/actions/reference/security/oidc).

## Resource and CPU configuration

A processor's instruction support, the compiler's target and runtime dispatch are different facts. Broadwell cannot
execute AVX-512 instructions. An AVX2-baseline bundle built on hart-cloud can run on hart-prod; a whole-build
Sapphire Rapids target cannot be assumed portable. Native dispatch tests and benchmarks must record which eligible
implementation actually ran and compare numerical results. Compilation alone does not prove this.

PostgreSQL tuning must use the database host's resources, alongside declared client pools and other resident services.
A local client's CPU count is not the capacity of a remote SQL server. The existing planners and live settings still
need whole-host reconciliation. `work_mem` applies to individual query operations and can be multiplied within a query;
it is not a complete per-connection memory bound.
[PostgreSQL's resource documentation explains these allocations](https://www.postgresql.org/docs/18/runtime-config-resource.html).

## Acceptance and recovery

The executable criteria and their evidence are in `acceptance/criteria.json` and [Operations #2](https://github.com/SaltyPatron/Laplace-Operations/issues/2).
A successful selected check does not mark unexecuted criteria complete. Cloud-off continuity has been executed through
public API and MCP while hart-cloud remained terminated. It proves that serving placement; it does not prove recovery
of lost application data or restoration of OpenBao.

Backup readability, a completed copy and a successful restore are different evidence. Recovery requires an isolated
restore and application reads against that restored state. Dedicated QA/load promotion jobs, a preview tenant/site,
full installer rollback, runner isolation and measured external round trips/bytes remain acceptance work; their names
do not represent environments or capabilities already installed.
