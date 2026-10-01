# Social Chemistry

Social-Chem-101 attests everything a breakdown row says of its rule of thumb as one record of the set, and a row whose situation, characters, rule, action, or judgment holds a double quote is not read.

The source is the "Social-Chem-101 Dataset": rules of thumb written by workers about situations, and the breakdowns workers made of them. One recipe reads its one table.

## Source

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `social-chemistry-101` | `Social-Chem-101 Dataset` | class `AcademicCurated` | `unicode`, `iso-639` | `social-chem-101.v1.0.tsv` | [`breakdowns.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/social-chemistry-101/breakdowns.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior is the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## The breakdowns

"The dataset is tab-separated with the following columns" (README), and its first row names them. A row is one worker's breakdown of one rule of thumb. It is said of the row's `rot-id`, and what the row says it says together: one record, witnessed once by the set, and its claims within it, so the worker (`breakdown-worker-id`) and the worker's answers stay in one record. The worker is not a witness: the set is. An empty field attests nothing; the README says an empty answer means the question was unanswered.

The file writes a field that holds a double quote between double quotes, with the quote doubled. The table reader does not read that notation, so a row whose `situation`, `characters`, `rot`, `action`, or `rot-judgment` begins with a double quote is left unread rather than recorded as written.

The Specification cells are from `README.v1.0.md`, "Dataset Columns".

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `rot-id` | an id | the subject: the rule of thumb, by its id as written | | "ID of the rule of thumb"; it includes the worker id of the RoT author and which RoT it was, from 1 to 5 |
| `rot` | text | said of the rule under the column's name | `[rot-id, rot, text]` | the rule of thumb written by the worker |
| `rot-worker-id` | an id | said of the rule | `[rot-id, rot-worker-id, value]` | the worker who wrote this rule of thumb; no relation to the breakdown worker, except by coincidence |
| `breakdown-worker-id` | an id | said of the rule | `[rot-id, breakdown-worker-id, value]` | the worker who did this RoT breakdown |
| `area` | a name | said of the rule | `[rot-id, area, value]` | source of the situation: confessions, dearabby, rocstories, amitheasshole |
| `m` | a number | said of the rule | `[rot-id, m, value]` | how many workers did the RoT breakdown for this RoT: 1, 3, 5, 50 |
| `split` | a name | said of the rule | `[rot-id, split, value]` | which split this RoT belongs to: train, dev, test, dev-extra, test-extra, analysis, none |
| `rot-agree` | `0` to `4` | said of the rule | `[rot-id, rot-agree, value]` | what portion of people probably agree with the rule of thumb; buckets in order: below 1%, 5% to 25%, 50%, 75% to 90%, above 99% |
| `rot-categorization` | `morality-ethics\|social-norms` | each part said of the rule under the column's name | `[rot-id, rot-categorization, morality-ethics]` | '"\|" separated list' of 0 to 4 RoT categorizations: morality-ethics, social-norms, advice, description |
| `rot-moral-foundations` | parts joined by `\|` | each part said of the rule | `[rot-id, rot-moral-foundations, care-harm]` | '"\|" separated list' of 0 to 5 moral-foundation axes: care-harm, fairness-cheating, loyalty-betrayal, authority-subversion, sanctity-degradation |
| `rot-char-targeting` | `char-none` or `char-N` | said of the rule | `[rot-id, rot-char-targeting, value]` | who the RoT is most likely targeting; char-N is a 0-index into `characters` |
| `rot-bad` | `0` or `1` | said of the rule | `[rot-id, rot-bad, value]` | whether the worker labeled the RoT as confusing, extremely vague, very low quality, or not splittable into action and judgment |
| `rot-judgment` | text | said of the rule | `[rot-id, rot-judgment, text]` | worker-written judgment portion of the RoT |
| `action` | text | said of the rule | `[rot-id, action, text]` | the action, a conjugated or tweaked substring of the RoT, written by the worker |
| `action-agency` | `agency` or `experience` | said of the rule | `[rot-id, action-agency, value]` | whether the action is something you do or control, or something you experience |
| `action-moral-judgment` | `-2` to `2` | said of the rule | `[rot-id, action-moral-judgment, value]` | which bucket matches the RoT's judgment of the action: very bad, bad, expected/OK, good, very good |
| `action-agree` | `0` to `4` | said of the rule | `[rot-id, action-agree, value]` | what portion of people probably agree that the action is that judgment; the buckets of `rot-agree` |
| `action-legal` | `legal`, `illegal`, `tolerated` | said of the rule | `[rot-id, action-legal, value]` | how legal the action is where the worker lives |
| `action-pressure` | `-2` to `2` | said of the rule | `[rot-id, action-pressure, value]` | how much cultural pressure the worker feels about the action: strong pressure against, pressure against, discretionary, pressure for, strong pressure for |
| `action-char-involved` | `char-none` or `char-N` | said of the rule | `[rot-id, action-char-involved, value]` | who is most likely to do the action or its opposite |
| `action-hypothetical` | a name | said of the rule | `[rot-id, action-hypothetical, value]` | whether that character is explicitly doing the action, or the action might happen: explicit-no, probable-no, hypothetical, probable, explicit |
| `situation` | text | said of the rule | `[rot-id, situation, text]` | text of the situation |
| `situation-short-id` | an id | said of the rule | `[rot-id, situation-short-id, value]` | unique id for the situation |
| `n-characters` | a number | said of the rule | `[rot-id, n-characters, value]` | how many characters were identified in the story during the character-identification task |
| `characters` | parts joined by `\|` | each part said of the rule under the column's name | `[rot-id, characters, narrator]` | '"\|" separated list' of the characters that appeared |

Nothing else is attested. The README is ordinary text, observed as [Attestations](../Semantics/Attestations.md#observations) says of ordinary content.
