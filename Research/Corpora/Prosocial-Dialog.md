# ProsocialDialog

ProsocialDialog attests a reply to an utterance, the rule of thumb the reply rests on, and the safety labels workers gave.

The composition is an utterance paired with a response. The masks are the ones the release fills: the response, the rule of thumb the response is grounded in, and the safety labels three workers gave. The value is that field. Witness ProsocialDialog, deviation 90, the recipe's choice. The recipe reads the refresh drop. There is no live directory.

A rule of thumb here is this dataset's text, not a row of [Social Chemistry](Social-Chemistry.md), unless the release says it was taken from there. It does not attest a wordnet sense or a dependency role. Three workers are three witnesses of the label on the same pair. Fanout is those three, plus the link from the response to the rule it cites. The utterance text itself is observed.

## Files, breakdown, and caveats

Taken from the recipe files. A line in a block is a directive. The prose above it is that file's own account of what is read, what is not, and what a row becomes.

### `prosocial-dialog/dialogues.recipe`

A JSON object on every line. The dataset card: `context` "the potentially unsafe utterance"; `safety_label` "the final verdict of the context"; `safety_annotations` "raw annotations from three workers". So an object is the thing its "context" names, and every other member is said of it under its own key.

```text
match train.json test.json valid.json
grammar json
records
identity * context
```

### `prosocial-dialog/source`

ProsocialDialog: dialogues in which an utterance is answered by a response grounded in rules-of-thumb, with the safety labels three workers gave. The dataset card's title: "Dataset Card for ProsocialDialog Dataset". The deviation is this recipe's choice for a curated academic resource; the specification does not give one.

```text
witness ProsocialDialog
deviation 90
root $LAPLACE_DATA/.refresh-*/Safety/ProsocialDialog/prosocial-dialog-*[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]
reads text
```
