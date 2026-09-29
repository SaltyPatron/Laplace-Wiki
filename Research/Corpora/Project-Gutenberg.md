# Project Gutenberg

Project Gutenberg's texts are observed content and attest nothing.

The composition is the text of a work, read from `/vault/Data/ProjectGutenberg/text`. Loaded measure: 2,791,039 compositions from 208 MB. There is no witness line. The recipe says the books are ordinary content: they are observed, and they attest nothing. A novel that contains the word dog does not attest the sense of dog, the part of speech of a token, or a dependency role.

[Engine Measurements](../Engine.md) uses these texts as the corpus the storage layer was timed on. That use observes the bytes. It does not promote the books into witnesses. There is no hop from a Gutenberg sentence into a wordnet except a hop some other witness supplies. Fanout does not arise, because there is no relation being attested.

## Files, breakdown, and caveats

Taken from the recipe files. A line in a block is a directive. The prose above it is that file's own account of what is read, what is not, and what a row becomes.

### `project-gutenberg/source`

Books from Project Gutenberg, as plain text. Ordinary content: it is observed, and attests nothing. Measured when it was loaded: 2,791,039 compositions from 208 MB, at 750 bytes each with their indexes and standings.

```text
root $LAPLACE_DATA/ProjectGutenberg/text
reads text
```
