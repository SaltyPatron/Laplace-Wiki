# Consensus

Everything attested about a claim, as a whole, provides its overall score: a Glicko-2 standing that tells how hard a strand tugs back.

## Deduplication

Same content means the same hash, and the deduplication applies to the attestations, to form a consensus.

## Glicko-2

Glicko-2 is what tells how hard a strand tugs back, and it replaces a lot of conventional AI mechanisms.

## Matchups

There are no rating periods. As content is observed, first in, first out, the matchups are played.

## No ETL

There are no consensus folds. ETL is forbidden: no delayed segments that group everything together, no lazy, manually updated hot caches, and no SQL doing the heavy operations.
