# 1. Unicode

The first operations fix one Unicode version and read every file tier 0 and segmentation are built from.

All digital content boils down to Unicode codepoints. Everything after this stage is computed from these files, and two installs agree only if they started from the same ones.

## Before this stage

Nothing. This is the start of the chain.

## Operations

### 1.1 Fix the version

- **In:** the Unicode release to build from.
- **Do:** choose one version of the Unicode data and the same version of the segmentation tooling. Tier 0 and segmentation always use the same Unicode version. A new version is adopted only when its data and its segmentation tooling are both final.
- **Out:** one version number that every later fingerprint depends on.
- **Check:** the segmentation library reports the same Unicode version as the data. ICU 70.1, on Unicode 14 rules, passed 756 of 766 grapheme tests, 1,940 of 1,944 word tests, and 512 of 512 sentence tests against the Unicode 17 files; ICU 78.3, on Unicode 17 rules, passed all of them. A mismatch fails the conformance tests in 1.7.
- **From:** [Atoms: Unicode versions](../Storage/Atoms.md#unicode-versions), [Research: Unicode: Conformance](../Research/Unicode.md#conformance).

### 1.2 Read the UCD XML

- **In:** `ucd.all.flat.xml` for the version.
- **Do:** read every element. UAX #42 divides codepoints into four element types, `char`, `reserved`, `surrogate`, and `noncharacter`, each carrying `cp` or `first-cp`/`last-cp` and its properties as attributes, with at most one element per codepoint. Reserved, surrogate, and noncharacter ranges carry the full non-Unihan attribute set with default values such as `gc=Cn`, `sc=Zzzz`, and `age="unassigned"`.
- **Out:** the properties of every codepoint: `gc`, `sc` and `scx`, `blk`, `age`, `na`; `bc`, `Bidi_M`, `ea`, `lb`, `vo`; `GCB`, `WB`, `SB`, and `InCB`, which drive segmentation; `ccc`, `dt`, `dm`, the normalization quick checks, `nt`, `nv`, and the case mappings; identifier properties; emoji properties; the CJK properties and, on `char` only, the Unihan properties.
- **Check:** the elements cover 1,114,112 codepoints, none uncovered, no overlaps. In 17.0.0: 159,869 `char` elements covering 297,334 codepoints, 789 `reserved` covering 814,664, 3 `surrogate` covering 2,048, 18 `noncharacter` covering 66.
- **From:** [Atoms: Unicode data](../Storage/Atoms.md#unicode-data), [Research: Unicode: The UCD in XML](../Research/Unicode.md#the-ucd-in-xml-uax-42-uax-44).

### 1.3 Read `allkeys.txt`

- **In:** the Default Unicode Collation Element Table for the version.
- **Do:** read the `@version` line, the `@implicitweights` lines, and every entry of the form `<cp>+ ; [.pppp.ssss.tttt]+`. Each collation element has a primary, secondary, and tertiary weight; `*` in place of `.` marks a variable element; one codepoint mapping to several elements is an expansion; several codepoints mapping to one entry is a contraction; an element with primary weight 0 is ignorable.
- **Out:** the explicit collation elements of every listed codepoint, and the implicit-weight ranges.
- **Check:** in 17.0.0: 39,749 entries, 38,785 single-codepoint, 964 contractions, 77 distinct contraction starters, 3,998 single entries expanding to more than one element, 8,496 single entries whose first element is variable, 6 `@implicitweights` lines.
- **From:** [Atoms: Unicode data](../Storage/Atoms.md#unicode-data), [Research: Unicode: allkeys.txt](../Research/Unicode.md#allkeystxt).

### 1.4 Read the normalization data

- **In:** `UnicodeData.txt`, or the `dm` and `ccc` attributes of the XML.
- **Do:** read every canonical decomposition mapping and combining class. These are needed in [4. Projection](Projection.md) to decompose Hangul syllables to jamo and to break ties at the identical level, and in [8. Content](Content.md) to record each source's normalization form as a filter.
- **Out:** the NFD of every codepoint.
- **Check:** no canonically decomposable character other than the 11,172 Hangul syllables lacks an explicit `allkeys.txt` entry.
- **From:** [Research: Unicode: How every codepoint gets weights](../Research/Unicode.md#how-every-codepoint-gets-weights).

### 1.5 Read the segmentation data

- **In:** the `Grapheme_Cluster_Break`, `Word_Break`, `Sentence_Break`, `Indic_Conjunct_Break`, and `Extended_Pictographic` properties, from the XML.
- **Do:** these drive the three kinds of UAX #29 segment: extended grapheme clusters by rules GB1–GB999, words by WB1–WB999, sentences by SB1–SB998. Line breaking is a separate specification, UAX #14, and is not a segmentation tier.
- **Out:** the property values every segmentation decision reads.
- **Check:** the conformance tests in 1.7.
- **From:** [Research: Unicode: Text segmentation](../Research/Unicode.md#text-segmentation-uax-29).

### 1.6 Read the bidi, CJK, and emoji data, and the flags

- **In:** the bidi data; the CJK data, including the Unihan properties; `emoji-sequences.txt`, `emoji-zwj-sequences.txt`, and the rest of the emoji data; the ISO and other flags that go with them.
- **Do:** read them in full. Emoji sequences are not in the XML; they are in the emoji data files. An emoji sequence is a modifier sequence, a flag of two regional indicators, a tag sequence, a keycap, or a ZWJ sequence, and every emoji sequence is a single grapheme cluster.
- **Out:** the flags that go with tier 0, from the standard's own lists.
- **Check:** in Emoji 17.0: 1,614 RGI ZWJ sequences, 665 modifier sequences, 259 flag sequences, 3 tag sequences, 12 keycap sequences.
- **From:** [Atoms: Unicode data](../Storage/Atoms.md#unicode-data), [Research: Unicode: Emoji sequences](../Research/Unicode.md#emoji-sequences-uts-51).

### 1.7 Run the conformance tests

- **In:** `GraphemeBreakTest.txt`, `WordBreakTest.txt`, `SentenceBreakTest.txt`, and `CollationTest_NON_IGNORABLE.txt` for the version.
- **Do:** every test line marks every position of a sequence with `÷` or `×`; conformance means reproducing every mark. The tests must come from the matching UCD version, because Unicode 17 adds the Line_Break value `HH` and changes the `Indic_Conjunct_Break` data.
- **Out:** proof that the segmentation tooling is at the version fixed in 1.1.
- **Check:** 766 of 766 grapheme, 1,944 of 1,944 word, 512 of 512 sentence lines pass. For the collation order this stage feeds into, the 286 disagreeing adjacent pairs out of 197,767 lines are all explained by expansions whose key is a strict prefix of another's, or by the combining probe; none is an error in the order of single codepoints.
- **From:** [Research: Unicode: Conformance tests](../Research/Unicode.md#conformance-tests), [Research: Unicode: Conformance](../Research/Unicode.md#conformance).

## What this stage leaves behind

- The codespace: all 1,114,112 codepoints, U+0000 to U+10FFFF, including unassigned, private-use, surrogate, and noncharacter codepoints. The scope is never reduced to the codepoints in use.
- Every codepoint's properties, collation elements, decomposition, segmentation classes, and flags, at one version.
- The proof that the segmentation tooling is at that version.

## What is stable and what is not

Per the Unicode stability policy, once a character is encoded it is never moved or removed; names never change; normalization output is identical across versions for text assigned in both; decomposition mappings and `ccc` never change once assigned; `gc=Cc`, `gc=Co`, `gc=Cs`, and the 66 noncharacters never change. Collation weights, segmentation rules and properties, script, line break, case mappings, and emoji properties can change. The codepoint is the one fully stable identifier, which is why an ID is derived from the codepoint and never from a weight or a rank.

## Without this stage

There is no codespace to place, no order to place it in, and no segmentation to break content with. Nothing after it can be versioned or fingerprinted.
