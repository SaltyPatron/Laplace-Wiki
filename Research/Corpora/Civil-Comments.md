# Civil Comments

Civil Comments attests toxicity labels that Jigsaw added to reader comments.

The composition is a reader comment. The mask is the toxicity label. The value is the label Jigsaw assigned. Witness civil_comments, deviation 90, the recipe's choice. The data is Parquet, which no recipe reads. The dataset card kept with the drop is read as text. That card names `text`, `toxicity`, `severe_toxicity`, `obscene`, `threat`, `insult`, `identity_attack`, and `sexual_explicit`, and says nothing of what a number stands for. The recipe therefore records each number as the number given, and does not take it for a score.

The Kaggle page for the Jigsaw Unintended Bias in Toxicity Classification challenge, which the Hugging Face card says this drop replicas, states the missing definition: each such attribute is the fraction of human raters who believed the attribute applied, from 0.0 to 1.0, and for evaluation a `target` of 0.5 or more is the positive class. TensorFlow Datasets says the same of the seven labels: the fraction of annotators who assigned the attribute. Up to ten annotators rated a comment. That fraction is an aggregate of annotators. It is not one annotator's label and it is not a second witness beside them. The identity-mention labels are the same kind of fraction, and the card says they exist only for a fraction of comments. `rating` is the civility rating Civil Comments users gave, which is a different witness from Jigsaw's raters.

Sources: `<https://www.kaggle.com/competitions/jigsaw-unintended-bias-in-toxicity-classification/data>` and the TensorFlow Datasets CivilComments description. There is no live directory. The refresh holds the drop.

A toxicity label does not attest a sense, a part of speech, or a dependency role of a token in the comment. The comment text, once read, is observed content carrying that label. Fanout does not arise inside the label. The label is one value on one comment.

## Files, breakdown, and caveats

Taken from the recipe files. A line in a block is a directive. The prose above it is that file's own account of what is read, what is not, and what a row becomes.

### `civil-comments/comments.recipe`

The set's files are Parquet; each is written out beside it as a table (extracted/, by parquet-to-text.py): the first row the columns' own names, every value as the file holds it. The set's card (README.md, "Data Fields"): text, toxicity, severe_toxicity, obscene, threat, insult, identity_attack, sexual_explicit. It says nothing of what a number stands for, so each is recorded as the number the set gives the comment under that name, and is not taken for a score. A comment has no name of its own in the set: it is the text it is.

```text
match train-*.tsv validation-*.tsv test-*.tsv
grammar table
header
escaped \
claims
together
subject in text
attest *
```

### `civil-comments/source`

Comments from the Civil Comments platform with the labels Jigsaw added. The dataset card's title: Dataset Card for "civil_comments". Its data is in Parquet files only, which no recipe reads; the card itself is read as text. The deviation is this recipe's choice for a curated academic resource; the specification does not give one. The files are Parquet, read as they are written out in extracted/.

```text
witness civil_comments
deviation 90
root $LAPLACE_DATA/.refresh-*/Safety/CivilComments/civil-comments-*[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]
except *.parquet
reads text
```
