# Unicode Character Database

The Unicode Character Database attests the properties of a code point, and the flat XML is that witness.

The composition is a code point. The mask is the property being asked: name, category, decomposition, numeric value, script, and the rest of what the standard records of that code point. The value is the property the database assigns. This is the floor every higher composition is built from. [Unicode](../Unicode.md) records which properties the text model uses.

The witness is the database, trust 1.0. The file that carries it is `ucd.all.flat.xml` under `/vault/Data/UCD/Public/UCD/latest`. Loaded measure: 20,147,624 compositions from 239 MB. `UnicodeData.txt` and the other property files are the same witness split into tables. `properties.recipe` reads only the properties those files have and the XML does not, and states that every other row says what the XML says. `special-casing.recipe` reads only rows with a `condition_list`, because the other rows are the case mappings already read. `do-not-emit.recipe` states that the XML already gives those rows as its `instead` elements. Reading the text file beside the XML assigns the same property twice.

A code point property does not attest a word, a sense, or a dependency role. Those are higher compositions. Collation keys and emoji data are further statements the same database makes about the code point. They are not a second publisher.

The hop out of a code point is into the compositions built on it. Fanout at this tier is the number of properties recorded of one code point, not a lexical relation. [Pull](../../Semantics/Pull.md) walks relations between claims. A property of a code point pulls on the token that contains the code point. It does not pull on a synset.

## Files, breakdown, and caveats

Taken from the recipe files. A line in a block is a directive. The prose above it is that file's own account of what is read, what is not, and what a row becomes.

### `unicode/aliases.recipe`

The standard's own list of what each property's short name stands for: the two names, as written side by side.

```text
match PropertyAliases.txt
grammar table
separator ;
comment #
columns short long
claims
pair
subject in short
object in long
```

### `unicode/allkeys.recipe`

The Default Unicode Collation Element Table. UTS #10, 12.1 Allkeys File Format, names the two parts of an entry:   "`<entry>` := `<charList>` ';' `<collElement>`+ `<eol>`"   "`<charList>` := `<char>`+"   "`<collElement>` := "[" `<alt>` `<weight>` "." `<weight>` "." `<weight>` ("." `<weight>`)? "]"" Every entry says of its characters their collation elements, recorded as written. The elements of one entry are written one after another with nothing between them, and are not parted here. The "@version" and "@implicitweights" lines are not read (an @implicitweights line speaks of a range).

```text
match allkeys.txt
grammar table
separator ;
comment #
columns charList collElement
claims
subject in charList.range
attest collElement
```

### `unicode/arabic-shaping.recipe`

ArabicShaping.txt. The header:   "# Field 0: the code point of a character, in hexadecimal form."   "# Field 1: gives a short schematic name for that character."   "#   Note that this schematic name is considered a comment,"   "#   and does not constitute a formal property value."   "# Field 2: defines the joining type (property name: Joining_Type)"   "# Field 3: defines the joining group (property name: Joining_Group)" Only the schematic name is read here: Joining_Type and Joining_Group are what the XML gives as jt and jg.

```text
match ArabicShaping.txt
grammar table
separator ;
comment #
columns "code point" "schematic name" Joining_Type Joining_Group
claims
subject in "code point".cps
attest "schematic name"
```

### `unicode/case-folding.recipe`

CaseFolding.txt. The header names the fields:   "# `<code>`; `<status>`; `<mapping>`; # `<name>`"   "# T: special case for uppercase I and dotted uppercase I" Only the rows of status T are read here: the rows of status C, F and S are the mappings the XML gives as cf and scf. A row says its status and its mapping, as the text it is, together.

```text
match CaseFolding.txt
grammar table
separator ;
comment #
columns code status mapping
claims
together
subject in code.range
predicate mapping
object in mapping.cps
attest status
```

### `unicode/confusables.recipe`

UTS #39 confusables and intentional confusables. Neither file names its fields, and UTS #39 is not on this machine: what is recorded is the pair the row writes, in the row's order, each side as the text it is. The columns are numbered here only to say where a part is; no name is recorded. The third field of confusables.txt (always MA) is not read.

