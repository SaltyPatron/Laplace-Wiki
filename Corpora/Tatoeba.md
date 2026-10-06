# Tatoeba

Tatoeba attests what it and its members say of a whole sentence, which is its text: its language, owner, translations, tags, audio, transcriptions and reviews; a sentence's id is Tatoeba's identifier of it, content Tatoeba attests of the sentence, by which the other files point at it; and nothing is attested of the words inside it.

One source, `tatoeba`, reads Tatoeba's weekly exports: tables of tab-separated fields, without a header row. Tatoeba's page ["Download sentences"](https://tatoeba.org/en/downloads) names every file's fields under "Fields and structure", and each recipe names its columns as the page does.

## Source

| Source | Witness | Trust | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `tatoeba` | `Tatoeba`; a row that names a member as its witness is witnessed by that member, `[Tatoeba, Username, name]` | class `UserCuratedResource` | `iso-639`, `wiktionary`, `conceptnet` | the nine files the recipes name below | [`recipes/tatoeba`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/tatoeba) |

## The record

A record is one row of one file. A field is what stands between two tabs; a tab, a line break or a backslash inside a field is written after `\`; a field written `\N` is one Tatoeba leaves empty and attests nothing. A sentence is its text. `sentences.csv` defines each sentence under its id (`key "Sentence id"`), and every file that points at a sentence by that id reads it as the sentence (`refer "Sentence id" tatoeba-sentences`): the files of `sentences.csv` are read first, and a row that points at an id no sentence has says nothing. The id is content, its digits as written, and `sentences.csv` attests that it names the sentence (`[Let's try it., Sentence id, value]`); as built the recipe resolves it and records nothing of it. A member is named as Tatoeba names them, `[Tatoeba, Username, name]`, and is the witness of what a row with `witness in Username` says.

| File | Piece | Laplace reads it as | Claim recorded |
| --- | --- | --- | --- |
| `sentences.csv` | Sentence id; Lang; Text | the sentence is its text; its language and its id said of it, the id content as written | `[Let's try it., Lang, eng]`, `[Let's try it., Sentence id, value]` |
| `sentences_CC0.csv` | Sentence id; Lang; Text; Date last modified | the same, with the date | `[text, Date last modified, value]` |
| `sentences_detailed.csv` | Sentence id; Lang; Text; Username; Date added; Date last modified | the same, witnessed by the member named: "The owner is who wrote the sentence" | `[text, Lang, eng]` by `[Tatoeba, Username, name]` |
| `links.csv` | Sentence id; Translation id | both read as the sentences they point at: one says of the other that it is its translation; the reciprocal row says the reverse | `[我們試試看！, Translation id, Versuchen wir es.]` |
| `tags.csv` | Sentence id; Tag name | the sentence, and its tag | `[Let's try it., Tag name, proverb]` |
| `sentences_with_audio.csv` | Sentence id; Audio id; Username; License; Attribution URL | the sentence; the audio's id, Tatoeba's identifier of the recording, content said of the sentence; who recorded it, its licence and attribution said of the sentence | `[text, License, value]` |
| `transcriptions.csv` | Sentence id; Lang; Script name; Username; Transcription | the sentence; the transcription said of it under the script's name, witnessed by the member who reviewed it; its language by Tatoeba | `[text, Hrkt, transcription]` by the member |
| `user_languages.csv` | Lang; Skill level; Username; Details | the member in that language, `[[Tatoeba, Username, name], eng]`; the skill level and details said of it, by the member | `[[member, eng], Skill level, 5]` by the member |
| `users_sentences.csv` | Username; Sentence id; Review; Date added; Date last modified | the member attests the sentence itself, the review its outcome (`-1` a loss, `1` a win); what else the row says, of the member's review of the sentence | the sentence, by the member, at the score; `[[member, text], Review, 1]` |

Each thing a row says is a claim, a tuple as [Claims](../Semantics/Claims.md#tuples) defines it.

## Not read

`sentences_in_lists.csv` names lists only by an id no file names, and `tags_detailed.csv` and `tag_metadata.csv` have no documented fields: nothing in them is content, and they are not read. `sentences_base.csv` and every other file under the root are not read. Nothing is read of a sentence's words.
