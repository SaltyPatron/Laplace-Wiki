# PropBank

PropBank attests a predicate's roleset and the roles in it.

The composition is a predicate roleset. The mask is the role of an argument of that predicate. The value is the roleset and the numbered or named role. The frames also record links to VerbNet and FrameNet. Those links are hops the PropBank file itself writes down. They are still the same witness's claim about the link, not VerbNet attesting the roleset.

Witness PropBank, deviation 90, the recipe's choice. The recipe reads the refresh extract of `frames/`. Loaded measure: 1,146,056 compositions from 30 MB. The live `propbank-frames-main.zip` unpack is the June branch tip of the same frames. Fanout is the number of roles leaving a roleset. A roleset does not attest a wordnet sense except where the link says so, and it does not attest a universal dependency label.

## Files, breakdown, and caveats

Taken from the recipe files. A line in a block is a directive. The prose above it is that file's own account of what is read, what is not, and what a row becomes.

### `propbank/frames.recipe`

A frame file. A predicate is its lemma and a roleset its id; everything else speaks of the roleset it is inside.

```text
match *.xml
grammar xml
identity predicate lemma
identity roleset id
```

### `propbank/source`

PropBank's frame files: every predicate's rolesets, their roles, and their links to VerbNet and FrameNet. The deviation is this recipe's choice for a curated academic resource; the specification does not give one. Measured when it was loaded: 1,146,056 compositions from 30 MB, at 750 bytes each with their indexes and standings.

```text
witness PropBank
deviation 90
root $LAPLACE_DATA/.refresh-*/PropBank/extracted/propbank-*/frames
```
