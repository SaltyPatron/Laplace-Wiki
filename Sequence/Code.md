# 26. Code

Software is constructed as structure under an exact target grammar and toolchain: reuse, then compose, then minimally adapt, then construct only novel structure, realize source only as the toolchain requires, compile and test, witness every outcome, repair the smallest divergent subtree, and remint only the changed ancestry up to a new repository root.

Everything is an AST, and the substrate is a Merkle DAG AST; that is why the tree-sitter grammars are exploited and why Laplace has its own. Laplace constructs software structure; it does not primarily predict source text, and syntactic illegality never has to be part of the search space. Source text is a realization of selected canonical structure, and a checkout is a realization of a repository root.

## Before this stage

[10. Recipes](Recipes.md): the grammars, and code corpora such as The Stack ingested as content. [20. Forward](Forward.md): the program, bound to the code lane. [23. Learning](Learning.md): the repair trajectory is witnessed there.

## Operations, per task

### 26.1 Bind the exact target

- **In:** a requirement or obligation.
- **Do:** bind the exact target language, grammar generation, runtime, toolchain, version, dialect, framework, ABI, and platform contract. A request for Bash is bound to the admitted Bash grammar and runtime; a request for Zsh requires a qualified Zsh provider, and if none exists the correct result is explicit missing capability, never Bash as a probabilistic substitute.
- **Out:** the bound target.
- **From:** `docs/guides/software-construction.md` §Exact language means exact language; `docs/CAPABILITIES.md` §Software construction.

### 26.2 Resolve the repository root

- **In:** the repository.
- **Do:** a repository is a recursively composed application root, ingested as content: expressions in statements in blocks in methods in files in directories up to the root `R0`, every subtree a canonical entity shared with every other repository that contains it. Git history is a trajectory of roots.
- **Out:** `R0`.
- **From:** `docs/INVENTION.md` §Repository root; `docs/guides/software-construction.md` §Repository root is the application.

### 26.3 Couple before inventing

- **In:** the requirement and `R0`.
- **Do:** COUPLE against known canonical composition, trajectory, call, dependency, and repair state, and ask in order: does this exact implementation already exist? Can existing canonical structures compose to satisfy the requirement? Is there a close lawful implementation that needs only a bounded mutation? Only then, what genuinely novel structure is required? Exact duplicates converge by identity; deeper duplicates are found by normalized AST projection, symbol and role normalization, call, dependency, control, and data-flow shape, algebraic equivalence under a declared numeric contract, behavioural evidence, and Fréchet comparison of ordered trajectories where lawful. Same semantics implemented several times is a consolidation candidate; same names prove nothing.
- **Out:** reuse, composition, adaptation, or a declared novelty.
- **From:** `docs/guides/software-construction.md` §Search before invention; `docs/INVENTIONS.md` #114, #115.

### 26.4 Construct under the constraints

- **In:** the decision of 26.3.
- **Do:** construct the canonical composition, satisfying grammar, type, name, API, and dependency obligations; project an AST, CST, or IR only where the selected toolchain requires it. Grammar productions, precedence, and associativity are knowledge that constrains lawful composition, not a second universe of parser enums.
- **Out:** the changed subtree.
- **From:** `docs/specs/36_Laplace_Forward_Pass.md` §Code lane; `docs/INVENTION.md` §3 "Software construction".

### 26.5 Remint the ancestry only

- **In:** the changed subtree.
- **Do:** `R0 + Δ → changed composition → changed file and container ancestry → R1`. Every unrelated canonical subtree stays shared with `R0`. Construction work is proportional to the semantic delta and its ancestry; realization work is proportional to the requested output bytes, and a full checkout does not redo cognition for unchanged files.
- **Out:** `R1`.
- **From:** `docs/CAPABILITIES.md` §The repository root is the application object; `docs/INVENTIONS.md` #118.

### 26.6 Realize source

- **In:** `R1` and the target of 26.1.
- **Do:** REALIZE the source, AST, CST, or IR the toolchain needs, in bulk, byte-exact for a checkout.
- **Out:** the files.
- **From:** `docs/guides/software-construction.md` §Full-repository realization.

### 26.7 Compile, link, test, analyze, simulate, run

