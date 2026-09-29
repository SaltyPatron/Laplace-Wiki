# Tatoeba

Tatoeba attests properties of a whole sentence and does not attest the words inside it.

## Format

| Record | Field | Order | Type | Specification |
| --- | --- | --- | --- | --- |
| Sentences | Sentence id | 1 | text | Tab-separated. Each sentence is associated with a unique id. |
| Sentences | Lang | 2 | text | Tab-separated. Each sentence is associated with an ISO 639-3 language code. |
| Sentences | Text | 3 | text | Tab-separated. Not defined beyond the column name. The export contains all the sentences in the selected language. |
| Detailed Sentences | Sentence id | 1 | text | Tab-separated. Not defined beyond the column name on this export. |
| Detailed Sentences | Lang | 2 | text | Tab-separated. Not defined beyond the column name on this export. |
| Detailed Sentences | Text | 3 | text | Tab-separated. Not defined beyond the column name on this export. |
| Detailed Sentences | Username | 4 | text | Tab-separated. The export contains additional fields for each sentence (owner name, date created/modified). Username is that owner name. |
| Detailed Sentences | Date added | 5 | text | Tab-separated. Not defined beyond the column name. The export says the additional fields include date created/modified and does not say which column is which. |
| Detailed Sentences | Date last modified | 6 | text | Tab-separated. Not defined beyond the column name. The export says the additional fields include date created/modified and does not say which column is which. |
| sentences_base.tar.bz2 | Sentence id | 1 | text | Tab-separated. Not defined beyond the column name on this export. |
| sentences_base.tar.bz2 | Base field | 2 | text | Tab-separated. Zero: the sentence is original, not a translation of another. Greater than zero: the id of the sentence from which it was translated. \N: Unknown (rare). |
| Sentences (CC0) | Sentence id | 1 | text | Tab-separated. Not defined beyond the column name on this export. The export contains all the sentences available under CC0. |
| Sentences (CC0) | Lang | 2 | text | Tab-separated. Not defined beyond the column name on this export. |
| Sentences (CC0) | Text | 3 | text | Tab-separated. Not defined beyond the column name on this export. |
| Sentences (CC0) | Date last modified | 4 | text | Tab-separated. Not defined beyond the column name on this export. |
| links.tar.bz2 | Sentence id | 1 | text | Tab-separated. 1 tab 77 means that sentence #77 is the translation of sentence #1. The reciprocal link is also present. |
| links.tar.bz2 | Translation id | 2 | text | Tab-separated. The second id in that pair. |
| tags.tar.bz2 | Sentence id | 1 | text | Tab-separated. Not defined beyond the column name on this export. |
| tags.tar.bz2 | Tag name | 2 | text | Tab-separated. 381279 tab proverb means that sentence #381279 has been assigned the "proverb" tag. |
| user_lists.tar.bz2 | List id | 1 | text | Tab-separated. Not defined beyond the column name. The export contains the list of sentence lists. |
| user_lists.tar.bz2 | Username | 2 | text | Tab-separated. Not defined beyond the column name. |
| user_lists.tar.bz2 | Date created | 3 | text | Tab-separated. Not defined beyond the column name. |
| user_lists.tar.bz2 | Date last modified | 4 | text | Tab-separated. Not defined beyond the column name. |
| user_lists.tar.bz2 | List name | 5 | text | Tab-separated. Not defined beyond the column name. |
| user_lists.tar.bz2 | Editable by | 6 | text | Tab-separated. Not defined beyond the column name. |
| sentences_in_lists.tar.bz2 | List id | 1 | text | Tab-separated. 13 tab 381279 means that sentence #381279 is contained by the list that has an id of 13. |
| sentences_in_lists.tar.bz2 | Sentence id | 2 | text | Tab-separated. The sentence contained by that list. |
| jpn_indices.tar.bz2 | Sentence id | 1 | text | Tab-separated. Sentence id refers to the id of the Japanese sentence. |
| jpn_indices.tar.bz2 | Meaning id | 2 | text | Tab-separated. Meaning id refers to the id of the English sentence. |
| jpn_indices.tar.bz2 | Text | 3 | text | Tab-separated. Not defined. The page says see another page for the format and does not include that format. |
| sentences_with_audio.tar.bz2 | Sentence id | 1 | text | Tab-separated. The id of a sentence, in any language, for which audio is available. |
| sentences_with_audio.tar.bz2 | Audio id | 2 | text | Tab-separated. A single sentence can have one or more audio, each from a different voice. A particular audio is downloaded by its audio id. |
| sentences_with_audio.tar.bz2 | Username | 3 | text | Tab-separated. The other fields indicate who recorded the audio, its license, and a URL to attribute the author. |
| sentences_with_audio.tar.bz2 | License | 4 | text | Tab-separated. If the license field is empty, the audio may not be reused outside the Tatoeba project. |
| sentences_with_audio.tar.bz2 | Attribution URL | 5 | text | Tab-separated. A URL to attribute the author. |
| user_languages.tar.bz2 | Lang | 1 | text | Tab-separated. Not defined beyond the column name. The export indicates the self-reported skill levels of members in individual languages. |
| user_languages.tar.bz2 | Skill level | 2 | text | Tab-separated. Not defined beyond the column name. |
| user_languages.tar.bz2 | Username | 3 | text | Tab-separated. Not defined beyond the column name. |
| user_languages.tar.bz2 | Details | 4 | text | Tab-separated. Not defined beyond the column name. |
| users_sentences.csv | Username | 1 | text | Tab-separated. Not defined beyond the column name. The export contains sentences reviewed by users. |
| users_sentences.csv | Sentence id | 2 | text | Tab-separated. Not defined beyond the column name on this export. |
| users_sentences.csv | Review | 3 | text | Tab-separated. The value of the review can be -1 (sentence not OK), 0 (undecided or unsure), or 1 (sentence OK). This data is still experimental. |
| users_sentences.csv | Date added | 4 | text | Tab-separated. Not defined beyond the column name on this export. |
| users_sentences.csv | Date last modified | 5 | text | Tab-separated. Not defined beyond the column name on this export. |
| Transcriptions | Sentence id | 1 | text | Tab-separated. Not defined beyond the column name on this export. |
| Transcriptions | Lang | 2 | text | Tab-separated. Not defined beyond the column name on this export. |
| Transcriptions | Script name | 3 | text | Tab-separated. The script name is defined according to the ISO 15924 standard. |
| Transcriptions | Username | 4 | text | Tab-separated. A username associated with a transcription indicates the user who last reviewed and possibly modified it. A transcription without a username has not been marked as reviewed. |
| Transcriptions | Transcription | 5 | text | Tab-separated. The export contains all transcriptions in auxiliary or alternative scripts. |

