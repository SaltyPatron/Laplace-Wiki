# NLTK

The Brown Corpus is a standard corpus of present-day edited American English, for use with digital computers, and the only corpus in this drop is that corpus in Form C (tagged).

## Files

| Path | Bytes | What the file is | Proof |
| --- | --- | --- | --- |
| /vault/Data/nltk_data/corpora/brown.zip | 3314357 | Zip of the Brown directory, 504 entries including the brown/ directory entry, the 500 text files, README, CONTENTS, and cats.txt. | Zip member names. |
| /vault/Data/nltk_data/corpora/brown | 10129853 | The Brown Corpus directory: 500 text files plus README, CONTENTS, and cats.txt. No other corpus directory is under /vault/Data/nltk_data. | Directory listing. README in the directory. CONTENTS in the directory. |

## Attestations

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| Brown Corpus, Form C | A standard corpus of present-day edited American English, for use with digital computers, by W. N. Francis and H. Kucera (1964), revised 1971, revised and amplified 1979. CONTENTS says this directory is Form C (tagged). Each filename is a c, a genre letter, and two digits. | a text file in corpora/brown | 500 text files | Brown Corpus | corpora/brown/README and corpora/brown/CONTENTS |
| genre | CONTENTS names the genres by letter: A press reportage, B press editorial, C press reviews, D religion, E skill and hobbies, F popular lore, G belles-lettres, H miscellaneous government and house organs, J learned, K fiction general, L fiction mystery, M fiction science, N fiction adventure, P fiction romance, R humor. cats.txt writes the same files as ca01 news through cr09 humor. | a text file | the genre on its cats.txt line | Brown Corpus | corpora/brown/CONTENTS and corpora/brown/cats.txt |
| tag | Not defined. A token in ca01 is written as word/tag, for example The/at and said/vbd. The README points at the Brown manual for the tag meanings. That URL did not resolve when opened. | a token in a Form C text | the tag after the slash | Brown Corpus | corpora/brown/ca01; corpora/brown/README, which cites [the Brown manual](http://www.hit.uib.no/icame/brown/bcm.html) |

## Records

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| tagged text | word/tag tokens separated by whitespace | One Form C file. A token is a word, a slash, and a tag, as ca01 writes it. Paragraph breaks are blank lines. The tag inventory's meanings are not in the files opened. | corpora/brown/ca01 and corpora/brown/CONTENTS |
| cats.txt line | filename, genre | One line pairing a text filename with a genre word. 500 lines, ca01 news through cr09 humor. | corpora/brown/cats.txt |

## Lineage

| Paths | What is shared | Proof |
| --- | --- | --- |
| /vault/Data/nltk_data/corpora/brown and /vault/Data/nltk_data/corpora/brown.zip | The zip's member names are the brown directory, the same text filenames, README, CONTENTS, and cats.txt. Bytes inside the zip were not compared to the extracted files. No second corpus is present under /vault/Data/nltk_data. | Zip listing and directory listing. |
