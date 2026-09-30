# Word sense disambiguation

A dataset of the WSD evaluation framework attests the words of each sentence, their lemma and part of speech, and the WordNet 3.0 sense keys of each annotated instance, every dataset as a witness of its own; each compared system attests its own answers; and the framework's README files, schema, and candidate list attest nothing of a word.

The source is the unified evaluation framework of Raganato, Camacho-Collados and Navigli (2017) at [lcl.uniroma1.it/wsdeval](http://lcl.uniroma1.it/wsdeval/): SemCor, SemCor+OMSTI, the five evaluation datasets and their concatenation ALL, every sense annotated with WordNet 3.0, and the answers of the systems the framework compared. Beside it stand tables made on this machine that map the gold keys to synsets and to the Collaborative Interlingual Index. Every dataset is its own witness, named as the framework names its directory, because the identifiers the data files write (`d000`, `d000.s000`, `d000.s000.t000`) begin again in every dataset.

## Sources

| Source | Witness | Uncertainty | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `wsd-evaluation-framework` | the dataset's directory name, such as `SemCor`, `senseval2`, `ALL`: every dataset is its own witness | deviation 90 | `princeton-wordnet`, `cili` | `*.data.xml` | [`data.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wsd-evaluation-framework/data.recipe) |
| `wsd-evaluation-framework` | the dataset's directory name | deviation 90 | `princeton-wordnet`, `cili` | `*.gold.key.txt` | [`gold.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wsd-evaluation-framework/gold.recipe) |
| `wsd-evaluation-framework` | the system's file name, without its extension: every system is its own witness | deviation 350 | `princeton-wordnet`, `cili` | `*.key` | [`systems.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wsd-evaluation-framework/systems.recipe) |
| `wsd-evaluation-framework` | `Data_Validation`, the directory the file is in | deviation 90 | `princeton-wordnet`, `cili` | `candidatesWN30.txt` | [`candidates.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wsd-evaluation-framework/candidates.recipe) |
| `wsd-evaluation-framework` | `ili_mapped`, the directory the files are in | deviation 350 | `princeton-wordnet`, `cili` | `*.gold.ili.tsv` | [`ili-mapped.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wsd-evaluation-framework/ili-mapped.recipe) |
| `wsd-evaluation-framework` | the directory the file is in | deviation 90 | `princeton-wordnet`, `cili` | `schema.xsd` | [`schema.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wsd-evaluation-framework/schema.recipe) |
| `wsd-evaluation-framework` | none: the files are read as text | | `princeton-wordnet`, `cili` | `README`, `PROVENANCE.md` | [`documentation.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wsd-evaluation-framework/documentation.recipe) |

The source's deviation of 90 is, the source file says, "this recipe's choice for a curated academic resource; the specification does not give one". The 350 of the systems' answers and of the ILI-mapped tables is the stock deviation of an unrated witness, as [Consensus](../Semantics/Consensus.md#entry) describes entry: the systems' files are each system's testimony, not the framework's, and the ILI-mapped tables were "made by a script, reviewed by no one". The number is not settled, and [Corpora](README.md#not-settled) lists it among what stays missing.

Two things under the root are not read. `Data_Validation/sample-dataset` holds `semeval2015.data.xml` and `semeval2015.gold.key.txt`, byte for byte the files of `Evaluation_Datasets/semeval2015`: they are read there, under that directory's name. `Training_Corpora/SemCor+OMSTI/semcor+omsti.data.xml` is not read: the XML reader parses a file whole, and at the rate SemCor took, this file takes more memory than the machine has. Its gold file is read.

## The data files

A record is one sentence. The file does not write a sentence as text: a sentence is the path of its words, in order. What is said of a word is said of the word, within its sentence, and every name and value is recorded as the file writes it. The README gives the tag order as "corpus -> text -> sentence", with `wf` the "non-disambiguated" tag and `instance` the "disambiguated" one.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `<corpus lang="en" source="senseval2">` | the root element | not read: the element is no thing and stands inside none, so nothing is said of it; what is inside it speaks | none | the README does not define `lang` or `source`; `schema.xsd` declares both with no type |
| `<text id="d000">` | an element, its `id` required | the text, named by its `id` within its dataset: the path of the directory's name and the id | the subject of what the element says | the README does not define the `text` id; `schema.xsd` has `id` `use="required"` |
| any other attribute of `text`, such as `source="br-e30"` | an attribute | said of the text under the attribute's name | `[[SemCor, d000], source, br-e30]` | "Note that it is possible to add additional attributes if needed (e.g. fine-grained PoS tags)." (the framework's `Data_Validation/README`) |
| `<sentence id="d000.s000">` | an element inside a text | the sentence, named by its `id` within its dataset, and a record of words: what it is about is the path of its words, in order; its place in the text is said of the text | `[[SemCor, d000], sentence, [SemCor, d000.s000]]`, `[[SemCor, d000.s000], sentence, [word, word, ...]]` | `schema.xsd` has `id` `use="required"` |
| `<wf lemma="the" pos="DET">The</wf>` | a word element inside a sentence | the word: its text, within its sentence | the subject of the claims of `lemma` and `pos` | `wf` is the "non-disambiguated" tag |
| `<instance id="d000.s000.t000" lemma="art" pos="NOUN">art</instance>` | a word element inside a sentence | the word, the same way | the subject of the claims of `id`, `lemma`, and `pos` | `instance` is the "disambiguated" tag |
| `lemma` | on `wf` and `instance` | said of the word under `lemma` | `[The, lemma, the]` | "Both types should contain two mandatory attributes ("lemma" and "pos")." |
| `pos` | on `wf` and `instance` | said of the word under `pos` | `[The, pos, DET]` | "The "pos" tag (Part-of-Speech), should follow the Universal PoS tags." [Universal POS tags](http://universaldependencies.org/u/pos/index.html) |
| `id` | on `instance` | the instance's identifier, a thing within its dataset: the path of the directory's name and the id, said of the word under `id`. It is the thing the gold file's first field names | `[art, id, [senseval2, d000.s000.t000]]` | "instance" should additionally contain an id, which should be present in the gold file (the framework's `Data_Validation/README`) |
| any other attribute of `wf` or `instance` | an attribute | said of the word under the attribute's name | `[word, name, value]` | "it is possible to add additional attributes if needed" |
| the text of `wf` or `instance` | character data | the word itself | the subject | `schema.xsd` extends `xs:string` |

