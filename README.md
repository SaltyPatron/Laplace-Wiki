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
- [Research](Research/README.md) — research collects the sourced findings and measured results that support the Laplace specification.
  - [Prototype](Research/Prototype.md) — a working prototype of the storage layer was built from the specification and tested against 195 Project Gutenberg texts, and every number on this page was measured on it.
  - [Placement](Research/Placement.md) — Codepoints are placed on the S³ by taking Marc Alexa's Super-Fibonacci points for n = 1,114,112 in the order of their 4D Hilbert value and giving DUCET rank *r* the *r*-th point, which puts collation neighbors next to each other in space.
  - [Sampling](Research/Sampling.md) — Super-Fibonacci spirals give a fixed-size, evenly spread set of points on the S³, and this page records their construction, their relation to the Hopf fibration and to incremental grids, radical-inverse ordering, and local numeric checks.
  - [Unicode](Research/Unicode.md) — Laplace's tier 0 and its segmentation rest on the Unicode data, and this page records what that data defines, what it covers, and which parts of it are stable across versions.
  - [Hashing](Research/Hashing.md) — Research on how BLAKE3, Merkle trees and DAGs, hash-consing, and IEEE-754 bit packing behave under the Laplace identity scheme.
  - [Geometry](Research/Geometry.md) — Research on how PostgreSQL and PostGIS store, index, and compute on four-dimensional geometry, and on the 4D distance, centroid, and curve tools that Laplace builds on them.
  - [Numerics](Research/Numerics.md) — Research on the floating-point limits of Laplace's coordinates and ID points, the cost of colliding its IDs, and how trajectory distance measures treat noise and repetition.
  - [Corpus Search](Research/Corpus-Search.md) — Laplace's Merkle DAG is a grammar-compressed corpus, so exact occurrence counts, distinct-document counts, and phrase search inside containers all have direct precedent in the literature on grammar-compressed and suffix-based text indexes.
  - [Prior Art](Research/Prior-Art.md) — Each mechanism in Laplace's storage layer has published precedent, and the research found no prior system that combines them.
  - [Relations Research](Research/Relations.md) — Research into rating models, evidence counts, search over rated relations, truth discovery, and provenance is groundwork for the future Relations layer, which is not yet specified.
- [Spitball](Spitball.md) — text that has not been properly considered for the documentation as a whole.