- **In:** the realization.
- **Do:** run the declared toolchain and verification providers. A valid AST is not correctness; type, link, runtime, behavioural, and toolchain evidence are separate.
- **Out:** diagnostics, exceptions, test results, analysis, simulation, and runtime observations.
- **From:** `docs/CAPABILITIES.md` §Software construction.

### 26.8 Witness every outcome

- **In:** the results of 26.7.
- **Do:** each is a typed, calculated outcome attached to the exact code, toolchain, environment, and target identities plus any derived projection, with its analyzer identity and version, [12. Attestations](Attestations.md) operation 12.10. A failure is reusable negative evidence: "compile failed, negative attestation, next iteration; oh wait, we tried this, it failed hard, abort, rethink." A success is an evidence-backed transition explaining which obligation failed, which structure changed, and which verification closed it. Toolchain failures are never disposable stderr appended to a prompt.
- **Out:** the witnessed trajectory `R0 → Δ1 → failures → Δ2 → … → verified R1`.
- **From:** `docs/guides/software-construction.md` §Development is a witnessed trajectory; `docs/INVENTOR_RECORD.md` §Gödel engine; `docs/INVENTIONS.md` #116.

### 26.9 Repair the smallest divergent subtree

- **In:** a failure.
- **Do:** attach the failure to the exact divergent structure and context, "one of these things is not like the others"; tug artifact identity, structure, dependencies, toolchain and runtime versions, target hardware, input, execution path, environment, and prior repair trajectories; avoid transformations already witnessed to fail under matching structure; mutate the smallest subtree; repeat from 26.5 until obligations close or a WHY_NOT remains, with the residual explicit when the current model cannot explain it.
- **Out:** the next Δ, or the WHY_NOT.
- **From:** `docs/guides/software-construction.md` §"One of these things is not like the others".

### 26.10 Couple the repair across repositories

- **In:** a verified repair.
- **Do:** ask other authorized repositories which contain the exact defective subtree, a normalized equivalent, the same dependency or control-flow preconditions, a Fréchet-close failure or repair trajectory, a verified solution, or an apparent mitigation. The match explains its evidence; Fréchet is one plane, not a universal score. Authority is separate from discovery: a principal may analyze, propose, validate, write, merge, or deploy only as granted.
- **Out:** the repositories that warrant inspection.
- **From:** `docs/guides/software-construction.md` §Cross-repository maintenance; `docs/INVENTIONS.md` #117.

### 26.11 Express the patch as a root transition

- **In:** `R0` and `R1`.
- **Do:** `FROM R0 TO R1`, with transfer = closure(`R1`) minus objects already present, proof = derivation plus compile, test, analysis, and runtime receipts, activate = `R1`, rollback = `R0`. Mutable database, configuration, secret, and external-system transitions remain explicit obligations; immutable structural sharing does not erase mutable world state.
- **Out:** the patch object.
- **From:** `docs/INVENTION.md` §Repository root; `docs/INVENTIONS.md` #119.

### 26.12 Deploy as a governed program

- **In:** the patch of 26.11.
- **Do:** resolve current state, verify authority, stage the missing closure, perform the declared migrations, verify the target state, activate, observe, witness, and roll back when the observed result violates the declared obligation. The engine deploying to itself is [18. Firmware](Firmware.md) operation 18.17.
- **Out:** the deployment, witnessed.
- **From:** `docs/CAPABILITIES.md` §Patch/deployment as a proven root transition.

### 26.13 Derive the machine cost of what was built

- **In:** the built artifact.
- **Do:** [17. Envelope](Envelope.md) operation 17.3, over the artifact: decoded instructions, control and data flow, execution-count variables, target ISA and microarchitecture, cycles, time, with unknowns symbolic and benchmarks as calibration witnesses.
- **Out:** the calculated cost, beside the measured one.
- **From:** `docs/guides/machine-cost-analysis.md`.

## What this stage leaves behind

Code as a player: grammar-valid structure built by reuse before novelty, every attempt and outcome witnessed against exact identities, repositories that remint only what changed, and patches that carry their own proof.

## Without this stage

Laplace can talk about code and cannot write it, and every generated program is a token guess that may not even parse.
