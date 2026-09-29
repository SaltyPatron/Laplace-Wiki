# GeoNames

GeoNames attests a place and the names and hierarchy recorded for it.

The composition is a place. The masks are the ones `readme.txt` defines column by column: the geoname record, its alternate names, its place in the hierarchy, and the code tables. The value is the column. Witness GeoNames Gazetteer, trust 0.67, because its own readme asks readers to correct it. The recipe reads the refresh directory. There is no live directory.

A place name does not attest a wordnet sense of the common noun inside the name, and it does not attest a dependency role. The hierarchy is a hop from a place to its parent place. Fanout is the number of children and alternate names leaving a record. [Pull](../../Semantics/Pull.md) caps that fanout. The language of an alternate name hops to [ISO 639](ISO-639.md). The code tables attest what a feature code means. They are not a second copy of the geoname rows.

## Files, breakdown, and caveats

Taken from the recipe files. A line in a block is a directive. The prose above it is that file's own account of what is read, what is not, and what a row becomes.

### `geonames/admin1-codes.recipe`

readme.txt:   "admin1CodesASCII.txt     : names in English for admin divisions. Columns: code, name, name ascii, geonameid"

```text
match admin1CodesASCII.txt
grammar table
columns code name "name ascii" geonameid
claims
subject in code
attest *
```

### `geonames/admin2-codes.recipe`

readme.txt:   "admin2Codes.txt          : names for administrative subdivision 'admin2 code' (UTF8), Format : concatenated codes `<tab>`name `<tab>` asciiname `<tab>` geonameId"

```text
match admin2Codes.txt
grammar table
columns "concatenated codes" name asciiname geonameId
claims
subject in "concatenated codes"
attest *
```

### `geonames/alternate-names.recipe`

The table 'alternate names'. readme.txt:   "alternateNamesV2.zip     : alternate names with language codes and geonameId, file with iso language codes, with new columns from and to"   "The table 'alternate names' :"   "alternateNameId   : the id of this alternate name, int"   "geonameid         : geonameId referring to id in table 'geoname', int"   "isolanguage       : iso 639 language code 2- or 3-characters, optionally followed by a hyphen and a countrycode for country specific variants (ex:zh-CN) or by a variant name (ex: zh-Hant); 4-characters 'post' for postal codes and 'iata','icao' and faac for airport codes, fr_1793 for French Revolution names,  abbr for abbreviation, link to a website (mostly to wikipedia), wkdt for the wikidataid, varchar(7)"   "alternate name    : alternate name or name variant, varchar(400)"   "isPreferredName   : '1', if this alternate name is an official/preferred name"   "isShortName       : '1', if this is a short name like 'California' for 'State of California'"   "isColloquial      : '1', if this alternate name is a colloquial or slang term. Example: 'Big Apple' for 'New York'."   "isHistoric        : '1', if this alternate name is historic and was used in the past. Example 'Bombay' for 'Mumbai'."   "from          : from period when the name was used"   "to          : to period when the name was used" Every row says of its alternateNameId what each other column holds, under the column's name as the readme writes it. The ids are numbers GeoNames gives its own records (readme: "geonameid : integer id of record in geonames database"; "geonameId referring to id in table 'geoname'"). A number names a record only as that kind of id, so each is recorded as the path of the column's own name and the number.

```text
match alternateNamesV2.txt
grammar table
columns alternateNameId geonameid isolanguage "alternate name" isPreferredName isShortName isColloquial isHistoric from to
kind alternateNameId alternateNameId
kind geonameid geonameid
claims
subject in alternateNameId
attest *
```

### `geonames/country-info.recipe`

readme.txt:   "countryInfo.txt          : country information : iso codes, fips codes, languages, capital ,..." The file begins with 49 lines of remarks, each beginning with #; its 50th line is its header row, and begins with # too: "#ISO    ISO3    ISO-Numeric    fips    Country    ..." So the lines before the header are skipped by their number, and no comment character is named (one would take the header away with the remarks). The first column is read as the file writes it, #ISO; it is the subject, so that name is not recorded. countryInfo.txt, line 45: "# The column 'languages' lists the languages spoken in a country ordered by the number of speakers." Languages and neighbours are written as several values with commas between them.

```text
match countryInfo.txt
grammar table
header
claims
subject in "#ISO"
attest *
```

### `geonames/feature-codes.recipe`

