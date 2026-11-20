# Universal Dependencies

Universal Dependencies is one source and one witness, its treebanks, its documentation pages and its validator data all files under one trunk: a treebank attests what it says of each word within its sentence, the validator's lists of parts of speech and relations are the highway's `upos` and `deprel` lists, and the documentation attests what each of those is.

One organization's corpus set is one source ([30. Conflicts](../Sequence/Conflicts.md) I3). Universal Dependencies ([release 2.18](https://lindat.mff.cuni.cz/repository/handle/11234/1-6149), [UniversalDependencies/docs](https://github.com/UniversalDependencies/docs/tree/pages-source), and [UniversalDependencies/tools](https://github.com/UniversalDependencies/tools/tree/10ce40cf8a577714e51cf56b443dd4c2c6d55f91/data)) forms one source trunk and one witness (`Universal Dependencies`), with all 353+ treebanks, documentation pages, and validator lists residing as files under that trunk (`Batch 2` consolidates the three `recipes/order` directories and per-treebank `witness {dir}` naming onto the single corpus trunk).

## Sources

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `universal-dependencies-tools` | `Universal Dependencies` trunk (as built, `UniversalDependencies tools`) | `AcademicCurated` (as built, `StandardsDerived`) | `unicode`, `iso-639` | `upos.json`, `udeprels.json` under `UD-Tools/*/data` | [`upos.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/universal-dependencies-tools/upos.recipe), [`udeprels.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/universal-dependencies-tools/udeprels.recipe) |
| `universal-dependencies-documentation` | `Universal Dependencies` trunk | `AcademicCurated` (as built, `StandardsDerived`) | `universal-dependencies-tools` | `*.md` under `UD-Docs/extracted/docs-pages-source` | [`pages.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/universal-dependencies-documentation/pages.recipe) |
| `universal-dependencies` | `Universal Dependencies` trunk (as built, `witness {dir}` per treebank) | class `AcademicCurated` | `unicode`, `iso-639` | `*.conllu` under `UD-Treebanks/ud-treebanks-*` | [`conllu.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/universal-dependencies/conllu.recipe) |

## From trunk to leaves: empirical POS counts & sentence-aligned layers

```text
Universal Dependencies           the source trunk, [source record, its files' trunks in path order]: the witness
├ source record                  "Universal Dependencies" and its release, content
├ _u-pos/ADJ.md …                the documentation pages, UD's definitions of its tags, relations and features: files
├ data/upos.json …               the validator's data, feeding highway upos and deprel banks: files under the same trunk
├ UD_Abaza-ATB/ …                a treebank directory under the one trunk (never a separate witness)
└ UD_English-EWT/en_ewt-ud-train.conllu
  ├ metadata                     OS file metadata + document/paragraph boundaries
  └ content                      [record, record, …], one record per CoNLL-U sentence
    └ record                     ordered sentence annotation bundle
      ├ sentence                 the `# text = …` sentence: UAX #29 words, graphemes, codepoints
      ├ tokens                   CoNLL-U syntactic tokens (e.g. `don't` -> `do`, `n't`), each FORM to codepoints
      ├ aligned layers           sentence-length UPOS, XPOS, LEMMA, and FEATS trajectories aligned 1:1 to `tokens`
      ├ dependency tree          DEPREL + HEAD syntactic subtrees (`deprel` bank, 6 bits at offset 19)
      ├ notes & participants     `text_en` parallel translation strands; `speaker_id` and `Annotator` as content
      └ lexical/POS strands      `[forces, NOUN]`, `[forces, force]`, `[forces, Number=Plur]` + `upos` entity bank (5 bits at offset 8)
```

Two Recording Law invariants govern treebank attestations:

1. **Empirical token POS and lemma counts are preserved (`k` occurrences = `k`-game series):** `UD_English-EWT` (English Web Treebank) and sister UD gold treebanks are human-reviewed syntactic annotations. When `[forces, NOUN]` occurs in `k` annotated tokens across the corpus while `[forces, VERB]` occurs in `m` tokens, those empirical token counts fold into the corpus witness's Glicko-2 series ([30. Conflicts](../Sequence/Conflicts.md) T3, I6) and occurrence observations—preserving real lexical POS priors and **never** discarding repeated token tags as "packaging".
2. **Sentence-aligned layer trajectories ([Types: Layers](../Reference/Types.md#layers)):** Down each sentence, `UPOS`, `XPOS`, `LEMMA`, `FEATS`, and `DEPREL(HEAD)` compose sentence-aligned annotation layer trajectories (`[sentence, UPOS_layer]`, dependency subtrees with `deprel` occurrence mask bits at offset `19` in `manifest/banks.tsv`). During `Forward` (`roles_of`), Laplace reads a word's POS and dependency role **in context at its ordinal along matching sentence trajectories** rather than picking a word's globally commonest tag out of context (`Batch 2` recipe/VM target: `conllu.recipe` currently emits token-level claims and flat `[word, deprel, head_word]` triples without composing the sentence-aligned layer paths or writing `upos`/`deprel` mask banks).

## The CoNLL-U sentence (`conllu.recipe`)

Each sentence block in `*.conllu` ([CoNLL-U format](https://universaldependencies.org/format.html)) consists of `#` comment lines followed by 10-column tab-separated token rows:

