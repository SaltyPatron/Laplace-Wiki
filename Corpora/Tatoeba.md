# Tatoeba

Tatoeba attests what it and its members say of a whole sentence, which is its text: its language, owner, translations, tags, audio, transcriptions and reviews; a sentence's id is Tatoeba's internal pointer to it, recorded nowhere, by which the other files point at the sentence; and nothing is attested of the words inside it.

One source, `tatoeba`, reads Tatoeba's weekly tab-separated exports ([Download sentences](https://tatoeba.org/en/downloads), "Fields and structure") under one `Tatoeba` corpus witness trunk.

## Source

| Source | Witness | Trust class | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `tatoeba` | `Tatoeba` source trunk | class `UserCuratedResource` | `iso-639`, `wiktionary`, `conceptnet` | Nine exported CSV/TSV tables + associated Tatoeba spoken audio recordings (`Batch 2`, `Laplace#1134`) | [`recipes/tatoeba/`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/tatoeba) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior bounds the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## The record

Each row is tab-separated with `\` escapes and `\N` for empty/unknown fields. Every sentence is its decoded UTF-8 `Text`, keyed by `Sentence id` (`key row "Sentence id"`) so companion tables resolve `Sentence id` directly to that sentence entity (`refer "Sentence id" tatoeba-sentences-detailed tatoeba-sentences tatoeba-sentences-cc0`) and record the numeric ID nowhere. Community contributors (`Username`) are participant content inside Tatoeba's records, never separate corpus witnesses ([30. Conflicts](../Sequence/Conflicts.md) I3).

Two Recording Law rules govern timestamps and multi-modal spoken audio:

- **Timestamp bookkeeping is omitted (`omit`)**: `Date added` and `Date last modified` in `sentences_CC0.csv`, `sentences_detailed.csv`, and `users_sentences.csv` are export-database timestamps (`omit "Date last modified"`, `omit "Date added"`), never semantic claims on a sentence.
- **Multi-modal spoken audio linkage (`sentences_with_audio.csv`, `Batch 2` `Laplace#1134`)**: `sentences_with_audio.csv` links each spoken `Sentence id` via `Audio id` to its actual Tatoeba audio recording (`<audio_id>.mp3`/`.opus`/`.wav` decomposed into its lossless audio trajectory trunk `audio_track`), attesting the grounded multi-modal tuple `[sentence, audio_track, speaker, license]` (with `Attribution URL` where required by CC-BY) while resolving and discarding the numeric `Audio id` pointer (`Batch 2` gap: `sentences-with-audio.recipe` currently attests `[sentence, who recorded the audio, Username]` and keys `Audio id` locally until Tatoeba audio streams are admitted alongside it in `Laplace#1134`).

| File | Fields | Laplace reads it as | Target attestation & current recipe state |
| --- | --- | --- | --- |
| `sentences.csv` | `Sentence id`; `Lang`; `Text` | canonical sentence `Text`, keyed by `Sentence id`; `Lang` resolved onto ISO 639-3 highway node | `[sentence, ISO 639-3 language code, eng]` |
| `sentences_CC0.csv` | `Sentence id`; `Lang`; `Text`; `Date last modified` | same as `sentences.csv`, with `Date last modified` omitted (`omit "Date last modified"`) | `[sentence, ISO 639-3 language code, eng]` (zero timestamp claims) |
| `sentences_detailed.csv` | `Sentence id`; `Lang`; `Text`; `Username`; `Date added`; `Date last modified` | sentence `Text`, language `Lang`, contributor `Username` as participant content, and both dates omitted (`omit`) | `[sentence, ISO 639-3 language code, eng]` + author relation `[sentence, owner, Username]` |
| `links.csv` | `Sentence id`; `Translation id` | both IDs resolved via `refer` to their sentences | sentence-tier translation strand `[sentence_a, translated, sentence_b]` (with zero `"Translation id"` column name in the claim) |
| `tags.csv` | `Sentence id`; `Tag name` | resolved sentence and Tatoeba tag (`proverb`, `idiom`, ...) | `[sentence, tag, proverb]` |
| `sentences_with_audio.csv` | `Sentence id`; `Audio id`; `Username`; `License`; `Attribution URL` | `Sentence id` → `sentence`; `Audio id` → `audio_track` media trunk (`key`/`refer`, numeric ID discarded); `Username` → speaker; `License` (`CC0`, `CC-BY`, ...) retained for reusable audio authority | target: `[sentence, audio_track, speaker, license]` multi-modal alignment (`Batch 2` `Laplace#1134`; currently `[sentence, who recorded the audio, Username]` until audio tracks are staged) |
| `transcriptions.csv` | `Sentence id`; `Lang`; `Script name`; `Username`; `Transcription` | resolved sentence, ISO 15924 `Script name` (`Hrkt`, `Latn`), `Transcription`, and reviewer `Username` | `[sentence, Hrkt, transcription]` qualified with `Username` |
| `user_languages.csv` | `Lang`; `Skill level`; `Username`; `Details` | speaker-language proficiency observation | `[[Username, eng], skill level, 5]` (observation) |
| `users_sentences.csv` | `Username`; `Sentence id`; `Review`; `Date added`; `Date last modified` | member review verdict (`-1` loss, `0` neutral, `+1` win) on `sentence`, with `Date added` and `Date last modified` omitted (`omit`) | scored review series on `sentence` qualified with `Username` |

## Relations

Tatoeba's recipes resolve `Sentence id` across all nine tables, omit `Date last modified` / `Date added` bookkeeping, keep contributors under the single `Tatoeba` witness trunk, and align `links.csv` with OpenSubtitles' sentence-tier translation strands. Admitting Tatoeba's audio archive in `Batch 2` (`Laplace#1134`) completes `Audio id` → `audio_track` cross-modal binding in `sentences_with_audio.csv`.
