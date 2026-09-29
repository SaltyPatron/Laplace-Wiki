# 7. Recipes

Before a format can be ingested, its recipe says how the generic decomposer takes a file apart into content and puts it back byte for byte.

Literally any standardized or fixed-format file is a modality to Laplace, and Laplace treats them all exactly the same: a generic decomposer uses a recipe to tell it how to extract the content. Plain text's recipe is UAX #29. Every other format's recipe is written before the first file of that format is ingested.

## Before this stage

[1. Unicode](Unicode.md): the segmentation data. [3. Builds](Builds.md): the decomposer and the grammars. [5. Tier 0](Tier-0.md): the atoms every decomposition bottoms out in.

## Operations, per format

### 7.1 Obtain the format's specification

- **In:** the format.
- **Do:** a recipe first needs the format's structure: fields, chunks, repeats, and choices. That comes from the format's own specification. Collected so far: PNG, RFC 1950, 1951, and 2083, GIF89a, ITU T.81 (JPEG), JFIF, EXIF 2.3 and the ExifTool tag table, BMP headers, WAVE, the MP3 frame header, ID3v2.3 and ID3v2.4, the MP4 box registry, the ZIP application note, FASTA, FASTQ, GenBank, GFF3, and TeX category codes.
- **Out:** the structure the recipe will follow.
- **From:** [Research: Recipes: Specifications](../Research/Recipes.md#specifications).

### 7.2 Choose the grammar

- **In:** the specification of 7.1.
- **Do:** one of three:
  - **Plain text:** UAX #29. Extended grapheme clusters by rules GB1–GB999, words by WB1–WB999, sentences by SB1–SB998. Letters, numbers, Katakana, and ExtendNumLet glue into runs; WB999 breaks everywhere else, so by default every punctuation mark and every Han ideograph is its own segment. Sentence rules are heuristic, and abbreviations such as "Mr." need CLDR suppressions. Scripts written without spaces, such as Thai or Chinese, need tailoring; ICU implements dictionary-based breaking for Thai, Lao, Khmer, Myanmar, and CJK. The rules are defined on NFD but can be applied directly to non-NFD text with equivalent results, so segmenting does not require normalizing.
  - **Binary formats:** a declarative structure such as Kaitai Struct's, whose format library has 189 specifications including BMP, PNG, GIF, JPEG, EXIF, WAV, RIFF, ID3, the QuickTime box structure, ZIP, gzip, ELF, and Ogg, handling repeats, switches, sub-streams, bit fields, and zlib.
  - **Code and markup:** a tree-sitter grammar. Every node records its byte range, and whitespace is the gap between tokens, so the tokens plus the stored gaps rebuild a source file exactly. The local collection has 303 grammars.
- **Out:** the grammar the decomposer parses with.
- **From:** [Compositions: Segmentation](../Storage/Compositions.md#segmentation), [Research: Unicode: Text segmentation](../Research/Unicode.md#text-segmentation-uax-29), [Research: Recipes: Grammars](../Research/Recipes.md#grammars).

### 7.3 Write the trunk: metadata and content

- **In:** the structure of 7.1.
- **Do:** a file has a trunk, with children for the file's metadata and for the file's content: EXIF data, headers, and so on. Every standardized file, such as `something.txt`, `audio.mp3`, or `image.bmp`, branches into its own trees. The recipe says which parts are metadata and which are content, and which tree each goes in.
- **Out:** the shape of the file's trunk.
- **From:** [Compositions: Files](../Storage/Compositions.md#files).

### 7.4 Write the tiers of the content tree

- **In:** the grammar of 7.2.
- **Do:** the recipe says how the content breaks down to codepoints, tier by tier. For text: codepoint ↔ grapheme ↔ word ↔ sentence ↔ document ↔ file, with paragraphs, titles, and the various separators besides, including dedicated separator codepoints, some of them language-specific. For an image: codepoint → digit → number → intensity → channel → pixel → patch → region → image. Numbers are compositions of codepoints: `[2,5,5]`. A value gets a type only when it is put into a composition, so the same `[2,5,5]` serves as a pixel channel intensity, a raw byte value, and an IP segment. Nothing is dropped: whitespace and punctuation are constituents like everything else. For code, every syntax subtree becomes a node whose ID is the hash of its children's IDs, with the gaps between children as text constituents; the node's kind is not hashed, because 331,616 distinct subtrees were given more than one kind by the grammars and hashing the kind would have split each into separate entities.
- **Out:** the decomposition of a file of this format into a Merkle DAG.
- **From:** [Compositions: Tiers](../Storage/Compositions.md#tiers), [Compositions: Types](../Storage/Compositions.md#types), [Compositions: Segmentation](../Storage/Compositions.md#segmentation), [Research: Recipes: Code, measured](../Research/Recipes.md#code-measured).

### 7.5 Write the repeats

- **In:** the tiers of 7.4.
- **Do:** repeats are not recorded one by one. An all-white image does not record a billion white pixels: the white pixel is one entity, and repeats are run-length encoded, with the run length in the vertex's M. Pixels, patches, and regions are finite in space, while large, and deduplicate heavily. Deduplicating two-dimensional structure at the highest tier, as a quadtree down to 8×8 patches with pixel values packed 8 per vertex, cut 26 PNGs' storage from 98.5 times the files to 11.2 times.
- **Out:** the run-length rule for this format.
- **From:** [Compositions: Repeats](../Storage/Compositions.md#repeats), [Physicality: Physicality](../Storage/Physicality.md#physicality), [Research: Recipes: Storage, measured](../Research/Recipes.md#storage-measured).

### 7.6 Write what gets reproducibility

- **In:** the specification of 7.1.
- **Do:** recipes denote how content is recorded, what content is recorded, what gets reproducibility, and what does not matter. Compressed payloads are the hard part: stored compressed they are opaque and never deduplicate; stored decoded the exact file is lost. The recipe stores the decoded content and a small record that reproduces the original bytes. Formats with Huffman or arithmetic coding re-encode exactly from their decoded symbols; LZ-family formats, deflate and LZW, need a stored diff of the encoder's choices, as preflate and precomp keep. For lossy codecs, the quantized coefficients are the stored content and decoded pixels are derived from them. Encrypted content has no value to Laplace: it is random binary blob storage.
- **Out:** the reconstruction record for this format.
- **Check:** the PNG recipe recomposed 26 of 26 files byte for byte, refiltering the rows, re-deflating with preflate's diff, and rebuilding the chunks and CRCs; its reconstruction data was 89,884 bytes, 19.5% of all compressed image data, most images needing 8 to 200 bytes. Plain zlib re-compression reproduced only 5 of the 26.
- **From:** [Ingestion: Recipes](../Storage/Ingestion.md#recipes), [Research: Recipes: Byte-exact recompression](../Research/Recipes.md#byte-exact-recompression), [Research: Recipes: PNG, measured](../Research/Recipes.md#png-measured).

### 7.7 Prove the recipe round-trips

- **In:** files of the format.
- **Do:** decompose each file with the recipe and recompose it from the DAG.
- **Out:** a recipe that is allowed to ingest.
- **Check:** byte for byte, every file. Text: 195 of 195 Gutenberg texts. PNG: 26 of 26. Code: 5,976 of 5,976 PostgreSQL and CPython source files.
- **From:** [Research: Prototype: Ingestion](../Research/Prototype.md#ingestion), [Research: Recipes: PNG, measured](../Research/Recipes.md#png-measured), [Research: Recipes: Code, measured](../Research/Recipes.md#code-measured).

## What this stage leaves behind

For each format, a recipe the generic decomposer runs: the decomposition of a file into a Merkle DAG and its recomposition byte for byte. The decomposer and the ingestion pipeline are optimized to the limit and powered by these recipes.

## Without this stage

A file of that format is a random binary blob, and nothing in it is content. No file of a format can be ingested before its recipe exists.
