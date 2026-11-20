# 21. Sessions

A tenant, a user, a session, a turn, a message, a tool call, and a content artifact are distinct entities; a session is a handle over the growing ordered trajectory of its turns, like a git ref, and not a content identity, every turn is content with its receipt, and chat, the OpenAI-compatible endpoint, MCP, the CLI, SQL, and the chess lab all bind the same program to it.

A conversation is like a chess game: each turn is its own entity and a point on the trajectory of the conversation. Laplace never forgets and has no fixed context window, because Laplace is the context window: prompt and session history are content and occurrence state inside the same substrate, and any part of the world can be treated as a prompt. State is reconstructed from the session trajectory and its witnessed dependencies, never from a process-local transcript or a topic-summary cache.

## Before this stage

[20. Forward](Forward.md): the program a turn runs. [16. Authority](Authority.md): the tenant and principal. [11. Content](Content.md): every turn is content.

## Operations

### 21.1 Establish the identities

- **In:** a caller.
- **Do:** resolve the tenant, the user or participant, the session, and for this request the turn, its messages, its tool calls, and the content artifacts it carries, each a distinct form: the tenant is authorization and isolation, the user or participant a witness, the session a handle, the turn one act, a message a content trunk, a tool call and its result a calculation, an artifact a file trunk with exact reconstruction, and the response Laplace's own content at its trust, attesting its dependence on the prompt. Tenant scope is authorization and isolation, not semantic trust; the participant, the model, the tool, the corpus, the analyzer, and the feedback source keep distinct source identities within it.
- **Out:** the identity hierarchy of the request.
- **From:** `docs/specs/34_Conversational_Provenance.md` §Identity hierarchy.

### 21.2 Keep the session handle as a projection

- **In:** the session.
- **Do:** the session handle stores its growing ordered turn manifest as a Projection physicality. Its constituent turn identities resolve to canonical content physicalities admitted through the governed writer. The handle never acquires a content physicality under a mutable manifest, and the projection does not claim that immutable whole-session snapshots have been admitted as content. The handle works like a git ref: a mutable pointer, never a content identity, whose referents, the turns, messages, artifacts, and receipts, are content with content-derived IDs.
- **Out:** the session's trajectory.
- **From:** `docs/specs/34_Conversational_Provenance.md` §Identity hierarchy.

### 21.3 Decompose the prompt in memory and bind prior-turn discourse referents

- **In:** the request and the session's prior turn trajectory (or `messages[]` history).
- **Do:** decompose the prompt **in C memory from mapped `tier0.bin` in microseconds**—never blocking the response on a synchronous database `COPY` of the prompt before answering. A multimodal prompt with text, an image, and audio is one trunk, `[metadata, content]`, whose content is `[text, image, audio]`, each decomposed down to Tier-0 codepoints; OCR or ASR links are explicit calculations with their analyzer receipts. Session and turn ordinal remain trajectory position, never hashed into content `lp_id`s, so identical prompt text across two turns is one entity occurring twice. **Resolved entities, topics, and open obligations from prior turns enter `RESOLVE` and seed `COUPLE` / `SCAN` with the `DISCOURSE` operand role** (weighted below explicit new content anchors when the user switches topic, and promoted directly when pronouns, demonstratives, definite descriptions, or elliptical follow-ups such as `"Where was he born?"`, `"What about its memory usage?"`, or `"Why?"` refer back), while keeping prior-turn and current-turn provenance distinct.
- **Out:** the in-memory turn observation and resolved prior-turn discourse seeds for [20. Forward](Forward.md) operations 20.1 and 20.2.
- **From:** `docs/specs/34_Conversational_Provenance.md` §Turn contract; `docs/read-path.md` §4.

### 21.4 Run the one program (with drop-in `/v1/chat/completions` compatibility)

