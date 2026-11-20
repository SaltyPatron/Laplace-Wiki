# Unicode Character Database

The Unicode Character Database attests everything the standard says of a code point, the flat XML is the record of it, and the property files add only what the XML does not carry.

Unicode is Tier 0, the floor of the entire Merkle DAG: [Atoms](../Storage/Atoms.md) places all 1,114,112 Unicode scalar values onto the $S^3$ shell (`tier0.bin`) and packs fixed deterministic character properties into the 256-bit `tier0.flags` ROM ([Research: Unicode](../Research/Unicode.md)). This page specifies what `unicode` attests during corpus ingestion: properties not already answered directly from `tier0.flags`, multi-codepoint decompositions and sequences, confusables, IDNA tables, and UTS #51 emoji names, versions, and palette hierarchies.

## Source

| Source | Witness | Trust class | After | Root | Recipes |
| --- | --- | --- | --- | --- | --- |
| `unicode` | `Unicode Character Database` source trunk | class `StandardsDerived` (prior `0.95`) | nothing: first in [`recipes/order`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/order) | `UCD/Public/UCD/latest` | [`recipes/unicode/`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/unicode) |

Every file shares the single `Unicode Character Database` witness trunk. Hexadecimal code points and sequences (`0041`, `231A..231B`, `1F468 200D 1F4BB`) resolve directly to the canonical Tier-0 atoms or multi-atom UTF-8 compositions they denote (`codepoints`, `range`), and empty property values attest nothing.

## The character database (`ucd.all.flat.xml`)

