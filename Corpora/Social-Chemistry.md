# Social Chemistry

Social-Chem-101 attests what a breakdown row says of its rule of thumb, which is the rule's text, as one record of the set; the row's ids are internal pointers recorded nowhere, and its bookkeeping columns attest nothing.

The source is the "Social-Chem-101 Dataset": rules of thumb written by workers about situations, and the breakdowns workers made of them. One recipe reads its one table.

## Source

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `social-chemistry-101` | `Social-Chem-101 Dataset` | class `AcademicCurated` | `unicode`, `iso-639` | `social-chem-101.v1.0.tsv` | [`breakdowns.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/social-chemistry-101/breakdowns.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior is the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## The breakdowns

"The dataset is tab-separated with the following columns" (README), and its first row names them. A row is one worker's breakdown of one rule of thumb. It is said of the rule of thumb, which is its `rot`, the rule's text; its `rot-id` is the set's pointer to it, recorded nowhere. What the row says it says together: one record, witnessed once by the set, and its claims within it, so one worker's answers stay in one record. The worker is not a witness: the set is. An empty field attests nothing; the README says an empty answer means the question was unanswered.

The file writes a field that holds a double quote between double quotes, with the quote doubled; the recipe reads that notation (`quoted`).

The Specification cells are from `README.v1.0.md`, "Dataset Columns".

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `rot-id` | an id | a pointer: the set's id of the rule of thumb, recorded nowhere (`key row rot-id`) | none | "ID of the rule of thumb"; it includes the worker id of the RoT author and which RoT it was, from 1 to 5 |
| `rot` | text | the subject: the rule of thumb, which is its text (`thing row rot`) | the first part of every claim of the row | the rule of thumb written by the worker |
| `rot-worker-id` | an id | a pointer, recorded nowhere | none | the worker who wrote this rule of thumb; no relation to the breakdown worker, except by coincidence |
| `breakdown-worker-id` | an id | a pointer, recorded nowhere | none | the worker who did this RoT breakdown |
| `area` | a name | said of the rule | `[rot, area, value]` | source of the situation: confessions, dearabby, rocstories, amitheasshole |
| `m` | a number | content of the row, not attested | none | how many workers did the RoT breakdown for this RoT: 1, 3, 5, 50 |
| `split` | a name | bookkeeping: `omit` | none | which split this RoT belongs to: train, dev, test, dev-extra, test-extra, analysis, none |
| `rot-agree` | `0` to `4` | said of the rule | `[rot, rot-agree, value]` | what portion of people probably agree with the rule of thumb; buckets in order: below 1%, 5% to 25%, 50%, 75% to 90%, above 99% |
| `rot-categorization` | `morality-ethics\|social-norms` | each part said of the rule under the column's name | `[rot, rot-categorization, morality-ethics]` | '"\|" separated list' of 0 to 4 RoT categorizations: morality-ethics, social-norms, advice, description |
| `rot-moral-foundations` | parts joined by `\|` | each part said of the rule | `[rot, rot-moral-foundations, care-harm]` | '"\|" separated list' of 0 to 5 moral-foundation axes: care-harm, fairness-cheating, loyalty-betrayal, authority-subversion, sanctity-degradation |
| `rot-char-targeting` | `char-none` or `char-N` | said of the rule | `[rot, rot-char-targeting, value]` | who the RoT is most likely targeting; char-N is a 0-index into `characters` |
| `rot-bad` | `0` or `1` | bookkeeping: `omit` | none | whether the worker labeled the RoT as confusing, extremely vague, very low quality, or not splittable into action and judgment |
| `rot-judgment` | text | said of the rule | `[rot, rot-judgment, text]` | worker-written judgment portion of the RoT |
| `action` | text | said of the rule | `[rot, action, text]` | the action, a conjugated or tweaked substring of the RoT, written by the worker |
| `action-agency` | `agency` or `experience` | said of the rule | `[rot, action-agency, value]` | whether the action is something you do or control, or something you experience |
| `action-moral-judgment` | `-2` to `2` | said of the rule | `[rot, action-moral-judgment, value]` | which bucket matches the RoT's judgment of the action: very bad, bad, expected/OK, good, very good |
| `action-agree` | `0` to `4` | said of the rule | `[rot, action-agree, value]` | what portion of people probably agree that the action is that judgment; the buckets of `rot-agree` |
| `action-legal` | `legal`, `illegal`, `tolerated` | said of the rule | `[rot, action-legal, value]` | how legal the action is where the worker lives |
| `action-pressure` | `-2` to `2` | said of the rule | `[rot, action-pressure, value]` | how much cultural pressure the worker feels about the action: strong pressure against, pressure against, discretionary, pressure for, strong pressure for |
| `action-char-involved` | `char-none` or `char-N` | said of the rule | `[rot, action-char-involved, value]` | who is most likely to do the action or its opposite |
| `action-hypothetical` | a name | said of the rule | `[rot, action-hypothetical, value]` | whether that character is explicitly doing the action, or the action might happen: explicit-no, probable-no, hypothetical, probable, explicit |
| `situation` | text | said of the rule | `[rot, situation, text]` | text of the situation |
| `situation-short-id` | an id | a pointer, recorded nowhere | none | unique id for the situation |
| `n-characters` | a number | bookkeeping: `omit` | none | how many characters were identified in the story during the character-identification task |
| `characters` | parts joined by `\|` | each part said of the rule under the column's name | `[rot, characters, narrator]` | '"\|" separated list' of the characters that appeared |

Nothing else is attested. The README is not read: no recipe of the source matches it, and the source does not read text (`reads`), so nothing of it is recorded.
