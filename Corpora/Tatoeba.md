# Tatoeba

Tatoeba attests what it and its members say of a whole sentence, its language, text, owner, translations, tags, lists, audio, transcriptions, and reviews, and attests nothing of the words inside it.

One source, `tatoeba`, reads Tatoeba's weekly exports: tables of tab-separated fields, without a header row. Tatoeba's page ["Download sentences"](https://tatoeba.org/en/downloads) names every file's fields under "Fields and structure", and those names are the recipes' column names: every predicate on this page is one of them, as Tatoeba writes it. Each file is read by its own recipe, one section below per file, in the order the recipes are listed.

## Source

| Source | Witness | Trust | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `tatoeba` | `Tatoeba`; a row that names a member as its witness is witnessed by that member, `[Tatoeba, Username, name]` | trust 0.67 | `iso-639`, `wiktionary`, `conceptnet` | the twelve files the recipes name below, under the source's root | [`recipes/tatoeba`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/tatoeba), one per file |

The source file says `trust 0.67` and, of it: "A witness entering unrated plays at Glicko-2's stock deviation (350, trust 0.67); its trust is then earned by its agreement with higher-tier witnesses", as [Research: Trust](../Research/Trust.md) describes and [Consensus](../Semantics/Consensus.md#entry) requires of a witness entering for the first time. The number each source enters at is the recipe writer's choice, and [Corpora](README.md#not-settled) lists it among what stays missing.

## The record

A record is one row of one file. Every row of every file follows these rules, which each recipe states:

- A field is what stands between two tabs. A tab, a line break, or a backslash inside a field is written after `\`: "the character written after `\` is itself and nothing else".
- A field written `\N` is one Tatoeba leaves empty, "\N: Unknown (rare)": it attests nothing.
- A Sentence id, a Username, a List id, or an Audio id names a thing only within Tatoeba (`kinds own`): it is recorded as the path of the witness, the kind, and the value, `[Tatoeba, Sentence id, 77]`, `[Tatoeba, Username, name]`, `[Tatoeba, List id, 13]`, `[Tatoeba, Audio id, 1]`. The kind is the column's name, as the recipe gives it.
- Every other field is recorded as written, under its column's name.
- A row of a file whose recipe says `witness in Username` is attested by the member it names, `[Tatoeba, Username, name]`, and by Tatoeba when that field is empty. Every other row is attested by Tatoeba.

Each thing a row says is a claim, a tuple as [Claims](../Semantics/Claims.md#tuples) defines it, and its tier is one above its highest part, as [Compositions](../Storage/Compositions.md#tiers) requires. The text of a sentence is content like any other: what Tatoeba says, it says of the sentence as a whole, and "it says nothing of a sentence's words one by one".

## links.csv

"Contains the links between the sentences. 1 [tab] 77 means that sentence #77 is the translation of sentence #1. The reciprocal link is also present." Fields and structure: Sentence id [tab] Translation id.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| Sentence id | the subject: the sentence, `[Tatoeba, Sentence id, 1]` | the first part of the row's claim | "1 [tab] 77 means that sentence #77 is the translation of sentence #1" |
| Translation id | a sentence, of the same kind as the subject, said of it under the column's name | `[[Tatoeba, Sentence id, 1], Translation id, [Tatoeba, Sentence id, 77]]` | "The reciprocal link is also present": the row `77 [tab] 1` records the claim the other way |

Tatoeba attests every row.

## sentences_CC0.csv

"Contains all the sentences available under CC0." Fields and structure: Sentence id [tab] Lang [tab] Text [tab] Date last modified.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| Sentence id | the subject: the sentence, `[Tatoeba, Sentence id, N]` | the first part of every claim of the row | "Each sentence is associated with a unique id" |
| Lang | said of the sentence under the column's name | `[[Tatoeba, Sentence id, N], Lang, eng]` | "an ISO 639-3 language code" |
| Text | said of the sentence under the column's name: the sentence's text, as content | `[[Tatoeba, Sentence id, N], Text, the sentence]` | |
| Date last modified | said of the sentence under the column's name | `[[Tatoeba, Sentence id, N], Date last modified, value]` | |

Tatoeba attests every row.

## sentences_detailed.csv

"Contains additional fields for each sentence (owner name, date created/modified)." Fields and structure: Sentence id [tab] Lang [tab] Text [tab] Username [tab] Date added [tab] Date last modified.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| Sentence id | the subject: the sentence, `[Tatoeba, Sentence id, N]` | the first part of every claim of the row | |
| Lang | said of the sentence under the column's name | `[[Tatoeba, Sentence id, N], Lang, eng]` | |
| Text | said of the sentence under the column's name | `[[Tatoeba, Sentence id, N], Text, the sentence]` | |
| Username | the member, `[Tatoeba, Username, name]`: said of the sentence under the column's name, and the witness of the row | `[[Tatoeba, Sentence id, N], Username, [Tatoeba, Username, name]]` | "owner name" |
| Date added | said of the sentence under the column's name | `[[Tatoeba, Sentence id, N], Date added, value]` | "date created/modified": the page does not say which column is which |
| Date last modified | said of the sentence under the column's name | `[[Tatoeba, Sentence id, N], Date last modified, value]` | "date created/modified" |

The recipe says `witness in Username`: "The owner is who wrote the sentence: what the row says, its owner says." A row whose Username is empty is attested by Tatoeba.

## sentences_in_lists.csv

"Indicates the sentences that are contained by any lists. 13 [tab] 381279 means that sentence #381279 is contained by the list that has an id of 13." Fields and structure: List id [tab] Sentence id.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| List id | the subject: the list, `[Tatoeba, List id, 13]` | the first part of the row's claim | "the list that has an id of 13" |
| Sentence id | the sentence, said of the list under the column's name | `[[Tatoeba, List id, 13], Sentence id, [Tatoeba, Sentence id, 381279]]` | "sentence #381279 is contained by the list" |

Tatoeba attests every row.

## sentences_with_audio.csv

"Contains the ids of the sentences, in all languages, for which audio is available. Other fields indicate who recorded the audio, its license and a URL to attribute the author." "A single sentence can have one or more audio, each from a different voice." Fields and structure: Sentence id [tab] Audio id [tab] Username [tab] License [tab] Attribution URL.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| Sentence id | the sentence, said of the audio under the column's name | `[[Tatoeba, Audio id, N], Sentence id, [Tatoeba, Sentence id, M]]` | "the ids of the sentences ... for which audio is available" |
| Audio id | the subject: the audio, `[Tatoeba, Audio id, N]` | the first part of every claim of the row | "one or more audio, each from a different voice" |
| Username | the member, `[Tatoeba, Username, name]`, said of the audio under the column's name | `[[Tatoeba, Audio id, N], Username, [Tatoeba, Username, name]]` | "who recorded the audio" |
| License | said of the audio under the column's name; empty attests nothing | `[[Tatoeba, Audio id, N], License, value]` | "its license"; "If the license field is empty, the audio may not be reused outside the Tatoeba project" |
| Attribution URL | said of the audio under the column's name | `[[Tatoeba, Audio id, N], Attribution URL, value]` | "a URL to attribute the author" |

Tatoeba attests every row: the recipe names no witness column, so the member who recorded the audio is what the row says, not who says it.

## sentences.csv

"Contains all the sentences in the selected language. Each sentence is associated with a unique id and an ISO 639-3 language code." Fields and structure: Sentence id [tab] Lang [tab] Text.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| Sentence id | the subject: the sentence, `[Tatoeba, Sentence id, N]` | the first part of every claim of the row | "a unique id" |
| Lang | said of the sentence under the column's name | `[[Tatoeba, Sentence id, N], Lang, eng]` | "an ISO 639-3 language code" |
| Text | said of the sentence under the column's name: the sentence's text, as content | `[[Tatoeba, Sentence id, N], Text, the sentence]` | |

Tatoeba attests every row.

## tags.csv

"Contains the list of tags associated with each sentence. 381279 [tab] proverb means that sentence #381279 has been assigned the "proverb" tag." Fields and structure: Sentence id [tab] Tag name.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| Sentence id | the subject: the sentence, `[Tatoeba, Sentence id, 381279]` | the first part of the row's claim | |
| Tag name | said of the sentence under the column's name | `[[Tatoeba, Sentence id, 381279], Tag name, proverb]` | "sentence #381279 has been assigned the "proverb" tag" |

Tatoeba attests every row.

## transcriptions.csv

"Contains all transcriptions in auxiliary or alternative scripts. A username associated with a transcription indicates the user who last reviewed and possibly modified it. A transcription without a username has not been marked as reviewed. The script name is defined according to the ISO 15924 standard." Fields and structure: Sentence id [tab] Lang [tab] Script name [tab] Username [tab] Transcription.

The recipe reads a row as two statements.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| Sentence id | the subject of both statements: the sentence, `[Tatoeba, Sentence id, N]` | the first part of every claim of the row | |
| Script name and Transcription | the transcription, said of the sentence under the script's name: the Script name field is the predicate, the Transcription field the object | `[[Tatoeba, Sentence id, N], script, transcription]` | "The script name is defined according to the ISO 15924 standard" |
| Username | the witness of the transcription claim, `[Tatoeba, Username, name]`; not a claim of its own | none | "the user who last reviewed and possibly modified it" |
| Lang | said of the sentence under the column's name, attested by Tatoeba | `[[Tatoeba, Sentence id, N], Lang, value]` | |

The transcription is attested by the member the row names, `witness in Username`; a row without a username, "not been marked as reviewed", is attested by Tatoeba. The Lang claim is Tatoeba's in every row.

## tags_detailed.csv and tag_metadata.csv

"tags_detailed.csv and tag_metadata.csv: Tatoeba's page does not give their fields." The recipe names no column and no kind.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| a row | the claim itself: the path of its fields, in the row's own order, each as written (`row tuple`) | `[field, field, ...]` | none: "No column is given a name: a row is recorded as the tuple of its fields, in the row's own order" |
| a row of one field | nothing: a tuple is two parts or more | none | |

Tatoeba attests every row. No field is a Sentence id or a Username of Tatoeba's kind, because no column is named to say so.

## user_languages.csv

"Indicates the self-reported skill levels of members in individual languages." Fields and structure: Lang [tab] Skill level [tab] Username [tab] Details.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| Username and Lang | the subject: the member in that language, the path of the member and the language, `[[Tatoeba, Username, name], eng]`; Lang is written as it is, not as a kind | the first part of every claim of the row | "members in individual languages" |
| Skill level | said of the member in that language, under the column's name | `[[[Tatoeba, Username, name], eng], Skill level, value]` | "self-reported skill levels" |
| Details | said of the member in that language, under the column's name | `[[[Tatoeba, Username, name], eng], Details, value]` | |

The recipe says `witness in Username`: "Self-reported: what the row says, the member says, of the member in that language."

## users_sentences.csv

"Contains sentences reviewed by users. The value of the review can be -1 (sentence not OK), 0 (undecided or unsure), or 1 (sentence OK). Warning: this data is still experimental." Fields and structure: Username [tab] Sentence id [tab] Review [tab] Date added [tab] Date last modified.

The recipe reads a row as two statements: "A review is a member saying of a sentence that it is OK, or not, or neither: the member attests the sentence itself, and the review is the outcome. What the row says besides is said of the member's review of the sentence."

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| Sentence id, with Review | the sentence itself, `[Tatoeba, Sentence id, N]`, attested by the member (`itself`, `witness in Username`); the row's score on the scale Review is written on, `score in Review from -1 to 1`: -1 a loss, 1 a win, 0 halfway a draw, as [Attestations](../Semantics/Attestations.md#outcomes) allows. A row whose Review is empty gives no score: a win | `[Tatoeba, Sentence id, N]`, with the outcome the review gives | "-1 (sentence not OK), 0 (undecided or unsure), or 1 (sentence OK)" |
| Username and Sentence id | the subject of the second statement: the member's review of the sentence, the path of the member and the sentence, `[[Tatoeba, Username, name], [Tatoeba, Sentence id, N]]` | the first part of the claims below | "sentences reviewed by users" |
| Review | said of the member's review under the column's name | `[[[Tatoeba, Username, name], [Tatoeba, Sentence id, N]], Review, 1]` | "The value of the review" |
| Date added | said of the member's review under the column's name | `[[[Tatoeba, Username, name], [Tatoeba, Sentence id, N]], Date added, value]` | |
| Date last modified | said of the member's review under the column's name | `[[[Tatoeba, Username, name], [Tatoeba, Sentence id, N]], Date last modified, value]` | |

Both statements are attested by the member the row names, `witness in Username`; a row whose Username is empty is attested by Tatoeba.

## Not read

A source takes the files its recipes name. Every other file under the root is not read: among them `sentences_base.csv` ("Zero: the sentence is original, not a translation of another. Greater than zero: the id of the sentence from which it was translated"), `user_lists.csv` (List id, Username, Date created, Date last modified, List name, Editable by), `jpn_indices.csv` (Sentence id, Meaning id, Text), and the copy of Tatoeba's "Download sentences" page kept beside the files in `documentation`. No recipe exists for them yet, and until one does they attest nothing.

Nothing is read of a sentence's words: no part of speech, sense, or relation of a word inside a sentence is attested by Tatoeba.
