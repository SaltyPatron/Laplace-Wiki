# 24. Models

A conventional checkpoint is admitted as a source and a witness: its files are named by their trunks, its tokenizer and configuration are decomposed as content, its tensors are recognized by shape as source-scoped operators, its numerics are consumed transiently to derive circuit physicalities and significance-contracted claims under the model's witness, and no raw weight is retained.

Static models are food for Laplace. A model is not recorded as raw weights, not prompted to see what falls out, and not replayed over retained tensors. Its learned relations, `king` to `queen` at some intensity, become Laplace records, attestations, and scores under the model witness, and Glicko-2 acts as the weight. The checkpoint enters as one witness among corpora, users, tools, and other models, and its knowledge aggregates with theirs in consensus. Model ingestion is not required; it only adds value.

## Before this stage

The whole chain through [23. Learning](Learning.md). [10. Recipes](Recipes.md): the safetensors provider. [6. Registries](Registries.md) operation 6.8: the operator templates.

## Operations, per checkpoint

### 24.1 Stage the checkpoint as a source generation

- **In:** the model files (Safetensors or GGUF).
- **Do:** [9. Sources](Sources.md): enumerate the artifact graph—config, tokenizer, weight shards or GGUF container, sidecars—with dispositions; identify each file in the substrate by its canonical trunk ([11. Content](Content.md) operation 11.2, using raw file byte-hashes only in the ingest journal to skip unchanged completed runs); the witness is the checkpoint's source trunk, its model name and revision recorded as content inside its source record, at trust class `AIModelProbe`, 0.50. Prefer unquantized Safetensors when available (since quantized GGUF/AWQ lose precision like MP3), while supporting both Safetensors and GGUF natively so any local checkpoint can be assimilated cleanly. The checkpoint's trunks establish its identity and provenance with `raw_weight_bytes_retained = 0` in durable storage.
- **Out:** the model as an active source generation with a witness trunk.
- **From:** `docs/plan/MODEL_INGESTION_DESIGN.md` §1; `docs/INVENTOR_RECORD.md` §Conventional models.

### 24.2 Read the container natively

- **In:** the Safetensors or GGUF files.
- **Do:** a native, memory-mapped C container reader (`src/model.c`) parses Safetensors or GGUF tensor metadata and embedded tokenizer/architecture keys once and decodes or dequantizes values in bulk as transient tile operands in memory. Managed code orchestrates lifecycle only; it is never the tensor inner loop, and raw weight blobs are never copied into PostgreSQL.
- **Out:** tensor descriptors and transient bulk tile access.
- **From:** `docs/plan/MODEL_INGESTION_DESIGN.md` §8; `docs/plan/ASSIMILATION_ROADMAP.md` workstream E1.

### 24.3 Decompose the tokenizer as one ordered composition

- **In:** the tokenizer files.
- **Do:** the vocabulary is one ordered composition whose trajectory ordinal is the model-local id. Each piece decodes through the exact tokenizer recipe and byte or string decoding to canonical underlying content where decodable; control pieces decode to their surface. A model-local piece, `str`, `Ġfoo`, a byte-fallback token, a sentencepiece boundary marker, is content as the file writes it, `Ġfoo` is `[Ġ,f,o,o]`, and an occurrence in the vocabulary, never promoted to a word because the tokenizer calls it a token, and never a private tier-0 alphabet. Merges are a trajectory, not `MERGES_WITH` testimony. Placing model tokens as anything other than text entities is sabotage.
- **Out:** the vocabulary entity, with its pieces as content and occurrences and its decodable content converging on shared identities.
- **From:** `docs/plan/MODEL_INGESTION_DESIGN.md` §3; `docs/plan/ASSIMILATION_ROADMAP.md` workstream E3.

### 24.4 Admit the configuration as facts

- **In:** the config and architecture files.
- **Do:** the config enters as facts on the checkpoint structure through governed scalar-valued relations: hidden size, number of layers, heads, KV heads, head dimension, feed-forward width, vocabulary size, tied embeddings, rotary base, normalization. Each value is a canonical scalar composition. Names such as embedding, Q, K, V, O, head, MLP, gate, up, down, router, expert, norm, layer, MLA, convolution, and diffusion block are coordinates of the source architecture, retained where the recipe needs them, and never the native ontology of Laplace cognition.
- **Out:** the structural facts of the checkpoint.
- **From:** `docs/plan/MODEL_INGESTION_DESIGN.md` §2; `engine/manifest/relation_types.toml` scalar-valued relations.

