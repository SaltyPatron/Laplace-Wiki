# Model Ingestion

First measurements of AI models as sources: a farm of 33 models surveyed from metadata alone, every tokenizer ingested as content, three models' embeddings recorded as witnessed testimony, and one model interviewed with templates taken from the corpus, all graded against the attested web.

Every number on this page was measured on the local model farm with prototype tools. The reference machine, database, and tools are described in [Engine Measurements](Engine.md).

## The farm, from metadata

A scan of 33 model directories read each one's configuration, tokenizer, declared base model, and weight files, without reading any weights. It took 15 s and covered about 500 GB of checkpoints.

- **Tokenizers:** the 25 tokenizers form 8 families that share at least 99% of their token strings.
  - One vocabulary of 151,643 tokens is shared by 15 models from three organizations: Qwen's coder, embedding, reranker, and vision-language models, NVIDIA's music-flamingo, and Jina's reranker.
  - Microsoft's phi-2 and Florence-2 share a vocabulary, as do MiniLM and Grounding-DINO, which both use BERT's.
- **Declared lineage chains,** such as Qwen3-Embedding ← Qwen3-Base, and an AWQ quantization ← Qwen2.5-Coder-7B-Instruct ← Qwen2.5-Coder-7B.
- **Byte tokens:** the tokens that are not whole characters vary by family, from 256 raw-byte tokens (TinyLlama) to 1,448 byte-level tokens that are not valid UTF-8 by themselves (Qwen).

## Vocabularies as content

Each tokenizer's tokens were decomposed like any text.

- **Markers:** SentencePiece's `▁` and byte-level BPE's `Ġ` became the spaces they stand for.
- **Byte tokens:** each one became its notation, `<0xAB>`. A token that is part of a character became the composition of its bytes' notations.
- **The vocabulary:** each became the path of its tokens in index order.

The 24 tokenizer files held 2,700,090 tokens, which deduplicated to 240,450 compositions in 5.1 s. The files held 11 distinct vocabularies: files with identical token lists became one trunk. Vocabularies with the same tokens in a different order, or with other added tokens, stayed distinct, like Qwen2.5's and Qwen3's.

Once recorded, the vocabularies answer by query. Every vocabulary in the farm that holds `king` as one token also holds “ king”, “ King”, and `<0xE2>`, except BERT's WordPiece, which holds only `king`.

## Reading a model's weights

The kernel behind "token b beats token c, given token a" works in blocks of rows:

- one GEMM computes the block's scores against every candidate while they stay in cache;
- each row's mean and spread are accumulated;
- only candidates above the row's own noise floor are kept.

On TinyLlama-1.1B, with 12 threads at 213 GFLOP/s:

| Reading | Time | Candidates above z = 4, per row | What it shows |
| --- | --- | --- | --- |
| Token embeddings, all 32,000 × 32,000 | 19.9 s | 37.3 | inflections, case, synonyms, and translations |
| Embedding straight to the output layer | 18.4 s | 3.5 | noise |
| One attention head's query-key table | 0.6 s | 0.1–1.9 | attention sinks and positional patterns |
| All 5,632 feed-forward neurons of one layer | 3.0 s | 3.5 | tokens each neuron promotes |

The embedding held knowledge: “ king” → King, queen, Kings, Queen, rey, roi, prince, and “ Paris” → París, London, France, Milan, Пари, Vienna, Berlin.

The direct path from embedding to output skips every layer, and in a 22-layer model it is a weak remainder, not the model's next-word knowledge. Attention heads read from weights alone showed structure (one head routes every token to the newline and end-of-text tokens) rather than knowledge. What a deep head does has to be observed by running text through the model.

## Graded against the attested web

TinyLlama's embedding neighbours at z ≥ 4 were checked for 5,164 English words that are single tokens:

| Attested relation | Share of neighbours | Random tokens |
| --- | --- | --- |
| Sibling (a shared hypernym) | 4.8% | 0.17% |
| Inflection or case | 4.2% | 0.01% |
| Hypernym or hyponym | 2.4% | 0.03% |
| Same concept | 2.0% | 0.01% |
| Translation of the same concept | 1.3% | 0.02% |
| Other WordNet relation | 1.1% | 0.01% |
| **Any** | **15.7%** | **0.25%** |

That is 63 times chance. The rest are not errors by default: they are associations no curated source here records, awaiting other witnesses.

## Testimony from three families

The embeddings of three independently trained models, TinyLlama (Llama), MiniLM (BERT), and Qwen3-Embedding-0.6B (Qwen), were recorded as claims `[token, near, token]`.

- **Each neighbour** above z = 3, up to 64 per token, became one claim between the entities its tokens decompose to.
- **Each claim went into `attestation`** with the model as witness and the embedding as condition.
- **Standings were updated as the rows arrived**, with set-based statements:
  - a new claim entered at the model's trust;
  - a claim another lineage already held played one matchup;
  - testimony from the same lineage joined the witness set.

| Model | Claims attested | New | Already attested by another family |
| --- | --- | --- | --- |
| TinyLlama-1.1B | 2,037,624 | 2,037,624 | 0 |
| MiniLM-L6 | 1,901,175 | 1,839,077 | 27,672 |
| Qwen3-Embedding-0.6B | 9,706,816 | 9,404,287 | 302,529 |

In a sample of 300,000 of these claims, graded against same concept, hypernym or hyponym, and translation:

| Independent families attesting | Claims | Attested by the curated web |
| --- | --- | --- |
| 1 | 283,087 | 3.7% |
| 2 | 15,318 | 12.1% |
| 3 | 584 | 12.7% |

A relation that a second, independently trained model also finds is attested more than three times as often. Truths cluster across models as they do across wordnets. This grade leaves out siblings and inflections, and it includes Qwen's code and fragment tokens, so its absolute rates are lower than TinyLlama's alone.

## Interviewing a model with templates

For 285 frequent three-word contexts in the Gutenberg texts, such as "one of the …":

- **Laplace** counted the exact continuations inside its stored trajectories, in 84 ms each.
- **TinyLlama** gave its next word, by a forward pass on the CPU, in 2,217 ms each.

The model's first choice was the continuation Laplace observed most often 43.9% of the time, and that continuation was in the model's top five 61.8% of the time. Where they differ, the model's answers show the text it was trained on: "part of the …" gives equation, code, story, and "end of the …" gives line, day, string, against continuations counted in nineteenth-century books.

## Sources

- Local models: TinyLlama-1.1B-Chat-v1.0, all-MiniLM-L6-v2, Qwen3-Embedding-0.6B, and the rest of the farm, read from their safetensors, configuration, and tokenizer files.
- Guangxuan Xiao et al., [Efficient Streaming Language Models with Attention Sinks](https://arxiv.org/abs/2309.17453), 2023. Nelson Elhage et al., [A Mathematical Framework for Transformer Circuits](https://transformer-circuits.pub/2021/framework/index.html), 2021, describes the direct path as bigram statistics in shallow models.
- Research notes on model ingestion, with 57 further sources, are kept with the prototype's research data.
