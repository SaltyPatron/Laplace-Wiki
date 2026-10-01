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

Codepoints are tier 0. Graphemes are tier 1, words tier 2, and so on. Tiers are dynamic across modalities.

A tier is a floor. Only codepoints go in tier 0. Everything else sits at tier 1 or above, because it is an n-ary composition, and which tier it is recorded at does not matter as long as it is recorded properly.

Every recipe has its own tiers: UAX #29 has its own, a wordnet file has its own, images have their own, chess games have their own, and PGN has its own.

The tier of a composition is always at least one more than the tier of its highest constituent.

A word can go straight from tier 0 constituents to tier 2.

For text content, the basic structure is codepoint ↔ grapheme ↔ word ↔ sentence ↔ document ↔ file. There is more besides: paragraphs, titles, and the various separators, including dedicated separator codepoints, some of them language-specific. Laplace speaks Unicode and renders language.

A node can fill a higher tier, but never a lower one. `[H,e,l,l,o]` is always a tier 2 word. Because the same content has the same hash, "Hello" on its own is never really a separate tier 3 sentence: the word fills that tier. "Hello!" is a tier 3 sentence. A tier 2 node can be a tier 3; a tier 3 node cannot be a tier 2.

## Types

Roles are agnostic across modalities. `[2,5,5]` can be a pixel channel intensity, a raw byte value, an IP segment, and more. It only gets a type when it is put into a Merkle DAG composition.

## Files

A file has a trunk, with children for the file's metadata and for the file's content: EXIF data, headers, and so on. Every standardized file, such as `something.txt`, `audio.mp3`, or `image.bmp`, branches into its own trees.

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