| Piece | Written as | Laplace reads it as | Target attestation & current recipe state | Specification |
| --- | --- | --- | --- | --- |
| `# text = ...` | mandatory comment | canonical UTF-8 sentence (`thing record text`) | sentence trajectory subject | [CoNLL-U format](https://universaldependencies.org/format.html) |
| `# sent_id = …`, `# newdoc id = …`, `# newpar id = …` | document/sentence IDs | internal pointers (`omit` / tree structure), recorded nowhere | none | mandatory sentence ID & document boundaries |
| `# text_en = …`, `# speaker_id = …`, other `# key = value` | sentence comments | `text_en` → sentence-tier English translation strand; `speaker_id` → speaker participant relation (not an extra witness) | `[sentence, translated, text_en]`, `[sentence, speaker, id]` (`Batch 2` replaces `own note:speaker_id` and raw comment keys) | sentence-level metadata |
| `ID` (`1`, `1-2`, `8.1`) & `HEAD` (`0`, `N`) | 1-based token index, multiword range, or enhanced empty node | sentence-local pointers (`key row ID`, `refer HEAD row`), recorded nowhere | resolved into token-span and dependency-tree structure (`1-2` spans tokens `1..2`) | CoNLL-U word/multiword/empty-node indexing |
| `FORM` | surface token | token entity at its sentence position (`thing row FORM`) | subject of token-level strands and layer slot | "Word form or punctuation symbol" |
| `LEMMA` | dictionary base form | aligned `LEMMA` layer + `[FORM, LEMMA]` lexical strand | `[forces, force]` + sentence `LEMMA` layer | "Lemma or stem of word form" |
| `UPOS` | one of 17 universal tags (`NOUN`, `VERB`, `ADJ`, ...) | `type UPOS upos` (`upos` bank: `5` bits at offset `8`), aligned sentence `UPOS` layer + `[FORM, UPOS]` empirical series | `[forces, NOUN]` (`k` occurrences preserved) + sentence `UPOS` layer | "Universal part-of-speech tag" |
| `XPOS` | treebank-specific tag (`NNP`, `VBD`, ...) | treebank tagset road class (crosswalked to `upos` where `manifest/slots/edges-tagsets.tsv` maps PTB/treebank tags) + sentence `XPOS` layer | `[FORM, XPOS_tag]` + sentence `XPOS` layer | "Optional language-specific part-of-speech tag" |
| `FEATS` | `Key=Value` pipe list (`Number=Plur\|Case=Nom`) | universal morphological feature values (`Number=Plur`) in the sentence's `FEATS` layer and on `FORM` | `[forces, Number=Plur]` + sentence `FEATS` layer | "List of morphological features" |
| `DEPREL` + `HEAD` & `DEPS` | universal dependency relation (`nsubj`, `root`, `obj`) and enhanced `head:rel` graph | sentence-aligned dependency tree (`deprel` occurrence bank: `6` bits at offset `19`) + enhanced `DEPS` graph | contextual dependency subtree (`Batch 2` upgrades flat `[word, nsubj, head]` to sentence-aligned dependency layers and attests `DEPS`) | CoNLL-U syntactic & enhanced dependencies |
| `MISC` | `Key=Value` pipe list (`Translit=...`, `SpaceAfter=No`, `Annotator=...`) | internal token IDs (`UI`, `Ref`, `LId`, `XmlId`, `AlignBegin/End`) and `SpaceAfter` (already in `# text`) omitted; `Translit`/`Gloss` attested; `Annotator` kept as participant content | `[word, transliteration, value]`, participant `Annotator` (`Batch 2` replaces `own MISC.Annotator`) | CoNLL-U miscellaneous annotations |
| `_` | underscore | empty CoNLL-U field, attests nothing | none | |

## Validator lists & documentation (`upos.recipe`, `udeprels.recipe`, `pages.recipe`)

`upos.json` (17 tags) and `udeprels.json` (37 universal dependency relations) register the frozen slots of the `upos` (`5` bits at offset `8`) and `deprel` (`6` bits at offset `19`) banks in `manifest/banks.tsv` and `highway.bin`. `pages.recipe` reads UD's Markdown documentation pages (`title`, `shortdef`, and feature value headings) to attest the human-readable definitions of every universal tag, relation, and morphological feature under the single `Universal Dependencies` trunk.
