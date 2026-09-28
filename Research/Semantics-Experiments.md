# Semantics Experiments

First experiments with semantic records on the local curated corpora measured how identifiers link words, concepts, and languages, how annotation layers deduplicate as content, and how well a first pull disambiguates word senses.

Everything on this page was measured with prototype scripts on the local datasets unless it cites a source. These are first cuts, not tuned systems.

## Concepts across languages

`dog` has seven noun senses in WordNet 3.0. Each maps through CILI to an ILI, and Open Multilingual Wordnet lexicalizes each ILI in other languages, with each lexicalization attested by a named witness:

| Sense | ILI | Some lexicalizations, with their witness |
| --- | --- | --- |
| the animal | i46360 | `Hund` [Wiktionary], `chien` [WOLF, Wiktionary], `犬` [Japanese WordNet, Wiktionary], `perro` [MCR], `koira` [Wiktionary] |
| a dull unattractive woman | i90107 | `chien` [WOLF], `adefesio` [MCR] |
| a smooth-textured sausage | i77293 | `hot-dog` [WOLF], `salchicha` [MCR], `parówka` [Polish WordNet] |
| a hinged catch in a ratchet | i57068 | `Sperrklinke` [Wiktionary], `trinquete` [MCR] |

- Several witnesses agreeing (`chien`, `犬`, `cane`) is consensus; a single witness is weaker. WOLF lists `chien` for all seven senses, including the andiron and the ratchet catch, and no other witness corroborates those.
- The Italian wordnet marks one sense with an explicit lexical gap (`GAP!`): a witness stating that Italian has no word for it.
- German has `Hund` and `Hündin` under the same ILI; choosing between them needs a feature (sex), not a different concept.

## The identifier highway

PredicateMatrix 1.3 (426,696 rows) ties each predicate to VerbNet, FrameNet, PropBank, WordNet, and MCR identifiers. For the verb *bite*, joined to CILI:

| WordNet sense | ILI | VerbNet | FrameNet | PropBank | SUMO |
| --- | --- | --- | --- | --- | --- |
| bite%2:35:00 | i28957 | 18.2 | Taking | bite.01 | Touching |
| bite%2:35:02 | i28954 | 40.8.3 | Cause_harm | bite.01 | Injuring |

- The same rows carry Catalan `mossegar` and Spanish `morder`, `dar`, and `pegar` for the same identifiers.
- Roles align across systems: VerbNet Agent with PropBank Arg0, VerbNet Patient with PropBank Arg1.
- One row maps *bite* to FrameNet *Arriving*, an error that only one witness makes.

## Observation and attestation together

`Butler` and `butler` are different entities, 0.045 apart on the S³ (measured on the H1 placement). In the Gutenberg corpus `Butler` occurs 314 times in 293 containers and `butler` 40 times in 40. Wiktionary attests `Butler` as a surname whose etymology leads to *butler*, and attests *butler* as a noun ("a manservant having charge of wines and liquors") and a verb. WordNet attests *butler* as ILI i88758.

Filtering the fillers of the gap query `[Captain, ' ', ?]` in Moby Dick by their part-of-speech attestations from 29 English UD treebanks and Wiktionary separates the function words (`of`: ADP 17,239; `and`: CCONJ 19,568; `is`: AUX 9,441) from the names. Dropping the fillers attested as function words, verbs, pronouns, and adverbs leaves the nine captains: Ahab, Peleg, Bildad, Sleet, Pollard, Mayhew, Scoresby, Boomer, and Butler.

## Annotation layers as content

All 686 files of UD v2.17: 186 languages, 2,313,529 sentences, 37,877,213 tokens. Each sentence's layer sequences were hashed like compositions:

| Whole-sentence layer | Distinct | Share of sentences |
| --- | --- | --- |
| Sentence text | 2,091,778 | 90.4% |
| UPOS sequence | 1,776,263 | 76.8% |
| Dependency relations with head offsets | 1,815,592 | 78.5% |
| Both | 1,909,657 | 82.5% |

Whole-sentence layers rarely repeat, as whole sentences rarely do. Their sub-structures do. Every dependency subtree's layer, the (UPOS, dependency relation) sequence it covers:

| Subtree size | Subtrees | Distinct | Share that is new |
| --- | --- | --- | --- |
| 2 tokens | 3,906,541 | 16,959 | 0.4% |
| 3–4 | 3,657,279 | 282,079 | 7.7% |
| 5–8 | 2,969,380 | 1,586,380 | 53.4% |
| 9–16 | 2,232,348 | 2,121,458 | 95.0% |
| 17 or more | 1,637,435 | 1,619,767 | 98.9% |

