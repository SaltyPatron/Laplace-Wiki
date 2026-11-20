# Wiktionary

Wiktextract's extract of Wiktionary attests multilingual lexical entries (`[lang_code, word, pos]`), word senses, inflected forms, IPA pronunciations, etymologies, semantic linkages, translations, `topics` and `categories` domain labels, and shared `wikidata` QID highway crosswalks (`Q23622`), whether read from the raw dump or kaikki.org's per-language files.

The program [wiktextract](https://github.com/tatuylonen/wiktextract) emits one JSON object per lexical entry. Two sources read that output under the same witness (`Wiktextract`, lineage `Wiktionary`) and shared recipe logic so identical entries across the full dump and [kaikki.org](https://kaikki.org/dictionary/) per-language extracts collide on the exact same entities.

## Sources

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `wiktionary` | `Wiktextract`, lineage `Wiktionary` | class `UserCuratedResource` | `unicode`, `iso-639` | `raw-wiktextract-data-*` (newest dated edition) | [`wiktextract.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wiktionary/wiktextract.recipe) |
| `wiktionary-kaikki` | `Wiktextract`, lineage `Wiktionary` | class `UserCuratedResource` | `unicode`, `iso-639`, `universal-dependencies-documentation` | `kaikki.org-dictionary-*.jsonl` | [`kaikki.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wiktionary-kaikki/kaikki.recipe) |

Copies of one lineage play one matchup series per claim ([30. Conflicts](../Sequence/Conflicts.md) C4, I6). Undated duplicate aliases and superseded snapshots alongside the newest dated dump are skipped so one release is admitted cleanly.

## The entry

Each JSON line is one entry for one written `word` in one `lang_code` and `pos` (`[en, free, noun]`), witnessed together as one record. Two Recording Law rules govern identifier and domain fields inside entries and senses:

- **`wikidata` QIDs (`Q23622`) are shared highway nodes, NEVER `omit`ted:** Unlike Wiktextract's internal `id` (`en-dictionary-en-noun-hIt8uVcE`) and `senseid` strings—which are extractor-local pointers omitted at ingest—a `wikidata` identifier (`Q23622`, `Q937`) is a universal content highway ID ([30. Conflicts](../Sequence/Conflicts.md) S1, I5) that directly cross-braces Wiktionary entries and senses with Wikidata, Wikipedia, ConceptNet, and [Natural Earth](Natural-Earth.md) on the exact same `lp_id` (`Batch 2` recipe gap: `kaikki.recipe` currently lists `wikidata` on its `omit` line and must retain and attest it).
- **`topics` and `categories` supply domain and subject attestations:** Entry- and sense-level `topics` (`"physics"`, `"medicine"`, `"law"`) and `categories` attest domain and taxonomic membership, whereas MediaWiki template expansion ASTs (`head_templates`, `etymology_templates`, `inflection_templates`, `info_templates`), disambiguation weights (`_dis`, `_dis1`), and character highlight offsets (`bold_*_offsets`, `italic_text_offsets`) are rendering packaging (`Batch 2` recipe gap: `kaikki.recipe` currently omits `topics` and `categories` alongside template machinery).

| Piece | Written as | Laplace reads it as | Target attestation & current recipe state | Specification |
| --- | --- | --- | --- | --- |
| `lang_code`, `word`, `pos` | `"en"`, `"free"`, `"noun"` | canonical entry composition `[lang_code, word, pos]` (`thing record lang_code word pos`) | subject `[en, free, noun]` | "word - the word form"; "pos - part-of-speech"; "lang_code - Wiktionary language code" |
| `senses` & `glosses` | list of sense dicts with `glosses` | each sense composed from its `glosses` (`thing senses glosses`), held by the entry (`relation "word sense" senses`) | `[entry, word sense, sense]` | "senses - list of word senses (dictionaries) for this word/part-of-speech" |
| `wikidata` (on entry or sense) | `"Q23622"` | **shared Wikidata highway node** (`[Q, 2, 3, 6, 2, 2]`), bridging Wiktionary ↔ Wikidata ↔ Wikipedia ↔ Natural Earth | target: `[sense_or_entry, Wikidata item, Q23622]` (`Batch 2` recipe gap: `kaikki.recipe` currently `omit`s `wikidata`—must be retained as highway content!) | Wikidata QID linked to the Wiktionary entry or sense |
| `wikipedia`, `wiktionary` | page title strings | cross-project encyclopedic links | `[sense_or_entry, Wikipedia page title, title]` | "wikipedia - list of Wikipedia page titles" |
| `topics`, `categories` | lists of domain and category strings | domain and taxonomic subject attestations on the entry or sense | target: `[sense_or_entry, topic/category, value]` (`Batch 2` recipe gap: `kaikki.recipe` currently `omit`s `topics` and `categories`) | Wiktionary topical domain labels and categories |
| `id`, `senseid`, `etymology_number` | `en-dictionary-en-noun-hIt8uVcE`, `3` | extractor-local sense keys and page-layout numbering (`omit`) | none | internal Wiktextract/page pointers |
| `forms` | dicts with `form`, `tags`, `ipa`, `roman` | inflected or alternative word forms (`thing forms form`) | `[entry, inflected or alternative form, form]` with `tags`/`roman` qualifiers | "forms - list of inflected or alternative forms" |
| `sounds` | dicts with `ipa`, `enpr`, `audio-ipa`, `tags` | pronunciation objects (`thing sounds ipa` / `enpr` / `audio-ipa`, `together sounds`) | `[entry, pronunciation, ipa]` | Wiktextract "Pronunciation" section |
| `translations` | dicts with `lang_code`, `word`, `sense`, `roman`, `tags` | `[lang_code, word]` lexical targets on the entry or sense | `[entry_or_sense, translation, [fi, vapari]]` | "translations - translation entries" |
| `synonyms`, `antonyms`, `hypernyms`, `hyponyms`, `holonyms`, `meronyms`, `troponyms`, `instances`, `derived`, `related`, `coordinate_terms`, `descendants`, `alt_of`, `form_of` | linkage dicts with `word` (and optional `lang_code`, `sense`, `tags`) | semantic and morphological linkage strands under their documented relations | `[entry_or_sense, synonym, target]`, `[entry_or_sense, more specific term, target]`, etc. | Wiktextract "Linkages to other words" & Wiktionary semantic relations |
| `examples` | dicts with `text`, `english`/`translation`, `roman`, `type` | usage examples (`thing examples text`) | `[sense, usage example, text]` | "examples - list of usage examples" |
| `etymology_text`, `etymology_links` | cleaned etymology prose and `[display, target]` pairs | etymological provenance on the entry | `[entry, etymology section, text]` | Wiktextract "Etymologies" |
| `title` + `redirect` (no `word`) | redirect object | redirect page (`thing redirect title`) | `[title, redirects to, target]` | redirect entry |
| `head_templates`, `etymology_templates`, `inflection_templates`, `info_templates`, `_dis`, `_dis1`, `bold_*_offsets`, `italic_text_offsets`, `*_url`, `code` | template expansion trees, disambiguation floats, byte offsets, media URLs, redundant `code` | MediaWiki/extractor packaging (`omit`) | none | rendering and extraction bookkeeping |
| `null`, `""`, `[]` | empty | attests nothing | none | |

## Relations

`kaikki.recipe` already maps Wiktionary's core lexical, morphological, phonetic, and semantic-linkage fields (`word sense`, `inflected or alternative form`, `translation`, `synonym`, `antonym`, `hypernym`, `more specific term`, `having a part`, `usage example`, `pronunciation`, `Wikipedia page title`, `qualifier of this form or sense`) onto documented semantic relations rather than raw JSON keys. Closing the `Batch 2` gaps restores `wikidata` QIDs as highway crosswalks, restores `topics` and `categories` as domain attestations, and resolves remaining unworded linkage keys (`proverbs`, `abbreviations`, `compound_of`, `homophones`, `rhymes`).
