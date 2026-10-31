# Laplace Workspace

This workspace (`E:\Repositories\Laplace`) contains the Laplace repositories, operational tooling, and documentation.

## Repository Map

| Family / Repo | Path | Role & Ownership | Status |
|---|---|---|---|
| **`laplace-mono`** | [Laplace](../Laplace/README.md) | Full-stack monorepo: ASP.NET Core API (`app/`), React/Vite web UI (`web/`), C/C++ engine & PostgreSQL extension (`engine/`, `extension/`), SQL migrations (`db/`), and Windows/Linux deployment (`deploy/`). | **Active** |
| **`laplace` modular** | [Laplace-Native](../Laplace-Native/README.md), [Laplace-postgres](../Laplace-postgres/README.md), [Laplace-Engine](../Laplace-Engine/README.md), [Laplace-MCP](../Laplace-MCP/README.md), [Laplace-UCI](../Laplace-UCI/README.md) | Modular native C/C++ substrate (`laplace_native`), PostgreSQL 18.6 extension (`laplace`), Engine CLI (`laplace`), MCP server (`laplace-modular-mcp`), and UCI adapter. | **Active** |
| **Operations** | [Laplace-Operations](../Laplace-Operations/README.md) | Multi-host provisioning (`setup.sh` / `setup.ps1`), PostgreSQL tuning (`tune-pg.*`), client packaging, and operational control (`laplace.ps1`). | **Active** |
| **Documentation** | [Laplace-Wiki](Laplace-Wiki/README.md) | Canonical Laplace documentation and specification wiki. | **Active** |
| **Conventional** | [Laplace-Conventional](../Laplace-Conventional/README.md) | Python/GPU tooling for conventional model comparison and probing. | **Active** |
| **Historical Reference** | [Laplace-Refactor](../Laplace-Refactor/README.md) | Frozen reference repository retained strictly for **recipe-driven ingestion**, typed recipe compilation, and source-admission design context. | **Frozen (Read-Only)** |

## Quick Reference

From any normal (non-elevated) terminal:

```powershell
# Build, run, and test from source
laplace-ops prepare
laplace-ops build
laplace-ops test
laplace-ops start | status | logs | stop | verify

# Deploy & update local IIS installation + databases
laplace-ops deploy -Target desktop
laplace-ops restart-iis

# Database lifecycle (status, migrate, repair after drop, or recreate)
laplace-ops db -Database both -DatabaseOperation status
laplace-ops db -Database substrate -DatabaseOperation repair
laplace-ops db -Database substrate -DatabaseOperation recreate -Yes
laplace-ops db -Database application -DatabaseOperation recreate -Yes

# Monorepo CLI
laplace-mono --where
laplace-mono status
laplace-mono ingest unicode
laplace-mono ingest document <path>

# Modular CLI
laplace --where
laplace status
```

See [Laplace/README.md](../Laplace/README.md), [AGENTS.md](AGENTS.md.txt), and [Laplace-Operations/docs/operating-laplace.md](../Laplace-Operations/docs/operating-laplace.md) for full architecture, host topology, and deployment workflows.

