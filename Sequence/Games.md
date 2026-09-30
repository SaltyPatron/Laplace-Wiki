# 28. Games

The Knowledge Arena turns the entity world, trajectories, evidence, and search into deterministic, replayable games over the same substrate, where a challenge pins the world epoch, the rules, the scopes, and the envelope, a game is a witnessed trajectory, and the receipt makes every score recomputable.

Games are a consumer and proving surface, not a second intelligence stack. They make exact identity, sparse traversal, evidence provenance, resource accounting, replayability, and experiment boundaries visible enough that humans can challenge the machine directly, and they make the compute model of [17. Envelope](Envelope.md) tangible: deeper and wider play spends a larger envelope over the same world.

## Before this stage

The chain through [23. Learning](Learning.md). Game rules are firmware, [18. Firmware](Firmware.md).

## As built

None. In the monorepo: `docs/guides/knowledge-arena.md` names the verbs MATCH, CONNECT, COMBINE, EXPLORE, PLAY; `/v1/explore/matchup` and `matchup/verdict`, `ops.arena_counts`, `Contracts/Matchup.cs`, the web `explore/matchup` view; the guide names issues #1401, #1404, #1420, #1421 as the owners of the rest ([Monorepo: Models](../Reference/Monorepo.md#models-export-code-chess-and-games)).

Status: **monorepo for the matchup; the challenge, receipt, and replay specified**. Every operation below is from the invention documents; [Reference: Traceability](../Reference/Traceability.md#28-games) indexes it.

## Operations, per challenge

### 28.1 Name the verb

- **In:** the game.
- **Do:** MATCH, A against B, compares shared and different evidence; CONNECT, A to B, finds an admissible typed path; COMBINE, A plus B, satisfies a composition or bridge obligation from both; EXPLORE materializes a bounded query-relative world around A; PLAY runs a challenge, rules, and event trajectory over the same operations. None owns private identity, embeddings, truth, meaning, scoring, or search.
- **Out:** the obligation the challenge compiles into.
- **From:** `docs/guides/knowledge-arena.md` §One machine, several game verbs.

### 28.2 Pin the challenge generation

- **In:** a ranked challenge.
- **Do:** the Tetris property: every contestant gets mechanically comparable state, the challenge set id and ordered queue, a closed world and evidence epoch, provider, relation, and calculation rules, source, domain, time, and sense scope, hop, fanout, and resource boundaries, anti-hub and specificity constraints, the visibility law, the scoring and tie law, and the server timing and event-order law. Later substrate growth produces a new generation instead of changing yesterday's board. Practice may target the live world; ranked play binds a closed epoch.
- **Out:** the challenge generation.
- **From:** `docs/guides/knowledge-arena.md` §Ranked fairness.

### 28.3 Resolve the pieces as entities

- **In:** the challenge's start, target, and inputs.
- **Do:** pieces are canonical entities under declared recipes; names, handles, translations, notations, and aliases are realization state, and missing pretty text does not make an entity missing. Submitted text resolves to actual entities and structured name-role realization; the Name Game is not `split(' ')` plus a private dictionary.
- **Out:** the entities.
- **From:** `docs/guides/knowledge-arena.md` §Identity is not the label and §Name Game.

### 28.4 Play through the program

- **In:** each action.
- **Do:** [20. Forward](Forward.md), with COUPLE preserving which typed routes answer before the game's routing collapses the problem into one path. CONNECT and Golf route A*, Dijkstra, and best-first path operators; Witness Hunt routes evidence and provenance operators under the dependence law, where copied sources do not become independent corroboration; COMBINE routes composition and bridge operators, with validity before novelty and no hidden intended result; Graphle gives typed feedback, hop bounds, relation overlap, containers, without leaking the target. A no-repeat rule forbids an entity already in the event trajectory: game firmware, not ontology. The hot path is prepared set access and one native search operator, never one call per hop.
- **Out:** the event trajectory `challenge → state → relation → state → … → completion, failure, or timeout`, each occurrence reusing canonical content.
- **From:** `docs/guides/knowledge-arena.md` §Query-relative game cognition, §Flagship modes, §Native execution grain.

### 28.5 Score by components

- **In:** the finished trajectory.
- **Do:** no universal one-number score is required. Compare lexicographically or by declared weights, retaining validity and obligations satisfied, server elapsed time, transition count, path and search cost, standing and evidence constraints, actual hops, fanout, candidate, and frontier work, machine work where measured, penalties, and an optional novelty component. Validity and hard rules come before style. A fast invalid path does not beat a valid one. A degree is always under a declared rule and epoch: raw, witnessed, typed, temporal, source, or cross-domain.
- **Out:** the score, with its components.
- **From:** `docs/guides/knowledge-arena.md` §Scoring law and §Laplace Degree.

### 28.6 Receipt and replay

- **In:** the run.
- **Do:** bind the challenge generation and queue, the substrate epoch, the exact inputs, the rule and firmware identity, provider and relation scope, source and domain scope, the envelope, the visibility policy, the selected transitions, routes, and evidence roots, the standing used, actual work and timing, the disposition, and the event trajectory fingerprint. Post-round cards, the best-known path under the same rule, the weakest edge used, the most disputed edge, equal-cost alternatives, a bridge new to the challenge history, each name the rule and epoch that make them meaningful.
- **Out:** a replayable receipt.
- **From:** `docs/guides/knowledge-arena.md` §Replay receipt and §Post-round derivations.

### 28.7 Admit results after the match

- **In:** the artifacts.
- **Do:** a ranked match never mutates the pinned world while contestants are compared; paths and results are recorded as match artifacts and admitted into a later epoch after the frozen comparison closes, and never self-certify as truth.
- **Out:** the next epoch.
- **From:** `docs/guides/knowledge-arena.md` §Ranked-state mutation law.

## What this stage leaves behind

A surface where the invention's identity, search, evidence, and cost are played against by people, with every score recomputable from a receipt.

## Without this stage

Laplace works. It is harder to see, and harder to be challenged.
