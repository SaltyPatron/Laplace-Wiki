# OpenSubtitles

OpenSubtitles attests, of each Japanese sentence of its English-Japanese pair, the English sentence on the same line of the other file, as built `[the Japanese sentence, en, the English sentence]`, at the sentence tier and of nothing inside it; both languages belong in the claim, and the Japanese side's own language is not yet recorded, and no other pair of languages is matched.

The source is OpenSubtitles v2024 as OPUS packages it "in Moses format": for each pair of languages two files of plain text, one sentence on a line, and a README and a LICENSE. The README's first line is "Corpus Name: OpenSubtitles", and it says "This package is part of OPUS - the open collection of parallel corpora". OPUS's [data formats](https://opus.nlpl.eu/legacy/trac/wiki/DataFormats.html) page describes the Moses format: a plain-text bitext is two files whose corresponding lines are aligned, named with file extensions that correspond to the language ID. Only the Moses package is read; OPUS's XML, TMX, and alignment files are not among its files.

## Source

| Source | Witness | Trust | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `opensubtitles` | `OpenSubtitles`, lineage `OPUS` | class `StructuredCorpus` | `unicode`, `iso-639` | `OpenSubtitles.en-ja.en`, `OpenSubtitles.en-ja.ja`, `README`, `LICENSE` | [`en.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/opensubtitles/en.recipe), [`ja.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/opensubtitles/ja.recipe), [`readme.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/opensubtitles/readme.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior is the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## The sentences

A file such as `OpenSubtitles.en-ja.en` is sentences, one on a line, nothing else: no header, no column, no identifier. Line N of `OpenSubtitles.en-ja.ja` is the same subtitle as line N of `OpenSubtitles.en-ja.en`, in the other language. What OpenSubtitles says is that this sentence was translated to that sentence, by one or more people, from one language to the other: the translation of the whole sentence, not of its words, so it is attested at the sentence tier, the highest the source asserts.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| a line of the `.en` file | one sentence | the English sentence, content, decomposed to its codepoints for its identity (`thing row en`, `content en`) | none of its own | "Corpus Name: OpenSubtitles" (the README's first line) |
| a line of the `.ja` file | one sentence | the Japanese sentence, content, the same way (`thing row ja`, `content ja`) | the subject of the pair | |
| line N against line N of the paired file | the same line number in the other file | how the two files are joined: the `.en` file numbers its lines (`numbered line`, `key row line`), and the `.ja` file's line N is read with the English sentence of the same number (`numbered en`, `refer en opensubtitles-en`). The line number is a position, written nowhere | as built `[the Japanese sentence, en, the English sentence]` (`attest row en`), with only one language where both belong | "corresponding lines are aligned" ([data formats](https://opus.nlpl.eu/legacy/trac/wiki/DataFormats.html)) |
| the file's name after its last dot | `en` in `OpenSubtitles.en-ja.en`, `ja` in `OpenSubtitles.en-ja.ja` | the language of the sentences, written only there. The English side's `en` is the name under which the pair is said; the Japanese side's `ja` is not recorded | in the pair, `en` only | the Moses files are named with "file extensions that correspond to the language ID" ([data formats](https://opus.nlpl.eu/legacy/trac/wiki/DataFormats.html)) |
| `README`, `LICENSE` | ordinary text | observed (`grammar text`) | none | |

Each line pair is one attestation, witnessed once by OpenSubtitles. Nothing is attested of the words inside a sentence: the source says nothing of them.

## Not yet recorded

- The Japanese sentence's own language. Both languages belong in what is attested, the language translated from and the language translated to; the shape of the claim that carries both is not yet decided.
- Any pair but English and Japanese: only `OpenSubtitles.en-ja.*` is matched.
- [Attestations](../Semantics/Attestations.md#attestations) says a sentence from OpenSubtitles is attested to be English, or whichever language it is, and that OpenSubtitles gives the language of sentences, not of words. That a sentence is in its language is not yet recorded of either side on its own.
