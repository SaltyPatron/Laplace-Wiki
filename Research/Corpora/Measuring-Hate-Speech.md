# Measuring Hate Speech

Measuring Hate Speech attests several annotators' ratings of comments.

The composition is a comment. The mask is the annotator's rating. The value is that rating. Several annotators rate the same comment, so the comment has several witnessed values, not one value copied into several files. Witness Measuring Hate Speech, deviation 90, the recipe's choice. The Parquet is not read. The extracted TSV is excluded. The dataset card is read as text. There is no live directory.

The dataset card at `<https://huggingface.co/datasets/ucberkeley-dlab/measuring-hate-speech>` defines `hate_speech_score` as a continuous measure: higher is more hateful, above 0.5 is approximately hate speech, below −1 is counter or supportive speech, and −1 to 0.5 is neutral or ambiguous. The ten ordinal labels (`sentiment`, `respect`, `insult`, `humiliate`, `status`, `dehumanize`, `violence`, `genocide`, `attack_defend`, `hatespeech`) are combined into that score. The score is derived from the ordinals. It is not an eleventh annotator. The ordinals are what the annotator attests. The card does not assign the unlisted fit columns (`infitms`, `outfitms`, `std_err`, `hypothesis`) to the comment or to the annotator. The recipe records them of the comment, beside `hate_speech_score`, and that assignment is the recipe's, not the card's.

The ratings do not attest sense or dependency structure. Agreement among annotators is agreement about the rating. It is not agreement with a wordnet or a treebank. Fanout is the number of annotators on one comment, which is the degree of that claim, capped like any other fanout when [Pull](../../Semantics/Pull.md) walks it.

## Files, breakdown, and caveats

Taken from the recipe files. A line in a block is a directive. The prose above it is that file's own account of what is read, what is not, and what a row becomes.

### `measuring-hate-speech/annotations.recipe`

The set's file is Parquet; it is written out beside it as a table (extracted/, by parquet-to-text.py): the first row the columns' own names, every value as the file holds it. The set's card (README.md): "39,565 comments annotated by 7,912 annotators, for 135,556 combined rows", and ("Key dataset columns"):   comment_id - unique ID for each comment          annotator_id - unique ID for each annotator   text - lightly processed text of a social media post   hate_speech_score - continuous hate speech measure   sentiment, respect, insult, humiliate, status, dehumanize, violence, genocide, attack_defend, hatespeech -     ordinal label that is combined into the continuous score   annotator_severity - annotator's estimated survey interpretation bias A row is one annotator's reading of one comment. What the annotator answered of the comment (the ten labels, and whom the comment targets) the annotator says, of the comment. What the set measured of the comment, and what it holds of the annotator, the set says. The card does not say which of the columns it does not list belong to the comment and which to the reading: infitms, outfitms, std_err and hypothesis are recorded of the comment, as the columns beside hate_speech_score.

```text
match train-*.tsv
grammar table
header
escaped \
kinds own
kind comment_id comment_id
kind annotator_id annotator_id
claims
subject in comment_id
attest text platform hate_speech_score infitms outfitms std_err hypothesis
claims
subject in comment_id
attest sentiment respect insult humiliate status dehumanize violence genocide attack_defend hatespeech
witness in annotator_id
claims
subject in comment_id
attest target_*
witness in annotator_id
claims
subject in annotator_id
attest annotator_severity annotator_infitms annotator_outfitms
claims
subject in annotator_id
attest annotator_gender* annotator_trans* annotator_educ* annotator_income* annotator_ideology* annotator_age* annotator_race* annotator_religion* annotator_sexuality*
```

### `measuring-hate-speech/source`

Comments, each annotated by several annotators. The dataset card's title: "Dataset card for Measuring Hate Speech". Its data is in Parquet files only, which no recipe reads; the card itself is read as text. The deviation is this recipe's choice for a curated academic resource; the specification does not give one. The files are Parquet, read as they are written out in extracted/.

```text
witness Measuring Hate Speech
deviation 90
root $LAPLACE_DATA/.refresh-*/Safety/MeasuringHateSpeech/measuring-hate-speech-*[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]
except *.parquet */extracted/measuring-hate-speech.tsv
reads text
```
