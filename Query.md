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

Containers can be searched with gaps: every "Captain ␣ Name" in Moby Dick, reading what fills the gap.

## Shape

Fréchet distance finds matching shapes, and the content that has that shape. See [Physicality](Storage/Physicality.md).
