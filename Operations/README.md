# Operations

Operations covers what Laplace runs on and how it is built, configured, deployed, and tuned, from bare hardware to loaded, indexed, and measured content.

- [Setup](Setup.md): hardware, storage layout, repositories, and toolchain.
- [Builds](Builds.md): building PostgreSQL, Laplace-Native, and Laplace-postgres.
- [Database](Database.md): the PostgreSQL configuration Laplace needs, and why.
- [Deployment](Deployment.md): from an empty server to benchmarked content.

Measurements quoted on these pages come from [Engine Measurements](../Research/Engine.md), taken on a reference machine: a 6-core Intel Core i7-6850K with 125 GB of RAM, an NVMe drive for the database heap, and SATA SSDs for the write-ahead log and temporary files.

## Workspace and host roles

Laplace is one product across its active repositories. `Laplace-MCP` supersedes
the old `code-search` service; its repository and relocated documentation remain
historical references. `Laplace-Refactor` is a separate, lowest-priority workstream
unless explicitly selected. Preserve invention documents, specifications and
research when updating operational guidance.

HART-DESKTOP is the development machine, not a GitHub Actions runner host.
Development builds and tests may run locally. CI uses the existing designated
runner hosts; routine cleanup or deployment must not provision replacement
runners on the desktop.

Setup owns privileged prerequisites, users, permissions, packages, IIS topology,
service installation and host configuration. The existing setup scripts compare
the declared installation with the host and report missing prerequisites.
`laplace-ops deploy` selects the source state, builds or reuses its qualified
components, updates installed IIS applications, services and endpoints, applies
required migrations, and verifies the installed result. Ordinary redeployment
must not require a new privileged physical-path or account change.

Configured editor MCP clients use the deployed authenticated HTTP endpoints.
Local CLI and stdio modes remain available for explicit local use and testing;
they do not establish that the configured HTTP integration works. The native
and monorepo MCP catalogs are separate surfaces; see the
[native MCP client contract](../Repositories/Laplace-MCP/docs/API.md#deployed-clients).

## Completion evidence

Committed, pushed, CI-qualified and deployed revisions are distinct states.
Report which exact revision and artifact each check exercised, and verify the
complete requested workflow and its live readback before claiming completion.
Failed, cancelled, skipped, partial or unverifiable checks are not successful
qualification. Optional work that was not requested must not be presented as
executed evidence.

Preserve live clients and shared databases. A cleanup is not authorization to
reset, reseed, download bulk corpora/models over the desktop's metered connection,
or remove historical research. Close issues only against their actual acceptance
criteria; a passing deployment does not complete unrelated architecture work.