readme.txt:   "featureCodes.txt         : name and description for feature classes and feature codes" The file here is featureCodes_en.txt. The readme names what the second and third fields are (name, description) and what they are said of (feature classes and feature codes); it gives the first column no name of its own. That column is the subject, so whatever it is called here is never recorded.

```text
match featureCodes_*.txt
grammar table
columns "feature classes and feature codes" name description
claims
subject in "feature classes and feature codes"
attest name description
```

### `geonames/geoname.recipe`

The 'geoname' table. readme.txt:   "allCountries.zip         : all countries combined in one file, see 'geoname' table for columns"   "The data format is tab-delimited text in utf8 encoding."   "The main 'geoname' table has the following fields :"   "geonameid         : integer id of record in geonames database"   "name              : name of geographical point (utf8) varchar(200)"   "asciiname         : name of geographical point in plain ascii characters, varchar(200)"   "alternatenames    : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)"   "latitude          : latitude in decimal degrees (wgs84)"   "longitude         : longitude in decimal degrees (wgs84)"   "feature class     : see <http://www.geonames.org/export/codes.html,> char(1)"   "feature code      : see <http://www.geonames.org/export/codes.html,> varchar(10)"   "country code      : ISO-3166 2-letter country code, 2 characters"   "cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters"   "admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)"   "admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80)"   "admin3 code       : code for third level administrative division, varchar(20)"   "admin4 code       : code for fourth level administrative division, varchar(20)"   "population        : bigint (8 byte int)"   "elevation         : in meters, integer"   "dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat."   "timezone          : the iana timezone id (see file timeZone.txt) varchar(40)"   "modification date : date of last modification in yyyy-MM-dd format" Every row says of its geonameid what each other column holds, under the column's name as the readme writes it. alternatenames and cc2 are "comma separated": each of their values is said on its own. The ids are numbers GeoNames gives its own records (readme: "geonameid : integer id of record in geonames database"; "geonameId referring to id in table 'geoname'"). A number names a record only as that kind of id, so each is recorded as the path of the column's own name and the number.

```text
match allCountries.txt
grammar table
columns geonameid name asciiname alternatenames latitude longitude "feature class" "feature code" "country code" cc2 "admin1 code" "admin2 code" "admin3 code" "admin4 code" population elevation dem timezone "modification date"
kind geonameid geonameid
claims
subject in geonameid
attest *
```

### `geonames/hierarchy.recipe`

readme.txt:   "hierarchy.zip        : parentId, childId, type. The type 'ADM' stands for the admin hierarchy modeled by the admin1-4 codes. The other entries are entered with the user interface. The relation toponym-adm hierarchy is not included in the file, it can instead be built from the admincodes of the toponym." A row has no identifier of its own: what it says of its parentId (the childId, and the type) it says together.

```text
match hierarchy.txt
grammar table
columns parentId childId type
claims
together
subject in parentId
attest childId type
```

### `geonames/language-codes.recipe`

readme.txt:   "iso-languagecodes.txt    : iso 639 language codes, as used for alternate names in file alternateNames.zip" The file has a header row: "ISO 639-3    ISO 639-2    ISO 639-1    Language Name". Language Name is the one column no row leaves empty; every row says of it the codes the other columns hold.

```text
match iso-languagecodes.txt
grammar table
header
claims
subject in "Language Name"
attest *
```

### `geonames/source`

The GeoNames gazetteer's extract files: the 'geoname' table, the alternate names, the hierarchy, and the tables of the codes they are written with. readme.txt documents every file and names every column. readme.txt's title: "Readme for GeoNames Gazetteer extract files" Entering unrated (Glicko-2's stock deviation, 350, trust 0.67), as tatoeba's source does for a source its users write; the specification does not give one. readme.txt: "please do use the wiki-style edit interface on our website <https://www.geonames.org> to correct inaccuracies and to add new records."

```text
witness GeoNames Gazetteer
trust 0.67
root $LAPLACE_DATA/.refresh-*/GeoNames
reads text
```

### `geonames/time-zones.recipe`

readme.txt:   "timeZones.txt            : countryCode, timezoneId, gmt offset on 1st of January, dst offset to gmt on 1st of July (of the current year), rawOffset without DST" The file has a header row of its own, and its names are the ones recorded, as the file writes them.

```text
match timeZones.txt
grammar table
header
claims
subject in TimeZoneId
attest *
```
