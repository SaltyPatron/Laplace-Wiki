# Laplace-Wiki

<p align="center"><img src="assets/laplace-logo.webp" alt="Laplace" width="640"></p>

This repository is the Laplace documentation. It explains how everything at every level works.

Read it online at <https://saltypatron.github.io/Laplace-Wiki/>.

Every page in this repository is listed below. Read every listed page in full.

## Pages

- [Architecture](Architecture.md) — Laplace is native C, with SQL and C# as orchestration.
- [Storage](Storage/README.md) — Laplace stores all digital content as a self-deduplicating Merkle DAG with deterministic, lossless storage, laid out as geometry in four dimensions.
  - [Space](Storage/Space.md) — Laplace places everything in a 4-ball inside a 4-cube, with Unicode projected across the 4-ball's surface, the S³, and compositions forming inside it.
  - [Atoms](Storage/Atoms.md) — codepoints are tier 0, the absolute floor: every Unicode codepoint has a deterministic ID and a deterministic coordinate on the S³.
  - [Compositions](Storage/Compositions.md) — a composition is an n-ary, recursive sequence of constituents, each of which is a codepoint or another composition.
  - [Identity](Storage/Identity.md) — every node's ID is the BLAKE3 hash of its constituents, so the same content always has the same ID.
  - [Physicality](Storage/Physicality.md) — every entity has a full, real 4D coordinate, and every composition's content is stored as a trajectory.
  - [Ingestion](Storage/Ingestion.md) — ingestion computes content's IDs on the client and deduplicates it trunk to leaf against what is already recorded.
- [Semantics](Semantics/README.md) — semantics are the relations Laplace records about entities, so that it can link concepts and languages and hop and fan out from anything to anything with integrity.
  - [Attestations](Semantics/Attestations.md) — curated corpora attest to entities, ordinary digital content is observed, and every attestation is a win, draw, or loss and/or a score from a witness.
  - [Claims](Semantics/Claims.md) — a claim is a tuple of entities with referential integrity, and its ID is computed from its components the same way a composition's is.
  - [Consensus](Semantics/Consensus.md) — everything attested about a claim, as a whole, provides its overall score: a Glicko-2 standing that tells how hard a strand tugs back.
  - [Pull](Semantics/Pull.md) — Laplace's forward pass is native C recursive operations with A* and indexed lookups, pulling on an interwoven web of entities and attestations.
  - [Personality firmware](Semantics/Firmware.md) — the personality firmware is a pull's decision tree: which segment of which branch to take, and how to combine them, from the observation, its attestations, and the tree across tiers, kept out of the training data.
