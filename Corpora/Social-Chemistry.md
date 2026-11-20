# Social Chemistry

Social-Chem-101 attests rules of thumb over everyday situations together with scored moral-judgment (`-2..+2`), cultural-pressure (`-2..+2`), agreement (`0..4`), legality, moral-foundation, and resolved character-targeting breakdowns feeding the `RISK` and `consensus` planes, while filtering or downweighting rows flagged `rot-bad = 1`.

The source is the Social-Chem-101 Dataset (Forbes et al. 2020): 292k rules of thumb (`rot`) written over real-life situations and decomposed into structured moral, normative, legal, and agency attributes. [`breakdowns.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/social-chemistry-101/breakdowns.recipe) reads `social-chem-101.v1.0.tsv` under one corpus witness trunk.

## Source

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `social-chemistry-101` | `Social-Chem-101 Dataset` source trunk | class `AcademicCurated` | `unicode`, `iso-639` | `social-chem-101.v1.0.tsv` | [`breakdowns.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/social-chemistry-101/breakdowns.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior bounds the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## The breakdowns

Each tab-separated row (with RFC-style doubled quotes) is one breakdown worker's structured analysis of one rule of thumb (`rot`) written for one `situation`. `rot-id` and `situation-short-id` are internal pointers resolved at ingest and recorded nowhere (`key row rot-id`, `key row situation-short-id`). `rot-worker-id` and `breakdown-worker-id` are participant identifiers recorded beside their respective assertions (`with rot-worker-id`, `with breakdown-worker-id`), with `Social-Chem-101 Dataset` as the sole witness trunk ([30. Conflicts](../Sequence/Conflicts.md) I3). An empty cell means the question was left unanswered and attests nothing.

Three Recording Law requirements govern this table:

- **Scored moral and normative judgments (`INVENTOR_RECORD.md:211`, `:351`)**: `action-moral-judgment` (`-2` very bad through `+2` very good), `action-pressure` (`-2` strong pressure against through `+2` strong pressure for), `rot-agree` (`0..4` agreement buckets), and `action-agree` (`0..4` agreement buckets) supply **scored moral/normative/risk attestations** on `action` and `rot` feeding the `RISK` and `consensus` planes (`BELIEF ≠ RISK ≠ ACTION`), never blind `WIN` string literals or dropped row quantities.
- **Quality gate on `rot-bad`**: `rot-bad = 1` marks rows where the breakdown worker flagged the rule of thumb as *"confusing, extremely vague, very low quality, or couldn't be split into action and judgment"*. Under the Recording Law, `rot-bad = 1` **filters out or downweights** those low-quality breakdown claims rather than being ignored as bookkeeping (`Batch 2` recipe gap: `breakdowns.recipe` currently `omit`s `rot-bad` without filtering `rot-bad = 1` rows).
- **Row-local character pointer resolution**: `rot-char-targeting` and `action-char-involved` encode 0-based indices (`char-0`, `char-1`, ...) into the row's `|`-separated `characters` list, or `char-none`. `breakdowns.recipe` resolves `char-N` directly to the actual character entity in `characters` (`index ... in characters matching ^char-([0-9]+)$`) and maps `char-none` onto explicit absence (`"no one listed"`), never recording raw `"char-0"` pointer strings.

Specification descriptions below follow `README.v1.0.md` ("Dataset Columns").

| Piece | Written as | Laplace reads it as | Target attestation & current recipe state | Specification |
| --- | --- | --- | --- | --- |
| `rot-id`, `situation-short-id` | opaque IDs | internal pointers (`key row ...`), recorded nowhere | none | rule-of-thumb ID and unique situation ID |
| `rot` | text | the subject: the rule of thumb, as decoded UTF-8 text (`thing row rot`) | canonical rule-of-thumb entity | the rule of thumb written by the worker |
| `situation` | text | the situation text | `[rot, RoTs per situation, situation]` qualified `with rot-worker-id` | text of the situation |
| `rot-worker-id`, `breakdown-worker-id` | worker IDs | participant content qualifying authorship and breakdown judgments | `with rot-worker-id` / `with breakdown-worker-id` | author of the RoT and worker who performed the breakdown |
| `rot-bad` | `0` or `1` | quality-control filter/downweight gate (`rot-bad = 1` suppresses or downweights noisy/unsplittable RoTs) | quality gate (`Batch 2` gap: `breakdowns.recipe` currently `omit`s `rot-bad` instead of filtering `when rot-bad is 0`) | `1` when worker labeled the RoT confusing, vague, very low quality, or unsplittable |
| `area` | domain name | origin domain of the situation | `[rot, domain, area]` | `confessions`, `dearabby`, `rocstories`, `amitheasshole` |
| `characters` | `\|`-separated list | characters appearing in `situation` (`part characters by \|`) | `[rot, characters that appeared, character]` | list of characters identified in the story |
| `rot-char-targeting` | `char-none` or `char-N` | 0-based pointer resolved into `characters` (`index ... in characters`), or `"no one listed"` | `[rot, Who is the RoT most likely targeting, character]` qualified `with breakdown-worker-id` | who the RoT is most likely targeting |
| `action-char-involved` | `char-none` or `char-N` | 0-based pointer resolved into `characters`, or `"no one listed"` | `[rot, who is most likely to do the action or its opposite, character]` qualified `with breakdown-worker-id` | character doing the action or its opposite |
| `rot-categorization` | `\|`-separated list | normative category labels (`morality-ethics`, `social-norms`, `advice`, `description`) | `[rot, category]` (`value -`) qualified `with breakdown-worker-id` | 0 to 4 RoT categorizations |
| `rot-moral-foundations` | `\|`-separated list | Moral Foundations axes (`care-harm`, `fairness-cheating`, `loyalty-betrayal`, `authority-subversion`, `sanctity-degradation`) | `[rot, axis]` (`value -`) qualified `with breakdown-worker-id` | 0 to 5 moral-foundation axes |
| `action`, `rot-judgment` | text | extracted action phrase and judgment phrase | `[rot, The action (conjugated / tweaked substring of RoT), action]`, `[rot, the judgment portion of the RoT, rot-judgment]` | action and judgment substrings of `rot` |
| `action-moral-judgment` | `-2` to `2` | moral valence scale (`-2` very bad, `-1` bad, `0` expected/OK, `+1` good, `+2` very good) | target: scored moral/harm attestation on `action` and `rot` (`[-2, +2]` → `[0, 1]` / `RISK` plane, modulated by `action-agree`; `Batch 2` gap: currently uncalibrated string value on `rot`) | moral judgment bucket of `action` |
| `action-pressure`, `rot-agree`, `action-agree` | `-2..2` and `0..4` | cultural pressure scale and consensus-agreement buckets | target: scored normative-pressure attestation and series confidence weights (`Batch 2` gap: `breakdowns.recipe` currently leaves `rot-agree`, `action-agree`, and `action-pressure` unattested in the row) | cultural pressure against/for `action`; estimated population agreement |
| `action-agency`, `action-legal`, `action-hypothetical` | controlled labels | agency (`agency`/`experience`), legality (`legal`/`illegal`/`tolerated`), and eventuality (`explicit-no`..`explicit`) | attested on `rot`/`action` (`value -`) qualified `with breakdown-worker-id` | agency, legality (`illegal` also informs `RISK`), and hypotheticality |
| `split`, `m`, `n-characters` | split name, counts | dataset packaging bookkeeping (`omit`) | none | split assignment, worker count, and character-list length |

## Relations

`breakdowns.recipe` already resolves `char-0`/`char-1` indices into `characters`, handles `char-none`, keeps workers as participant qualifiers under one `Social-Chem-101 Dataset` trunk, and maps categorical columns onto README-defined relations. Closing the `Batch 2` gap adds the `rot-bad = 0` quality filter/downweight and maps `action-moral-judgment` (`-2..+2`), `action-pressure` (`-2..+2`), `rot-agree` (`0..4`), and `action-agree` (`0..4`) onto scored `RISK` and normative standing attestations.
