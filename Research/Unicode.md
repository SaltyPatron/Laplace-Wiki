# Unicode

Laplace's tier 0 and its segmentation rest on the Unicode data, and this page records what that data defines, what it covers, and which parts of it are stable across versions.

The pages that use it are [Atoms](../Storage/Atoms.md#unicode-data), for the codespace and its data, and [Placement](Placement.md), for the order the codepoints are placed in.

> [!NOTE]
> The local data is Unicode 17.0.0. Numbers marked *measured* were computed by the local analysis script from `allkeys.txt` (sha256 `2503d093…99ecd`) and `ucd.all.flat.xml` (sha256 `925bf557…0fd1a`), or counted from the local emoji and break-test files. Section numbers and quotations are from the Unicode 17 revisions of each report. Unicode 18.0 has since been published, and the unversioned report URLs now serve its revisions.

## Text segmentation (UAX #29)

UAX #29 defines default boundaries for three kinds of segment, each driven by UCD properties. Line breaking is a separate specification, UAX #14.

| Segment | Rules | Driving properties |
| --- | --- | --- |
| Extended grapheme cluster | GB1–GB999 | `Grapheme_Cluster_Break`, `Indic_Conjunct_Break`, `Extended_Pictographic` |
| Word | WB1–WB999 | `Word_Break` |
| Sentence | SB1–SB998 | `Sentence_Break` |

### Grapheme rules

- GB3: CR × LF.
- GB4, GB5: break around controls.
- GB6–GB8: Hangul L, V, T, LV, and LVT jamo sequences stay together.
- GB9, GB9a, GB9b: no break before Extend, ZWJ, or SpacingMark, and no break after Prepend.
- GB9c: Indic conjunct clusters, such as Devanagari consonant + virama + consonant.
- GB11: `ExtPict Extend* ZWJ × ExtPict`, which keeps emoji ZWJ sequences together.
- GB12, GB13: regional indicators pair into flags.
- GB999: break everywhere else.

Grapheme clusters are language-agnostic by design, determined "without requiring language or font metadata". Aksara and orthographic-syllable clusters for Indic scripts are tailorings.

### Word and sentence rules

Letters, numbers, Katakana, and ExtendNumLet glue into runs (WB5–WB13b), and WB3d keeps runs of horizontal whitespace together. WB999 breaks everywhere else, "including around ideographs", so by default every punctuation mark and every Han ideograph is its own segment. Sentence rules use classes such as STerm, ATerm, Close, and Sp; they are heuristic, and abbreviations such as "Mr." need CLDR suppressions.

### Where the defaults need tailoring

UAX #29 §2 states that "reliable detection of word boundaries in languages such as Thai, Lao, Chinese, or Japanese requires the use of dictionary lookup or other mechanisms". §4 groups scripts by their line-breaking class:

| Style | Recognized by | Default word boundaries | Default line breaks |
| --- | --- | --- | --- |
| Western (Latin, Arabic, Devanagari, …) | lb=AL | adequate | adequate |
| East Asian and Brahmic (Chinese, Japanese, Brahmi, Javanese, …) | lb=ID, AK, or AS | need tailoring | adequate |
| South-East Asian (Thai, Lao, Myanmar, Khmer, …) | lb=SA | need tailoring (dictionary) | need tailoring (dictionary) |

Hangul is in the first group for words and the second for line breaks. The conformance clauses allow either the default rules or a declared profile that adds or removes boundaries. CLDR carries locale tailorings and sentence-break suppressions (UTS #35 Part 1), and ICU implements dictionary-based breaking for Thai, Lao, Khmer, Myanmar, and CJK.

### Segments are lossless

A boundary is an offset in the text. The rules break at the start and end of any non-empty text, and segments are the spans between consecutive boundaries, so they tile the string exactly. Whitespace, punctuation, and controls are never dropped. The rules are defined on NFD but "can be applied directly to non-NFD text and yield equivalent results" (§2), so segmenting does not require normalizing the text. Tailored rules may not keep that equivalence.

### Conformance tests

The files `GraphemeBreakTest.txt`, `WordBreakTest.txt`, `SentenceBreakTest.txt`, and `LineBreakTest.txt` mark every position of each test sequence with `÷` (break) or `×` (no break). Conformance to the default rules means reproducing every mark. The tests "cannot be exhaustive", but they cover all pairs of property values. Measured test-line counts:

| File | Test lines |
| --- | --- |
| GraphemeBreakTest | 766 |
| WordBreakTest | 1,944 |
| SentenceBreakTest | 512 |
| LineBreakTest | 19,338 |

Unicode 17 adds the Line_Break value `HH` and changes the `Indic_Conjunct_Break` data, so the tests must come from the matching UCD version.

## Collation (UTS #10 and DUCET)

### allkeys.txt

`allkeys.txt` is the Default Unicode Collation Element Table (DUCET). It starts with `@version 17.0.0`, then `@implicitweights` lines, then entries of the form `<cp>+ ; [.pppp.ssss.tttt]+ # comment` (§12.1).

- Each collation element has a primary (base letter), secondary (accents), and tertiary (case and variant) weight.
- `*` in place of `.` marks a variable element: spaces, punctuation, and symbols, which can be shifted to a fourth level.
- One codepoint mapping to several collation elements is an expansion; several codepoints mapping to one entry is a contraction.
- An element with primary weight 0 is ignorable; `[.0000.0000.0000]` is completely ignorable (§3.2).

Measured counts in the 17.0.0 file:

| Measure | Count |
| --- | --- |
| Total entries | 39,749 |
| Single-codepoint entries | 38,785 |
| Contractions | 964 (956 of length 2, 8 of length 3) |
| Distinct contraction starters | 77, each with its own single entry |
| Single entries expanding to more than one element | 3,998 |
| Single entries whose first element is variable | 8,496 |
| `@implicitweights` lines | 6 |

### Implicit weights

Every codepoint not listed in the table gets two collation elements, `[.AAAA.0020.0002][.BBBB.0000.0000]` (§10.1.2–10.1.3, Table 16):

| Class | AAAA | BBBB |
| --- | --- | --- |
| Tangut | FB00 | (CP − 17000) \| 8000 |
| Tangut Components | FB01 | (CP − 18800) \| 8000 |
| Tangut Supplement | FB00 | (CP − 17000) \| 8000 |
| Tangut Components Supplement | FB01 | (CP − 18800) \| 8000 |
| Nushu | FB02 | (CP − 1B170) \| 8000 |
| Khitan Small Script | FB03 | (CP − 18B00) \| 8000 |
| Core Han | FB40 + (CP >> 15) | (CP & 7FFF) \| 8000 |
| Other Han | FB80 + (CP >> 15) | (CP & 7FFF) \| 8000 |
| Everything else: unassigned, private use, noncharacters, surrogates | FBC0 + (CP >> 15) | (CP & 7FFF) \| 8000 |

- The Tangut, Nushu, and Khitan ranges apply to assigned codepoints only; unassigned codepoints in those blocks take FBC0 and up.
- Hangul syllables have no entries. Step 1 of the algorithm (NFD) decomposes them to conjoining jamo, which do (§10.1.5).
- For surrogates, an implementation may give them implicit weights "as if it were an unassigned code point"; they must never be ignorable or variable (§10.1.1).
- The Unicode 17 text gives the other-Han lead range as "FB80, FB84..FB85". Extensions at U+30000 and above need FB86; revision 55 (Unicode 18) corrects this. The formula, not the parenthetical range, is authoritative.
- A supplement block shares its base AAAA with the main block and counts BBBB from the main block's start, so Tangut Supplement (U+18D00–18D7F) sorts after all of Tangut. Counting from the supplement's own start instead would place U+18D00 among the first Tangut ideographs; the prototype had exactly that bug until the collation conformance test below exposed it.
- Within each class the order is codepoint order, so implicit-weighted codepoints never tie.

### How every codepoint gets weights

Measured over all 1,114,112 codepoints:

| Source | Codepoints |
| --- | --- |
| Explicit single entry | 38,785 |
| Hangul syllables through NFD to jamo | 11,172 |
| Tangut, Nushu, and Khitan implicit (assigned) | 7,925 |
| Core Han implicit (FB40: 12,800; FB41: 8,192) | 20,992 |
| Other Han implicit (FB80: 6,592; FB84: 32,768; FB85: 28,203; FB86: 13,429) | 80,992 |
| FBC0 and up (137,468 private use, 814,664 reserved, 2,048 surrogates, 66 noncharacters) | 954,246 |
| **Total** | **1,114,112** |

No canonically decomposable character other than the Hangul syllables lacks an explicit entry.

### The deterministic total order

One deterministic order of all 1,114,112 codepoints is derived in three steps:

1. **Collation elements.** Take the explicit entry, the Hangul jamo through NFD, or the implicit pair, with non-ignorable variable weighting: `*` weights are used as-is. Under the default "shifted" setting, the 8,496 variable characters would collapse at levels 1–3.
2. **Sort key.** Form the UCA sort key L1 | L2 | L3 from the non-zero weights.
3. **Ties.** Break ties first by the identical level, the codepoint's canonical decomposition (NFD, computed from the Unicode 17 `UnicodeData.txt`), then by codepoint, the deterministic comparison of UTS #10 Appendix A. The identical level alone is not enough for single codepoints, because canonical singletons such as U+212B and U+00C5 still tie. Skipping it misorders pairs such as U+2001 EM QUAD, whose NFD is U+2003, against U+2002 EN SPACE.

Measured results:

- Before step 3 there are 1,419 tie groups covering 6,324 codepoints, and 1,109,207 distinct sort keys. The largest group is the 962 completely ignorable codepoints. In total 1,640 codepoints are primary-ignorable and sort first.
- Ranks: U+0000 is rank 0; the first non-ignorable codepoint is at rank 1,640; U+0020 at 1,648; `a` at 12,142; `A` at 12,159; U+AC00 at 25,261; U+4E00 at 56,415; U+D800 at 161,100; U+E000 at 163,148; U+FFFE at 169,681; U+10FFFF at 1,114,110. The last codepoint is U+FFFD, whose fixed primary FFFD sorts above all implicit weights.
- The SHA-256 of the order, written as 3-byte big-endian codepoints, is `31548536a65d75e4f4e3f866d4bb5315ddbfe803edb7d0a018eebfb5c89257e0`. An earlier order without the identical level and with the Tangut supplement bug hashed to `85474f71…` and is superseded.

### Conformance

Measured against the official test files in the local Unicode 17.0.0 data:

| Test | ICU 70.1 (Unicode 14 rules) | ICU 78.3 (Unicode 17 rules) |
| --- | --- | --- |
| `GraphemeBreakTest.txt` | 756 of 766 | 766 of 766 |
| `WordBreakTest.txt` | 1,940 of 1,944 | 1,944 of 1,944 |
| `SentenceBreakTest.txt` | 512 of 512 | 512 of 512 |

The ICU 70 failures are all rules added after Unicode 14, such as Indic conjunct clusters (grapheme rule GB9c, Unicode 15.1), emoji ZWJ sequences, and Arabic and Syriac word breaks. Segmentation has to use the same Unicode version as tier 0.

`CollationTest_NON_IGNORABLE.txt` lists strings in the order the UCA must produce. Each test line is a codepoint followed by a probe character, so the order of the codepoints within each probe group was compared with the total order above: 197,767 lines, 286 disagreeing adjacent pairs. 285 of them are explained by expansions whose key is a strict prefix of another's (for example U+2A74 `⩴`, which collates as `: : =`): alone, the shorter key sorts first; with a probe appended, the longer one can. The remaining pair involves the combining probe U+0334, which canonical ordering moves inside U+01FE `Ǿ`. None is an error in the order of single codepoints.

Contractions do not change the order of single codepoints. They matter for strings: sorting strings needs the full algorithm with maximal-match contraction lookup (§3.5). Most contractions are Thai, Lao, and Tai Viet prevowel + consonant pairs; others include Cyrillic U+0438 U+0306 and Tibetan U+0FB2 U+0F71 U+0F80. The conformance data is `CollationTest.zip` (§12.2). CLDR's root collation is a tailored DUCET, so ICU's default order is not raw DUCET.

### DUCET across versions

- §6.8: "The contents of the DUCET will remain unchanged in any particular version of the UCA. However, the contents may change between successive versions."
- §1.9.2 lists stability of binary sort keys as a non-goal: "weights in the DUCET may change between versions."
- The change-management policy says weight changes for characters older than two years "should generally be disallowed" except for egregious errors; symbols, punctuation, and format controls are exempt.
- Every release renumbers primaries as characters are inserted. UCA 17 adjusted the implicit weighting of Tangut. UCA 18 gives U+FFFE the fixed primary 0200 and U+FFFF the fixed FFFF; in DUCET 17 both are ordinary FBC1 implicits.

The relative order of older characters is largely, but not absolutely, stable; absolute weights are not. The order is therefore pinned to a specific version, and IDs are never derived from weights or ranks. See [Atoms](../Storage/Atoms.md#unicode-versions).

## The UCD in XML (UAX #42, UAX #44)

UAX #42 §4.2 divides codepoints into four element types, each carrying `cp` or `first-cp`/`last-cp` and its properties as attributes: `char` (assigned, including private use), `noncharacter`, `surrogate`, and `reserved`. There is at most one element per codepoint (§4.1). The specification does not require complete coverage, but the `ucd.all` files cover the whole codespace. The flat files list every element; the grouped files factor shared attributes into groups. The `nounihan` and `unihan` variants split out the Unihan `k*` properties.

Measured in `ucd.all.flat.xml`:

| Element | Elements | Codepoints |
| --- | --- | --- |
| `char` | 159,869 | 297,334 (including 137,468 private use in 3 ranges) |
| `reserved` | 789 | 814,664 |
| `surrogate` | 3 | 2,048 |
| `noncharacter` | 18 | 66 |
| **Total** | | **1,114,112, none uncovered, no overlaps** |

Reserved, surrogate, and noncharacter ranges carry the full non-Unihan attribute set, 111 attributes against 112 on `char`, with default values such as `gc=Cn`, `sc=Zzzz`, `lb=XX`, `ea=N`, and `age="unassigned"`. Per-codepoint metadata for the entire codespace therefore comes from one file.

Largest General_Category totals, measured:

| gc | Codepoints |
| --- | --- |
| Cn | 814,730 (814,664 reserved + 66 noncharacters) |
| Lo | 141,062 |
| Co | 137,468 |
| So | 7,468 |
| Ll | 2,283 |
| Mn | 2,059 |
| Cs | 2,048 |
| Lu | 1,886 |

The file also holds blocks, named sequences, standardized variants, CJK radicals, emoji sources, and do-not-emit data. Emoji sequences are not in the XML; they are in the emoji data files.

### Per-codepoint properties

UAX #44 Table 7 groups the properties as General, Case, Emoji, Numeric, Normalization, Shaping and Rendering, Bidirectional, Identifiers, Segmentation, CJK, Miscellaneous, and Contributory. Attributes of particular use:

- `gc` General_Category; `sc` and `scx` Script and Script_Extensions, as ISO 15924 codes; `blk`; `age`; `na`, `na1`, and name aliases.
- `bc` Bidi_Class, `Bidi_M`, `bmg`, `bpt`, `bpb`; `ea` East_Asian_Width; `lb` Line_Break; `vo` Vertical_Orientation.
- `GCB`, `WB`, `SB`, and `InCB`, which drive segmentation.
- `ccc`, `dt`, `dm`, and the normalization quick checks; `nt` and `nv`; the case mappings `uc`, `lc`, `tc`, `cf`, `scf`, `NFKC_CF`.
- Identifier properties such as `XIDS`, `XIDC`, `Pat_Syn`, `Pat_WS`; emoji properties `Emoji`, `EPres`, `EMod`, `EBase`, `EComp`, `ExtPict`.
- CJK: `UIdeo` (measured: 101,996 codepoints), `Ideo`, `Radical`, and the IDS properties.
- Unihan, on `char` only, measured: `kDefinition` on 23,285 characters, `kRSUnicode` (normative) on 102,998, `kMandarin` on 44,348; also other readings, stroke counts, IRG sources, and variants.

## Stability policy

The Unicode Character Encoding Stability Policies guarantee:

- **Encoding stability:** "Once a character is encoded, it will not be moved or removed." The codepoint is the one fully stable identifier.
- **Names:** character names, formal aliases, and named sequences never change.
- **Normalization:** NFC, NFD, NFKC, and NFKD output is identical across versions for text assigned in both. Decomposition mappings and `ccc` never change once assigned.
- **Properties:** normative and informative properties are never removed, property domains are fixed, and property and value aliases are never removed or reassigned.
- **Fixed sets:** gc=Cc, gc=Co, gc=Cs, the 66 noncharacters, Pattern_Syntax, and Pattern_White_Space never change. No new General_Category values are added.
- Also: identifier and case-folding stability, new Bidi_Class values only with new controls, decimal digits in contiguous 0–9 runs, and `sc` ∈ `scx`.

Not guaranteed:

- Other properties may change as long as a character's identity is kept, including Script, Line_Break, the segmentation properties, East_Asian_Width, case mappings, and emoji properties.
- Contributory and provisional properties.
- Collation weights (see [DUCET across versions](#ducet-across-versions)).
- Segmentation rules, as with `Indic_Conjunct_Break` in 15.1 and `lb=HH` in 17.0.

Per-codepoint properties are therefore versioned by UCD version. Only the codepoint, name, decomposition mapping, `ccc`, and membership in Cc, Co, Cs, and the noncharacters are immutable.

## Emoji sequences (UTS #51)

UTS #51 defines the multi-codepoint emoji sequences:

- ED-13, modifier sequence: an emoji modifier base followed by a skin-tone modifier, U+1F3FB–U+1F3FF.
- ED-14, flag: two regional indicators.
- ED-14a, tag sequence: a base, tag characters U+E0020–U+E007E, and U+E007F, as in the England, Scotland, and Wales flags.
- ED-14c, keycap: `[0-9#*] FE0F 20E3`.
- ED-16, ZWJ sequence: elements joined by U+200D.
- ED-17: "all emoji sequences are single grapheme clusters: there is never a grapheme cluster boundary within an emoji sequence".

The grapheme rules GB9, GB11, GB12, and GB13 produce this. `Extended_Pictographic` is also pre-assigned to unassigned codepoints in emoji blocks (ED-4), so future ZWJ sequences already segment as one cluster. A family ZWJ sequence can have about ten codepoints. The RGI lists are a closed catalog of recommended emoji; segmentation is rule-based and open-ended.

Measured in the local Emoji 17.0 data:

| Data | Count |
| --- | --- |
| RGI ZWJ sequences | 1,614 |
| RGI modifier sequences | 665 |
| RGI flag sequences | 259 |
| RGI tag sequences | 3 |
| Keycap sequences | 12 |
| Basic emoji lines | 502 |

`emoji-test.txt` lists 3,944 fully-qualified, 1,029 minimally-qualified, 243 unqualified, and 9 component entries.

## Concept and language identifiers

### CILI

The Collaborative Interlingual Index (Global WordNet Association) gives language-independent concept IDs. An ILI ID is the letter `i` followed by a positive integer, allocated sequentially with no semantic structure; its URI is `http://globalwordnet.org/ili/i<N>`.

- **Data.** `ili.ttl` gives each ID as a Concept or Instance with an English definition and its Princeton WordNet 3.0 source; tab-separated maps link IDs to WordNet 3.0 and 3.1 offsets.
- **Measured in the local copy:** 117,659 IDs, 109,929 Concepts and 7,730 Instances; the WordNet 3.0 map by part of speech is n 82,115, v 13,767, a 7,463, s 10,693, r 3,621. The local copy (June 2024) is behind upstream, which has since added sense mappings and a pull-request proposal workflow.
- **New IDs** are proposed through WN-LMF with an English definition of 10–500 characters, and start as provisional.
- **License:** CC BY 4.0 or any later version, with attribution to the Global Wordnet Association.
- The Open Multilingual Wordnet lists 4,960 core ILIs.

### ISO 639 and BCP 47

- **ISO 639-3** (SIL, code tables dated 2026-04-15), measured: 7,929 identifiers; by scope 7,862 individual, 63 macrolanguages, 4 special; by type 7,084 living, 602 extinct, 215 historical, 24 constructed, 4 special; 184 have ISO 639-1 two-letter codes.
- **Terms of use:** the tables may be incorporated into software with attribution to SIL, identifiers must not be modified or extended except privately in qaa–qtz, and the code set must not be redistributed. The codes are referenced, not republished.
- **IANA Language Subtag Registry** (BCP 47, file date 2026-05-05), measured: 8,275 language subtags and 225 script subtags. The subtags are freely usable.

### CLDR

CLDR supplies the supplemental data, likely subtags, validity data, BCP 47 extensions, segmentation tailorings and suppressions (UTS #35 Part 1), and the root collation. The local files carry no version stamp. CLDR is under the Unicode License v3.

## Sources

- Unicode Standard Annex #29, [Unicode Text Segmentation](https://www.unicode.org/reports/tr29/tr29-47.html), revision 47, Unicode 17.0.0; [latest revision](https://www.unicode.org/reports/tr29/).
- Unicode Technical Standard #10, [Unicode Collation Algorithm](https://www.unicode.org/reports/tr10/tr10-53.html), revision 53, Unicode 17.0.0; [latest revision](https://www.unicode.org/reports/tr10/).
- Unicode, [Change Management for the Unicode Collation Algorithm](https://www.unicode.org/collation/ducet-changes.html) and [DUCET criteria](https://www.unicode.org/collation/ducet-criteria.html).
- Unicode Standard Annex #42, [Unicode Character Database in XML](https://www.unicode.org/reports/tr42/tr42-38.html), revision 38; [latest revision](https://www.unicode.org/reports/tr42/).
- Unicode Standard Annex #44, [Unicode Character Database](https://www.unicode.org/reports/tr44/tr44-36.html), revision 36; [latest revision](https://www.unicode.org/reports/tr44/).
- Unicode, [Unicode Character Encoding Stability Policies](https://www.unicode.org/policies/stability_policy.html).
- Unicode Technical Standard #51, [Unicode Emoji](https://www.unicode.org/reports/tr51/tr51-29.html), revision 29, Emoji 17.0; [latest revision](https://www.unicode.org/reports/tr51/).
- Unicode Technical Standard #35, [Unicode Locale Data Markup Language](https://www.unicode.org/reports/tr35/).
- Francis Bond, Piek Vossen, John P. McCrae, Christiane Fellbaum, [CILI: the Collaborative Interlingual Index](https://aclanthology.org/2016.gwc-1.9/), GWC 2016; [CILI repository](https://github.com/globalwordnet/cili) and [proposal guide](https://github.com/globalwordnet/cili/blob/master/PROPOSING_ILIS.md).
- [Open Multilingual Wordnet](https://omwn.org/).
- SIL International, [ISO 639-3 code tables and terms of use](https://iso639-3.sil.org/code_tables/download_tables).
- Unicode, [Unicode License v3](https://www.unicode.org/license.txt).
