# OpenSubtitles

OpenSubtitles attests the language of a subtitle sentence and does not attest the language of a word.

The composition is a subtitle sentence. The mask is the language of that sentence, one sentence a line, in a language pair, Moses format, v2024. The value is the language of the line. Witness OpenSubtitles, lineage OPUS, trust 0.67, because the bitext is the OPUS release of OpenSubtitles. Root `/vault/Data/OpenSubtitles/extracted`. The zip files beside the extract are that release again.

[Attestations](../../Semantics/Attestations.md) uses this corpus as the example of the tier limit. The corpus supports the language of the sentence. It does not support the language of a word inside the sentence, and it does not support a sense or a dependency role. A hop to the paired sentence is a sentence-to-sentence link. Fanout is one: the other side of the pair. Promoting the language mark onto each token is the error the tier limit exists to stop.

## Files, breakdown, and caveats

Taken from the recipe files. A line in a block is a directive. The prose above it is that file's own account of what is read, what is not, and what a row becomes.

### `opensubtitles/readme.recipe`

The package's own README and LICENSE: ordinary text.

```text
match README LICENSE
grammar text
```

### `opensubtitles/sentences.recipe`

A file of sentences, one on a line, nothing else: no header, no column, no identifier. Ordinary content, read as text. The language of the sentences is written only in the file's name, after its last dot (OpenSubtitles.en-ja.en, OpenSubtitles.en-ja.ja), and nothing in the file says what line N of the other file is to line N of this one: neither is attested here, because the recipe language has no way to say either.

```text
match OpenSubtitles.*
grammar text
```

### `opensubtitles/source`

OpenSubtitles v2024 as OPUS packages it "in Moses format": for each pair of languages two files of plain text, one sentence on a line, and a README and a LICENSE. The README's first line: "Corpus Name: OpenSubtitles". The README: "This package is part of OPUS - the open collection of parallel corpora". Entering unrated, as tatoeba's recipe does for a source written by its users; the specification does not give one.

```text
witness OpenSubtitles
lineage OPUS
trust 0.67
root $LAPLACE_DATA/OpenSubtitles/extracted
```