The record is the path of the sentence's words and of what is said of each, witnessed once, as one ledger row, by the dataset whose directory the file is in; every claim in it plays its matchup as [Consensus](../Semantics/Consensus.md#matchups) describes. The same id in another dataset names another thing: `d000.s000.t000` is one word in SemCor and another in senseval2. ALL's ids carry the dataset's name, `senseval2.d000.s000.t000`, and are ALL's own.

## The gold keys

A record is one line: an instance id, then its gold key or keys, parted by spaces. The README names neither field, so the recipe names only the first column, `id`, and records the pair of the two, never a predicate.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| the first field | `d000.s000.t000` | the instance, within its dataset: the path of the directory's name and the id, the same thing the data file's `instance` refers to | the subject | "Each line is space-separated, where the first column corresponds to the instance id and the remaining columns correspond to the gold key/s." "The .txt gold file should contain all the disambiguation instances included in the XML." |
| each further field | `art%1:09:00::` | a sense key, as written; the pair of the instance and the key. Two keys on a line are two pairs | `[[senseval2, d000.s000.t000], art%1:09:00::]`, `[[senseval2, d000.s000.t002], peculiar%5:00:00:specific:00]` | "the remaining columns correspond to the gold key/s"; "All senses are annotated with WordNet 3.0." |

The key is recorded whole. Its parts, `lemma%ss_type:lex_filenum:lex_id:head_word:head_id`, are the wordnet's to define, and [Wordnets](Wordnets.md) is where the sense key is the subject.

## The systems' answers

Each `*.key` file is the answers of one system the framework compared, on the dataset ALL: a line for each instance, of the same shape as the gold file. Each file is that system's testimony, not the framework's, and is witnessed under the file's own name.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| the first field | `senseval2.d000.s000.t000` | the instance, within ALL: the path of `ALL` and the id | the subject | the ids are ALL's |
| each further field | a sense key | the pair of the instance and the key | `[[ALL, senseval2.d000.s000.t000], key]` | |

## The candidates

`Data_Validation/candidatesWN30.txt` is a table whose fields are parted by tabs: a lemma, a letter, and one sense key or more. Nothing names its fields: the README of `Data_Validation` says of it only that ValidateGold "will check that all gold keys are in fact candidate synsets from the given lemma in WordNet 3.0".

| Piece | Laplace reads it as | Claim recorded |
| --- | --- | --- |
| a line | the tuple of its fields, in its own order | `[lemma, letter, key, key, ...]` |

## The ILI-mapped gold keys

The tables of `ili_mapped/` are not the framework's. They were made on this machine, by a script, from a dataset's gold file, WordNet 3.0's `index.sense`, and the Collaborative Interlingual Index's `ili-map-pwn30.tab`. Nothing in the set names their maker, and `PROVENANCE.md` says only "plus ILI-mapped gold keys", so the witness is named as the directory they are in is named, `ili_mapped`, and enters at the stock deviation of an unrated witness, 350.

| Piece | Laplace reads it as | Claim recorded |
| --- | --- | --- |
| a line, `iid <TAB> k <TAB> off <TAB> ili` | the tuple of its four fields, in its own order; the script gives the fields no names | `[iid, k, off, ili]` |

## What attests nothing

`schema.xsd` is recorded as its syntax tree, every byte as written: no element of it is a thing, so it says nothing of a word. The README files are read as text, and so is `PROVENANCE.md`, which is not the framework's: it was written on this machine and says where the archive was fetched from. All of these are observed content, as [Attestations](../Semantics/Attestations.md#observations) says of ordinary content, and attest nothing. Every other file under the root is matched by no recipe and is not read.