```text
match confusables.txt intentional.txt
grammar table
separator ;
comment #
columns 0 1 2
claims
pair
subject in 0.range
object in 1.cps
```

### `unicode/decomps.recipe`

The decompositions used in generating the Default Unicode Collation Element Table. The header:   "# Field 0: code point"   "# Field 1: decomposition tag"   "# Field 2: decomposition" The decomposition is recorded as the text it is.

```text
match decomps.txt
grammar table
separator ;
comment #
columns "code point" "decomposition tag" decomposition
claims
subject in "code point".cps
attest "decomposition tag"
claims
subject in "code point".cps
predicate decomposition
object in decomposition.cps
```

### `unicode/do-not-emit.recipe`

DoNotEmit.txt. The header:   "#    Field 0  A sequence of Unicode code point values"   "#    Field 1  A replacement sequence of Unicode code point values"   "#    Field 2  DoNotEmit type of the original character sequence" The XML gives the same rows as its "instead" elements (of, use, because), which the recipe for the XML does not read. Field 1 is described, not named: the sequence and its replacement are recorded as the pair the row writes, each as the text it is. A row whose sequence is a range speaks of the range.

```text
match DoNotEmit.txt
grammar table
separator ;
comment #
columns 0 1 "DoNotEmit type"
claims
pair
subject in 0.range
object in 1.cps
claims
subject in 0.range
attest "DoNotEmit type"
```

### `unicode/emoji-sequences.recipe`

UTS #51 emoji sequences: every row says of its code point or sequence its type_field and its description, under the names the file's header gives its fields:   "# Format:"   "#   code_point(s) ; type_field ; description # comments" (the header's list of fields calls the third "short name: CLDR short name of sequence"). The code points are recorded as the text they are. A row whose code_point(s) is a range (231A..231B) speaks of the range, recorded as the range it is: the path of its first and its last.

```text
match emoji-sequences.txt emoji-zwj-sequences.txt
grammar table
separator ;
comment #
columns code_point(s) type_field description
claims
subject in code_point(s).range
attest type_field description
```

### `unicode/emoji-sources.recipe`

EmojiSources.txt. The header:   "# Fields:"   "# 0: Unicode code point or sequence"   "# 1: DoCoMo Shift-JIS code"   "# 2: KDDI Shift-JIS code"   "# 3: SoftBank Shift-JIS code"

```text
match EmojiSources.txt
grammar table
separator ;
comment #
columns "Unicode code point or sequence" "DoCoMo Shift-JIS code" "KDDI Shift-JIS code" "SoftBank Shift-JIS code"
claims
subject in "Unicode code point or sequence".cps
attest "DoCoMo Shift-JIS code" "KDDI Shift-JIS code" "SoftBank Shift-JIS code"
```

### `unicode/emoji-test.recipe`

UTS #51 emoji keyboard/display test data: every row says of its code points their status. The header:   "# Format: code points; status # emoji name" The emoji name is written after the #, where the file writes its comments, and is not read; nor are the "# group:" and "# subgroup:" lines, which are comment lines that speak of the rows after them.

```text
match emoji-test.txt
grammar table
separator ;
comment #
columns "code points" status
claims
subject in "code points".cps
attest status
```

### `unicode/identifier-status.recipe`

UTS #39 Identifier_Status. The header:   "# Field 0: code point"   "# Field 1: Identifier_Status value" A row whose code point is a range speaks of the range, recorded as the range it is: the path of its first and its last.

```text
match IdentifierStatus.txt
grammar table
separator ;
comment #
columns "code point" Identifier_Status
claims
subject in "code point".cps
attest Identifier_Status
```

### `unicode/identifier-type.recipe`

UTS #39 Identifier_Type. The header:   "# Field 0: code point"   "# Field 1: set of Identifier_Type values" The values of a set are parted by spaces, and each is said of the code point. A row whose code point is a range speaks of the range, recorded as the range it is: the path of its first and its last.

```text
match IdentifierType.txt
grammar table
separator ;
comment #
columns "code point" Identifier_Type
claims
subject in "code point".cps
attest Identifier_Type
```

### `unicode/idna-mapping.recipe`

