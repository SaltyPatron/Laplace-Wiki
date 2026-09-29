# HateCheck

HateCheck attests labels on constructed hate-speech tests, and SGHateCheck is that test extended to Malay, Mandarin, Singlish, and Tamil.

The composition is a constructed test case. The mask is the label. The value is the label ten annotators gave the case. Witness HateCheck, deviation 90, the recipe's choice. SGHateCheck is the same kind of test for Malay, Mandarin, Singlish, and Tamil: templates, placeholders, a sample of annotations, and language-model readings, read after HateCheck. `code/` and the PNG files are excluded. Both live in the refresh `Safety` tree. Neither has a live directory.

The cases are built to probe a behavior. They are not a treebank and not a wordnet. A label on a constructed sentence does not attest the sense of a word inside it. The language of an SGHateCheck section hops to [ISO 639](ISO-639.md). Fanout is the number of annotators on a case. A language-model reading shipped in SGHateCheck is a model's output, lineage of that model, not a second annotator.

## Files, breakdown, and caveats

Taken from the recipe files. A line in a block is a directive. The prose above it is that file's own account of what is read, what is not, and what a row becomes.

### `hatecheck/annotations.recipe`

HateCheck's README, of "test_suite_annotations.csv" and "all_annotations.csv":   label_[1:10] "The label provided for the test case by a given annotator. We recruited and trained a team of ten   annotators. Each test case was annotated by exactly five annotators."   count_label_h "The number of annotators who labeled a given test case as hateful."   count_label_nh, likewise   label_annot_maj "The majority label." Each of the ten columns is an annotator, and its field what that annotator says of the case: nothing is written between the case and the label. The other columns are said of the case by the set, under their own names.

```text
match all_annotations.csv test_suite_annotations.csv
grammar table
separator ,
header
quoted
kinds own
kind case_id case_id
kind templ_id templ_id
claims
subject in case_id
attest functionality templ_id test_case label_gold count_label_h count_label_nh label_annot_maj
voices label_1 label_2 label_3 label_4 label_5 label_6 label_7 label_8 label_9 label_10
```

### `hatecheck/cases.recipe`

HateCheck's README names every column of "test_suite_cases.csv" and "all_cases.csv":   case_id "The unique ID of the test case"; test_case "The text of the test case."; label_gold "The gold standard   label (hateful/non-hateful) of the test case"; ref_case_id "the ID of the simpler hateful case which was   perturbed to generate them", or "of the hateful case which is contrasted"; ref_templ_id "The equivalent, but for   template IDs."; templ_id "The unique ID of the template from which the test case was generated" Every column is said of the case, under the column's own name. The first column has no name and says nothing.

```text
match all_cases.csv test_suite_cases.csv
grammar table
separator ,
header
quoted
kinds own
kind case_id case_id
kind ref_case_id case_id
kind templ_id templ_id
kind ref_templ_id templ_id
claims
together
subject in case_id
attest *
```

### `hatecheck/placeholders.recipe`

HateCheck's README: "template_placeholders.csv" contains the tokens that the placeholders in the case templates are replaced with for generating the test cases. Two columns, Placeholder and Values; a field of Values holds several, parted by commas.

```text
match template_placeholders.csv
grammar table
separator ,
header
quoted
claims
subject in Placeholder
attest Values
```

### `hatecheck/source`

The data of the paper "HateCheck: Functional Tests for Hate Speech Detection Models": test cases, and the labels ten annotators gave them. The README names it by that title. The deviation is this recipe's choice for a curated academic resource; the specification does not give one.

```text
witness HateCheck
deviation 90
root $LAPLACE_DATA/.refresh-*/Safety/HateCheck/extracted/hatecheck-*
reads text
```

### `sghatecheck/annotations.recipe`

The README, "/annotations": "This folder contains annotations of selected test cases", and "Human annotation of test cases": "up to three bilingual annotators annotated the test cases as hateful if it has harmful language directed at a protected group. Other annotation choices are non-hateful and nonsensical". The columns' names are the files' own: c_id, annotator_1, annotator_2, annotator_3, p_label, p_value, p_target, c_testcase, t_case_local, t_function, t_gold, t_direction, t_id, c_order, annotation_common, annotation_selected. Each annotator column is an annotator of that file's language, and its field what that annotator says of the test case; nothing is written between the two. The rest is said of the test case by the set.

```text
match annotations/*_annotations.csv
grammar table
separator ,
header
quoted
voices within-file
claims
subject in c_testcase
attest c_id p_label p_value p_target t_case_local t_function t_gold t_direction t_id c_order annotation_common annotation_selected
voices annotator_*
```

### `sghatecheck/source`

SGHateCheck: functional tests for hate speech detection in Malay, Mandarin, Singlish and Tamil: test cases made of templates and placeholders, annotations of a sample of them, and language models' readings of them. The README's title: "SGHateCheck: Functional Tests for Detecting Hate Speech in Low-Resource Languages of Singapore". The deviation is this recipe's choice for a curated academic resource; the specification does not give one.

```text
witness SGHateCheck
deviation 90
root $LAPLACE_DATA/.refresh-*/Safety/SGHateCheck/extracted/sghatecheck-*
except */code/* *.png
reads text
```

### `sghatecheck/testcases.recipe`

The README, "/testcases": "This folder contains test cases that were generated using the techniques described in the paper." It does not describe the columns; their names are the files' own, in the first row:   p_label, p_value, p_target, c_testcase, t_case_local, t_function, t_gold, t_direction, t_id A test case has no name of its own here: it is the text it is (c_testcase). A column without a name says nothing.

```text
match testcases/*_testcases_all.csv
grammar table
separator ,
header
quoted
claims
together
subject in c_testcase
attest *
```
