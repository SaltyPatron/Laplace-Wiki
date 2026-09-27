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

The tier of a composition is always at least one more than the tier of its highest constituent.

A node can fill a higher tier, but never a lower one. `[H,e,l,l,o]` is always a tier 2 word. Because the same content has the same hash, "Hello" on its own is never really a separate tier 3 sentence: the word fills that tier. "Hello!" is a tier 3 sentence. A tier 2 node can be a tier 3; a tier 3 node cannot be a tier 2.

## Segmentation

UAX #29 breaks text down, language-agnostically, from its meaningful codepoints. Laplace applies the same kind of breakdown to every modality. For an image:

```text
codepoint → digit → number → intensity → channel → pixel → patch → region → image
```

All digital content boils down to Unicode codepoints and is broken down into its smallest constituent components. Numbers are compositions of codepoints:

```text
[c,a,t]
[3,.,1,4,1,5,...]
[2,5,5]
```
