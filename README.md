# Laplace-Wiki

<p align="center"><img src="assets/laplace-logo.webp" alt="Laplace" width="640"></p>

This repository is the Laplace documentation. It explains how everything at every level works.

Read it online at <https://saltypatron.github.io/Laplace-Wiki/>.

Every page in this repository is listed below. Read every listed page in full.

## Pages

- [Architecture](Architecture.md) — Laplace is native C, with SQL and C# as orchestration.
- [Storage](Storage/README.md) — Laplace stores all digital content as a self-deduplicating Merkle DAG with deterministic, lossless storage, laid out as geometry in four dimensions.
  - [Space](Storage/Space.md) — Laplace places everything in an S³ "ball in a box", with Unicode projected across its surface and compositions forming inside it.
  - [Atoms](Storage/Atoms.md) — codepoints are tier 0, the absolute floor: every Unicode codepoint has a deterministic ID and a deterministic coordinate on the S³.
  - [Compositions](Storage/Compositions.md) — a composition is an n-ary, recursive sequence of constituents, each of which is a codepoint or another composition.
  - [Identity](Storage/Identity.md) — every node's ID is the BLAKE3 hash of its constituents, so the same content always has the same ID.
  - [Physicality](Storage/Physicality.md) — every composition has a full, real 4D coordinate, and its content is stored as a trajectory.
  - [Ingestion](Storage/Ingestion.md) — ingestion computes content's IDs on the client and deduplicates it trunk to leaf against what is already recorded.
- [Query](Query.md) — Laplace finds content by computing its ID and coordinates on the client and looking them up with spatial indexes.
- [Spitball](Spitball.md) — text that has not been properly considered for the documentation as a whole.
