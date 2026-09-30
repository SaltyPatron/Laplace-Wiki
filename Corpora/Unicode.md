# Unicode Character Database

The Unicode Character Database attests everything the standard says of a code point, the flat XML is the record of it, and the property files add only what the XML does not carry.

Unicode is the floor of everything: [Atoms](../Storage/Atoms.md) builds tier 0 from it, and [Research: Unicode](../Research/Unicode.md) records what the data defines and which parts are stable. This page is what the source attests once it is ingested: which piece of which file says what, of which code point.

## Source

| Source | Witness | Trust | After | Root | Recipes |
| --- | --- | --- | --- | --- | --- |
| `unicode` | `Unicode Character Database` | 1.0, the standard itself | nothing: it is first in [`recipes/order`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/order) | `UCD/Public/UCD/latest` | [`recipes/unicode`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/unicode), one per file |

Every file's witness is the database as a whole, and no file is lineage of another. A property is recorded under the name the standard writes: the XML attribute or the file's field name, never a name of Laplace's own. A value that is itself code points is recorded as the text those code points are, and a value the standard leaves empty attests nothing.

## The character database

`ucd.all.flat.xml` is the whole database in the flat form of [UAX #42](https://www.unicode.org/reports/tr42/): one element per code point or range, with every property as an attribute. It is read on every core, element by element.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| `<char cp="0041" ...>` | the character its `cp` names: the code point itself, a tier 0 atom | the subject | the `cp` attribute is the code point [UAX #42, 4.4.1](https://www.unicode.org/reports/tr42/) |
| `<char first-cp="4E00" last-cp="9FFF" ...>` | the range of code points: the path of its first and its last | the subject; what is said of a range is said of the range | `first-cp` and `last-cp` bound a range of code points [UAX #42](https://www.unicode.org/reports/tr42/) |
| `<reserved>`, `<noncharacter>`, `<surrogate>` | the code point or range the same way | the subject | the reserved, noncharacter, and surrogate code points [UAX #42](https://www.unicode.org/reports/tr42/) |
| every other attribute of the element: `gc`, `bc`, `ccc`, `dt`, `nt`, `nv`, `sc`, `scx`, `blk`, `age`, `na`, the binary properties, the Unihan `k` properties, and the rest | said of the code point under the attribute's name, the value as written | `[A, gc, Lu]`, `[A, sc, Latn]`, `[A, Upper, Y]` | the properties of [UAX #44](https://www.unicode.org/reports/tr44/), as UAX #42 names their attributes |
| `dm`, `lc`, `tc`, `uc`, `cf`, `scf`, `slc`, `stc`, `suc`, `bmg`, `bpb`, `FC_NFKC`, `NFKC_CF`, `NFKC_SCF`, `EqUIdeo`, `ideograph`, `first-cp`, `last-cp` | code points written in hex: recorded as the text they are | `[Å, dm, Å]` where the object is the decomposed text itself | the attributes UAX #42 defines as code point values |
| `#` in a value | the code point itself | the object is the character | the standard writes `#` for the code point itself in a mapping [UAX #42, 4.4.2](https://www.unicode.org/reports/tr42/) |
| `<name-alias alias="..." type="..."/>` inside a `char` | speaks of the character: each attribute said of it, together as one record | `[cp, alias, value]`, `[cp, type, value]` | "name-alias" [UAX #42, 4.4.3](https://www.unicode.org/reports/tr42/) |
| `<named-sequence cps="..." name="..."/>` | the sequence its `cps` names, as the text it is | `[sequence, name, value]` | [UAX #42, 4.4.5](https://www.unicode.org/reports/tr42/) |
| `<standardized-variant cps="..." desc="..." when="..."/>` | the sequence its `cps` names | `[sequence, desc, value]`, `[sequence, when, value]` | [UAX #42, 4.4.7](https://www.unicode.org/reports/tr42/) |
| `<cjk-radical number="..." radical="..." ideograph="..."/>` | the radical character | `[radical, number, value]`, `[radical, ideograph, character]` | [UAX #42, 4.4.8](https://www.unicode.org/reports/tr42/) |
| `<block first-cp="..." last-cp="..." name="..."/>` | the block its `name` names | `[block, first-cp, first]`, `[block, last-cp, last]` | [UAX #42, 4.4.4](https://www.unicode.org/reports/tr42/) |
| an empty attribute value | what the standard leaves empty | nothing | |
| `<description>`, `<repertoire>`, the `<group>` wrappers | structure, not statements | nothing | |

## The property files

Each file that says something the XML does not is a table of `;`-separated fields, comments after `#`, read by its own recipe. A row whose first field is a range `231A..231B` speaks of the range, recorded as the path of its first and its last. The claims are named exactly as the file's own header names its fields; a file that does not name a field gets a numbered column, and the number is only where the part is, never a recorded name.

| File | Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `PropertyAliases.txt` | short name; long name | the pair, as written | `[gc, General_Category]` | [UAX #44, 5.8](https://www.unicode.org/reports/tr44/) |
| `PropertyValueAliases.txt` | property; short value; long value | said of the property, under the short name | `[gc, Lu, Uppercase_Letter]` | [UAX #44, 5.8](https://www.unicode.org/reports/tr44/) |
| `allkeys.txt` | charList; collElement+ | said of the characters, under `collElement`, the elements of one entry as one text | `[cp, collElement, the elements as written]` | "entry := charList ';' collElement+ eol" [UTS #10, 12.1](https://www.unicode.org/reports/tr10/) |
| `allkeys.txt` | `@version`, `@implicitweights` | not read | nothing | |
| `decomps.txt` | code point; decomposition tag; decomposition | said of the code point under `decomposition tag`; the decomposition as the text it is under `decomposition` | `[cp, decomposition tag, value]`, `[cp, decomposition, text]` | the file's header, fields 0 to 2 |
| `ArabicShaping.txt` | field 1, the schematic name | said of the code point under `schematic name` | `[cp, schematic name, value]` | "Field 1: gives a short schematic name for that character" [UAX #44](https://www.unicode.org/reports/tr44/) |
| `ArabicShaping.txt` | fields 2 and 3 | not read: the XML gives them as `jt` and `jg` | nothing | |
| `CaseFolding.txt` | rows of status `T` | the mapping as the text it is, and the status, together | `[cp, mapping, text]`, `[cp, status, T]` | "T: special case for uppercase I and dotted uppercase I" [UAX #44](https://www.unicode.org/reports/tr44/) |
| `CaseFolding.txt` | rows of status `C`, `F`, `S` | not read: the XML gives them as `cf` and `scf` | nothing | |
| `SpecialCasing.txt` | rows with a condition list | each of lower, title, and upper as the text it is, with every condition of the list, together; an empty mapping attests nothing | `[cp, lower, text]`, `[cp, condition_list, Final_Sigma]` | "code; lower; title; upper; (condition_list;)?" [UAX #44](https://www.unicode.org/reports/tr44/) |
| `SpecialCasing.txt` | rows without a condition list | not read: the XML gives them as `lc`, `tc`, `uc` | nothing | |
| `PropList.txt`, `DerivedCoreProperties.txt`, `DerivedNormalizationProps.txt` | rows of `Hyphen`, `Grapheme_Link`, `Expands_On_NFC`, `Expands_On_NFD`, `Expands_On_NFKC`, `Expands_On_NFKD` | the pair of the code point and the property | `[cp, Hyphen]` | properties the XML does not carry; [UAX #44, 5.3](https://www.unicode.org/reports/tr44/) |
| `DerivedNormalizationProps.txt` | rows of `FC_NFKC` | the mapping as the text it is, under `FC_NFKC` | `[cp, FC_NFKC, text]` | |
| those three files | every other row | not read: the XML says the same | nothing | |
| `extracted/DerivedNumericValues.txt` | field 1 and field 3 | each said of the code point under `Numeric_Value`: the decimal writing and the fraction | `[½, Numeric_Value, 0.5]`, `[½, Numeric_Value, 1/2]` | "Derived Property: Numeric_Value" [UAX #44](https://www.unicode.org/reports/tr44/) |
| `NormalizationCorrections.txt` | fields 1, 2, 3 | the original and the corrected decomposition as text, under the header's own phrases; the version as a pair | `[cp, Original (erroneous) decomposition, text]`, `[cp, Corrected decomposition, text]`, `[cp, version]` | [UAX #44](https://www.unicode.org/reports/tr44/) |
| `DoNotEmit.txt` | fields 0, 1, 2 | the sequence and its replacement as a pair, each as text; the type under `DoNotEmit type` | `[sequence, replacement]`, `[sequence, DoNotEmit type, value]` | the file's header, fields 0 to 2 |
| `Index.txt` | index entry; code point | the pair, as written | `[LATIN CAPITAL LETTER A, A]` | "Index.txt is another exception. It uses a tab-delimited format, with field 0 consisting of an index entry string, and field 1 a code point." [UAX #44](https://www.unicode.org/reports/tr44/) |
| `EmojiSources.txt` | fields 1, 2, 3 | said of the code point or sequence under the header's field names | `[cp, DoCoMo Shift-JIS code, value]` | the file's header, fields 0 to 3 |
| `emoji-sequences.txt`, `emoji-zwj-sequences.txt` | type_field; description | said of the code points or range | `[sequence, type_field, RGI_Emoji_ZWJ_Sequence]`, `[sequence, description, text]` | "code_point(s) ; type_field ; description" [UTS #51](https://www.unicode.org/reports/tr51/) |
| `emoji-test.txt` | status | said of the code points | `[sequence, status, fully-qualified]` | "code points; status # emoji name" [UTS #51](https://www.unicode.org/reports/tr51/) |
| `emoji-test.txt` | the emoji name after `#`; `# group:` and `# subgroup:` lines | not read: comments | nothing | |
| `IdentifierStatus.txt` | Identifier_Status | said of the code point or range | `[cp, Identifier_Status, Allowed]` | [UTS #39, 3.1](https://www.unicode.org/reports/tr39/) |
| `IdentifierType.txt` | Identifier_Type, a space-separated set | each value said of the code point or range | `[cp, Identifier_Type, Uncommon_Use]` | [UTS #39, 3.1](https://www.unicode.org/reports/tr39/) |
| `confusables.txt`, `intentional.txt` | fields 0 and 1 | the pair, the source as written and the target as text | `[cp, text]` | [UTS #39, 4](https://www.unicode.org/reports/tr39/) |
| `confusables.txt` | field 2, always `MA` | not read | nothing | |
| `IdnaMappingTable.txt` | fields 1, 2, 3 | each as a pair with the code point or range: the status, the mapping as text, the further status | `[cp, mapped]`, `[cp, text]`, `[cp, NV8]` | [UTS #46, 5](https://www.unicode.org/reports/tr46/) |
| `Idna2008.txt` | IDNA2008_Category | said of the code point or range | `[cp, IDNA2008_Category, PVALID]` | "Field 1: IDNA2008_Category" |
| `USourceData.txt` | fields 1, 3 to 9 | said of the U-source identifier under the header's field names; the sources of field 6, parted by `*`, each on its own | `[identifier, Status, value]`, `[identifier, kRSUnicode, value]` | [UAX #38](https://www.unicode.org/reports/tr38/) and the file's header |
| `USourceData.txt` | field 2, when it is one code point `U+2B88A` | the pair of the identifier and the character | `[identifier, character]` | "Field 2: The Unicode code point of this ideograph, if any" |
| `ReadMe.txt`, `ucdxml.readme.txt` | ordinary text | observed, as [Attestations](../Semantics/Attestations.md#observations) says of ordinary content | nothing | |

Every file of the database not named here is not read: either the XML already says what it says, or no recipe exists for it yet. A file that is read is read whole; a row it does not name is not filled in.
