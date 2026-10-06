# Glossary

Every term the documentation uses, defined once, with the page that owns it.

| Term | Definition | Owner |
| --- | --- | --- |
| atom | a codepoint, an entity of tier 0; its physicality is a POINT ZM holding its own ID | [Atoms](../Storage/Atoms.md) |
| attestation | a link between IDs: a strand and the witness that pulls on it, with the outcome and the games played; a strand in a record path under the witness's trunk, as built a row of `attestation` | [Attestations](../Semantics/Attestations.md#strands) |
| bank | the mask of one semantic group (a part of speech, a dependency relation, a kind), its bits the frozen slots of one list | [Types](Types.md#masks) |
| claim | a tuple of entities with referential integrity, a composition whose path relates them; the address of a standing | [Claims](../Semantics/Claims.md) |
| composition | an entity of tier 1 or above: an ordered sequence of constituents, its ID the hash of theirs, its coordinate their exact average | [Compositions](../Storage/Compositions.md) |
| consensus, standing | a claim's Glicko-2 rating, deviation, volatility, and match count, updated in place | [Consensus](../Semantics/Consensus.md) |
| constituent, child | an entity a composition is made of, a vertex of its path | [Compositions](../Storage/Compositions.md) |
| container, parent | a composition whose path holds an entity | [Query](../Query.md) |
| coordinate, real | an entity's point in the 4-ball, fixed point `m / 2^53`, stored as POINT ZM | [Physicality](../Storage/Physicality.md) |
| DAG, Merkle | the graph of compositions over their constituents, acyclic by tier, each node named by the hash of its children | [Storage](../Storage/README.md) |
| deduplication, trunk to leaf | the O(tier) check that a trunk found recorded has its whole subtree recorded | [Ingestion](../Storage/Ingestion.md) |
| entity | anything with an ID: an atom, a composition, a claim, a record, a file, a witness | [Physicality](../Storage/Physicality.md) |
| fan | how many claims that hold an entity a hop reads | [Personality firmware](../Semantics/Firmware.md) |
| fingerprint | the BLAKE3-256 of a tier-0 table; two installs with one fingerprint give the same content the same coordinates | [Atoms](../Storage/Atoms.md) |
| firmware | one human being's decisions for a pull, a file never a record | [Personality firmware](../Semantics/Firmware.md) |
| flags | the 256 bits per codepoint holding the Unicode Standard's properties | [Atoms](../Storage/Atoms.md) |
| games | how many times a witness has attested a strand; a claim is a game series, games plus a score | [Attestations](../Semantics/Attestations.md#strands) |
| Hilbert value | the 4D Hilbert curve position of a coordinate on a 16-bit grid, for locality and ordering | [Physicality](../Storage/Physicality.md) |
| hop | following a claim from an entity to the entity at its other end | [Pull](../Semantics/Pull.md) |
| ID | BLAKE3-128 of pure content | [Identity](../Storage/Identity.md) |
| lineage | the witness a witness derives from; copies of one lineage play one matchup | [Attestations](../Semantics/Attestations.md) |
| matchup | one Glicko-2 update of a standing by one attestation, the witness playing at the deviation its trust gives | [Consensus](../Semantics/Consensus.md) |
| metadata | of a file: what is said of it that is not its content, beginning with its name | [Compositions](../Storage/Compositions.md) |
| node table | the engine's in-memory table of every composition of a run, sharded by ID | [Ingest](Ingest.md) |
| observation | what a trajectory gives without anyone attesting: precedes, contains, co-occurrence | [Attestations](../Semantics/Attestations.md) |
| path, trajectory, physicality | the geometry that records an entity's constituents in order, one vertex per run, the ID packed in X, Y, Z and the run and kind in M | [Physicality](../Storage/Physicality.md) |
| perf-cache | a memory-mapped, fingerprinted, rebuildable file of deterministic records; tier 0 is the anchor | [Atoms](../Storage/Atoms.md) |
| pull | a read of the web under a firmware; the forward pass | [Pull](../Semantics/Pull.md) |
| recipe | how a kind of file decomposes and what it attests | [Ingestion](../Storage/Ingestion.md) |
| record | a set of claims witnessed together, a sentence with what is said of it, one attestation | [Recipes](Recipes.md) |
| run | a vertex's repeat count, the low 30 bits of M | [Physicality](../Storage/Physicality.md) |
| said | what a vertex is within its path: claim, record, tuple, metadata; the high bits of M | [Formats](Formats.md) |
| segment | a UAX #29 word segment, tier 2; also a contiguous run of one trajectory | [Compositions](../Storage/Compositions.md) |
| source | a body of content with one identity, however many files it comes in; the witness when it attests | [Recipes](Recipes.md) |
| strand | a claim: a composition of the entities it connects, its path any geometry ZM | [Attestations](../Semantics/Attestations.md#strands) |
| tier | an entity's level of composition: atoms 0, and a composition one above its highest constituent; never part of an ID | [Compositions](../Storage/Compositions.md) |
| tier 0 | the perf-cache of every codepoint's ID, coordinate, Hilbert value, and rank | [Atoms](../Storage/Atoms.md) |
| trunk | the top of a file's DAG, `[metadata, content]`; also the composition of a prompt | [Compositions](../Storage/Compositions.md) |
| trust | how far a witness is believed, −1 to 1, played as the opponent's deviation | [Consensus](../Semantics/Consensus.md) |
| tuple | a path of things that together name one thing; not text, not a claim | [Claims](../Semantics/Claims.md) |
| wall | the surface of the 4-ball, `Σ m² = 2^106`, which no coordinate crosses | [Space](../Storage/Space.md) |
| witness | whoever testifies: a source trunk, `[source record, its files' trunks]`, its name content inside its source record, its lineage and trust keyed by the trunk; as built a row of `witness` | [Attestations](../Semantics/Attestations.md) |
