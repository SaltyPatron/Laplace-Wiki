# Reads

The read commands compute the entity on the client, fetch one set from the database through the container index, and do everything else in the engine: `hop`, `translate`, `degrees`, `fills`, and `pull`.

`pull.c` says of itself: this is not yet the forward pass; it is the lookups the forward pass is made of. Nothing here changes a standing.

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

Two lookups: `[word, FROM, ?]`, ordered as the firmware's `order` says, the witness's own order first under `order witness`, then standing, giving the concepts; then `[?, TO, concept]` for each target language, ordered by standing. Measured: `[dog, eng, ?]` 3.3 ms, `[?, language, i46360]` for eight languages 1.2 ms.

## laplace degrees

A best-first search from one entity toward another over `lp_frontier`: every claim that holds the current entity is a strand, its cost `lp_cost(standing, k, lambda)`, the entity at its other end reached at the accumulated cost, up to `hops` hops with at most `fan` strands read per entity, `--batch` entities expanded per round trip. With a target, the cheapest chain and its claims; without, what is nearest. The estimate is 0, so the search is Dijkstra; landmarks and the geodesic distance are documented and not built.

A read is route planning, and the highway is its road network. The road classes are the identifier systems, the highway's type lists: words in each language, a wordnet's synsets, the ILI, the ISO 639 languages, FrameNet's frames, frame elements and lexical units, VerbNet's classes and roles, PropBank's rolesets, VerbAtlas's frames, the parts of speech, dependency relations and lexicographer files. The interchanges are the mapping strands where a route changes class: the lexicalizations, CILI's maps, SemLink, the Predicate Matrix, MapNet, VerbAtlas, WordFrameNet and FrameBase. A trip is planned by A*, changing class at the interchanges, its cost a strand's −ln of its confidence plus λ a hop; a node that holds more claims than the fan, such as `NOUN` or `eng`, is a fan-limited node, reached and not crossed. The geometric estimate is close to zero for content-derived coordinates, so landmarks, the highway nodes, give the heuristic, and the highway ROM, the type lists and the mapping edges, is the precomputed freeway network. As built, `degrees` is Dijkstra, A* with an estimate of 0, over claims read from the database, and no read walks the highway ROM's edges.

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

## What is specified beyond this

The eleven-stage program of [20. Forward](../Sequence/Forward.md), the coupling field, the typed channels, the trace, and the envelope are specified in the monorepo and not built here. The built reads are the operators that program calls: containment, continuation, the claims of an entity, the two-lookup translation, the best-first search over costs.
