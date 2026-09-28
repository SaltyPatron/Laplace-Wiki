# Recipes

Research and measurements on how one generic decomposer can take any standardized file format apart into content and put it back together byte for byte.

Numbers marked measured come from prototype scripts on local files; everything else is from the sources.

## Grammars

A recipe first needs the format's structure: fields, chunks, repeats, and choices.

- [Kaitai Struct](https://kaitai.io/) describes binary formats declaratively. Its format library has 189 specifications, including BMP, PNG, GIF, JPEG, EXIF, WAV, RIFF, ID3, QuickTime (the box structure MP4 uses), ZIP, gzip, ELF, and Ogg. It handles repeats, switches, sub-streams, bit fields, and zlib, but it cannot express entropy decoding or LZW, cannot join a stream split across chunks (its PNG leaves the image data raw), and records none of an encoder's choices.
- [Tree-sitter](https://tree-sitter.github.io/) grammars describe code and markup. Every node records its byte range, and whitespace is the gap between tokens, so the tokens plus the stored gaps rebuild a source file exactly. The local collection has 303 grammars, including C, Python, JSON, HTML, Markdown, BibTeX, and LaTeX; the LaTeX grammar needs `tree-sitter generate` before use. TeX can change its category codes at runtime, so any fixed grammar only approximates it.
- UAX #29 is the grammar for plain text. See [Unicode](Unicode.md).

## Byte-exact recompression

Compressed payloads (deflate in PNG and ZIP, LZW in GIF, Huffman coding in JPEG and MP3) are the hard part. Stored compressed, they are opaque and never deduplicate; stored decoded, the exact file is lost. Published tools decode to meaningful content and keep a small record that reproduces the original bytes:

| Tool | Format | Stored content | Result |
| --- | --- | --- | --- |
| [Lepton](https://www.usenix.org/conference/nsdi17/technical-sessions/presentation/horn) | JPEG | DCT coefficients plus header, padding, and restart details | 77% of original size; 203 PiB processed at Dropbox by February 2017; refuses a file rather than lose data |
| packJPG | JPEG | coefficients | about 20% smaller |
| packMP3 | MP3 | spectral coefficients | about 16% smaller |
| [preflate](https://github.com/deus-libri/preflate) | deflate (PNG, ZIP, gzip) | decoded data plus a diff of the encoder's choices | bit-exact reconstruction |
| precomp | GIF, and deflate | decoded indices plus where codes differ | bit-exact reconstruction |

Formats with Huffman or arithmetic coding re-encode exactly from their decoded symbols. LZ-family formats (deflate, LZW) need the stored diff. For lossy codecs, pixels or samples cannot rebuild the exact bytes; every tool keeps the quantized coefficients as the stored content, and decoded pixels are derived from them. No open bit-exact tool was found for AAC, H.264, or AV1.

## PNG, measured

A prototype PNG recipe decomposed each file into a metadata tree (every chunk, the image data's split sizes, the zlib header, and each row's filter type) and a content tree with real Laplace IDs: channel value (a digit composition, so 255 is `[2,5,5]`) → pixel → row → image. It then recomposed each file by refiltering the rows, re-deflating with preflate's diff, and rebuilding the chunks and CRCs.

| Measure | Result |
| --- | --- |
| Files recomposed byte for byte | 26 of 26, in 13 s |
| Pixels | 2,899,069, of which 171,038 are distinct (5.9%) |
| Rows | 4,439, of which 3,746 are distinct |
| Distinct images | 24 of 26: two files are the same image |
| Reconstruction data | 89,884 bytes, 19.5% of all compressed image data |

Most images needed 8 to 200 bytes of reconstruction data; one large RGBA image needed 78,637 bytes, 21% of its compressed size. Plain zlib re-compression reproduced only 5 of the 26 files exactly.

## Code, measured

The PostgreSQL and CPython source trees were parsed with tree-sitter's C and Python grammars. Every syntax subtree became a content-addressed node: its ID is the hash of its children's IDs, with the gaps between children as text constituents, and the node's kind is not hashed.

| Measure | Result |
| --- | --- |
| Files | 5,976 (133 MB), in 93 s |
| Recomposed byte for byte | 5,976 of 5,976 |
| Distinct files | 5,911: 65 are exact duplicates of others |

| Subtree size | Subtrees | Distinct | New |
| --- | --- | --- | --- |
| 1–2 tokens | 1,050,115 | 86,276 | 8.2% |
| 3–8 | 4,756,239 | 1,612,129 | 33.9% |
| 9–32 | 2,106,468 | 1,460,665 | 69.3% |
| 33–128 | 351,273 | 324,539 | 92.4% |
| 129 or more | 173,388 | 170,001 | 98.0% |
| All | 8,437,483 | 3,653,610 | 43.3% |

331,616 distinct subtrees were given more than one node kind by the grammars, such as the same text parsed as an identifier in one place and as a type identifier in another. Hashing the kind would have split each of those into separate entities.

## Specifications

Collected locally: PNG (2nd and 3rd editions), RFC 1950, RFC 1951, and RFC 2083, GIF89a, ITU T.81 (JPEG), JFIF, EXIF 2.3 and the ExifTool tag table, BMP headers, WAVE, the MP3 frame header, ID3v2.3 and ID3v2.4, the MP4 box registry, the ZIP application note, FASTA, FASTQ, GenBank, GFF3, and TeX category codes. EXIF 3.0 and ISO 14496-12 (the MP4 box specification) were not obtained.

## Sources

- Daniel Reiter Horn et al. [The Design, Implementation, and Deployment of a System to Transparently Compress Hundreds of Petabytes of Image Files for a File-Storage Service](https://www.usenix.org/conference/nsdi17/technical-sessions/presentation/horn). NSDI 2017 (Lepton).
- [Kaitai Struct](https://kaitai.io/) and its [format gallery](https://formats.kaitai.io/).
- [Tree-sitter](https://tree-sitter.github.io/).
- [preflate](https://github.com/deus-libri/preflate) and [precomp](https://github.com/schnaader/precomp-cpp).
- W3C, [Portable Network Graphics (PNG) Specification, Third Edition](https://www.w3.org/TR/png-3/).
