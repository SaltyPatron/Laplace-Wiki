# Hashing

Research on how BLAKE3, Merkle trees and DAGs, hash-consing, and IEEE-754 bit packing behave under the Laplace identity scheme.

> [!NOTE]
> Numbers marked **measured** were produced by the local research script `pack_verify.py`. Every other number comes from the cited sources or follows from the stated formula.

The scheme under study is the one in [Identity](../Storage/Identity.md): a node's ID is the BLAKE3 hash of its pure content, truncated to 128 bits and bit-packed into the X, Y, and Z mantissas of a point ZM.

## BLAKE3

BLAKE3 targets 128-bit security for all of its goals: preimage, second preimage, collision, and differentiability. Its default output is 256 bits.

BLAKE3 is an extendable-output function (XOF). Output of any length comes from repeating the root compression with an incrementing counter, and the specification states that outputs of different lengths are not domain separated: "Shorter outputs are prefixes of longer ones." A 128-bit ID is therefore exactly the first 16 bytes of the standard 256-bit hash. **Measured:** `digest(16) == digest(32)[:16]`.

BLAKE3 has three modes, selected by flags in the compression function:

| Mode | Input | Flags |
| --- | --- | --- |
| `hash` | message | none beyond the tree flags |
| `keyed_hash` | 256-bit key, message | `KEYED_HASH` (2⁴) |
| `derive_key` | context string, key material | `DERIVE_KEY_CONTEXT` (2⁵), `DERIVE_KEY_MATERIAL` (2⁶) |

The tree flags are `CHUNK_START` (2⁰), `CHUNK_END` (2¹), `PARENT` (2²), and `ROOT` (2³).

BLAKE3's own internal chunk tree is sound by the Daemen et al. conditions: subtree-freeness (the `ROOT` flag), radical-decodability (no ambiguity of tree shape), and message-completeness. Those guarantees cover the chunk tree of one input. A Merkle DAG built over BLAKE3 gets the equivalent properties from how it forms each node's input, below.

## Truncation to 128 bits

For an n-bit output the generic bounds are:

| Attack | Work |
| --- | --- |
| Collision | about 2^(n/2) = 2⁶⁴ at 128 bits |
| Preimage, second preimage | about 2ⁿ = 2¹²⁸ |
| Multi-target second preimage against N stored IDs | about 2¹²⁸ / N; about 2⁷⁸ at N = 10¹⁵ |

The probability of any accidental collision among n nodes is 1 − exp(−n(n−1) / 2¹²⁹):

| Nodes n | log₂ n | P(any collision), 128 bits |
| --- | --- | --- |
| 10⁹ | 29.9 | 1.47 × 10⁻²¹ |
| 10¹² | 39.9 | 1.47 × 10⁻¹⁵ |
| 10¹⁵ | 49.8 | 1.47 × 10⁻⁹ |
| 10¹⁸ | 59.8 | 1.47 × 10⁻³ |
| 2⁶⁴ ≈ 1.8 × 10¹⁹ | 64 | 0.39 |

At 128 bits the probability reaches 10⁻¹² at 2.6 × 10¹³ nodes, 10⁻⁶ at 2.6 × 10¹⁶, and 0.5 at 2.2 × 10¹⁹. For comparison, at n = 10¹² a 64-bit ID gives a probability of about 1, a 96-bit ID 6.3 × 10⁻⁶, and a 256-bit ID 4.3 × 10⁻⁵⁴.

