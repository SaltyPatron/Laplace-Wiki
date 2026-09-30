# GeoNames

GeoNames attests what its gazetteer's tables say of each place, alternate name, and code under the column names its readme gives, and its readme itself is observed text that attests nothing.

One source, `geonames`, reads the GeoNames Gazetteer extract files: the `geoname` table, the alternate names, the hierarchy, and the tables of the codes they are written with. "The data format is tab-delimited text in utf8 encoding." [readme.txt](https://download.geonames.org/export/dump/readme.txt), "Readme for GeoNames Gazetteer extract files", documents every file and names every column, and the recipes take their column names from it, or from the file's own header row where it has one. Every predicate on this page is a column name as the readme or the header writes it. Each file is read by its own recipe, one section below per file, in the order the recipes are listed.

## Source

| Source | Witness | Trust | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `geonames` | `GeoNames Gazetteer` | trust 0.67 | `unicode`, `iso-639` | the nine files the recipes name below, under the source's root; every other `.txt` or `.md` file under it as plain text (`reads text`) | [`recipes/geonames`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/geonames), one per file |

The source file says `trust 0.67` and, of it: "Entering unrated (Glicko-2's stock deviation, 350, trust 0.67), as tatoeba's source does for a source its users write; the specification does not give one." It quotes the readme: "please do use the wiki-style edit interface on our website <https://www.geonames.org> to correct inaccuracies and to add new records." The number is the recipe writer's choice, and [Corpora](README.md#not-settled) lists it among what stays missing. Every file's witness is the gazetteer as a whole, and no file is lineage of another.

## The record

A record is one row of one file: fields parted by tabs, each recorded as written under its column's name, and an empty field attests nothing. In the `geoname` table and the alternate names, an id is a kind: "The ids are numbers GeoNames gives its own records ... A number names a record only as that kind of id, so each is recorded as the path of the column's own name and the number", `[geonameid, 2643743]`, `[alternateNameId, 1]`. In every other file the recipe names no kind, and an id is the number as written. Each thing a row says is a claim, a tuple as [Claims](../Semantics/Claims.md#tuples) defines it, and its tier is one above its highest part, as [Compositions](../Storage/Compositions.md#tiers) requires.

## admin1CodesASCII.txt

"admin1CodesASCII.txt : names in English for admin divisions. Columns: code, name, name ascii, geonameid" [readme.txt](https://download.geonames.org/export/dump/readme.txt). The recipe names the columns as the readme does.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| code | the subject: the admin1 code, as written | the first part of every claim of the row | "admin1 code : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code" |
| name | said of the code under the column's name | `[code, name, value]` | "names in English for admin divisions" |
| name ascii | said of the code under the column's name | `[code, name ascii, value]` | |
| geonameid | said of the code under the column's name; the number as written, not a kind | `[code, geonameid, number]` | |

## admin2Codes.txt

"admin2Codes.txt : names for administrative subdivision 'admin2 code' (UTF8), Format : concatenated codes \<tab>name \<tab> asciiname \<tab> geonameId" [readme.txt](https://download.geonames.org/export/dump/readme.txt). The recipe names the columns as the readme does.

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| concatenated codes | the subject: the admin2 code, as written | the first part of every claim of the row | "admin2 code : code for the second administrative division, a county in the US, see file admin2Codes.txt" |
| name | said of the code under the column's name | `[concatenated codes, name, value]` | |
| asciiname | said of the code under the column's name | `[concatenated codes, asciiname, value]` | |
| geonameId | said of the code under the column's name; the number as written, not a kind | `[concatenated codes, geonameId, number]` | |

## alternateNamesV2.txt

"alternateNamesV2.zip : alternate names with language codes and geonameId, file with iso language codes, with new columns from and to" [readme.txt](https://download.geonames.org/export/dump/readme.txt). "Every row says of its alternateNameId what each other column holds, under the column's name as the readme writes it."

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| alternateNameId | the subject: the alternate name, `[alternateNameId, N]` | the first part of every claim of the row | "alternateNameId : the id of this alternate name, int" |
| geonameid | the place, `[geonameid, M]`, said of the alternate name under the column's name | `[[alternateNameId, N], geonameid, [geonameid, M]]` | "geonameid : geonameId referring to id in table 'geoname', int" |
| isolanguage | said of the alternate name under the column's name, as written: a language code, or one of the other marks the readme lists | `[[alternateNameId, N], isolanguage, en]` | "isolanguage : iso 639 language code 2- or 3-characters, optionally followed by a hyphen and a countrycode for country specific variants (ex:zh-CN) or by a variant name (ex: zh-Hant); 4-characters 'post' for postal codes and 'iata','icao' and faac for airport codes, fr_1793 for French Revolution names, abbr for abbreviation, link to a website (mostly to wikipedia), wkdt for the wikidataid, varchar(7)" |
| alternate name | said of the alternate name under the column's name: the name, as content | `[[alternateNameId, N], alternate name, text]` | "alternate name : alternate name or name variant, varchar(400)" |
| isPreferredName | said of the alternate name under the column's name; empty attests nothing | `[[alternateNameId, N], isPreferredName, 1]` | "isPreferredName : '1', if this alternate name is an official/preferred name" |
| isShortName | the same | `[[alternateNameId, N], isShortName, 1]` | "isShortName : '1', if this is a short name like 'California' for 'State of California'" |
| isColloquial | the same | `[[alternateNameId, N], isColloquial, 1]` | "isColloquial : '1', if this alternate name is a colloquial or slang term. Example: 'Big Apple' for 'New York'." |
| isHistoric | the same | `[[alternateNameId, N], isHistoric, 1]` | "isHistoric : '1', if this alternate name is historic and was used in the past. Example 'Bombay' for 'Mumbai'." |
| from | said of the alternate name under the column's name | `[[alternateNameId, N], from, value]` | "from : from period when the name was used" |
| to | said of the alternate name under the column's name | `[[alternateNameId, N], to, value]` | "to : to period when the name was used" |

## countryInfo.txt

"countryInfo.txt : country information : iso codes, fips codes, languages, capital ,..." [readme.txt](https://download.geonames.org/export/dump/readme.txt). The recipe reads the file's own header row: "The file begins with 49 lines of remarks, each beginning with #; its 50th line is its header row, and begins with # too: `#ISO ISO3 ISO-Numeric fips Country ...` So the lines before the header are skipped by their number, and no comment character is named (one would take the header away with the remarks)."

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| the first 49 lines | remarks: not rows (`skip 49`) | none | the comment lines of [countryInfo.txt](https://download.geonames.org/export/dump/countryInfo.txt) |
| the 50th line | the header: the columns' names, as the file writes them | none | the header row of [countryInfo.txt](https://download.geonames.org/export/dump/countryInfo.txt) |
| `#ISO` | the subject: the country, by its ISO code, as written. "The first column is read as the file writes it, #ISO; it is the subject, so that name is not recorded" | the first part of every claim of the row | |
| ISO3, ISO-Numeric, fips, Country, Capital, Area(in sq km), Population, Continent, tld, CurrencyCode, CurrencyName, Phone, Postal Code Format, Postal Code Regex, EquivalentFipsCode | each said of the country under the header's name for it (`attest *`) | `[code, Country, value]`, `[code, Capital, value]`, `[code, Continent, value]` | the header row of [countryInfo.txt](https://download.geonames.org/export/dump/countryInfo.txt) |
| Languages | several values with commas between them: each said of the country on its own under `Languages` (`list Languages ,`) | `[code, Languages, es-AR]` | "The column 'languages' lists the languages spoken in a country ordered by the number of speakers." [countryInfo.txt](https://download.geonames.org/export/dump/countryInfo.txt), line 45 |
| geonameid | said of the country under the header's name; the number as written, not a kind | `[code, geonameid, number]` | |
| neighbours | several values with commas between them: each said of the country on its own under `neighbours` (`list neighbours ,`) | `[code, neighbours, value]` | |

## featureCodes_en.txt

"featureCodes.txt : name and description for feature classes and feature codes" [readme.txt](https://download.geonames.org/export/dump/readme.txt). The recipe matches `featureCodes_*.txt`; "The file here is featureCodes_en.txt. The readme names what the second and third fields are (name, description) and what they are said of (feature classes and feature codes); it gives the first column no name of its own. That column is the subject, so whatever it is called here is never recorded."

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| the first field | the subject: the feature class or feature code, as written, such as `A.ADM1` | the first part of every claim of the row | "feature class : see <http://www.geonames.org/export/codes.html>"; "feature code : see <http://www.geonames.org/export/codes.html>" |
| the second field | said of the code under `name` | `[A.ADM1, name, first-order administrative division]` | "name and description for feature classes and feature codes" |
| the third field | said of the code under `description` | `[A.ADM1, description, text]` | "name and description for feature classes and feature codes" |

## allCountries.txt

"allCountries.zip : all countries combined in one file, see 'geoname' table for columns" [readme.txt](https://download.geonames.org/export/dump/readme.txt). "The main 'geoname' table has the following fields", and the recipe names the columns as the readme does: "Every row says of its geonameid what each other column holds, under the column's name as the readme writes it."

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| geonameid | the subject: the place, `[geonameid, N]` | the first part of every claim of the row | "geonameid : integer id of record in geonames database" |
| name | said of the place under the column's name: the name, as content | `[[geonameid, N], name, value]` | "name : name of geographical point (utf8) varchar(200)" |
| asciiname | said of the place under the column's name | `[[geonameid, N], asciiname, value]` | "asciiname : name of geographical point in plain ascii characters, varchar(200)" |
| alternatenames | several names with commas between them: each said of the place on its own under `alternatenames` (`list alternatenames ,`) | `[[geonameid, N], alternatenames, value]` | "alternatenames : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)" |
| latitude | said of the place under the column's name | `[[geonameid, N], latitude, value]` | "latitude : latitude in decimal degrees (wgs84)" |
| longitude | said of the place under the column's name | `[[geonameid, N], longitude, value]` | "longitude : longitude in decimal degrees (wgs84)" |
| feature class | said of the place under the column's name | `[[geonameid, N], feature class, A]` | "feature class : see <http://www.geonames.org/export/codes.html>, char(1)" |
| feature code | said of the place under the column's name | `[[geonameid, N], feature code, ADM1]` | "feature code : see <http://www.geonames.org/export/codes.html>, varchar(10)" |
| country code | said of the place under the column's name | `[[geonameid, N], country code, value]` | "country code : ISO-3166 2-letter country code, 2 characters" |
| cc2 | several codes with commas between them: each said of the place on its own under `cc2` (`list cc2 ,`) | `[[geonameid, N], cc2, value]` | "cc2 : alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters" |
| admin1 code | said of the place under the column's name | `[[geonameid, N], admin1 code, value]` | "admin1 code : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)" |
| admin2 code | said of the place under the column's name | `[[geonameid, N], admin2 code, value]` | "admin2 code : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80)" |
| admin3 code | said of the place under the column's name | `[[geonameid, N], admin3 code, value]` | "admin3 code : code for third level administrative division, varchar(20)" |
| admin4 code | said of the place under the column's name | `[[geonameid, N], admin4 code, value]` | "admin4 code : code for fourth level administrative division, varchar(20)" |
| population | said of the place under the column's name | `[[geonameid, N], population, value]` | "population : bigint (8 byte int)" |
| elevation | said of the place under the column's name | `[[geonameid, N], elevation, value]` | "elevation : in meters, integer" |
| dem | said of the place under the column's name | `[[geonameid, N], dem, value]` | "dem : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat." |
| timezone | said of the place under the column's name | `[[geonameid, N], timezone, value]` | "timezone : the iana timezone id (see file timeZone.txt) varchar(40)" |
| modification date | said of the place under the column's name | `[[geonameid, N], modification date, value]` | "modification date : date of last modification in yyyy-MM-dd format" |

A code a place carries is recorded as written, and nothing is filled in between it and the rows of the code's own table.

## hierarchy.txt

"hierarchy.zip : parentId, childId, type. The type 'ADM' stands for the admin hierarchy modeled by the admin1-4 codes. The other entries are entered with the user interface. The relation toponym-adm hierarchy is not included in the file, it can instead be built from the admincodes of the toponym." [readme.txt](https://download.geonames.org/export/dump/readme.txt). "A row has no identifier of its own: what it says of its parentId (the childId, and the type) it says together."

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| parentId | the subject: the parent, the number as written, not a kind | the first part of both claims of the row | "parentId" |
| childId | said of the parent under the column's name | `[parentId, childId, number]` | "childId" |
| type | said of the parent under the column's name | `[parentId, type, ADM]` | "The type 'ADM' stands for the admin hierarchy modeled by the admin1-4 codes. The other entries are entered with the user interface." |

The row says its claims `together`: it is one record, the path of its claims, witnessed once, and its claims within it. A row that says only one thing, because its other field is empty, is that one claim.

## iso-languagecodes.txt

"iso-languagecodes.txt : iso 639 language codes, as used for alternate names in file alternateNames.zip" [readme.txt](https://download.geonames.org/export/dump/readme.txt). The recipe reads the file's own header row, "ISO 639-3 ISO 639-2 ISO 639-1 Language Name", and says: "Language Name is the one column no row leaves empty; every row says of it the codes the other columns hold."

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| Language Name | the subject: the language, by its name, as written | the first part of every claim of the row | the header row |
| ISO 639-3 | said of the language under the header's name; empty attests nothing | `[language name, ISO 639-3, code]` | the header row |
| ISO 639-2 | the same | `[language name, ISO 639-2, code]` | the header row |
| ISO 639-1 | the same | `[language name, ISO 639-1, code]` | the header row |

The codes are those of ISO 639; [ISO 639](ISO-639.md) is the source that reads the standard itself, and this file is not lineage of it.

## timeZones.txt

"timeZones.txt : countryCode, timezoneId, gmt offset on 1st of January, dst offset to gmt on 1st of July (of the current year), rawOffset without DST" [readme.txt](https://download.geonames.org/export/dump/readme.txt). "The file has a header row of its own, and its names are the ones recorded, as the file writes them."

| Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- |
| TimeZoneId | the subject: the time zone, by its id, as written | the first part of every claim of the row | "timezoneId"; the header writes it `TimeZoneId` |
| every other column of the header | said of the time zone under the header's name for it, not the readme's (`attest *`) | `[TimeZoneId, header name, value]` | "countryCode, ... gmt offset on 1st of January, dst offset to gmt on 1st of July (of the current year), rawOffset without DST" |

## Not read

`readme.txt`, and every other `.txt` or `.md` file under the root that no recipe above names, is read as plain text through the source's `reads text`: ordinary content, observed as [Attestations](../Semantics/Attestations.md#observations) says, and attesting nothing. A file of any other kind that no recipe names is not read. No file of the gazetteer says anything of the words inside a name: a name is content, said of its place as a whole.