### 24.5 Recognize operators by shape

- **In:** the descriptors of 24.2, the config of 24.4, the templates of [6. Registries](Registries.md) operation 6.8.
- **Do:** bind the model dimension by axis frequency, the vocabulary size by the tokenizer, the layer count by path repetition, the rest from config, and a feed-forward width per instance; then match every tensor to a template: vocabulary projection, position and segment embeddings, norms, grouped-query self-attention, fused QKV in either orientation, latent attention, gated, fused-gated, and plain MLP, router, stacked experts, low-rank factor pairs. Names only break symmetries between equal shapes; undecided slots are ambiguous and unclaimed tensors are unrecognized, never guessed.
- **Out:** every tensor's source role, or its ambiguity.
- **From:** `docs/plan/ASSIMILATION_ROADMAP.md` law 14 and workstream E2.

### 24.6 Derive each circuit's physicality

- **In:** the recognized operators and their transient values.
- **Do:** a circuit's identity is its content, the composition of the salient coupled entities its trajectory orders, hashed like any composition. The model, plane, layer, and head where it was found, `[plane, layer, n, head, m]`, are observations of it under the model's source trunk and never part of its ID, so the same circuit found in two models is one entity with two witnesses. Its durable representation is a Projection physicality: an ordered trajectory of the salient coupled canonical entities, a coordinate and Hilbert value from placement, and the constituent count. Layer and head ordinals are the source's structural coordinates; two heads with the same ordinal are not the same circuit, and two differently numbered components can be functionally correlated. An order-sensitive factor trajectory preserves its order in the trajectory; a centroid cannot recover it. Native numeric, tensor, and factor kernels run over contiguous tiles.
- **Out:** one entity and one Projection physicality per circuit, with `raw_weight_bytes_retained = 0` in the receipt.
- **From:** `docs/plan/MODEL_INGESTION_DESIGN.md` §1 and §9; `docs/specs/09_Substrate_LM_Synthesis.txt` §Checkpoint witnessing.

### 24.7 Contract to empirically calibrated excitatory and inhibitory claims

- **In:** each circuit's coupling scores over the shared canonical entities.
- **Do:** extract the model's lottery-ticket structure via an **empirically calibrated two-sided significance contract** over each operator's own empirical score distribution and spectral energy—rather than a fixed top-*k*, an arbitrary constant floor, or a dogmatic one-sided Gaussian `z ≥ +√(2 ln N)` cutoff that miscalibrates heavy-tailed rotated spectra and throws away negative/inhibitory circuits! Specifically, calibrate positive and negative tail thresholds (`|z|` / tail-FDR / spectral-energy knee) per operator family against the tensor's empirical distribution: strongly positive couplings emit affirmative graded scores (`score > 0.5`), and **verified strongly negative / inhibitory couplings** (copy-suppression heads, antonym/exclusion circuits, gating inhibitions) emit inhibitory/refuting circuit evidence (`score < 0.5` or typed inhibitory circuit polarity), while the uninformative near-zero bulk is discarded (`raw_weight_bytes_retained = 0`). Token membership in a circuit is read directly from the circuit's `physicality.path` trajectory rather than duplicated as membership rows, no dense all-pairs table is persisted, and every calculated claim names its assimilation recipe and analyzer version.
- **Out:** calibrated excitatory and inhibitory model testimony under the checkpoint's witness trunk, folded by [13. Consensus](Consensus.md).
- **From:** `docs/plan/ASSIMILATION_ROADMAP.md` laws 12, 13; `docs/INVENTIONS.md` #102, #106; `docs/specs/08_Record_vs_Calculate_Spec.txt`.

### 24.8 Optionally, trace deep contextual activations as a versioned calculation

