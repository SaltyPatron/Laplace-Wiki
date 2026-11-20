# NLTK

The Brown Corpus attests paragraphs, sentences, words, and sentence-aligned Brown part-of-speech annotations crosswalked to `upos`, together with `cats.txt` and `CONTENTS` document-to-genre classifications under one corpus witness trunk.

## Source

| Source | Witness | Trust class | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `brown` | `Brown Corpus` source trunk | class `AcademicCurated` | `unicode`, `iso-639` | `c[a-z][0-9][0-9]`, plus `cats.txt` and `CONTENTS` under `$LAPLACE_DATA/Brown/brown` | [`tagged.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/brown/tagged.recipe) (`cats.txt` and `CONTENTS` genre recipes queued for `Batch 2`) |

## Tagged text (`c[a-z][0-9][0-9]`) & genre catalogs (`cats.txt`, `CONTENTS`)

[`tagged.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/brown/tagged.recipe) parses the 500 Brown Corpus documents (`ca01`..`cr09`) with the compiled `brown_tagged` grammar ([NLTK `TaggedCorpusReader`](https://www.nltk.org/api/nltk.corpus.reader.TaggedCorpusReader.html)): blank lines separate paragraphs, newlines separate sentences, whitespace separates `word/tag` tokens, and the final `/` splits the word from its tag so `and/or/CC` retains `and/or` as its canonical word entity.

Each Brown POS tag (`nn-tl`, `vbd`, `jj`, 472 tags in `manifest/slots/brown.tsv`) retains its exact fine-grained Brown tag identity while reaching Universal Dependencies' `upos` bank (`5` bits at offset `8`) through the frozen NLTK universal tagset crosswalk in `manifest/slots/edges-tagsets.tsv` (`type ... upos crosswalk brown`, [Types](../Reference/Types.md#perf-caches)), preserving both empirical token POS counts and sentence-aligned POS layer trajectories.

Alongside the 500 tagged files, `cats.txt` (mapping each `ca01`..`cr09` file ID to its genre category such as `news`, `editorial`, `reviews`, `religion`, `hobbies`, `lore`, `belles_lettres`, `government`, `learned`, `fiction`, `mystery`, `science_fiction`, `adventure`, `romance`, `humor`) and `CONTENTS` (bibliographic source titles, authors, and genre hierarchy) bind each document's file trunk (`refer` by file stem `ca01`, discarding the bare `ca01` pointer where resolved) to its genre and bibliographic provenance (`Batch 2` recipe gap: `cats.txt` and `CONTENTS` do not yet have recipes under `recipes/brown/`).

| Piece | Written as | Laplace reads it as | Target attestation & current recipe state |
| --- | --- | --- | --- |
| `c[a-z][0-9][0-9]` paragraph / sentence / `word/tag` | `The/at Fulton/np-tl County/nn-tl ...` | paragraph → sentence → word trajectory + aligned Brown POS layer crosswalked via `brown` → `upos` | empirical `[word, brown_tag]` → `upos` series + sentence POS layer (`tagged.recipe` active) |
| `cats.txt` (`file_id category`) | `ca01 news` | `ca01` resolved (`refer`) to document trunk `ca01`; genre category attested of that document | target: `[doc_trunk, genre, news]` (`Batch 2` gap: `cats.txt` recipe queued) |
| `CONTENTS` | section headings & per-file bibliographic citations | genre taxonomy and source publication provenance on each `c[a-z][0-9][0-9]` document | target: document bibliographic provenance (`Batch 2` gap: `CONTENTS` recipe queued) |
