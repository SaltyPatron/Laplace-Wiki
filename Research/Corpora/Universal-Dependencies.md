# Universal Dependencies

A Universal Dependencies treebank attests the part of speech and the dependency role of a token, and the tools and the documentation attest the tag set rather than the sentence.

The composition in a treebank is a token in a sentence. Two masks are filled. The part-of-speech mask takes the universal part-of-speech tag as its value. The dependency-role mask takes the relation between a head token and a dependent token as its value. Each treebank is its own witness, named by its directory, because the sentences are that treebank's annotation. Deviation 90, the recipe's choice. Loaded measure: 15,632,387 compositions from 501 MB. [Trust](../Trust.md) measures 88 of these languages. v2.17, held live, and v2.18, held in the refresh, are the same corpus versioned. `ud-treebanks-v2.17.tgz` is the live release again. Both roots are declared.

The tools are a different composition: the inventory. The mask is whether a tag, relation, or feature is one the project permits, language by language, plus auxiliaries and tokens with spaces. Witness: UniversalDependencies tools. Loaded measure: 388,693 compositions from 6.7 MB. The documentation, read after the tools, attests what the project calls each tag, relation, and feature. A treebank that uses a tag and the documentation that defines the tag are not two witnesses of the token.

A treebank does not attest sense. Joining a token to a synset is a hop on [Hops](Hops.md), and only where a mapping says so. It is not implied by both files containing words. Fanout inside a sentence is the number of dependents of a head. [Pull](../../Semantics/Pull.md) caps fanout. The dependency edge pulls between the two tokens. It does not pull on a wordnet synset unless an explicit hop exists.

The language of the treebank is a hop to [ISO 639](ISO-639.md), not an attestation that every token is in that language. [Attestations](../../Semantics/Attestations.md) keeps a language mark at the composition that was marked.

## Files, breakdown, and caveats

Taken from the recipe files. A line in a block is a directive. The prose above it is that file's own account of what is read, what is not, and what a row becomes.

### `universal-dependencies/conllu.recipe`

CoNLL-U. A sentence is a record: its notes, then a row for every word. The columns are named as Universal Dependencies' format names them; every value is recorded as the treebank writes it.

```text
match *.conllu
grammar table
columns ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC
comment #
attest LEMMA UPOS XPOS
pairs FEATS | = ,
pairs MISC | =
```

### `universal-dependencies/source`

Universal Dependencies: treebanks of sentences, each with a row for every word and what the treebank says of it. Every treebank is its own witness, named as its directory is named. The deviation is this recipe's choice for a curated academic treebank; the specification does not give one. Measured when it was loaded: 15,632,387 compositions from 501 MB of it, at 750 bytes each with their indexes and standings.

```text
witness {dir}
deviation 90
root $LAPLACE_DATA/.refresh-*/UD-Treebanks/extracted/ud-treebanks-*
root $LAPLACE_DATA/UD-Treebanks/ud-treebanks-*
```

### `universal-dependencies-tools/data.recipe`

Every file is one object whose keys name what it lists ("upos", "deprels", "features", "auxiliaries", ...). What is written under a key is said of it: the path from the key to each value, every key and value as written.

```text
match *.json
grammar json
```

### `universal-dependencies-tools/source`

The data of Universal Dependencies' validator: the tags, relations and features the project permits, language by language, and its auxiliaries and tokens with spaces. The repository names itself "tools", of UniversalDependencies. The deviation is this recipe's choice for a curated academic resource; the specification does not give one. Measured when it was loaded: 388,693 compositions from 6.7 MB, at 750 bytes each with their indexes and standings.

```text
witness UniversalDependencies tools
deviation 90
root $LAPLACE_DATA/.refresh-*/UD-Tools/*/data
reads text
```

### `universal-dependencies-documentation/pages.recipe`

A page documents one tag, relation or feature, named by its title. The page's head says what it is, shortly (shortdef: 'number'), and a feature's page says what each of its values is:   ### `<a name="Sing">``Sing``</a>`: singular number        is        [Number, Sing, singular number]

```text
match *.md
grammar lines
claims
claims
```

### `universal-dependencies-documentation/source`

Universal Dependencies' own documentation of its tags, relations and features: what each one is called, in the project's own words. Every page is also read as the text it is. The deviation is this recipe's choice for a curated academic resource; the specification does not give one.

```text
witness Universal Dependencies
deviation 90
root $LAPLACE_DATA/.refresh-*/UD-Docs/extracted/docs-pages-source
```