## Value

| Field | Composition | Mask | What is recorded | Lineage or hop | Specification |
| --- | --- | --- | --- | --- | --- |
| Sentences / Sentence id | the sentence | not a mask | the unique id | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Each sentence is associated with a unique id. |
| Sentences / Lang | the sentence | not a mask | the ISO 639-3 language code | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Each sentence is associated with an ISO 639-3 language code. |
| Sentences / Text | the sentence | not a mask | the sentence text | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name. |
| Detailed Sentences / Sentence id | the sentence | not a mask | the id | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name on this export. |
| Detailed Sentences / Lang | the sentence | not a mask | Lang | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name on this export. |
| Detailed Sentences / Text | the sentence | not a mask | Text | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name on this export. |
| Detailed Sentences / Username | the sentence | not a mask | the owner name | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Additional field for each sentence: owner name. |
| Detailed Sentences / Date added | the sentence | not a mask | Date added | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined. The export names date created/modified and does not map that phrase onto this column. |
| Detailed Sentences / Date last modified | the sentence | not a mask | Date last modified | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined. The export names date created/modified and does not map that phrase onto this column. |
| sentences_base.tar.bz2 / Sentence id | the sentence | not a mask | the id | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name on this export. |
| sentences_base.tar.bz2 / Base field | the sentence | not a mask | zero, a sentence id, or \N | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Zero means original. Greater than zero is the id of the sentence from which it was translated. \N means Unknown (rare). |
| Sentences (CC0) / Sentence id | the sentence | not a mask | the id | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name on this export. The export contains all the sentences available under CC0. |
| Sentences (CC0) / Lang | the sentence | not a mask | Lang | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name on this export. |
| Sentences (CC0) / Text | the sentence | not a mask | Text | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name on this export. |
| Sentences (CC0) / Date last modified | the sentence | not a mask | Date last modified | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name on this export. |
| links.tar.bz2 / Sentence id | the sentence | not a mask | the sentence id | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | 1 tab 77 means that sentence #77 is the translation of sentence #1. The reciprocal link is also present. |
| links.tar.bz2 / Translation id | the sentence | not a mask | the translation sentence id | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | The id of the translation sentence. Not a property of a word inside either sentence. |
| tags.tar.bz2 / Sentence id | the sentence | not a mask | the id | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name on this export. |
| tags.tar.bz2 / Tag name | the sentence | not a mask | the tag | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | The tag assigned to the sentence. Not a part of speech, sense, or dependency role of a word. |
| user_lists.tar.bz2 / List id | the list | not a mask | the list id | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name. The export is the list of sentence lists. It does not attest a word. |
| user_lists.tar.bz2 / Username | the list | not a mask | Username | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name. |
| user_lists.tar.bz2 / Date created | the list | not a mask | Date created | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name. |
| user_lists.tar.bz2 / Date last modified | the list | not a mask | Date last modified | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name. |
| user_lists.tar.bz2 / List name | the list | not a mask | the list name | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name. |
| user_lists.tar.bz2 / Editable by | the list | not a mask | Editable by | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name. |
| sentences_in_lists.tar.bz2 / List id | the sentence | not a mask | the list id | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | The list that contains the sentence. |
| sentences_in_lists.tar.bz2 / Sentence id | the sentence | not a mask | the sentence id | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | The sentence contained by the list. |
| jpn_indices.tar.bz2 / Sentence id | the Japanese sentence | not a mask | the Japanese sentence id | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Sentence id refers to the id of the Japanese sentence. |
| jpn_indices.tar.bz2 / Meaning id | the Japanese sentence and the English sentence | not a mask | the English sentence id | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Meaning id refers to the id of the English sentence. |
| jpn_indices.tar.bz2 / Text | the Japanese sentence and the English sentence | not a mask | Not defined | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined. No part of speech, sense, or dependency role is read out of this text. |
| sentences_with_audio.tar.bz2 / Sentence id | the sentence | not a mask | the sentence id | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | The sentence for which audio is available. |
| sentences_with_audio.tar.bz2 / Audio id | the sentence | not a mask | the audio id | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | One sentence can have one or more audio, each from a different voice. |
| sentences_with_audio.tar.bz2 / Username | the sentence | not a mask | who recorded the audio | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | The other fields indicate who recorded the audio, its license, and a URL to attribute the author. |
| sentences_with_audio.tar.bz2 / License | the sentence | not a mask | the license | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | If the license field is empty, the audio may not be reused outside the Tatoeba project. |
| sentences_with_audio.tar.bz2 / Attribution URL | the sentence | not a mask | the attribution URL | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | A URL to attribute the author. |
| user_languages.tar.bz2 / Lang | the member | not a mask | Lang | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name. This export is a member's self-reported skill, not a sentence and not a word. |
| user_languages.tar.bz2 / Skill level | the member | not a mask | Skill level | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name. |
| user_languages.tar.bz2 / Username | the member | not a mask | Username | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name. |
| user_languages.tar.bz2 / Details | the member | not a mask | Details | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name. |
| users_sentences.csv / Username | the sentence | not a mask | Username | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name. The export contains sentences reviewed by users. |
| users_sentences.csv / Sentence id | the sentence | not a mask | the sentence id | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name on this export. |
| users_sentences.csv / Review | the sentence | not a mask | -1, 0, or 1 | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | -1 sentence not OK, 0 undecided or unsure, 1 sentence OK. Still experimental. |
| users_sentences.csv / Date added | the sentence | not a mask | Date added | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name on this export. |
| users_sentences.csv / Date last modified | the sentence | not a mask | Date last modified | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name on this export. |
| Transcriptions / Sentence id | the sentence | not a mask | the sentence id | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name on this export. |
| Transcriptions / Lang | the sentence | not a mask | Lang | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined beyond the column name on this export. |
| Transcriptions / Script name | the sentence | not a mask | the ISO 15924 script name | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | The script name is defined according to the ISO 15924 standard. |
| Transcriptions / Username | the sentence | not a mask | the last reviewer, or empty | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | A username indicates the user who last reviewed and possibly modified the transcription. Empty means not marked as reviewed. |
| Transcriptions / Transcription | the sentence | not a mask | the transcription | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | A transcription of the sentence in an auxiliary or alternative script. Not a segmentation of the sentence into words. |
| word | the sentence | not a mask | Not defined | [Attestations](../Semantics/Attestations.md): a claim stays at the composition that was marked. | Not defined. No part of speech, sense, or dependency role is assigned to a word inside the sentence. |
