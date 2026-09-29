# Word sense disambiguation

A sense-annotated corpus attests which wordnet sense a token carries, and each dataset is its own witness because its identifiers start over.

The composition is a token in a sentence. The mask is sense. The value is the WordNet 3.0 sense the annotators assigned, and the tables made on this machine that map that key to a synset and to CILI. This is not the lexicon. The lexicon attests that the sense exists. This corpus attests that this token carries it.

The witness is per dataset. SemCor, SemCor+OMSTI, the five evaluation sets and their concatenation, and the systems' answers each start their identifiers (`d000`, `d000.s000`, `d000.s000.t000`) over again, so they are not one witness with one namespace. Read after WordNet 3.0 and CILI. Deviation 90, the recipe's choice. Loaded measure of what is read: 6,459,459 compositions from 119 MB.

`Data_Validation/sample-dataset` holds the semeval2015 XML and gold key byte for byte with `Evaluation_Datasets/semeval2015`, so those files are read once. `SemCor+OMSTI/semcor+omsti.data.xml` is 1,300,362,941 bytes and is not read. Its gold file is. The unread XML is the same sentences the gold file attests. Reading both would attest the token twice.

The hop is from the token's sense key into [Wordnets](Wordnets.md). Fanout is one sense key per token in the gold file, then whatever fanout that synset has in the wordnet. The corpus does not attest the dependency role of the token and does not attest the interlingual gloss. [Semantics Experiments](../Semantics-Experiments.md) and [Trust](../Trust.md) use these assignments.

## Files, breakdown, and caveats

Taken from the recipe files. A line in a block is a directive. The prose above it is that file's own account of what is read, what is not, and what a row becomes.

### `wsd-evaluation-framework/candidates.recipe`

Data_Validation/candidatesWN30.txt. Data_Validation/README says of it only that ValidateGold "will check that all gold keys are in fact candidate synsets from the given lemma in WordNet 3.0"; nothing names its fields, which are parted by tabs: a lemma, a letter, and one sense key or more. Each line is recorded as the tuple of its fields, in its own order.

```text
match candidatesWN30.txt
grammar table
claims
row tuple
```

### `wsd-evaluation-framework/data.recipe`

A data set of the framework: texts of sentences, each sentence the words it is made of. The file does not write a sentence as text: a sentence is the path of its words, in order. What is said of a word (its lemma, its pos, and for an instance its id) is said of the word, within its sentence. The ids are the data set's own: d000.s000.t000 is a different word in SemCor, in senseval2 and in semeval2013. An id is therefore recorded within its data set, which is the directory the file is in, as the framework names it.

```text
match *.data.xml
grammar xml
identity text id kind {dir}
identity sentence id kind {dir}
refer instance.id {dir}
words sentence wf instance
```

### `wsd-evaluation-framework/documentation.recipe`

The framework's README files, read as text; and PROVENANCE.md, which is not the framework's: it was written on this machine, and says where the archive was fetched from.

```text
match README PROVENANCE.md
grammar text
```

### `wsd-evaluation-framework/gold.recipe`

README: each line is an instance id followed by its gold key or keys, separated by spaces. The README names neither field, so what is recorded is the pair of the two, the id within its data set (see data.recipe).

```text
match *.gold.key.txt
grammar table
separator space
columns id
claims
pair
subject in id
subject-kind {dir}
rest values
```

### `wsd-evaluation-framework/ili-mapped.recipe`

NOT the framework's. The tables of ili_mapped/ were made on this machine, by tools/sensekey_to_ili.py, from a dataset's gold file, WordNet 3.0's index.sense and the Collaborative Interlingual Index's ili-map-pwn30.tab. Nothing in the set names their maker (PROVENANCE.md says only "plus ILI-mapped gold keys"): the witness is named as the directory they are in is named, ili_mapped. The script writes each line as  iid `<TAB>` k `<TAB>` off `<TAB>` ili  and gives the fields no names: each line is recorded as the tuple of its four fields, in its own order. Made by a script, reviewed by no one: an unrated witness plays at Glicko-2's stock deviation.

```text
match *.gold.ili.tsv
grammar table
witness {dir}
deviation 350
claims
row tuple
```

### `wsd-evaluation-framework/schema.recipe`

The schema of the data files (Data_Validation/schema.xsd), recorded as its syntax tree, every byte as written.

```text
match schema.xsd
grammar xml
```

### `wsd-evaluation-framework/source`

The unified evaluation framework for word sense disambiguation of Raganato, Camacho-Collados and Navigli (2017): SemCor, SemCor+OMSTI, the five evaluation datasets and their concatenation, every sense annotated with WordNet 3.0; the answers of the systems the framework compared; and, beside the framework, tables made on this machine that map the gold keys to synsets and to the Collaborative Interlingual Index. Every dataset is its own witness, named as the framework names its directory (SemCor, senseval2, ALL ...): the identifiers the data files write (d000, d000.s000, d000.s000.t000) begin again in every dataset. The deviation is this recipe's choice for a curated academic resource; the specification does not give one. Data_Validation/sample-dataset holds semeval2015.data.xml and semeval2015.gold.key.txt, byte for byte the files of Evaluation_Datasets/semeval2015: they are read there, under that directory's name. Training_Corpora/SemCor+OMSTI/semcor+omsti.data.xml is 1,300,362,941 bytes. The XML reader parses a file whole: SemCor's 39 MB took 3.3 GB of memory, and at that rate this file takes more than this machine has. It is not read. Its gold file is. Measured when it was loaded: 6,459,459 compositions from 119 MB, at 750 bytes each with their indexes and standings.

```text
witness {dir}
deviation 90
root $LAPLACE_DATA/WSD
except */sample-dataset/*
except */semcor+omsti.data.xml
```

### `wsd-evaluation-framework/systems.recipe`

The answers of the systems the framework compared, one file for each system, on the data set ALL. Each file is that system's testimony, not the framework's, and is named as its file is named. The ids are ALL's. The deviation is the stock deviation of an unrated witness; the source gives none.

```text
match *.key
grammar table
separator space
columns id
witness {name}
deviation 350
claims
pair
subject in id
subject-kind ALL
rest values
```
