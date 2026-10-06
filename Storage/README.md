# Storage

Laplace stores all digital content as a self-deduplicating Merkle DAG with deterministic, lossless storage, laid out as geometry in four dimensions.

The storage exploits spatial datatypes and old technologies. Like Git and IPFS, the same content always has the same hash.

The PostGIS tables are the structure of the Census Bureau's MAF/TIGER applied to knowledge. TIGER's blocks are shared by overlapping hierarchies, tracts nesting in counties and states while ZCTAs, places, and school and congressional districts cross them, as content is shared by many trees; a GEOID is a structured pointer; an MTFCC class is an identifier system; a feature name is a lexicalization; the geocoder's normalize-and-resolve with a rating is pointer resolution with standing; and routing over classed edges is A* over strands. Laplace goes further: identity is content, not an assigned ID that changes with every vintage.

Laplace is both a Merkle DAG and an AST. Tree-sitter is the example: a grammar gives every file its syntax tree, and Laplace records that tree as content.

All digital content boils down to Unicode codepoints. Content is broken down into its smallest constituent components, the Merkle DAG of those components is persisted, and the content is stored as trajectories in the [space](Space.md).

- [Space](Space.md) is the 4-ball that everything is placed in.
- [Atoms](Atoms.md) are the codepoints, the floor of everything.
- [Compositions](Compositions.md) are built from atoms and from other compositions.
- [Identity](Identity.md) is the BLAKE3 hash that names every node.
- [Physicality](Physicality.md) is every node's real 4D coordinate and trajectory.
- [Ingestion](Ingestion.md) is how new content is deduplicated and recorded.
