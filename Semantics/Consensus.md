# Consensus

Everything attested about a claim, as a whole, provides its overall score: a Glicko-2 standing that tells how hard a strand tugs back.

## Deduplication

Same content means the same hash, and the deduplication applies to the attestations, to form a consensus.

## Glicko-2

Glicko-2 is what tells how hard a strand tugs back, and it replaces a lot of conventional AI mechanisms. See [Research: Learning](../Research/Learning.md#rating-one-matchup-at-a-time) and [Research: Chess](../Research/Chess.md).

## Matchups

There are no global, delayed rating periods. As content is observed, first in, first out, the matchups are played.

If WordNet says a dog is a noun 30 times, that is one attestation with 30 games. An attestation is one per strand and witness: its games, how many times that witness asserts the strand, and a score, and Glicko-2 plays that series, n games in the witness's rating period, at its trust. The client folds a source's repeats before the database sees anything, so the database receives one update per strand per witness. Different witnesses play first in, first out.

Run-length encoding is content structure only: identical consecutive children in a path, with the run in M. A sentence pasted a million times into one prompt is a run in that prompt's content, an observation that attests nothing; the same message across turns lengthens the session's trajectory. Across users or witnesses, repeats are separate witnesses, independent only as far as their dependence roots are. Copies count once: a derived witness records its lineage, so dependence never masquerades as independent confirmation.

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
