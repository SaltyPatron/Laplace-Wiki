# Reads

The read commands compute the entity on the client, fetch one set from the database through the container index, and do everything else in the engine: `hop`, `translate`, `degrees`, `fills`, and `pull`.

`pull.c` holds the single-operation lookups (`hop`, `translate`, `degrees`), `forward.c` holds `pull`, and `program.c` executes the stateful eleven-stage forward program (`laplace turn`). Nothing in the read-only operations changes a standing.

## Naming an entity

`entity_named(ctx, text)`: `lp_text_parts` over the mapped tier 0, giving the text's trunk, its tier, coordinate, and its constituents in order, with no database call. `laplace text` prints exactly this.

## The claims that hold an entity

`claims_like(pg, part[3], have[3], fan, k)`: the given parts, at most three, as a `blake3[]` parameter, and one prepared statement, planned once per connection under `plan_cache_mode = force_generic_plan`:

```sql
SELECT entity, path, rating, deviation, volatility, matches
FROM laplace_claims($1::blake3[], $2::bigint, $3::smallint[], $4::blake3[])
```

with `$2 = fan + 1`, so `capped` says whether more exist than the fan reads; `$3` the claim's kind bit; `$4` the predicates the firmware refuses, taken out in the read itself, before the fan ([SQL: The web](SQL.md#the-web)). Each path is decoded in the engine to the claim's parts, up to 12; a claim is kept when the given parts stand in their places, the first given first, the last given last, the middle between; its confidence is `lp_confidence(standing, k)`. `claims_of` is the same with one part and no place. `refused()` also removes, in the engine, strands whose witness the firmware refuses. Then the sort: by confidence (`claim_by_conf`), or, under `order witness` on an open claim, by the position the witness gave (`positions_of` reads it from `attestation`, `claim_by_position`) before confidence.

## laplace hop

For a text: the entity named; its claims by `claims_of` under the firmware's `fan` and `k`, printed by confidence with rating, deviation, matches, and the witness's position; then what holds it, its containers by tier, from `laplace_containers($1, '{}') WHERE NOT (mask ? 0)`: what holds it, claims left out. For `SUBJECT PREDICATE OBJECT` with `?`: `claims_like` with the parts given. Text for every part comes through the `Reader`: paths fetched one level at a time for every entity at once, one round trip per level, expanded in the engine to tier 0, so a screen of claims costs a few round trips. Measured: `dog` in the engine database, 612 claims, 131 matched at least once and 481 untouched stock.

## laplace translate

Resolves the word's senses along the firmware's recipe-declared `lexicalization` (`[lemma, language, ILI]`, matching ISO 639 codes joined by `equivalent`), ordered by concordance `usages`, witness order, and standing, then resolves the target languages' lexicalizations of each concept and renders its `gloss` ([Firmware](Firmware.md)). Measured: `[dog, eng, ?]` 3.3 ms, `[?, language, i46360]` for eight languages 1.2 ms.

## laplace degrees

A best-first search from one entity toward another over `lp_frontier`: every claim that holds the current entity is a strand, its cost `lp_cost(standing, k, lambda)`, the entity at its other end reached at the accumulated cost, up to `hops` hops with at most `fan` strands read per entity, `--batch` entities expanded per round trip. With a target, the cheapest chain and its claims; without, what is nearest. In standalone `degrees`, `estimate` is `0` (Dijkstra).

A read is route planning, and the highway is its road network. The road classes are the identifier systems, the highway's type lists: words in each language, a wordnet's synsets, the ILI, the ISO 639 languages, FrameNet's frames, frame elements and lexical units, VerbNet's classes and roles, PropBank's rolesets, VerbAtlas's frames, the parts of speech, dependency relations and lexicographer files. The interchanges are the mapping strands where a route changes class: the lexicalizations, CILI's maps, SemLink, the Predicate Matrix, MapNet, VerbAtlas, WordFrameNet and FrameBase. A node that holds more claims than `fan`, such as `NOUN` or `eng`, is a fan-limited hub, reached and not crossed (bubbled past via two-key `up` relations in `program.c`). While standalone `degrees` runs Dijkstra over database claims alone, `program.c`'s `SCAN` stage maps `highway.bin` (`lp_highway_map`) and walks `lp_highway_edges` across non-bank highway lists alongside `holds_capped` database claims; `Batch 2` (`Laplace-Engine#31`) adds landmark Highway A* heuristics and N-ary (`np >= 4`) claim traversal.

## laplace fills

What follows a phrase, counted by occurrence across every source:

