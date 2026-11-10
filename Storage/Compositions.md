# Compositions

A composition is an n-ary, recursive sequence of constituents, each of which is a codepoint or another composition.

## Constituents

A composition can reference any tier. Its constituents can be [atoms](Atoms.md), other compositions, or both. Nothing is dropped: whitespace and punctuation are constituents like everything else.

"The cat sat on the mat" is a sentence composed of words and codepoints:

```text
[The, ' ', cat, ' ', sat, ' ', on, ' ', the, ' ', mat]
```

"Sherlock Holmes" decomposes into two words and a codepoint:

```text
[[S,h,e,r,l,o,c,k], ' ', [H,o,l,m,e,s]]
```

## Tiers

Codepoints are tier 0. Every composition of two or more children has tier `1 + max(child.tier)`, and a one-child composition collapses to its single child (`n == 1` returns `ch[0]` unchanged, with no wrapper entity and no tier inflation). Tiers are intrinsic Merkle DAG heights across all modalities.

Only codepoints sit at tier 0. Everything else sits at tier 1 or above, determined strictly by its constituent height (`1 + max(child.tier)`).

Every modality and grammar decomposes into the same Merkle DAG: UAX #29 text, XML/JSON/Turtle/CSV records, ASTs, images, audio, and chess games.

A single-codepoint grapheme or one-character word `"a"` is tier 0. A word composed of single-codepoint graphemes (`[H,e,l,l,o]`, `[k,i,n,g]`) has tier 1; a word containing a multi-codepoint grapheme cluster (`e + \u0301`) has tier 2.

For text content, the UAX #29 segmentation hierarchy is codepoint ↔ grapheme ↔ word ↔ sentence ↔ paragraph ↔ document ↔ file, where each level with two or more parts advances `tier = 1 + max(child.tier)` and any single-child level collapses to that child.

Because the same content always has the same hash and tier (`1 + max(child.tier)`), `"Hello"` (`[H,e,l,l,o]`) is always tier 1, and a one-word sentence `"Hello"` is that tier 1 word itself, never a separate sentence wrapper entity. `"Hello!"` (`[[H,e,l,l,o], !]`) is tier 2 (`1 + max(1, 0)`).

## Types

Roles are agnostic across modalities. `[2,5,5]` can be a pixel channel intensity, a raw byte value, an IP segment, and more. It only gets a type when it is put into a Merkle DAG composition.

## Files

A file has a trunk, with children for the file's metadata and for the file's content: EXIF data, headers, and so on. Every standardized file, such as `something.txt`, `audio.mp3`, or `image.bmp`, branches into its own trees.

Every domain has its own natural tier ladder, and those tier ladders **nest recursively inside one another**:

1. **Text ladder (UAX #29):** `codepoint` → `grapheme` → `word` → `phrase / clause / sentence`, each a Merkle height (`1 + max(child.tier)`), not a fixed number: `[H,e,l,l,o]` is tier 1, a sentence of such words tier 2.
2. **Document / Literary ladder:** sentences compose into `paragraphs` → `sections / scenes` → `chapters / articles` → `book / body`.
3. **File / Container ladder:** the document body sits alongside format-specific `headers`, `metadata`, `tags`, or `records` (XML elements, JSON objects, TSV rows, CoNLL-U blocks, PGN games, ELF/PE sections) under a `File Trunk`, which itself sits under a `Directory / Repository / Corpus Trunk`.

Because `entity.tier = max(child.tier) + 1`, tier is **structural altitude in the Merkle DAG**, not a fixed semantic label. When a sequence of >64 children is chunked into 64-child binary-tree spine nodes (`blocks_of`), those intermediate spine nodes are structural balance helpers; top-down (`Trunk → Leaf`) database deduplication skips synthetic `blocks_of` spine nodes and probes logical domain children directly so shared subtrees are amputated immediately.

## Repeats

Repeats are not recorded one by one. An all-white image does not record a billion white pixels: the white pixel is one entity, and repeats are run-length encoded. Pixels, patches, and regions are finite in space, while large, and deduplicate heavily.

## Segmentation

UAX #29 breaks text down from its meaningful codepoints, using Unicode's character properties rather than any one language's rules; scripts written without spaces between words, such as Thai or Chinese, need tailoring. See [Research: Unicode](../Research/Unicode.md). Laplace applies the same kind of breakdown to every modality. For an image:

```text
codepoint → digit → number → intensity → channel → pixel → patch → region → image
```

All digital content boils down to Unicode codepoints and is broken down into its smallest constituent components. Numbers are compositions of codepoints:

```text
[c,a,t]
[3,.,1,4,1,5,...]
[2,5,5]
```
