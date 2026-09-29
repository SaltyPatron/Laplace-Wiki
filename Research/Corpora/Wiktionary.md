# Wiktionary

Wiktextract attests a written word in one language as one part of speech, and every edition of that extract is the same witness.

The composition is an entry: a written word, in one language, as one part of speech. The mask is that part of speech, and the entry's further statements (senses, forms, translations) are values on that entry. The witness is Wiktextract's output. Lineage is Wiktionary, trust 0.67, because the people who wrote the entries wrote them in Wiktionary, and the extract is derived from that. The extract is not a second publisher.

The recipe reads the latest raw edition held, 2026-08-28, under the refresh `Wiktionary` root. The source file says the older editions beside it are the same witness saying the same entries earlier. Measured, not loaded: 1,147,563,067 compositions from 24,537 MB. The kaikki.org English-language slice under `/vault/Data/Wiktionary` is the same witness and the same lineage, read after the Universal Dependencies documentation. Measured, not loaded: 85,893,026 compositions from 2,912 MB. Loading both as independent witnesses would count one Wiktionary entry twice.

The part of speech on an entry is Wiktionary's category for the headword. It is not the part-of-speech mask a treebank fills for a token. The language field hops to [ISO 639](ISO-639.md). A translation inside an entry is a hop to another language's entry, not an attestation by [Tatoeba](Tatoeba.md). Fanout is the number of senses and translations leaving the entry, capped by [Pull](../../Semantics/Pull.md).

## Files, breakdown, and caveats

Taken from the recipe files. A line in a block is a directive. The prose above it is that file's own account of what is read, what is not, and what a row becomes.

### `wiktionary/source`

The English Wiktionary as extracted by the program wiktextract: a JSON object on every line, one for each entry (a written word, in one language, as one part of speech). The file does not name itself inside; its name is raw-wiktextract-data, and the program's own documentation is titled "Wiktextract" and says it is "for extracing data from Wiktionary". The witness is the program's output; Wiktionary is what it derives from. Entering unrated, as tatoeba's recipe does for a source written by its users; the specification does not give one. The edition read is the latest one held (2026-08-28). The older editions beside it are the same witness saying the same entries earlier. Measured, not loaded: 1,147,563,067 compositions from 24,537 MB, at 750 bytes each with their indexes and standings.

```text
witness Wiktextract
lineage Wiktionary
trust 0.67
root $LAPLACE_DATA/.refresh-*/Wiktionary
```

### `wiktionary/wiktextract.recipe`

A JSON object on every line. Wiktextract's README, "Format of the extracted word entries": "Information returned for each word is a dictionary", of "a single word and part-of-speech", with   word - the word form;  pos - part-of-speech;  lang_code - Wiktionary language code;   etymology_number - "the number of the etymology under which this entry appeared" so an entry is the thing those members name together: [en, free, noun, 3]. A translation or a linked word holds "word", and "lang_code" when it is in another language: [fi, vapari]. A redirect holds "title" and no "word". A sense is the thing its glosses name ("glosses - list of gloss strings for the word sense"), a form the thing its "form" names, an example the thing its "text" names ("each example being a dictionary with text field containing the example text"). What a sense, a form, a translation or a linked word holds it says of its being there in the entry ("sense - optional sense indicating the meaning for which this is a translation"), not of the word alone. Lists of pairs are pairs ("links in the etymology as [display text, target] pairs"). Every key and value is recorded as written. The edition read is the dated one; the undated file beside it is the same witness saying the same entries earlier.

```text
match raw-wiktextract-data-*
grammar json
records
named word by lang_code word pos etymology_number
identity * title
identity senses glosses
identity forms form
identity examples text
specifics claims under senses
tuples
```

### `wiktionary-kaikki/kaikki.recipe`

The entries of one language, as kaikki.org gives them: the same JSON object on every line as in the raw file (see wiktextract.recipe for what Wiktextract's README says of it), and read the same way, so that what two editions say of the same entry, they say of the same thing. Here a sense also holds an "id" of its own (en-dictionary-en-noun-hIt8uVcE), which is said of the sense like everything else it holds.

```text
match kaikki.org-dictionary-*.jsonl
grammar json
records
named word by lang_code word pos etymology_number
identity * title
identity senses glosses
identity forms form
identity examples text
specifics claims under senses
tuples
```

### `wiktionary-kaikki/source`

The English Wiktionary's entries of one language, as kaikki.org gives them from the program wiktextract: a JSON object on every line, one for each entry (a written word, in one language, as one part of speech). The witness is the program's output, as for the raw file (wiktionary); Wiktionary is what it derives from. Entering unrated, as a source written by its users; the specification does not give one. Measured, not loaded: 85,893,026 compositions from 2,912 MB, at 750 bytes each with their indexes and standings.

```text
witness Wiktextract
lineage Wiktionary
trust 0.67
root $LAPLACE_DATA/Wiktionary
```
