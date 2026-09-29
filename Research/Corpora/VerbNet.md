# VerbNet

VerbNet attests class membership of a verb and the thematic roles and frames of that class.

The composition is a verb in a class. The mask is class membership, and with it the thematic roles and syntactic frames of that class. The value is the class. Witness VerbNet, the 3.4 release the recipe reads from the refresh extract of `verbnet3.4`. Deviation 90, the recipe's choice. Loaded measure: 96,668 compositions from 3.2 MB. The live tree is the June unpack of `verbnet-master.zip`, which is the same project at a branch tip rather than the pinned release.

A class membership does not attest a FrameNet frame or a PropBank roleset. Those joins are [SemLink](SemLink.md) and [Predicate Matrix](Predicate-Matrix.md). Fanout is the number of members and roles leaving a class. The hop stops at the class unless one of those mappings continues it. VerbNet does not attest the dependency role of a token in a sentence.

## Files, breakdown, and caveats

Taken from the recipe files. A line in a block is a directive. The prose above it is that file's own account of what is read, what is not, and what a row becomes.

### `verbnet/classes.recipe`

A class file. A class and a subclass are their IDs and a member its key; everything else speaks of the class it is inside.

```text
match *.xml
grammar xml
identity VNCLASS ID
identity VNSUBCLASS ID
identity MEMBER verbnet_key
```

### `verbnet/source`

VerbNet's classes: their members, thematic roles and frames. The deviation is this recipe's choice for a curated academic resource; the specification does not give one. Measured when it was loaded: 96,668 compositions from 3.2 MB, at 750 bytes each with their indexes and standings.

```text
witness VerbNet
deviation 90
root $LAPLACE_DATA/.refresh-*/VerbNet/extracted/verbnet-*/verbnet3.4
```
