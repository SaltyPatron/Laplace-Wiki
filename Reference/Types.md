# Types, masks and the highway

What a curated resource writes in its enumerations is content like everything else, and a type besides: a value from a fixed list, held by its content's ID in a perf-cache and as a flag in a mask.

This page sets out, against the specification, how types are held — in perf-caches, in vertices, in masks — and what that removes from the DAG. Each point names the page it follows.

## Content and plumbing

[Identity](../Storage/Identity.md) says the hash is purely content and that a hash is never faked from a made-up string. [Claims](../Semantics/Claims.md) says relations are tied together by types, that an ILI synset is a type like an IP segment is, and that parts of speech, senses, dependency relations "and so on" are enums: fixed in scope, perf-cachable, held in mask columns. [Claims: Tuples](../Semantics/Claims.md#tuples) says Laplace speaks Unicode and renders language: `NOUN` is English, `noun` is still an entity, `is a` is a sentence and not an enum name, and only pregenerated relations, types, and kinds that act like a perf-cache or flagged enums are generated ahead. So what a seeded corpus writes falls into two kinds:

- **keys** the file uses to point at its own things — a synset id, a sense key, a sentence's id, `sent_id`, a token's `id` — resolved inside the reader and written nowhere;
- **values of a fixed list** — `NOUN`, `nsubj`, a lexicographer file — which are content: the entity of the text as the source writes it, a part of a claim like any other entity, and also a slot in a perf-cache and a flag in its mask, so that a filter needs no read.

Identifiers are not masked ([Claims: Masks](../Semantics/Claims.md#masks)): an ILI, a VerbNet class, a FrameNet frame, a PropBank roleset each have a slot in the highway's perf-cache, and none has a mask bit.

What is content: words, phrases, sentences, texts; definitions, glosses, examples; the set of members a synset lists; a frame's name as the resource titles it. A thing's identity is its content: a synset is the composition of its members in the order listed (so every wordnet listing the same members lands on one entity, and their attestations meet there); a sense is `[written form, synset]`; a lexical entry is its written form; a sentence is its tokens. `key TIER NAME` in a recipe means the part is the key, not that the thing is the string, and `thing TIER NAME...` says what the thing is; things whose members arrive later in a file are composed when the file has been read through.

## Perf-caches

[Atoms](../Storage/Atoms.md) defines the form: generated native C, marshalled into PostgreSQL, memory-mapped so a lookup is O(1) in microseconds and never a database call, modular, with a fingerprint every install agrees on. Tier 0 (`tier0.bin`) is one; the flags that go with it (`tier0.flags`, one 256-bit record per codepoint, its layout written beside it from the standard's own property and value lists) is another, already built the same way.

The **highway** is the third: `highway.bin`, with its layout beside it. One record per type value, in the form of a tier-0 record — the ID of the value's *content* (the text `NOUN` as UD writes it; an ILI's English definition as CILI gives it; a frame's name), its real coordinate, and its slot. The lists are the resources' own, each type's slot frozen when it is first listed (Laplace-Native's `manifest/slots`) and new types appended after, so a slot never moves: UD-Tools' `upos.json`, `deprels.json`, `feats.json`; WordNet's sense numbering (sense *k* of a lemma); CILI's `ili.ttl`; VerbNet's classes; FrameNet's frames, lexical units and frame elements; PropBank's rolesets and arguments; MCR's domains and SUMO. The mappings between them — the rows of PredicateMatrix, SemLink, MapNet, WordFrameNet, CILI's maps — are the highway's edges, held in the same file: a slot in one list to slots in the others. `laplace highway` generates it from those sources the way `laplace tier0` and `laplace flags` generate theirs; the database setting `laplace.highway` names it, and the extension maps it in each backend as it maps tier 0.

## Values in vertices

[Identity](../Storage/Identity.md) leaves 28 spare mantissa bits in a packed vertex, dynamic, "holding values from known lists; a small tag says which layout they are in", and [Research: Recipes](../Research/Recipes.md) measured the effect: storing perf-cache values in place of their 128-bit references, eight to a vertex, cut image storage 8.8 times. A vertex therefore has layouts: tag 0, a full ID; other tags, one or several slots of a named list. The ID of the composition is unchanged in form — BLAKE3 over its constituents' IDs — where a slot's constituent ID is the ID recorded for it in the perf-cache. The path stores the slot, not the 128-bit reference. As built, Laplace-Native writes and reads the spare bits (`lp_ewkb_runs_spare`, `lp_xyz_spare`) and its scans match through the ID's bits only, but neither the Engine nor the extension writes a value into them yet.

## Masks

[Claims](../Semantics/Claims.md): separate columns hold bitmasks that denote which part of speech, sense, dependency relation, and so on apply. On an entity's row: its part-of-speech mask (UD's 17), its sense mask (sense 1 to 256 of that lemma, per the sense numbering), and the like — set as the layers that attest them are recorded, in the same set-based statement as the load. On a claim's row (the consensus), the masks of the types it holds, and whether it is a claim at all, which is what tells it from a sentence.

The container index carries them: its keys are the packed IDs a path holds *and* the mask bits of the row, so "the claims that hold `dog` and say NOUN" is one intersection of posting lists — no scan of the sentences that hold `dog`, which is what made a hub cost seconds ([Physicality](../Storage/Physicality.md#indexes) defines the index over constituents; the mask bits are the further keys).

As built, each semantic group is a bank of its own, declared in Laplace-Native's [`manifest/banks.tsv`](https://github.com/SaltyPatron/Laplace-Native/blob/main/manifest/banks.tsv): the bank, the list it flags, its group (lexical: what a word is; structural: a role inside a structure; kind: what a row is), its carrier (the entity's row, an occurrence inside a layer, or the physicality row), and the width it keeps for values still to come. A value's bit is its frozen slot in `manifest/slots/LIST.tsv`: slots are appended and retired, never moved or reused, so a bit means the same thing in every build. Today's banks are `kind` (8), `upos` (32), `lexfile` (64), `deprel` (64) and `vnrole` (64). Only the `kind` bank is written so far, on `physicality.mask`; the entity and occurrence carriers are not built, so a read that filters on a lexical or structural bank finds nothing yet.

## Layers

[Research: Semantics Experiments](../Research/Semantics-Experiments.md#annotation-layers-as-content) measured what a treebank is as content: one record per token per layer would be 75.8 million records for two layers over UD; one claim per sentence per layer is 4.6 million, with per-token detail held as vertices, and composed hierarchically the layers share their small sub-structures almost entirely. So a CoNLL-U sentence is recorded as: the sentence (its tokens); a UPOS layer, one claim `[sentence, UPOS, layer]` whose layer is a path of slots aligned to the tokens; a dependency layer, whose vertices hold the relation's slot and the head's offset, its subtrees composed as paths so that a phrase analysed the same way is one node wherever it occurs; feature layers likewise. What a treebank says of a word by itself — that `dog` is NOUN, that its lemma is `dog` — is the standing of `[dog, NOUN]` with NOUN a slot, one claim per pair, and the bits on `dog`'s row. `id`, `sent_id`, `SpaceAfter` are not claims: the first two are keys, the third is the trajectory.

## Segmentation

[Compositions](../Storage/Compositions.md) says punctuation is a constituent like everything else and that UAX #29 is tailored. At the word tier a separator separates: the rules that keep a MidLetter, MidNum or ExtendNumLet inside a segment (WB6, WB7, WB11, WB12, WB13a, WB13b) are not applied, so `microsoft.com` is `[microsoft] [.] [com]`, `3.14` is `[3] [.] [14]`, `word_1` is `[word] [_] [1]`. The codepoint `.` is one entity; whether it ends a sentence is the sentence tier's reading of the path, as it is now. The sentence and grapheme rules stand.

## Repeats

[Compositions](../Storage/Compositions.md#repeats): repeats are not recorded one by one. A run is a constituent repeated adjacently, at every tier (`aaa`, `no no no`). A repeated *block* is factored from the content alone, by one rule — leftmost, the shortest period, recursive — so `banana` is `b [an]×2 a` and `mississippi` is `m [i [s×2]]×2 i [p×2] i`, and the block is an entity every other composition that holds it shares. Never against what was recorded before: the ID stays a function of content.

## The extension owns the schema

The five tables, their partitions, their indexes, the lookups, the web's functions and the views over it are what `CREATE EXTENSION laplace` makes, as PostGIS makes `spatial_ref_sys`: the tables are the extension's configuration tables, so `pg_dump` carries their data. `laplace deploy` becomes the database, its extensions and its settings; the engine, and any interface after it, are clients of that.

## What this changes

Every ID above tier 0 (segmentation, repeats), the readers (identity as key, layers, masks), the schema (masks, index keys, the extension owning it), and a fourth perf-cache. The order of work: Laplace-Native (segmentation, repeats, the highway map and its API), Laplace-postgres (schema in the extension, mask columns and keys, `laplace.highway`), Laplace-Engine (`laplace highway`, the readers, masks at load), Laplace-Operations (`highway` as a deploy step beside `tier0` and `flags`), then the database rebuilt from the sources.
