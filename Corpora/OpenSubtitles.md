# OpenSubtitles

OpenSubtitles' sentence files are read as plain text and attest nothing: neither the language a file's name gives its sentences nor the pairing of line N in one file with line N in the other is recorded, because the recipe language has no way to say either.

The source is OpenSubtitles v2024 as OPUS packages it "in Moses format": for each pair of languages two files of plain text, one sentence on a line, and a README and a LICENSE. The README's first line is "Corpus Name: OpenSubtitles", and it says "This package is part of OPUS - the open collection of parallel corpora". OPUS's [data formats](https://opus.nlpl.eu/legacy/trac/wiki/DataFormats.html) page describes the Moses format: a plain-text bitext is two files whose corresponding lines are aligned, named with file extensions that correspond to the language ID. Only the Moses package is read; OPUS's XML, TMX, and alignment files are not among its files.

## Source

| Source | Witness | Trust | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `opensubtitles` | `OpenSubtitles`, lineage `OPUS` | trust 0.67 | `unicode`, `iso-639` | `OpenSubtitles.*`, `README`, `LICENSE` | [`sentences.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/opensubtitles/sentences.recipe), [`readme.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/opensubtitles/readme.recipe) |

The trust is "entering unrated, as tatoeba's recipe does for a source written by its users; the specification does not give one": the number is the recipe's choice, and [Corpora](README.md#not-settled) lists it among what stays missing. The witness and its lineage are named, though no claim is yet recorded under them.

## The sentences

A file such as `OpenSubtitles.en-ja.en` is sentences, one on a line, nothing else: no header, no column, no identifier.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| a line | one sentence | ordinary content, read as text: observed, as [Attestations](../Semantics/Attestations.md#observations) says of ordinary content | none | "Corpus Name: OpenSubtitles" (the README's first line) |
| the file's name after its last dot | `en` in `OpenSubtitles.en-ja.en`, `ja` in `OpenSubtitles.en-ja.ja` | not read: the language of the sentences is written only there, and the recipe language has no way to say it | none | the Moses files are named with "file extensions that correspond to the language ID" ([data formats](https://opus.nlpl.eu/legacy/trac/wiki/DataFormats.html)) |
| line N against line N of the paired file | the same line number in the other file | not read: nothing in the file says what line N of the other file is to line N of this one, and the recipe language has no way to say it | none | "corresponding lines are aligned" ([data formats](https://opus.nlpl.eu/legacy/trac/wiki/DataFormats.html)) |
| `README`, `LICENSE` | ordinary text | observed | none | |

[Attestations](../Semantics/Attestations.md#attestations) says a sentence from OpenSubtitles is attested to be English, or whichever language it is, and that OpenSubtitles gives the language of sentences, not of words. No recipe records that attestation yet.
