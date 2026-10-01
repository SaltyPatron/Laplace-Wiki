# Query

Laplace finds content by computing its ID and coordinates on the client and looking them up with spatial indexes.

## Lookup by ID

With tier 0 [memory-mapped](Storage/Atoms.md#generation), the client deterministically produces the coordinates of the real Merkle DAG of any content. The UAX #29 decomposition of "Sherlock Holmes" is:

```text
[[S,h,e,r,l,o,c,k], ' ', [H,o,l,m,e,s]]
```

That trunk has one deterministic [ID](Storage/Identity.md) for all of it.

## Containers and occurrences

GIN finds every container of that ID, such as every sentence that contains a word, and GiST indexes the geometry. Lookups by ID exploit the spatial datatypes.

## Files

File metadata trees are searchable the same way as content: "Show me all ISO 100 images."

## Gaps

Containers can be searched with gaps: every "Captain ␣ Name" in Moby Dick, reading what fills the gap. See [Research: Corpus Search](Research/Corpus-Search.md) and [Research: Prototype](Research/Prototype.md#queries).

## Shape

Shape is the tree. A composition is a tree of constituents across tiers, and its trajectory is that tree recorded in order. Fréchet distance, Fréchet distance tolerant of *k* outliers, DTW, and EDR compare those trees. Each measure answers a different kind of difference. See [Physicality](Storage/Physicality.md) and [Research: Numerics](Research/Numerics.md).

The comparison adds a semantic relation the ID does not. Two records with different timestamps, request ids, or line numbers are different content, so their IDs differ. Their trees can still be the same pattern. A close shape says so.

Error logs from an application's telemetry are that case. One log has a shape. Across 1,000 clients and 10,000 repositories, that shape can lie very close to 50,000 other logs. Those 50,000 are the same pattern, and finding the pattern once is finding all of them.

The measure that skips the variable vertices, or tolerates that jitter, is the one that holds the pattern together. Favoring it is the [firmware](Semantics/Firmware.md). The trees stay the records.

## Functions in queries

The perf-cache is also available inside the database as native functions, so queries can compute IDs and coordinates in place instead of scanning tables. Such a function is evaluated once when the query is planned, and the query becomes an index lookup on the result.