- [Corpora](Corpora/README.md) — Each page specifies one collection's record format and the attestation that format supplies.
  - [Unicode Character Database](Corpora/Unicode.md) — The Unicode Character Database attests everything the standard says of a code point, the flat XML is the record of it, and the property files add only what the XML does not carry.
  - [ISO 639](Corpora/ISO-639.md) — ISO 639 attests what each list says of a language code, under the list's own field names, and nothing renames or reconciles the codes across the lists.
  - [Wordnets](Corpora/Wordnets.md) — The wordnets attest sense, each of its own synsets and senses under its own names, and CILI is the hop between them that carries a sense across languages without becoming a second witness of the Princeton gloss; the manual pages attest nothing.
  - [Word sense disambiguation](Corpora/Word-Sense-Disambiguation.md) — A sense-annotated corpus attests which wordnet sense a token carries, and each dataset is its own witness because its identifiers start over.
  - [Universal Dependencies](Corpora/Universal-Dependencies.md) — A Universal Dependencies treebank attests what it says of each word within its sentence, the validator's data attests which tags, relations, and features the project permits, and the documentation attests what each of those is called.
  - [Hops](Corpora/Hops.md) — The lexicons are separate witnesses, and a hop is the curated edge that lets consensus on a claim in one of them pull on a claim in another.
  - [FrameNet](Corpora/FrameNet.md) — FrameNet attests frames, the roles in them, and the lexical units that evoke them.
  - [VerbNet](Corpora/VerbNet.md) — VerbNet attests class membership of a verb and the thematic roles and frames of that class.
  - [PropBank](Corpora/PropBank.md) — PropBank attests a predicate's roleset and the roles in it.
  - [SemLink](Corpora/SemLink.md) — SemLink attests the mapping between PropBank, VerbNet, and FrameNet, which is a hop and not a third lexicon.
  - [Predicate Matrix](Corpora/Predicate-Matrix.md) — Predicate Matrix attests one predicate role joined across VerbNet, WordNet, FrameNet, and PropBank.
  - [MapNet](Corpora/MapNet.md) — MapNet attests a generated mapping from FrameNet 1.3 to WordNet 1.6, with the precision its own README states and no score on a row.
  - [VerbAtlas](Corpora/VerbAtlas.md) — VerbAtlas attests a clustering of WordNet synsets into frames.
  - [FrameBase](Corpora/FrameBase.md) — FrameBase attests a frame schema and its links to WordNet 3.0, and it is not FrameNet.
  - [WordFrameNet](Corpora/WordFrameNet.md) — WordFrameNet's files pair a frame with a word and a synset offset, and no witness is named because the fields are undefined.
  - [Wiktionary](Corpora/Wiktionary.md) — Wiktextract attests a written word in one language as one part of speech, and every edition of that extract is the same witness.
  - [ConceptNet](Corpora/ConceptNet.md) — ConceptNet attests an assertion of a relation between two concepts.
  - [ATOMIC](Corpora/ATOMIC.md) — ATOMIC 2020 attests commonsense tuples written as a head, a relation, and a tail, and ATOMIC10X is a model-generated witness of the same shape that enters unrated.
  - [Tatoeba](Corpora/Tatoeba.md) — Tatoeba attests what it and its members say of a whole sentence, its language, text, owner, translations, tags, lists, audio, transcriptions, and reviews, and attests nothing of the words inside it.
  - [OpenSubtitles](Corpora/OpenSubtitles.md) — OpenSubtitles attests the language of a subtitle sentence and does not attest the language of a word.
  - [Project Gutenberg](Corpora/Project-Gutenberg.md) — Project Gutenberg's texts are observed content and attest nothing.
  - [Tokenizers](Corpora/Tokenizers.md) — A model tokenizer's vocabulary is observed content and attests nothing.
  - [GeoNames](Corpora/GeoNames.md) — GeoNames attests what its gazetteer's tables say of each place, alternate name, and code under the column names its readme gives, and its readme itself is observed text that attests nothing.
  - [Civil Comments](Corpora/Civil-Comments.md) — Civil Comments attests the seven numbers Jigsaw gave each comment under their own names, as numbers and not as scores, and the identity columns of other releases are not in these files.
  - [Measuring Hate Speech](Corpora/Measuring-Hate-Speech.md) — Measuring Hate Speech attests what each annotator says of a comment as that annotator's own witness, and what the set measured of the comment and holds of the annotator, and the Parquet files and the card attest nothing.
  - [HateCheck](Corpora/HateCheck.md) — HateCheck attests what its gold standard and each of its ten annotators say of every test case, SGHateCheck attests the same of its test cases in Malay, Mandarin, Singlish, and Tamil with each annotator of each file a witness of its own, and the language models' readings of the SGHateCheck cases attest nothing.
  - [ProsocialDialog](Corpora/Prosocial-Dialog.md) — ProsocialDialog attests everything a line says of its context, the potentially unsafe utterance, as one record of the set, and a member that is null attests nothing.
  - [RealToxicityPrompts](Corpora/RealToxicityPrompts.md) — RealToxicityPrompts attests what each instance says of its file name and what its prompt and its continuation each say of their text, as a witness whose lineage is the Perspective API, and a score is recorded as the number written, not as an outcome.
  - [Social Bias Frames](Corpora/Social-Bias-Frames.md) — Social Bias Frames attests what each MTurk worker answered of a post as that worker's own witness, what the set says of the post and of the worker, and the same aggregated per post, where the first, unnamed column attests nothing.
  - [Social Chemistry](Corpora/Social-Chemistry.md) — Social-Chem-101 attests everything a breakdown row says of its rule of thumb as one record of the set, and a row whose situation, characters, rule, action, or judgment holds a double quote is not read.
  - [ToxiGen](Corpora/ToxiGen.md) — ToxiGen attests what the set says of each generation and of its prompt, what each prompt file's name says of its texts, what the annotated set says of each text, and what each hashed worker says of a text and of themself, and the CSV and Parquet copies attest nothing.
  - [XSTest](Corpora/XSTest.md) — XSTest attests what its prompt file says of each prompt and what each model's completion file says of the prompt as that model completed it, with the two annotation columns each a witness of its own, and the evaluation files attest nothing.
  - [COCO](Corpora/COCO.md) — COCO has no recipe yet, so its annotation JSON and images are not ingested and attest nothing.
  - [Code authority](Corpora/Code-Authority.md) — The `cpython`, `docs`, `postgres`, and `runtime` checkouts have no recipe yet, so they are not ingested and attest nothing.
  - [Code corpus](Corpora/Code-Corpus.md) — The old project trees have no recipe yet, so they are not ingested and attest nothing.
  - [Games](Corpora/Games.md) — The PGN collections and the Lichess opening tables have no recipe yet, so they are not ingested and attest nothing.
  - [NLTK](Corpora/NLTK.md) — The Brown Corpus in NLTK's tagged form has no recipe yet, so it is not ingested and attests nothing.
  - [Natural Earth](Corpora/Natural-Earth.md) — Natural Earth's shapefiles have no recipe yet, so they are not ingested and attest nothing.
  - [The Stack v2](Corpora/Stack-v2.md) — The Stack v2 has no recipe yet, so its Parquet rows are not ingested and attest nothing.
  - [Tiny codes](Corpora/Tiny-Codes.md) — Tiny Codes has no recipe yet, so its rows are not ingested and attest nothing.
  - [Tree-sitter](Corpora/TreeSitter.md) — Tree-sitter grammars are what the Engine parses files with, named by a recipe's `grammar` line, and they are not a source: nothing in them is attested.
  - [Weights](Corpora/Weights.md) — Model weights have no recipe yet, so they are not ingested and attest nothing, and Spitball holds the intent to assimilate them.

