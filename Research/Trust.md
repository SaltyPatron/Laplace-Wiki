# Trust

Research and measurements on how much a witness's attestation should count and how hard each kind of word or relation should pull, measured on the local witnesses, on 88 languages of Universal Dependencies, and on word sense disambiguation.

Numbers marked measured come from prototype scripts on local data; numbers marked simulated come from a simulation; everything else is from the sources.

## Source trust

### Signed trust and the optimal weight

For independent binary witnesses with known accuracy *p*, the rule that minimizes error weighs each vote by log(*p* / (1 − *p*)) (Nitzan and Paroush, restated by [Berend and Kontorovich](https://arxiv.org/abs/1312.0451)). With *t* = 2*p* − 1:

- *t* = 1: always right. The weight is unbounded.
- *t* = 0: right half the time, a coin flip. The weight is 0: the witness carries no information.
- *t* < 0: right less than half the time. The weight is negative: its answers carry information once flipped.

Being reliably wrong is informative; being randomly wrong is not. The same signed scale appears in truth discovery, where trust −1 means "systematically wrong" and 0 means "random statements" ([Galland et al. 2010](http://pierre.senellart.com/publications/galland2010corroborating.pdf)), and in crowdsourcing, where malicious annotators get negative weights ([Raykar and Yu 2012](https://jmlr.org/papers/volume13/raykar12a/raykar12a.pdf); [Karger, Oh, and Shah](https://arxiv.org/abs/1110.3564)).

Negative trust needs an anchor. Without facts known to be true, "every witness is right" and "every witness is lying" explain agreement equally well; published methods break the tie by assumption. A tier of verified facts, such as mathematical results and verifiers, breaks it with evidence. Small amounts of known truth calibrate trust well: [semi-supervised truth discovery](https://www.microsoft.com/en-us/research/wp-content/uploads/2011/03/fr743-yin.pdf) reached 81% accuracy with 1% of the ground truth against 83% with all of it.

### Trust as a Glicko-2 opponent

Glicko-2 weighs every matchup by g(φ) = 1 / √(1 + 3φ² / π²), where φ is the opponent's deviation. [Glickman (1999)](http://www.glicko.net/research/glicko.pdf) derives g as the flattening of the win-probability curve caused by uncertainty in the opponent's strength. Setting g(φ) = |*t*| turns trust into the deviation a witness plays with, φ = (π / √3) · √(1/*t*² − 1):

| Trust *t* | Deviation (rating scale) | Information per attestation (*t*²) |
| --- | --- | --- |
| 1.0 | 0 | 1.00 |
| 0.9 | 153 | 0.81 |
| 0.67 | 349 | 0.45 |
| 0.5 | 546 | 0.25 |
| 0.3 | 1,002 | 0.09 |
| 0.1 | 3,135 | 0.01 |
| 0.05 | 6,294 | 0.0025 |

- The step a matchup makes scales with *t*; the information it adds scales with *t*². Ten attestations at trust 0.3 carry 0.9 units of information, less than one attestation at trust 1.0.
- Glicko-2's default deviation for an unrated player, 350, corresponds to trust 0.67.
- A signed g equal to a negative *t* gives exactly the same update as flipping the outcome at weight |*t*|.
- Glickman validated the approximation with opponent deviations around 50; very low trust means very large deviations, outside that tested range.
- Elo, Glicko, and TrueSkill are all simplified Kalman filters ([Szczecinski and Tihon 2021](https://arxiv.org/abs/2104.14012)), in which a noisier observation moves the estimate less; trust sets that noise.

Simulated, with 4,000 claims per row, each witness attesting each claim with the accuracy shown:

| Witnesses | Every witness weighted alike | Signed trust | Signed trust without lineage |
| --- | --- | --- | --- |
| Three honest witnesses (*p* = 0.9, 0.75, 0.6) | 85.1% | 89.8% | 89.8% |
| … plus four coin-flippers (*p* = 0.5) | 73.0% | 90.0% | 90.0% |
| … plus one reliably wrong witness (*p* = 0.2) | 55.2% | 91.4% | 91.4% |
| … plus a weak witness (*p* = 0.55) copied six times | 70.3% | 88.5% | 84.4% |

With signed trust the coin-flippers change nothing, the reliably wrong witness improves the consensus, and lineage keeps copies from counting as independent agreement. A verified anchor settling 10% of the claims raised accuracy from 91.7% to 92.4%, and settling 50% raised it to 96.0%.

### Truths cluster

Measured on Open Multilingual Wordnet: for 16 languages with an expert-built wordnet, that wordnet served as the reference for its language, and every lexicalization from the Wiktionary-derived and CLDR-derived wordnets was checked against it on the concepts the reference covers.

| Witness | Lexicalizations checked | In the reference | Earned trust 2*p* − 1 |
| --- | --- | --- | --- |
| Wiktionary-derived | 157,864 | 76.0% | 0.52 |
| CLDR-derived | 4,592 | 68.9% | 0.38 |
| ItalWordNet, against MultiWordNet (both expert-built) | 18,774 | 63.8% | 0.28 |

| Independent derived witnesses asserting the lexicalization | Lexicalizations | In the reference |
| --- | --- | --- |
| One | 157,764 | 75.4% |
| Two | 2,346 | 89.6% |

- Agreement between independent witnesses raised precision in every language measured: Finnish from 67.5% to 93.0%, Italian from 77.2% to 97.9%, Greek from 58.3% to 95.5%, Dutch from 77.1% to 96.8%.
- Lexicalizations found in the reference were agreed on by both witnesses 1.7% of the time; lexicalizations not found there, 0.6%. Right answers agree; wrong ones scatter.
- A reference is incomplete, so these precisions are lower bounds: Italy's two expert wordnets share only 64% of their lemmas, and 85% of the Wiktionary-derived Italian lexicalizations appear in at least one of them.
- Form matters: the expert Arabic wordnet writes lemmas with diacritics and Wiktionary without, so 18.6% match exactly and 63.4% match either form. The two spellings are different content, linked only by a claim.
- Lineage matters: a reference built partly from the same kind of source as the witness it judges agrees with it for that reason. Portuguese agrees at 98.8%, which may reflect shared construction rather than accuracy (not verified).

### Self-generated data

- Training a model only on its own outputs loses the rare cases first ([Shumailov et al. 2024](https://www.nature.com/articles/s41586-024-07566-y)); keeping 10% of the original data left only minor degradation.
- Keeping the real data and adding to it keeps error bounded; replacing it makes error grow with every generation ([Gerstgrasser et al. 2024](https://arxiv.org/abs/2404.01413)).
- With a perfect verifier, generated data helps at any error rate below 100%; with no verifier, only below 50%. A model judging its own outputs chose correctly 19.2% of the time, against 60.4% for an oracle choosing among the same 50 candidates ([Feng et al. 2024](https://arxiv.org/abs/2406.07515)).
- Generated reasoning kept only when its answer checked out raised accuracy from 60.0% to 72.5% ([STaR](https://arxiv.org/abs/2203.14465)).

## Role trust

### Information by part of speech and relation

Measured on Universal Dependencies v2.17: the 88 languages with at least 20,000 tokens, 37.4 million tokens in all. Each language's sentences were split in half by parity, counts came from one half and were scored on the other, each language's values were divided by its largest, and the languages were averaged.

| UPOS | Information of the word | UPOS | Information of the word |
| --- | --- | --- | --- |
| PROPN | 0.93 | ADV | 0.74 |
| ADJ | 0.88 | SCONJ, PART | 0.56 |
| NOUN | 0.87 | PRON | 0.54 |
| NUM | 0.85 | ADP | 0.53 |
| INTJ | 0.85 | DET | 0.52 |
| VERB | 0.79 | AUX | 0.48 |
| | | CCONJ | 0.47 |
| | | PUNCT | 0.38 |

How much a dependent tells about its head, as held-out information gain:

| Deprel | Information about the head | Deprel | Information about the head |
| --- | --- | --- | --- |
| fixed | 0.91 | nsubj | 0.09 |
| flat | 0.64 | det | 0.10 |
| compound | 0.57 | advmod | 0.05 |
| iobj | 0.29 | case | 0.04 |
| nummod | 0.27 | punct | 0.02 |
| obj | 0.24 | cop | 0.02 |
| amod | 0.26 | cc | 0.01 |

In the other direction, from head to dependent, function words score high (`fixed` 0.90, `det` 0.46, `aux` 0.50), because their heads predict them, not because they carry meaning.

In the literature, part-of-speech weights improve retrieval beyond frequency alone, with gains of up to 16.6% in mean average precision on news collections, and those weights are nearly uncorrelated with inverse document frequency ([Lioma and Blanco 2009](https://arxiv.org/abs/1704.01617)). Frequency-based weighting such as a / (a + *p*(*w*)) ([Arora et al. 2017](https://openreview.net/forum?id=SyK00v5xx)) crushes `not`, whose weight has to be kept.

### Role trust in word sense disambiguation

Measured with the evaluation framework used on [Semantics Experiments](Semantics-Experiments.md#word-sense-disambiguation). Each candidate sense's record set is:

- the words of its Open English WordNet definitions and examples;
- its synset members;
- the members of its one-hop relation neighbors;
- SemCor's co-occurrence observations.

The sentence's context is intersected with that record set. Every shared record is weighted by the role trust of the context word, by its informativeness from Gutenberg container counts, and by its strand, and is added to the candidate's log prevalence.

- The part of speech, dependency relation, and syntactic link of every word came from a UD parse of SemCor and the test sets by [Stanza](https://stanfordnlp.github.io/stanza/), an outside witness. It parsed 72 sentences per second on a GTX 1080 Ti, and 7 per second on six CPU threads.
- Weights were fitted by coordinate ascent on SemCor, split by document: prevalence and co-occurrence came from the even documents, and accuracy was measured on 36,410 instances from the odd ones.
- The four test sets were then scored once, with prevalence from WordNet's counts and co-occurrence from all of SemCor.

| Role trust | SemCor, held-out documents | Four test sets (6,613 instances) |
| --- | --- | --- |
| None: prevalence only | 64.0 | 64.6 |
| Knowledge only: definitions, members, relations, fitted | 64.5 | 64.7 |
| From the information per part of speech and relation above | 64.7 | 65.5 |
| Uniform | 64.5 | 65.6 |
| Drafted by hand | 64.8 | **66.2** |
| Fitted | **65.8** | **66.2** |

WordNet's first sense scores 65.2 on 6,574 of the same instances.

The fitted weights, each divided by the largest in its group:

| Context word | Fitted role trust |
| --- | --- |
| NOUN, ADJ, NUM | 1.0 |
| PROPN | 0.75 |
| VERB, ADV, ADP, PART | 0.5 |
| PRON, DET, CCONJ, PUNCT | 0.25 |
| SCONJ | 0.05 |
| AUX | 0 |

| Syntactic link to the target word | Fitted role trust |
| --- | --- |
| The target's head, or its dependent | 1.0 |
| Another dependent of the same head | 0.5 |
| Anywhere else in the sentence | 0.25 |

- Function words pull a quarter as hard as content words, or not at all. Words attached to the target pull four times as hard as words elsewhere in the sentence.
- With part of speech and link in place, per-relation and per-lexname weights scattered around their starting value and did not improve held-out accuracy.
- Nearly all of the gain came from SemCor's co-occurrence observations. Definitions, members, and relations alone added 0.1.
- Raw overlaps had to be normalized by the size of each record set, as cosine similarity normalizes a dot product. Unnormalized, a sense with more records shared something with every sentence: definition overlap at a weight of 0.001 lowered accuracy by 1.3 points. Co-occurrence had to count against a sense as well as for it, for every context word, rather than only for shared words.

## Sources

- Daniel Berend and Aryeh Kontorovich. [Consistency of weighted majority votes](https://arxiv.org/abs/1312.0451). NIPS 2014. Restates Shmuel Nitzan and Jacob Paroush, "Optimal decision rules in uncertain dichotomous choice situations", International Economic Review 23(2), 1982.
- Alban Galland, Serge Abiteboul, Amélie Marian, and Pierre Senellart. [Corroborating information from disagreeing views](http://pierre.senellart.com/publications/galland2010corroborating.pdf). WSDM 2010.
- Vikas C. Raykar and Shipeng Yu. [Eliminating spammers and ranking annotators for crowdsourced labeling tasks](https://jmlr.org/papers/volume13/raykar12a/raykar12a.pdf). JMLR 13, 2012.
- David R. Karger, Sewoong Oh, and Devavrat Shah. [Budget-optimal task allocation for reliable crowdsourcing systems](https://arxiv.org/abs/1110.3564). Operations Research 62(1), 2014.
- Xiaoxin Yin and Wenzhao Tan. [Semi-supervised truth discovery](https://www.microsoft.com/en-us/research/wp-content/uploads/2011/03/fr743-yin.pdf). WWW 2011.
- Mark E. Glickman. [Parameter estimation in large dynamic paired comparison experiments](http://www.glicko.net/research/glicko.pdf). Applied Statistics 48, 1999.
- Leszek Szczecinski and Raphaëlle Tihon. [Simplified Kalman filter for online rating](https://arxiv.org/abs/2104.14012). 2021.
- Ilia Shumailov et al. [AI models collapse when trained on recursively generated data](https://www.nature.com/articles/s41586-024-07566-y). Nature 631, 2024.
- Matthias Gerstgrasser et al. [Is model collapse inevitable?](https://arxiv.org/abs/2404.01413) 2024.
- Yunzhen Feng et al. [Beyond model collapse: scaling up with synthesized data requires verification](https://arxiv.org/abs/2406.07515). 2024.
- Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah D. Goodman. [STaR: bootstrapping reasoning with reasoning](https://arxiv.org/abs/2203.14465). NeurIPS 2022.
- Christina Lioma and Roi Blanco. [Part of speech based term weighting for information retrieval](https://arxiv.org/abs/1704.01617). ECIR 2009.
- Sanjeev Arora, Yingyu Liang, and Tengyu Ma. [A simple but tough-to-beat baseline for sentence embeddings](https://openreview.net/forum?id=SyK00v5xx). ICLR 2017.
- Peng Qi, Yuhao Zhang, Yuhui Zhang, Jason Bolton, and Christopher D. Manning. [Stanza: a Python natural language processing toolkit for many human languages](https://aclanthology.org/2020.acl-demos.14/). ACL 2020.
- Local witnesses: Open Multilingual Wordnet, Universal Dependencies v2.17, SemCor, Open English WordNet 2025+, and the WSD evaluation framework of Raganato et al. (2017).
