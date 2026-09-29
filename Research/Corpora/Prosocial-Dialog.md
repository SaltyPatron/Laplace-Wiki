# ProsocialDialog

ProsocialDialog attests a reply to an utterance, the rule of thumb the reply rests on, and the safety labels workers gave.

## Files

| Path | Bytes | What the file is | Proof |
| --- | --- | --- | --- |
| /vault/Data/.refresh-20260903/Safety/ProsocialDialog/prosocial-dialog-d77d7ad3c624c51030f2f32c83e892b3d620b3d4.commit.tsv | 119 | Tab-separated snapshot id, source, and time: d77d7ad3c624c51030f2f32c83e892b3d620b3d4, allenai/prosocial-dialog, 2026-09-03T09:58:34Z. | The file itself. Source link: [allenai/prosocial-dialog](https://huggingface.co/datasets/allenai/prosocial-dialog). |
| /vault/Data/.refresh-20260903/Safety/ProsocialDialog/prosocial-dialog-d77d7ad3c624c51030f2f32c83e892b3d620b3d4.files.sha256 | 397 | sha256 sidecar. Each line is a digest and a path in the snapshot. | The file itself. |
| /vault/Data/.refresh-20260903/Safety/ProsocialDialog/prosocial-dialog-d77d7ad3c624c51030f2f32c83e892b3d620b3d4/.gitattributes | 2362 | Git LFS attributes for the snapshot. | The file itself. |
| /vault/Data/.refresh-20260903/Safety/ProsocialDialog/prosocial-dialog-d77d7ad3c624c51030f2f32c83e892b3d620b3d4/README.md | 3762 | Dataset card stored with the snapshot. Its safety_label sentence matches the publisher card that was opened. | [ProsocialDialog card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md) |
| /vault/Data/.refresh-20260903/Safety/ProsocialDialog/train.json | 85050121 | Train split, one JSON object per line. Byte-identical to the snapshot copy. | [ProsocialDialog card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md). cmp -s exit 0. |
| /vault/Data/.refresh-20260903/Safety/ProsocialDialog/prosocial-dialog-d77d7ad3c624c51030f2f32c83e892b3d620b3d4/train.json | 85050121 | Snapshot copy of train.json. | [ProsocialDialog card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md) |
| /vault/Data/.refresh-20260903/Safety/ProsocialDialog/valid.json | 14421180 | Validation split, one JSON object per line. Byte-identical to the snapshot copy. | [ProsocialDialog card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md). cmp -s exit 0. |
| /vault/Data/.refresh-20260903/Safety/ProsocialDialog/prosocial-dialog-d77d7ad3c624c51030f2f32c83e892b3d620b3d4/valid.json | 14421180 | Snapshot copy of valid.json. | [ProsocialDialog card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md) |
| /vault/Data/.refresh-20260903/Safety/ProsocialDialog/test.json | 17644365 | Test split, one JSON object per line. Byte-identical to the snapshot copy. | [ProsocialDialog card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md). cmp -s exit 0. |
| /vault/Data/.refresh-20260903/Safety/ProsocialDialog/prosocial-dialog-d77d7ad3c624c51030f2f32c83e892b3d620b3d4/test.json | 17644365 | Snapshot copy of test.json. | [ProsocialDialog card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md) |
| /vault/Data/.refresh-20260903/.jobs/prosocial-dialog.log | 112 | Refresh log. First line: dataset-estate-refresh: prosocial-dialog LFS snapshot already present: d77d7ad3c624c51030f2f32c83e892b3d620b3d4 | The file itself. |
| /vault/Data/.refresh-20260903/.jobs/prosocial-dialog.pid | 8 | Refresh pid file. Contents: 3973718 | The file itself. |
| /vault/Data/.refresh-20260903/.jobs/prosocial-dialog.rc | 2 | Refresh exit file. Contents: 0 | The file itself. |

## Attestations

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| context | the potentially unsafe utterance | the utterance | string | GPT-3. The card's creation section says GPT-3 generates the potentially unsafe utterances. | [ProsocialDialog card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md); /vault/Data/.refresh-20260903/Safety/ProsocialDialog/prosocial-dialog-d77d7ad3c624c51030f2f32c83e892b3d620b3d4/README.md |
| response | the guiding utterance grounded on rules-of-thumb (rots) | the context | string | crowdworkers. The card's creation section says crowdworkers provide prosocial responses. | [ProsocialDialog card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md); /vault/Data/.refresh-20260903/Safety/ProsocialDialog/prosocial-dialog-d77d7ad3c624c51030f2f32c83e892b3d620b3d4/README.md |
| rots | the relevant rules-of-thumb for text not labeled as __casual__. The card writes text in that sentence. | the context | list of string or null | Not defined. The card does not name who wrote the rules. | [ProsocialDialog card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md); /vault/Data/.refresh-20260903/Safety/ProsocialDialog/prosocial-dialog-d77d7ad3c624c51030f2f32c83e892b3d620b3d4/README.md |
| safety_label | the final verdict of the context according to safety_annotations: __casual__, __possibly_needs_caution__, __probably_needs_caution__, __needs_caution__, __needs_intervention__ | the context | one of those five strings | derived from safety_annotations. Not a fourth worker. | [ProsocialDialog card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md); /vault/Data/.refresh-20260903/Safety/ProsocialDialog/prosocial-dialog-d77d7ad3c624c51030f2f32c83e892b3d620b3d4/README.md |
| safety_annotations | raw annotations from three workers: casual, needs caution, needs intervention | the context | list of three strings | the three workers | [ProsocialDialog card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md); /vault/Data/.refresh-20260903/Safety/ProsocialDialog/prosocial-dialog-d77d7ad3c624c51030f2f32c83e892b3d620b3d4/README.md |
| safety_annotation_reasons | the reasons behind the safety annotations in free-form text from each worker | the context | list of strings | the three workers | [ProsocialDialog card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md); /vault/Data/.refresh-20260903/Safety/ProsocialDialog/prosocial-dialog-d77d7ad3c624c51030f2f32c83e892b3d620b3d4/README.md |
| source | the source of the seed text that was used to craft the first utterance of the dialogue: socialchemistry, sbic, ethics_amt, ethics_reddit | the dialogue | one of those four strings | ProsocialDialog | [ProsocialDialog card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md); /vault/Data/.refresh-20260903/Safety/ProsocialDialog/prosocial-dialog-d77d7ad3c624c51030f2f32c83e892b3d620b3d4/README.md |
| etc | other information | the dialogue turn | string or null | ProsocialDialog | [ProsocialDialog card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md); /vault/Data/.refresh-20260903/Safety/ProsocialDialog/prosocial-dialog-d77d7ad3c624c51030f2f32c83e892b3d620b3d4/README.md |
| dialogue_id | the dialogue index | the dialogue | int | ProsocialDialog | [ProsocialDialog card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md); /vault/Data/.refresh-20260903/Safety/ProsocialDialog/prosocial-dialog-d77d7ad3c624c51030f2f32c83e892b3d620b3d4/README.md |
| response_id | the response index | the turn | int | ProsocialDialog | [ProsocialDialog card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md); /vault/Data/.refresh-20260903/Safety/ProsocialDialog/prosocial-dialog-d77d7ad3c624c51030f2f32c83e892b3d620b3d4/README.md |
| episode_done | an indicator of whether it is the end of the dialogue | the turn | bool | ProsocialDialog | [ProsocialDialog card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md); /vault/Data/.refresh-20260903/Safety/ProsocialDialog/prosocial-dialog-d77d7ad3c624c51030f2f32c83e892b3d620b3d4/README.md |

## Records

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| dialogue turn | context, response, rots, safety_label, safety_annotations, safety_annotation_reasons, source, etc, dialogue_id, response_id, episode_done | One turn: an utterance, the reply, the rules of thumb, and the safety labels. The card says 58K dialogues, 331K utterances, 160K unique RoTs, and 497K dialogue safety labels. Key order was read from the first line of train.json, valid.json, and test.json. | [ProsocialDialog card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md) |

## Lineage

| Paths | What is shared | Proof |
| --- | --- | --- |
| ProsocialDialog/*.json and prosocial-dialog-d77d7ad3c624c51030f2f32c83e892b3d620b3d4/*.json | train.json, valid.json, and test.json are each byte-identical to the snapshot copy (cmp -s exit 0). | cmp -s on this machine. |
| safety_label and safety_annotations | The card says safety_label is the final verdict of the context according to the three workers' safety_annotations. | [ProsocialDialog card](https://huggingface.co/datasets/allenai/prosocial-dialog/raw/main/README.md) |
| dialogues.recipe | The recipe match is train.json test.json valid.json. | [dialogues.recipe](/repos/src/Laplace-Engine/recipes/prosocial-dialog/dialogues.recipe) |
