# ConceptNet

ConceptNet attests an assertion of a relation between two concepts.

The composition is an edge: two concepts and a relation. The mask is the relation. The value is the assertion, one edge a line. Witness ConceptNet, deviation 90, the recipe's choice. Root `/vault/Data/ConceptNet`. Its own documentation of the edges, the URI hierarchy, and the relations is read beside the file. That documentation attests what the relation names mean. It is not a second copy of the edge list. Measured, not loaded: 254,147,905 compositions from 10,157 MB. [Relations Research](../Relations.md#local-datasets) counts 34,074,917 edges and 50 relations in this file.

An assertion does not attest a wordnet sense, a frame, or a dependency role unless the concept's URI says which inventory it came from. Where the URI names another witness, that is lineage or a hop, and it is not independent agreement with that witness. Fanout is the number of edges leaving a concept. [Pull](../../Semantics/Pull.md) caps it. ConceptNet is the commonsense tier in [Relations Research](../Relations.md), beside ATOMIC, and it is not ATOMIC.

## Files, breakdown, and caveats

Taken from the recipe files. A line in a block is a directive. The prose above it is that file's own account of what is read, what is not, and what a row becomes.

### `conceptnet/assertions.recipe`

One edge on every line, five fields parted by tabs, no header row. ConceptNet's documentation (Downloads):   "The five fields of each line are: The URI of the whole edge; The relation expressed by the edge; The node at the    start of the edge; The node at the end of the edge; A JSON structure of additional information about the edge" and (Edges) names the fields: uri, rel, start, end, and in the JSON weight, sources, license, dataset, surfaceText. The edge is its start, its relation and its end. Its uri and everything in the JSON are said of the edge itself.  (URI hierarchy) "Every object in ConceptNet has a URI that is structured like a path"; "Concept URIs contain the text of the concept, with spaces replaced by underscores"; a concept has "the initial /c", "a part that indicates its language", "a part with the concept text", and "an optional fourth component gives the part of speech". So   /c/en/ice_cream/n   is   [c, en, [ice, cream], n] and an assertion's URI, "in a bracketed list", /a/[/r/IsA/,/c/en/dog/,/c/en/animal/], is   [a, [[r, IsA], [c, en, dog], [c, en, animal]]]  (Edges) "sources: the sources that, when combined, say that this assertion should be true": each "contributor" among them is a witness of its own and attests the edge. An edge that names no contributor is attested by ConceptNet. (Edges) "weight: the strength with which this edge expresses this assertion. A typical weight is 1, but weights can be higher or lower. All weights are positive." It gives no scale, so the weight is recorded as what is said of the edge and is not taken for a score.

```text
match assertions.csv
grammar table
columns uri rel start end json
specifics
claims
subject in start
predicate in rel
object in end
json json
witnesses sources contributor
attest uri
```

### `conceptnet/relations.recipe`

ConceptNet's page "Relations in ConceptNet 5": a table, a row for each relation, under the headings the page gives:   | Relation URI | Description | Examples   | /r/IsA | A is a subtype or a specific instance of B; every A is a B. ... | car → vehicle; Chicago → city What a row says of a relation is said under the heading of its column.

```text
match Relations.md
grammar lines
claims
predicate Description
claims
predicate Examples
```

### `conceptnet/source`

ConceptNet 5.7's assertions: one edge on every line. ConceptNet's own documentation of the file (Downloads, Edges, URI hierarchy, Relations) is beside it, in "documentation", and is read as the text it is. The deviation is this recipe's choice for a curated academic resource; the specification does not give one. Measured, not loaded: 254,147,905 compositions from 10,157 MB, at 750 bytes each with their indexes and standings.

```text
witness ConceptNet
deviation 90
root $LAPLACE_DATA/ConceptNet
```
