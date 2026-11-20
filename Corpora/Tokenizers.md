# Tokenizers

A model tokenizer (`tokenizer.json`, `tokenizer.model`, or GGUF vocabulary metadata) is both recorded losslessly as structured file content and decoded from subword transport notation (`Ġ`, `▁`, `##`, byte-level BPE) onto canonical Tier-0 and UAX #29 UTF-8 text `lp_id`s so every assimilated model shares the open `laplace-blake3-v1` Merkle vocabulary.

The `tokenizers` source reads model tokenizer files under `$LAPLACE_MODELS` (`*/tokenizer.json` and Hugging Face hub snapshots `models--*/snapshots/*/tokenizer.json`), paired with native vocabulary decoding during checkpoint assimilation ([Weights](Weights.md), [Research: Models](../Research/Models.md#vocabularies-as-content)).

## Source

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `tokenizers` | `Model tokenizers` source trunk | class `UserCuratedResource` | `unicode` | `tokenizer.json` across `$LAPLACE_MODELS` (plus `tokenizer.model` / GGUF vocabulary tables during model assimilation) | [`recipes/tokenizers/source`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/tokenizers/source) (`reads json`; subword-to-UTF-8 text binding in `src/model.c` / `Batch 3` `Laplace#1719`) |

## Two-level contract: lossless JSON tree & canonical UTF-8 text decoding

Under the Recording Law ([INVENTOR_RECORD](../Repositories/Laplace/docs/INVENTOR_RECORD.md): *"placing AI model tokens as anything other than text entities is rape and sabotage"*), Laplace never treats BPE, WordPiece, or Unigram integer IDs or raw subword transport glyphs as isolated model-private symbols:

1. **Lossless file observation (`reads json`):** `tokenizer.json` ([Hugging Face tokenizers](https://huggingface.co/docs/tokenizers/api/models)) is decomposed as its exact JSON syntax tree (`model.type`, `model.vocab`, `model.merges`, `added_tokens`, `normalizer`, `pre_tokenizer`, `decoder`), recomposing byte for byte and deduplicating identical tokenizer files across model derivatives onto one file trunk.
2. **Subword decoding onto canonical UTF-8 text `lp_id`s (`laplace-blake3-v1`):** Each vocabulary entry's transport encoding—GPT-2/RoBERTa/Qwen/Llama-3 byte-level BPE (`Ġ` → U+0020 space, `Ċ` → U+000A newline, `Ā`..printable byte-to-Unicode table), SentencePiece/Unigram `▁` (U+2581 → U+0020 space), WordPiece `##` continuation prefixes, and `<0xXX>` byte fallbacks—is inverted through the tokenizer's declared `decoder` / `pre_tokenizer` specification to recover the exact UTF-8 character/word/phrase entity (`lp_id`) in the universal Merkle DAG (marking special control tokens such as `<|endoftext|>` or `<unk>` as format control markers rather than lexical words).

| Piece | Written as | Laplace reads it as | Target representation & current state |
| --- | --- | --- | --- |
| `model.vocab` entry | `"ĠKing": 14821`, `"▁King": 4219`, `"##ing": 2075` | JSON member in the file tree **plus** decoded UTF-8 text entity (`[" ", "King"]` / `"King"`, `"ing"`) mapped from vocabulary row `id` during model assimilation | lossless JSON syntax tree active in `recipes/tokenizers/source`; full byte-BPE / `▁` / `##` / `<0xXX>` decoding onto canonical UTF-8 `lp_id`s powers `Weights` assimilation in `Batch 3` (`Laplace#1719`) |
| `added_tokens` | `{"id": 128000, "content": "<\|begin_of_text\|>", "special": true}` | JSON object in the file tree; `special: true` flags delimiter/control tokens so they are never confused with natural-language words | preserved in JSON tree; control-token gating wired in `src/model.c` (`Batch 3`) |
| `model.merges`, `normalizer`, `pre_tokenizer`, `post_processor`, `decoder` | BPE merge pairs and pipeline rules | lossless JSON tree + exact deterministic specification for inverting subword strings to UTF-8 text | preserved byte for byte |
