# 15. Users

A user's prompt is content, ingested at user-prompt trust and pulled under that user's firmware, and only now does Laplace answer anyone.

Everything before this stage is what has to exist before a user can do anything.

## Before this stage

All of [1. Unicode](Unicode.md) through [14. Pull](Pull.md).

## Operations, per user

### 15.1 Give the user a firmware

- **In:** the user.
- **Do:** [13. Firmware](Firmware.md), for this human being. How the knowledge is navigated, and how an answer is reached, is individual to each human being. The same records can be pulled under different firmware; what differs is the selection.
- **Out:** the firmware the user's pulls run under.
- **From:** [Personality firmware: Knowledge and control](../Semantics/Firmware.md#knowledge-and-control).

### 15.2 Set the user's operating language

- **In:** the user.
- **Do:** users have an operating language, while Laplace can speak any. Language is a filter on the claims, applied when querying. Laplace speaks Unicode and renders language: everything stored is Unicode content, and a language is something Laplace renders.
- **Out:** the language filter on the user's queries.
- **From:** [Semantics](../Semantics/README.md).

### 15.3 Ingest the prompt as content

- **In:** the user's prompt.
- **Do:** [14. Pull](Pull.md) operation 14.7. The prompt lands on the same nodes as any other content with the same words: a prompt that repeats a recorded sentence is that sentence, and deduplicates against it.
- **Out:** the prompt's trunk.
- **From:** [Pull: The forward pass](../Semantics/Pull.md#the-forward-pass), [Identity: Same content, same hash](../Storage/Identity.md#same-content-same-hash).

### 15.4 Record what the user gave as observation

- **In:** the prompt and anything the user uploads.
- **Do:** normal digital content, such as what users upload during normal usage, does not give attestations. It gives observations: the physicality trajectory alone gives precedes, contains, co-occurrences, and more. Where a user's input is played as an attestation at all, it enters at user-prompt trust, below user-curated corpora and above social media posts, and Laplace's own prompts are lower trust than user prompts, by design.
- **Out:** observations, at the user's tier of trust.
- **From:** [Attestations: Observations](../Semantics/Attestations.md#observations), [Consensus: Trust](../Semantics/Consensus.md#trust).

### 15.5 Pull, and answer

- **In:** the trunk of 15.3 and the firmware of 15.1.
- **Do:** [14. Pull](Pull.md) operations 14.8 to 14.10. Querying picks the records with higher scores, but does not change scores: no standing changes because of a pull.
- **Out:** the answer.
- **From:** [Pull](../Semantics/Pull.md), [Consensus: Matchups](../Semantics/Consensus.md#matchups).

## What this stage leaves behind

The first use of Laplace, and the first observations that came from a user rather than a corpus.

## Without everything before it

There is nothing to prompt.
