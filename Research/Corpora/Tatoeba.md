# Tatoeba

Tatoeba attests properties of a whole sentence and does not attest the words inside it.

The composition is a sentence. The masks filled are the ones the export actually has: the sentence, its language, who wrote it, which sentences translate it, and its tags, lists, audio, and reviews. The value is that field. Witness Tatoeba, trust 0.67. The recipe reads the refresh weekly export. The live tree is the smaller export of the same project. Measured, not loaded: 294,452,005 compositions from 3,191 MB. The field list is the page "Download sentences," kept beside the export.

Nothing in the export assigns a part of speech, a sense, or a dependency role to a word. [Attestations](../../Semantics/Attestations.md) keeps the claim at the composition that was marked. A translation link is a hop between two sentences, not a hop from a word to a synset. The language column hops to [ISO 639](ISO-639.md). Fanout is the number of translation links leaving a sentence. Tokenizing the sentence and treating each token as attested by Tatoeba would invent a mask the corpus does not fill.

## Files, breakdown, and caveats

Taken from the recipe files. A line in a block is a directive. The prose above it is that file's own account of what is read, what is not, and what a row becomes.

### `tatoeba/links.recipe`

"Contains the links between the sentences. 1 [tab] 77 means that sentence #77 is the translation of sentence #1. The reciprocal link is also present"   Fields and structure: Sentence id [tab] Translation id "\N: Unknown (rare)."

```text
match links.csv
grammar table
escaped \
empty-matches ^\\N$
columns "Sentence id" "Translation id"
kinds own
kind "Sentence id" "Sentence id"
kind "Translation id" "Sentence id"
claims
subject in "Sentence id"
attest "Translation id"
```

### `tatoeba/sentences-cc0.recipe`

"Contains all the sentences available under CC0." Fields and structure: Sentence id [tab] Lang [tab] Text [tab] Date last modified "\N: Unknown (rare)."

```text
match sentences_CC0.csv
grammar table
escaped \
empty-matches ^\\N$
columns "Sentence id" Lang Text "Date last modified"
kinds own
kind "Sentence id" "Sentence id"
claims
subject in "Sentence id"
attest Lang Text "Date last modified"
```

### `tatoeba/sentences-detailed.recipe`

"Contains additional fields for each sentence (owner name, date created/modified)." Fields and structure: Sentence id [tab] Lang [tab] Text [tab] Username [tab] Date added [tab] Date last modified The owner is who wrote the sentence: what the row says, its owner says. "\N: Unknown (rare)."

```text
match sentences_detailed.csv
grammar table
escaped \
empty-matches ^\\N$
columns "Sentence id" Lang Text Username "Date added" "Date last modified"
kinds own
kind "Sentence id" "Sentence id"
kind Username Username
claims
subject in "Sentence id"
attest Lang Text Username "Date added" "Date last modified"
witness in Username
```

### `tatoeba/sentences-in-lists.recipe`

"Indicates the sentences that are contained by any lists. 13 [tab] 381279 means that sentence #381279 is contained by the list that has an id of 13."   Fields and structure: List id [tab] Sentence id "\N: Unknown (rare)."

```text
match sentences_in_lists.csv
grammar table
escaped \
empty-matches ^\\N$
columns "List id" "Sentence id"
kinds own
kind "List id" "List id"
kind "Sentence id" "Sentence id"
claims
subject in "List id"
attest "Sentence id"
```

### `tatoeba/sentences-with-audio.recipe`

"Contains the ids of the sentences, in all languages, for which audio is available. Other fields indicate who recorded the audio, its license and a URL to attribute the author." "A single sentence can have one or more audio, each from a different voice." Fields and structure: Sentence id [tab] Audio id [tab] Username [tab] License [tab] Attribution URL "\N: Unknown (rare)."

```text
match sentences_with_audio.csv
grammar table
escaped \
empty-matches ^\\N$
columns "Sentence id" "Audio id" Username License "Attribution URL"
kinds own
kind "Sentence id" "Sentence id"
kind "Audio id" "Audio id"
kind Username Username
claims
subject in "Audio id"
attest "Sentence id" Username License "Attribution URL"
```

### `tatoeba/sentences.recipe`

