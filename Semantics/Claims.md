# Claims

A claim is a tuple of entities with referential integrity, and its ID is computed from its components the same way a composition's is.

## Tuples

Claims are tuples with referential integrity: every part of a claim is an entity. `noun` is `[n,o,u,n]`, the same entity as the word "noun" anywhere else. Any tier's entity can be a predicate.

The relations form a complex tree around each entity:

```text
dog  → noun
dog  → ILI i46360
dog  → eng
Hund → ILI i46360
Hund → deu
```

Relations are tied together by types and tiers. An ILI synset is a type, just like an IP segment is.

## IDs

Deterministic content determines a claim's ID. A claim is a limited path trajectory, so its hash is computed the same way as a composition's: from the IDs along its path.

Witnessing and consensus are two different beasts:

- For witnessing, the hash covers the claim's specifics.
- For consensus, the hash covers only the main components that make the claim unique.

## Masks

Separate columns hold bitmasks, such as 256-bit masks, that denote which part of speech, sense, dependency relation, and so on apply. These are enums: fixed in scope, and perf-cachable.

## The Linguistic Super Highway

The mappings between curated resources, such as SemLink, PredicateMatrix, MapNet, WordFrameNet, and CILI, which link PropBank, VerbNet, FrameNet, WordNet, and ILIs to one another, are part of the Linguistic Super Highway. The highway is part of the foundation behind the part-of-speech, sense, and dependency-relation masks. See [Research: Semantics Experiments](../Research/Semantics-Experiments.md#the-identifier-highway).
