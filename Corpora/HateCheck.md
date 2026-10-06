# HateCheck

HateCheck attests what its gold standard and each of its ten annotators say of every test case, SGHateCheck attests the same of its test cases in Malay, Mandarin, Singlish, and Tamil with each annotator of each file a witness of its own, and the language models' readings of the SGHateCheck cases attest nothing.

Two sources read the two suites, in the order [`recipes/order`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/order) gives: `hatecheck`, then `sghatecheck`. Each is a witness of its own, and neither is lineage of the other. The sources name them by their papers' titles, "HateCheck: Functional Tests for Hate Speech Detection Models" and "SGHateCheck: Functional Tests for Detecting Hate Speech in Low-Resource Languages of Singapore".

## Sources

| Source | Witness | Trust class | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `hatecheck` | `HateCheck`; each of the columns `label_1` to `label_10` is a witness of its own, `[HateCheck, label_1]` | class `AcademicCurated` | `unicode`, `iso-639` | `all_cases.csv`, `test_suite_cases.csv`; `all_annotations.csv`, `test_suite_annotations.csv`; `template_placeholders.csv` | [`cases.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/hatecheck/cases.recipe), [`annotations.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/hatecheck/annotations.recipe), [`placeholders.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/hatecheck/placeholders.recipe) |
| `sghatecheck` | `SGHateCheck`; each `annotator_N` column of each annotation file is a witness of its own, `[SGHateCheck, ms_annotations, annotator_1]` | class `AcademicCurated` | `unicode`, `iso-639`, `hatecheck` | `testcases/*_testcases_all.csv`; `annotations/*_annotations.csv`; not `*/code/*` or `*.png` | [`testcases.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/sghatecheck/testcases.recipe), [`annotations.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/sghatecheck/annotations.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior is the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

Every file is a table of comma-separated fields whose first row names the columns. A field may stand between double quotes, where it may hold a comma or a line's end, and a quote in it is written twice. A column the first row gives no name says nothing, and an empty field attests nothing. Each claim is a tuple, as [Claims](../Semantics/Claims.md#tuples) defines it, every part as the file writes it.

## The cases

`test_suite_cases.csv` and `all_cases.csv`. A row is one test case, which is its `test_case`, the sentence itself; "case" below is that sentence. `case_id` and `templ_id` are HateCheck's internal pointers to the case and to the template it was made from, recorded nowhere (`key row case_id`, `key row templ_id`, `key row ref_templ_id`); `ref_case_id` points at another case by its pointer and is read as that case's sentence (`refer ref_case_id hatecheck-cases`). Every other named column is said of the case under the column's own name, and what a row says it says together: one record, witnessed once by HateCheck, and its claims within it. The quotations are the [HateCheck README](https://raw.githubusercontent.com/paul-rottger/hatecheck-data/main/README.md)'s.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| `case_id` | a pointer, recorded nowhere | nothing | "The unique ID of the test case" |
| `functionality` | said of the case | `[case, functionality, value]` | "The shorthand for the functionality tested by the test case." |
| `test_case` | the subject: the case, the sentence itself | | "The text of the test case." |
| `label_gold` | said of the case | `[case, label_gold, hateful]` | "The gold standard label (hateful/non-hateful) of the test case" |
| `target_ident` | said of the case | `[case, target_ident, value]` | "Where applicable, the protected group targeted or referenced by the test case." |
| `direction` | said of the case | `[case, direction, value]` | "For hateful cases, the binary secondary label indicating whether they are directed at an individual as part of a protected group or aimed at the group in general." |
| `focus_words` | said of the case | `[case, focus_words, value]` | "Where applicable, the key word or phrase in a given test case." |
| `focus_lemma` | said of the case | `[case, focus_lemma, value]` | "Where applicable, the corresponding lemma." |
| `ref_case_id` | said of the case: the case it points at, as that case's sentence | `[I have met many women and I hate every single one of them., ref_case_id, I hate women.]` | "the ID of the simpler hateful case which was perturbed to generate them", or "of the hateful case which is contrasted" |
| `ref_templ_id`, `templ_id` | pointers, recorded nowhere | nothing | "The unique ID of the template from which the test case was generated" |
| `case_templ` | said of the case under the column's name | `[case, case_templ, value]` | the README does not name it |
| the first column, which has no name | nothing | none | |

## The annotations

`test_suite_annotations.csv` and `all_annotations.csv`. A row is one case, `case_id`, with what the set says of it and what each of ten annotators said. The ten columns `label_1` to `label_10` are voices: each is a witness of its own, named `[HateCheck, label_1]`, and its field is what that annotator says of the case, with nothing written between the two, so the claim is a pair. What the set says, HateCheck says, each claim on its own.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| `test_case` | the subject: the case, its sentence; `case_id` and `templ_id` pointers, as in the cases file | | "The text of the test case." |
| `label_1` to `label_10` | what annotator N says of the case: a pair, witnessed by `[HateCheck, label_N]` | `[case, hateful]` | "The label provided for the test case by a given annotator. We recruited and trained a team of ten annotators. Each test case was annotated by exactly five annotators." |
| `functionality`, `label_gold` | said of the case by HateCheck, as in the cases file | `[I hate women., label_gold, hateful]` | as above |
| `count_label_h` | said of the case by HateCheck | `[case, count_label_h, value]` | "The number of annotators who labeled a given test case as hateful." |
| `count_label_nh` | said of the case by HateCheck | `[case, count_label_nh, value]` | the same, for non-hateful |
| `label_annot_maj` | said of the case by HateCheck | `[case, label_annot_maj, hateful]` | "The majority label." |
| the first column, which has no name | nothing | none | |

## The placeholders

`template_placeholders.csv` "contains the tokens that the placeholders in the case templates are replaced with for generating the test cases".

| Piece | Written as | Laplace reads it as | Claim recorded |
| --- | --- | --- | --- |
| `Placeholder` | the token as written in a template | the subject | |
| `Values` | several tokens, parted by commas | each token said of the placeholder under `Values`, each claim on its own | `[placeholder, Values, token]` |

## SGHateCheck's test cases

`testcases/*_testcases_all.csv`, one file per language. The README, "/testcases": "This folder contains test cases that were generated using the techniques described in the paper." It does not describe the columns. A test case has no name of its own here: it is the text it is, `c_testcase`, and every other named column is said of it under the column's own name, together: one record per row, witnessed once by SGHateCheck.

| Piece | Laplace reads it as | Claim recorded |
| --- | --- | --- |
| `c_testcase` | the subject: the test case, as the text it is | |
| `p_label`, `p_value`, `p_target`, `t_case_local`, `t_function`, `t_gold`, `t_direction`, `t_id` | said of the test case under the column's name | `[test case, t_gold, value]` |
| a column with no name | nothing | none |

## SGHateCheck's annotations

`annotations/*_annotations.csv`, one file per language. The README, "/annotations": "This folder contains annotations of selected test cases", and, of the annotation: "up to three bilingual annotators annotated the test cases as hateful if it has harmful language directed at a protected group. Other annotation choices are non-hateful and nonsensical". The subject is again the text, `c_testcase`. Each `annotator_N` column is a voice standing within its file: its witness is `[SGHateCheck, ms_annotations, annotator_1]`, the path of the source, the file's name, and the column's, so annotator 1 of the Malay file and annotator 1 of the Tamil file are two witnesses. The rest is said of the test case by SGHateCheck, each claim on its own.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| `c_testcase` | the subject: the test case, as the text it is | | |
| `annotator_1`, `annotator_2`, `annotator_3`, where the file has them | what that annotator says of the test case: a pair, witnessed by `[SGHateCheck, file, annotator_N]` | `[test case, hateful]` | "hateful", "non-hateful", "nonsensical" |
| `c_id`, `p_label`, `p_value`, `p_target`, `t_case_local`, `t_function`, `t_gold`, `t_direction`, `t_id`, `c_order`, `annotation_common`, `annotation_selected` | said of the test case under the column's name, by SGHateCheck | `[test case, t_gold, value]` | the README does not describe them |
| `c_group`, `index`, `Unnamed: 0`, `Unnamed: 0.1`, and a column with no name, where a file has them | not read: the recipe does not name them | none | |

Nothing else of either source is attested. The READMEs, the annotation guidelines, and SGHateCheck's files of what the language models answered of the cases (`classified`, `actual`, `case_id`; `output`, `actual_label`) are not read: no recipe of either source matches them, and neither source reads text (`reads`), so nothing of them is recorded. SGHateCheck's `code` directories and its images are not the source at all.
