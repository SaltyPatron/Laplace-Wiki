# WordFrameNet

WordFrameNet's files pair a frame with a word and a synset offset, and no witness is named because the fields are undefined.

## Files

| Path | Bytes | What the file is | Proof |
| --- | ---: | --- | --- |
| `/vault/Data/WordFrameNet/WFN.tar.gz` | 218272 | Gzip tar archive. One member, `WordFrameNet`, 625,643 bytes. | `tarfile` listing |
| `/vault/Data/WordFrameNet/WFN/WordFrameNet` | 625643 | That member, extracted. SHA-256 matches the archive member. | SHA-256 of the member and the file |
| `/vault/Data/WordFrameNet/XWFN.tar.gz` | 136895 | Gzip tar archive. One member, `eXtendedWFN`, 451,382 bytes. | `tarfile` listing |
| `/vault/Data/WordFrameNet/XWFN/eXtendedWFN` | 451382 | That member, extracted. SHA-256 matches the archive member. | SHA-256 of the member and the file |

## Attestations

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| `Frame:` line | Not defined. Both files contain lines that begin `Frame:`. Nothing in the drop says what the token after `Frame:` is, or who attests it. [Claims](../../Semantics/Claims.md#the-linguistic-super-highway) names WordFrameNet. [Pull](../../Semantics/Pull.md#hop-and-fanout) is the pull across a hop. [Hops](Hops.md) lists the edge as not defined. | Not defined | Not defined | Not named in the files | The two files, and the queries below |
| Fields of a line under `Frame:` in `WordFrameNet` | Not defined. | Not defined | Not defined | Not named in the files | `/vault/Data/WordFrameNet/WFN/WordFrameNet` and the queries below |
| Fields of a line under `Frame:` in `eXtendedWFN` | Not defined. | Not defined | Not defined | Not named in the files | `/vault/Data/WordFrameNet/XWFN/eXtendedWFN` and the queries below |

## Records

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| `WordFrameNet` | Not a fixed list. 722 lines match `Frame:` plus the rest of the line. 1,444 lines are blank. 9,122 other lines match a non-space token, a single character, and an eight-digit number, a hyphen, and a letter, sometimes with more text after that. 206 other lines match neither, including a line that begins `abusive`, a vertical bar, then `a 01114176-a 0 by physical or psychological maltreatment`. | A text file with no header and no README. 11,494 lines. | `/vault/Data/WordFrameNet/WFN/WordFrameNet` |
| `eXtendedWFN` | A blank line, or `Frame:` plus the rest of the line, or exactly three whitespace-separated tokens. | A text file with no header and no README. 22,031 lines: 722 blank, 722 `Frame:` lines, 20,587 three-token lines. | `/vault/Data/WordFrameNet/XWFN/eXtendedWFN` |

## Lineage

| Paths | What is shared | Proof |
| --- | --- | --- |
| `/vault/Data/WordFrameNet/WFN.tar.gz` and `/vault/Data/WordFrameNet/XWFN.tar.gz` | Not byte-identical. Sizes 218,272 and 136,895. Each archive holds one member, and the members are different files. | `stat` and `tarfile` |
| `WFN/WordFrameNet` and `XWFN/eXtendedWFN` | Not byte-identical. Sizes 625,643 and 451,382. The 722 `Frame:` lines are the same set of strings. The other lines are not one shared file: 8,386 lines only in `WordFrameNet`, 16,497 only in `eXtendedWFN`, 729 lines in both, and those 729 are mostly the shared `Frame:` lines. | SHA-256 and a line-set compare |
| Publisher format | Not in the drop. There is no README. The queries below did not return a column specification for these files. [eXtended WordFrameNet](https://aclanthology.org/L10-1550/) (Laparra and Rigau, LREC 2010, ELRA) describes integrating FrameNet and WordNet. A text search of [the PDF](https://aclanthology.org/L10-1550.pdf) for format, column, `Frame:`, download, synset offset, and file did not return a column specification. [adimen.si.ehu.es/web/WordFrameNet](http://adimen.si.ehu.es/web/WordFrameNet) did not resolve. | The queries: `WordFrameNet WFN eXtendedWFN format columns frame synset offset publisher`; `WordFrameNet Laparra Rigau "Frame:" lexical unit synset offset file format`; `site:adimen.si.ehu.es WordFrameNet download format`; `"WordFrameNet" "Frame:" download txt OR tarball OR "eXtendedWFN" format columns`; `"eXtended WordFrameNet" file "synset" Laparra download resource format` |