- [Query](Query.md) — Laplace finds content by computing its ID and coordinates on the client and looking them up with spatial indexes.
- [Operations](Operations/README.md) — Operations covers what Laplace runs on and how it is built, configured, deployed, and tuned, from bare hardware to loaded, indexed, and measured content.
  - [Setup](Operations/Setup.md) — Laplace runs on x86-64 CPUs, uses every SIMD level the CPU has, never requires a GPU, and wants its database heap, write-ahead log, and temporary files on separate fast drives.
  - [Builds](Operations/Builds.md) — PostgreSQL, Laplace-Native, and Laplace-postgres are built from source with Intel's compilers, with floating-point settings that give the same bits on every CPU.
  - [Database](Operations/Database.md) — PostgreSQL's defaults suit small general-purpose servers; Laplace tunes memory, I/O, and planning to its hardware and to the way it uses geometry and indexes.
  - [Deployment](Operations/Deployment.md) — A Laplace database goes from empty to benchmarked in five steps: extensions, schema, ingestion, indexes, and measurement.
- [Research](Research/README.md) — research collects the sourced findings and measured results that support the Laplace specification.
  - [Prototype](Research/Prototype.md) — a working prototype of the storage layer was built from the specification and tested against 195 Project Gutenberg texts, and every number on this page was measured on it.
  - [Placement](Research/Placement.md) — Codepoints are placed on the S³ by taking Marc Alexa's Super-Fibonacci points for n = 1,114,112 in the order of their 4D Hilbert value and giving DUCET rank *r* the *r*-th point, which puts collation neighbors next to each other in space.
  - [Sampling](Research/Sampling.md) — Super-Fibonacci spirals give a fixed-size, evenly spread set of points on the S³, and this page records their construction, their relation to the Hopf fibration and to incremental grids, radical-inverse ordering, and local numeric checks.
  - [Unicode](Research/Unicode.md) — Laplace's tier 0 and its segmentation rest on the Unicode data, and this page records what that data defines, what it covers, and which parts of it are stable across versions.
  - [Hashing](Research/Hashing.md) — Research on how BLAKE3, Merkle trees and DAGs, hash-consing, and IEEE-754 bit packing behave under the Laplace identity scheme.
  - [Geometry](Research/Geometry.md) — Research on how PostgreSQL and PostGIS store, index, and compute on four-dimensional geometry, and on the 4D distance, centroid, and curve tools that Laplace builds on them.
  - [Numerics](Research/Numerics.md) — Research on the floating-point limits of Laplace's coordinates and of IDs written into geometry, the cost of colliding its IDs, and how trajectory distance measures treat noise and repetition.
  - [Semantics Experiments](Research/Semantics-Experiments.md) — first experiments with semantic records on the local curated corpora measured how identifiers link words, concepts, and languages, how annotation layers deduplicate as content, how witnessed claims translate between languages, and how well a pull disambiguates word senses.
  - [Chess](Research/Chess.md) — Glicko-2 ratings computed from observed chess games alone, one game at a time in the order the games were played, predicted over-the-board results better than the official ratings once each player entered at an attested rating.
  - [Learning](Research/Learning.md) — Research on how ratings can be updated one matchup at a time, how retrieval compares with knowledge stored in model weights, and what the literature reports about softmax, unlearning, execution feedback, and interpretability.
  - [Recipes](Research/Recipes.md) — research and measurements on how one generic decomposer can take any standardized file format apart into content and put it back together byte for byte.
  - [Corpus Search](Research/Corpus-Search.md) — Laplace's Merkle DAG is a grammar-compressed corpus, so exact occurrence counts, distinct-document counts, and phrase search inside containers all have direct precedent in the literature on grammar-compressed and suffix-based text indexes.
  - [Prior Art](Research/Prior-Art.md) — Each mechanism in Laplace's storage layer has published precedent, and the research found no prior system that combines them.
  - [Trust](Research/Trust.md) — Research and measurements on how much a witness's attestation should count and how hard each kind of word or relation should pull, measured on the local witnesses, on 88 languages of Universal Dependencies, and on word sense disambiguation.
  - [Engine Measurements](Research/Engine.md) — The first shared components of the real implementation, Laplace-Native and Laplace-postgres, were measured on a tuned PostgreSQL server with the Gutenberg corpus, and every number on this page comes from their benchmarks.
  - [Model Ingestion](Research/Models.md) — First measurements of AI models as sources: a farm of 33 models surveyed from metadata alone, every tokenizer ingested as content, three models' embeddings recorded as witnessed testimony, and one model interviewed with templates taken from the corpus, all graded against the attested web.
  - [Relations Research](Research/Relations.md) — Research into rating models, evidence counts, search over rated relations, truth discovery, and provenance is background for Laplace's semantics layer.
- [Spitball](Spitball.md) — text that has not been properly considered for the documentation as a whole.
