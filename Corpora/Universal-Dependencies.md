# Universal Dependencies

A Universal Dependencies treebank attests what it says of each word within its sentence, the validator's data attests which tags, relations, and features the project permits, and the documentation attests what each of those is called.

Three sources read Universal Dependencies, in the order [`recipes/order`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/order) gives: the tools, then the documentation, then the treebanks. Each is a witness of its own. None is lineage of another: the treebanks use the tags the tools permit and the documentation names, but the treebank is the one saying that this word carries that tag.

## Sources

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `universal-dependencies` | the treebank's directory name, such as `UD_English-EWT`: every treebank is its own witness | class `AcademicCurated` | `unicode`, `iso-639` | `*.conllu` under `UD-Treebanks/ud-treebanks-*` | [`conllu.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/universal-dependencies/conllu.recipe) |
| `universal-dependencies-tools` | `UniversalDependencies tools` | class `StandardsDerived` | `unicode`, `iso-639` | `*.json` under `UD-Tools/*/data` | [`data.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/universal-dependencies-tools/data.recipe) |
| `universal-dependencies-documentation` | `Universal Dependencies` | class `StandardsDerived` | `universal-dependencies-tools` | `*.md` under `UD-Docs/extracted/docs-pages-source` | [`pages.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/universal-dependencies-documentation/pages.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior is the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## The treebank

A record is one sentence: its comment lines, then a row for every word, then a blank line. The columns are the ten CoNLL-U fields, and every value is recorded as the treebank writes it. "Word lines contain the annotation of a word, token, or node in 10 fields separated by single tab characters." "Blank lines mark sentence boundaries." "Comment lines occur at the beginning of sentences, before word lines." [CoNLL-U format](https://universaldependencies.org/format.html)

Each thing the treebank says is a claim, a tuple of entities as [Claims](../Semantics/Claims.md#tuples) defines them, every part written as the treebank writes it. The tier of a claim is one above its highest part, as [Compositions](../Storage/Compositions.md#tiers) requires of any composition, so a claim of a word sits one tier above the word and a claim of the sentence one above the sentence.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `# text = ...` | a comment line | what the record is about: the sentence, as content like any other | none of its own; the sentence is the subject every note is said of and the scope every word stands within | the `text` comment holds the sentence and is mandatory since UD v2 [CoNLL-U format](https://universaldependencies.org/format.html) |
| `# sent_id = …`, `# newdoc id = …`, `# newpar id = …`, `# newdoc`, `# newpar` | comment lines | how the treebank points at its sentences, documents and paragraphs: keys, recorded nowhere (`key sent_id "newdoc id" "newpar id" newdoc newpar`) | nothing | `sent_id` is mandatory [CoNLL-U format](https://universaldependencies.org/format.html) |
| `# key = value`, any other | a comment line, such as `# text_en = …` | a note of the record, said of the sentence under its key | `[sentence, text_en, value]` | comment lines hold sentence-level metadata |
| ID | `1`, `2`, ... | the row's number: what HEAD and DEPS refer to. `1-2` is a row that spans rows 1 to 2; `8.1` is a row like any other | none of its own | "Word index, integer starting at 1 for each new sentence; may be a range for multiword tokens; may be a decimal number for empty nodes" [CoNLL-U format](https://universaldependencies.org/format.html) |
| FORM | the word | the subject: the word, as written, within the sentence | the first part of every claim of the row | "Word form or punctuation symbol" |
| LEMMA | the lemma | said of the word under the column's name | `[word, LEMMA, value]` | "Lemma or stem of word form" |
| UPOS | one of the 17 tags | said of the word under the column's name | `[word, UPOS, ADJ]` | "Universal part-of-speech tag" |
| XPOS | the treebank's own tag | said of the word under the column's name | `[word, XPOS, value]` | "Optional language-specific (or treebank-specific) part-of-speech / morphological tag; underscore if not available" |
| FEATS | `Key=Value` parts joined by `\|`; a value may be `A,B` | each value said of the word under its key; `Gender=Masc,Fem` is two claims | `[word, Number, Plur]` | "List of morphological features from the universal feature inventory or from a defined language-specific extension; underscore if not available" |
| HEAD and DEPREL | a row number and a relation | the word's relation to the word of the row HEAD numbers; `0` numbers no row, and the relation stands alone | `[word, nsubj, head word]`; `[barked, root]` | "Head of the current word, which is either a value of ID or zero (0)"; "Universal dependency relation to the HEAD (root iff HEAD = 0) or a defined language-specific subtype of one" |
| each column, down the sentence | LEMMA, UPOS, XPOS, FEATS, MISC, DEPREL | one layer of the sentence: the composition of the words' values in order, said of the sentence under the column's name; a word's several values one tuple, an empty one the treebank's `_`, a relation its type and head word | `[The dog barked., UPOS, DET NOUN VERB PUNCT]`, `[The dog barked., DEPREL, [det, dog] [nsubj, barked] root [punct, barked]]` | [Types](../Reference/Types.md#layers): one claim per sentence per layer, with the words' own claims beside |
| DEPS | `head:rel` parts joined by `\|` | further relations of the word, of the same shape; one that repeats the row's own relation is said once | `[word, rel, head word]` | "Enhanced dependency graph in the form of a list of head-deprel pairs" |
| MISC | `Key=Value` parts joined by `\|`; a part may have no `=` | each value said of the word under its key; a part without `=` is said under `MISC` | `[word, SpaceAfter, No]`; `[word, MISC, part]` | "Any other annotation" |
| `_` | in any field | what the treebank leaves empty: attests nothing | none | "Fields ... underscore if not available" |
| a row whose ID is `a-b` | a multiword token | the token, and the words of the rows it spans | `[token, [word, word, ...]]` | "Multiword tokens are indexed with integer ranges like 1-2 or 3-5" [CoNLL-U format](https://universaldependencies.org/format.html) |
| a row whose ID is `i.1` | an empty node | a row as any other: its HEAD `_` gives no relation, its DEPS do | as the row's fields say | "Empty nodes are indexed i.1, i.2, etc." [CoNLL-U format](https://universaldependencies.org/format.html) |

The record is the path of the sentence, its layers, its notes, its spans, and its words' claims; UPOS and DEPREL are the highway's `upos` and `deprel` lists, mask fields of every entity that carries one ([Types](../Reference/Types.md#masks)). The record is what is witnessed, once, as one ledger row; every claim in it plays its matchup as [Consensus](../Semantics/Consensus.md#matchups) describes. A claim said twice in one record is witnessed in it once. Nothing is renamed, reordered, or filled in.

Only `.conllu` files are read. The treebank's README, LICENSE, and statistics are not.

## The validator's data

The `tools` repository of UniversalDependencies carries, under `data`, the tags, relations, and features the validator permits, language by language, and its auxiliaries and tokens with spaces. Every file is one JSON object.

| Piece | Laplace reads it as | Claim recorded |
| --- | --- | --- |
| a key of the file's object, such as `upos` or `deprels` | a thing | the subject |
| what is written under it | said of the key: the path from the key through every nested key to each value, every key and value as written; an array says each of its values under the same path | `[key, ..., value]` |
| `null`, an empty text | nothing | none |

Everything one file says it says together: one record, witnessed once, and its claims within it.

## The documentation

Each page of the project's documentation source documents one tag, relation, or feature, named by its `title`. The page's head says what it is, shortly, and a feature's page says what each of its values is.

| Piece | Written as | Laplace reads it as | Claim recorded |
| --- | --- | --- | --- |
| `title: 'ADJ'` | the front matter's title | what the page is about | the subject |
| `shortdef: 'adjective'` | the front matter's short definition | said of what the page is about, under `shortdef` | `[ADJ, shortdef, adjective]` |
| ``### <a name="Sing">`Sing`</a>: singular number`` | a value's heading on a feature's page | the value and what it is, said of the feature | `[Number, Sing, singular number]` |
| everything else on the page | as written | not a claim | none |

The documentation attests what a tag is called. It does not attest that any word carries it: that is the treebank's to say, and only the treebank's directory is the witness of it.
