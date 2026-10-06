# Universal Dependencies

Universal Dependencies is one source and one witness, its treebanks, its documentation pages and its validator data all files under one trunk: a treebank attests what it says of each word within its sentence, the validator's lists of parts of speech and relations are the highway's `upos` and `deprel` lists, and the documentation attests what each of those is.

One organization's corpus set is one source. Universal Dependencies is one source trunk and one witness, and everything it publishes is observation and witnessing by that one source: its treebanks, [release 2.18](https://lindat.mff.cuni.cz/repository/handle/11234/1-6149); its documentation pages, UD's own definitions of each part of speech, relation, and feature, from the `pages-source` branch of [UniversalDependencies/docs](https://github.com/UniversalDependencies/docs/tree/pages-source); and its validator's data, derived by UD's own system from those definitions, the `data` folder of [UniversalDependencies/tools](https://github.com/UniversalDependencies/tools/tree/10ce40cf8a577714e51cf56b443dd4c2c6d55f91/data) at commit `10ce40cf`. Every treebank is a directory of files under that trunk, each file with its path, and so are the documentation pages and the validator's data; none of them is a witness of its own. The treebanks are the ones saying that this word carries that tag; the documentation says what the tag is. The Engine is built otherwise: three sources read Universal Dependencies, in the order [`recipes/order`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/order) gives, the tools, then the documentation, then the treebanks, each with a witness of its own, and the `universal-dependencies` source names a witness per treebank, by its directory (`witness {dir}`). The target is the one trunk.

## Sources

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `universal-dependencies` | `Universal Dependencies`, the source trunk; a treebank, such as `UD_English-EWT`, is a directory of files under it. As built, the Engine names a witness per treebank by its directory name (`witness {dir}`) | class `AcademicCurated` | `unicode`, `iso-639` | `*.conllu` under `UD-Treebanks/ud-treebanks-*` | [`conllu.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/universal-dependencies/conllu.recipe) |
| `universal-dependencies-tools` | `Universal Dependencies`, the same source trunk: the validator's data is files under it. As built, a source of its own with the witness `UniversalDependencies tools` | as built, class `StandardsDerived`; the one trunk has one class, `AcademicCurated` | `unicode`, `iso-639` | `upos.json`, `udeprels.json` under `UD-Tools/*/data` | [`upos.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/universal-dependencies-tools/upos.recipe), [`udeprels.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/universal-dependencies-tools/udeprels.recipe) |
| `universal-dependencies-documentation` | `Universal Dependencies`, the same source trunk: the documentation pages are files under it. As built, a source of its own | as built, class `StandardsDerived`; the one trunk has one class, `AcademicCurated` | `universal-dependencies-tools` | `*.md` under `UD-Docs/extracted/docs-pages-source` | [`pages.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/universal-dependencies-documentation/pages.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior is the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## From trunk to leaves

Universal Dependencies is one tree, from its source trunk down to the codepoints every other tree shares:

```text
Universal Dependencies           the source trunk, [source record, its files' trunks in path order]: the witness
├ source record                  "Universal Dependencies" and its release, content
├ _u-pos/ADJ.md …                the documentation pages, UD's definitions of its tags, relations and features: files
├ data/upos.json …               the validator's data, derived from those definitions: files under the same trunk
├ UD_Abaza-ATB/ …                a treebank, one of 2.18's 353: a directory, its path the files' metadata; no witness
└ UD_English-EWT/en_ewt-ud-train.conllu
  │                              a file, [metadata, content]; README.md, LICENSE.txt and stats.xml are files too
  ├ metadata                     the OS's record, and what the file says of itself (the newdoc and newpar notes)
  └ content                      [record, record, …], one record a sentence
    └ record                     a path over what the treebank says of this sentence
      ├ sentence                 the `# text` sentence: UAX #29 words, graphemes, codepoints
      ├ tokens                   UD's own segmentation (don't as do and n't), each FORM down to its codepoints
      ├ layers                   UPOS, XPOS, LEMMA and FEATS, aligned to the tokens; identical layers are one
      ├ dependency tree          DEPREL by HEAD, its subtrees composed and shared
      ├ notes                    text_en and the like, said of the sentence at the sentence's tier
      ├ speaker, annotator       content: [sentence, speaker_id, SP], [token, Annotator, Sv], which the corpus attests
      └ strands                  [forces, NOUN], [forces, force], [forces, Number=Plur]: what it says of each word
```

The pointers, `ID`, `HEAD`, `sent_id`, `newdoc id`, `newpar id` and MISC's ids and offsets, resolve into the tree and are recorded nowhere. One walk up from `[forces, NOUN]` reaches the records, files and trunk that assert it, the attribution and its count; one walk up from `forces` reaches every trunk that holds it, the witnessing. A strand occurring in k records under the trunk is one attestation of the corpus with k games, counted off the tree, a series the client solves as one update ([Consensus: Matchups](../Semantics/Consensus.md#matchups)). English-EWT's README says its UPOS and features were mainly assigned automatically: content under the trunk a read can use, and an automatic tag repeated token by token is packaging, not the corpus saying it again.

As built, the Engine differs: each treebank is a witness of its own (`witness {dir}`); claims are emitted as events outside the tree; no layer is composed; `relate row DEPREL to HEAD` makes the type-level `[word, nsubj, head word]`, with the sentence lost; MISC's `Annotator` and the `speaker_id` note are witnesses of their own (`own`); and the README, LICENSE and statistics are not read. Open Multilingual Wordnet's `witness {first label}`, a witness per lexicon, is the same mistake ([Wordnets](Wordnets.md)).

## Relations

As built, the relation of a claim above is the name of the field that carries its value: the CoNLL-U column's name, a FEATS or MISC key, or a comment's key. That is markup, not meaning. A relation is what the source means, resolved through the road classes, never the name of a field, column, attribute, or layer: a tagset value is a value of its tagset with its attested equivalence, a per-span label belongs in the sentence's annotation layer, and a pointer's attribute name is in no claim, [10. Recipes](../Sequence/Recipes.md#1011-disposition-every-recovered-field).

| Claim, as built | Its relation, as built | What it means: the target |
| --- | --- | --- |
| `[word, UPOS, ADJ]` | the column's name, `UPOS` | `ADJ` is a value of the UPOS road class, "Universal part-of-speech tag": the strand is `[word, ADJ]`, as `[forces, NOUN]` is, one claim per pair with the bit on the word's row, and the sentence's UPOS layer beside it |
| `[word, XPOS, value]` | the column's name, `XPOS` | a value of the treebank's own tagset, "language-specific (or treebank-specific)", a road class of its own, with its attested equivalence to UPOS; in the sentence's XPOS layer |
| `[word, LEMMA, value]` | the column's name, `LEMMA` | the word's lemma, "Lemma or stem of word form": `[forces, force]`, in the sentence's LEMMA layer |
| `[word, Number, Plur]` | the feature's name, `Number` | `Number=Plur`, a value of the universal feature inventory: `[forces, Number=Plur]`, the feature a part of the value, not a relation |
| `[word, nsubj, head word]`, `[barked, root]` | the DEPREL value | already meaning, a value of the dependency road class; what is wrong as built is the type-level shape with the sentence lost, and the target is the sentence's dependency layer |
| `[sentence, text_en, value]`, and every other comment key | the comment's key | what the key documents: `text_en` is the sentence in English, a sentence-tier translation strand, as OpenSubtitles' are; a key nothing documents is an explicit unresolved obligation |
| `[sentence, speaker_id, value]` | the comment's key | that this speaker said this sentence, a relation the corpus attests |
| `[word, Translit, value]`, `[word, Annotator, value]`, `[word, MISC, part]` | the MISC key, or the column's name | what Universal Dependencies documents each MISC key to mean, a transliteration for `Translit`; that this annotator annotated the token for `Annotator`; a part without a key has no documented meaning and is an explicit unresolved obligation |
| `[ADJ, shortdef, adjective]` | the front matter's key | what the documentation calls the tag: its short definition |
| `[Number, Sing, singular number]` | the value's name, `Sing` | the value `Number=Sing` and what the page says it is |

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

Only `.conllu` files are read. The treebank's README, LICENSE, and statistics are not; they are files under the trunk and are to be read.

## The validator's data

The validator's data is files under the Universal Dependencies trunk, observation and witnessing by the same source as the treebanks; as built it is a source of its own. The `tools` repository of UniversalDependencies carries, under `data`, the tags, relations, and features the validator permits, language by language, and its auxiliaries and tokens with spaces. Two files of it are read: `upos.json` and `udeprels.json`, each the list of the universal tags or relations (`content`), and each a list of the highway's (`types upos`, `types deprel`, each value keyed by itself). The rest of the data is the validator's own configuration, read by nothing.

## The documentation

The documentation pages are files under the Universal Dependencies trunk, UD's own definitions, witnessed by the same source as the treebanks; as built they are a source of their own. Each page of the project's documentation source documents one tag, relation, or feature, named by its `title`. The page's head says what it is, shortly, and a feature's page says what each of its values is.

| Piece | Written as | Laplace reads it as | Claim recorded |
| --- | --- | --- | --- |
| `title: 'ADJ'` | the front matter's title | what the page is about | the subject |
| `shortdef: 'adjective'` | the front matter's short definition | said of what the page is about, under `shortdef` | `[ADJ, shortdef, adjective]` |
| ``### <a name="Sing">`Sing`</a>: singular number`` | a value's heading on a feature's page | the value and what it is, said of the feature | `[Number, Sing, singular number]` |
| everything else on the page | as written | not a claim | none |

The documentation attests what a tag is called. It does not attest that any word carries it: that is the treebanks' to say, as files under the corpus's one trunk.
