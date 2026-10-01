# 17. Envelope

Every operation runs under an explicit compute envelope: hops, fanout, frontier, candidates, providers, trajectory expansion, calculation, memory, I/O, concurrency, and output, planned before execution, reserved, enforced under counters, receipted, and reconciled.

Hops and fanout are first-class work coordinates. The work of a pull is shaped by the admitted frontier and indexed lookup cost, not by an obligation to compare every object to every other. Laplace sells measured cognition over the same intelligence: a sophisticated question may be cheap when strong evidence is near the root, and a simple one expensive when the caller requests exhaustive depth. There is no fixed token context window; the envelope bounds the work of one operation without making older state unreachable.

## Before this stage

[16. Authority](Authority.md): the entitled world the envelope is spent over. [14. Indexes](Indexes.md): the lookup costs a plan is estimated from.

## Operations, per request

### 17.1 Name the dimensions

- **In:** a compiled program, from [20. Forward](Forward.md) operation 20.4.
- **Do:** the dimensions are hop depth, `H`; fanout or frontier width per hop, `F_h`; candidate and evidence-cell work; eligible relation, provider, and operator families; trajectory and containment expansion; search, geometry, and calculation work; CPU, memory, I/O, and concurrency; and the realization and output budget. Presets such as quick, standard, deep, and custom are presentation over these explicit dimensions. The firmware may spend less than the envelope and never more.
- **Out:** the envelope of this request.
- **From:** `docs/INVENTION.md` §9 and §16; `docs/CAPABILITIES.md` §Compute depth is the product tier; `docs/specs/39_Personality_Firmware.md` §3.

### 17.2 Plan and EXPLAIN

- **In:** the program and the envelope.
- **Do:** the routed program exposes the same hop, fanout, provider, index, and operator dimensions that execution will consume; there is no separate billing model. Estimate the semantic work: roots and occurrences, hops, fanout and frontier widths, families, expected index probes and rows and physicalities touched, trajectory expansion, calculation work, standing cells, realization work. `EXPLAIN` over the physical plan is part of execution, not billing decoration; plan cost and executor cost are measured independently where planning a large partition tree is itself material.
- **Out:** the semantic work estimate.
- **From:** `docs/specs/36_Laplace_Forward_Pass.md` §Compute envelope and preflight; `docs/read-path.md` §5 and §9; `docs/INVENTIONS.md` #92.

### 17.3 Derive the machine cost

- **In:** the estimate of 17.2 and the target machine.
- **Do:** lower the artifact or program through the chain: source → grammar AST → compiler and linker artifacts → bytecode, object, or executable container → functions, symbols, basic blocks → decoded machine instructions → control-flow graph → data and dependency graph → execution-count variables → target ISA → microarchitecture and scheduling model → memory and initial-state assumptions → clock → resource-constrained cycles → machine time. A JAR has its own boundary through the selected JVM, its mode, and its JIT before the target processor, and no "opcode = N cycles" shortcut is invented. Unknown loop counts, cache state, branch history, I/O service time, and scheduler interference stay symbolic, conditional, or distributional: `cycles(N) = setup + N·body + branch/cache terms`. Two independently scheduled instructions do not cost the sum of their latencies; the dependency DAG and the resource model own the result. A measured run validates or calibrates the model and does not replace derivable work with "it took N ms on my box".
- **Out:** an exact, symbolic, or conditional cycle expression and a time.
- **From:** `docs/guides/machine-cost-analysis.md`; `docs/CAPABILITIES.md` §Deterministic machine-cost derivation; `docs/INVENTIONS.md` #120, #121.

### 17.4 Reserve a hard ceiling

- **In:** the estimate.
- **Do:** where work is billable or capacity-controlled, reserve compute credits against the admitted upper bound. A serviceable estimate on a managed host preserves database, product, runner, and control-plane headroom; full logical-CPU saturation is a separate, explicitly labelled experiment.
- **Out:** the reservation.
- **From:** `docs/INVENTIONS.md` #93, #95.

### 17.5 Execute under counters

- **In:** the reservation.
- **Do:** run the program with hard resource counters on every dimension of 17.1. If convergence, uncertainty, or obligation state is already sufficient, stop early and return the unused reserve. The envelope belongs to the principal and the tier; the firmware chooses how much of it to spend.
- **Out:** the run, bounded.
- **From:** `docs/INVENTIONS.md` #94; `docs/specs/39_Personality_Firmware.md` §3.

### 17.6 Write the actual receipt

- **In:** the run.
- **Do:** report the work actually performed against the same dimensions: codepoints, recursive structural nodes, candidates and frontier cells examined and admitted, evidence cells resolved, trajectory constituents and containment hits, routes and hops expanded, realized structures and bytes, CPU, memory, I/O, database calls, and boundary crossings, with the workload, host, revision, artifact, thread count, execution provider, and database participation named. A token-per-second figure is a normalization of that work, not its unit. Semantic work and implementation waste stay separate: thousands of avoidable SQL, SPI, or P/Invoke crossings are an optimization defect, never permanent pricing authority.
- **Out:** the work receipt.
- **From:** `docs/INVENTION.md` §17.6; `docs/read-path.md` §10; `docs/INVENTIONS.md` #96, #97.

### 17.7 Reconcile

- **In:** the reservation of 17.4 and the receipt of 17.6.
- **Do:** refund the unused reserve; compare calculated against observed to calibrate the physical and environment model; residual error tugs cache assumptions, branch behaviour, frequency scaling, OS scheduling, memory latency, JIT and compiler differences, and omitted machine semantics.
- **Out:** the reconciled charge and a calibration witness.
- **From:** `docs/CAPABILITIES.md` §Compute depth is the product tier; `docs/guides/machine-cost-analysis.md` §Calculated versus observed.

## What this stage leaves behind

A request that knows before it runs how far and how wide it may pull, a run that cannot exceed that, and a receipt that says what it did in the units it did it in, over the same world every other request sees.

## Without this stage

Work is unbounded or arbitrary, cost is a guess from output tokens, and a product tier can only be a smaller model.
