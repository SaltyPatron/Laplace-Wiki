# ConceptNet

ConceptNet attests each edge of its assertions as the claim of its start, its relation, and its end, witnessed by every contributor the edge's sources name, and its relations page attests what each relation is described and exemplified as; its weight and surface text are said of the edge, and its URI, dataset, licence, process and activity are bookkeeping, read by nothing.

The source is ConceptNet 5.7's assertions, one edge on every line, with ConceptNet's own documentation of the file beside it. The documentation's pages [Downloads](https://github.com/commonsense/conceptnet5/wiki/Downloads), [Edges](https://github.com/commonsense/conceptnet5/wiki/Edges), [URI hierarchy](https://github.com/commonsense/conceptnet5/wiki/URI-hierarchy), and [Relations](https://github.com/commonsense/conceptnet5/wiki/Relations) are what the recipes quote.

## Sources

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `conceptnet` | `ConceptNet`, and each contributor an edge's sources name | class `UserCuratedResource` | `unicode`, `iso-639`, `wiktionary` | `assertions.csv` | [`assertions.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/conceptnet/assertions.recipe) |
| `conceptnet` | `ConceptNet` | class `UserCuratedResource` | `unicode`, `iso-639`, `wiktionary` | `Relations.md` | [`relations.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/conceptnet/relations.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior is the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

A URI is a path. "Every object in ConceptNet has a URI that is structured like a path"; "Concept URIs contain the text of the concept, with spaces replaced by underscores"; a concept has "the initial /c", "a part that indicates its language", "a part with the concept text", and "an optional fourth component gives the part of speech" ([URI hierarchy](https://github.com/commonsense/conceptnet5/wiki/URI-hierarchy)). The recipe takes a URI's pieces apart (`part … by /`): a concept is its text, the third piece, its `_` read as spaces, so `/c/en/ice_cream/n` is the term `ice cream`, paired with `en` and `n`; a relation is its name, `/r/IsA` is `IsA`. An edge's own URI is not read.

## The assertions

A record is one line: five fields parted by tabs, no header row. "The five fields of each line are: The URI of the whole edge; The relation expressed by the edge; The node at the start of the edge; The node at the end of the edge; A JSON structure of additional information about the edge" ([Downloads](https://github.com/commonsense/conceptnet5/wiki/Downloads)). The recipe names the columns as [Edges](https://github.com/commonsense/conceptnet5/wiki/Edges) names them: `uri`, `rel`, `start`, `end`, and the JSON. The edge is its start, its relation, and its end; everything in the JSON is said of the edge itself; its `uri` is a key.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `start` | `/c/en/dog` | the subject: the term, the URI's third piece with `_` read as a space (`start/3`); its language and part of speech, the second and fourth pieces, paired with it (`pair edge start/2 start/4 of start/3`) | the first part of the claim; `[dog, en]`, and `[dog, n]` where the URI gives a part of speech | "The node at the start of the edge"; "The URI of the first argument of the assertion" |
| `rel` | `/r/IsA` | the predicate: the relation's name, the URI's second piece (`rel/2`) | the second part | "The relation expressed by the edge"; "The URI of the predicate of this assertion" |
| `rel` `/r/ExternalURL` | `/r/ExternalURL` | not read: the line is skipped (`where rel is-not /r/ExternalURL`). Its end is a URL of the term on another site, which split at its slashes made `wiki` and `en.wiktionary.org` things of their own | none | "ExternalURL: Points to a URL outside of ConceptNet" |
| `end` | `/c/en/animal` | the object, as `start` is, its pieces paired with it the same way | `[dog, IsA, animal]` | "The node at the end of the edge"; "The URI of the second argument of the assertion" |
| `uri` | `/a/[/r/IsA/,/c/en/dog/,/c/en/animal/]` | bookkeeping: `omit`; the edge's own three parts already are it | nothing | "The URI of the whole edge"; "A unique URI for the assertion being expressed" |
| `sources` in the JSON, each `contributor` in it | `"sources": [{"contributor": "/s/contributor/..."}]` | who witnessed the edge: each contributor named is a witness of its own and attests the claim with its specifics. An edge that names no contributor is attested by `ConceptNet` | the witness of the attestation, not a claim | "sources: the sources that, when combined, say that this assertion should be true" |
| everything else in `sources` | the other members of each source object | not read: of a source object, only `contributor` | nothing | |
| `weight` in the JSON | `"weight": 1.0` | said of the edge (`attest edge json`); not taken for a score, because the documentation gives no scale | `[edge, weight, 1.0]` | "weight: the strength with which this edge expresses this assertion. A typical weight is 1, but weights can be higher or lower. All weights are positive." |
| `dataset`, `license` in the JSON | URIs | bookkeeping: `omit`, with `process` and `activity` | nothing | "A URI representing the dataset, or the batch of data from a particular source that created this edge"; "A Creative Commons URI for the license that governs this data" |
| `surfaceText` in the JSON | a text, or `null` | said of the edge, with `surfaceStart` and `surfaceEnd`; `null` says nothing | `[edge, surfaceText, text]` | "The original natural language text that expressed this statement. May be null, because not every statement was derived from natural language input." |
| an empty field | | nothing | none | |

The attestation is the claim and its specifics, witnessed once by each contributor the edge names, or once by ConceptNet when it names none; the claim `[start, rel, end]` is what stands and plays its matchups as [Consensus](../Semantics/Consensus.md#matchups) describes. The row takes no column for a score, so it attests the claim as a win.

## The relations page

`Relations.md` is ConceptNet's page "Relations in ConceptNet 5": a table with a row for each relation, under the headings `Relation URI`, `Description`, and `Examples`. What a row says of a relation is said under the heading of its column; the relation is its name, the URI after `/r/`.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| the `Relation URI` cell | `/r/IsA` | the subject: the relation's name | `IsA` | [Relations](https://github.com/commonsense/conceptnet5/wiki/Relations) |
| the `Description` cell | "A is a subtype or a specific instance of B; every A is a B. ..." | said of the relation under `Description` | `[IsA, Description, A is a subtype or a specific instance of B; every A is a B. ...]` | |
| the `Examples` cell | `car → vehicle; Chicago → city` | said of the relation under `Examples`, the cell as one text | `[IsA, Examples, car → vehicle; Chicago → city]` | |
| every other line of the page | | not a row of the table: not a claim | none | |

The page attests what a relation is called and described as. It does not attest that any edge carries it: that is the assertions' to say.

## What is not read

The other documentation pages beside `Relations.md` — Downloads, Edges, URI hierarchy — are matched by no recipe and are not read; the recipes quote them, as this page does. Every other file under the root is not read either.
