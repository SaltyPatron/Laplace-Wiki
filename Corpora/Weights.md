# Weights

Conventional AI checkpoints (`Safetensors` and `GGUF`) assimilate into Laplace by shape-driven operator recognition, transiently reducing tensor weights into circuit trajectories and Glicko-2-scored token, head, and layer attestations with zero raw weight bytes retained (`raw_weight_bytes_retained = 0`), and powering CPU Mold-a-Model `laplace-blake3-v1` export.

Under the Recording Law ([INVENTOR_RECORD](../Repositories/Laplace/docs/INVENTOR_RECORD.md), [24. Models](../Sequence/Models.md), [25. Export](../Sequence/Export.md)), an AI model is admitted as one source trunk and one witness (`class AIModel`) in native C ([`Laplace-Engine/src/model.c`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/src/model.c) + `Laplace-Native` SIMD/MKL/Eigen/Spectra kernels)—never stored as opaque binary weight blobs and never decomposed through legacy C# walkers.

## Shape-driven assimilation & zero retained weights

Whether a checkpoint comes from a dense transformer, Mixture-of-Experts (MoE), encoder/reranker, or diffusion/vision-language family, container parsing separates format framing (`Safetensors` JSON header + mmap'd tensor buffers, preferred lossless fp16/bf16/fp32 source; `GGUF` metadata KV + quantized blocks) from **shape-driven operator classification**:

1. **Vocabulary grounding onto canonical UTF-8 text (`laplace-blake3-v1`):** Every vocabulary row index `0..V-1` resolves via [Tokenizers](Tokenizers.md) onto its decoded UTF-8 text `lp_id` (`"King"` in Qwen == `"King"` in Llama == `"King"` in WordNet), never minting model-private integer token IDs.
2. **Shape-first operator recognition:** Tensor dimensions `(V, d_model)`, `(n_heads * d_head, d_model)`, `(n_kv * d_head, d_model)`, `(d_ff, d_model)`, `(n_experts, ...)`, and `(d_model,)` classify token embeddings, `Q`/`K`/`V`/`O` attention projections, `gate`/`up`/`down` MLP projections, norms, RoPE frequencies, and routers from `config.json` / GGUF hyper-parameters and tensor shapes—using tensor names as corroborating provenance rather than hardcoded provider regexes.
3. **Transient spectral/significance contraction (`raw_weight_bytes_retained = 0`):** Native CPU kernels project embedding/unembedding couplings, `Q`/`K` interaction and `V`/`O` value-routing circuits, and MLP feature activations over the canonical text vocabulary, detecting each operator's intrinsic noise/Lottery-Ticket significance floor rather than applying an arbitrary fixed top-`k` cutoff. Significant couplings emit ordered circuit trajectories (`physicality`) and calibrated game-series claims (`attestation` → Glicko-2 `consensus`) under the model's witness trunk; raw floating-point/quantized weight arrays are discarded once reduced (`raw_weight_bytes_retained = 0`).
4. **Round-table consensus & CPU Mold-a-Model export:** Multiple assimilated checkpoints meet curatorial corpora on the **same** 4 tables without a separate judge (`round-table` consensus), and CPU Mold-a-Model synthesis ([25. Export](../Sequence/Export.md)) exports clean `laplace-blake3-v1` `Safetensors` and `GGUF` checkpoints from attested standing and trajectories without gradient descent, preserving exact Fisher `SUM(share_bp) = 10000` witness attribution.

## Current Engine state vs. `Batch 3` (`Laplace#1719`)

| Artifact | Target specification | Current `Laplace-Engine` state & `Batch 3` closure |
| --- | --- | --- |
| `*.safetensors` + `config.json` + `tokenizer.json` | Shape-driven assimilation of embeddings, `Q`/`K`/`V`/`O` heads, MLP/MoE circuits, and norms into `entity`, `physicality`, `attestation`, and `consensus` (`raw_weight_bytes_retained = 0`) | `src/model.c` (`laplace model`) maps `Safetensors` + vocabulary and runs native MKL/SVD operator analysis; full database stage/merge assimilation and CPU Mold-a-Model synthesis close in `Batch 3` (`Laplace#1719`) |
| `*.gguf` checkpoints | Native `GGUF` header/KV + dequantized block reader feeding the identical shape-driven assimilation pipeline; clean `laplace-blake3-v1` `GGUF` / `Safetensors` export validated in `llama.cpp` | Native `GGUF` assimilation + `laplace-blake3-v1` export proven end-to-end in `llama.cpp` with `share_bp = 10000` attribution in `Batch 3` (`Laplace#1719`) |

Existing local checkpoints under `$LAPLACE_MODELS` (`E:\Data\Ingest` / `/vault/models`) are used for verification; `HART-DESKTOP` never bulk-downloads checkpoints over metered links.
