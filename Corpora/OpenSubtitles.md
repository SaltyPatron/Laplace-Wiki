# OpenSubtitles

OpenSubtitles attests the language of a subtitle sentence and does not attest the language of a word.

## Value

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| language ID | The name follows the typical name conventions used in Moses, i.e. using file extensions that correspond to the language ID. Plain text files contain 2 files in which corresponding lines are aligned with each other. The files are untokenized, and they may contain multiple sentences per line in case they are aligned together. Empty alignments are excluded. All plain text files are encoded in Unicode UTF-8. | a line of the Moses file | the file extension | OPUS | [OPUS Data Formats, Plain Text / Moses](https://opus.nlpl.eu/legacy/trac/wiki/DataFormats.html) |
| language of a word | Not defined. The Plain Text / Moses section defines the language ID of the file and says what a line is. It does not define the language of a word. [Attestations](../Semantics/Attestations.md) | a word | Not defined | OPUS | [OPUS Data Formats, Plain Text / Moses](https://opus.nlpl.eu/legacy/trac/wiki/DataFormats.html); [Attestations](../Semantics/Attestations.md) |

## Format

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| Moses line | one line of plain text; the language ID is the filename extension, not a column | One line of an OPUS plain-text bitext file. Corresponding lines of the two files are aligned. The line may contain multiple sentences. This drop's extracted pair is OpenSubtitles.en-ja.en and OpenSubtitles.en-ja.ja. | [OPUS Data Formats, Plain Text / Moses](https://opus.nlpl.eu/legacy/trac/wiki/DataFormats.html) |
