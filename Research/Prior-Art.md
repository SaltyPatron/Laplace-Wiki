# Prior Art

Each mechanism in Laplace's storage layer has published precedent, and the research found no prior system that combines them.

## How to read this page

This page maps the [Storage](../Storage/README.md) layer onto published work. It uses three labels:

- **Known**: the mechanism is published, and the source is cited.
- **No match found**: the research searched for the mechanism or combination and found no published instance. This is not a claim that the idea is certainly new, nor that it has been shown to work.
- **Closest precursors**: the published work nearest to a component that has no exact match.

The Laplace side of each comparison is as the Storage pages describe it: every codepoint has a fixed point on the S³ ([Atoms](../Storage/Atoms.md)), content is recomposed into an n-ary Merkle DAG ([Compositions](../Storage/Compositions.md)) named by BLAKE3 ([Identity](../Storage/Identity.md)), and every composition has a real 4D centroid and a trajectory that records the order of its constituents ([Physicality](../Storage/Physicality.md)). Nothing on this page was measured; all findings are from the cited sources.

## Vector symbolic architectures

Vector symbolic architectures (VSA), also called hyperdimensional computing, compose fixed symbol vectors into vectors for structures.

- [Kanerva (2009)](https://redwood.berkeley.edu/wp-content/uploads/2018/01/kanerva2009hyperdimensional.pdf) computes with about 10,000-dimensional random vectors. The operations are addition (bundling, normalised to a mean vector), multiplication (binding), and permutation. "The sum (and the mean) of random vectors has the following important property: it is similar to each of the vectors being added together." Kanerva also stores sequences as pointer chains in an associative memory.
- Plate's Holographic Reduced Representations ([1991](https://www.ijcai.org/Proceedings/91-1/Papers/006.pdf); [1995](https://pages.ucsd.edu/~msereno/170/readings/06-Holographic.pdf)) bind by circular convolution. Plate states that such memories cannot reconstruct accurately, so recall needs "an additional error-correcting auto-associative item memory". Plate's sequence encoding by repeated self-binding is called "trajectory association"; the name matches Laplace's trajectory, but the mechanism differs.
- [Gayler (2003)](https://arxiv.org/abs/cs/0412059) coined the term and argued that binding and bundling together give compositional structure.
- The survey by Kleyko, Rachkovskij, Osipov and Rahimi ([Part I](https://arxiv.org/abs/2111.06077), [Part II](https://arxiv.org/abs/2112.15424)) is the reference map. The item memory of atoms often does not need to be stored, because it "can be easily rematerialized" from a seed. Superposition keeps the result similar to its inputs; binding makes it dissimilar. Sequences are encoded by position binding or by repeated permutation, and one scheme superimposes a bag-of-symbols part and an ordered part.
- Recovering items from a superposition is a signal-detection problem, and exact recovery holds only for bounded structures ([Thomas, Dasgupta & Rosing](https://arxiv.org/abs/2010.07426)).
- [Haley & Smolensky (COLING 2020)](https://aclanthology.org/2020.coling-main.328/) use cryptographic hashing to generate role vectors for unboundedly many tree positions, and invert parse trees from a 30,000-dimensional tensor product representation with less than 1% error. It is the only published combination of cryptographic hashing and vector composition the research found.

| Laplace | VSA counterpart |
| --- | --- |
| A fixed, deterministic point per codepoint | An atomic vector per symbol in an item memory, often regenerated from a seed |
| A composition's coordinate is the centroid of its constituents | Bundling: the normalised sum or mean, similar to every constituent |
| Order kept separately, in the trajectory | A bag part plus an ordered part; Kanerva's pointer chains |
| Nearest-neighbour search in the spatial index | Clean-up memory: lookup in the item memory |
| Recursively composed wholes | Part–whole hierarchies |

The differences the literature points to:

- **Dimension.** VSA relies on 10³ to 10⁴ dimensions so that random atoms are nearly orthogonal and bundles can be decoded. Laplace uses four. A 4D centroid cannot be decoded back into its constituents; in Laplace the DAG holds the constituents exactly, so the centroid is a summary rather than the representation.
- **Exact identity and lossless recovery.** VSA equality is approximate similarity, and recovery is noisy clean-up. Laplace has exact equality through BLAKE3 and recovery by walking the DAG. Plate's separate item memory is, in Laplace, the DAG itself.
- **Binding.** Laplace has no binding operator. In VSA, "dog bites man" and "man bites dog" differ inside one vector, and a query such as "who is the agent?" is answered by unbinding. In Laplace, the two sentences share a centroid and differ in their trajectories and IDs; roles come from the containing composition (see [Types](../Storage/Compositions.md#types)).
- **Atom layout.** VSA atoms are random, or correlated by level for scalars. Laplace atoms are placed by collation order, so related characters are neighbours, and the layout is the same for every install. The research found no VSA work that fixes one universal codebook over all of Unicode.
- **Hashing.** Haley and Smolensky hash positions to make role vectors; the vector is the representation and inversion is approximate. Laplace hashes content to make an identity, stores it beside a low-dimensional geometric summary, and inverts through the DAG.

A property from this literature applies to any centroid: for `n` independent uniform points on the S³, the expected squared norm of their mean is `1/n`. Distance from the centre therefore mostly reflects how many distinct, spread-out constituents are averaged. Anagrams share a centroid, as [Physicality](../Storage/Physicality.md#centroids) states for `[c,a,t]` and `[a,c,t]`.

## Hyperbolic embeddings

- [Nickel & Kiela (NeurIPS 2017)](https://arxiv.org/abs/1705.08039) learn embeddings in the Poincaré ball. The root of a tree sits at the origin and the leaves near the boundary; the norm encodes the level in the hierarchy and the angle encodes similarity. The Lorentz-model follow-up is [Nickel & Kiela (2018)](https://arxiv.org/abs/1806.03417).
- Ganea, Bécigneul and Hofmann extend this to [hyperbolic neural networks](https://arxiv.org/abs/1805.09112) and to partial orders as nested [entailment cones](https://arxiv.org/abs/1804.01882).
- [Sarkar (2011)](https://homepages.inf.ed.ac.uk/rsarkar/papers/HyperbolicDelaunayFull.pdf) shows that any tree embeds in the hyperbolic plane with arbitrarily low distortion.
- [De Sa, Gu, Ré & Sala (ICML 2018)](https://arxiv.org/abs/1804.03329) give a combinatorial, non-learned construction that reaches a mean average precision of 0.989 on WordNet in two dimensions, but needs about 500 bits of precision. At fixed precision, the dimension needed grows linearly with the longest path.

What matches: a whole hierarchy inside a finite ball, with radius tied to structure and angle to similarity. De Sa et al. show that a deterministic, non-learned hierarchy embedding is possible.

What differs:

- **Direction.** Poincaré embeddings put the most general node at the centre and the most specific at the boundary. Laplace puts the atoms on the surface ([Space](../Storage/Space.md)), and compositions fall inward.
- **Metric.** Hyperbolic distance gives exponentially more room toward the boundary, which is what lets trees embed with low distortion. Laplace averages in Euclidean 4D, which gives less room toward the centre as compositions grow.
- **Learned or derived.** Poincaré positions are optimised to reproduce a given graph. Laplace positions are computed from content, and the graph is stored separately.
- **Precision.** De Sa et al.'s result is that fixed floating-point precision limits how deep a geometric hierarchy can be told apart. It applies to deep centroids of floating-point coordinates.

## Character and subword sums

- [fastText (Bojanowski et al. 2017)](https://arxiv.org/abs/1607.04606): "We represent a word by the sum of the vector representations of its n-grams." The n-grams are hashed into a fixed table; the vectors are learned.
- [Charagram (Wieting et al. 2016)](https://arxiv.org/abs/1607.02789): a word or sentence vector is a nonlinearity applied to a sum of learned character n-gram vectors.
- Averaging word vectors is a standard sentence baseline, for example SIF ([Arora, Liang & Ma, ICLR 2017](https://openreview.net/forum?id=SyK00v5xx)).
- [Random Indexing](https://en.wikipedia.org/wiki/Random_indexing) (Kanerva, Kristoferson & Holst 2000; [Sahlgren 2005](https://www.diva-portal.org/smash/get/diva2:1041127/FULLTEXT01.pdf)) gives each term a fixed sparse random index vector, and context vectors are running sums. Sahlgren, Holst and Kanerva (2008) add order by permuting index vectors by position.

What matches: a fixed vector per unit, composition by sum or mean, and, as in Random Indexing, atoms assigned once with no training so that new items can be added incrementally. Laplace's centroid is a bag-of-characters average applied recursively.

What differs: fastText and Charagram learn their vectors for semantic similarity. Laplace's atoms are fixed by collation order, so the similarity a centroid carries is orthographic: `cat` falls near `act`, not near `kitten`. None of these systems keeps an exact identity or a recoverable structure.

## Content-addressed code and data

- **Unison.** A definition's identity is "a 512-bit SHA3 digest of a term or a type's internal structure, excluding all names" ([The Big Idea](https://www.unison-lang.org/docs/the-big-idea/); [Hashes](https://www.unison-lang.org/docs/language-reference/hashes/)). "Names are just separately stored metadata that don't affect the function's hash." Mutually recursive definitions are hashed as one cycle: recursive references are replaced by a De Bruijn index of the cycle, members are sorted by hash, and each member becomes `#ccc.n` ([FAQ](https://www.unison-lang.org/docs/usage-topics/general-faqs/)).
- **Hash-consing** (Ershov 1958; Goto 1974; Filliâtre & Conchon 2006): structurally equal values are shared as one node ([overview](https://en.wikipedia.org/wiki/Hash_consing)).
- **Merkle trees and DAGs** (Merkle 1979; git; [IPFS](https://arxiv.org/abs/1407.3561)): links are hashes of their targets, a node can have many parents, and deduplication follows ([overview](https://en.wikipedia.org/wiki/Merkle_tree)).
- **Hashlife** (Gosper 1984): hash-consed quadtrees, a spatial, hierarchical, content-addressed structure ([overview](https://en.wikipedia.org/wiki/Hashlife)).
- **Sequitur** ([Nevill-Manning & Witten 1997](https://arxiv.org/abs/cs/9709102)): repeated phrases in a symbol stream are replaced by rules, building a DAG of shared sub-sequences. RePair and LZ78 are relatives. See [Corpus Search](Corpus-Search.md#the-dag-as-a-grammar) for the grammar view of Laplace's DAG.

What matches: Laplace's [identity](../Storage/Identity.md), the BLAKE3 hash of the constituents with the same content always giving the same ID, is the Unison, Merkle, and hash-consing principle applied to all content. Unison's "names are metadata, not identity" parallels Laplace's [types](../Storage/Compositions.md#types): `[2,5,5]` is a number, and it gets a type only from the composition that uses it.

What differs:

- **Cycles.** Unison hashes cycles because code can be mutually recursive. A Laplace composition is always at least one tier above its constituents, so the DAG is acyclic by construction and needs no cycle hashing. Mutual reference, such as two documents that cite each other, is then not containment; it would belong to a relations layer (see [Relations Research](Relations.md)).
- **Geometry.** Unison, git, IPFS, and hash-consing attach no coordinate to a hash. Laplace attaches a derived 4D coordinate to every hash-identified node.
- **Segmentation.** IPFS chunks bytes by size or content; Sequitur learns phrases from repetition. Laplace uses one Unicode-standard segmentation hierarchy per modality, down to codepoints. The research found hierarchical text chunking, but not a single canonical decomposition for all content.

## Addressing all possible content

- **Gödel numbering** (1931) encodes a sequence `x₁ … xₙ` as `2^x₁ · 3^x₂ · 5^x₃ · …`, injective by unique factorisation ([overview](https://en.wikipedia.org/wiki/G%C3%B6del_numbering)).
- **Leibniz's characteristic numbers** (1679) give primitive concepts primes and a compound concept their product: if "animal" is 2 and "rational" is 3, "man" is 6. "Every S is P" holds when P's number divides S's, so the number reveals composition and containment ([IEP](https://iep.utm.edu/leib-log/); [SEP](https://plato.stanford.edu/entries/leibniz-logic-influence/); [Characteristica universalis](https://en.wikipedia.org/wiki/Characteristica_universalis)). Leibniz found that it fails for particular propositions and moved to pairs of coprime numbers.
- **Wilkins (1668)** spelled each word of a philosophical language by its place in a universal taxonomy ([overview](https://en.wikipedia.org/wiki/An_Essay_Towards_a_Real_Character,_and_a_Philosophical_Language)). Borges' essay "The Analytical Language of John Wilkins" is the classic critique of universal classification.
- **The Library of Babel.** Borges' 1941 story has a library of every possible book. [libraryofbabel.info](https://libraryofbabel.info/About.html) contains every 3,200-character page over a 29-symbol alphabet and stores none of them ([overview](https://en.wikipedia.org/wiki/The_Library_of_Babel_(website))). Its author needed an algorithm "regular enough to create the same block of text in the same place every time, yet random-seeming enough that no user would notice patterns", and invertible so that search works; after Halton-sequence attempts lost information to floating-point division, he used "a formula combining modular arithmetic and bit-shifting operations" ([theory](https://libraryofbabel.info/theory4.html)).

A Babel address is a bijective pseudo-random permutation of the text read as an integer, chosen so that neighbouring addresses are unrelated ([theory](https://libraryofbabel.info/theory.html)). It gives identity and lossless recovery, and no similarity or containment structure.

| | Identity | Lossless recovery | Position carries structure | Exact containment from the number |
| --- | --- | --- | --- | --- |
| Gödel numbering | Yes | Yes | No | No |
| Leibniz's characteristic numbers | Yes | Yes | Yes | Yes, by divisibility |
| Library of Babel | Yes | Yes | No, by design | No |
| Laplace | Yes, BLAKE3 | Yes, through the DAG | Yes, the centroid | No; containment is in the DAG, found through the trajectory index |

Laplace runs a Babel-like address (the hash) and a Leibniz-like structured address (the centroid) side by side. Unlike Gödel and Leibniz numbers, which are unbounded and exact, a 4D centroid is finite, and many multisets share one. The centroid of a whole lies in the convex hull of its parts, but lying in a hull does not imply containment.

## The periodic-table standard

Laplace is framed as organising knowledge the way the periodic table organises the elements. The standard the periodic table set was confirmed prediction. In 1871 Mendeleev published gaps in his table with predicted properties, and independent discoveries confirmed them ([overview](https://en.wikipedia.org/wiki/Mendeleev%27s_predicted_elements)):

| Predicted element | Discovered as | Predicted | Found |
| --- | --- | --- | --- |
| Eka-aluminium | Gallium (Lecoq de Boisbaudran, 1875) | Mass 68, density 6.0, oxide Ea₂O₃ | Mass 69.7, density 5.91, Ga₂O₃ |
| Eka-boron | Scandium (Nilson, 1879) | Mass 44 | — |
| Eka-silicon | Germanium (Winkler, 1886) | Mass 72, density 5.5, grey, dioxide density 4.7 | Mass 72.6, density 5.32, grey, dioxide density 4.23 |
| Eka-manganese | Technetium (1937) | Mass 100 | About 97–98 |

The periodic table's predictive power came from periodicity: properties recur with position because of an underlying physical law.

Organisations of knowledge and of computing that have been called periodic tables:

- **Leibniz, Wilkins, and Ranganathan's Colon Classification** (1933) are universal, compositional organisations of concepts. They are not geometric, and the record does not show them predicting unobserved members.
- **Idreos et al., the Periodic Table of Data Structures** ([2018](https://stratos.seas.harvard.edu/publications/periodic-table-data-structures)) and the **Data Calculator** ([arXiv 1808.02066](https://arxiv.org/abs/1808.02066)) build data structures from design primitives. Gaps in the design space suggest undiscovered structures, and their performance is computed without implementing them.
- **I-Con** ([Alshammari et al., ICLR 2025](https://arxiv.org/abs/2504.16929)) recovers more than 20 representation-learning methods from one information-theoretic equation. A gap in its table led to a new clustering method about 8% better on unsupervised ImageNet.

A test of Laplace against Mendeleev's standard is future work: an empty region or gap in the geometry that implies unobserved content with specific, checkable properties, later confirmed.

## Near matches

The research searched for Unicode placed on spheres, text stored as PostGIS geometry, hash IDs packed into coordinates, Merkle DAG and embedding hybrids, geometric content addressing, and sentence trajectories compared with Fréchet distance. It found no system that combines these. The nearest matches, closest first:

1. **Chaos Game Representation and Universal Sequence Maps** (Jeffrey 1990; [Almeida & Vinga 2002](https://doi.org/10.1186/1471-2105-3-6); [Almeida et al. 2025](https://arxiv.org/abs/2508.06641); review by [Chan & Corless](https://arxiv.org/abs/2012.09638); [overview](https://en.wikipedia.org/wiki/Chaos_game_representation)). The closest geometric precursor. Each symbol is a fixed vertex: a unit square for DNA, a hypercube for larger alphabets. A sequence is mapped by `x_k = (x_{k−1} + vertex(s_k)) / 2`, a running exponentially weighted average of symbol points, so every point lies inside the convex hull of the vertices, and the sequence of points is a trajectory. Universal Sequence Maps are claimed bijective given enough precision. Differences: the average is weighted toward the most recent symbols rather than uniform; the map is flat per sequence rather than a recursive DAG; there is no hash identity; and the alphabet is small, never all of Unicode.
2. **Semantic hashing** ([Salakhutdinov & Hinton 2009](https://www.cs.utoronto.ca/~rsalakhu/papers/semantic_final.pdf)). "Documents are mapped to memory addresses in such a way that semantically similar documents are located at nearby addresses." The address is learned, lossy, and not unique.
3. **SimHash and locality-sensitive hashing** ([Charikar 2002](https://www.cs.princeton.edu/courses/archive/spr04/cos598B/bib/CharikarEstim.pdf)). Similarity-preserving fingerprints, the usual complement to cryptographic hashes; many deduplication systems store both. In Laplace the centroid plays the similarity-preserving role and BLAKE3 the cryptographic one. Storing both is common practice; storing the similarity side as a geometric point in a spatial index is not something the research found.
4. **Haley & Smolensky (2020)**, above: cryptographic hashing combined with invertible compositional embedding of trees.
5. **Hashlife** and **S2 cell IDs**. Hashlife is spatial and content-addressed. [S2](http://s2geometry.io/devguide/s2cell_hierarchy.html) derives 64-bit IDs from positions on the sphere along a Hilbert curve; the ID encodes the position. In Laplace the position is computed from content, and the ID is packed into the mantissas of a separate [ID point](../Storage/Identity.md#the-id-point).
6. **Super-Fibonacci spirals** ([Alexa, CVPR 2022](https://openaccess.thecvf.com/content/CVPR2022/papers/Alexa_Super-Fibonacci_Spirals_Fast_Low-Discrepancy_Sampling_of_SO3_CVPR_2022_paper.pdf)). The sampling Laplace uses for [placement](../Storage/Atoms.md#placement). Published for low-discrepancy sampling of orientations, not for symbol codebooks.
7. **Fréchet distance for trajectories** (Alt & Godau 1995). Mature for GPS tracks and curves. The research found no work that compares texts as Fréchet polylines through fixed symbol points; the closest are distances between CGR images and Word Mover's Distance over point clouds.

## Known and no match found

| Component | Status | Closest precursors |
| --- | --- | --- |
| A fixed, training-free point per symbol | Known | VSA item memory regenerated from a seed; Random Indexing; CGR vertices |
| All 1,114,112 codepoints placed by DUCET rank on Super-Fibonacci points taken in Hilbert order on the S³ | No match found for the universal codebook; each ingredient is published | DUCET; Alexa 2022; Hilbert ordering as in S2 |
| A composition's coordinate is the unweighted centroid of its constituents | Known | VSA bundling (Kanerva's mean vector); bag-of-characters and word averaging; SIF; fastText sums |
| Every composition falls inside the ball, and only repeats of a single codepoint sit on the surface | Known: a convex combination of points on a strictly convex sphere | CGR (inside the convex hull); Poincaré (inside the ball, learned, reversed direction) |
| Radius as an axis | Known in another form: for spread-out constituents, the norm of a mean falls as about `1/√n` | Poincaré norm as hierarchy level, reversed |
| Order kept in a separate trajectory beside an unordered summary | Known in concept | Kleyko et al.'s bag plus ordered parts; Kanerva's pointer chains; CGR trajectories |
| Texts compared as Fréchet polylines | No match found | Fréchet trajectory search; CGR image distances; Word Mover's Distance |
| A content-addressed Merkle DAG with maximal sharing | Known | Merkle 1979; hash-consing; git; IPFS; Unison |
| Acyclicity by tiering, with no cycle hashing | Known design choice | Merkle DAGs; contrast Unison's `#x.n` cycles |
| One Unicode-standard segmentation per modality, down to codepoints, as the DAG's levels | No match found as a universal design | Sequitur and RePair (learned phrases); IPFS chunking (bytes) |
| Type only from the containing composition | Known in spirit | Unison's names as metadata; VSA role–filler binding; Frege's context principle |
| An exact identity and a similarity-bearing coordinate in one record | Pairing known in practice; as geometry in a spatial database, no match found | SimHash with SHA; semantic hashing; Haley & Smolensky |
| A hash ID bit-packed into the mantissas of a geometry point | No match found | S2 cell IDs (the reverse direction) |
| A spatial database as the store and index for a Merkle DAG of all content | No match found | Hashlife (spatial and content-addressed, for cellular automata) |
| A binding operator | Not present in Laplace; VSA has one | Plate; Gayler; Kanerva |
| Position reveals composition | Partly: the centroid is not injective in 4D; containment is exact in the DAG | Leibniz 1679 (exact, unbounded); Gödel 1931 |
| Organising knowledge like a periodic table | Framing known; a test of confirmed prediction is future work | Mendeleev 1871; Idreos 2018; I-Con 2025 |

Each mechanism above has precedent: fixed atoms, averaging, trajectories, Merkle and hash-consing identity, low-discrepancy sphere sampling, and Fréchet distance. What the research did not find anywhere is their combination: one fixed, collation-ordered geometric codebook over all of Unicode; one canonical, recursive, cross-modal Merkle DAG; and every node carrying both an exact cryptographic identity and a derived 4D coordinate, stored as spatial database points and trajectories.

## Sources

- Kanerva, [Hyperdimensional Computing](https://redwood.berkeley.edu/wp-content/uploads/2018/01/kanerva2009hyperdimensional.pdf), Cognitive Computation 1(2), 2009.
- Plate, [Holographic Reduced Representations](https://www.ijcai.org/Proceedings/91-1/Papers/006.pdf), IJCAI 1991; [Holographic Reduced Representations](https://pages.ucsd.edu/~msereno/170/readings/06-Holographic.pdf), IEEE TNN 6(3), 1995.
- Gayler, [Vector Symbolic Architectures Answer Jackendoff's Challenges for Cognitive Neuroscience](https://arxiv.org/abs/cs/0412059), 2003.
- Kleyko, Rachkovskij, Osipov & Rahimi, [A Survey on Hyperdimensional Computing aka Vector Symbolic Architectures, Part I](https://arxiv.org/abs/2111.06077) and [Part II](https://arxiv.org/abs/2112.15424).
- Thomas, Dasgupta & Rosing, [A Theoretical Perspective on Hyperdimensional Computing](https://arxiv.org/abs/2010.07426), JAIR 2021.
- Haley & Smolensky, [Invertible Tree Embeddings using a Cryptographic Role Embedding Scheme](https://aclanthology.org/2020.coling-main.328/), COLING 2020.
- Nickel & Kiela, [Poincaré Embeddings for Learning Hierarchical Representations](https://arxiv.org/abs/1705.08039), NeurIPS 2017; [Learning Continuous Hierarchies in the Lorentz Model of Hyperbolic Geometry](https://arxiv.org/abs/1806.03417), 2018.
- Ganea, Bécigneul & Hofmann, [Hyperbolic Neural Networks](https://arxiv.org/abs/1805.09112); [Hyperbolic Entailment Cones for Learning Hierarchical Embeddings](https://arxiv.org/abs/1804.01882), 2018.
- Sarkar, [Low Distortion Delaunay Embedding of Trees in Hyperbolic Plane](https://homepages.inf.ed.ac.uk/rsarkar/papers/HyperbolicDelaunayFull.pdf), 2011.
- De Sa, Gu, Ré & Sala, [Representation Tradeoffs for Hyperbolic Embeddings](https://arxiv.org/abs/1804.03329), ICML 2018.
- Bojanowski, Grave, Joulin & Mikolov, [Enriching Word Vectors with Subword Information](https://arxiv.org/abs/1607.04606), 2017.
- Wieting, Bansal, Gimpel & Livescu, [Charagram: Embedding Words and Sentences via Character n-grams](https://arxiv.org/abs/1607.02789), 2016.
- Arora, Liang & Ma, [A Simple but Tough-to-Beat Baseline for Sentence Embeddings](https://openreview.net/forum?id=SyK00v5xx), ICLR 2017 (cited, not read).
- [Random indexing](https://en.wikipedia.org/wiki/Random_indexing), Wikipedia; Sahlgren, [An Introduction to Random Indexing](https://www.diva-portal.org/smash/get/diva2:1041127/FULLTEXT01.pdf), 2005 (cited, not read).
- Unison, [The Big Idea](https://www.unison-lang.org/docs/the-big-idea/), [Hashes](https://www.unison-lang.org/docs/language-reference/hashes/), and [General FAQs](https://www.unison-lang.org/docs/usage-topics/general-faqs/).
- [Hash consing](https://en.wikipedia.org/wiki/Hash_consing), [Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree), and [Hashlife](https://en.wikipedia.org/wiki/Hashlife), Wikipedia.
- Benet, [IPFS: Content Addressed, Versioned, P2P File System](https://arxiv.org/abs/1407.3561), 2014.
- Nevill-Manning & Witten, [Identifying Hierarchical Structure in Sequences: A linear-time algorithm](https://arxiv.org/abs/cs/9709102), JAIR 7, 1997.
- [Gödel numbering](https://en.wikipedia.org/wiki/G%C3%B6del_numbering), Wikipedia.
- [Leibniz: Logic](https://iep.utm.edu/leib-log/), Internet Encyclopedia of Philosophy; [Leibniz's Influence on 19th Century Logic](https://plato.stanford.edu/entries/leibniz-logic-influence/), Stanford Encyclopedia of Philosophy; [Characteristica universalis](https://en.wikipedia.org/wiki/Characteristica_universalis), Wikipedia.
- [An Essay Towards a Real Character, and a Philosophical Language](https://en.wikipedia.org/wiki/An_Essay_Towards_a_Real_Character,_and_a_Philosophical_Language), Wikipedia.
- Basile, [libraryofbabel.info: About](https://libraryofbabel.info/About.html), [Theory](https://libraryofbabel.info/theory.html), and [the algorithm](https://libraryofbabel.info/theory4.html); [The Library of Babel (website)](https://en.wikipedia.org/wiki/The_Library_of_Babel_(website)), Wikipedia.
- [Mendeleev's predicted elements](https://en.wikipedia.org/wiki/Mendeleev%27s_predicted_elements), Wikipedia.
- Idreos et al., [The Periodic Table of Data Structures](https://stratos.seas.harvard.edu/publications/periodic-table-data-structures), IEEE Data Engineering Bulletin 2018; Idreos et al., [The Internals of the Data Calculator](https://arxiv.org/abs/1808.02066).
- Alshammari et al., [I-Con: A Unifying Framework for Representation Learning](https://arxiv.org/abs/2504.16929), ICLR 2025.
- Chan & Corless, [Chaos Game Representation](https://arxiv.org/abs/2012.09638); [Chaos game representation](https://en.wikipedia.org/wiki/Chaos_game_representation), Wikipedia.
- Almeida & Vinga, [Universal sequence map (USM) of arbitrary discrete sequences](https://doi.org/10.1186/1471-2105-3-6), BMC Bioinformatics 3:6, 2002 (cited, not read); Almeida et al., [Fractal Language Modelling by Universal Sequence Maps (USM)](https://arxiv.org/abs/2508.06641), 2025.
- Salakhutdinov & Hinton, [Semantic Hashing](https://www.cs.utoronto.ca/~rsalakhu/papers/semantic_final.pdf), 2009.
- Charikar, [Similarity Estimation Techniques from Rounding Algorithms](https://www.cs.princeton.edu/courses/archive/spr04/cos598B/bib/CharikarEstim.pdf), STOC 2002.
- Google, [S2 Cells](http://s2geometry.io/devguide/s2cell_hierarchy.html).
- Alexa, [Super-Fibonacci Spirals: Fast, Low-Discrepancy Sampling of SO(3)](https://openaccess.thecvf.com/content/CVPR2022/papers/Alexa_Super-Fibonacci_Spirals_Fast_Low-Discrepancy_Sampling_of_SO3_CVPR_2022_paper.pdf), CVPR 2022.
- Cited without a public copy: Jeffrey, Chaos game representation of gene structure, Nucleic Acids Research 18, 1990; Filliâtre & Conchon, Type-Safe Modular Hash-Consing, ML Workshop 2006; Alt & Godau, Computing the Fréchet distance between two polygonal curves, IJCGA 5, 1995; Sahlgren, Holst & Kanerva, Permutations as a Means to Encode Order in Word Space, CogSci 2008.