"Contains all the sentences in the selected language. Each sentence is associated with a unique id and an ISO 639-3 language code."   Fields and structure: Sentence id [tab] Lang [tab] Text "\N: Unknown (rare)."

```text
match sentences.csv
grammar table
escaped \
empty-matches ^\\N$
columns "Sentence id" Lang Text
kinds own
kind "Sentence id" "Sentence id"
claims
subject in "Sentence id"
attest Lang Text
```

### `tatoeba/source`

Tatoeba's weekly exports: tables of tab-separated fields, without a header row. Tatoeba's page "Download sentences" names every file's fields ("Fields and structure"); it is kept beside the files, in "documentation". What Tatoeba says is of whole sentences: a sentence, its language, who wrote it, which sentences translate it, its tags, lists, audio and reviews. It says nothing of a sentence's words one by one. A witness entering unrated plays at Glicko-2's stock deviation (350, trust 0.67); its trust is then earned by its agreement with higher-tier witnesses (Research: Trust). Measured, not loaded: 294,452,005 compositions from 3,191 MB, at 750 bytes each with their indexes and standings.

```text
witness Tatoeba
trust 0.67
root $LAPLACE_DATA/.refresh-*/Tatoeba
```

### `tatoeba/tags.recipe`

"Contains the list of tags associated with each sentence. 381279 [tab] proverb means that sentence #381279 has been assigned the "proverb" tag."   Fields and structure: Sentence id [tab] Tag name "\N: Unknown (rare)."

```text
match tags.csv
grammar table
escaped \
empty-matches ^\\N$
columns "Sentence id" "Tag name"
kinds own
kind "Sentence id" "Sentence id"
claims
subject in "Sentence id"
attest "Tag name"
```

### `tatoeba/transcriptions.recipe`

"Contains all transcriptions in auxiliary or alternative scripts. A username associated with a transcription indicates the user who last reviewed and possibly modified it. A transcription without a username has not been marked as reviewed. The script name is defined according to the ISO 15924 standard." Fields and structure: Sentence id [tab] Lang [tab] Script name [tab] Username [tab] Transcription "\N: Unknown (rare)."

```text
match transcriptions.csv
grammar table
escaped \
empty-matches ^\\N$
columns "Sentence id" Lang "Script name" Username Transcription
kinds own
kind "Sentence id" "Sentence id"
kind Username Username
claims
subject in "Sentence id"
predicate in "Script name"
object in Transcription
witness in Username
claims
subject in "Sentence id"
attest Lang
```

### `tatoeba/undocumented.recipe`

tags_detailed.csv and tag_metadata.csv: Tatoeba's page does not give their fields. No column is given a name: a row is recorded as the tuple of its fields, in the row's own order. "\N: Unknown (rare)."

```text
match tags_detailed.csv tag_metadata.csv
grammar table
escaped \
empty-matches ^\\N$
claims
row tuple
```

### `tatoeba/user-languages.recipe`

"Indicates the self-reported skill levels of members in individual languages." Fields and structure: Lang [tab] Skill level [tab] Username [tab] Details Self-reported: what the row says, the member says, of the member in that language. "\N: Unknown (rare)."

```text
match user_languages.csv
grammar table
escaped \
empty-matches ^\\N$
columns Lang "Skill level" Username Details
kinds own
kind Username Username
claims
subject in Username Lang
attest "Skill level" Details
witness in Username
```

### `tatoeba/users-sentences.recipe`

"Contains sentences reviewed by users. The value of the review can be -1 (sentence not OK), 0 (undecided or unsure), or 1 (sentence OK). Warning: this data is still experimental." Fields and structure: Username [tab] Sentence id [tab] Review [tab] Date added [tab] Date last modified A review is a member saying of a sentence that it is OK, or not, or neither: the member attests the sentence itself, and the review is the outcome. What the row says besides is said of the member's review of the sentence. "\N: Unknown (rare)."

```text
match users_sentences.csv
grammar table
escaped \
empty-matches ^\\N$
columns Username "Sentence id" Review "Date added" "Date last modified"
kinds own
kind "Sentence id" "Sentence id"
kind Username Username
claims
subject in "Sentence id"
witness in Username
score in Review from -1 to 1
claims
subject in Username "Sentence id"
attest Review "Date added" "Date last modified"
witness in Username
```
