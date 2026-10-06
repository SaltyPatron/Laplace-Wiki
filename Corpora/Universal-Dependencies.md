# Universal Dependencies

A Universal Dependencies treebank attests what it says of each word within its sentence, the validator's lists of parts of speech and relations are the highway's `upos` and `deprel` lists, and the documentation attests what each of those is called.

Three sources read Universal Dependencies, in the order [`recipes/order`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/order) gives: the tools, then the documentation, then the treebanks. None is lineage of another: the treebanks use the tags the tools permit and the documentation names, but the treebanks are the ones saying that this word carries that tag. Universal Dependencies is one source trunk and one witness: every treebank is a directory of files under that trunk, each file with its path, and a treebank is never a witness of its own. The Engine is built otherwise: the `universal-dependencies` source names a witness per treebank, by its directory (`witness {dir}`), and the target is the one trunk.

## Sources

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `universal-dependencies` | `Universal Dependencies`, the source trunk; a treebank, such as `UD_English-EWT`, is a directory of files under it. As built, the Engine names a witness per treebank by its directory name (`witness {dir}`) | class `AcademicCurated` | `unicode`, `iso-639` | `*.conllu` under `UD-Treebanks/ud-treebanks-*` | [`conllu.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/universal-dependencies/conllu.recipe) |
| `universal-dependencies-tools` | `UniversalDependencies tools` | class `StandardsDerived` | `unicode`, `iso-639` | `upos.json`, `udeprels.json` under `UD-Tools/*/data` | [`upos.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/universal-dependencies-tools/upos.recipe), [`udeprels.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/universal-dependencies-tools/udeprels.recipe) |
| `universal-dependencies-documentation` | `Universal Dependencies` | class `StandardsDerived` | `universal-dependencies-tools` | `*.md` under `UD-Docs/extracted/docs-pages-source` | [`pages.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/universal-dependencies-documentation/pages.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior is the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## The treebank

A record is one sentence: its comment lines, then a row for every word, then a blank line. The columns are the ten CoNLL-U fields, and every value is recorded as the treebank writes it. "Word lines contain the annotation of a word, token, or node in 10 fields separated by single tab characters." "Blank lines mark sentence boundaries." "Comment lines occur at the beginning of sentences, before word lines." [CoNLL-U format](https://universaldependencies.org/format.html)

Each thing the treebank says is a claim, a tuple of entities as [Claims](../Semantics/Claims.md#tuples) defines them, every part written as the treebank writes it. The tier of a claim is one above its highest part, as [Compositions](../Storage/Compositions.md#tiers) requires of any composition, so a claim of a word sits one tier above the word and a claim of the sentence one above the sentence.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `# text = ...` | a comment line | what the record is about: the sentence, as content like any other | none of its own; the sentence is the subject every note is said of and the scope every word stands within | the `text` comment holds the sentence and is mandatory since UD v2 [CoNLL-U format](https://universaldependencies.org/format.html) |
| `# sent_id = …`, `# newdoc id = …`, `# newpar id = …` | comment lines | the treebank's pointers to where a sentence, document or paragraph is in it: recorded nowhere (`omit "newdoc id" "newpar id" sent_id`) | none | `sent_id` is mandatory [CoNLL-U format](https://universaldependencies.org/format.html) |
| `# key = value`, any other | a comment line, such as `# text_en = …` | a note of the record, said of the sentence under its key | `[sentence, text_en, value]` | comment lines hold sentence-level metadata |
| `# speaker_id = …` | a comment line | who spoke the sentence: the speaker is content, and that this speaker said this sentence is a relation the treebank attests. As built, the Engine makes the speaker a witness of its own, `[the treebank, speaker_id, value]` (`own note:speaker_id`); the target is the treebank's relation, with Universal Dependencies the witness | `[sentence, speaker_id, value]` | comment lines hold sentence-level metadata |
| ID | `1`, `2`, ... | the row's number, a position inside the sentence and never part of an ID: what HEAD and DEPS refer to. `1-2` is a row that spans rows 1 to 2; `8.1` is a row like any other | none of its own | "Word index, integer starting at 1 for each new sentence; may be a range for multiword tokens; may be a decimal number for empty nodes" [CoNLL-U format](https://universaldependencies.org/format.html) |
| FORM | the word | the subject: the word, as written, within the sentence | the first part of every claim of the row | "Word form or punctuation symbol" |
| LEMMA | the lemma | said of the word under the column's name | `[word, LEMMA, value]` | "Lemma or stem of word form" |
| UPOS | one of the 17 tags | said of the word under the column's name | `[word, UPOS, ADJ]` | "Universal part-of-speech tag" |
| XPOS | the treebank's own tag | said of the word under the column's name | `[word, XPOS, value]` | "Optional language-specific (or treebank-specific) part-of-speech / morphological tag; underscore if not available" |
| FEATS | `Key=Value` parts joined by `\|`; a value may be `A,B` | each value said of the word under its key; `Gender=Masc,Fem` is one value, `Masc,Fem`, since only `\|` and `=` part the column | `[word, Number, Plur]` | "List of morphological features from the universal feature inventory or from a defined language-specific extension; underscore if not available" |
| HEAD and DEPREL | a row number and a relation | the word's relation to the word of the row HEAD numbers; `0` numbers no row, and the relation stands alone | `[word, nsubj, head word]`; `[barked, root]` | "Head of the current word, which is either a value of ID or zero (0)"; "Universal dependency relation to the HEAD (root iff HEAD = 0) or a defined language-specific subtype of one" |
| each column, down the sentence | LEMMA, UPOS, XPOS, FEATS, MISC, DEPREL | nothing composes a layer down the sentence: each value is said of its word alone | none | [Types](../Reference/Types.md#layers): one claim per sentence per layer, with the words' own claims beside |
| DEPS | `head:rel` parts joined by `\|` | parted (`part DEPS by \| is :`) and kept as content of the row; not attested | none | "Enhanced dependency graph in the form of a list of head-deprel pairs" |
| MISC | `Key=Value` parts joined by `\|`; a part may have no `=` | each value said of the word under its key; a part without `=` is said under `MISC`. The treebank's own pointers to a token and its positions (`UI`, `Ref`, `ref`, `LId`, `LemmaId`, `OccId`, `ChunkId`, `XmlId`, `LvtbNodeId`, `AlignBegin`, `AlignEnd`) are recorded nowhere, and `SpaceAfter`, which the sentence's text already says, is not read (`omit MISC.…`). `Annotator` names who annotated the token: the annotator is content, and that this annotator gave the token its lemma, tags and features is a relation the treebank attests; as built, the Engine makes the annotator a witness of its own of the row's LEMMA, UPOS, XPOS and FEATS (`own MISC.Annotator`, `attest row … by MISC.Annotator`), and the target is the treebank's relation, with Universal Dependencies the witness | `[word, Translit, value]`; `[word, MISC, part]`; `[word, Annotator, value]` | "Any other annotation" |
| `_` | in any field | what the treebank leaves empty: attests nothing | none | "Fields ... underscore if not available" |
| a row whose ID is `a-b` | a multiword token | a row like any other: nothing composes the token over the words it spans | as the row's fields say | "Multiword tokens are indexed with integer ranges like 1-2 or 3-5" [CoNLL-U format](https://universaldependencies.org/format.html) |
| a row whose ID is `i.1` | an empty node | a row as any other: its HEAD `_` gives no relation, its DEPS do | as the row's fields say | "Empty nodes are indexed i.1, i.2, etc." [CoNLL-U format](https://universaldependencies.org/format.html) |

The record is the path of the sentence, its layers, its notes, its spans, and its words' claims; UPOS is read as a type of the highway's `upos` list (`type UPOS upos`); DEPREL is content as written; the banks they belong to are not written on any row yet ([Types](../Reference/Types.md#masks)). The record is what is witnessed, once, as one attestation; every claim in it plays its matchup as [Consensus](../Semantics/Consensus.md#matchups) describes. A claim said twice in one record is witnessed in it once. Nothing is renamed, reordered, or filled in.

Only `.conllu` files are read. The treebank's README, LICENSE, and statistics are not.

## The validator's data

The `tools` repository of UniversalDependencies carries, under `data`, the tags, relations, and features the validator permits, language by language, and its auxiliaries and tokens with spaces. Two files of it are read: `upos.json` and `udeprels.json`, each the list of the universal tags or relations (`content`), and each a list of the highway's (`types upos`, `types deprel`, each value keyed by itself). The rest of the data is the validator's own configuration, read by nothing.

## The documentation

Each page of the project's documentation source documents one tag, relation, or feature, named by its `title`. The page's head says what it is, shortly, and a feature's page says what each of its values is.

| Piece | Written as | Laplace reads it as | Claim recorded |
| --- | --- | --- | --- |
| `title: 'ADJ'` | the front matter's title | what the page is about | the subject |
| `shortdef: 'adjective'` | the front matter's short definition | said of what the page is about, under `shortdef` | `[ADJ, shortdef, adjective]` |
| ``### <a name="Sing">`Sing`</a>: singular number`` | a value's heading on a feature's page | the value and what it is, said of the feature | `[Number, Sing, singular number]` |
| everything else on the page | as written | not a claim | none |

The documentation attests what a tag is called. It does not attest that any word carries it: that is the treebanks' to say, as files under the corpus's one trunk.
