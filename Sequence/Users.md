# 22. Users

A user's prompt is content, admitted at user-prompt trust as observation and zero semantic attestation, pulled under that user's firmware within that user's authority and envelope, and only now does Laplace answer anyone.

Everything before this stage is what has to exist before a user can do anything. Users will not be ingesting models or Wiktionary or Tatoeba; the inventor seeds those. Users will just be talking to it, and the seeded, higher-trust knowledge is what makes sense of what they say.

## Before this stage

All of [1. Unicode](Unicode.md) through [21. Sessions](Sessions.md).

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

### 22.5 Decompose the prompt in memory and admit uploads losslessly

- **In:** the user's prompt and any attached files.
- **Do:** [21. Sessions](Sessions.md) operation 21.3. The prompt decomposes in C memory from `tier0.bin` in microseconds, landing on the exact same `lp_id`s as every recorded word, phrase, or sentence in the substrate with zero synchronous database `COPY` blocking the answer. Attached user documents or media decompose losslessly through their format recipes, and nothing in the prompt is normalized, lower-cased, or stripped.
- **Out:** the in-memory prompt DAG and trunk `lp_id`, plus any uploaded artifact trunks.
- **From:** [Identity: Same content, same hash](../Storage/Identity.md#same-content-same-hash); `docs/INVENTION.md` §15; `docs/INVENTOR_RECORD.md` §Identity.

### 22.6 Keep prompts as observations; honor presentation instructions without escalating authority

- **In:** the prompt and anything the user uploads.
- **Do:** normal user prompts and uploads create observation and trajectory state and **zero semantic attestations merely by being said**: the seeded higher-trust facts are what the prompt's words are read against, so a million prompts asserting the earth is flat move `consensus` standing by zero, while unverified feedback accounts are bounded by causal-lineage and Sybil governance ([13. Consensus](Consensus.md) operations 13.2 and 13.3; [16. Authority](Authority.md) operation 16.4)—never by capping independent witnesses across an entire trust class. Explicit user feedback (`confirm` / `refute`) enters the governed feedback lane of [23. Learning](Learning.md). Turn-level `system`, `developer`, and user instructions asking for an output format, target language, verbosity, or persona (`"Reply in concise JSON"`, `"Explain like a pirate"`, `"Answer in Spanish"`) steer `ORIENT`, `STEER`, and `REALIZE` for that turn or session ([18. Firmware](Firmware.md) operations 18.3 and 18.13), whereas prompt instructions asking for unauthorized capabilities, restricted scopes, or standing mutations grant zero privileges and alter zero truth.
- **Out:** in-memory observation state, turn-level presentation framing, and governed feedback where explicitly submitted.
- **From:** [Attestations: Observations](../Semantics/Attestations.md#observations); [18. Firmware](Firmware.md) operation 18.3; `docs/INVENTOR_RECORD.md` §Attestations.

### 22.7 Pull, answer, and witness at turn end

- **In:** the prompt DAG of 22.5 and the firmware of 22.2.
- **Do:** execute [20. Forward](Forward.md) in `2–3` batched binary probes (`<100–200ms`), then commit episodic witnessing at turn completion ([21. Sessions](Sessions.md) operation 21.5). Querying reads standing and never mutates it. Coherent multi-clause answers are realized in the target language with witness attribution (`SUM(share_bp) = 10000`); polysemous or genuinely disputed questions answer from the strongest/shared attested structure, surface contested views with provenance, or ask a concise clarifying question, while honest `ABSTAIN` is reserved strictly for when zero relevant witnessed evidence exists or authority denies disclosure.
- **Out:** the answer and its provenance receipt.
- **From:** [Pull](../Semantics/Pull.md); [20. Forward](Forward.md) operations 20.8 to 20.11; `docs/guides/knowledge-authority.md` §Honest abstention.

## What this stage leaves behind

The first use of Laplace, the first observations that came from a user rather than a corpus, and the first consequences for a firmware to be rated by.

## Without everything before it

There is nothing to prompt.
