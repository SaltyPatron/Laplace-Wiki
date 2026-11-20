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

Laplace does not speak English; it speaks Unicode and renders language. `NOUN` is English. `noun` is still an entity, probably a word that gets ingested, and `is a` is a sentence, not a hard-coded enum name. Attestations are links and relations between the IDs of entities, and only of entities: a physicality has no identity of its own, being the entity's row keyed by the entity's ID, so nothing attests a physicality. Pregenerated relations, types, and kinds that act like a perf-cache or flagged enums may be generated ahead; nothing else is hard-coded.

A claim's relation, like every other part of it, is what the source means, never the name of the field, column, attribute, or layer the source's markup happens to use. FrameNet's BNC layer tags `dog` `NN1`: `BNC` is a layer name, and `NN1` is a value of the BNC's CLAWS C5 tagset meaning a singular common noun, which reaches `NOUN` through an attested equivalence; `[dog, BNC, NN1]` records the markup, not the meaning. A per-span label belongs in its sentence's annotation layer, and a pointer's attribute name, such as `feID`, is in no claim.

## IDs

Deterministic content determines a claim's ID. A claim is an n-ary composition of entity IDs (`lp_id_compose`), computed from the ordered 16-byte BLAKE3 IDs along its `physicality.path` (`POINT ZM` or `LINESTRING ZM`) identically to any other composition.

There is **one** `blake3` claim composition ID shared across all four canonical tables — `entity.id`, `physicality.entity`, `attestation.claim`, and `consensus.claim` — never separate hashes for witnessing and consensus. Two witnesses asserting the exact same proposition collide on that single `claim` ID in `consensus`, while per-witness specifics (`witness`, `lineage`, `games`, `tokens`, `score`, `position`, `trust`) live as columns on `attestation` (keyed by `(claim, witness, lineage)`) and as `M` / spare-bit metadata on the asserting record's `physicality.path` vertex.

## Masks

Both `entity.mask` and `physicality.mask` carry a single fixed `bit(64)` (`uint64_t`) bitmask defined by `Laplace-Native/manifest/banks.tsv` and indexed by GIN (`laplace_mask_ops`): `kind` (`8`-bit row-role flags at bit `0`: `CLAIM`, `RECORD`, `TUPLE`, `FILE`), `upos` (`5` bits at offset `8`), `lexfile` (`6` bits at offset `13`), `deprel` (`6` bits at offset `19`), `vnrole` (`6` bits at offset `25`), and `wnframe` (`6` bits at offset `31`), where enum banks store `slot + 1` (`0` = absent). (By contrast, the 256-bit Unicode Character Database property bitmap per codepoint lives in the separate `tier0.flags` ROM perf-cache, never as 256-bit SQL columns.)

Masks are made for enums, and the enums are flagged too, enumerated as completely as possible at once. Identifiers are not masked: an ILI is an identifier, and there is no mask for 116,000 ILI concepts. The question a mask answers is asked across all of the sources: does this source say this is a noun? Does it say it is this? Is it that?

Relation types are attestation types, a different semantic group from part of speech, sense, and dependency relation.

## The Linguistic Super Highway

The mappings between curated resources, such as SemLink, PredicateMatrix, MapNet, WordFrameNet, and CILI, which link PropBank, VerbNet, FrameNet, WordNet, and ILIs to one another, are part of the Linguistic Super Highway. The highway is part of the foundation behind the part-of-speech, sense, and dependency-relation masks. See [Research: Semantics Experiments](../Research/Semantics-Experiments.md#the-identifier-highway).