The rule in [Ingestion](../Storage/Ingestion.md#deduplication), that matching trunks have matching children, holds up to these probabilities. The cost of a deliberate collision at 128 bits and at wider truncations is in [Numerics](Numerics.md#collision-economics).

## Hash input

Laplace hashes pure content only:

- a codepoint, for a leaf;
- the ordered child IDs, for a composition.

Type, tier, source, and position are observations about a node, not content, and are not part of the hash input.

Every child ID has the same fixed width, so a composition's input is a concatenation of fixed-width fields. That concatenation parses in exactly one way, and the byte length fixes the child count: `[a,a]` is twice as long as `[a]`. A composition with one child collapses to that child, so no composition input consists of a single child ID. Together, fixed-width child IDs and one-child collapse keep leaf inputs and composition inputs apart: a leaf's input is the 1 to 4 bytes of one codepoint's UTF-8 and a composition's is at least 32 bytes, so no domain byte is prepended, unlike RFC 6962 below.

The classic ambiguity of hashing concatenated variable-length content, `"ab" + "c" == "a" + "bc"`, cannot arise: the input holds child IDs, not child content.

### Structure and spelling

The hash covers structure. `[ab,c]` and `[a,bc]` both spell "abc" and have different IDs. Equal text deduplicates across documents when it is segmented into the same tree wherever it occurs, so segmentation must be a deterministic function of local content. Laplace segments with UAX #29 and its analogues for other modalities; see [Compositions](../Storage/Compositions.md#segmentation).

### How other systems form hash input

Other content-addressed systems put more than content into the hash input. They are listed here for comparison.

| System | Hash input |
| --- | --- |
| Git | `"<type> <size>\0"` followed by the object content; trees are sorted lists of (mode, name, ID) |
| RFC 6962 (Certificate Transparency) | `0x00 ‖ leaf` for leaves, `0x01 ‖ left ‖ right` for interior nodes; the split point is the largest power of two below n |
| IPFS CID | `<multibase><version><multicodec><multihash>`; the multihash is `<hash code><digest length><digest>`, and BLAKE3 has multicodec `0x1e` |

## Merkle trees and DAGs

Merkle's 1987 paper introduced the hash tree to authenticate many one-time-signature public keys with a logarithmic-size path.

Git stores blobs, trees, commits, and tags as a Merkle DAG in which equal subtrees are shared. SHA-1 collisions (SHAttered, 2017) led Git to add SHA-256 repositories.

IPFS and IPLD form a content-addressed Merkle DAG. A dag-pb node is an ordered list of links (hash, name, size) plus data, and duplicate links are allowed, as repeated children are in Laplace.

## The CVE-2012-2459 lesson

Bitcoin's Merkle root duplicates the last hash when a level has an odd count, so `[1,2,3,4,5,6]` and `[1,2,3,4,5,6,5,6]` have the same root. The cause is implicit padding: the tree input stops being injective.

Laplace hashes the explicit ordered child list, with no padding, sorting, or removal of repeats before hashing. `[2,5,5]` and `[2,5]` are different inputs, and so are different IDs. Run-length encoding lives in M, as metadata of the [trajectory](../Storage/Physicality.md#trajectories), and is not part of the hash input.

## Hash-consing and chunking

Hash-consing is maximal sharing of structurally equal values through a global table keyed by constructor and children identities, so that equality becomes identity equality. Its origins go back to Ershov (1958) and Goto (1974); Filliâtre and Conchon give a type-safe OCaml library with weak tables, and Braibant, Jourdan, and Monniaux implement it in Coq.

Classic hash-consing uses a non-cryptographic hash and a full structural comparison on a bucket hit. Laplace's deduplication is hash-consing keyed by a cryptographic hash, with the ID itself as the identity.

Content-defined chunking takes the other route to deduplication. Rabin fingerprinting (1981) cuts a byte stream where a rolling hash satisfies `fp mod D == r`, so boundaries depend only on local content and survive insertions. FastCDC (USENIX ATC 2016) uses a Gear rolling hash, cut-point skipping, and normalized chunking, and is about 10× faster than Rabin-based chunking with a similar deduplication ratio.

Chunk boundaries are byte-statistical; Laplace's boundaries are semantic. Both rely on the same property: boundaries are a deterministic function of local content.

## Sync and deduplication

| System | What is compared | Round trips |
| --- | --- | --- |
| Git fetch | client sends `want`s, then `have` commit IDs in blocks of 32 in flight; the server acknowledges common ancestors and gives up after 256 unacknowledged haves | O(history depth / 32) for negotiation, then one packfile |
| IPFS Bitswap | wantlists of CIDs; v1.2 adds `want-have`, `want-block`, `Have`, `DontHave` | one per DAG level, because child CIDs are learned from the parent block |
| rsync | a weak rolling checksum and a strong hash per fixed block | one, flat |
| Merkle Search Trees | a Merkle tree over a key-ordered search tree, compared top down, recursing only on mismatches | O(log N); bandwidth proportional to differences × log N |
| Range-based set reconciliation | fingerprints of key ranges, split recursively on mismatch | O(log N) |

Git's negotiation relies on a closure invariant: having a commit implies having all its ancestors, trees, and blobs. Shallow and partial clones are the cases where Git relaxes it.

In Laplace the client already holds the whole tree, because it computed every ID itself ([Ingestion](../Storage/Ingestion.md#client-side)). Two query shapes follow:

- Tier by tier, trunk to leaf: one round trip per tier, sending only the IDs not yet pruned.
- Flat: one round trip sending every ID. At 16 bytes per ID, 10⁶ nodes is 16 MB.

Pruning on a trunk match is sound when the store holds the same closure invariant as Git: a node is recorded only when everything under it is recorded. Recording bottom up, leaves first, in one transaction maintains it.

## Packing into IEEE-754 doubles

### NaN boxing

JavaScript and Lua engines hide tags and pointers in NaN payloads. LuaJIT GC64 uses 47-bit pointers under 13 set high bits; SpiderMonkey PUNBOX64 uses 47-bit payloads and canonicalizes NaNs on store (`JS::CanonicalizeNaN`); JavaScriptCore instead offsets doubles by 2⁴⁹. NaN payloads are not preserved by arbitrary code: JS engines, WebAssembly, ARM default-NaN mode, and x87 quieting of signaling NaNs all change them. Data that must survive untouched stays in ordinary normal numbers.

### The safe region

With sign 0 and biased exponent fixed at `0x3FF`, a double lies in [1, 2) and all 2⁵² fraction patterns are normal, finite numbers. The region excludes:

- NaN and infinity (exponent `0x7FF`);
- subnormals (exponent 0), which flush-to-zero and denormals-are-zero modes turn into zero;
- ±0, which compare equal while differing bitwise;
- negative values.

x87 80-bit loads and stores of a normal double are exact, and FTZ/DAZ affect only subnormals, so values in this region survive being moved.

### Layout

```text
ID bits 127..85 (43) -> X fraction bits 51..9   (bits 8..0 spare)
ID bits  84..42 (43) -> Y fraction bits 51..9   (bits 8..0 spare)
ID bits  41..0  (42) -> Z fraction bits 51..10  (bits 9..0 spare)
each double: sign 0 | exponent 0x3FF | fraction   => X, Y, Z in [1, 2)
```

> [!NOTE]
> Laplace uses biased exponent `0x3FD` instead, so X, Y, and Z lie between 0.25 and 0.5, inside the 4-ball. That region is equally safe: every fraction pattern is a normal, finite, nonzero number. The prototype places the 43, 43, and 42 ID bits in the low fraction bits. See [Identity](../Storage/Identity.md#the-id-in-geometry).

The spare bits total 28, as in [Identity](../Storage/Identity.md#the-id-in-geometry). Unpacking can check the sign, the exponent, and the spare bits as a cheap corruption test.

**Measured:** 1,000,008 IDs (0, 2¹²⁸ − 1, `0x55…`, `0xAA…`, every single-bit ID, and 10⁶ random IDs) round-tripped exactly. Every value was finite and normal, in [1, 1.9999999999998863].

### Text round trips

**Measured** over 100,000 packed IDs:

| Text format | IDs corrupted |
| --- | --- |
| `%.15f` (15 decimal places) | 98,919 |
| `%.16f` (16 decimal places) | 0 |
| `%.17g` (17 significant digits) | 0 |
| shortest repr (PostgreSQL ≥ 12 `float8` output) | 0 |

PostGIS `ST_AsText` defaults to 15 decimal digits, and its documentation warns that WKT may not keep full floating-point precision. `ST_AsBinary` and binary COPY carry the doubles bit for bit. [Geometry](Geometry.md#text-output) has the PostGIS details.

Arithmetic destroys the payload: averaging, snapping, reprojection, simplification, and `ST_SnapToGrid` or `ST_Transform` all change the bits. [Numerics](Numerics.md#exponent-ranges-for-ids-in-geometry) measures how often.

## Sources

- [BLAKE3 specification](https://github.com/BLAKE3-team/BLAKE3-specs/blob/master/blake3.pdf), O'Connor, Aumasson, Neves, Wilcox-O'Hearn: security targets (§4.1), XOF (§2.6), modes and flags (§2.3, Table 3), tree soundness (§4.3), `derive_key` (§6.2).
- [BLAKE3 README](https://github.com/BLAKE3-team/BLAKE3/blob/master/README.md).
- [Merkle, "A Digital Signature Based on a Conventional Encryption Function", CRYPTO '87](https://link.springer.com/content/pdf/10.1007/3-540-48184-2_32.pdf).
- [RFC 6962, Certificate Transparency](https://www.rfc-editor.org/rfc/rfc6962.txt).
- [Bitcoin `consensus/merkle.cpp`](https://github.com/bitcoin/bitcoin/blob/master/src/consensus/merkle.cpp), header comment on CVE-2012-2459.
- [Git Internals: Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects).
- [Git pack protocol](https://github.com/git/git/blob/master/Documentation/gitprotocol-pack.adoc) and [Git protocol v2](https://github.com/git/git/blob/master/Documentation/gitprotocol-v2.adoc).
- [Benet, "IPFS: Content Addressed, Versioned, P2P File System", arXiv:1407.3561](https://arxiv.org/abs/1407.3561).
- [CID specification](https://github.com/multiformats/cid), [multihash specification](https://github.com/multiformats/multihash), and [dag-pb specification](https://github.com/ipld/specs/blob/master/block-layer/codecs/dag-pb.md).
- [Bitswap protocol](https://github.com/ipfs/specs/blob/main/src/bitswap-protocol.md).
- [Tridgell and Mackerras, "The rsync algorithm", TR-CS-96-05](https://www.andrew.cmu.edu/course/15-749/READINGS/required/cas/tridgell96.pdf).
- [Auvolat and Taïani, "Merkle Search Trees", SRDS 2019](https://hal.science/hal-02303490).
- [Meyer, "Range-Based Set Reconciliation", arXiv:2212.13567](https://arxiv.org/abs/2212.13567).
- [Filliâtre and Conchon, "Type-Safe Modular Hash-Consing", ML Workshop 2006](https://usr.lmf.cnrs.fr/~jcf/publis/hash-consing2.pdf).
- [Braibant, Jourdan, Monniaux, "Implementing hash-consed structures in Coq", arXiv:1304.6038](https://arxiv.org/abs/1304.6038).
- [Rabin, "Fingerprinting by Random Polynomials", Harvard TR-15-81](http://www.xmailserver.org/rabin.pdf).
- [Xia et al., "FastCDC", USENIX ATC 2016](https://www.usenix.org/system/files/conference/atc16/atc16-paper-xia.pdf).
- [LuaJIT `lj_obj.h`](https://github.com/LuaJIT/LuaJIT/blob/v2.1/src/lj_obj.h), [SpiderMonkey `Value.h`](https://github.com/mozilla-firefox/firefox/blob/main/js/public/Value.h), and [JavaScriptCore `JSCJSValue.h`](https://github.com/WebKit/WebKit/blob/main/Source/JavaScriptCore/runtime/JSCJSValue.h).
- [PostGIS `ST_AsText`](https://postgis.net/docs/ST_AsText.html) and [PostGIS `ST_AsBinary`](https://postgis.net/docs/ST_AsBinary.html).
