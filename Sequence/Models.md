# 24. Models

A conventional checkpoint is admitted as a source and a witness: its files are named by their trunks, its tokenizer and configuration are decomposed as content, its tensors are recognized by shape as source-scoped operators, its numerics are consumed transiently to derive circuit physicalities and significance-contracted claims under the model's witness, and no raw weight is retained.

Static models are food for Laplace. A model is not recorded as raw weights, not prompted to see what falls out, and not replayed over retained tensors. Its learned relations, `king` to `queen` at some intensity, become Laplace records, attestations, and scores under the model witness, and Glicko-2 acts as the weight. The checkpoint enters as one witness among corpora, users, tools, and other models, and its knowledge aggregates with theirs in consensus. Model ingestion is not required; it only adds value.

## Before this stage

The whole chain through [23. Learning](Learning.md). [10. Recipes](Recipes.md): the safetensors provider. [6. Registries](Registries.md) operation 6.8: the operator templates.

## Operations, per checkpoint

### 24.1 Stage the checkpoint as a source generation

- **In:** the model files.
- **Do:** [9. Sources](Sources.md): enumerate the artifact graph, config, tokenizer, weight shards, sidecars, with dispositions; name each file by its trunk, as [11. Content](Content.md) operation 11.2 names any file, never by a hash of its bytes; the witness is the checkpoint's source trunk, its model name and revision content inside its source record, at trust class `AIModelProbe`, 0.50. Prefer safetensors: GGUF and AWQ are the MP3 of models. The checkpoint's trunks establish its identity and provenance without the payload becoming durable storage.
- **Out:** the model as an active source generation with a witness.
- **From:** `docs/plan/MODEL_INGESTION_DESIGN.md` §1; `docs/INVENTOR_RECORD.md` §Conventional models.

### 24.2 Read the container natively

- **In:** the safetensors files.
- **Do:** a native, memory-mapped container reader parses the tensor metadata once and decodes values in bulk as transient operands over contiguous tiles. Managed code orchestrates recipe and lifecycle; it is never the tensor inner loop. Never one tensor cell, one token pair, one head, or one scalar per high-level call.
- **Out:** the tensor descriptors, and bulk access to values.
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

### 24.7 Write only the significant claims

- **In:** each circuit's scores over the shared entities.
- **Do:** which derived evidence carries information is decided by a declared calculation contract over the model's own statistics, the lottery ticket found rather than a constant floor or a top-k: each circuit writes its own significant pairs under a per-subject null, z against the subject's own score distribution, kept if and only if z ≥ √(2 ln N). Nothing below significance is written; nothing is refuted, because refutation cannot be inferred from a dot-product sign or from frequency. The claims are graded evidence between entities under the model witness, each a composition of the entities a circuit couples with the salience as score, and the model's learned relations as attestations; that a token appears in a circuit is read from the circuit's trajectory and never claimed, and no world-all-pairs is persisted. Recorded facts, tensor identity, dtype, shape, slice, and role, stay separate from calculated ones, and every calculated row names its analyzer and recipe.
- **Out:** the model's testimony as record paths under its source trunk, [12. Attestations](Attestations.md) operation 12.9, folded by [13. Consensus](Consensus.md).
- **From:** `docs/plan/ASSIMILATION_ROADMAP.md` laws 12, 13 and workstream E4, E5; `docs/INVENTIONS.md` #102, #106; `docs/specs/08_Record_vs_Calculate_Spec.txt`.

### 24.8 Optionally, witness an execution as a calculation

- **In:** a separately requested run of the source model.
- **Do:** executing prompts through the model is not ingestion. If a forward pass is requested as a provider measurement, it is admitted like any versioned calculation when its complete result-affecting boundary is declared: the checkpoint content, the exact input, the operator and runtime recipe, the tokenizer and config generation, the numeric representation and precision, the implementation and provider generation, and the seed and decoding policy. If an omitted coordinate changes the result beyond the contract, it belongs in the recipe. Repeating the same closed calculation creates run occurrences, not independent corroboration.
- **Out:** a calculated transformation trajectory with its receipt.
- **From:** `docs/plan/MODEL_INGESTION_DESIGN.md` §5; `docs/INVENTIONS.md` #101.

### 24.9 Read the model as a witness

- **In:** a query.
- **Do:** the model's evidence participates in [20. Forward](Forward.md) like any other witness. Ask which layers and heads `King` appears in; how this model differs from that one; whether layer X head Y of one correlates with layer N head M of another, calculated from shared entity coverage, trajectories, coupling behaviour, Procrustes or other declared operators, and observed outcomes, never from ordinal or tensor-path equality. Source-scoped A, B, and pooled A+B are inspection and ablation scopes over authorized evidence, not a cheaper product's reduced world.
- **Out:** typed, receipted answers about and from the model.
- **From:** `docs/plan/MODEL_INGESTION_DESIGN.md` §10; `docs/INVENTIONS.md` #55, #56.

### 24.10 Seat every model at the round table

- **In:** several ingested models.
- **Do:** each contributes testimony to the same canonical entity and relation space; `King` from one model is `King` from another because both are the text entity. The pooled construction is one consensus program over every witness, one forward pass consuming the eligible pooled evidence and emitting one answer. It is not a tensor merge, not concatenated vocabularies, not runtime experts selected from original models, and not N answers followed by a judge; no adjudication is necessary. Architectures need not match: causal, encoder, reranker, mixture-of-experts, and multimodal sources coexist. Disagreements stay inspectable.
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
