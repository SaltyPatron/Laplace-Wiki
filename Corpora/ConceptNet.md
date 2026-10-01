# ConceptNet

ConceptNet attests each edge of its assertions as the claim of its start, its relation, and its end, witnessed by every contributor the edge's sources name, and its relations page attests what each relation is described and exemplified as; the edge's URI, weight, dataset, license, and surface text are the claim's specifics and attest nothing of their own.

The source is ConceptNet 5.7's assertions, one edge on every line, with ConceptNet's own documentation of the file beside it. The documentation's pages [Downloads](https://github.com/commonsense/conceptnet5/wiki/Downloads), [Edges](https://github.com/commonsense/conceptnet5/wiki/Edges), [URI hierarchy](https://github.com/commonsense/conceptnet5/wiki/URI-hierarchy), and [Relations](https://github.com/commonsense/conceptnet5/wiki/Relations) are what the recipes quote.

## Sources

| Source | Witness | Uncertainty | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `conceptnet` | `ConceptNet`, and each contributor an edge's sources name | deviation 90 | `unicode`, `iso-639`, `wiktionary` | `assertions.csv` | [`assertions.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/conceptnet/assertions.recipe) |
| `conceptnet` | `ConceptNet` | deviation 90 | `unicode`, `iso-639`, `wiktionary` | `Relations.md` | [`relations.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/conceptnet/relations.recipe) |

The deviation is "this recipe's choice for a curated academic resource; the specification does not give one": the number is not settled, and [Corpora](README.md#not-settled) lists it among what stays missing.

A URI is a path. "Every object in ConceptNet has a URI that is structured like a path"; "Concept URIs contain the text of the concept, with spaces replaced by underscores"; a concept has "the initial /c", "a part that indicates its language", "a part with the concept text", and "an optional fourth component gives the part of speech" ([URI hierarchy](https://github.com/commonsense/conceptnet5/wiki/URI-hierarchy)). So a value that begins with `/` is recorded as the tuple of its parts, and a part's words, joined by `_`, as the tuple of the words: `/c/en/ice_cream/n` is `[c, en, [ice, cream], n]`, and an assertion's URI, "in a bracketed list", `/a/[/r/IsA/,/c/en/dog/,/c/en/animal/]`, is `[a, [[r, IsA], [c, en, dog], [c, en, animal]]]`.

## The assertions

A record is one line: five fields parted by tabs, no header row. "The five fields of each line are: The URI of the whole edge; The relation expressed by the edge; The node at the start of the edge; The node at the end of the edge; A JSON structure of additional information about the edge" ([Downloads](https://github.com/commonsense/conceptnet5/wiki/Downloads)). The recipe names the columns as [Edges](https://github.com/commonsense/conceptnet5/wiki/Edges) names them: `uri`, `rel`, `start`, `end`, and the JSON. The edge is its start, its relation, and its end; everything in the JSON is said of the edge itself; its `uri` is a key.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `start` | `/c/en/dog` | the subject, as the path its URI is | the first part of the claim | "The node at the start of the edge"; "The URI of the first argument of the assertion" |
| `rel` | `/r/IsA` | the predicate, as a path | the second part | "The relation expressed by the edge"; "The URI of the predicate of this assertion" |
| `end` | `/c/en/animal` | the object, as a path | `[[c, en, dog], [r, IsA], [c, en, animal]]` | "The node at the end of the edge"; "The URI of the second argument of the assertion" |
| `uri` | `/a/[/r/IsA/,/c/en/dog/,/c/en/animal/]` | ConceptNet's key to the edge, which the edge's own three parts already are: recorded nowhere | nothing | "The URI of the whole edge"; "A unique URI for the assertion being expressed" |
| `sources` in the JSON, each `contributor` in it | `"sources": [{"contributor": "/s/contributor/..."}]` | who witnessed the edge: each contributor named is a witness of its own and attests the claim with its specifics. An edge that names no contributor is attested by `ConceptNet` | the witness of the ledger row, not a claim | "sources: the sources that, when combined, say that this assertion should be true" |
| everything else in `sources` | the other members of each source object | specifics of the claim, under `sources` | among the claim's specifics | |
| `weight` in the JSON | `"weight": 1.0` | a specific of the claim, said of the edge; not taken for a score, because the documentation gives no scale | `[weight, 1.0]` among the claim's specifics | "weight: the strength with which this edge expresses this assertion. A typical weight is 1, but weights can be higher or lower. All weights are positive." |
| `dataset`, `license` in the JSON | URIs | specifics of the claim, each as the path its URI is | `[dataset, [d, ...]]`, `[license, value]` among the claim's specifics | "A URI representing the dataset, or the batch of data from a particular source that created this edge"; "A Creative Commons URI for the license that governs this data" |
| `surfaceText` in the JSON | a text, or `null` | a specific of the claim; `null` says nothing | `[surfaceText, text]` among the claim's specifics | "The original natural language text that expressed this statement. May be null, because not every statement was derived from natural language input." |
| an empty field | | nothing | none | |

The ledger row is the claim and its specifics, witnessed once by each contributor the edge names, or once by ConceptNet when it names none; the claim `[start, rel, end]` is what stands and plays its matchups as [Consensus](../Semantics/Consensus.md#matchups) describes. The row takes no column for a score, so it attests the claim as a win.

## The relations page

`Relations.md` is ConceptNet's page "Relations in ConceptNet 5": a table with a row for each relation, under the headings `Relation URI`, `Description`, and `Examples`. What a row says of a relation is said under the heading of its column; the relation's URI is a path, as above.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| the `Relation URI` cell | `/r/IsA` | the subject, as a path | `[r, IsA]` | [Relations](https://github.com/commonsense/conceptnet5/wiki/Relations) |
| the `Description` cell | "A is a subtype or a specific instance of B; every A is a B. ..." | said of the relation under `Description` | `[[r, IsA], Description, A is a subtype or a specific instance of B; every A is a B. ...]` | |
| the `Examples` cell | `car → vehicle; Chicago → city` | said of the relation under `Examples`, the cell as one text | `[[r, IsA], Examples, car → vehicle; Chicago → city]` | |
| every other line of the page | | not a row of the table: not a claim | none | |

The page attests what a relation is called and described as. It does not attest that any edge carries it: that is the assertions' to say.

## What is not read

The other documentation pages beside `Relations.md` — Downloads, Edges, URI hierarchy — are matched by no recipe and are not read; the recipes quote them, as this page does. Every other file under the root is not read either.
