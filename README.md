# Laplace-Wiki

<p align="center"><img src="assets/laplace-logo.webp" alt="Laplace" width="640"></p>

This repository is the Laplace documentation. It explains how everything at every level works.

Read it online at <https://saltypatron.github.io/Laplace-Wiki/>.

Every page in this repository is listed below. Read every listed page in full.

## Pages

- [Architecture](Architecture.md) — Laplace is native C, with SQL and C# as orchestration.
- [Storage](Storage/README.md) — Laplace stores all digital content as a self-deduplicating Merkle DAG with deterministic, lossless storage, laid out as geometry in four dimensions.
  - [Space](Storage/Space.md) — Laplace places everything in a 4-ball inside a 4-cube, with Unicode projected across the 4-ball's surface, the S³, and compositions forming inside it.
  - [Atoms](Storage/Atoms.md) — codepoints are tier 0, the absolute floor: every Unicode codepoint has a deterministic ID and a deterministic coordinate on the S³.
  - [Compositions](Storage/Compositions.md) — a composition is an n-ary, recursive sequence of constituents, each of which is a codepoint or another composition.
  - [Identity](Storage/Identity.md) — every node's ID is the BLAKE3 hash of its constituents, so the same content always has the same ID.
  - [Physicality](Storage/Physicality.md) — every entity has a full, real 4D coordinate, and every composition's content is stored as a trajectory.
  - [Ingestion](Storage/Ingestion.md) — ingestion computes content's IDs on the client and deduplicates it trunk to leaf against what is already recorded.
- [Semantics](Semantics/README.md) — semantics are the relations Laplace records about entities, so that it can link concepts and languages and hop and fan out from anything to anything with integrity.
  - [Attestations](Semantics/Attestations.md) — curated corpora attest to entities, ordinary digital content is observed, and every attestation is a win, draw, or loss and/or a score from a witness.
  - [Claims](Semantics/Claims.md) — a claim is a tuple of entities with referential integrity, and its ID is computed from its components the same way a composition's is.
  - [Consensus](Semantics/Consensus.md) — everything attested about a claim, as a whole, provides its overall score: a Glicko-2 standing that tells how hard a strand tugs back.
  - [Pull](Semantics/Pull.md) — Laplace's forward pass is native C recursive operations with A* and indexed lookups, pulling on an interwoven web of entities and attestations.
- [Query](Query.md) — Laplace finds content by computing its ID and coordinates on the client and looking them up with spatial indexes.
- [Operations](Operations/README.md) — Operations covers what Laplace runs on and how it is built, configured, deployed, and tuned, from bare hardware to loaded, indexed, and measured content.
  - [Setup](Operations/Setup.md) — Laplace runs on x86-64 CPUs, uses every SIMD level the CPU has, never requires a GPU, and wants its database heap, write-ahead log, and temporary files on separate fast drives.
  - [Builds](Operations/Builds.md) — PostgreSQL, Laplace-Native, and Laplace-postgres are built from source with Intel's compilers, with floating-point settings that give the same bits on every CPU.
  - [Database](Operations/Database.md) — PostgreSQL's defaults suit small general-purpose servers; Laplace tunes memory, I/O, and planning to its hardware and to the way it uses geometry and indexes.
  - [Deployment](Operations/Deployment.md) — A Laplace database goes from empty to benchmarked in five steps: extensions, schema, ingestion, indexes, and measurement.
- [Research](Research/README.md) — research collects the sourced findings and measured results that support the Laplace specification.
  - [Prototype](Research/Prototype.md) — a working prototype of the storage layer was built from the specification and tested against 195 Project Gutenberg texts, and every number on this page was measured on it.
  - [Placement](Research/Placement.md) — Codepoints are placed on the S³ by taking Marc Alexa's Super-Fibonacci points for n = 1,114,112 in the order of their 4D Hilbert value and giving DUCET rank *r* the *r*-th point, which puts collation neighbors next to each other in space.
  - [Sampling](Research/Sampling.md) — Super-Fibonacci spirals give a fixed-size, evenly spread set of points on the S³, and this page records their construction, their relation to the Hopf fibration and to incremental grids, radical-inverse ordering, and local numeric checks.
  - [Unicode](Research/Unicode.md) — Laplace's tier 0 and its segmentation rest on the Unicode data, and this page records what that data defines, what it covers, and which parts of it are stable across versions.
  - [Hashing](Research/Hashing.md) — Research on how BLAKE3, Merkle trees and DAGs, hash-consing, and IEEE-754 bit packing behave under the Laplace identity scheme.
  - [Geometry](Research/Geometry.md) — Research on how PostgreSQL and PostGIS store, index, and compute on four-dimensional geometry, and on the 4D distance, centroid, and curve tools that Laplace builds on them.
  - [Numerics](Research/Numerics.md) — Research on the floating-point limits of Laplace's coordinates and of IDs written into geometry, the cost of colliding its IDs, and how trajectory distance measures treat noise and repetition.
  - [Semantics Experiments](Research/Semantics-Experiments.md) — first experiments with semantic records on the local curated corpora measured how identifiers link words, concepts, and languages, how annotation layers deduplicate as content, how witnessed claims translate between languages, and how well a pull disambiguates word senses.
  - [Chess](Research/Chess.md) — Glicko-2 ratings computed from observed chess games alone, one game at a time in the order the games were played, predicted over-the-board results better than the official ratings once each player entered at an attested rating.
  - [Learning](Research/Learning.md) — Research on how ratings can be updated one matchup at a time, how retrieval compares with knowledge stored in model weights, and what the literature reports about softmax, unlearning, execution feedback, and interpretability.
  - [Recipes](Research/Recipes.md) — research and measurements on how one generic decomposer can take any standardized file format apart into content and put it back together byte for byte.
  - [Corpus Search](Research/Corpus-Search.md) — Laplace's Merkle DAG is a grammar-compressed corpus, so exact occurrence counts, distinct-document counts, and phrase search inside containers all have direct precedent in the literature on grammar-compressed and suffix-based text indexes.
  - [Prior Art](Research/Prior-Art.md) — Each mechanism in Laplace's storage layer has published precedent, and the research found no prior system that combines them.
  - [Trust](Research/Trust.md) — Research and measurements on how much a witness's attestation should count and how hard each kind of word or relation should pull, measured on the local witnesses, on 88 languages of Universal Dependencies, and on word sense disambiguation.
  - [Engine Measurements](Research/Engine.md) — The first shared components of the real implementation, Laplace-Native and Laplace-postgres, were measured on a tuned PostgreSQL server with the Gutenberg corpus, and every number on this page comes from their benchmarks.
  - [Relations Research](Research/Relations.md) — Research into rating models, evidence counts, search over rated relations, truth discovery, and provenance is background for Laplace's semantics layer.
- [Spitball](Spitball.md) — text that has not been properly considered for the documentation as a whole.
