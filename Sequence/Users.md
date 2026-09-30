# 22. Users

A user's prompt is content, admitted at user-prompt trust as observation and zero semantic attestation, pulled under that user's firmware within that user's authority and envelope, and only now does Laplace answer anyone.

Everything before this stage is what has to exist before a user can do anything. Users will not be ingesting models or Wiktionary or Tatoeba; the inventor seeds those. Users will just be talking to it, and the seeded, higher-trust knowledge is what makes sense of what they say.

## Before this stage

All of [1. Unicode](Unicode.md) through [21. Sessions](Sessions.md).

## As built

None: `laplace pull PROMPT` computes the prompt's trunk on the client and records nothing ([Reads: laplace pull](../Reference/Reads.md#laplace-pull)); no prompt is admitted as content and no user exists. In the monorepo: `UserPromptContent.cs`, `ResponseContent.cs`, `UserArtifactContent.cs`, `/v1/content/text` and `/v1/content/code`; the trust classes `UserPromptContent` 0.30 and `ResponseContent` 0.20; `converse.chat` witnesses the prompt under UserPrompt and the response under Response, the side of [Conflicts C1](Conflicts.md) that attests; `LAPLACE_AUTH_DEV_PRINCIPAL` for a sandbox ([Monorepo: Surfaces](../Reference/Monorepo.md#surfaces-sessions-authority-and-the-envelope)).

Status: **monorepo**. Every operation below is from the invention documents; [Reference: Traceability](../Reference/Traceability.md#22-users) indexes it.

## Operations, per user

### 22.1 Compose the user's effective mind

- **In:** the user.
- **Do:** a person's usable Laplace is composed, not trained: the shared world, plus licensed and institutional knowledge grants, plus private organizational or personal knowledge, plus witnessed personal experience, plus governance and firmware, plus the current active scope, plus the current compute envelope. A school grants curriculum packages by grade; an employer adds and removes project access; a user activates only the portion relevant to one task. "I know kung fu" is the product verb: grant or materialize an authorized, receipted portion of the existing witnessed world.
- **Out:** the user's packages and capabilities, [16. Authority](Authority.md).
- **From:** `docs/CAPABILITIES.md` §"AI for every human"; `docs/INVENTIONS.md` #122.

### 22.2 Give the user a firmware

- **In:** the user.
- **Do:** [18. Firmware](Firmware.md), for this human being: an image, with its identity, chosen by the principal or by governance within authority, whose standing from [23. Learning](Learning.md) is visible evidence for that choice. Whether Laplace may pick among activated images by standing on its own is open, Q4. How the knowledge is navigated, and how an answer is reached, is individual to each human being; the same records can be pulled under different firmware, and what differs is the selection.
- **Out:** the firmware the user's passes run under.
- **From:** [Personality firmware: Knowledge and control](../Semantics/Firmware.md#knowledge-and-control); `docs/specs/39_Personality_Firmware.md` §6 and §9 Q4.

### 22.3 Set the user's operating language

- **In:** the user.
- **Do:** users have an operating language, while Laplace can speak any. Language is a filter on the claims, applied when querying, and a realization choice when rendering: the forward pass reads the prompt's language through the bindings, reads standing on the language-neutral key, and realizes the key through the bindings in the query's language. Laplace speaks Unicode and renders language.
- **Out:** the language filter and the realization language.
- **From:** [Semantics](../Semantics/README.md); `docs/plan/ASSIMILATION_ROADMAP.md` workstream B.

### 22.4 Set the user's envelope

- **In:** the user's entitlement.
- **Do:** [17. Envelope](Envelope.md): the hops, fanout, and work this user's tier grants, over the same world. Support-provider entitlement enters as an external witness under [16. Authority](Authority.md) operation 16.9.
- **Out:** the ceiling.
- **From:** `docs/CAPABILITIES.md` §Compute depth is the product tier.

### 22.5 Admit the prompt as content

- **In:** the user's prompt.
- **Do:** [21. Sessions](Sessions.md) operation 21.3. The prompt lands on the same nodes as any other content with the same words: a prompt that repeats a recorded sentence is that sentence, and deduplicates against it. Uploads are ordinary digital content through their format's decomposer, with exact reconstruction declared, because a document the user asked Laplace to keep must be handed back byte for byte. Nothing in the prompt is normalized, lower-cased, or stripped.
- **Out:** the prompt's trunk and the upload's trunks.
- **From:** [Identity: Same content, same hash](../Storage/Identity.md#same-content-same-hash); `docs/INVENTION.md` §15; `docs/INVENTOR_RECORD.md` §Identity.

### 22.6 Record what the user gave as observation

- **In:** the prompt and anything the user uploads.
- **Do:** normal digital content, such as what users upload during normal usage, does not give attestations. It gives observations: the physicality trajectory alone gives precedes, contains, co-occurrences, and more, and the seeded higher-trust facts are what the prompt's words are then read against. A prompt creates exact observation and trajectory state and zero semantic attestations merely by being said; where any of it is played as an attestation at all, it enters under `UserPromptContent` at 0.30, below user-curated corpora and above social media, and Laplace's own response at `ResponseContent` 0.20 is lower still, by design. A user's explicit `attest confirm` or `attest refute` is feedback; whether it is testimony by the user as a witness or an assertion that becomes a matchup only after independent adjudication is part of conflict C1. A prompt asking for a personality or an unauthorized effect installs no policy value and grants no capability.
- **Out:** observations, and feedback into the lanes of [23. Learning](Learning.md).
- **From:** [Attestations: Observations](../Semantics/Attestations.md#observations); `docs/INVENTOR_RECORD.md` §Attestations; `docs/specs/39_Personality_Firmware.md` §9 C1 and §11.

### 22.7 Pull, and answer

- **In:** the trunk of 22.5 and the firmware of 22.2.
- **Do:** [20. Forward](Forward.md), the whole program, and [21. Sessions](Sessions.md) operation 21.5 to witness it. Querying picks the records with higher scores and does not change scores: no standing changes because of a pull. The answer comes back in the user's language with its receipt, and an honest abstention comes back as one when the world does not support an answer, the evidence is ambiguous, the envelope ran out, or the user lacks authority to be told.
- **Out:** the answer.
- **From:** [Pull](../Semantics/Pull.md); [Consensus: Matchups](../Semantics/Consensus.md#matchups); `docs/guides/knowledge-authority.md` §Honest abstention.

## What this stage leaves behind

The first use of Laplace, the first observations that came from a user rather than a corpus, and the first consequences for a firmware to be rated by.

## Without everything before it

There is nothing to prompt.