UTS #46 IDNA mapping table. The file does not name its fields, and UTS #46 is not on this machine: what is recorded is the pairs a row writes, the code point with each of its further fields, the second of them (a mapping, written as code points) as the text it is. The columns are numbered here only to say where a part is; no name is recorded. A row whose code point is a range speaks of the range, recorded as the range it is: the path of its first and its last.

```text
match IdnaMappingTable.txt
grammar table
separator ;
comment #
columns 0 1 2 3
claims
pair
subject in 0.range
object in 1
claims
pair
subject in 0.range
object in 2.cps
claims
pair
subject in 0.range
object in 3
```

### `unicode/idna2008.recipe`

The IDNA2008_Category property (RFC 5892's derived property). The header:   "# Field 0: Unicode code point value or range of code point values"   "# Field 1: IDNA2008_Category, consisting of one of these values" A row whose code point is a range speaks of the range, recorded as the range it is: the path of its first and its last.

```text
match Idna2008.txt
grammar table
separator ;
comment #
columns "code point" IDNA2008_Category
claims
subject in "code point".cps
attest IDNA2008_Category
```

### `unicode/index.recipe`

Index.txt, the index of character names. The file has no header. UAX #44:   "Index.txt is another exception. It uses a tab-delimited format, with field 0"   " consisting of an index entry string, and field 1 a code point." What is recorded is the pair the row writes, in the row's order: the index entry and the character. The columns are numbered here only to say where a part is; no name is recorded.

```text
match Index.txt
grammar table
separator tab
columns 0 1
claims
pair
subject in 0
object in 1.cps
```

### `unicode/normalization-corrections.recipe`

NormalizationCorrections.txt. The header:   "#   Field 0: Unicode code point"   "#   Field 1: Original (erroneous) decomposition"   "#   Field 2: Corrected decomposition"   "#   Field 3: Version of Unicode for which the correction was"   "#            entered into UnicodeData.txt, in n.n.n format." The decompositions are recorded as the text they are. Field 3 is described by a sentence, not a name: it is recorded as the pair of the code point and the version.

```text
match NormalizationCorrections.txt
grammar table
separator ;
comment #
columns "Unicode code point" 1 2 3
claims
subject in "Unicode code point".cps
predicate Original (erroneous) decomposition
object in 1.cps
claims
subject in "Unicode code point".cps
predicate Corrected decomposition
object in 2.cps
claims
pair
subject in "Unicode code point".cps
object in 3
```

### `unicode/numeric-values.recipe`

extracted/DerivedNumericValues.txt. The header:   "# Derived Property:   Numeric_Value"   "#  Field 1:"   "#    The values are based on field 8 of UnicodeData.txt, plus the fields"   "#  Field 2:"   "#    This field is empty; it used to be a copy of the numeric type."   "#  Field 3:"   "#    expressing the same numeric value either as a whole integer"   "#    where possible, or as a rational fraction such as "1/6"." Both writings of the value are said of the code point under the property's name. The XML gives the value once, as nv, written as UnicodeData.txt writes it. A row whose code point is a range speaks of the range.

```text
match DerivedNumericValues.txt
grammar table
separator ;
comment #
columns 0 1 2 3
claims
subject in 0.range
predicate Numeric_Value
object in 1
claims
subject in 0.range
predicate Numeric_Value
object in 3
```

### `unicode/properties.recipe`

The properties that the property files give and the XML does not: Hyphen (PropList.txt), Grapheme_Link (DerivedCoreProperties.txt), and Expands_On_NFC, Expands_On_NFD, Expands_On_NFKC, Expands_On_NFKD and FC_NFKC (DerivedNormalizationProps.txt). Every other row of these files says what the XML says. A row of a binary property writes the code point and the property: that pair is recorded. A row of FC_NFKC writes the code point, the property and the mapping, which is recorded as the text it is. The files do not name their fields; the columns are numbered here only to say where a part is. A row whose code point is a range speaks of the range, recorded as the range it is: the path of its first and its last.

```text
match PropList.txt DerivedCoreProperties.txt DerivedNormalizationProps.txt
grammar table
separator ;
comment #
columns 0 1 2
claims
pair
subject in 0.range
object in 1
claims
subject in 0.range
predicate in 1
object in 2.cps
```

### `unicode/readme.recipe`

The ReadMe files of the directories: ordinary text.

```text
match ReadMe.txt ucdxml.readme.txt
grammar text
```

### `unicode/source`

The Unicode Standard's data: the character database, the collation table, the emoji data. The floor of everything. The standard that defines these properties. Measured when it was loaded: 20,147,624 compositions from 239 MB, at 750 bytes each with their indexes and standings.

```text
witness Unicode Character Database
trust 1.0
root $LAPLACE_DATA/UCD/Public/UCD/latest
```

### `unicode/special-casing.recipe`

SpecialCasing.txt. The header names the fields:   "# `<code>`; `<lower>`; `<title>`; `<upper>`; (`<condition_list>`;)? # `<comment>`"   "# The `<condition_list>` is optional. Where present, it consists of one or more language IDs"   "# or casing contexts, separated by spaces." Only the rows that carry a condition_list are read here: the rows without one are the full case mappings the XML gives as lc, tc and uc. A row says each of its mappings together with its conditions: the mapping, as the text it is, and each condition of the list, are one record. A mapping the row leaves empty attests nothing.

```text
match SpecialCasing.txt
grammar table
separator ;
comment #
columns code lower title upper condition_list
claims
together
subject in code.range
predicate lower
object in lower.cps
attest condition_list
claims
together
subject in code.range
predicate title
object in title.cps
attest condition_list
claims
together
subject in code.range
predicate upper
object in upper.cps
attest condition_list
```

### `unicode/ucd.recipe`

The Unicode Character Database in XML (UAX #42), flat form: every codepoint, and every range of codepoints, with everything the standard says of it: [codepoint, property, value], the property and the value as the standard writes them. A character is recorded as the character it is, and a value that is itself codepoints as the text they are. The standard writes # for the codepoint itself. What the standard leaves empty attests nothing. A character's other names, the named sequences, the standardized variants, the radicals and the blocks are read the same way: each is the thing its own attribute names. Every thing is on lines of its own: the file is read in parts, on every core.

```text
match ucd.all.flat.xml
grammar xml
records
identity char cp.cp
identity char first-cp..last-cp
identity reserved cp.cp
identity reserved first-cp..last-cp
identity noncharacter cp.cp
identity noncharacter first-cp..last-cp
identity surrogate cp.cp
identity surrogate first-cp..last-cp
identity named-sequence cps.cps
identity standardized-variant cps.cps
identity cjk-radical radical.cps
identity block name
```

### `unicode/usource.recipe`

USourceData.txt, the U-source ideographs. The header:   "# Field 0: U-source identifier"   "# Field 1: Status"   "# Field 2: The Unicode code point of this ideograph, if any; otherwise, the code point specifies the encoded      ideograph to which this entry is related, generally as a variant"   "# Field 3: kRSUnicode property value (see UAX #38)"   "# Field 4: Virtual KangXi dictionary position"   "# Field 5: Ideographic Description Sequence (IDS)"   "# Field 6: Sources"   "# Field 7: General comments"   "# Field 8: kTotalStrokes property value (see UAX #38)"   "# Field 9: First residual stroke" Field 2 is described, not named: it is recorded as the pair of the identifier and the character, and the name given to its column here only says where it is. Only a field 2 that is one code point (U+2B88A) is read: one that writes several code points, or an identifier, or +2B756, is not. The sources of field 6 are written with * between them, and each is said of the identifier.

```text
match USourceData.txt
grammar table
separator ;
comment #
columns "U-source identifier" Status 2 kRSUnicode "Virtual KangXi dictionary position" "Ideographic Description Sequence (IDS)" Sources "General comments" kTotalStrokes "First residual stroke"
claims
subject in "U-source identifier"
attest Status kRSUnicode "Virtual KangXi dictionary position" "Ideographic Description Sequence (IDS)" Sources "General comments" kTotalStrokes "First residual stroke"
claims
pair
subject in "U-source identifier"
object in 2.cps
```

### `unicode/value-aliases.recipe`

The standard's own list of what each property's values stand for: the property, the value's short name, its long name.

```text
match PropertyValueAliases.txt
grammar table
separator ;
comment #
columns property short long
claims
subject in property
predicate in short
object in long
```
