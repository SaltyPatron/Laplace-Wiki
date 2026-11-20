# 25. Export

Mold-a-Model exports a conventional model artifact as a filtered snapshot of current standing, geometry, and selected operators under an authorized scope: a content-addressed recipe names the target architecture, the operator that fills each slot, and the substrate calculations that derive every weight, and the artifact is validated by loading it elsewhere.

Export is "I know kung fu", not `cp model.gguf`. The live substrate is the primary state; conventional model files are optional render targets. The model export reinvents what gradient descent produced: nouns, standing, and trajectories become the cosine similarities, dot products, and probabilities that a target format expects, generated at runtime from the queries of [20. Forward](Forward.md). Export comes after the reads are right; until the forward program reads correctly, export work muddies the data.

## Before this stage

[20. Forward](Forward.md) reading correctly on a coherent seed. [16. Authority](Authority.md): the EXPORT capability. [24. Models](Models.md) where a source-scoped export is wanted.

## Operations, per export

### 25.1 Resolve authority and export scope

- **In:** the principal and the request.
- **Do:** resolve the effective authority, and require EXPORT when the artifact leaves the boundary. Select source, context, and evidence scope only within that authority: source A, source B, pooled A+B, or the whole entitled world. Selecting a narrow artifact does not make the live world forget anything, and a narrow export is never the cheap-tier execution path.
- **Out:** the export scope.
- **From:** `docs/specs/12_Mold_A_Model_Synthesis_Map.txt` §Authority law and §Construction law step 1; `docs/invention/recipe-schema.md` §Authority and scope boundary.

### 25.2 Deposit the recipe as content

- **In:** the target architecture and the operator choices.
- **Do:** a recipe is a versioned JSON description deposited as a content-addressed `Model_Recipe` entity, its hyperparameters also emitted as scalar attestations; export reads the stored recipe, and a hand-written recipe fixture goes through deposit like any other. Its fields: `structure` dense or MoE; `hidden_size`, an integer or `auto` for the spectral rank of the selected operators' graph; `num_layers`; `rope`; `tie_embeddings`; `norm`; `vocab`, the canonical entity selection (from a reference tokenizer vocabulary, a topic/curriculum crawl with seeds, hops, fanout, and size, or a multi-tier Merkle vocabulary spanning codepoints, graphemes, words, phrases, AST nodes, chess moves, and highway identifiers); `embed`, defaulting to **full-rank multi-plane synthesis across trajectory, relational/highway, and 4D geometric planes** (never 4D `coord` alone); `lm_head`, defaulting to trajectory + relational log-odds synthesis; and `layers`, one entry per layer with its KV heads, attention-head operators, and FFN operator. Every vocabulary entry carries **both** its realized UTF-8 surface string (for standard GGUF/`llama.cpp` tokenization) **and** its 16-byte `blake3` `lp_id` (`laplace-blake3-v1`), binding every exported token row directly back to the Merkle DAG. The user designs the vessel and chooses the scope; the substrate determines every weight value on CPU with zero gradient descent.
- **Out:** the recipe entity.
- **From:** `docs/invention/recipe-schema.md`.

### 25.3 Choose each slot's operator (and synthesize full-rank embeddings)

- **In:** each embedding, attention head, FFN, and output-head slot.
- **Do:** **why token embeddings must combine trajectory + relational + geometric planes rather than 4D `entity.coord` alone:** `entity.coord` lives in ℝ⁴, so any linear projection of 4D coordinates into `hidden_size = 512..4096` has matrix rank ≤ 4 (leaving *d* − 4 dimensions degenerate!), and because `entity.coord` is the unweighted centroid of constituent codepoints, every anagram (`"dog"` and `"god"`, `"listen"` and `"silent"`, `"act"` and `"cat"`) shares the **exact same 4D centroid** and would receive bit-identical token embeddings. Mold-a-Model therefore synthesizes full-rank token embeddings (`embed`, rank = `hidden_size`) on CPU via deterministic spectral/SVD/orthogonal block synthesis (`Spectra` / `Eigen` / `MKL`) across three complementary planes:
  1. **Trajectory & context plane (`physicality.path`):** ordered left/right continuation, gap, and constituent-sequence contexts, cleanly separating `"dog"` from `"god"` and capturing distributional syntax;
  2. **Relational & highway plane (`consensus` + `highway.bin`):** trust-bounded Glicko-2 affinities across taxonomic, lexical, frame, and assimilated model-circuit claims;
  3. **4D geometric & curve plane (`entity.coord` + realized curves):** orthographic/structural proximity and realized child-coordinate curve harmonics (`frechet4d` / `dtw4d` / angular neighborhoods).

  Across transformer layers, each attention head and FFN fills its own subspace from distinct operators rather than tiling top-*k* of a single matrix: `relation` operators drive Q/K affinity and V/O value transport per semantic family; `metric` operators drive structural/curve heads; `trajectory` conditional log-odds and factor circuits (`24.6`) drive sequential heads, gated MLPs/experts, and `lm_head`. Early layers emphasize orthographic, syntactic, and lexical equivalence; middle layers compose taxonomic, frame, and multi-hop relational bridges; final layers sharpen sequential continuation and output log-odds.
