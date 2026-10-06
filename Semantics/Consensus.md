# Consensus

Everything attested about a claim, as a whole, provides its overall score: a Glicko-2 standing that tells how hard a strand tugs back.

## Deduplication

Same content means the same hash, and the deduplication applies to the attestations, to form a consensus.

## Glicko-2

Glicko-2 is what tells how hard a strand tugs back, and it replaces a lot of conventional AI mechanisms. See [Research: Learning](../Research/Learning.md#rating-one-matchup-at-a-time) and [Research: Chess](../Research/Chess.md).

## Matchups

There are no global, delayed rating periods. As content is observed, first in, first out, the matchups are played.

Repetition is run length, read off the tree: a sentence pasted a million times into one prompt is one vertex with a run length of a million in M; the same message across turns lengthens the session's trajectory; a corpus asserting `[forces, NOUN]` in k records is that strand occurring k times under the corpus's trunk. A witness plays one matchup per strand per ingestion, its outcome at its trust, with n, the run length, carried as the certainty of its assertion. The client folds a source's repeats before the database sees anything, so the database receives one update per strand per witness. Different witnesses play first in, first out.

n is never played as n separate Glicko-2 games, because repetition played that way does not limit itself. For n identical results against one opponent in one period, 1/v = n·g²·E(1−E), and μ′ − μ = n·g·(s−E) / (1/φ*² + n·g²·E(1−E)), which tends to (s−E) / (g·E(1−E)) as n grows: one full Newton step, larger for a low-trust witness than for a high-trust one. Low trust only needs more games to get there: a million refutations at an opponent deviation of 1500 would take a claim at 2300 with deviation 60 to −720, with deviation 1.9. Run length as the certainty inside one matchup has no such runaway: a million identical repeats from one witness are one matchup with n = 1,000,000. Across users or witnesses, repeats are separate witnesses, independent only as far as their dependence roots are. Because a standing saturates, the run length n is also kept as a count beside the claim, never only merged into the standing. Copies count once: a derived witness records its lineage, so dependence never masquerades as independent confirmation.

A number a source states, such as WordNet's `tag_cnt 10742`, is content, an observation, not games. Packaging is not repetition: a cross-product table layout, the Predicate Matrix's rows, or an automatic tagger's per-token output, FrameNet's BNC and PENN layers or Universal Dependencies EWT's mostly automatic UPOS, repeating one fact is not the source saying it again.

Incoming records play existing records, for attestation and Glicko-2 scores. Querying picks the records with higher scores, but does not change scores.

The more something is attested to, the more its score rises or lowers, just like a chess rating. Uncertainty, source trust, and the like all affect an attestation's weight and how much it can change a consensus: a low-trust user prompt or social media post weighs far less than the results of mathematical algorithms or curated academic sources.

## Trust

Trust runs from MANDATE, 1.0, down through mathematical results, academically curated datasets, user-curated corpora, user prompts, and social media posts, to 0, or to −1, since attestations are a win, draw, or loss. Laplace's own prompts are lower trust than user prompts, by design.

AI models rank above user prompts, around user-curated sources, and below academically curated datasets: still curated content, but honestly, still the opinions of others.

There are also trusts that differentiate subjects, pronouns, stopwords, and so on: a trust level for part of speech, for sense, and for dependency relation, so that filler does not drown everything. See [Research: Trust](../Research/Trust.md).

## Entry

A witness or claim entering for the first time starts from a stock default for its level of attestation: whether synonyms matter more or less than meronyms, nouns than verbs, proper nouns than stopwords, and the source's trust, stability, and uncertainty.

## No ETL

There are no delayed consensus folds. ETL is forbidden: no delayed segments that group everything together, no lazy, manually updated hot caches, and no SQL doing the heavy operations.
