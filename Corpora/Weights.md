# Weights

The Engine's dedicated `laplace model` command reads local model weights and reports native tensor analysis, while database assimilation and model export remain separate roadmap work.

## Source

Models use a dedicated binary reader rather than text corpus recipes. The Engine's [model.c](https://github.com/SaltyPatron/Laplace-Engine/blob/main/src/model.c) reads a local model directory, its configuration and vocabulary, and its safetensors weights. It analyzes attention and feed-forward projections through Native/MKL and reports the results; this command currently does not load those reports into PostgreSQL.

The monorepo also has an existing [ModelDecomposer](https://github.com/SaltyPatron/Laplace/blob/main/app/Laplace.Decomposers/Model/ModelDecomposer.cs) route. Its existence is distinct from convergence on the Native owner, complete model admission, `laplace-blake3-v1` export and royalty attribution. Those are tracked by [Native#6](https://github.com/SaltyPatron/Laplace-Native/issues/6) and [Laplace#1719](https://github.com/SaltyPatron/Laplace/issues/1719). A successful diagnostic run is not evidence of completed model assimilation.

Use existing model files under `LAPLACE_MODELS`; HART-DESKTOP must not download large checkpoints for verification.

## Format

| Artifact | Current Engine reader | Companion content |
| --- | --- | --- |
| safetensors weights | dedicated native model command | configuration and tokenizer/vocabulary files from the same model directory |
| GGUF, PyTorch checkpoints and exported cartridges | support must be established by the corresponding model/export implementation | the model's format metadata and tokenizer contract |

The presence of a model card or file extension does not establish reader support or a populated substrate.
