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

A FIDE ID is a publicly known identifier used across sources and languages, and so a highway node: the node for a player, as an ILI is for a concept. A player's `Name` in the rating list, the names a PGN writes in its `White` and `Black` tags, and the player's names in every other language and script are lexicalizations of that node, and the languages the player speaks are attested relations, [27. Chess](../Sequence/Chess.md).

## Record kinds

A PGN file holds several kinds of record, and a recipe disposes each by what it is (SaltyPatron/Laplace-Engine#46). This is a proposal for the recipe; the inventor decides it.

| Kind | How the source marks it | What it is |
| --- | --- | --- |
| Played game | the Seven Tag Roster and a result of `1-0`, `0-1` or `1/2-1/2` | A line (the ordered trajectory of positions and moves, shared by every game that plays it) and an occurrence: players, date, event, site, round, clocks and result. Every tag is a statement; none is dropped and none is hashed into an identity. |
| Custom start | `[SetUp "1"]` with `[FEN "…"]` | The trajectory begins at that position instead of the standard one. |
| Chess960 / freestyle | `[Variant "Chess960"]` with SetUp and FEN | The variant is a ruleset, and rules are firmware ([28. Games](../Sequence/Games.md)): it governs which moves are legal, castling above all, and is never part of a position's identity. The start position is P0. |
| Incomplete | `[Result "*"]`, or a Termination of abandoned or forfeit | The trajectory is content; no outcome is claimed. Termination is a statement about how it ended. |
| Study, lesson or annotated game | variations in parentheses, `{comments}`, numeric annotation glyphs (`$1`, `!?`) | Not a played game: the variations make a tree of lines, comments are text, and the glyphs are the annotator's judgments. All of it is the study's own testimony, under its source, with no occurrence of anyone playing it. |
| Puzzle or composed problem | a start position and a solution line | The composer's claimed solution: testimony about a line from that position. |

The monorepo's chess ingest, the only one built so far, keeps moves and positions losslessly and content-derived, and differs from the law in what Engine#46 lists: minted player, event and occurrence identities with folded names, dropped tags (Site, Round, Link, UTC times, Tournament), a domain byte in composition, a private atom alphabet instead of the codepoint floor, and a four-bit castling encoding instead of [27.1](../Sequence/Chess.md)'s eight-bit mask.
