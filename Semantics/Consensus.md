# Consensus

Everything attested about a claim, as a whole, provides its overall score: a Glicko-2 standing that tells how hard a strand tugs back.

## Deduplication

Same content means the same hash, and the deduplication applies to the attestations, to form a consensus.

## Glicko-2

Glicko-2 is what tells how hard a strand tugs back, and it replaces a lot of conventional AI mechanisms. See [Research: Learning](../Research/Learning.md#rating-one-matchup-at-a-time) and [Research: Chess](../Research/Chess.md).

## Matchups

There are no rating periods. As content is observed, first in, first out, the matchups are played.

Incoming records play existing records, for attestation and Glicko-2 scores. Querying picks the records with higher scores, but does not change scores.

The more something is attested to, the more its score rises or lowers, just like a chess rating. Uncertainty, source trust, and the like all affect an attestation's weight and how much it can change a consensus: a low-trust user prompt or social media post weighs far less than the results of mathematical algorithms or curated academic sources.

## Entry

A witness or claim entering for the first time starts from a stock default for its level of attestation: whether synonyms matter more or less than meronyms, nouns than verbs, proper nouns than stopwords, and the source's trust, stability, and uncertainty.

## No ETL

There are no consensus folds. ETL is forbidden: no delayed segments that group everything together, no lazy, manually updated hot caches, and no SQL doing the heavy operations.
