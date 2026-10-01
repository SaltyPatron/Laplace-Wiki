# Reference

Reference documents the machine as built, exactly: every artifact with its byte layout, every table as its DDL, every native function, SQL function, command, and file grammar with its contract, every configuration value with its default and its consumer, the pipeline as the engine runs it, and the checks that prove each part.

The specification pages say what Laplace is. The [Sequence](../Sequence/README.md) says the order it is built and operated in. Reference says what exists in the repositories that implement it, taken from their sources and nothing else: the split repositories Laplace-Native 0.2.0, Laplace-postgres 1.0, and Laplace-Engine, which the wiki calls Laplace itself; Laplace-Prototype, the test bench; and the monorepo SaltyPatron/Laplace, the first full implementation and the home of the invention documents, at their current heads. Where the built machine differs from the specification, or where a stage is specified and not yet built, the page says so; it does not resolve the difference.

Conventions. A name in fixed width is exact as it appears in a source or a file: `lp_id_compose`, `entity_t2_a`, `LAPLACE_TIER0`. A byte layout is given in the order the bytes are written, little-endian unless stated. "Measured" values come from the reference machine in [Research: Engine Measurements](../Research/Engine.md) and name the operation they measured. A status is one of: **built**, in the split repositories; **monorepo**, built in SaltyPatron/Laplace and not in the split repositories; **prototype**, in Laplace-Prototype only; **specified**, in the invention documents and not yet built in any repository the wiki documents; **operator**, done by hand following the [Operations](../Operations/README.md) pages, with no Laplace program doing it. Built in the split repositories and built in the monorepo are two different machines with different laws; [Monorepo: How it differs](Monorepo.md#how-it-differs-from-the-split-repositories) lists the differences.

- [Repositories](Repositories.md): what each repository holds, what it builds, and the artifact graph between them.
- [Monorepo](Monorepo.md): SaltyPatron/Laplace as built: its extension, engine, application, manifests, pipeline, and checks, and how its laws differ from the split repositories'.
- [Environment](Environment.md): every variable and setting, its default, and who reads it.
- [Build](Build.md): the flags, presets, targets, scripts, and the tests that run after a build.
- [Formats](Formats.md): the byte layouts: IDs, the tier-0 record, the flags, coordinates, Hilbert values, packed paths, wire and COPY formats.
- [Schema](Schema.md): the tables, partitions, indexes, and settings, as DDL.
- [SQL](SQL.md): every type, operator, and function the extension installs.
- [Native](Native.md): every function of the shared library, by module, with its contract.
- [CLI](CLI.md): every command of the engine, its options, inputs, outputs, and exit status.
- [Recipes](Recipes.md): the source and recipe file grammars, the stock recipes, and how a file becomes a trunk.
- [Firmware](Firmware.md): the firmware file grammar, its defaults, and the program's own firmware.
- [Ingest](Ingest.md): the ingest pipeline as the engine runs it, phase by phase, with its statements and its counters.
- [Reads](Reads.md): the read commands as built, the statements each issues, and what is computed where.
- [Checks](Checks.md): every check that proves the machine: the native tests, the prototype verification, the status and bench commands, the query benchmark.
- [Glossary](Glossary.md): the terms, each defined once.
- [Types, masks and the highway](Types.md): types are never content: perf-caches, values in vertices, masks, layers, segmentation, repeats, the extension owning the schema.
