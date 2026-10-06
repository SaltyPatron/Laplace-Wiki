# Social Bias Frames

Social Bias Frames attests what each MTurk worker answered of a post, what the set says of the post and of the worker, and the same aggregated per post, where the first, unnamed column attests nothing.

The source is "the data splits from v2 of Social Bias Frames / Social Bias Inference Corpus": posts, what MTurk workers said of each, and the same aggregated per post. Two recipes read it: the annotations, one line per worker per post, and the aggregation, one line per post.

## Source

| Source | Witness | Trust class | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `social-bias-frames` | `Social Bias Frames`; as built, in the annotations each worker is also a witness of their own, `[Social Bias Frames, WorkerId, value]` (`own WorkerId`) | class `AcademicCurated` | `unicode`, `iso-639` | `SBIC.v2.trn.csv`, `SBIC.v2.dev.csv`, `SBIC.v2.tst.csv`; `SBIC.v2.agg.*.csv` | [`annotations.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/social-bias-frames/annotations.recipe), [`aggregated.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/social-bias-frames/aggregated.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior is the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

Every file is a table of comma-separated fields whose first row names the columns, and a field may stand between double quotes, where it may hold a comma or a line's end, and a quote in it is written twice. An empty field attests nothing. The quotations are the set's README's, "Each line in the file contains the following fields (in order)".

## The annotations

`SBIC.v2.trn.csv`, `SBIC.v2.dev.csv`, `SBIC.v2.tst.csv`. A line is one worker's reading of one post. The post is its text; its `HITId` is the crowdsourcing task's pointer to it, recorded nowhere (`key row HITId`). The worker is named as the set names them, the path `[Social Bias Frames, WorkerId, value]`, "post" and "worker" below. What the worker answered of the post, Social Bias Frames reports of the worker: the worker is content, never a witness, and that this worker gave this answer of this post is a relation of the worker and the post that Social Bias Frames attests, added to the web explicitly. As built, those claims are witnessed by the worker, a witness of their own (`own WorkerId`), which is what "by the worker" means in the rows below; the target is the set's relation. What the line holds of the worker is said of the worker, and the post's text and source are said of the post, both by Social Bias Frames. Each claim is its own attestation.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| `HITId` | the crowdsourcing task's pointer to the post: recorded nowhere | nothing | "id that uniquely identifies each post" |
| `WorkerId` | the worker, content: the subject of what is said of the worker, and a part of each relation of an answer; as built, also the witness of the worker's answers | `[Social Bias Frames, WorkerId, value]` | "hashed version of the MTurk workerId" |
| `post` | the subject: the post, as the text it is | | "post that was annotated" |
| `dataSource` | said of the post, by Social Bias Frames | `[post, dataSource, value]` | "source of the post" |
| `whoTarget` | said of the post, by the worker | `[post, whoTarget, value]` | "group vs. individual target" |
| `intentYN` | said of the post, by the worker | `[post, intentYN, value]` | "was the intent behind the statement to offend" |
| `sexYN` | said of the post, by the worker | `[post, sexYN, value]` | "is the post a sexual or lewd reference" |
| `sexReason` | said of the post, by the worker | `[post, sexReason, text]` | "free text explanations of what is sexual" |
| `offensiveYN` | said of the post, by the worker | `[post, offensiveYN, value]` | "could the post be offensive to anyone" |
| `sexPhrase` | said of the post, by the worker | `[post, sexPhrase, text]` | "part of the post that references something sexual" |
| `speakerMinorityYN` | said of the post, by the worker | `[post, speakerMinorityYN, value]` | "whether the speaker was part of the same minority group that's being targeted" |
| `targetMinority` | said of the post, by the worker | `[post, targetMinority, value]` | "demographic group targeted" |
| `targetCategory` | said of the post, by the worker | `[post, targetCategory, value]` | "high-level category of the demographic group(s) targeted" |
| `targetStereotype` | said of the post, by the worker | `[post, targetStereotype, text]` | "implied statement" |
| `annotatorGender`, `annotatorMinority`, `annotatorPolitics`, `annotatorRace`, `annotatorAge` | said of the worker, by Social Bias Frames | `[worker, annotatorGender, value]` | of the MTurk worker |

## The aggregation

`SBIC.v2.agg.*.csv`, the files "aggregated per post": for a post, the mean of `whoTarget`, `intentYN`, `sexYN`, and `offensiveYN` over its annotations, and the set of what was written as `targetMinority`, `targetCategory`, and `targetStereotype`, each written as a JSON list ("To load the list of implications, use json.loads"). A post has no `HITId` here: it is the text it is. Every named column is said of the post under the column's own name, together: one record per row, witnessed once by Social Bias Frames, and its claims within it.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `post` | the text | the subject: the post, as the text it is | | |
| `targetMinority`, `targetCategory`, `targetStereotype` | a JSON list of texts, `["a", "b"]` | each text said of the post under the column's name | `[post, targetStereotype, text]` | "To load the list of implications, use json.loads" |
| `whoTarget`, `intentYN`, `sexYN`, `offensiveYN` | a number | said of the post under the column's name, the number as written | `[post, offensiveYN, value]` | the mean over the post's annotations |
| `dataSource` | as in the annotations | said of the post | `[post, dataSource, value]` | |
| `hasBiasedImplication` | `0` or `1` | said of the post | `[post, hasBiasedImplication, value]` | the README computes it: `gDf["hasBiasedImplication"] = (gDf["targetStereotype"].apply(len) == 0).astype(int)` |
| the first column, which has no name | a number | nothing | none | |

Nothing else is attested. The README is not read: no recipe of the source matches it, and the source does not read text (`reads`), so nothing of it is recorded.

## Relations

As built, the relation of every claim above is the column's name, `[post, offensiveYN, value]`, `[worker, annotatorGender, value]`: markup, not meaning. A relation is what the source means, never the name of a field, column, attribute, or layer, [10. Recipes](../Sequence/Recipes.md#1011-disposition-every-recovered-field). The target for each column is what the source documents it to mean, quoted in the Specification column; a column whose meaning the source does not document is an explicit unresolved obligation, its target the meaning the source documents. `offensiveYN` is the worker's answer to "could the post be offensive to anyone", `targetStereotype` the "implied statement", and in the aggregation each number is the mean over the post's annotations; `hasBiasedImplication` is a calculation the README gives.
