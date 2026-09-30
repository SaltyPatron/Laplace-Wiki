# Sequence

Laplace is built in one order, and each stage is impossible without the one before it: Unicode onto the S³, tier 0, the registries and perf-caches, the store, sources through recipes into content, attestations, consensus, indexes, the web, authority, the compute envelope, the firmware, the forward program, sessions, and only then a user, whose consequences feed the learning loop that models, export, code, chess, and games all run on.

Each stage is its own page, and each page is the operations of that stage in the order they run. An operation is one numbered heading with six lines:

- **In:** what it takes, and from which earlier operation.
- **Do:** what it does, in the words of the specification and the invention documents.
- **Out:** what it leaves for the next operation.
- **Check:** what proves it, with the measured value where one exists.
- **Mechanism:** what in the four repositories performs it, by name, linked to the [Reference](../Reference/README.md) page that documents that artifact, function, statement, or file; then its status.
- **From:** the specification page or invention document the operation comes from.

A status is one of **built**, in Laplace-Native, Laplace-postgres, and Laplace-Engine; **monorepo**, built in SaltyPatron/Laplace, the first full implementation, and not in those three; **prototype**, in Laplace-Prototype only; **specified**, in the invention documents and not yet built in any repository the wiki documents; or **operator**, done by hand following the [Operations](../Operations/README.md) pages. Where the monorepo does the operation under a different law from the split repositories, the Mechanism line says both; [Reference: Monorepo](../Reference/Monorepo.md) collects the differences. A qualified status, "built for tier 0; the rest specified", says which part is which. Where the built machine does something other than what **Do** says, the **Mechanism** line says so; the operation keeps the specification's words, and the difference is recorded, not resolved. [Reference: Traceability](../Reference/Traceability.md) indexes every operation's mechanism, check, and status on one page.

A stage's first operation needs the last operation of the stage before it. The specification pages of this wiki and the invention documents of the monorepo (`docs/INVENTION.md`, `docs/INVENTIONS.md`, `docs/CAPABILITIES.md`, and the binding specs 05, 06, 08, 09, 11, 12, 33, 34, 36, 37, 38, 39) are the authority; these pages repeat them operation by operation so that the order itself is recorded, and link to the page each operation comes from. Where the two authorities disagree, the disagreement is recorded in [30. Conflicts](Conflicts.md) and not resolved here.

## Where to start

- To build an install: stages 1 to 14 in order, with [Reference: Build](../Reference/Build.md), [Environment](../Reference/Environment.md), and [CLI](../Reference/CLI.md) open beside them; `deploy.sh` runs stages 3 to 14 as one logged script.
- To write a source: [9. Sources](Sources.md) and [10. Recipes](Recipes.md), with [Reference: Recipes](../Reference/Recipes.md) for the grammar.
- To read what is recorded: [15. Web](Web.md), [18. Firmware](Firmware.md), [19. Pull](Pull.md), with [Reference: Reads](../Reference/Reads.md) and [Firmware](../Reference/Firmware.md).
- To see what a byte, a row, or a function is: [Reference: Formats](../Reference/Formats.md), [Schema](../Reference/Schema.md), [SQL](../Reference/SQL.md), [Native](../Reference/Native.md).
- To see what is built and what is not: [Reference: Traceability](../Reference/Traceability.md).

## The artifacts

