# WordFrameNet

WordFrameNet (`WFN` and `XWFN`) attests cross-resource alignments between FrameNet frames (`fnframe`), lexicalized lemmas and parts of speech, and WordNet 3.0 synset offsets resolved onto `ILI` highway nodes under one corpus witness trunk.

WordFrameNet and eXtended WordFrameNet align Berkeley FrameNet frames with Princeton WordNet 3.0 synsets and lexical units, serving as a cross-lexicon bridge under [Hops](Hops.md). Compressed `*.tar.gz` archives are unpacked rather than read twice; both extracted tables share the single `WordFrameNet` witness trunk in [`recipes/order`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/order) after `verbatlas`.

## Source

| Source | Witness | Trust class | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `wordframenet` | `WordFrameNet` source trunk | class `AcademicCurated` | `unicode`, `iso-639`, `framenet`, `cili`, `verbatlas` | `WFN/WordFrameNet`, `XWFN/eXtendedWFN` | [`wfn.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wordframenet/wfn.recipe), [`xwfn.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wordframenet/xwfn.recipe) |

## Records and target highway resolution

Both files consist of blank-line-separated blocks headed by `Frame: <FrameName>` followed by one alignment row per lexical unit / synset pairing (carrying the lemma, part-of-speech tag, WordNet 3.0 synset offset, score/weight where present in `XWFN`, and synset gloss).

Under the Recording Law ([30. Conflicts](../Sequence/Conflicts.md) S1, I5, I7):

- `Frame: <FrameName>` resolves `<FrameName>` onto its FrameNet `fnframe` highway node (`Abandonment`), and pairs `[<FrameName>, <lemma>.<pos>]` onto `fnlu` where FrameNet lists that lexical unit.
- Each row's WordNet 3.0 `(offset, pos)` is an edition-local byte-offset pointer resolved through `highway.bin` (`cili` PWN 3.0 map) onto its canonical `ILI` highway node (`i46360`) and `[lemma, eng, ILI]` lexicalization strand, with the raw byte offset recorded nowhere.
- Any `XWFN` alignment confidence weight scores the interchange attestation (`LP_OUTCOME_SCORE`), while the row emits one `[fnframe, [lemma, eng, ILI]]` interchange strand and `fnframe`↔`ili` / `fnlu`↔`ili` edges into `highway.bin`.

| Piece | Written as | Laplace reads it as | Target attestation & current recipe state |
| --- | --- | --- | --- |
| `Frame: NAME` header line | `Frame: Abandonment` | FrameNet frame highway node (`type ... fnframe`) | block subject `Abandonment` |
| alignment row (`WFN` / `XWFN`) | lemma, POS notation, WordNet 3.0 offset, optional `XWFN` confidence, gloss | sub-grammar decomposes lemma, POS (`wordnet-pos` → `upos`), and WN 3.0 offset → `ILI` (`type ... ili`), scored by `XWFN` weight where present | target: `[fnframe, [lemma, eng, ILI]]` interchange strand + `fnframe`↔`ili` highway edge (`Batch 2` recipe gap: `wfn.recipe` and `xwfn.recipe` currently retain each alignment line whole under its `Frame: NAME` subject without parsing row fields or resolving WN 3.0 offsets onto `ILI`) |

## Relations

In target form, WordFrameNet rows are pure cross-lexicon interchange strands (`[fnframe, lexicalization]` and `fnframe`↔`ili` highway edges) with zero markup field names. Closing the `Batch 2` gap adds the alignment-row field grammar to `wfn.recipe` and `xwfn.recipe`, resolves WordNet 3.0 offsets through `highway.bin` onto `ILI`, and feeds `maps` directives into `laplace highway`.
