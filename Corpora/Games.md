# Games

The PGN collections and the Lichess opening tables have no recipe yet, so they are not ingested and attest nothing.

## Source

No directory under [`recipes/`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes) reads this collection, and `recipes/order` does not name it. Until a recipe exists, nothing in it is decomposed, recorded, or attested; see [Attestations](../Semantics/Attestations.md#observations). The format below is the publisher's, kept so that a recipe can be written from it.

## Format

| Record | Fields in order | What a record is | Specification |
| --- | --- | --- | --- |
| PGN game | Event, Site, Date, Round, White, Black, Result, then the movetext | A tag-pair section followed by a movetext section. For export format the Seven Tag Roster appears in that order before any other tag. Other tags may follow. The game termination marker concludes the movetext and matches Result. | [PGN specification](https://github.com/fsmosca/PGN-Standard/blob/master/PGN-Standard.txt) sections 8.1.1 and 8.2, opened as PGN-Standard.txt. |
| opening row | eco, name, pgn | One opening: its ECO code, its English name, and a PGN move sequence. The README also describes uci and epd in a dist/ build that is not in this tarball. | README.md and a.tsv inside the Lichess openings tarball. The same header is on the TSV tables. |
| FIDE player | FideId, Name, Federation, Sex, Title, Standard, Rapid, Blitz, BirthYear, Flag | One object in the Players array of the snapshot. What Standard, Rapid, and Blitz mean beyond those key names is not defined on a page opened for this row. | rating-list.snapshot.json.gz |
| files-345.txt line | one URL | The download URL of one table file. | files-345.txt |
