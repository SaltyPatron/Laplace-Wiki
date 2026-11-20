# Ingestion

Ingestion computes content's IDs on the client and deduplicates it trunk to leaf against what is already recorded.

## Client-side

The client breaks content down and computes its IDs and coordinates itself, using the memory-mapped [tier 0](Atoms.md#generation) (`tier0.bin`) and linguistic super highway (`highway.bin`) perf-caches.

Creation proceeds **bottom-up (leaf to trunk)** through canonical domain tier boundaries (such as UAX #29 for text: codepoint $\rightarrow$ grapheme $\rightarrow$ word $\rightarrow$ phrase/sentence; or grammar AST rules for structured records and files):

- **Bit-perfect coordinates** come from the compiler flags (`-fp-model=precise`, `-ffp-contract=off`), CORE-MATH (`cr_sin`/`cr_cos`), and exact signed `int64` fixed-point coordinates ($m / 2^{53}$) on $S^3$ with `__int128` centroid accumulation.
- **Universal content determinism** comes from the perf-caches (`tier0.bin`, `tier0.flags`, `highway.bin`, `chess.bin`): the same content produces the exact same 16-byte `blake3` ID everywhere, regardless of OS or x86-64 ISA level.
- **Canonical in-RAM deduplication**: Because composition respects canonical tier boundaries rather than arbitrary BPE/SentencePiece subword splits, every repeated character, word, phrase, or shared highway identifier (`i46360`, `abandon.01`, `Q937`, `va:0001f`, `give-13.1`, `NOUN`) collapses in $O(1)$ into the client's lock-free in-RAM node table (`src/table.c`) before any database round-trip occurs, while release-local internal pointers (`sent_id`, byte offsets, or `geonameid`) resolve via `key`/`refer` and are recorded nowhere.

## Recipes

Literally any standardized or fixed-format file is a modality to Laplace, and Laplace treats them all exactly the same: a generic decomposer uses a recipe to tell it how to extract the content.

Encrypted content has no value to Laplace: it is random binary blob storage. The database itself can be encrypted.

The decomposer and the ingestion pipeline are optimized to the limit and powered by recipes that denote how to decompose content into Laplace records: how content is recorded, what content is recorded, what gets reproducibility, and what does not matter.

## Deduplication

Deduplication against PostgreSQL is an O(tier) check from **trunk to leaf** (the opposite direction of client-side creation). Everything it finds already recorded is eliminated along with its entire descendant subtree, so the check reduces its own total count as it goes.

The client has decomposed the content leaf-to-trunk and holds a deterministic trunk ID for every tier, with the records, their coordinates, and their physicality trajectories already made and deduplicated in RAM on the client. The check is the client saying "I have these IDs: which do you already have?" and omitting those—and everything below them—from what it writes. It goes by the logical domain trunks: the file trunk, the trunks of the file's metadata and of its content tree, then their logical children (records, sentences, words), skipping synthetic binary-tree (`blocks_of`) spine nodes. It never searches the tiers.

Asking first is what removes conflict handling and reduces the WAL: only new records are written. The check should take next to nothing, even for gigabytes.

## Assembly-Line Record Streaming & Pipelined Staging (`stage.*`)

Ingestion is a continuous, non-blocking **assembly line** driven by record framing from the outer packaging grammar—never a row-by-row chumper and never a lagged end-of-source "consensus fold":

1. **Single-Pass Grammar-Bounded Record Streaming**: Stream files in a single pass, slicing strictly on outer grammar record boundaries (XML `<LexicalEntry>` / `<Synset>`, Turtle statement block, JSONL line, CoNLL-U sentence block, PGN game, CSV/TSV row)—never splitting at arbitrary byte offsets and never reading or decomposing a file twice.
2. **Parallel Arena-Allocated Record Workers**: Worker threads pull record slices from the ring buffer, parse each record via reusable thread-local `TSParser` + chained sub-grammars (`ts_parser_set_included_ranges`) + compiled integer `TSSymbol`/`TSFieldId` jump tables, compose bottom-up into the lock-free `NODE[]`/`VTX[]` table, and accumulate per-witness `(claim, games, score)` series directly in-stream using thread-local arenas reset per record (`0` `malloc`/`free` calls per record). Cross-record internal pointers (`key` / `refer`) resolve against a lock-free concurrent `key_hash -> EntityID` table—never by holding a whole-file `STree`/`SNode` DOM in RAM.
3. **Continuous Pipelined `stage.lp_*` COPY & In-DB Series Updates**: `laplace_ensure_stage()` prepares three `UNLOGGED` column templates (`stage.entity`, `stage.physicality`, `stage.attestation`), from which each ingest run creates `UNLOGGED` `stage.lp_*` working tables (`stage.lp_entity_*`, `stage.lp_path_*`, `stage.lp_delta_*`, `stage.lp_pending_*`, `stage.lp_witness_*`, `stage.lp_affected_*`). As each window fills, top-down `Trunk -> Leaf` deduplication (`laplace_present_ids`) prunes known subtrees, and novel rows plus accumulated claim series stream via binary `COPY` into `stage.lp_*` using bounded connection concurrency without Two-Phase Commit (`PREPARE TRANSACTION`). Inside PostgreSQL, `laplace_merge_stage` merges Hilbert-ordered content into the partitioned `entity` and `physicality` tables, `laplace_clean_stage` drains GIN pending lists, and set-based `laplace_attest_series` publishes witness series into `attestation` (recording the source trunk ID directly in `attestation.witness`, with no separate `witness` table) and updates rooted Glicko-2 standings in `consensus` (`consensus_0`..`consensus_f`).

The checks are set-based operations, not per-row conflict handling such as `ON CONFLICT`. See [Research: Engine Measurements](../Research/Engine.md#ingestion).

Same content means the same hash. If a trunk node matches, its children match as well; if they do not, the ingestion was done wrong. See [Research: Hashing](../Research/Hashing.md) and [Research: Prototype](../Research/Prototype.md#verification).