The artifact each stage produces, and which later stage consumes it, is the graph in [Reference: Repositories](../Reference/Repositories.md#the-artifact-graph): the Unicode data to tier 0 and the flags; the dependencies to the library; the library to the extension and the engine; the grammars to the engine; the extension, tier 0, and the flags to the database; the recipes, the firmware, and the corpora to the engine; the engine to the database by COPY and back by paths and standings.

## The stages

```mermaid
flowchart TD
    U[1. Unicode] --> T[2. Toolchain]
    T --> B[3. Builds]
    B --> S[4. Projection]
    S --> Z[5. Tier 0]
    Z --> G[6. Registries]
    G --> PC[7. Perfcaches]
    PC --> D[8. Database]
    D --> SO[9. Sources]
    SO --> R[10. Recipes]
    R --> C[11. Content]
    C --> A[12. Attestations]
    A --> K[13. Consensus]
    K --> I[14. Indexes]
    I --> W[15. Web]
    W --> AU[16. Authority]
    AU --> E[17. Envelope]
    E --> F[18. Firmware]
    F --> P[19. Pull]
    P --> FP[20. Forward]
    FP --> SE[21. Sessions]
    SE --> H[22. Users]
    H --> L[23. Learning]
    L --> M[24. Models]
    L --> X[25. Export]
    L --> CO[26. Code]
    L --> CH[27. Chess]
    L --> GA[28. Games]
    L --> MA[29. Maintenance]
```

- [1. Unicode](Unicode.md): one version, every file.
- [2. Toolchain](Toolchain.md): the machine and every dependency, built the same way.
- [3. Builds](Builds.md): the server, the library, the extension, the engine, one deployed revision.
- [4. Projection](Projection.md): every codepoint onto the S³.
- [5. Tier 0](Tier-0.md): the anchor perf-cache and its fingerprint.
- [6. Registries](Registries.md): relations, qualifiers, trust classes, entity types, vocabularies, firmware policy kinds: governed, append-only, bit-stable.
- [7. Perfcaches](Perfcaches.md): the derived ROM lattice above tier 0.
- [8. Database](Database.md): the tuned server and the four families of durable state.
- [9. Sources](Sources.md): a source generation: authority, release, artifact graph, provider, recipe, activated together.
- [10. Recipes](Recipes.md): one format decomposer per format, one semantic recipe per source.
- [11. Content](Content.md): the ingest spine, from unpack to fold completion.
- [12. Attestations](Attestations.md): witnesses, typed claims, qualifiers, collections, record versus calculate.
- [13. Consensus](Consensus.md): one matchup per attestation, at the witness's trust.
- [14. Indexes](Indexes.md): after the bulk load, then measurement.
- [15. Web](Web.md): the spider-colony web and its typed channels.
- [16. Authority](Authority.md): knowledge, authority, and compute as three axes; packages and capabilities.
- [17. Envelope](Envelope.md): hops, fanout, and work: plan, reserve, execute, receipt, reconcile.
- [18. Firmware](Firmware.md): the program over the instruction set, kept out of the records.
- [19. Pull](Pull.md): the lookups and operators a stage of the program calls.
- [20. Forward](Forward.md): RESOLVE, COUPLE, ORIENT, ROUTE, SCAN, COMPOSE, PROPOSE, STEER, SELECT, REALIZE, WITNESS.
- [21. Sessions](Sessions.md): tenant, user, session, turn, and the surfaces that bind the one program.
- [22. Users](Users.md): the first prompt.
- [23. Learning](Learning.md): OODA, the three rates, the feedback lanes, and the Gödel lane.
- [24. Models](Models.md): a checkpoint as a witness.
- [25. Export](Export.md): Mold-a-Model.
- [26. Code](Code.md): software as structural construction.
- [27. Chess](Chess.md): the proving domain.
- [28. Games](Games.md): the Knowledge Arena.
- [29. Maintenance](Maintenance.md): forget, sweep, reseed, regenerate, upgrade.
- [30. Conflicts](Conflicts.md): what the two authorities say differently, recorded and unresolved.

## What comes after the chain

Stages 24 to 29 need the whole chain and add to it. They are not stages of the chain; each is a lane that runs through [20. Forward](Forward.md) and [23. Learning](Learning.md) again. A new Unicode version runs [1. Unicode](Unicode.md) through [5. Tier 0](Tier-0.md) again with a new fingerprint, under the rules of [29. Maintenance](Maintenance.md).
