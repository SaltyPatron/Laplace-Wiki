# Games

PGN collections attest a chess game by the Seven Tag Roster, Event, Site, Date, Round, White, Black, and Result, and by the movetext, and the Lichess opening tables are a separate witness of an ECO code, an English opening name, and a PGN move sequence.

## Value

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| Event | The name of the tournament or match event. | a PGN game | the tag value | LumbrasGigaBase; The Week in Chess; chess.com PGN archives | [PGN specification](https://github.com/fsmosca/PGN-Standard/blob/master/PGN-Standard.txt) sections 8.1.1 and 8.2, opened as PGN-Standard.txt. |
| Site | The location of the event. | a PGN game | the tag value | LumbrasGigaBase; The Week in Chess; chess.com PGN archives | [PGN specification](https://github.com/fsmosca/PGN-Standard/blob/master/PGN-Standard.txt) sections 8.1.1 and 8.2, opened as PGN-Standard.txt. |
| Date | The starting date of the game, in YYYY.MM.DD. | a PGN game | the tag value | LumbrasGigaBase; The Week in Chess; chess.com PGN archives | [PGN specification](https://github.com/fsmosca/PGN-Standard/blob/master/PGN-Standard.txt) sections 8.1.1 and 8.2, opened as PGN-Standard.txt. |
| Round | The playing round ordinal of the game. | a PGN game | the tag value | LumbrasGigaBase; The Week in Chess; chess.com PGN archives | [PGN specification](https://github.com/fsmosca/PGN-Standard/blob/master/PGN-Standard.txt) sections 8.1.1 and 8.2, opened as PGN-Standard.txt. |
| White | The player of the white pieces. | a PGN game | the tag value | LumbrasGigaBase; The Week in Chess; chess.com PGN archives | [PGN specification](https://github.com/fsmosca/PGN-Standard/blob/master/PGN-Standard.txt) sections 8.1.1 and 8.2, opened as PGN-Standard.txt. |
| Black | The player of the black pieces. | a PGN game | the tag value | LumbrasGigaBase; The Week in Chess; chess.com PGN archives | [PGN specification](https://github.com/fsmosca/PGN-Standard/blob/master/PGN-Standard.txt) sections 8.1.1 and 8.2, opened as PGN-Standard.txt. |
| Result | The result of the game. It is the same as the game termination marker that concludes the movetext. The four values are 1-0, 0-1, 1/2-1/2, and *. | a PGN game | the tag value | LumbrasGigaBase; The Week in Chess; chess.com PGN archives | [PGN specification](https://github.com/fsmosca/PGN-Standard/blob/master/PGN-Standard.txt) sections 8.1.1 and 8.2, opened as PGN-Standard.txt. |
| movetext | The usually enumerated and possibly annotated moves of the game, in SAN, along with the concluding game termination marker. | a PGN game | the moves | LumbrasGigaBase; The Week in Chess; chess.com PGN archives | [PGN specification](https://github.com/fsmosca/PGN-Standard/blob/master/PGN-Standard.txt) sections 8.1.1 and 8.2, opened as PGN-Standard.txt. A movetext section was read in LumbrasGigaBase_OTB_2025.pgn, twic1650.pgn, and MagnusCarlsen_chesscom.pgn. |
| eco | ECO classification. | an opening row | the eco column | Lichess openings | README.md inside the openings tarball, and the header of a.tsv. |
| name | Opening name in English. | an opening row | the name column | Lichess openings | README.md inside the openings tarball. |
| pgn | Well known sequence of moves, or the most common moves to reach the opening position based on master games, as PGN. | an opening row | the pgn column | Lichess openings | README.md inside the openings tarball. |
| FIDE player | Not defined beyond the keys on each Players object. The snapshot's SourceUrl is the FIDE players list zip at [players_list_xml.zip](https://ratings.fide.com/download/players_list_xml.zip). That download page was not opened. | one Players object | 1923799 players | rating-list.snapshot.json.gz | The snapshot. |
| Syzygy table file | Not defined. No Syzygy specification page was opened. files-345.txt lists the download URL of each file, 145 under the path 3-4-5-wdl and 145 under 3-4-5-dtz. | a .rtbw or .rtbz file | 290 files | files-345.txt | files-345.txt |

## Format

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| PGN game | Event, Site, Date, Round, White, Black, Result, then the movetext | A tag-pair section followed by a movetext section. For export format the Seven Tag Roster appears in that order before any other tag. Other tags may follow. The game termination marker concludes the movetext and matches Result. | [PGN specification](https://github.com/fsmosca/PGN-Standard/blob/master/PGN-Standard.txt) sections 8.1.1 and 8.2, opened as PGN-Standard.txt. |
| opening row | eco, name, pgn | One opening: its ECO code, its English name, and a PGN move sequence. The README also describes uci and epd in a dist/ build that is not in this tarball. | README.md and a.tsv inside the Lichess openings tarball. The same header is on /vault/Data/Games/Chess/openings/a.tsv. |
| FIDE player | FideId, Name, Federation, Sex, Title, Standard, Rapid, Blitz, BirthYear, Flag | One object in the Players array of the snapshot. What Standard, Rapid, and Blitz mean beyond those key names is not defined on a page opened for this row. | rating-list.snapshot.json.gz |
| files-345.txt line | one URL | The download URL of one table file. | files-345.txt |
