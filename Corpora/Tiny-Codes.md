# Tiny codes

Tiny Codes is a multi-language instructional code-synthesis Parquet corpus queued for declarative `.recipe`, native Parquet, and Tree-sitter AST admission (`Batch 3`, `Laplace#894`), pairing structured natural-language specifications with parsed code ASTs across programming languages.

## Source & `Batch 3` admission queue

Tiny Codes ([`nampdn-ai/tiny-codes`](https://huggingface.co/datasets/nampdn-ai/tiny-codes)) is queued for `Batch 3` code admission (`Laplace#894`, [INVENTOR_RECORD](../Repositories/Laplace/docs/INVENTOR_RECORD.md): *"parquet files from tiny codes, whatever i have downloaded from stackv2... we have coding corpus"*). Admitted as one corpus trunk (`Tiny Codes`, `class AIModelProbe`, since its tasks and solutions are synthetically generated), native Parquet reading + language-dispatched Tree-sitter grammars decompose each `response` snippet into its exact syntax tree rather than flat text lines.

Under the Recording Law ([Corpora](README.md#page-shape), [26. Code](../Sequence/Code.md)):

- **Row `idx` omitted as internal pointer:** The integer `idx` column is a dataset row index (`key row idx`), resolved and recorded nowhere.
- **Language-routed AST decomposition:** `programming_language` (`Python`, `C++`, `Rust`, `TypeScript`, `Julia`, `Go`, `C#`, `Java`, `SQL`, `Bash`, ...) routes `response` (unwrapping Markdown code fences where present) through the matching compiled Tree-sitter grammar in `$LAPLACE_GRAMMARS` so functions, types, control flow, and identifiers share canonical AST subtrees with [Code corpus](Code-Corpus.md) and [Code authority](Code-Authority.md).

## Publisher record format

| Record | Fields in order | Target Laplace semantics | Specification |
| --- | --- | --- | --- |
| Instructional code row (`part_*.parquet`, 9 shards) | `prompt`, `main_topic`, `subtopic`, `adjective`, `action_verb`, `scenario`, `target_audience`, `programming_language`, `common_sense_topic`, `idx`, `response` | `idx` omitted (`key`); `prompt` decomposed by UAX #29; `response` parsed into its language AST via `programming_language`; attests `[prompt, programming_language, response_ast]` together with task-slot qualifiers (`main_topic`, `subtopic`, `action_verb`, `scenario`, `common_sense_topic`, `target_audience`) under `class AIModelProbe` | [Tiny Codes dataset card](https://huggingface.co/datasets/nampdn-ai/tiny-codes) |