`ucd.all.flat.xml` ([UAX #42](https://www.unicode.org/reports/tr42/)) carries one element per code point or range, parsed in parallel across cores by [`ucd.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/unicode/ucd.recipe):

| Piece | Laplace reads it as | Attestation recorded | Specification |
| --- | --- | --- | --- |
| `<char cp="0041" ...>`, `<reserved>`, `<noncharacter>`, `<surrogate>` | Tier-0 atom (`cp`) or `[first-cp, last-cp]` range | subject | [UAX #42, §4.4.1](https://www.unicode.org/reports/tr42/) |
| Properties materialized in `tier0.flags` (`gc`, `bc`, `ccc`, `dt`, `nt`, `sc`, `blk`, `age`, `ea`, `lb`, `GCB`, `WB`, `SB`, binary flags) | served in $O(1)$ from mmap'd `tier0.flags` (`perfcache`), not duplicated as rows | read directly from `tier0.flags` | [UAX #44](https://www.unicode.org/reports/tr44/) |
| Remaining attributes (`na`, `na1`, `nv`, `scx`, `JSN`, Unihan `k*` properties) | attested of the code point or range | `[A, Name, LATIN CAPITAL LETTER A]` (aliased via `PropertyAliases.txt`) | [UAX #44](https://www.unicode.org/reports/tr44/), [UAX #38](https://www.unicode.org/reports/tr38/) |
| Code-point mapping attributes (`dm`, `lc`, `tc`, `uc`, `cf`, `scf`, `bmg`, `bpb`, `FC_NFKC`, `NFKC_CF`, `EqUIdeo`, ...; `#` = self) | decoded from hex to the target character/sequence entity | `[Å, Decomposition_Mapping, …]` | [UAX #42, §4.4.2](https://www.unicode.org/reports/tr42/) |
| `<name-alias>`, `<named-sequence>`, `<standardized-variant>`, `<cjk-radical>`, `<block>` | character aliases, named/variant code-point sequences, CJK radicals, and named blocks | attested on the atom, sequence, radical, or block | [UAX #42, §4.4.3–4.4.8](https://www.unicode.org/reports/tr42/) |

## The supplementary property, UTS #10/#39/#46, & UTS #51 emoji files

Each table under `recipes/unicode/` adds properties and sequences not carried in `ucd.all.flat.xml`:

| File | Piece | Laplace reads it as | Attestation recorded | Specification |
| --- | --- | --- | --- | --- |
| `PropertyAliases.txt`, `PropertyValueAliases.txt` | short/long property & value names | canonical property and enumerated-value equivalences (`na` ↔ `Name`, `Lu` ↔ `Uppercase_Letter`) | `[gc, General_Category]`, `[gc, Lu, Uppercase_Letter]` | [UAX #44, §5.8](https://www.unicode.org/reports/tr44/) |
| `allkeys.txt` | `charList ; collElement+` | DUCET collation weights (`allkeys.recipe`, underpinning Tier-0 $S^3$ placement) | `[cp_or_seq, collElement, weights]` | [UTS #10, §12.1](https://www.unicode.org/reports/tr10/) |
| `decomps.txt`, `ArabicShaping.txt`, `CaseFolding.txt` (`T`), `SpecialCasing.txt` (conditional), `PropList.txt` / `Derived*Props.txt` (non-XML rows), `DerivedNumericValues.txt`, `NormalizationCorrections.txt`, `DoNotEmit.txt`, `Index.txt` | supplementary UCD tables | non-redundant mappings, numeric fractions (`1/2`), conditional casing (`Final_Sigma`), and index entries | attested per UCD table recipe | [UAX #44](https://www.unicode.org/reports/tr44/) |
| `EmojiSources.txt`, `emoji-sequences.txt`, `emoji-zwj-sequences.txt` | carrier mappings, `type_field`, `description` | emoji carrier mappings and RGI/ZWJ sequence descriptions | `[sequence, RGI_Emoji_ZWJ_Sequence]`, `[sequence, description]` | [UTS #51](https://www.unicode.org/reports/tr51/) |
| `emoji-test.txt` (`emoji-test.recipe`) | `sequence ; status # display E<ver> name` plus `# group: …` and `# subgroup: …` headers | parsed by compiled `emoji_palette` grammar (`format emoji_palette`): **retains UTS #51 `status`, `emoji name`, `emoji version` (`E<major>.<minor>`), and `[group, subgroup]` palette taxonomy** while omitting only the redundant inline display glyph (`omit display`) | `[sequence, status]`, `[sequence, emoji name, name]`, `[sequence, emoji version, version]`, `[sequence, group_name, subgroup_name]` | [UTS #51, §1.5.2](https://www.unicode.org/reports/tr51/) |
| `IdentifierStatus.txt`, `IdentifierType.txt`, `confusables.txt`, `intentional.txt`, `link-*.txt` | security status, usage types, visual confusables, linkification rules | UTS #39 / UTS #58 identifier security and confusable skeleton pairs | `[source_seq, target_seq]`, `Identifier_Status`, `Identifier_Type` | [UTS #39](https://www.unicode.org/reports/tr39/) |
| `IdnaMappingTable.txt`, `Idna2008.txt` | IDNA status & mapped sequences | UTS #46 and RFC 5892 domain-name mappings | `[cp, mapped_seq]`, `IDNA2008_Category` | [UTS #46](https://www.unicode.org/reports/tr46/) |
| `USourceData.txt`, `RadicalStrokeIndex.txt`, `*Test.txt` (`break-tests`, `normalization-tests`, `bidi-character-tests`) | U-source ideographs and conformance test vectors | ideograph metadata and normative segmentation/normalization/bidi conformance cases | attested per recipe | [UAX #38](https://www.unicode.org/reports/tr38/), [UAX #29](https://www.unicode.org/reports/tr29/), [UAX #15](https://www.unicode.org/reports/tr15/), [UAX #9](https://www.unicode.org/reports/tr9/) |
| `ReadMe.txt`, `ucdxml.readme.txt` | plain text | observed documentation files (`readme.recipe`) | none | |

## Relations

`PropertyAliases.txt` and `PropertyValueAliases.txt` tie XML short attribute handles (`na`, `dm`, `gc`, `Lu`) directly to their full UAX #44 property and value identities, while `emoji-test.recipe` already preserves full UTS #51 emoji names, versions, and `# group:` / `# subgroup:` palette classifications via `format emoji_palette`.
