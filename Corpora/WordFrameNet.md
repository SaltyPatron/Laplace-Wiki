# WordFrameNet

WordFrameNet's WFN and XWFN files are read as frame-alignment blocks under one corpus source trunk.

## Source

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `wordframenet` | `WordFrameNet` source trunk | `AcademicCurated` | `unicode`, `iso-639` | `WFN/WordFrameNet`, `XWFN/eXtendedWFN` | [wfn.recipe](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wordframenet/wfn.recipe), [xwfn.recipe](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wordframenet/xwfn.recipe) |

## Records

Both recipes read blank-line-separated blocks. The first line names the frame as `Frame: NAME`; the remaining lines are alignment rows. The frame name supplies the block's subject. Each following row is retained and attested as a value of that frame.

The current recipes retain each row whole. They do not yet turn its lemma, part-of-speech notation, synset offset and gloss into separate highway references. Recipe presence establishes block/row coverage, not a fully typed WordNet crosswalk.

## Not read

The [source](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/wordframenet/source) excludes `*.tar.gz`; the extracted files are read instead. The source is present in [recipes/order](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/order) after `verbatlas`. WFN and XWFN recipe labels do not create independent corpus witnesses.
