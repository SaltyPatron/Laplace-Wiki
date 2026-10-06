# Wiktionary

Wiktextract's extract of the English Wiktionary attests, entry by entry, what Wiktionary says of a written word in one language as one part of speech, whether read from the raw extract or from kaikki.org's file for one language, and a member that is null or empty attests nothing.

The program [wiktextract](https://github.com/tatuylonen/wiktextract) writes a JSON object on every line, one for each entry. Two sources read that output: the raw file, and the per-language files [kaikki.org](https://kaikki.org/dictionary/) makes from it. Both are the same witness, `Wiktextract`, with `Wiktionary` as its lineage, and both are read by the same recipe, so that what two editions say of the same entry, they say of the same thing.

## Sources

| Source | Witness | Trust | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `wiktionary` | `Wiktextract`, lineage `Wiktionary` | class `UserCuratedResource` | `unicode`, `iso-639` | `raw-wiktextract-data-*`, the newest edition held | [`wiktextract.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wiktionary/wiktextract.recipe) |
| `wiktionary-kaikki` | `Wiktextract`, lineage `Wiktionary` | class `UserCuratedResource` | `unicode`, `iso-639`, `universal-dependencies-documentation` | `kaikki.org-dictionary-*.jsonl` | [`kaikki.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wiktionary-kaikki/kaikki.recipe) |

The witness is the program's output, as its own documentation is titled "Wiktextract" and says it is "for extracing data from Wiktionary"; Wiktionary is what it derives from, so copies of the one lineage play one matchup per claim. The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior is the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source. The raw file read is the dated one; the undated file beside it, and the older editions, are the same witness saying the same entries earlier, and are not read.

## The entry

A record is one line: one JSON object, one entry. Wiktextract's README, "Format of the extracted word entries", says "Information returned for each word is a dictionary", of "a single word and part-of-speech". Every key and value is recorded as written; a claim is the path from a thing to a value, and a list says each of its values under the same key.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `word`, `lang_code`, `pos` | `"word": "free"`, `"lang_code": "en"`, `"pos": "noun"` | name the entry together, in the order `lang_code`, `word`, `pos`: the entry is the path of those it holds, `[en, free, noun]`, one thing however many etymologies the page gives it | the subject, `[en, free, noun]` | "word - the word form"; "pos - part-of-speech"; "lang_code - Wiktionary language code" |
| `etymology_number` | `"etymology_number": 3` | where on the page the entry appeared: bookkeeping, read by nothing (`omit`) | nothing | "etymology_number - the number of the etymology under which this entry appeared" |
| `lang`, `etymology_text`, and any other member holding a text or a number | `"lang": "English"` | said of the entry under its key | `[entry, lang, English]` | "lang - name of the language this word belongs to" |
| `senses` | a list of objects | each sense is the thing its `glosses` name; the sense's place in the entry is a claim, and what the sense holds are claims of their own, said of its being there | `[entry, senses, sense]`; `[[entry, senses, sense], tags, value]` | "senses - list of word senses (dictionaries) for this word/part-of-speech" |
| `glosses` | a list of strings inside a sense | names the sense: one gloss is the sense, several are the path of them | the sense | "glosses - list of gloss strings for the word sense (usually only one)" |
| `id`, `senseid`, `wikidata` inside a sense | `en-dictionary-en-noun-hIt8uVcE`, `Q23622` | how the extract and Wikidata point at the sense: `omit`, read by nothing | nothing | |
| `examples` | a list of objects inside a sense | each example is the thing its `text` names; its place in the sense is the claim, and its other members are that claim's specifics: recorded with it as what is witnessed, no claim of their own | `[[entry, senses, sense], examples, text]` | "each example being a dictionary with text field containing the example text" |
| `forms` | a list of objects with `form` and `tags` | each form is the thing its `form` names; its place in the entry is the claim, and its other members are the claim's specifics | `[entry, forms, form]`, with `[tags, value]` among its specifics | "forms - list of inflected or alternative forms specified for the word"; "Each dictionary has a form key and a tags key. It may also contain ipa, roman, and source." |
| `translations` | a list of objects on the entry or on a sense, each holding `word` | each is the thing its `lang_code` and `word` name together, and `pos` when it holds it; its place, in the entry or in the sense, is the claim, and its other members are the claim's specifics | `[entry, translations, [fi, vapari]]`; `[[entry, senses, sense], translations, [fi, vapari]]` | "sense - optional sense indicating the meaning for which this is a translation" |
| any other object holding `word`, such as a linked word | an object inside the entry or a sense | the thing those members name together, the same way; what it holds it says of its being there | `[entry, key, [lang_code, word]]` | |
| `etymology_links`, and any list of pairs | `[[display text, target], ...]` | each inner list of plain values is one tuple, said under the key | `[entry, etymology_links, [display text, target]]` | "links in the etymology as [display text, target] pairs" |
| `etymology_templates`, `head_templates`, `inflection_templates`, `categories`, `topics`, `source`, the `_dis` and `*_offsets` members | objects with `name`, `args`, `expansion` | bookkeeping: `omit`, read by nothing | nothing | "Each object has name, args, and expansion." |
| `title` | on an object that holds no `word` | names the thing: a redirect | the subject; what the object holds is said of it under its key | a redirect holds `title` and no `word` |
| `null`, an empty text | | nothing | none | |

Everything one entry says it says together: it is one record, witnessed once, and its claims within it; a claim said twice in one record is witnessed in it once. A sense, a form, a translation, or a linked word says what it holds of its being there in the entry, not of the word alone.

## Relations

As built, the relation of a claim above is the JSON key that holds its value, `[entry, senses, sense]`, `[entry, forms, form]`, `[entry, translations, [fi, vapari]]`, `[entry, lang, English]`: markup, not meaning. A relation is what the source means, never the name of a field, [10. Recipes](../Sequence/Recipes.md#1011-disposition-every-recovered-field). The target for each key is what Wiktextract's README documents it to mean, quoted in the Specification column: a sense of the word and part of speech, an inflected or alternative form, a translation for a sense, the name of the language; a key it does not document is an explicit unresolved obligation. `pos` is a value of Wiktextract's part-of-speech list, with its attested equivalence to the shared vocabulary.
