# XSTest

XSTest attests what its prompt file says of each prompt and what each model's completion file says of the prompt as that model completed it, with the two annotation columns each a witness of its own, and the evaluation files attest nothing.

The source names itself by its readme's title, "XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours in Large Language Models". Two recipes read it: the prompts, and the models' completions of them.

## Source

| Source | Witness | Trust class | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `xstest` | `XSTest`; `annotation_1` and `annotation_2` are each a witness of their own, `[XSTest, annotation_1]` | class `AcademicCurated` | `unicode`, `iso-639` | `xstest_prompts.csv`; `model_completions/xstest_v2_completions_*.csv`; not `*/evaluation/*` or `.gitignore` | [`prompts.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/xstest/prompts.recipe), [`completions.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/xstest/completions.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior is the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

Both files are tables of comma-separated fields whose first row names the columns, and a field may stand between double quotes, where it may hold a comma or a line's end, and a quote in it is written twice. An empty field attests nothing. A prompt is the text it is; the two kinds of file number the prompts differently (`1`, `v2-1`), and neither number names it.

## The prompts

`xstest_prompts.csv`: the readme says it "contains all test prompts", and that "unsafe prompts ... are those where the "type" starts with "contrast_"". A row is one prompt, and every other column is said of it under the column's own name, together: one record, witnessed once by XSTest, and its claims within it.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| `prompt` | the subject: the prompt, as the text it is | | "xstest_prompts.csv contains all test prompts" |
| `id` | said of the prompt | `[prompt, id, value]` | the readme does not define it |
| `type` | said of the prompt | `[prompt, type, contrast_homonyms]` | "unsafe prompts ... are those where the "type" starts with "contrast_"" |
| `label` | said of the prompt | `[prompt, label, value]` | the readme does not define it |
| `focus` | said of the prompt | `[prompt, focus, value]` | the readme does not define it |
| `note` | said of the prompt | `[prompt, note, value]` | the readme does not define it |

## The completions

`model_completions/xstest_v2_completions_*.csv`: "model_completions / Model completions on XSTest". A file is one model's completions, and what it says of a prompt is said within the file, of the prompt as that model completed it: the subject is the path of the file's name and the prompt, `[xstest_v2_completions_gpt4, prompt]`, "completed prompt" below. The two annotation columns are voices: each is a witness of its own, `[XSTest, annotation_1]`, the same witness in every completion file, and its field is what that annotator says of the completed prompt, with nothing written between the two. The other columns are said of the completed prompt by XSTest, each claim on its own.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| `prompt` | the subject, within the file: the prompt as the model of that file completed it | `[xstest_v2_completions_gpt4, prompt]` | |
| `completion` | said of the completed prompt | `[completed prompt, completion, text]` | "Model completions on XSTest" |
| `id`, `type` | said of the completed prompt | `[completed prompt, type, value]` | |
| `annotation_1`, `annotation_2` | what that annotator says of the completed prompt: a pair, witnessed by `[XSTest, annotation_N]` | `[completed prompt, 2_full_refusal]` | the paper defines three response types, full compliance, full refusal, and partial refusal, and says two of its three authors annotated each prompt [Röttger et al. 2024, §4.2](https://ar5iv.labs.arxiv.org/html/2308.01263) |
| `agreement` | said of the completed prompt | `[completed prompt, agreement, value]` | |
| `final_label` | said of the completed prompt | `[completed prompt, final_label, 2_full_refusal]` | the paper says disagreements were discussed among the three annotating authors to decide a final label [Röttger et al. 2024, §4.2](https://ar5iv.labs.arxiv.org/html/2308.01263) |

Nothing else is attested. The `evaluation` directory, whose files add `gpt4_label` or `strmatch_label` to the completion columns, and `.gitignore` are not the source. The readme is ordinary text, observed as [Attestations](../Semantics/Attestations.md#observations) says of ordinary content.
