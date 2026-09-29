# 10. Recipes

One generic decomposer per standardized format turns bytes into structure, and one semantic recipe per curated source says what each recovered field becomes: content, occurrence, reference, provenance, testimony, calculation, packaging, or an explicit unresolved obligation.

Literally any standardized or fixed-format file is a modality to Laplace, and Laplace treats them all exactly the same: a generic decomposer uses a recipe to tell it how to extract the content. Format is generic and semantics are per source. Recipes are Laplace grammars: UAX #29 but for semantics, modality agnostic. A recipe is written before the first file of its format is ingested, and a curated source's recipe is written against the staged release it will be activated with.

## Before this stage

[1. Unicode](Unicode.md): the segmentation data. [3. Builds](Builds.md): the decomposer and the grammars. [5. Tier 0](Tier-0.md): the atoms every decomposition bottoms out in. [6. Registries](Registries.md): the relations, qualifiers, vocabularies, and types a recipe may name. [9. Sources](Sources.md): the staged release and its recovered schema.

## Operations, per format

### 10.1 Obtain the format's specification

- **In:** the format.
- **Do:** a recipe first needs the format's structure: fields, chunks, repeats, and choices. That comes from the format's own specification. Collected so far: PNG, RFC 1950, 1951, and 2083, GIF89a, ITU T.81 (JPEG), JFIF, EXIF 2.3 and the ExifTool tag table, BMP headers, WAVE, the MP3 frame header, ID3v2.3 and ID3v2.4, the MP4 box registry, the ZIP application note, FASTA, FASTQ, GenBank, GFF3, and TeX category codes. The formats in the curated estate: XML (WN-LMF, UCD XML, FrameNet, VerbNet, PropBank frames, UD metadata, ISO 639), RDF Turtle and RDF/XML (CILI, FrameBase, ISO 639), TSV and CSV (ISO 639-3, CILI maps, OMW, Tatoeba, ConceptNet, ATOMIC 2020, Lichess openings, GeoNames, the UCD `.txt` files), JSON and JSON Lines (Wiktextract, ATOMIC, SemLink, safety sets), CoNLL-U (UD), PGN and FEN (TWIC, chess corpora), Parquet, WNDB, Moses parallel text, safetensors, BibTeX, TOML, Markdown, and HTML.
- **Out:** the structure the recipe will follow.
- **From:** [Research: Recipes: Specifications](../Research/Recipes.md#specifications); `docs/plan/ASSIMILATION_ROADMAP.md` workstream D.

### 10.2 Choose the provider

- **In:** the specification of 10.1.
- **Do:** one of four:
  - **Plain text:** UAX #29. Extended grapheme clusters by rules GB1–GB999, words by WB1–WB999, sentences by SB1–SB998. Letters, numbers, Katakana, and ExtendNumLet glue into runs; WB999 breaks everywhere else, so by default every punctuation mark and every Han ideograph is its own segment. Sentence rules are heuristic, and abbreviations such as "Mr." need CLDR suppressions. Scripts written without spaces need tailoring; ICU implements dictionary-based breaking for Thai, Lao, Khmer, Myanmar, and CJK. The rules are defined on NFD but apply directly to non-NFD text with equivalent results, so segmenting does not require normalizing. Whitespace is Latin-specific: a space is an entity in the path, and the link between `Captain` and `Ahab` has a hop.
  - **Binary formats:** a declarative structure such as Kaitai Struct's, whose library has 189 specifications including BMP, PNG, GIF, JPEG, EXIF, WAV, RIFF, ID3, the QuickTime box structure, ZIP, gzip, ELF, and Ogg, handling repeats, switches, sub-streams, bit fields, and zlib.
  - **Code and markup:** a tree-sitter grammar. Every node records its byte range, and whitespace is the gap between tokens, so the tokens plus the stored gaps rebuild a source file exactly. The local collection has 303 grammar directories, about 30,208 files, including CSV, XML, Markdown, SQL, disassembly, and configuration formats. Tree-sitter is a grammar estate, a compatibility parser, a validator, and a realizer; it is not required in the hot path merely because a grammar exists.
  - **Huge shallow standards files:** a streaming standards reader, when a 2.8 GB Wiktextract, a FrameBase Turtle, or the UCD XML exposes the required facts directly and materializing an equivalent tree is redundant work.
  - The provider is registered by format id and injected: one format-decomposer interface, each implementation turning bytes into nodes or records with fields and positions and exposing that structure as the file's content physicality.
- **Out:** the provider the decomposer parses with.
- **From:** [Compositions: Segmentation](../Storage/Compositions.md#segmentation); [Research: Unicode: Text segmentation](../Research/Unicode.md#text-segmentation-uax-29); [Research: Recipes: Grammars](../Research/Recipes.md#grammars); `docs/plan/INGEST_BOUNDARY_AND_RECIPE_LAW.md` §Universal tier / trajectory boundary; `docs/plan/ASSIMILATION_ROADMAP.md` workstream D.

### 10.3 Keep the five boundaries apart

- **In:** the provider of 10.2.
- **Do:** the physical artifact, the transport read or feed buffer, the parser's record or node, the canonical content, and the persistence batch are five boundaries, and none becomes another because two happen to have the same cardinality in one implementation. A UTF-8 scalar, a quoted record, a token, an AST construct, a sample, or a compressed block may cross a transport boundary, and the provider carries enough state to recover the same structure regardless of legal transport partitioning. A parser record is observed structure, not automatically content: the recipe decides. A probe batch, a COPY buffer, a transaction, or a partition task may change performance, WAL, memory, and scheduling; it may not change canonical world state. A file, line, row, AST node, parser callback, fixed record block, or I/O buffer is never content identity by default.
- **Out:** a provider whose output is invariant to how it was fed.
- **From:** `docs/plan/INGEST_BOUNDARY_AND_RECIPE_LAW.md` §Five boundaries that are not interchangeable.

### 10.4 Write the trunk: metadata and content

- **In:** the structure of 10.1.
- **Do:** a file has a trunk, with children for the file's metadata and for the file's content: EXIF data, headers, and so on. Every standardized file branches into its own trees. A source is a trunk entity above its files: UD is one source trunk, each of its files is a trunk under it, and each record from each file sits under that, so the physicality trajectories are what link content to its sources; when two sources collide on a sentence, that sentence now has two parents. The recipe says which parts are metadata and which are content, and which tree each goes in.
- **Out:** the shape of the source's and the file's trunks.
- **From:** [Compositions: Files](../Storage/Compositions.md#files); `docs/INVENTOR_RECORD.md` §Decomposition.

### 10.5 Write the tiers of the content tree

- **In:** the provider of 10.2.
- **Do:** the recipe says how the content breaks down to codepoints, tier by tier, and tiers are modality-specific and dynamic. For text: codepoint ↔ grapheme ↔ word ↔ sentence ↔ document ↔ file, with paragraphs, titles, pages, and the various separators besides, including dedicated separator codepoints, some of them language-specific. For code: codepoints → tokens → expressions → statements and functions → files → directories → repository root. For an image: codepoint → digit → number → channel intensity → pixel → patch → region → image → scene. For audio: codepoint → digit → number → sample → window → segment → track. For video: ordered frame roots plus audio roots plus timing and synchronization occurrences → video root. For a game: pieces, squares, moves, positions, lines, games. For a model: tokenizer, config, components, circuits. Numbers are compositions of codepoints under a declared exact scalar recipe: `255 → ['2','5','5']`, `0.34567 → ['0','.','3','4','5','6','7']`, `-32768 → ['-','3','2','7','6','8']`; a value gets a type only when it is put into a composition. Nothing is dropped: whitespace and punctuation are constituents like everything else. For code, every syntax subtree becomes a node whose ID is the hash of its children's IDs, with the gaps between children as text constituents; the node's kind is not hashed, because 331,616 distinct subtrees were given more than one kind by the grammars and hashing the kind would have split each into separate entities. Grammar productions, precedence, associativity, delimiters, arity, and field roles are themselves ordinary entities, relations, and attestations that constrain which higher-tier composition applies; a parser's `MultiplicationOperator` node is optional derived structure, not the meaning.
- **Out:** the decomposition of a file of this format into a Merkle DAG.
- **From:** [Compositions: Tiers](../Storage/Compositions.md#tiers); [Compositions: Types](../Storage/Compositions.md#types); `docs/INVENTION.md` §3; `docs/invention/modality-ladder-law.md`; `docs/specs/05_Substrate_Invariants.txt` Rule #1c; [Research: Recipes: Code, measured](../Research/Recipes.md#code-measured).

### 10.6 Declare the scalar recipe

- **In:** any numeric field of the format.
- **Do:** the scalar recipe is deterministic and lossless for the admitted digital representation. It declares, as applicable, the radix, sign, decimal point, exponent form, leading and trailing zero normalization, exact precision and scale, whether the source representation is integer, rational, fixed, or floating, and signed-zero, NaN, and infinity handling. Canonicalization starts from the exact admitted representation and its precision boundary; an incidental host floating-point rendering is not authority when it loses source precision. No amplitude, colour, or sample value is minted as a tier-0 atom.
- **Out:** the scalar recipe of the format.
- **From:** `docs/invention/modality-ladder-law.md` §Exact scalar canonicalization; `docs/invention/modality-codepoint-floor-checklist.md`.

### 10.7 Write the repeats

- **In:** the tiers of 10.5.
- **Do:** repeats are not recorded one by one. An all-white image does not record a billion white pixels: the white pixel is one entity, and repeats are run-length encoded, with the run length in the vertex's M. A million identical amplitudes are one scalar root and a million sample occurrences. Pixels, patches, and regions are finite in space, while large, and deduplicate heavily; an 8×8 region references 204 square occurrences, 64 of 1×1 through one of 8×8, and introduces only the roots not already known. Deduplicating two-dimensional structure at the highest tier, as a quadtree down to 8×8 patches with pixel values packed 8 per vertex, cut 26 PNGs' storage from 98.5 times the files to 11.2 times.
- **Out:** the run-length and multiscale rule for this format.
- **From:** [Compositions: Repeats](../Storage/Compositions.md#repeats); [Physicality: Physicality](../Storage/Physicality.md#physicality); `docs/specs/33_Perfcache_Blob_Law.md` §Multiscale image basis; [Research: Recipes: Storage, measured](../Research/Recipes.md#storage-measured).

### 10.8 Write what gets reproducibility

- **In:** the specification of 10.1.
- **Do:** recipes denote how content is recorded, what content is recorded, what gets reproducibility, and what does not matter. Curated sources are mined for knowledge, not recorded bit-perfect: records, files, and packaging are not content, and only user content needs exact reconstruction. Where a recipe declares exact reconstruction, the canonical trajectories plus the retained provider and packaging facts must reproduce the admitted bytes. Compressed payloads are the hard part: stored compressed they are opaque and never deduplicate; stored decoded the exact file is lost. The recipe stores the decoded content and a small record that reproduces the original bytes. Formats with Huffman or arithmetic coding re-encode exactly from their decoded symbols; LZ-family formats, deflate and LZW, need a stored diff of the encoder's choices, as preflate and precomp keep. For lossy codecs, the quantized coefficients are the stored content and decoded pixels are derived from them. Container offsets, compression blocks, paths, and codec framing remain provenance and reconstruction state unless the recipe declares otherwise. Encrypted content has no value to Laplace: it is random binary blob storage.
- **Out:** the reconstruction record, or the declared loss, for this format.
- **Check:** the PNG recipe recomposed 26 of 26 files byte for byte, refiltering the rows, re-deflating with preflate's diff, and rebuilding the chunks and CRCs; its reconstruction data was 89,884 bytes, 19.5% of all compressed image data, most images needing 8 to 200 bytes. Plain zlib re-compression reproduced only 5 of the 26.
- **From:** [Ingestion: Recipes](../Storage/Ingestion.md#recipes); `docs/plan/ASSIMILATION_ROADMAP.md` law 2; `docs/INVENTION.md` §15; [Research: Recipes: Byte-exact recompression](../Research/Recipes.md#byte-exact-recompression); [Research: Recipes: PNG, measured](../Research/Recipes.md#png-measured).

### 10.9 Prove the format recipe round-trips

- **In:** files of the format.
- **Do:** decompose each file with the recipe and recompose it from the DAG.
- **Out:** a format decomposer that is allowed to ingest.
- **Check:** byte for byte, every file. Text: 195 of 195 Gutenberg texts. PNG: 26 of 26. Code: 5,976 of 5,976 PostgreSQL and CPython source files.
- **From:** [Research: Prototype: Ingestion](../Research/Prototype.md#ingestion); [Research: Recipes: PNG, measured](../Research/Recipes.md#png-measured); [Research: Recipes: Code, measured](../Research/Recipes.md#code-measured).

## Operations, per curated source

### 10.10 Name the format decomposer and the witness

- **In:** the source generation of [9. Sources](Sources.md).
- **Do:** a curated source's recipe names its format, receives that format decomposer by injection, and adds only the semantic layer: claims, vocabularies, qualifiers, and witness. The engine's source file names the source, its witness and lineage, its trust or deviation, the root directory, the files and exceptions, the working room, what it comes after, and what it reads. It contains no parser of its own.
- **Out:** the source's recipe header.
- **From:** `docs/plan/ASSIMILATION_ROADMAP.md` law 11; [Research: Engine Measurements](../Research/Engine.md).

### 10.11 Disposition every recovered field

- **In:** the native schema of [9. Sources](Sources.md) operation 9.3.
- **Do:** the recipe does not choose one bucket for a record; it declares how each recovered field or role contributes, and one object can produce content and testimony about that content at once. The lowering:
  - sentence, definition text, example text, prose, literal source code or media → a canonical content entity with its normal physicality and trajectory, plus a separately retained artifact and span occurrence; never a high-trust fact merely because the source contains the bytes;
  - `frame X HAS_DEFINITION text Y`, `sense X HAS_EXAMPLE sentence Y` → ensure X and Y exist under their own identity laws, then emit attributed testimony `(X, relation, Y, source, context)`; never a private edge or a duplicated text identity;
  - a sense key, synset id, frame id, roleset id, or other external record key → a typed reference under a governed identity, with a realization only when that state class participates geometrically; never ordinary text merely because the identifier is UTF-8. An ILI is not `dog`'s label; it is an identifier bound to content by a witnessed claim;
  - a row, file, span, annotation occurrence, token ordinal, gap, or containment → occurrence, trajectory, and provenance state over canonical identities; never an independent witness count;
  - release, license, file path, archive member, parser version → source, provenance, and packaging coordinates; never content or truth unless declared;
  - a deterministic parser, normalizer, or geometry consequence → versioned calculation state carrying its recipe and provider identity, marked with the derivation/calculation qualifier; never empirical testimony;
  - a field whose semantics are not mapped → an explicit unresolved obligation; never a silent fall back to content, to a string label, or to a dropped field.
  - A structured value decomposes: `06975898-n` is an offset and a part of speech, and the `-n` attests something rather than hiding inside an identifier.
- **Out:** a complete field disposition.
- **From:** `docs/plan/INGEST_BOUNDARY_AND_RECIPE_LAW.md` §Recipe lowering; `docs/plan/ASSIMILATION_ROADMAP.md` law 6; `docs/INVENTOR_RECORD.md` §Decomposition.

### 10.12 Choose the shape of every set-valued field

- **In:** each multi-valued field of 10.11.
- **Do:** three shapes, one emitter. An ordered sequence, word order in a sentence, is trajectory geometry. A single-valued attribute, `HAS_BLOCK`, `HAS_AGE`, `HAS_SCRIPT`, `HAS_LINE_BREAK`, is one typed edge. A set-valued attribute, a form's morphological analysis `{nominative, singular, masculine}`, the dialect tags on one transcription, a sense's usage register, is one composition entity and one edge, never a fan of edges, because a fan gives the set no identity, no witness can corroborate or refute the set as a whole, and the single context slot of an attestation cannot hold a set. The test: would a second witness corroborate or refute the members as a whole? Then a bundle. Does each member answer a differently named question, as UD's `FEATS` do with one relation per feature against a `Name=Value` entity? Then a record, one typed edge per field. Is each member an independent claim, as WordNet's several definitions per synset are? Then multi-valued, one edge each.
- **Out:** the shape declaration for each field.
- **From:** `docs/specs/38_Collections_Are_Compositions.md` §1, §6.

### 10.13 Normalize to the governed vocabularies

- **In:** each coded field of 10.11.
- **Do:** map the source's codes to the registries of [6. Registries](Registries.md) through declared value aliases: WordNet `n` to `NOUN`, a two-letter language code to ISO 639-3, the UCD's `can` to `Canonical`. Justify each mapping by a governed authority. Within reason, normalization is acceptable from curated seeded sources handled specially, UD, Wiktionary, WordNet, PropBank, FrameNet, SemLink, CILI, where one source indicates a noun differently from another but means the same; user content is never normalized.
- **Out:** the alias tables of the recipe.
- **From:** `docs/plan/ASSIMILATION_ROADMAP.md` law 3; `docs/INVENTOR_RECORD.md` §Decomposition.

### 10.14 Declare the claims at the right tier

- **In:** the dispositions of 10.11.
- **Do:** the engine's recipe language declares each claim block: its predicate, whether it enters, whether it is ordered, distinct, or a pair, its witnesses, its score, and whether it stands by itself or together with another. Attestations attach to the compositional object the source actually asserts, at the highest tier possible for the corpus: OpenSubtitles gives the language of sentences, not of words; a stroke count is about a codepoint; a City/State/Zip record is not sprayed across every constituent. Nothing is blanketed across tiers.
- **Out:** the claim declarations.
- **From:** `docs/INVENTIONS.md` #27; [Attestations: Attestations](../Semantics/Attestations.md#attestations); `docs/INVENTOR_RECORD.md` §Decomposition.

### 10.15 Declare what is recorded and what is calculated

- **In:** the dispositions of 10.11.
- **Do:** a decomposer records only source-observable content and assertions: literal content and ordered composition; names, identifiers, declared metadata, and source relationships; outcomes or labels supplied by the source; and the source and context responsible. Recording is deterministic transcription and must not depend on a mutable model, a heuristic threshold, an external evaluator, or current consensus. Parsing, classification, projection, correlation, evaluation, move quality, circuit analysis, inferred relations, and generated outcomes are calculated testimony, and every calculated witness identifies its analyzer identity and version, inputs, parameters and recipe, output relation and score domain, and execution receipt. A PGN result is recorded; an engine's blunder score is calculated. A calculated proxy never overwrites the literal outcome it estimates.
- **Out:** the record and calculate declarations of the recipe.
- **From:** `docs/specs/08_Record_vs_Calculate_Spec.txt`.

### 10.16 Materialize locally and qualify

- **In:** the recipe of 10.10 to 10.15 and the fixtures of [9. Sources](Sources.md).
- **Do:** run the recipe through the same native code the seed runs, locally, before any push: it materializes the exact rows, entities, claims, and masks the seed will write, so a reserved column name, an undeclared entity type, a missing gate entry, or an undeclared qualifier fails here. Prove identical output across every provider shape the format allows. Then run the invariance and coverage qualification of [9. Sources](Sources.md) operation 9.7.
- **Out:** a source recipe that is allowed to admit.
- **Check:** the recipe engine proved identical output across six provider shapes for one source; five pipeline failures in one session would have been caught by local materialization.
- **From:** `docs/plan/ASSIMILATION_ROADMAP.md` workstream J and commit `147dbc4c2`.

## What this stage leaves behind

For each format, a generic decomposer that is allowed to ingest any file of that format as normal digital content and recompose it byte for byte; and for each curated source, a semantic recipe that names its format, its witness, the disposition of every field, the shape of every set, the vocabulary every code lands on, the tier every claim attaches to, and which of its facts are recorded and which calculated. Users curate recipes, and Laplace produces them from ingesting models.

## Without this stage

A file of that format is a random binary blob, a source's fields fall silently into content, a set becomes a fan with no identity, and no two sources can ever say the same thing.
