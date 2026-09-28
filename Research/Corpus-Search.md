# Corpus Search

Laplace's Merkle DAG is a grammar-compressed corpus, so exact occurrence counts, distinct-document counts, and phrase search inside containers all have direct precedent in the literature on grammar-compressed and suffix-based text indexes.

## Scope

This page collects research on searching and counting over the [Storage](../Storage/README.md) layer. It sets Laplace beside the published engines that count exact n-grams over trillion-token corpora, the index structures for phrases inside documents, the critiques of tokenization, and the distributional-semantics work that rests on exact co-occurrence counts.

Numbers are quoted from the cited sources unless they are marked as an estimate. No number on this page was measured by a local research script.

## The DAG as a grammar

A straight-line program (SLP) is a context-free grammar in Chomsky normal form that derives exactly one string. The general form is a context-free grammar with rules `A → α1 … αt`, and run-length grammars add rules `A → B^s` ([Navarro](https://arxiv.org/pdf/2004.02781); [Navarro & Pacheco](https://arxiv.org/pdf/2406.00221)).

A Laplace [composition](../Storage/Compositions.md) is a rule of that kind, n-ary rather than binary:

| Grammar compression | Laplace |
| --- | --- |
| Terminal symbol | [Atom](../Storage/Atoms.md): a codepoint, tier 0 |
| Nonterminal and its rule | Composition: a word, a sentence, a paragraph |
| Start symbol | A document's trunk node |
| Set of start symbols over shared rules | The whole corpus, one DAG |
| Grammar tree: the parse tree pruned at the first mention of each nonterminal | Storage: one record per distinct node, by [identity](../Storage/Identity.md) |

One difference is in how the rules are chosen. Grammar-compression algorithms such as RePair, LZ-derived schemes, and locally consistent parsing choose rules to minimise the grammar size. Laplace's rules are fixed by [segmentation](../Storage/Compositions.md#segmentation), so a repeat becomes a shared node when it aligns with a segment: a whole word, sentence, or document. A phrase such as "breast cancer" is not a node; it is the run `[breast, ' ', cancer]` inside a sentence node. Whole-document and whole-sentence duplication is the dominant kind in web-scale corpora (see [Duplication in large corpora](#duplication-in-large-corpora)).

## Occurrence counting

The number of times node `v` occurs in the corpus is the number of paths from document trunks down to `v`. It is a sum over the parents' counts:

```text
occ(trunk) = 1                                  (or the number of times that trunk was ingested)
occ(v)     = Σ occ(p)  over every child position of v in every parent p
```

A word used twice in one sentence contributes twice, because each child position is its own edge. One pass in tier order, from the trunks down, computes every count in `O(V + E)` over the distinct nodes `V` and child positions `E`; the tiers give that order without a separate topological sort.

The grammar-index literature uses the same quantity. Every occurrence of a nonterminal `A` triggers the same fixed number of secondary occurrences, so indexes store a count `c(A)` per rule ([Navarro, document listing](https://arxiv.org/pdf/1707.06374); [Navarro & Pacheco](https://arxiv.org/pdf/2406.00221)).

In a general SLP, path counts can grow exponentially in the grammar size: `g` rules can derive a string of length `2^g`. Laplace's depth is bounded by its tiers, so `occ(v)` is at most the corpus length and fits in 64 bits.

Maintenance under ingestion (estimate, not from a source): ingesting a document `D` adds `occ_D(v)` to every node reachable from `D`'s trunk. `occ_D` is the same pass restricted to `D`'s sub-DAG, which costs at most `O(|D|)`. This holds even when `D` reuses an existing sentence, because that sentence's descendants are exactly the nodes that gain counts. Removal is the same pass with subtraction.

## Distinct-document counting

Occurrence count is not document frequency. `occ(v)` sums over paths; "in how many distinct documents does `v` appear" is a union over ancestor trunks and does not decompose additively.

This is the document listing and document counting problem on repetitive collections. [Navarro](https://arxiv.org/pdf/1707.06374) lists the documents containing a pattern of length `m` in `O(m log^{1+ε} N · ndoc)`, and gives a grammar index of `O(r log N)` bits that counts occurrences in `O(m² + m log^{2+ε} r)`.

In Laplace, a node's distinct documents are found by walking up through its containers and deduplicating the trunks reached. The cost is the number of distinct ancestors: for "cancer", every distinct sentence that contains it and all of their ancestors.

## Phrase search inside containers

### Primary and secondary occurrences

Every grammar index rests on one idea ([Gagie et al.](https://arxiv.org/pdf/1109.3954); [Christiansen et al.](https://arxiv.org/pdf/1811.12779); [Navarro & Pacheco](https://arxiv.org/pdf/2406.00221)):

- A primary occurrence of a pattern crosses a boundary between the children of some rule. Its locus is the lowest node that covers it.
- A secondary occurrence is a copy of a primary occurrence inside another mention of that node or of its ancestors.

In Laplace, "breast cancer" inside a sentence is a primary occurrence whose locus is that sentence node, with the cut between the child `breast` and the children `' ', cancer`. Every other place the same sentence occurs is a secondary occurrence, and there are `occ(sentence)` of them in total. The total count of a phrase is therefore:

```text
count(phrase) = Σ occ(S)  over every primary occurrence of the phrase, with locus node S
```

This is the counting scheme of the grammar indexes: each grid point that marks a child boundary carries `c(A)`, and a two-dimensional range sum adds them up.

### How Laplace finds the containers

In Laplace, every container of a node is found with the GIN index over each [trajectory's](../Storage/Physicality.md#trajectories) constituents, and the trajectory records their order. A phrase is a contiguous run of constituents in a container's trajectory. The containers that match are distinct nodes, so a sentence repeated 61,036 times (see [below](#duplication-in-large-corpora)) is found once and weighted by its `occ`.

Matching the run is a comparison of trajectories: a window of the container's path equal to the phrase's path, at Fréchet distance 0. On the prototype, finding every continuation of "the capital of" in 3,846 containers took 30 ms with the comparison done on raw vertex bytes in C; see [Prototype](Prototype.md#continuation-as-geometry).

### Published structures

The structures below are how other systems answer phrase and substring queries. They are literature, listed for their costs.

| Structure | Unit indexed | Count cost | Space | Source |
| --- | --- | --- | --- | --- |
| Positional inverted index | Word occurrence, with positions | Intersect word lists, then check positions `p, p+1, …`; dominated by the lists of common words | Positions dominate; a few common-word lists exceed 10% of a Web index | [Zobel & Moffat](https://dmice.ohsu.edu/bedricks/courses/cs506-problem-solving-with-large-clusters/articles/week1/zobel_invertedindex.pdf) |
| Two-word phrase index | Word pair | One list lookup | Complete: about 50% of the source; pairs starting with the 3 commonest words: about 1%, halving phrase query time | [Zobel & Moffat](https://dmice.ohsu.edu/bedricks/courses/cs506-problem-solving-with-large-clusters/articles/week1/zobel_invertedindex.pdf) |
| Nextword plus partial phrase index | Word, next word, positions | About 1/4 of the time of an inverted index | 26% extra space | Williams, Zobel & Bahle 2004 (abstract only); related scheme: [Veretennikov](https://arxiv.org/pdf/1801.09079) |
| Suffix array | Every suffix of the text | `O(m log N)`, independent of the occurrence count | About 7 bytes per token in infini-gram | [Liu et al.](https://arxiv.org/pdf/2401.17377) |
| FM-index | Every suffix, compressed | `O(m · H0)` | 0.26–0.44 × the text | [Xu et al.](https://arxiv.org/pdf/2506.12229) |
| r-index | BWT runs | `O(m)` count, `O(m + occ)` locate | `O(r)`, small for repetitive text | [Gagie, Navarro & Prezza](https://arxiv.org/pdf/1809.02792) |
| Grammar index | Child boundaries of each rule | `O(m log n + m log^{2+ε} g)` for general grammars; `O(m log^{2+ε} n)` in `O(g_rl)` space for run-length grammars | `O(g)` | [Christiansen et al.](https://arxiv.org/pdf/1811.12779); [Navarro & Pacheco](https://arxiv.org/pdf/2406.00221) |
| CDAWG over a grammar-compressed string | Grammar plus CDAWG | `O(ra(m) + occ)`, where `ra` is grammar random-access time | — | [Cleary et al.](https://arxiv.org/pdf/2407.08826) |

A pattern that spans two containers, such as the end of one sentence and the start of the next, or a substring that does not align with word nodes, is a cross-boundary pattern. The grammar indexes above handle that case; the containers of a single node do not.

## Exact n-gram engines

These are the published baselines for exact counting and continuation queries over corpora of trillions of tokens.

| Engine | Structure | Scale | Index size | Count latency |
| --- | --- | --- | --- | --- |
| [infini-gram](https://arxiv.org/pdf/2401.17377) (COLM 2024) | Suffix array over the tokenized corpus | About 5T tokens (Dolma, RedPajama, Pile, C4) | 7 bytes per token, 3.5 × the tokenized data | About 7–14 ms for n = 1 to 1000 on RedPajama, independent of n and of frequency |
| [infini-gram mini](https://arxiv.org/pdf/2506.12229) (EMNLP 2025) | FM-index on raw UTF-8 bytes, no tokenizer | 83 TB indexed | 0.44 × the corpus, down to about 0.26 × | 4–32 ms for a 1-byte query, 0.1–0.4 s for 10 bytes, 5–25 s for 1000 bytes |

infini-gram:

- All occurrences of `x1 … xn` form one contiguous range of the suffix array. The count is the width of the range, found by two binary searches in `O(n log N)` comparisons. The indexes stay on disk.
- The RedPajama suffix array (1.4T tokens) took about 48 hours on one node with 128 CPUs and 1 TiB of RAM.
- A 5-gram count table for 1.4T tokens would take 28 TB. The implicit count table behind infini-gram has at least 2 × 10^15 distinct in-document n-grams.
- An n-gram next-token distribution takes 31 ms; an ∞-gram probability 90 ms; a full ∞-gram next-token distribution 88–180 ms.
- The ∞-gram (the longest suffix with a nonzero count) predicts the next token of human text with 47% accuracy. Interpolated with neural language models, it cuts perplexity by up to 73%.
- It counts token n-grams, so its counts depend on the tokenizer. It does not deduplicate: repeated text is indexed every time it occurs.

infini-gram mini:

- It is the closest precedent to indexing below the tokenizer: it works on bytes, where Laplace works on codepoints.
- Indexing is 18 × faster than the best earlier FM-index implementation and uses 3.2 × less RAM. About 1 PB of Common Crawl would take roughly 1,200 node-days.
- It trades time for space: on the Pile, infini-gram counts in 13 ms, infini-gram mini in 106–696 ms.
- It found benchmark contamination of up to 74.2% (GSM8K) in Internet crawls.

## Duplication in large corpora

[Lee et al.](https://arxiv.org/pdf/2107.06499) (ACL 2022) deduplicated training data with a suffix array over the BPE byte stream:

- A single 61-word English sentence repeats 61,036 times in C4.
- Over 1% of unprompted language-model output is verbatim training data, falling to about 0.1% after deduplication. Over 4% of standard validation sets overlap with training data.
- Duplicate substrings are adjacent suffix-array entries with a common prefix of at least 50 BPE tokens. Building the suffix array for C4 (350 GB) took under 12 hours wall-clock, and deduplication under 1 hour, on 96 cores with 768 GB of RAM.

[Elazar et al.](https://arxiv.org/pdf/2310.20707) (What's In My Big Data?, ICLR 2024) analysed more than 35 TB:

- About 50% of the documents in RedPajama and LAION-2B-en are exact duplicates, and more than 60% in the Pile.
- Exact counts are used where the key space fits in RAM. Elsewhere, such as for 10-grams, they use hashed "compressed counts" that accept collision error. Exact duplicate detection on C4 by keeping the strings would need more than 800 GB of RAM, which is why they hash.

In Laplace, such a sentence or document is one node, and its count is recovered by [occurrence counting](#occurrence-counting). Every node already has an exact content ID, so the counts need no hashing approximation.

## Tokenization

Laplace's units are codepoints and the compositions built from them. The published critiques of tokenizers, and the models that avoid them, are:

- [Petrov et al.](https://arxiv.org/pdf/2305.15425) (NeurIPS 2023): the same text translated across languages differs in token length by up to 15 × (Shan against English). With the ChatGPT and GPT-4 tokenizer, Italian takes 1.6 × as many tokens as English, Bulgarian 2.6 × and Arabic 3 ×. Even character- and byte-level encodings differ by over 4 × (Burmese and Tibetan against Chinese, in bytes).
- [UAX #29](https://www.unicode.org/reports/tr29/): the default word boundaries are not adequate for Thai, Lao, Khmer, and Myanmar, which need tailoring, and ideographs break at every character. Reliable word detection in Thai, Lao, Chinese, and Japanese requires dictionary lookup. The number of nodes per unit of meaning therefore still varies by script.
- [ByT5](https://arxiv.org/pdf/2105.13626) (TACL 2022): an unmodified T5 on UTF-8 bytes. Competitive with mT5, more robust to noise, and better on spelling-sensitive tasks; inference is 1.5–9.5 × slower depending on the task.
- [CANINE](https://arxiv.org/pdf/2103.06874) (TACL 2022): codepoint input with multi-hash embeddings in place of a vocabulary. It beats mBERT by 5.7 F1 on TyDi QA with fewer parameters. Like Laplace, it uses Unicode codepoints rather than bytes.
- [MEGABYTE](https://arxiv.org/pdf/2305.07185) (NeurIPS 2023): fixed-size byte patches, with a global model over patches and a local model within them. Self-attention cost falls to `O(N^{4/3})`, and it models sequences of more than 1M bytes.
- [Byte Latent Transformer](https://arxiv.org/pdf/2412.09871) (2024): dynamic patches that end where the next-byte entropy of a small byte model exceeds a threshold. It matches Llama 3 at fixed training FLOPs with up to 50% fewer inference FLOPs.

All of these are input schemes for learned models: their units are transient and not addressable. Laplace's units are content-addressed, stored, and countable. The Byte Latent Transformer's entropy patching is the closest published analogue to a data-driven segmentation, and grammar compressors such as RePair are the other known way to make frequent runs into rules.

## Distributional semantics

The distributional hypothesis ties meaning to co-occurrence:

- Harris (1954), "Distributional Structure": differences in meaning correspond to differences in distribution.
- Firth (1957): "You shall know a word by the company it keeps." [Brunila & LaViolette](https://arxiv.org/pdf/2205.07750) argue that Harris's version is purely formal, while Firth's includes situational and cultural context.

Exact counts and their use as semantics:

- [Church & Hanks](https://aclanthology.org/J90-1003.pdf) (1990): pointwise mutual information (PMI) over windowed co-occurrence counts, for lexicography. This is the canonical use of exact counts as semantics.
- [Baroni, Dinu & Kruszewski](https://aclanthology.org/P14-1023.pdf) (ACL 2014), "Don't count, predict!": count vectors (PMI and LMI, reduced with SVD or NMF) against word2vec-style predictive vectors on about 2.8B tokens. The predictive models won.
- [Levy & Goldberg](https://papers.nips.cc/paper_files/paper/2014/file/b78666971ceae55a8e87efb7cbfd9ad4-Paper.pdf) (NeurIPS 2014): skip-gram with negative sampling implicitly factorises a word-context PMI matrix shifted by `log k`. A sparse shifted positive PMI matrix does as well or better on similarity.
- [Levy, Goldberg & Dagan](https://aclanthology.org/Q15-1016.pdf) (TACL 2015): most of the advantage of embeddings comes from hyperparameters such as context-distribution smoothing and subsampling. Transferred to count models, these leave mostly local or insignificant differences.

What this means for exact counts in Laplace:

- Sentence-level co-occurrence is `count(a, b) = Σ occ(S)` over the distinct sentences `S` that contain both `a` and `b`. The marginals are `occ(a)`, `occ(b)`, and the corpus total. Exact PMI and positive PMI are therefore available without sampling or hashing.
- The trajectory gives structural windows (same sentence, same paragraph, same document) as well as positional ones. Baroni et al. found the window size matters (2 against 5 words).
- Exact counts give attribution and provenance. By themselves they do not generalise to unseen combinations: the ∞-gram reaches 47% next-token accuracy but needs neural interpolation for perplexity. The published comparisons evaluate similarity against reweighted and reduced count baselines (shifted positive PMI, SVD), not raw counts.

## Sources

- Liu, Min, Zettlemoyer, Choi & Hajishirzi, [infini-gram](https://arxiv.org/pdf/2401.17377), COLM 2024.
- Xu, Liu, Choi, Smith & Hajishirzi, [infini-gram mini](https://arxiv.org/pdf/2506.12229), EMNLP 2025.
- Lee et al., [Deduplicating Training Data Makes Language Models Better](https://arxiv.org/pdf/2107.06499), ACL 2022.
- Elazar et al., [What's In My Big Data?](https://arxiv.org/pdf/2310.20707), ICLR 2024.
- Zobel & Moffat, [Inverted files for text search engines](https://dmice.ohsu.edu/bedricks/courses/cs506-problem-solving-with-large-clusters/articles/week1/zobel_invertedindex.pdf), ACM Computing Surveys 2006.
- Williams, Zobel & Bahle, [Fast phrase querying with combined indexes](https://people.eng.unimelb.edu.au/jzobel/fulltext/acmtois04.pdf), ACM TOIS 2004 (figures from the abstract; the full text was not retrieved).
- Veretennikov, [Using additional indexes for fast full-text search of phrases that contain frequently used words](https://arxiv.org/pdf/1801.09079).
- Gagie, Navarro & Prezza, [Fully functional suffix trees and optimal text searching in BWT-runs bounded space](https://arxiv.org/pdf/1809.02792) (r-index).
- Navarro, [Indexing Highly Repetitive String Collections, Part I](https://arxiv.org/pdf/2004.02781), ACM Computing Surveys 2021.
- Navarro & Pacheco, [Counting on General Run-Length Grammars](https://arxiv.org/pdf/2406.00221), CPM 2025.
- Navarro, [Document listing on repetitive collections with guaranteed performance](https://arxiv.org/pdf/1707.06374).
- Gagie, Gawrychowski, Kärkkäinen, Nekrich & Puglisi, [A faster grammar-based self-index](https://arxiv.org/pdf/1109.3954).
- Christiansen et al., [Optimal-time dictionary-compressed indexes](https://arxiv.org/pdf/1811.12779).
- Cleary et al., [The CDAWG Index and Pattern Matching on Grammar-Compressed Strings](https://arxiv.org/pdf/2407.08826).
- Petrov et al., [Language Model Tokenizers Introduce Unfairness Between Languages](https://arxiv.org/pdf/2305.15425), NeurIPS 2023.
- Unicode, [UAX #29: Unicode Text Segmentation](https://www.unicode.org/reports/tr29/).
- Xue et al., [ByT5](https://arxiv.org/pdf/2105.13626), TACL 2022.
- Clark et al., [CANINE](https://arxiv.org/pdf/2103.06874), TACL 2022.
- Yu et al., [MEGABYTE](https://arxiv.org/pdf/2305.07185), NeurIPS 2023.
- Pagnoni et al., [Byte Latent Transformer](https://arxiv.org/pdf/2412.09871), 2024.
- Harris, [Distributional Structure](https://www.tandfonline.com/doi/abs/10.1080/00437956.1954.11659520), Word 10(2–3), 1954 (paywalled; cited, not read).
- Firth, A synopsis of linguistic theory 1930–1955, in Studies in Linguistic Analysis, Blackwell, 1957 (no online copy; cited, not read).
- Brunila & LaViolette, [What company do words keep? Revisiting the distributional semantics of J.R. Firth & Zellig Harris](https://arxiv.org/pdf/2205.07750).
- Church & Hanks, [Word association norms, mutual information, and lexicography](https://aclanthology.org/J90-1003.pdf), Computational Linguistics 16(1), 1990.
- Baroni, Dinu & Kruszewski, [Don't count, predict!](https://aclanthology.org/P14-1023.pdf), ACL 2014.
- Levy & Goldberg, [Neural Word Embedding as Implicit Matrix Factorization](https://papers.nips.cc/paper_files/paper/2014/file/b78666971ceae55a8e87efb7cbfd9ad4-Paper.pdf), NeurIPS 2014.
- Levy, Goldberg & Dagan, [Improving Distributional Similarity with Lessons Learned from Word Embeddings](https://aclanthology.org/Q15-1016.pdf), TACL 2015.
