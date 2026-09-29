# Social Bias Frames

Social Bias Frames attests what workers said a post implied, both per annotation and aggregated per post.

The composition is a post. The mask is the implication the worker recorded: the frame's fields for what the post conveys. The value is that record. The release has the individual annotations and the same annotations aggregated per post. The aggregate is derived from the annotations. It is lineage of those annotations, not a second group of workers. Witness Social Bias Frames, the v2 release, deviation 90, the recipe's choice. The recipe reads the refresh drop. There is no live directory.

The frame here is this dataset's frame, not a [FrameNet](FrameNet.md) frame, unless a mapping says so. No such mapping is in the drop. The post text does not attest sense or dependency role. Fanout is the number of workers on a post. The aggregate collapses that fanout into one derived value and must not be walked as if the workers had spoken again.

## Files, breakdown, and caveats

Taken from the recipe files. A line in a block is a directive. The prose above it is that file's own account of what is read, what is not, and what a row becomes.

### `social-bias-frames/aggregated.recipe`

The set's README ("Aggregation"): the files "aggregated per post": for a post, the mean of whoTarget, intentYN, sexYN and offensiveYN over its annotations, the set of what was written as targetMinority, targetCategory and targetStereotype, each written as a JSON list ("To load the list of implications, use json.loads"), and hasBiasedImplication. A post has no HITId here: it is the text it is. The first column has no name and says nothing.

```text
match SBIC.v2.agg.*.csv
grammar table
separator ,
header
quoted
claims
together
subject in post
attest *
```

### `social-bias-frames/annotations.recipe`

The set's README: "Each line in the file contains the following fields (in order)":   whoTarget: group vs. individual target;  intentYN: was the intent behind the statement to offend;   sexYN: is the post a sexual or lewd reference;  sexReason: free text explanations of what is sexual;   offensiveYN: could the post be offensive to anyone;  sexPhrase: part of the post that references something sexual;   speakerMinorityYN: whether the speaker was part of the same minority group that's being targeted;   WorkerId: hashed version of the MTurk workerId;  HITId: id that uniquely identifies each post;   annotatorGender, annotatorMinority, annotatorPolitics, annotatorRace, annotatorAge: of the MTurk worker;   post: post that was annotated;  targetMinority: demographic group targeted;   targetCategory: high-level category of the demographic group(s) targeted;  targetStereotype: implied statement;   dataSource: source of the post A line is one worker's reading of one post. What the worker answered of the post, the worker says, of the post; what the line holds of the worker is said of the worker; the post's text and source, the set says.

```text
match SBIC.v2.trn.csv SBIC.v2.dev.csv SBIC.v2.tst.csv
grammar table
separator ,
header
quoted
kinds own
kind HITId HITId
kind WorkerId WorkerId
claims
subject in HITId
attest post dataSource
claims
subject in HITId
attest whoTarget intentYN sexYN sexReason offensiveYN sexPhrase speakerMinorityYN targetMinority targetCategory targetStereotype
witness in WorkerId
claims
subject in WorkerId
attest annotator*
```

### `social-bias-frames/source`

The README: "the data splits from v2 of Social Bias Frames / Social Bias Inference Corpus": posts, and what MTurk workers said of each; and the same aggregated per post. The deviation is this recipe's choice for a curated academic resource; the specification does not give one.

```text
witness Social Bias Frames
deviation 90
root $LAPLACE_DATA/.refresh-*/Safety/SocialBiasFrames/extracted
reads text
```
