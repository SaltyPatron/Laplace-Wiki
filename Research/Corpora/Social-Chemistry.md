# Social Chemistry

Social-Chem-101 attests rules of thumb about situations and the breakdowns workers made of them.

## Files

| Path | Bytes | What the file is | Proof |
| --- | --- | --- | --- |
| `/vault/Data/.refresh-20260903/Safety/SocialChemistry101/social-chem-101.zip` | 27610699 | Zip archive beside the extracted files. The archive was not opened. | `stat` |
| `/vault/Data/.refresh-20260903/Safety/SocialChemistry101/extracted/social-chem-101/README.v1.0.md` | 12886 | Social-Chem-101 v1.0 README shipped with the dataset. Section Dataset Columns defines the TSV columns. | The file |
| `/vault/Data/.refresh-20260903/Safety/SocialChemistry101/extracted/social-chem-101/social-chem-101.v1.0.tsv` | 147421453 | Tab-separated table. The header names the 25 columns in the README's order. | Header line; `csv.reader` counted 355922 data rows |

## Attestations

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| `area` | Source of the situation. The README's values are confessions, dearabby, rocstories, amitheasshole. | the situation | one of those four strings | the dataset, not a breakdown worker | README.v1.0.md, Dataset Columns |
| `m` | How many workers did the RoT breakdown for this RoT. The README's values are 1, 3, 5, 50. | the rule of thumb | that count | the dataset | README.v1.0.md, Dataset Columns |
| `split` | Which split this RoT belongs to. The README's values are train, dev, test, dev-extra, test-extra, analysis, none. | the rule of thumb | that split name | the dataset | README.v1.0.md, Dataset Columns |
| `rot-agree` | Worker answer to what portion of people probably agree with the rule of thumb. Buckets in order: below 1%, 5% to 25%, 50%, 75% to 90%, above 99%. Empty means the question was unanswered. | the rule of thumb | 0, 1, 2, 3, 4, or empty | `breakdown-worker-id` | README.v1.0.md, Dataset Columns |
| `rot-categorization` | Worker-labeled list of 0 to 4 RoT categorizations, separated by a vertical bar. Choices: morality-ethics, social-norms, advice, description. | the rule of thumb | that list | `breakdown-worker-id` | README.v1.0.md, Dataset Columns |
| `rot-moral-foundations` | Worker-labeled list of 0 to 5 moral-foundation axes, separated by a vertical bar. Choices: care-harm, fairness-cheating, loyalty-betrayal, authority-subversion, sanctity-degradation. | the rule of thumb | that list | `breakdown-worker-id` | README.v1.0.md, Dataset Columns |
| `rot-char-targeting` | Worker answer to who the RoT is most likely targeting. Empty means unanswered. char-none means no one listed. char-N is a 0-index into `characters`, and N is 0 to 5. | the rule of thumb | char-none, char-N, or empty | `breakdown-worker-id` | README.v1.0.md, Dataset Columns |
| `rot-bad` | Whether the worker labeled the RoT as confusing, extremely vague, very low quality, or not splittable into action and judgment. | the rule of thumb | 0 or 1 | `breakdown-worker-id` | README.v1.0.md, Dataset Columns |
| `rot-judgment` | Worker-written judgment portion of the RoT. The README says it was intended to be thrown away and was used for priming. Empty means unanswered. | the rule of thumb | that string, or empty | `breakdown-worker-id` | README.v1.0.md, Dataset Columns |
| `action` | The action, a conjugated or tweaked substring of the RoT, written by the worker. Empty means unanswered. | the action the worker wrote | that string, or empty | `breakdown-worker-id` | README.v1.0.md, Dataset Columns |
| `action-agency` | Worker answer to whether the action is something you do or control, or something you experience. Empty means unanswered. | the action | agency, experience, or empty | `breakdown-worker-id` | README.v1.0.md, Dataset Columns |
| `action-moral-judgment` | Worker answer for which bucket matches the RoT's judgment of the action. Buckets in order: very bad, bad, expected/OK, good, very good. Empty means unanswered. | the action | -2, -1, 0, 1, 2, or empty | `breakdown-worker-id` | README.v1.0.md, Dataset Columns |
| `action-agree` | Worker answer to what portion of people probably agree that the action is that judgment. Same buckets as `rot-agree`. Empty means unanswered. | the action | 0, 1, 2, 3, 4, or empty | `breakdown-worker-id` | README.v1.0.md, Dataset Columns |
| `action-legal` | Worker answer to how legal the action is where the worker lives. Empty means unanswered. | the action | legal, illegal, tolerated, or empty | `breakdown-worker-id` | README.v1.0.md, Dataset Columns |
| `action-pressure` | Worker answer to how much cultural pressure they feel about the action. Buckets in order: strong pressure against, pressure against, discretionary, pressure for, strong pressure for. Empty means unanswered. | the action | -2, -1, 0, 1, 2, or empty | `breakdown-worker-id` | README.v1.0.md, Dataset Columns |
| `action-char-involved` | Worker answer to who is most likely to do the action or its opposite. Empty, char-none, and char-N mean the same as in `rot-char-targeting`. | the action | char-none, char-N, or empty | `breakdown-worker-id` | README.v1.0.md, Dataset Columns |
| `action-hypothetical` | Worker answer to whether that character is explicitly doing the action, or the action might happen. Empty means unanswered. The README says the question is skipped, and left empty, when `action-char-involved` is char-none. | the action | explicit-no, probable-no, hypothetical, probable, explicit, or empty | `breakdown-worker-id` | README.v1.0.md, Dataset Columns |
| `situation` | Text of the situation. | the situation | that text | the dataset. Not a breakdown answer. | README.v1.0.md, Dataset Columns |
| `situation-short-id` | Unique id for the situation. The README calls it shorter and more convenient. | the situation | that id | the dataset | README.v1.0.md, Dataset Columns |
| `rot` | The rule of thumb written by the worker. | the rule of thumb | that text | `rot-worker-id` | README.v1.0.md, Dataset Columns |
| `rot-id` | Id of the rule of thumb. The README says it includes the worker id of the RoT author and which RoT it was, from 1 to 5. | the rule of thumb | that id | the dataset | README.v1.0.md, Dataset Columns |
| `rot-worker-id` | The worker who wrote this rule of thumb. The README says there is no relation to the breakdown worker, except by coincidence. | that worker | that id | the dataset | README.v1.0.md, Dataset Columns |
| `breakdown-worker-id` | The worker who did this RoT breakdown. The README says there is no relation to the worker who wrote the RoT, except by coincidence. | that worker | that id | the dataset | README.v1.0.md, Dataset Columns |
| `n-characters` | How many characters were identified in the story during the character-identification task. The README says the minimum is 1, because the narrator is included, and that 10 is the maximum seen, with no stated upper limit. At most 6 characters are displayed. | the situation | that count | the character-identification task, not the breakdown worker | README.v1.0.md, Dataset Columns and section 2 |
| `characters` | Vertical-bar-separated list of characters that appeared. The README says 1 to 6 are shown. It also says three character annotations were collected per situation and the largest set from any one annotator was kept. | the situation | that list | the character-identification task, not the breakdown worker | README.v1.0.md, Dataset Columns and section 2 |

## Records

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| `social-chem-101.v1.0.tsv` row | `area`, `m`, `split`, `rot-agree`, `rot-categorization`, `rot-moral-foundations`, `rot-char-targeting`, `rot-bad`, `rot-judgment`, `action`, `action-agency`, `action-moral-judgment`, `action-agree`, `action-legal`, `action-pressure`, `action-char-involved`, `action-hypothetical`, `situation`, `situation-short-id`, `rot`, `rot-id`, `rot-worker-id`, `breakdown-worker-id`, `n-characters`, `characters` | One tab-separated row. The columns hold one situation, one rule of thumb, and one worker's breakdown of that rule. | Header matches the README column order. `csv.reader` counted 355922 data rows and 25 fields. |

## Lineage

| Paths | What is shared | Proof |
| --- | --- | --- |
| `social-chem-101.zip` and `extracted/social-chem-101/` | Both sit in `SocialChemistry101`. The zip was not opened, so identity with the extracted TSV was not checked. | `stat` on both paths |
