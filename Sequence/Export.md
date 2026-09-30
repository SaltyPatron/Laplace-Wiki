# 25. Export

Mold-a-Model exports a conventional model artifact as a filtered snapshot of current standing, geometry, and selected operators under an authorized scope: a content-addressed recipe names the target architecture, the operator that fills each slot, and the substrate calculations that derive every weight, and the artifact is validated by loading it elsewhere.

Export is "I know kung fu", not `cp model.gguf`. The live substrate is the primary state; conventional model files are optional render targets. The model export reinvents what gradient descent produced: nouns, standing, and trajectories become the cosine similarities, dot products, and probabilities that a target format expects, generated at runtime from the queries of [20. Forward](Forward.md). Export comes after the reads are right; until the forward program reads correctly, export work muddies the data.

## Before this stage

[20. Forward](Forward.md) reading correctly on a coherent seed. [16. Authority](Authority.md): the EXPORT capability. [24. Models](Models.md) where a source-scoped export is wanted.

## As built

None. In the monorepo: `FoundryExport.cs` builds the planes (consensus, trajectory next, gap, window) as sparse matrices, `FoundryCommands.cs`, `FoundryExportService.cs`, `/v1/synthesis/export` and `/v1/foundry`, `generation.foundry_crawl` and `foundry_vocab`; native `gguf_writer`, `format_writer`, `arch_template`, `recipe.cpp`; specs 09, 12, 14 ([Monorepo: Models](../Reference/Monorepo.md#models-export-code-chess-and-games)).

Status: **monorepo**. Every operation below is from the invention documents; [Reference: Traceability](../Reference/Traceability.md#25-export) indexes it.

## Operations, per export

### 25.1 Resolve authority and export scope

- **In:** the principal and the request.
- **Do:** resolve the effective authority, and require EXPORT when the artifact leaves the boundary. Select source, context, and evidence scope only within that authority: source A, source B, pooled A+B, or the whole entitled world. Selecting a narrow artifact does not make the live world forget anything, and a narrow export is never the cheap-tier execution path.
- **Out:** the export scope.
- **From:** `docs/specs/12_Mold_A_Model_Synthesis_Map.txt` §Authority law and §Construction law step 1; `docs/invention/recipe-schema.md` §Authority and scope boundary.

### 25.2 Deposit the recipe as content

- **In:** the target architecture and the operator choices.
- **Do:** a recipe is a versioned JSON description deposited as a content-addressed `Model_Recipe` entity, its hyperparameters also emitted as scalar attestations; export reads the stored recipe, never a disk file, and a hand-written recipe is a development fixture that goes through deposit like any other. Its fields: `structure` dense or MoE; `hidden_size`, an integer or `auto` for the spectral rank of the selected operators' graph; `num_layers`; `rope`; `tie_embeddings`; `norm`; `vocab`, the content selection from a real tokenizer, a topic crawl with seeds, hops, fanout, and size, or the grapheme floor; `embed`, default the coordinate operator; `lm_head`, default the trajectory operator; and `layers`, one entry per layer with its KV heads, its heads each as an operator, and its FFN operator. The user designs the vessel and chooses what fills it; the substrate determines every weight value; the math turning knowledge into weights is fixed.
- **Out:** the recipe entity.
- **From:** `docs/invention/recipe-schema.md`.

### 25.3 Choose each slot's operator

- **In:** each head, embedding, output head, and FFN slot.
- **Do:** the operator catalog: `relation` with a type, `IS_A` or any attestation type, from the consensus plane of that relation, drives a head's Q and K as rated affinity and its V and O as residual; `metric`, angular, Fréchet, or Hausdorff, from metric edges over realized curves and coordinates, drives a metric head; `trajectory`, from the continuation conditional plane, drives the output head's log-odds or a sequential head or FFN; `coord`, the native S³ coordinate, drives the token embedding; `spectral`, the Laplacian eigenmap of the selected graph, drives an alternative embedding; `unary`, the per-token consensus covariance, drives an FFN. Each head fills its own rows from its operator, never top-k of one operator tiled across heads. The recommended schedule runs neighbourhood to structure to continuation: early layers equivalence and associative with angular, middle layers taxonomic and partitive with Fréchet, last layers causal and sequential with a trajectory FFN. The slot map: vocabulary from the Unicode floor and canonical entities; embedding from content placement; position from trajectory ordinal and Hilbert locality; Q, K, QK, V, O from the forward program's roles; heads from source circuits grouped by witnessed function; MLP and experts from factor trajectories; router from ORIENT and ROUTE; residual from typed strata; normalization from a recipe scale policy; logit head from typed completion candidates and conservative consensus; layers as target slots, not native ontology; loss as witnessed outcomes.
- **Out:** the operator array.
- **From:** `docs/invention/recipe-schema.md` §Operator catalog and §`layers[]`; `docs/specs/12_Mold_A_Model_Synthesis_Map.txt` §Slot map.

### 25.4 Resolve the witnesses and build the circuits

- **In:** the scope of 25.1 and the recipe of 25.2.
- **Do:** resolve canonical content and eligible recorded and calculated witnesses from the scope; build bounded candidate circuits and operators from factors and trajectories; fold corroboration and conflict while retaining source provenance. A source's `L5.H7` stays source-scoped and may correlate with another's `L9.H3` or with nothing. Layer and head counts are recipe outputs; nothing is copied from a hardcoded template. Glicko-complete edge state, support, uncertainty, refutation, source semantics, and witness saturation, reaches construction under the declared recipe.
- **Out:** the constructed operator schedule.
- **From:** `docs/specs/12_Mold_A_Model_Synthesis_Map.txt` §Construction law steps 2 to 6; `docs/INVENTIONS.md` #82, #83.

### 25.5 Materialize every weight, in bulk

- **In:** the schedule of 25.4.
- **Do:** every weight value, embedding, Q, K, V, O, gate, up, down, output head, norms, is derived: it is the rated attestations, calculated. Nothing in the weights is chosen, which is why provenance is auditable. Derived too: head dimension, each operator's rank, the hidden size when `auto`, the intermediate size default, token coordinates, consensus rating and deviation, the recipe id, and the weight-to-source provenance. Format writers stream bulk tensors and metadata natively, never one boundary crossing per scalar. Any codec limitation fails explicitly rather than reshaping the invention into a supported template.
- **Out:** the tensors, with a cell-to-tensor receipt per slot.
- **From:** `docs/invention/recipe-schema.md` §Knobs vs derived vs fixed; `docs/specs/12_Mold_A_Model_Synthesis_Map.txt` §Export law; `docs/INVENTIONS.md` #90.

### 25.6 Emit the artifact and its receipts

- **In:** the tensors of 25.5.
- **Do:** translate the constructed program into SafeTensors, GGUF, or another target through its codec. Every output slot declares its recipe, source scope, substrate cells, calculations, and determinism inputs. The artifact retains a reproducible recipe and never silently copies unknown witness weights because the format expects a tensor. Seeded corpora and checkpoints are exported as world state, a snapshot, never round-tripped bit-perfect; user content the operator asked Laplace to keep is the case that requires exact realization, and that is the other lane.
- **Out:** the file and its provenance receipts.
- **From:** `docs/INVENTION.md` §15; `docs/specs/12_Mold_A_Model_Synthesis_Map.txt` §Export law.

### 25.7 Validate by loading and by ablation

- **In:** the artifact.
- **Do:** a loadable file is not success. Load it in the declared external runtime and pass held-out semantic, source-ablation, and provenance checks; a single-operator model has a predictable signature that is the correctness gate: `IS_A` alone climbs hypernyms, `king → monarch → ruler → person`, then stalls; `IS_SYNONYM_OF` alone clusters synonyms without progression; `trajectory` alone continues n-grams fluently and driftlessly; `metric:angular` alone returns category-mates regardless of relation; `HAS_DEFINITION` alone returns sentence fragments. Source-only and pooled recipes are reproducible. Behavioural validation of the export is separate from proof of the native substrate.
- **Out:** a validated consumer artifact.
- **From:** `docs/invention/recipe-schema.md` §Validation by ablation; `docs/specs/09_Substrate_LM_Synthesis.txt` §Construction and export and §Acceptance.

## What this stage leaves behind

A clean conventional model with no training artifacts and no gradient jitter, every weight traceable to the cells and calculations that produced it, exportable for one source, for several at the round table, or for the whole entitled world.

## Without this stage

Laplace still answers. It cannot hand its knowledge to a machine that only runs conventional models.
