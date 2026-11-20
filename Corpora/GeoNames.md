# GeoNames

GeoNames attests what its gazetteer's tables say of each place, which is its name, latitude and longitude together; a geonameid is GeoNames's internal pointer to the place, recorded nowhere, by which the other tables point at it; the codes' own tables say what each code is; and the readme is not read.

One source, `geonames`, reads the GeoNames Gazetteer UTF-8 tab-delimited extract files: the `geoname` table (`allCountries.txt`), alternate names, administrative/parent hierarchy, country metadata, and code tables. Each recipe names its columns as [readme.txt](https://download.geonames.org/export/dump/readme.txt) specifies.

## Source

| Source | Witness | Trust class | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `geonames` | `GeoNames Gazetteer` source trunk | class `UserCuratedResource` | `unicode`, `iso-639` | Nine gazetteer tables (`allCountries.txt`, `hierarchy.txt`, `admin1CodesASCII.txt`, `admin2Codes.txt`, `alternateNamesV2.txt`, `countryInfo.txt`, `featureCodes_en.txt`, `iso-languagecodes.txt`, `timeZones.txt`) | [`recipes/geonames/`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/geonames) |

## The record

A record is one tab-separated row; an empty field attests nothing. Every place is its canonical `[name, latitude, longitude]` composition, keyed in `allCountries.txt` by `geonameid` (`key geonameid`) so companion tables resolve `geonameid` via `refer geonameid geonames-geoname` directly to `[name, latitude, longitude]` and record the numeric `geonameid` nowhere (`modification date` columns are registry bookkeeping and omitted). Feature, country, administrative, and timezone codes (`US.CA`, `A.ADM1`, `Europe/Andorra`, `AD`) are highway/reference identifiers recorded as written, cross-bracing with [ISO 639](ISO-639.md) and [Natural Earth](Natural-Earth.md).

| File | Piece | Laplace reads it as | Attestation recorded |
| --- | --- | --- | --- |
| `allCountries.txt` | 19 `geoname` columns | place `[name, latitude, longitude]` keyed by `geonameid`; `asciiname`, `alternatenames`, `feature class`, `feature code`, `country code`, `cc2`, `admin1..4`, `population`, `elevation`, `dem`, `timezone` attested of the place (`modification date` omitted) | `[[Earth, 0, 0], feature code, AREA]`, `[[Roc Meler, 42.58765, 1.7418], alternate name, Roc Mélé]` |
| `hierarchy.txt` | `parentId`; `childId`; `type` | both IDs resolved via `refer` to their places, forming one hierarchy edge | `[parent_place, hierarchy_type, child_place]` |
| `admin1CodesASCII.txt`, `admin2Codes.txt` | `code`; `name`; `asciiname`; `geonameid` | `geonameid` resolved to its place; administrative code and names attested | `[place, admin_code, AD.06]` |
| `alternateNamesV2.txt` | `alternateNameId`; `geonameid`; `isolanguage`; `alternate name`; flags (`isPreferredName`, `isShortName`, `isColloquial`, `isHistoric`, `from`, `to`) | `alternateNameId` omitted (`key`); `geonameid` resolved to `place`; multilingual name lexicalizations (`[name, isolanguage, place]`) and link/Wikidata codes where `isolanguage` is `wkdt`/`link` | `[place, isolanguage, alternate name]` (including `wkdt` Wikidata QIDs `Q...`) |
| `countryInfo.txt` | 19 country columns | ISO country code (`#ISO`), linked to its resolved `geonameid` place, `Capital`, `Continent`, `CurrencyCode`, `Languages`, `neighbours`, `ISO3`, `fips` | `[AD, Capital, Andorra la Vella]`, `[AD, place]` |
| `featureCodes_en.txt` | `code`; `name`; `description` | feature code (`A.ADM1`), title, and definition | `[A.ADM1, first-order administrative division, description]` |
| `iso-languagecodes.txt` | ISO 639-3, 639-2, 639-1, `Language Name` | language code equivalences and English name | `[fra, Language Name, French]` |
| `timeZones.txt` | `CountryCode`; `TimeZoneId`; `GMT` / `DST` / `rawOffset` | IANA timezone ID and UTC offsets | `[Europe/Andorra, rawOffset, 1.0]` |

## Relations

In target form ([10. Recipes](../Sequence/Recipes.md#1011-disposition-every-recovered-field)), pointer column names (`geonameid`, `childId`, `parentId`) appear in zero claims, `alternateNamesV2.txt` binds multilingual names `[alternate_name, isolanguage, place]` and retains `isolanguage = wkdt` Wikidata QIDs (`Q...`) as shared highway nodes, and `modification date` bookkeeping is omitted.