- **In:** the checkpoint and a pinned set of reference corpus trajectories (or a companion sparse dictionary / transcoder checkpoint).
- **Do:** static weight contraction (24.6–24.7) extracts direct embedding, unembedding, shallow attention, and factor couplings with zero model inference, while deep residual-stream attention heads and MoE routers often operate in context-rotated subspaces. When deeper circuit recovery is wanted, **optional deterministic activation / circuit tracing** over pinned corpus trajectories (recording which deep heads, MLP factors, MoE experts, or sparse-autoencoder features activate and couple entities in context) runs on CPU under a fully pinned calculation recipe—recording checkpoint trunk, input trajectory IDs, numeric precision, and analyzer version—and deposits those deep contextual circuit physicalities and claims as `DerivedCalculation` / `AIModelProbe` testimony ([30. Conflicts](Conflicts.md) C8). Repeating an identical deterministic trace produces no duplicate corroboration.
- **Out:** optional deep-layer contextual circuit trajectories and claims with reproducible calculation receipts.
- **From:** `docs/INVENTION.md` §14; `docs/plan/MODEL_INGESTION_DESIGN.md` §5; [Research: Model Ingestion](../Research/Models.md); [30. Conflicts](Conflicts.md) C8.

### 24.9 Read the model as a witness

- **In:** a query.
- **Do:** the model's evidence participates in [20. Forward](Forward.md) like any other witness. Ask which layers and heads `King` appears in; how this model differs from that one; whether layer X head Y of one correlates with layer N head M of another, calculated from shared entity coverage, trajectories, coupling behaviour, Procrustes or other declared operators, and observed outcomes, never from ordinal or tensor-path equality. Source-scoped A, B, and pooled A+B are inspection and ablation scopes over authorized evidence, not a cheaper product's reduced world.
- **Out:** typed, receipted answers about and from the model.
- **From:** `docs/plan/MODEL_INGESTION_DESIGN.md` §10; `docs/INVENTIONS.md` #55, #56.

### 24.10 Seat every model at the round table

- **In:** several ingested models.
- **Do:** each assimilated checkpoint contributes testimony to the exact same canonical entity and predicate space; `King` from `Qwen` is `King` from `Llama` and `DeepSeek` because all three resolve to the exact same text entity `lp_id`. Because independently trained model families have distinct causal lineages ([13. Consensus](Consensus.md) operation 13.3—never capped together as one witness merely because they share `AIModelProbe` trust class!), agreement across `Llama + Qwen + DeepSeek` genuinely strengthens `consensus` standing while curated standards and lexicons anchor factual truth above them. The pooled construction is one consensus substrate read by one forward pass emitting one answer—not a tensor average, not concatenated vocabularies, not runtime MoE routing over original weight blobs, and not *N* model completions judged by a hidden LLM. Architectures need not match: causal, encoder, reranker, MoE, and multimodal checkpoints compound in the same four tables, and disagreements stay inspectable per witness.
- **Out:** one answer that is the models and more.
- **From:** `docs/specs/09_Substrate_LM_Synthesis.txt` §Pooled heterogeneous-model consensus; `docs/specs/12_Mold_A_Model_Synthesis_Map.txt` §Round-table law; `docs/INVENTOR_RECORD.md` §Conventional models.

### 24.11 Receipt the ingest

- **In:** the run.
- **Do:** report artifacts, tensors, components, and scalars decoded; entities and trajectories reused against newly admitted; factor and circuit trajectories; calculation and evidence cells derived; kernel invocations and tile widths; boundary crossings; CPU, memory, I/O, database, and accelerator work; provider, precision, and recipe identity; and result fingerprints. An optional GPU or AVX provider holds semantics constant and proves parity under the declared numeric contract; installed hardware is not proof the world is GPU-resident.
- **Out:** the model-ingest receipt.
- **From:** `docs/plan/MODEL_INGESTION_DESIGN.md` §12.

## What this stage leaves behind

A checkpoint reduced to what carries information: its structure as content and references, its circuits as content entities with trajectories and placement, found at the model's layers and heads, its knowledge as graded, witnessed claims that compete on an even playing field with every other source, and nothing that could be copied back out as the model it came from.

## Without this stage

Laplace works, from corpora alone. With it, conventional models are consumed rather than competed with.
