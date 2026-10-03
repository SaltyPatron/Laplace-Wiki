# GeoNames

GeoNames attests what its gazetteer's tables say of each place, which is its name, latitude and longitude together; a geonameid is GeoNames's key to the place, recorded nowhere, by which the other tables point at it; the codes' own tables say what each code is; and the readme is not read.

One source, `geonames`, reads the GeoNames Gazetteer extract files: the `geoname` table, the alternate names, the hierarchy, and the tables of the codes they are written with. "The data format is tab-delimited text in utf8 encoding." Each recipe names its columns as [readme.txt](https://download.geonames.org/export/dump/readme.txt) does.

## Source

| Source | Witness | Trust | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `geonames` | `GeoNames Gazetteer` | class `UserCuratedResource` | `unicode`, `iso-639` | the nine files the recipes name below; every other `.txt` or `.md` as plain text | [`recipes/geonames`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/geonames) |

## The record

A record is one row of one file: fields parted by tabs, each recorded as written under its column's name; an empty field attests nothing. A place is its `name`, `latitude` and `longitude` together, the path of the three; `allCountries.txt` defines each under its geonameid (`key geonameid`), and every table that points at a place by geonameid reads it as the place (`refer geonameid geonames-geoname`), its file read after `allCountries.txt`. A code (`US.CA`, `A.ADM1`, `Europe/Andorra`, an ISO country code) is the content a code table defines and is recorded as written.

| File | Piece | Laplace reads it as | Claim recorded |
| --- | --- | --- | --- |
| `allCountries.txt` | the `geoname` table's 19 columns | the place, `[name, latitude, longitude]`; every other column said of it under the readme's name, `alternatenames` and `cc2` each value on its own | `[[Earth, 0, 0], feature code, AREA]`, `[[Roc Meler, 42.58765, 1.7418], alternatenames, Roc Mélé]` |
| `hierarchy.txt` | parentId; childId; type | both ids read as places; the row says together of the parent which child it has and of what type | `[[Earth, 0, 0], childId, [Europe, 48.69096, 9.14062]]`, `[[Earth, 0, 0], type, ADM]` |
| `admin1CodesASCII.txt` | code; name; name ascii; geonameid | the place the geonameid points at; its name and ascii name said of it; the code a key | `[[Sant Julià de Loria, …], name, Sant Julià de Loria]` |
| `admin2Codes.txt` | concatenated codes; name; asciiname; geonameId | the same | |
| `alternateNamesV2.txt` | alternateNameId; geonameid; isolanguage; alternate name; isPreferredName; isShortName; isColloquial; isHistoric; from; to | the place; each other column said of it; the row's own id a key | `[place, alternate name, Roc Mélé]`, `[place, isolanguage, fr]` |
| `countryInfo.txt` | the header's 19 columns | the country by its `#ISO` code; each other column said of it, `Languages` and `neighbours` each value on its own; the geonameid column read as the country's place | `[AD, Capital, Andorra la Vella]`, `[AD, geonameid, [Principality of Andorra, 42.55, 1.58333]]` |
| `featureCodes_en.txt` | the code; name; description | the code, as written; its name and description | `[A.ADM1, name, first-order administrative division]` |
| `iso-languagecodes.txt` | the header's columns | the language by its name; its codes | `[French, ISO 639-3, fra]` |
| `timeZones.txt` | the header's columns | the time zone by its id; the rest | `[Europe/Andorra, rawOffset, 1.0]` |

## Not read

`readme.txt` and every other `.txt` or `.md` under the root that no recipe names is not read: the source has no `reads` line.