- **Out:** the full-rank multi-plane embedding and per-layer operator schedule.
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

### 25.6 Emit stock-compatible GGUF / SafeTensors alongside `laplace-blake3-v1` metadata and `share_bp` attribution

- **In:** the tensors of 25.5.
- **Do:** write the synthesized checkpoint into **GGUF**, **SafeTensors** (plus `tokenizer.json` / `config.json`), or an encrypted cartridge (`LPCART01` AES-256-GCM envelope) natively in C. **For GGUF exports, emit the standard `tokenizer.ggml.tokens` UTF-8 surface strings, `tokenizer.ggml.scores`, `tokenizer.ggml.token_type`, merges/model metadata, and special-token keys alongside `laplace.tokenizer.scheme = "laplace-blake3-v1"`, `laplace.vocab.size`, and `laplace.vocab.blake3_ids` (the parallel 16-byte BLAKE3 entity IDs):** that way **stock, unmodified `llama.cpp`** loads and runs the exported GGUF file directly out of the box, while Laplace-aware tools read the exact 16-byte Merkle entity IDs and cell provenance from the `laplace.*` metadata keys! In the same native C + SQL pass, compute the **Source Attribution Receipt** (`source_id`, `claims_touched`, `games`, `fisher_weight`, `share_bp` summing to exact integer `10000` basis points) across all witness trunks in the export scope, weighted by each witness's Glicko-2 Fisher information on the exported cells (`app.billing_royalties`). All weight synthesis, scoped consensus reading, and attribution run in native C + SQL—never in managed C# scalar loops—and `raw_weight_bytes_retained = 0` remains invariant in PostgreSQL.
- **Out:** a stock-`llama.cpp`-loadable GGUF or SafeTensors checkpoint carrying `laplace-blake3-v1` IDs, cell-to-tensor provenance, and a `SUM(share_bp) = 10000` attribution receipt ([17. Envelope](Envelope.md) operation 17.7).
- **From:** `docs/INVENTION.md` §15; `docs/specs/12_Mold_A_Model_Synthesis_Map.txt` §Export law & native source attribution.

### 25.7 Validate by loading and by ablation

- **In:** the artifact.
- **Do:** a loadable file is not success. Load it in the declared external runtime and pass held-out semantic, source-ablation, and provenance checks; a single-operator model has a predictable signature that is the correctness gate: `IS_A` alone climbs hypernyms, `king → monarch → ruler → person`, then stalls; `IS_SYNONYM_OF` alone clusters synonyms without progression; `trajectory` alone continues n-grams fluently and driftlessly; `metric:angular` alone returns category-mates regardless of relation; `HAS_DEFINITION` alone returns sentence fragments. Source-only and pooled recipes are reproducible. Behavioural validation of the export is separate from proof of the native substrate.
- **Out:** a validated consumer artifact.
- **From:** `docs/invention/recipe-schema.md` §Validation by ablation; `docs/specs/09_Substrate_LM_Synthesis.txt` §Construction and export and §Acceptance.

## What this stage leaves behind

A clean conventional model with no training artifacts and no gradient jitter, every weight traceable to the cells and calculations that produced it, exportable for one source, for several at the round table, or for the whole entitled world.

## Without this stage

Laplace still answers. It cannot hand its knowledge to a machine that only runs conventional models.