1. The phrase's constituents, computed on the client; the container tier is the tier above the phrase's highest part.
2. Containers: `SELECT entity, path, tier FROM laplace_containers($1::blake3[], '{}'::smallint[])`, the tier bound computed inside it, keyed by the phrase's compositions and never its lone separators, which are in nearly every path; each path scanned by `lp_follows` for the exact run, separators included, and the vertex after each run kept.
3. Leaf to trunk: the parents of those paths, then theirs, one fetch per level, each node once: `SELECT entity, id, times, tier FROM laplace_fills($1::blake3[])`, in chunks of 20,000.
4. Trunk to leaf: a node occurs as often as the sum over its parents of the parent's occurrences times the times the parent holds it, runs included, a trunk counting once; a sentence repeated in fifty books counts fifty times (`occ_of`).
5. Every continuation weighted by the occurrences of the path it came from.

Measured: `[Captain, ' ', ?]` in Moby Dick, Ahab 105, Peleg 52, Bildad 27, 9.2 ms; "the capital of ", the 456, a 82, an 15, his 12, 24.7 ms.

## laplace pull

The prompt through `text_ref` into the node table, its trunk and its constituents, runs written out; a word is one constituent of itself. First, every segment of the prompt at once, through `laplace_forward` (one set, one kept statement per segment): every run of at least two of its constituents that holds a word, in the order the pass walks them, `The dog`, `The dog barked`, and every other, each with how many observations hold it, how many as a run, and what follows the run in them, counted. That is precedes, contains and co-occurrence read off the trajectories ([Physicality](../Storage/Physicality.md#trajectories), [Pull](../Semantics/Pull.md#the-forward-pass)); a segment that is only tier-0 atoms, a space or a letter, says nothing of the prompt, is passed over, and is not printed. Then the fold: the observations that hold a run of two or more of the prompt's words, at most 128 containers a segment and 2,048 observations in all, are tugged at once, through one `laplace_claims_each` call of at most 64 claims each, refused predicates out and the firmware's weights applied; each strand's path is decoded in order, and the entity at its other end (the subject when the observation is the object, the object when it is the subject, never the predicate) pulls back by the strand's standing, summed over every strand that reaches it; the prompt's own words pull on nothing. What pulls back hardest is printed with its pull and its strand count. Then the firmware's `for pull` steps in order: `take segment`, the rest of the branch the prompt is a run of, followed along what was observed through the continuation lookup; `take attestations N`, the N strongest strands of the prompt by `claims_of`; `take constituents N`, the N strongest strands of each constituent; `take fact`, the single curated fact when the fact branch fires; `take chain N RELATION...`, from each of the N words that pull hardest, the relations followed in order to where the chain ends. Under `top within N`, `take_top` draws among tied strands with the seed. Each strand is printed as `confidence rating deviation matches [claim]`.

## The eleven-stage forward program (`program.c`)

`Laplace-Engine/src/program.c` (`laplace turn`) implements the stateful eleven-stage pass of [20. Forward](../Sequence/Forward.md) (`RESOLVE` → `COUPLE` → `ORIENT` → `ROUTE` → `SCAN` → `COMPOSE` → `PROPOSE` → `STEER` → `SELECT` → `REALIZE` → `WITNESS`):

- **Typed coupling and channels:** `COUPLE` expands trajectory segments (`laplace_forward`), rated claims (`holds_capped`), two-key hub bubbling (`up`), multi-round frontier coupling (`rounds`, `breadth`), BLAKE3-seeded random walks with restart (`CH_WALK`), co-occurrence lift (`CH_BESIDE`), negation polarity scopes, and 4D curve-shape neighbors (`laplace_couple`).
- **Highway and strand scan:** `SCAN` walks best-first from oriented centers across both `lp_highway_edges` in the mapped `highway.bin` ROM and rated database claims.
- **Stepwise election and receipts:** `PROPOSE`, `STEER`, `SELECT`, and `REALIZE` compare proposals key by key (`elect`) without collapsing channels into one scalar, appending each chosen constituent to the active trajectory and streaming JSONL receipts (`--receipt`) before `WITNESS` records `[prompt, response]`.
- **`Batch 2` & `Batch 4` roadmap:** `Batch 2` collapses `program.c`'s per-turn SQL round trips into 2–3 batched binary probes (`<100–200ms`), weights content obligations ahead of stop-word question frames, and adds Gödel OODA gates (`Laplace-Engine#10`, `#31`), while `Batch 4` enforces pre-`COUPLE` authority scopes and machine-cost compute envelopes (`Laplace#1708`, `#1709`).
