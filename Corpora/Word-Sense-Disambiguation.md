# Word sense disambiguation

A dataset of the WSD evaluation framework attests the words of each sentence, their lemma and part of speech, every dataset as a witness of its own; the ids the data files write (`d000.s000.t000`) number the framework's documents, sentences and tokens in order, positions in its own files and not attested, and the gold keys and the systems' answers, which name instances only by those ids, are not read; the README files, schema and candidate list attest nothing.

The source is the unified evaluation framework of Raganato, Camacho-Collados and Navigli (2017) at [lcl.uniroma1.it/wsdeval](http://lcl.uniroma1.it/wsdeval/). Every dataset is its own witness, named as the framework names its directory.

## Sources

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `wsd-evaluation-framework` | the dataset's directory name, `SemCor`, `senseval2`, `ALL` | class `AcademicCurated` | `princeton-wordnet`, `cili` | `*.data.xml` | [`data.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wsd-evaluation-framework/data.recipe) |
| `wsd-evaluation-framework` | the directory the file is in | class `AcademicCurated` | | `schema.xsd` | [`schema.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wsd-evaluation-framework/schema.recipe) |
| `wsd-evaluation-framework` | none: read as text | | | `README`, `PROVENANCE.md` | [`documentation.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wsd-evaluation-framework/documentation.recipe) |

`Data_Validation/sample-dataset` repeats `semeval2015` byte for byte and is read there; `semcor+omsti.data.xml` is not read, as the source says.

## The data files

A record is one sentence: the path of its words, in order (`words sentence wf instance`). What is said of a word is said of the word within its sentence, every name and value as the file writes it.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `<corpus lang="en" source="senseval2">` | the root | nothing: no thing is inside none | none | |
| `<text id="d000">` | an element | not a thing; its `id` the document's number in the framework, `d` and its position, not attested (`key id`) | none | "corpus -> text -> sentence" |
| `<sentence id="d000.s000">` | inside a text | the record of its words; its `id` its position, the document's number and its own, not attested | the record `[[This, document, is, …], [This, lemma, this], …]` | |
| `<wf lemma="this" pos="DET">This</wf>`, `<instance id="…" lemma="document" pos="NOUN">document</instance>` | word elements | the word, its text; `lemma` and `pos` said of it as it stands in its sentence; an instance's `id` its position, not attested | `[This, lemma, this]`, `[This, pos, DET]` | "Both types should contain two mandatory attributes ("lemma" and "pos")." |

The record is witnessed once, as one attestation, by the dataset whose directory the file is in.

## Not read

The gold keys (`*.gold.key.txt`), the systems' answers (`*.key`), `candidatesWN30.txt` and the `ili_mapped` tables point at instances by the framework's ids and nothing else: an id is only a position, so a row says its sense key of the word at that position, and no recipe reads them yet. The sense keys themselves are content, identifiers the highway's `ili` list holds. When an id points at a word across files of one source ([Recipes](../Reference/Recipes.md#what-each-named-part-is): `refer`), the gold keys can say of each instance's word the concept it is annotated with; that is not yet written for XML words. `schema.xsd` is recorded as its syntax tree; the READMEs and `PROVENANCE.md` are read as text: observed content that attests nothing.
