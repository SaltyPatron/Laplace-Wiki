# Word sense disambiguation

The WSD evaluation framework (`SemCor`, `semcor+omsti`, and the five evaluation benchmarks) attests sentences, token lemmas and parts of speech, and gold sense bindings resolved from `*.gold.key.txt` across `d000.s000.t000` internal pointers onto `[lemma, eng, ILI]` lexicalizations under one corpus witness trunk.

The source is the unified WSD evaluation and training framework of Raganato, Camacho-Collados, and Navigli (2017) at [lcl.uniroma1.it/wsdeval](http://lcl.uniroma1.it/wsdeval/): `Training_Corpora` (`SemCor` and `SemCor+OMSTI`) and `Evaluation_Datasets` (`senseval2`, `senseval3`, `semeval2007`, `semeval2013`, `semeval2015`, and `ALL`). The entire framework is one source trunk and one witness (`Word Sense Disambiguation: A Unified Evaluation Framework`); individual datasets are directories of files under that trunk (`Data_Validation/sample-dataset` is excluded only because it duplicates `semeval2015` byte for byte).

## Sources

| Source | Witness | Trust class | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `wsd-evaluation-framework` | `Word Sense Disambiguation: A Unified Evaluation Framework` source trunk | class `AcademicCurated` | `princeton-wordnet`, `cili` | `*.data.xml` (including `semcor.data.xml` and `semcor+omsti.data.xml`), `*.gold.key.txt`, `schema.xsd`, `README`, `PROVENANCE.md` | [`data.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wsd-evaluation-framework/data.recipe), [`gold.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wsd-evaluation-framework/gold.recipe), [`schema.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wsd-evaluation-framework/schema.recipe), [`documentation.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wsd-evaluation-framework/documentation.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior bounds the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## The XML sentence files (`*.data.xml`) and gold keys (`*.gold.key.txt`)

Each `<sentence>` in `*.data.xml` is composed in order from its `<wf>` and `<instance>` word elements, including full `SemCor` and `SemCor+OMSTI` training corpora via streaming grammar-bounded XML records. Each `<instance id="d000.s000.t000" lemma="document" pos="NOUN">document</instance>` registers `d000.s000.t000` as a cross-file internal pointer (`key instance id`).

`*.gold.key.txt` pairs each `d000.s000.t000` instance ID with one or more WordNet 3.0 sense keys (`document%1:10:00::`). At ingest, `gold.recipe` resolves `instance id` via `refer "instance id" wsd-data` directly to the word-in-sentence occurrence in `*.data.xml`, resolves the WordNet sense key through `highway.bin`, attests the disambiguated sense binding on that contextualized word instance, and **discards both `d000.s000.t000` and the raw sense-key pointer string afterward** ([30. Conflicts](../Sequence/Conflicts.md) S1, I7).

| Piece | Written as | Laplace reads it as | Target attestation & current recipe state | Specification |
| --- | --- | --- | --- | --- |
| `<text id="d000">`, `<sentence id="d000.s000">` | XML containers with `id` | document and ordered sentence trajectory of `<wf>` and `<instance>` tokens; `id` attributes resolved as internal pointers (`key`) and recorded nowhere | sentence trajectory `[[This, document, is, …], …]` | "corpus -> text -> sentence" (`schema.xsd`) |
| `<wf lemma="this" pos="DET">This</wf>` | context token | token text within its sentence, with `lemma` and `pos` (`upos`) attested in the sentence's annotation layer | contextual `[token, lemma]` and `[token, UPOS]` | "mandatory attributes (`lemma` and `pos`)" |
| `<instance id="d000.s000.t000" lemma="document" pos="NOUN">document</instance>` | disambiguated target token | token occurrence in its sentence, keyed by `id` (`key instance id`) so `*.gold.key.txt` binds to it; `d000.s000.t000` is recorded nowhere | contextual token occurrence + lemma + `UPOS` | target word instance (`schema.xsd`) |
| `d000.s000.t000 document%1:10:00::` in `*.gold.key.txt` | space-separated `instance_id` and WordNet 3.0 sense key(s) | `refer "instance id" wsd-data` resolves the contextual token; sense key resolves via `highway.bin` to the lexicalization `[lemma, eng, ILI]` | target: contextual word-in-sentence → `[lemma, eng, ILI]` lexicalization binding (`gold.recipe` already resolves `instance id` and maps sense keys to `ILI` via `type "gold key" ili`; refining the target from bare `ILI` to `[lemma, eng, ILI]` closes in `Batch 2`) | `Data_Validation/README`: "first column corresponds to the instance id and the remaining columns correspond to the gold key/s" |
| `schema.xsd`, `README`, `PROVENANCE.md` | XML schema and documentation | observed file syntax trees and text under the corpus trunk | none | |

## System outputs and derived tables

Baseline system output files (`Output_Systems/*.key`), `candidatesWN30.txt`, and local `ili_mapped` convenience tables are either non-gold model predictions or redundant projections of WordNet 3.0 + CILI that `highway.bin` already resolves natively, so gold testimony comes strictly from `*.data.xml` + `*.gold.key.txt`.

## Relations

`data.recipe` and `gold.recipe` resolve `d000.s000.t000` pointers across XML and gold key files without leaking internal IDs into claims. Closing the remaining `Batch 2` items binds sense keys onto `[lemma, eng, ILI]` lexicalization strands ([30. Conflicts](../Sequence/Conflicts.md) I7) rather than bare `ILI` concept nodes and composes sentence-aligned `LEMMA`/`UPOS`/sense layers under the single `wsd-evaluation-framework` witness trunk.
