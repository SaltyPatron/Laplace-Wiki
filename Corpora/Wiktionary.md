# Wiktionary

Wiktextract attests a written word in one language as one part of speech, and every edition of that extract is the same witness.

## Format

| Record | Field | Order | Type | Specification |
| --- | --- | --- | --- | --- |
| word entry | word | JSON, unordered | string | The word form. One JSON object per line: one written word, in one language, as one part of speech. |
| word entry | lang | JSON, unordered | string | Name of the language this word belongs to (e.g., English). |
| word entry | pos | JSON, unordered | string | Part of speech, such as "noun", "verb", "adj", "adv", "pron", "determiner", "prep" (preposition), "postp" (postposition), and many others. The complete list of values returned by the package is wiktextract.PARTS_OF_SPEECH. This is Wiktionary's category for the headword, not a Universal Dependencies UPOS on a token, and not the part-of-speech mask in [Claims](../Semantics/Claims.md#masks). |
| word entry | senses | JSON, unordered | list of objects | List of word senses (dictionaries) for this word/part-of-speech. |
| sense | glosses | JSON, unordered | list of strings | List of gloss strings for the word sense (usually only one). This has been cleaned, and should be straightforward text with no tagging. |
| word entry | forms | JSON, unordered | list of objects | List of inflected or alternative forms specified for the word. Each dictionary has a form key and a tags key. It may also contain ipa, roman, and source. The form can be "-" when the word is marked as not having that form. |
| word entry | etymology_text | JSON, unordered | string | Etymology section as cleaned text. The contents of the whole etymology section cleaned into human-readable text. Etymological information is stored under etymology_text or etymology_texts. |
| word entry | etymology_texts | JSON, unordered | Not defined | Named as the other place etymological information is stored. The field list does not give etymology_texts its own sentence. |
| word entry | etymology_links | JSON, unordered | list of pairs | Links in the etymology as [display text, target] pairs, using the same format as sense links. |
| word entry | etymology_templates | JSON, unordered | list of objects | Templates and their arguments and expansions from the etymology section. Each object has name, args, and expansion. Certain common templates that do not signify etymological relations are not included. |
| word entry | etymology_number | JSON, unordered | string | For words with multiple numbered etymologies, the number of the etymology under which this entry appeared, as a string as of May 2026. |
| word entry or sense | translations | JSON, unordered | list of objects | Non-disambiguated translation entries on the word, or sense-disambiguated translation entries on the sense. Each dictionary has alt, code, english, lang, note, roman, sense, tags, taxonomic, and word, and possibly others. word is the translation in the specified language and may be missing when note is present. code is Wiktionary's 2- or 3-letter language code. lang is the language name that the translation is for. sense is a free-text string and may not match any gloss exactly. |

## Value

| Field | Composition | Mask | What is recorded | Lineage or hop | Specification |
| --- | --- | --- | --- | --- | --- |
| word | the word entry: one written word, one language, one part of speech | not a mask | the word form | Every edition of this extract is the same witness. | The word form. |
| lang | the word entry: one written word, one language, one part of speech | not a mask | the language name | Every edition of this extract is the same witness. | Name of the language this word belongs to. |
| pos | the word entry: one written word, one language, one part of speech | Wiktionary's category for the headword, not a Universal Dependencies UPOS | pos | Every edition of this extract is the same witness. | Part of speech as Wiktionary categorizes the headword. Not a Universal Dependencies UPOS on a token. |
| senses | the word entry: one written word, one language, one part of speech | not a mask | the sense dictionaries | Every edition of this extract is the same witness. | List of word senses for this word/part-of-speech. |
| glosses | a sense of that word entry | not a sense mask | the gloss strings | Every edition of this extract is the same witness. | List of gloss strings for the word sense (usually only one), cleaned to text with no tagging. |
| forms | the word entry: one written word, one language, one part of speech | not a mask | the inflected or alternative forms | Every edition of this extract is the same witness. | Each form object has form and tags, and may have ipa, roman, and source. The form can be "-". |
| etymology_text | the word entry: one written word, one language, one part of speech | not a mask | the cleaned etymology section | Every edition of this extract is the same witness. | Etymology section as cleaned text. When several parts of speech are listed under the same etymology, the same data is copied to each part-of-speech entry under that etymology. |
| etymology_texts | the word entry: one written word, one language, one part of speech | not a mask | Not defined | Every edition of this extract is the same witness. | Not defined beyond the name. The field list says etymological information is stored under etymology_text or etymology_texts. |
| etymology_links | the word entry: one written word, one language, one part of speech | not a mask | [display text, target] pairs | Every edition of this extract is the same witness. | Links in the etymology. The field is omitted when no links are found. |
| etymology_templates | the word entry: one written word, one language, one part of speech | not a mask | name, args, expansion | Every edition of this extract is the same witness. | Templates from the etymology section. args maps argument names to cleaned values. Positional arguments have keys that are numeric strings, starting with "1". expansion is the cleaned text the template expands to. |
| etymology_number | the word entry: one written word, one language, one part of speech | not a mask | the etymology number | Every edition of this extract is the same witness. | The number of the etymology under which this entry appeared, as a string as of May 2026. |
| translations | the word entry, or one sense of that entry | not a mask | the translation word in lang | Every edition of this extract is the same witness. | Stored on the word when not sense-disambiguated, and on the sense when sense-disambiguated. word may be missing when note is present. The translation sense string may not match any gloss exactly. |
