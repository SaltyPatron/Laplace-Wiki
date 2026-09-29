# WordFrameNet

WordFrameNet's files pair a frame with a word and a synset offset, and no witness is named because the fields are undefined.

## Value

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| `Frame:` line | Not defined. Both files contain lines that begin `Frame:`. Nothing in the drop says what the token after `Frame:` is, or who attests it. [Claims](../Semantics/Claims.md#the-linguistic-super-highway) names WordFrameNet. [Pull](../Semantics/Pull.md#hop-and-fanout) is the pull across a hop. [Hops](Hops.md) lists the edge as not defined. | Not defined | Not defined | Not named in the files | The two files, and the queries below |
| Fields of a line under `Frame:` in `WordFrameNet` | Not defined. | Not defined | Not defined | Not named in the files | `/vault/Data/WordFrameNet/WFN/WordFrameNet` and the queries below |
| Fields of a line under `Frame:` in `eXtendedWFN` | Not defined. | Not defined | Not defined | Not named in the files | `/vault/Data/WordFrameNet/XWFN/eXtendedWFN` and the queries below |

## Format

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| `WordFrameNet` | Not a fixed list. 722 lines match `Frame:` plus the rest of the line. 1,444 lines are blank. 9,122 other lines match a non-space token, a single character, and an eight-digit number, a hyphen, and a letter, sometimes with more text after that. 206 other lines match neither, including a line that begins `abusive`, a vertical bar, then `a 01114176-a 0 by physical or psychological maltreatment`. | A text file with no header and no README. 11,494 lines. | `/vault/Data/WordFrameNet/WFN/WordFrameNet` |
| `eXtendedWFN` | A blank line, or `Frame:` plus the rest of the line, or exactly three whitespace-separated tokens. | A text file with no header and no README. 22,031 lines: 722 blank, 722 `Frame:` lines, 20,587 three-token lines. | `/vault/Data/WordFrameNet/XWFN/eXtendedWFN` |
