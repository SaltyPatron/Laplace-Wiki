# Social Bias Frames

Social Bias Frames attests what workers said a post implied, both per annotation and aggregated per post.

## Files

| Path | Bytes | What the file is | Proof |
| --- | --- | --- | --- |
| /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/SBIC.v2.tgz | 9464583 | gzip archive. file(1) says it was SBIC.v2.tar. | file(1) on this machine. |
| /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/LICENSE | 18657 | Creative Commons Attribution 4.0 International license text. | First line of the file. |
| /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md | 2393 | v2 README. Defines the annotation fields in order and shows the aggregation code. | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/SBIC.v2.trn.csv | 27721458 | Train annotations, one worker's reading of one post per row. | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/SBIC.v2.dev.csv | 4162581 | Dev annotations, same header as the train file. | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/SBIC.v2.tst.csv | 4395701 | Test annotations, same header as the train file. | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/SBIC.v2.agg.trn.csv | 7559567 | Train posts aggregated as the README's aggregation code describes. | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/SBIC.v2.agg.dev.csv | 1079264 | Dev posts aggregated the same way. | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/SBIC.v2.agg.tst.csv | 1123118 | Test posts aggregated the same way. | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| /vault/Data/.refresh-20260903/.jobs/social-bias-frames-v2.log | 141 | Refresh log. First line: dataset-estate-refresh: social-bias-frames-v2 already staged and verified: /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/SBIC.v2.tgz | The file itself. |
| /vault/Data/.refresh-20260903/.jobs/social-bias-frames-v2.pid | 8 | Refresh pid file. Contents: 3973639 | The file itself. |
| /vault/Data/.refresh-20260903/.jobs/social-bias-frames-v2.rc | 2 | Refresh exit file. Contents: 0 | The file itself. |

## Attestations

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| whoTarget | group vs. individual target | the post | the field as written on the annotation row | the MTurk worker | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| intentYN | was the intent behind the statement to offend | the post | the field as written on the annotation row | the MTurk worker | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| sexYN | is the post a sexual or lewd reference | the post | the field as written on the annotation row | the MTurk worker | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| sexReason | free text explanations of what is sexual | the post | the field as written on the annotation row | the MTurk worker | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| offensiveYN | could the post be offensive to anyone | the post | the field as written on the annotation row | the MTurk worker | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| annotatorGender | gender of the MTurk worker | the MTurk worker | the field as written on the annotation row | the MTurk worker | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| annotatorMinority | whether the MTurk worker identifies as a minority | the MTurk worker | the field as written on the annotation row | the MTurk worker | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| sexPhrase | part of the post that references something sexual | the post | the field as written on the annotation row | the MTurk worker | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| speakerMinorityYN | whether the speaker was part of the same minority group that's being targeted | the post | the field as written on the annotation row | the MTurk worker | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| WorkerId | hashed version of the MTurk workerId | the MTurk worker | the field as written on the annotation row | the MTurk worker | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| HITId | id that uniquely identifies each post | the post | the field as written on the annotation row | Social Bias Frames | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| annotatorPolitics | political leaning of the MTurk worker | the MTurk worker | the field as written on the annotation row | the MTurk worker | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| annotatorRace | race of the MTurk worker | the MTurk worker | the field as written on the annotation row | the MTurk worker | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| annotatorAge | age of the MTurk worker | the MTurk worker | the field as written on the annotation row | the MTurk worker | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| post | post that was annotated | the post | the field as written on the annotation row | the MTurk worker | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| targetMinority | demographic group targeted | the post | the field as written on the annotation row | the MTurk worker | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| targetCategory | high-level category of the demographic group(s) targeted | the post | the field as written on the annotation row | the MTurk worker | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| targetStereotype | implied statement | the post | the field as written on the annotation row | the MTurk worker | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| dataSource | source of the post (t/... means Twitter, r/... means a subreddit) | the post | the field as written on the annotation row | the MTurk worker | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| (blank) | Not defined. The aggregated files have an empty first header cell. | Not defined | empty header | Not defined | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| post (aggregated) | The post the annotations were grouped by. The README groups on post. | the post | the post text | derived from the annotation rows | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| targetMinority (aggregated) | Text field. The README aggregation takes the sorted set of non-empty values, then json.dumps. To load the list, use json.loads. | the post | a JSON list | derived from the annotation rows | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| targetCategory (aggregated) | Text field, aggregated the same way as targetMinority. | the post | a JSON list | derived from the annotation rows | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| targetStereotype (aggregated) | Text field, aggregated the same way as targetMinority. The README calls targetStereotype the implied statement. | the post | a JSON list | derived from the annotation rows | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| whoTarget (aggregated) | Class field. The README aggregation sets it to np.mean of the annotation values for that post. | the post | the mean | derived from the annotation rows | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| intentYN (aggregated) | Class field. The README aggregation sets it to np.mean of the annotation values for that post. | the post | the mean | derived from the annotation rows | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| sexYN (aggregated) | Class field. The README aggregation sets it to np.mean of the annotation values for that post. | the post | the mean | derived from the annotation rows | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| offensiveYN (aggregated) | Class field. The README aggregation sets it to np.mean of the annotation values for that post. | the post | the mean | derived from the annotation rows | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| dataSource (aggregated) | The column is in the aggregated files. The aggregation code block in the README does not define it. | Not defined | Not defined | Not defined | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| hasBiasedImplication | The README assigns gDf["hasBiasedImplication"] = (gDf["targetStereotype"].apply(len) == 0).astype(int), after targetStereotype has been reduced to a list and before json.dumps. | the post | 0 or 1 from that expression | derived from the annotation rows | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |

## Records

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| annotation | whoTarget, intentYN, sexYN, sexReason, offensiveYN, annotatorGender, annotatorMinority, sexPhrase, speakerMinorityYN, WorkerId, HITId, annotatorPolitics, annotatorRace, annotatorAge, post, targetMinority, targetCategory, targetStereotype, dataSource | One MTurk worker's annotation of one post. SBIC.v2.trn.csv, SBIC.v2.dev.csv, and SBIC.v2.tst.csv share this header. | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md. Headers read from the three files. |
| aggregated post | (blank), post, targetMinority, targetCategory, targetStereotype, whoTarget, intentYN, sexYN, offensiveYN, dataSource, hasBiasedImplication | One post, with the means and JSON lists the README aggregation builds. The same header is on the three agg files. | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md. Headers read from the three agg files. |

## Lineage

| Paths | What is shared | Proof |
| --- | --- | --- |
| SBIC.v2.agg.*.csv and SBIC.v2.{trn,dev,tst}.csv | The README says the aggregated files are compiled from the annotations by grouping on post. The aggregate is derived from those rows. | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| hasBiasedImplication and targetStereotype | The README code sets hasBiasedImplication from (targetStereotype list length == 0).astype(int). | /vault/Data/.refresh-20260903/Safety/SocialBiasFrames/extracted/README.md |
| annotations.recipe and aggregated.recipe | annotations.recipe matches SBIC.v2.trn.csv, SBIC.v2.dev.csv, and SBIC.v2.tst.csv. aggregated.recipe matches SBIC.v2.agg.*.csv. | [annotations.recipe](/repos/src/Laplace-Engine/recipes/social-bias-frames/annotations.recipe); [aggregated.recipe](/repos/src/Laplace-Engine/recipes/social-bias-frames/aggregated.recipe) |