One record per token per layer would be 75.8 million records for two layers; one claim per sentence per layer is 4.6 million, with per-token detail held as geometry vertices. Composed hierarchically, like text, layers share their small sub-structures almost entirely.

## Word sense disambiguation

The test uses the standard evaluation framework of [Raganato et al. (2017)](https://aclanthology.org/E17-1010.pdf): SemCor (226,036 sense-tagged instances) and five test sets. Every gold WordNet 3.0 sense key maps to an ILI through `index.sense` and CILI. Following common practice, SemEval-2007 was used for tuning and the other four sets, 6,798 instances, for scoring.

The pull scored each candidate sense as its prior, the attested sense frequency, plus the pull of the sentence's other words through WordNet's identifier hubs (hypernyms, supersense, definition words, synset members), discounting frequent hubs:

| Set | Instances | Prior only | Prior + pull |
| --- | --- | --- | --- |
| Senseval-2 | 2,282 | 65.5 | 66.1 |
| Senseval-3 | 1,850 | 65.3 | 66.3 |
| SemEval-2013 | 1,644 | 63.0 | 63.4 |
| SemEval-2015 | 1,022 | 67.2 | 67.7 |
| **All four** | 6,798 | **65.1** | **65.8** |

The pull improved every set. A naive use of SemCor as a second witness (context-word co-occurrence with each witnessed sense) did not add to the total, though it helped on SemEval-2013 and SemEval-2015. Tuning chose the largest weights tried, so the weights are not yet settled.

For reference, on the full five-set ALL:

| System | F1 | Source |
| --- | --- | --- |
| Extended Lesk | 48.7 | Raganato et al. 2017 |
| UKB (personalized PageRank) | 53.2 | Raganato et al. 2017 |
| Most frequent sense | 64.8 | Raganato et al. 2017 |
| WordNet first sense | 65.2 | Raganato et al. 2017 |
| UKB with sense priors | 67.3 | [Agirre et al. 2018](https://arxiv.org/pdf/1805.04277) |
| IMS (supervised) | 68.4 | Raganato et al. 2017 |
| BEM (neural) | 79.0 | [Blevins & Zettlemoyer 2020](https://aclanthology.org/2020.acl-main.95.pdf) |
| ConSeC (neural) | 82.0 | [Barba et al. 2021](https://aclanthology.org/2021.emnlp-main.112.pdf) |

Post-2019 papers score ALL without SemEval-2007, as done here, which moves the most-frequent-sense baseline from 64.8 to 65.5.

## Sources

- Alessandro Raganato, Jose Camacho-Collados, and Roberto Navigli. [Word Sense Disambiguation: A Unified Evaluation Framework and Empirical Comparison](https://aclanthology.org/E17-1010.pdf). EACL 2017. Data: [WSD_Evaluation_Framework](http://lcl.uniroma1.it/wsdeval/data/WSD_Evaluation_Framework.zip).
- Eneko Agirre, Oier López de Lacalle, and Aitor Soroa. [Random Walks for Knowledge-Based Word Sense Disambiguation](https://aclanthology.org/J14-1003.pdf). Computational Linguistics, 2014.
- Eneko Agirre, Oier López de Lacalle, and Aitor Soroa. [The risk of sub-optimal use of Open Source NLP Software: UKB is inadvertently state-of-the-art in knowledge-based WSD](https://arxiv.org/pdf/1805.04277). 2018.
- Terra Blevins and Luke Zettlemoyer. [Moving Down the Long Tail of Word Sense Disambiguation with Gloss Informed Bi-encoders](https://aclanthology.org/2020.acl-main.95.pdf). ACL 2020.
- Edoardo Barba, Luigi Procopio, and Roberto Navigli. [ConSeC: Word Sense Disambiguation as Continuous Sense Comprehension](https://aclanthology.org/2021.emnlp-main.112.pdf). EMNLP 2021.
- Francis Bond, Piek Vossen, John P. McCrae, and Christiane Fellbaum. [CILI: the Collaborative Interlingual Index](https://aclanthology.org/2016.gwc-1.9.pdf). GWC 2016.
- Francis Bond and Ryan Foster. [Linking and Extending an Open Multilingual Wordnet](https://aclanthology.org/P13-1133.pdf). ACL 2013.
- Joakim Nivre et al. [Universal Dependencies v2](https://aclanthology.org/2020.lrec-1.497.pdf). LREC 2020; [CoNLL-U format](https://universaldependencies.org/format.html).
- Local witnesses: WordNet 3.0, CILI, Open Multilingual Wordnet, PredicateMatrix 1.3, UD v2.17, and the Wiktionary English extract (kaikki.org).
