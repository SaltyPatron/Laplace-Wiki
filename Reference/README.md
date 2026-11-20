# Reference

Reference documents the machine as built, exactly: every artifact with its byte layout, every table as its DDL, every native function, SQL function, command, and file grammar with its contract, every configuration value with its default and its consumer, the pipeline as the engine runs it, and the checks that prove each part.

The specification pages say what Laplace is. The [Sequence](../Sequence/README.md) says the order it is built and operated in. Reference says what exists on `HEAD` across the converging modular stack, taken from the sources and nothing else: `Laplace-Native` (the shared C library and generated `Laplace.Native.Interop` bindings), `Laplace-postgres` (`CREATE EXTENSION laplace` and `laplace.reconcile.sql`), `Laplace-Engine` (`laplace` CLI, compiled `.recipe` VM, `.firmware`, and `program.c`), `Laplace-MCP` (`lpm` and `Laplace.Modular.Web`), `Laplace-UCI`, `Laplace-Operations` (`components.lock.tsv`, build, deploy, and verification), `Laplace-Prototype` (the cleanroom test bench), and the converging product application `SaltyPatron/Laplace` (home of the invention documents and OpenAI-compatible `/v1/*`, Web/Glome, Chess Lab, Foundry, Code player, Arena, and `app.*` billing surfaces, which in `Batch 1` retires its pre-modular duplicate substrate onto `Laplace-Native` and the single `laplace` database). Where the built machine differs from the specification, or where a stage is scheduled in an upcoming batch, the page says so; it does not rewrite the specification to excuse drift.

Conventions. A name in fixed width is exact as it appears in a source or a file: `lp_id_compose`, `entity_t2`, `LAPLACE_TIER0`. A byte layout is given in the order the bytes are written, little-endian unless stated. "Measured" values come from the reference machine in [Research: Engine Measurements](../Research/Engine.md) and name the operation they measured. A status is one of: **built**, in the modular packages (`Laplace-Native`, `Laplace-postgres`, `Laplace-Engine`, `Laplace-MCP`); **monorepo**, built in `SaltyPatron/Laplace`'s product layer or pre-Batch-1 substrate; **prototype**, in `Laplace-Prototype` only; **specified**, in the invention documents and not yet built; **operator**, done by hand following the [Operations](../Operations/README.md) pages. [Monorepo: How it differs](Monorepo.md#how-it-differs-from-the-split-repositories) records the pre-modular monorepo differences being retired under `one-substrate`.

- [Repositories](Repositories.md): what each repository holds, what it builds, and the artifact graph between them.
- [Monorepo](Monorepo.md): `SaltyPatron/Laplace` product surfaces and the pre-Batch-1 substrate being retired onto the modular packages.
- [Environment](Environment.md): every variable and setting, its default, and who reads it.
- [Build](Build.md): the flags, presets, targets, scripts, and the tests that run after a build.
- [Formats](Formats.md): the byte layouts: IDs, the tier-0 record, the flags, coordinates, Hilbert values, packed paths, wire and COPY formats.
- [Schema](Schema.md): the tables, partitions, indexes, and settings, as DDL.
- [SQL](SQL.md): every type, operator, and function the extension installs.
- [Native](Native.md): every public header and function of the shared library, by module, with its contract.
- [CLI](CLI.md): all thirty-one commands of `laplace`, their options, inputs, outputs, and exit status.
- [Recipes](Recipes.md): the source, format, and recipe grammars, the compiled Tree-sitter VM, the stock recipes, and how a file becomes a trunk.
- [Firmware](Firmware.md): the firmware file grammar, its defaults, and `program.firmware`.
- [Ingest](Ingest.md): the ingest pipeline as the engine runs it, phase by phase, with its statements and its counters.
- [Reads](Reads.md): the read commands and 11-stage forward program as built, the statements each issues, and what is computed where.
- [Laplace-MCP](Laplace-MCP.md): `lpm` and `Laplace.Modular.Web`, exposing the 25-tool HTTP and MCP surface over `Laplace-Native`, `Laplace-postgres`, and `Laplace-Engine`.
- [Checks](Checks.md): every check that proves the machine: the native tests, the prototype verification, the status and bench commands, the database checks against the deployed database, the query benchmark.
- [Glossary](Glossary.md): the terms, each defined once.
- [Types, masks and the highway](Types.md): types are content and highway slots: perf-caches, values in vertices, 64-bit masks, layers, segmentation, repeats, the extension owning the schema.