- **In:** the turn and discourse context of 21.3.
- **Do:** run [20. Forward](Forward.md) in-process under the caller's `.firmware`, authority, and envelope. Every surface—Web UI, OpenAI-compatible `/v1/chat/completions`, MCP, CLI `laplace turn`, SQL, and Chess Lab—drives the exact same C forward loop without template fallbacks. For drop-in compatibility with unmodified OpenAI SDKs, IDE clients, and agent harnesses, `/v1/chat/completions` maps standard fields cleanly instead of rejecting them with HTTP 400:
  - `messages[]` (`system`, `developer`, `user`, `assistant`, `tool`) → ordered discourse context, turn-level format/language/verbosity/persona instructions ([18. Firmware](Firmware.md) operation 18.3), and the active turn observation;
  - `max_tokens` / `max_completion_tokens` → compute envelope output cap ([17. Envelope](Envelope.md) operation 17.1);
  - `temperature` → firmware near-tie selection spread (`0` = deterministic top election; `> 0` = bounded seeded near-tie spread, [18. Firmware](Firmware.md) operation 18.10);
  - `seed` → deterministic selection and replay seed ([18. Firmware](Firmware.md) operation 18.10);
  - `stop` → realization stop sequence(s) ([20. Forward](Forward.md) operation 20.10);
  - `stream` → SSE incremental realization over the same pass;
  - `tools`, `tool_choice`, and `response_format` → typed action proposals and structured output constraints; standard sampling hints (`top_p`, `presence_penalty`, `frequency_penalty`) map to firmware diversity/anti-repetition bounds or are accepted gracefully.
- **Out:** the response, its provenance/attribution receipt (`SUM(share_bp) = 10000`), and its semantic trace.
- **From:** `docs/OPERATING_SEQUENCE.md` §4; `docs/specs/34_Conversational_Provenance.md` §API parity; `docs/INVENTOR_RECORD.md` §Product.

### 21.5 Witness the turn at completion

- **In:** the completed response of 21.4.
- **Do:** commit the episodic turn (`[prompt, response]`), provenance receipt, `firmware_id`, and any tool calls/results at turn completion (or asynchronously off the streaming critical path; omitted on stateless ephemeral read-only requests). Because `[prompt, response]` is content-addressed, retrying the same turn in a session deduplicates naturally without multiplying observations (`turn_witness` in `src/program.c`, `laplace turn`, and `laplace said`). Explicit user feedback and runtime statements enter through `laplace witness` ([Reference: Ingest](../Reference/Ingest.md#what-a-runtime-witness-states)).
- **Out:** the durable episodic turn on the session trajectory.
- **From:** `docs/specs/34_Conversational_Provenance.md` §Turn contract; `docs/specs/39_Personality_Firmware.md` §5.

### 21.6 Correct, refer back, and return

- **In:** a later turn.
- **Do:** a correction adds testimony that refutes or supersedes a prior claim while the original turn is preserved. Anaphora and topic return resolve against the ordered session trajectory and evidence scope, and survive a process restart because nothing lived only in a process. Unsupported claims stay unknown or cause abstention under the declared policy. Derived topic or orientation caches may accelerate reads and remain invalidatable projections.
- **Out:** later selection changed, history intact.
- **From:** `docs/specs/34_Conversational_Provenance.md` §Conversation state and §Acceptance.

### 21.7 Isolate and inspect

- **In:** any read.
- **Do:** reads default to the caller's authorized tenant and session context; source-scoped and pooled views are explicit. Every response can expose a bounded receipt of the evidence sources, relations, operation stages, selection, and writes the turn caused.
- **Out:** the receipt, on request.
- **From:** `docs/specs/34_Conversational_Provenance.md` §Isolation and inspection.

## What this stage leaves behind

A witnessed conversation trajectory per session, one program behind every surface, and a turn contract that lets a correction, a reference, or a restart be answered from the record.

## Without this stage

Every surface would invent its own memory, its own template path, and its own idea of who said what.
