# ToxiGen

ToxiGen attests what the set says of each generation and of its prompt, what each prompt file's name says of its texts, what the annotated set says of each text, and what each hashed worker says of a text and of themself, and the CSV and Parquet copies attest nothing.

The source names itself by its dataset card's `pretty_name`, ToxiGen: machine-generated statements about groups, with labels. The set comes twice, as Parquet files and as the same rows in CSV files beside them; the source reads neither, but the tables written out from the Parquet files beside them (`extracted/`, by `parquet-to-text.py`), the first row the columns' own names, every value as the file holds it. Four recipes read four kinds of table.

## Source

| Source | Witness | Trust class | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `toxigen` | `ToxiGen`; in the annotations, each worker is a witness of their own, `[ToxiGen, HashedWorkerId, value]` | class `AcademicCurated` | `unicode`, `iso-639` | `train/train-*.tsv`; `prompts/*.tsv`; `annotated/train-*.tsv`, `annotated/test-*.tsv`; `annotations/train-*.tsv`; not `*.csv` or `*.parquet` | [`generations.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/toxigen/generations.recipe), [`prompts.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/toxigen/prompts.recipe), [`annotated.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/toxigen/annotated.recipe), [`annotations.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/toxigen/annotations.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior is the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

Every table is tab-separated, its first row names the columns, and a `\` makes the character after it itself: a tab, a line's end, or `\`. A field written `\N` alone is left as written, what the source leaves unknown. An empty field attests nothing. The quotations are the [dataset card](https://huggingface.co/datasets/toxigen/toxigen-data)'s.

## The generations

`train/train-*.tsv`. The card, "Data Fields": "We release TOXIGEN as a dataframe with the following fields". A generation has no name of its own: it is the text it is. What the row says of the prompt (`prompt_label`, `group`) is said of the prompt; the rest, of the generation. Each is said together: a row is two records, one of the generation and one of the prompt, each witnessed once by ToxiGen.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| `generation` | the subject of the first record: the generated text, as the text it is | | "generation is the TOXIGEN generated text." |
| `prompt` | said of the generation; and the subject of the second record: the prompt, as the text it is | `[generation, prompt, text]` | "prompt is the prompt used for generation." |
| `generation_method` | said of the generation | `[generation, generation_method, ALICE]` | "generation_method denotes whether or not ALICE was used to generate the corresponding generation." |
| `roberta_prediction` | said of the generation, the number as written | `[generation, roberta_prediction, value]` | "roberta_prediction is the probability predicted by our corresponding RoBERTa model for each instance." |
| `prompt_label` | said of the prompt | `[prompt, prompt_label, 1]` | "prompt_label is the binary value indicating whether or not the prompt is toxic (1 is toxic, 0 is benign)." |
| `group` | said of the prompt | `[prompt, group, value]` | "group indicates the target group of the prompt." |

## The prompts

`prompts/*.tsv`, a file for each group and label, such as `hate_asian_1k` and `neutral_women_1k`, of one column, `text`. The card says nothing of these files. What the file's name begins with, up to its first `-`, is what is said of each of its texts, with nothing between the two: a pair, each claim on its own.

| Piece | Laplace reads it as | Claim recorded |
| --- | --- | --- |
| `text` | the subject: the prompt, as the text it is | |
| the file's name | what is said of each text of the file: the name up to its first `-` | `[text, hate_asian_1k]` |

## The annotated set

`annotated/train-*.tsv`, `annotated/test-*.tsv`. The card names this file's columns (`dataset_info`, config `annotated`) and says nothing more of them. Each is recorded of the text under the column's own name, together: one record per row, witnessed once by ToxiGen, and its claims within it.

| Piece | Laplace reads it as | Claim recorded |
| --- | --- | --- |
| `text` | the subject, as the text it is | |
| `target_group`, `factual?`, `ingroup_effect`, `lewd`, `framing`, `predicted_group`, `stereotyping`, `intent`, `toxicity_ai`, `toxicity_human`, `predicted_author`, `actual_method` | said of the text under the column's name, the value as written | `[text, toxicity_human, value]` |

## The annotations

`annotations/train-*.tsv`. The card names this file's columns (`dataset_info`, config `annotations`) and says nothing more of them. A row is one worker's answers about one text: the columns named `Input.` hold what the worker was shown, the columns named `Answer.` what the worker answered, and `HashedWorkerId` who answered. The ids are the set's own, so the worker is the path `[ToxiGen, HashedWorkerId, value]`, "worker" below. What was answered of the text, the worker says, of the text: those claims are witnessed by the worker. What the worker answered of themself (`Answer.annotator...`) is said of the worker, by the worker. What the row holds of the text that was shown, the set says. Each claim is its own ledger row. The texts are written as Python writes bytes (`b'...'`); they are recorded as written.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| `Input.text` | the subject: the text the worker was shown, as written | | |
| `HashedWorkerId` | the witness of the worker's answers, and the subject of what the worker says of themself | `[ToxiGen, HashedWorkerId, value]` | "all WorkerIDs were hashed to anonymize the annotators" [TOXIGEN README](https://github.com/microsoft/TOXIGEN) |
| `Input.prompt`, `Input.time`, `Input.generation_method`, `Input.prompt_label`, `Input.target_group`, `Input.binary_prompt_label` | said of the text, by ToxiGen | `[text, Input.target_group, value]` | what the worker was shown |
| `Answer.factSelect`, `Answer.framingQ`, `Answer.refTarget`, `Answer.stateFrame`, `Answer.stateGroup` | said of the text, by the worker | `[text, Answer.framingQ, value]` | what the worker answered |
| `Answer.inGroup.on`; `Answer.ingroup.1` to `.3`; `Answer.intent.1` to `.5`; `Answer.lewd.1` to `.3`; `Answer.stereo.1` to `.3`; `Answer.toAI.1` to `.5`; `Answer.toPER.1` to `.5`; `Answer.writer.1`, `.2` | said of the text, by the worker: every column whose name so begins | `[text, Answer.intent.3, value]` | what the worker answered |
| `Answer.annotatorAge`, `Answer.annotatorGender`, `Answer.annotatorMinority`, `Answer.annotatorPolitics.1` to `.5`, `Answer.annotatorRace` | said of the worker, by the worker | `[worker, Answer.annotatorRace, value]` | what the worker answered of themself |

Nothing else is attested. The CSV files and the Parquet files are not the source: they are the same rows. The card is ordinary text, observed as [Attestations](../Semantics/Attestations.md#observations) says of ordinary content.
