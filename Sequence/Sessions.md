# 21. Sessions

A tenant, a user, a session, a turn, a message, a tool call, and a content artifact are distinct entities; a session is a stable identity whose ordered trajectory contains turns, every turn is content with its receipt, and chat, the OpenAI-compatible endpoint, MCP, the CLI, SQL, and the chess lab all bind the same program to it.

A conversation is like a chess game: each turn is its own entity and a point on the trajectory of the conversation. Laplace never forgets and has no fixed context window, because Laplace is the context window: prompt and session history are content and occurrence state inside the same substrate, and any part of the world can be treated as a prompt. State is reconstructed from the session trajectory and its witnessed dependencies, never from a process-local transcript or a topic-summary cache.

## Before this stage

[20. Forward](Forward.md): the program a turn runs. [16. Authority](Authority.md): the tenant and principal. [11. Content](Content.md): every turn is content.

## As built

None: `laplace` is a command-line program with no session, turn, or surface; a prompt is `laplace pull PROMPT` ([CLI: laplace pull](../Reference/CLI.md#laplace-pull)). In the monorepo: `conversation_session.c`: a session is a Projection physicality, type 3, over its turn ids in order, rewritten on each append; `converse.session_turns`, `session_trajectory`, `session_topics`; `TurnWitness` makes the tenant the source identity and the session the context of every attestation; `/v1/chat/completions`, `/v1/completions`, the MCP server's `op` tool, the CLI's query commands, the SQL schemas `converse`, `generation`, `ops`; spec 34 ([Monorepo: Surfaces](../Reference/Monorepo.md#surfaces-sessions-authority-and-the-envelope)).

Status: **monorepo**. Every operation below is from the invention documents; [Reference: Traceability](../Reference/Traceability.md#21-sessions) indexes it.

## Operations

### 21.1 Establish the identities

- **In:** a caller.
- **Do:** resolve the tenant, the user or participant, the session, and for this request the turn, its messages, its tool calls, and the content artifacts it carries, each a distinct entity. Tenant scope is authorization and isolation, not semantic trust; the participant, the model, the tool, the corpus, the analyzer, and the feedback source keep distinct source identities within it.
- **Out:** the identity hierarchy of the request.
- **From:** `docs/specs/34_Conversational_Provenance.md` §Identity hierarchy.

### 21.2 Keep the session handle as a projection

- **In:** the session.
- **Do:** the session handle stores its growing ordered turn manifest as a Projection physicality. Its constituent turn identities resolve to canonical content physicalities admitted through the governed writer. The handle never acquires a content physicality under a mutable manifest, and the projection does not claim that immutable whole-session snapshots have been admitted as content.
- **Out:** the session's trajectory.
- **From:** `docs/specs/34_Conversational_Provenance.md` §Identity hierarchy.

### 21.3 Admit the prompt as a turn

- **In:** the request.
- **Do:** the prompt is content, [11. Content](Content.md) on the client, under the prompt source at its declared class. The turn records session and ordinal; role, participant, and source; the exact content entity and its trajectory; reply and dependency edges to prior turns or tool results; request parameters and the declared source and context scope. Prior turn and content identities enter the program as ordered discourse state with the `DISCOURSE` operand role, never rendered to a transcript and reparsed, and never merged into the prompt's semantic seed frontier.
- **Out:** the turn, and the discourse operand of [20. Forward](Forward.md) operation 20.1.
- **From:** `docs/specs/34_Conversational_Provenance.md` §Turn contract; `docs/read-path.md` §4.

### 21.4 Run the one program

- **In:** the turn of 21.3.
- **Do:** [20. Forward](Forward.md), under the caller's firmware, authority, and envelope. Roles, parameters, tools, streaming, and non-streaming alter declared inputs and transport only; they never select a weaker template path. The OpenAI-compatible surface binds roles, parameters, and tools to Laplace semantics and reports unsupported or translated behaviour honestly, without leaking transformer ontology. An MCP agent reads, witnesses, gives feedback, ingests, inspects traces, and invokes the same operation surfaces under governance. Equivalent requests over MCP, HTTP, CLI, and SQL produce equivalent semantic traces.
- **Out:** the response, its trace, and its receipt.
- **From:** `docs/OPERATING_SEQUENCE.md` §4; `docs/specs/34_Conversational_Provenance.md` §API parity; `docs/INVENTIONS.md` #78, #79, #80.

### 21.5 Witness the turn

- **In:** the response of 21.4.
- **Do:** the turn's response content, outcome, and provenance receipt, the selected operation program, the semantic trace, and `firmware_id` are appended through the governed write lane. The reply attests its dependency on the prompt under the response source; tool calls and results remain ordered and attributable. Prompt, reply, tool, and feedback witnesses use the same lane; replaying a read manufactures no testimony; the same write retried carries an idempotency key. An effect proposal is canonicalized with its firmware identity, and the executor verifies the approved envelope before execution.
- **Out:** the durable turn.
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
