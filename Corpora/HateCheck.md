# HateCheck

HateCheck and SGHateCheck attest functional hate-speech test cases, targeted protected groups, perturbation contrast links, and scored gold and per-annotator hate vs. non-hate risk verdicts across English, Malay, Mandarin, Singlish, and Tamil, each suite under one corpus witness trunk.

Two sources read the two suites in [`recipes/order`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/order): `hatecheck` ("HateCheck: Functional Tests for Hate Speech Detection Models") and `sghatecheck` ("SGHateCheck: Functional Tests for Detecting Hate Speech in Low-Resource Languages of Singapore"). Each suite is one source trunk and one witness; annotators named inside the CSV tables are participant content (`with {field}`), never separate witnesses ([30. Conflicts](../Sequence/Conflicts.md) I3).

## Sources

| Source | Witness | Trust class | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `hatecheck` | `HateCheck` source trunk | class `AcademicCurated` | `unicode`, `iso-639` | `all_cases.csv`, `test_suite_cases.csv`; `all_annotations.csv`, `test_suite_annotations.csv`; `template_placeholders.csv` | [`cases.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/hatecheck/cases.recipe), [`annotations.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/hatecheck/annotations.recipe), [`placeholders.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/hatecheck/placeholders.recipe) |
| `sghatecheck` | `SGHateCheck` source trunk | class `AcademicCurated` | `unicode`, `iso-639`, `hatecheck` | `testcases/*_testcases_all.csv`; `annotations/*_annotations.csv` | [`testcases.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/sghatecheck/testcases.recipe), [`annotations.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/sghatecheck/annotations.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior bounds the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

Every file is RFC 4180 quoted CSV with a header row; unnamed index columns and empty cells attest nothing. Under the Recording Law ([INVENTOR_RECORD](../Repositories/Laplace/docs/INVENTOR_RECORD.md)), `label_gold`, `label_annot_maj`, `label_1..10`, `t_gold`, and `annotator_1..3` (`hateful` vs. `non-hateful`) supply **scored harm/risk vs. benign contrast attestations** feeding the `RISK` and `consensus` planes (`BELIEF ≠ RISK ≠ ACTION`), teaching Laplace both genuine hate speech (`hateful`) and benign look-alikes such as reclaimed slurs, counter-speech, and neutral group mentions (`non-hateful`).

## The cases (`hatecheck`)

`test_suite_cases.csv` and `all_cases.csv`. A row's subject is `test_case`, the sentence itself (`thing row test_case`). `case_id`, `templ_id`, and `ref_templ_id` are internal pointers resolved at ingest and recorded nowhere (`key row ...`), while `ref_case_id` resolves via `refer ref_case_id hatecheck-cases` to the contrasted or perturbed sentence itself. Quotations are from the [HateCheck README](https://raw.githubusercontent.com/paul-rottger/hatecheck-data/main/README.md).

| Piece | Laplace reads it as | Target attestation & current recipe state | Specification |
| --- | --- | --- | --- |
| `case_id`, `templ_id`, `ref_templ_id` | internal pointers (`key row ...`), recorded nowhere | none | "The unique ID of the test case"; "The unique ID of the template" |
| `test_case` | the subject: the test case sentence | canonical sentence entity | "The text of the test case." |
| `functionality` | functional capability class tested | `[case, functionality_value]` (`value - functionality`) | "The shorthand for the functionality tested by the test case." |
| `label_gold` | gold hate/non-hate risk verdict (`hateful` / `non-hateful`) | target: scored harm/risk attestation (`hateful` negative/high-risk, `non-hateful` benign contrast) on the `RISK` / `consensus` plane (`cases.recipe` currently attests `value - label_gold` as a vocabulary label; scored risk polarity lands in `Batch 2`) | "The gold standard label (hateful/non-hateful) of the test case" |
| `target_ident` | protected group targeted or referenced | `[case, the protected group targeted or referenced by the test case, value]` | "Where applicable, the protected group targeted or referenced by the test case." |
| `direction` | individual vs. group-general direction label | `[case, direction_value]` (`value - direction`) | "whether they are directed at an individual as part of a protected group or aimed at the group in general." |
| `focus_words` | key word or phrase in the test case | `[case, the key word or phrase, value]` | "Where applicable, the key word or phrase in a given test case." |
| `focus_lemma` | lemma of the focus expression | `[case, the corresponding lemma, value]` | "Where applicable, the corresponding lemma." |
| `ref_case_id` | resolved sentence of the perturbed (`hateful`) or contrasted (`non-hateful`) base case | `[case, the simpler hateful case which was perturbed to generate them, base_sentence]` or `[case, the hateful case which is contrasted, base_sentence]` | "the ID of the simpler hateful case which was perturbed to generate them" / "contrasted" |
| `case_templ` | template pattern with `[IDENTITY]` / `[SLUR]` placeholders | `[case, case templates, value]` | template text paired with `template_placeholders.csv` |

## The annotations (`hatecheck`)

`test_suite_annotations.csv` and `all_annotations.csv`. Each of five assigned raters out of `label_1..label_10` labels `test_case`. `HateCheck` witnesses every judgment with the column's annotator identifier as participant content (`attest row label_1 ... label_10 with {field}`), while `count_label_h` and `count_label_nh` are redundant summaries of the ten columns (`omit count_label_h count_label_nh`).

| Piece | Laplace reads it as | Target attestation & current recipe state | Specification |
| --- | --- | --- | --- |
| `test_case` | the subject (`case_id` and `templ_id` resolved as keys) | canonical sentence entity | "The text of the test case." |
| `label_1` to `label_10` | annotator `N`'s hate/non-hate verdict on `test_case` | `[case, hateful/non-hateful]` qualified `with label_N`, feeding scored risk standing in `Batch 2` | "The label provided for the test case by a given annotator." |
| `label_annot_maj` | majority rater verdict | `[case, The majority label, hateful/non-hateful]` | "The majority label." |
| `count_label_h`, `count_label_nh` | derived counts of `label_1..10` (`omit`) | none (already represented by the individual rater series) | "The number of annotators who labeled a given test case as hateful / non-hateful." |

## The placeholders (`hatecheck`)

`template_placeholders.csv` maps each template token (`Placeholder`) to comma-separated replacement strings (`Values`), attesting `[placeholder, token]` substitutions used to instantiate functional cases.

## SGHateCheck (`sghatecheck`)

`testcases/*_testcases_all.csv` and `annotations/*_annotations.csv` extend the same functional contrast design to Malay (`ms`), Mandarin (`zh`), Singlish (`en`/`sg`), and Tamil (`ta`). `c_testcase` is the canonical sentence subject; local case/order numbers (`c_id`, `t_id`, `c_order`, `index`, `Unnamed:*`) are internal pointers/bookkeeping; `t_gold`, `t_function`, `t_direction`, `p_target`, `t_case_local`, and file-scoped `annotator_1..3` verdicts (`hateful`, `non-hateful`, `nonsensical`) attest multilingual hate/risk and benign-contrast judgments under the `SGHateCheck` witness trunk (`Batch 2` aligns SGHateCheck's undocumented `t_*`/`p_*` header names onto HateCheck's semantic relations and scored `RISK` polarity). Baseline classifier output dumps (`*/classified*`) and plotting scripts (`*/code/*`, `*.png`) are benchmark evaluation artifacts, not corpus ground truth.

## Relations

`hatecheck/cases.recipe` and `hatecheck/annotations.recipe` already replace raw CSV column headers (`target_ident`, `focus_words`, `ref_case_id`, `label_1..10`) with publisher-documented semantic relations and participant qualifiers under the single `HateCheck` witness trunk. In `Batch 2`, gold and rater `hateful` / `non-hateful` judgments map onto signed/scored `RISK` plane outcomes (`BELIEF ≠ RISK ≠ ACTION`) and `sghatecheck` columns unify onto the same semantic relation vocabulary.
