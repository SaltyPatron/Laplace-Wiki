# NLTK

The Brown Corpus's tagged text is read by a declarative grammar that preserves paragraphs, sentences, words and aligned part-of-speech annotations.

## Source

The [brown](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/brown) source names one Brown Corpus witness and reads `c[a-z][0-9][0-9]` files under `$LAPLACE_DATA/Brown/brown`, after Unicode. Its [tagged.recipe](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/brown/tagged.recipe) uses the compiled `brown_tagged` grammar.

## Format

Blank lines separate paragraphs; newlines separate sentences; whitespace separates `word/tag` tokens. The final slash separates the word from its tag, so `and/or/CC` retains `and/or` as its word. This is the tagged-text structure documented by [NLTK's TaggedCorpusReader](https://www.nltk.org/api/nltk.corpus.reader.TaggedCorpusReader.html).

Words have canonical content identities. Sentence records retain the ordered word and tag layers, and the recipe attests the source's written POS annotations. It preserves the original tag spelling rather than silently translating Brown tags into UPOS.

## Not read

`cats.txt` and `CONTENTS` do not match the tagged-text recipe; their genre metadata is not currently attested. Local development acceptance uses a labeled format fixture because the raw Brown distribution is absent; recipe coverage does not claim a complete Brown ingest.
