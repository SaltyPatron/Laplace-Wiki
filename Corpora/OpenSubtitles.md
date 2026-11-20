# OpenSubtitles

OpenSubtitles attests sentence-tier parallel translations (`[lang1, sent1, lang2, sent2]`) across aligned OPUS Moses bitext files for all admitted ISO 639 language pairs (11 language pairs currently wired in `recipes/opensubtitles/`, extensible to any ISO 639 pair), resolving aligned line numbers at ingest and recording them nowhere.

The source is OpenSubtitles v2024 as packaged by OPUS in Moses bitext format ([OPUS data formats](https://opus.nlpl.eu/legacy/trac/wiki/DataFormats.html)): for each language pair `<l1>-<l2>`, two plain-text files (`OpenSubtitles.<l1>-<l2>.<l1>` and `OpenSubtitles.<l1>-<l2>.<l2>`) whose corresponding lines are aligned subtitle translations, accompanied by `README` and `LICENSE`. Only one canonical representation (the Moses bitext) is needed; redundant XML/TMX packagings of the same sentences are not duplicated.

## Source

| Source | Witness | Trust class | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `opensubtitles` | `OpenSubtitles` source trunk, lineage `OPUS` | class `StructuredCorpus` | `unicode`, `iso-639` | `OpenSubtitles.<pair>.<lang>` across all locally extracted OPUS bitext directories (`ar-en`, `de-en`, `el-en`, `en-es`, `en-fr`, `en-hi`, `en-ja`, `en-ko`, `en-ru`, `en-zh_cn`, `en-zh_tw`, extensible to any ISO 639 pair), plus `README`, `LICENSE` | Pair recipes under [`recipes/opensubtitles/`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/opensubtitles) (`ar-en-*.recipe`, `de-en-*.recipe`, `el-en-*.recipe`, `en-es-*.recipe`, `en-fr-*.recipe`, `en-hi-*.recipe`, `en.recipe`/`ja.recipe`, `en-ko-*.recipe`, `en-ru-*.recipe`, `en-zh_cn-*.recipe`, `en-zh_tw-*.recipe`, `readme.recipe`) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior bounds the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## Parameterized OPUS bitext contract

Every OPUS Moses language pair obeys one uniform semantic contract:

1. Line `N` of `OpenSubtitles.<l1>-<l2>.<l1>` and line `N` of `OpenSubtitles.<l1>-<l2>.<l2>` are aligned subtitle sentences in ISO 639 languages `lang1` and `lang2` (including script/region distinctions such as `zh_cn` vs. `zh_tw` mapped onto their ISO 639 / BCP-47 highway identifiers).
2. Each sentence is decomposed losslessly to UAX #29 words, graphemes, and Tier-0 codepoints for its content `lp_id`, paired with its own ISO 639 language node (`[sent1, lang1]` and `[sent2, lang2]`, e.g., `thing sentence text literal ara` and `thing sentence text literal eng` in `ar-en`).
3. Line number `N` is pair-local alignment plumbing (`numbered line`, `key sentence line` / `refer aligned opensubtitles-<pair>-<l1>`), resolved in memory at ingest and **recorded nowhere**.
4. The aligned pair attests a symmetric sentence-tier translation strand binding both sentences and both languages (`[[sent2, lang2], translated, [sent1, lang1]]` / `[lang1, sent1, lang2, sent2]`) at the sentence tier—never claiming word-by-word alignment where the source asserts only whole-subtitle equivalence.

| Piece | Written as | Laplace reads it as | Target attestation & current recipe state | Specification |
| --- | --- | --- | --- | --- |
| line `N` of `OpenSubtitles.<pair>.<l1>` | one UTF-8 subtitle sentence | `[sent1, lang1]` sentence-in-language entity, keyed by pair-local line `N` (`key sentence line`) | first side of the aligned translation strand, with its ISO 639 language bound | "Corpus Name: OpenSubtitles" (`README`) |
| line `N` of `OpenSubtitles.<pair>.<l2>` | aligned UTF-8 subtitle sentence | `[sent2, lang2]` sentence-in-language entity, resolving line `N` via `refer aligned` | `[[sent2, lang2], translated, [sent1, lang1]]` across all 11 active pairs (`en.recipe`/`ja.recipe` is slated to match the two-language `literal jpn`/`literal eng` pattern used by the other 10 pairs, and parameterized pair matching generalizes to any newly staged OPUS directory without cloning two recipe files per pair) | "corresponding lines are aligned"; file extensions name the language ID ([OPUS data formats](https://opus.nlpl.eu/legacy/trac/wiki/DataFormats.html)) |
| line number `N` | implicit 1-based line ordinal | pair-local join key (`numbered`), discarded after resolution | none | Moses parallel line alignment |
| `README`, `LICENSE` | plain text | observed file content (`readme.recipe`) | none | |

## Relations

In `ar-en`, `de-en`, `el-en`, `en-es`, `en-fr`, `en-hi`, `en-ko`, `en-ru`, `en-zh_cn`, and `en-zh_tw`, the recipes already bind both ISO 639-3 language highway nodes (`ara`/`eng`, `deu`/`eng`, `ell`/`eng`, `spa`/`eng`, `fra`/`eng`, `hin`/`eng`, `kor`/`eng`, `rus`/`eng`, `cmn`/`zho`/`eng`) and attest `relation "translated"` rather than a file-extension field name. Unifying `en-ja` onto the same two-language strand and parameterizing OPUS pair discovery in the recipe loader lets any ISO 639 OPUS bitext snap in automatically.
