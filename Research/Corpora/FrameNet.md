# FrameNet

FrameNet attests frames, the roles in them, and the lexical units that evoke them.

The composition is a frame, a frame element, or a lexical unit. The mask on a lexical unit is the frame it evokes. The value is that frame, its elements, and the relations between frames. Annotated sentences attest that a span in a sentence evokes the frame. That is a claim about the span, not a claim that the frame owns the word.

Witness FrameNet, release 1.7, deviation 90, the recipe's choice. Read from `framenet_v17`, with both the refresh extract and the live tree declared. Loaded measure: 15,952,613 compositions from 854 MB. `framenet_v17.zip` is that release again. [Relations Research](../Relations.md#local-datasets) counts 1,221 frames in this release.

The hop to a wordnet sense or a PropBank role is not in FrameNet's own files. It is in [SemLink](SemLink.md), [Predicate Matrix](Predicate-Matrix.md), [MapNet](MapNet.md), and [FrameBase](FrameBase.md). Fanout is the number of lexical units and frame elements leaving a frame, which [Pull](../../Semantics/Pull.md) caps. FrameNet does not attest a universal dependency relation.

## Files, breakdown, and caveats

Taken from the recipe files. A line in a block is a directive. The prose above it is that file's own account of what is read, what is not, and what a row becomes.

### `framenet/framenet.recipe`

FrameNet's XML. FrameNet numbers each kind of thing from one: the number 4489 is a frame element, a lexical unit, a lemma, a lexeme and a word form, five different things. So a thing is named by its kind and its name together, as FrameNet's own attributes do when they refer to one (feID, luID, lemmaID, frameName): [FE, 4489], [frame, Abandonment]. Every name and value is as the files write them. the things, and what names each elements that are a frame element spoken of again attributes that name a thing a frame's relation to another frame: `<frameRelation type="Inherits from">``<relatedFrame>`Name`</relatedFrame>` a label speaks of the stretch of its sentence's text from start to end; FrameNet's end is the last character

```text
match *.xml
grammar xml
identity frame name kind
identity FE ID kind
identity lexUnit ID kind
identity lu ID kind lexUnit
identity semType name kind
identity superType superTypeName kind semType
identity corpus name kind
identity document name kind
identity sentence ID kind
identity annotationSet ID kind
identity annoSet ID kind annotationSet
identity frameRelationType name kind
identity statusType name kind
identity Lemma id kind
identity WordForm id kind
identity WordForm ID kind
identity Lexeme ID kind
identity memberFE ID kind FE
identity requiresFE ID kind FE
identity excludesFE ID kind FE
refer lexUnit.frame frame
refer frameName frame
refer feID FE
refer luID lexUnit
refer lemmaID Lemma
refer frameRelation.subFrameName frame
refer frameRelation.superFrameName frame
refer FERelation.subID FE
refer FERelation.supID FE
```

### `framenet/source`

FrameNet Release 1.7 (Berkeley FrameNet, ICSI), in the form NLTK redistributes: frames with their frame elements and lexical units, the relations between frames, the semantic types, the lemma and lexeme tables, and the annotated sentences of the lexical units and of the full texts. README.txt: "Welcome to Release 1.7 of the FrameNet data!" ... "The FrameNet database in XML format" The deviation is this recipe's choice for a curated academic resource; the specification does not give one. Measured when it was loaded: 15,952,613 compositions from 854 MB, at 750 bytes each with their indexes and standings.

```text
witness FrameNet
deviation 90
root $LAPLACE_DATA/.refresh-*/FrameNet/framenet_v17
root $LAPLACE_DATA/FrameNet/framenet_v17
reads text
```
