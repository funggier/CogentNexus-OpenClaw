# Real Provider and Model Runtime Usage — Development Plan

Status: `PRODUCT / ARCHITECTURE DEVELOPMENT PLAN`  
Owner: `Operator`  
Scope: `CogentNexus-OpenClaw`  
Goal reference: `docs/architecture/goals/REAL_PROVIDER_MODEL_RUNTIME_USAGE_GOAL.md`  
Coordination status: This document is planning guidance only. It does not create or authorize a CNX coordination task.

---

## 1. Purpose

This plan turns the real provider/model runtime usage goal into an executable development sequence.

The target user experience is:

```text
Open Web Chat
    |
    v
Select Provider
    |
    v
Select Model
    |
    v
Chat normally
    |
    v
Change Model and continue
    |
    v
Change Provider and continue
    |
    v
Keep the same session, conversation, CogentNexus-OpenClaw state, and execution semantics
```

The plan deliberately begins from the known working Ollama path and derives the common provider architecture from real runtime behavior.

The plan does **not** begin by replacing OpenClaw's provider subsystem or by inventing a new abstraction before the existing path is understood.

The governing principle is:

> Preserve working behavior first. Generalize only what is proven to be provider-specific.

---

## 2. Desired End State

The system should eventually satisfy all of the following:

- Web Chat exposes available providers.
- Web Chat exposes models available/configured for the selected provider.
- Provider and model can be changed during an existing conversation.
- A provider/model change does not create a new session by itself.
- Conversation history remains available.
- CogentNexus-OpenClaw session/ticket/project state remains intact.
- The same Agent Core and tool pipeline remain in use.
- Provider-specific differences are expressed through capabilities and adapter behavior.
- Ollama remains fully usable.
- OpenAI becomes fully usable through the same ordinary Web Chat path.
- Additional providers can be integrated through the same contract.
- Streaming, cancellation, timeout, failure, retry/recovery, and tool behavior are qualified.
- Provider changes are observable and auditable without leaking credentials.

The final acceptance path is:

```text
Session S
  |
  +-- Ollama / Model A -> turn 1
  |
  +-- Ollama / Model B -> turn 2
  |
  +-- OpenAI / Model C -> turn 3
  |
  +-- Ollama / Model A -> turn 4
  |
  +-- same session
  +-- same conversation
  +-- same CogentNexus-OpenClaw continuity
```

---

## 3. Planning Principles

### 3.1 Real path before abstraction

Use the real working Ollama path as the reference implementation.

Do not assume that the provider boundary is where the current code structure appears to place it.

Trace actual runtime flow first.

### 3.2 Session continuity above provider identity

Provider and model are execution selections.

Session identity must not depend on provider identity.

### 3.3 Minimum-delta integration and routing authority

OpenClaw is the provider/model/auth/routing authority for Cloud/pass-through operation in the current v0.9.6 architecture.

Prefer preserving and qualifying existing OpenClaw provider/model behavior over creating a parallel CogentNexus-OpenClaw-only provider stack.

CogentNexus-OpenClaw owns continuity, Ticket/session/generation policy, durable delivery/recovery fences, and provider-independent execution safeguards. It must not become a second provider-routing authority.

A second independent provider architecture would create drift, duplicated lifecycle rules, and future maintenance cost.

### 3.4 Capability-aware behavior

Models/providers are not assumed equivalent.

Differences should be explicit:

- tools/function calling;
- streaming;
- structured output;
- reasoning controls;
- context limits;
- image/multimodal support;
- cancellation behavior;
- usage metadata;
- other provider-specific capabilities.

### 3.5 Vertical qualification

A feature is not complete merely because an adapter returns data.

A vertical slice must be demonstrated through:

```text
Web Chat
 -> Session
 -> Selection state
 -> Provider router
 -> Provider adapter
 -> Model
 -> Stream/result
 -> Persistence
 -> Same session on next turn
```

### 3.6 Preserve the known-good Ollama experience

Every provider-related change must include an Ollama regression check.

### 3.7 Evidence before repair

When behavior differs from expectation:

1. capture actual runtime state;
2. locate the owning layer;
3. reproduce with the smallest test;
4. repair the true owner;
5. re-run the vertical qualification.

### 3.8 No task-number preallocation

This plan does not assign future CNX task IDs.

Future coordination tasks should be created only when authorized by the active coordination state.

---

## 4. Architectural Target

The preferred logical boundary is:

```text
+-------------------------------------------------------------+
|                         Web Chat                            |
|  provider selector | model selector | conversation UI      |
+-------------------------------+-----------------------------+
                                |
                                v
+-------------------------------------------------------------+
|                    Session / Conversation                   |
| history | session state | ticket/project references         |
| selected execution target metadata                          |
+-------------------------------+-----------------------------+
                                |
                                v
+-------------------------------------------------------------+
|                         Agent Core                          |
| prompt/context assembly | tools | policies | execution      |
+-------------------------------+-----------------------------+
                                |
                                v
+-------------------------------------------------------------+
|             OpenClaw Provider / Model Routing               |
| resolve provider | resolve model | auth | provider dispatch |
+-----------+-------------------+-------------------+---------+
            |                   |                   |
            v                   v                   v
        +-------+           +--------+         +-----------+
        |Ollama |           |OpenAI  |         |Provider N |
        |Adapter|           |Adapter |         |Adapter     |
        +---+---+           +---+----+         +-----+-----+
            |                   |                    |
            v                   v                    v
         Model A             Model B              Model C
```

The exact implementation may reuse OpenClaw internals rather than introducing all of these as new classes/modules.

The architecture diagram describes ownership, not mandatory file structure.

---

## 5. Ownership Boundaries

### 5.1 Web Chat owns

- displaying current provider;
- displaying current model;
- presenting available selections;
- sending the selected execution target with the normal session action;
- showing capability or availability information when useful.

Web Chat must **not** own:

- provider authentication logic;
- provider transport;
- session identity;
- provider-specific retry semantics;
- provider-specific tool translation.

### 5.2 Session layer owns

- conversation identity;
- conversation history;
- session-scoped CogentNexus-OpenClaw state;
- persisted selected provider/model metadata when persistence is desired;
- continuity across turns.

### 5.3 OpenClaw provider/model routing owns

- resolving the requested provider;
- resolving the requested model;
- OpenClaw-owned authentication/configuration;
- checking provider/model availability;
- selecting the correct provider adapter/client;
- provider/model dispatch;
- routing errors and provider-native execution semantics.

CogentNexus-OpenClaw should consume only the non-secret execution identity/capability evidence required to preserve its own continuity and safety contracts.

### 5.4 Provider Adapter owns

- provider-specific request formation;
- authentication/config consumption;
- transport;
- stream translation;
- provider-specific cancellation;
- provider-specific error mapping;
- provider/model metadata retrieval where applicable.

### 5.5 Agent Core owns

- provider-neutral conversation execution;
- prompt/context construction;
- tool exposure;
- tool-result integration;
- execution lifecycle;
- provider-neutral event handling.

---

## 6. Core Data Concepts

The implementation should converge on explicit concepts only where needed by CogentNexus-OpenClaw continuity and verification. Existing OpenClaw provider/model structures remain authoritative for routing and should be reused rather than duplicated.

### 6.1 Provider ID

Stable machine-readable provider identity.

Examples conceptually:

```text
ollama
openai
provider-x
```

### 6.2 Model ID

Provider-scoped model identity.

Avoid assuming model names are globally unique.

Conceptually:

```text
(providerId, modelId)
```

is the execution target.

### 6.3 Execution Target

A normalized selection object:

```text
ExecutionTarget
  providerId
  modelId
  optional profile/account/endpoint reference
  capability snapshot or resolved capability reference
```

Credentials must not be embedded in ordinary session history or UI-visible state.

### 6.4 Provider Capability Descriptor

At minimum, consider:

```text
chat
streaming
toolCalling
structuredOutput
multimodal
cancellation
usageMetadata
contextLimit
```

The exact capability model should be derived from real provider behavior.

### 6.5 Selection Lifetime

The implementation must explicitly decide and document whether provider/model selection is:

- per-turn;
- sticky per-session;
- inherited from agent/default configuration;
- overridden by UI for a single turn;
- persisted across application restart.

This must not remain accidental behavior.

A likely useful precedence model is:

```text
explicit turn selection
    >
session selection
    >
agent/default selection
    >
system default
```

This is a design candidate, not a requirement until verified against existing OpenClaw behavior.

---

## 7. Workstreams

The plan is divided into parallel conceptual workstreams, but execution should remain phase-gated.

### W1 — Runtime Archaeology

Understand the current end-to-end Ollama path and current OpenClaw provider/model machinery.

### W2 — Provider Contract

Extract the minimum provider-neutral contract from observed working behavior.

### W3 — Session and Selection Semantics

Define where provider/model selection lives and how it survives turns.

### W4 — Web Chat Integration

Expose provider/model selection through the normal Web Chat path.

### W5 — OpenAI Qualification

Make OpenAI work through the same path as Ollama.

### W6 — Switching Semantics

Prove model and provider switching inside one session.

### W7 — Tools and Reliability

Qualify tools, streaming, cancellation, failure, timeout, and recovery.

### W8 — Extensibility and Acceptance

Prove that a future provider can fit without redesigning Session/Core and complete release-quality acceptance.

---

# 8. Development Phases

## Phase 0 — Baseline Freeze and Evidence Pack

### Objective

Establish a trustworthy reference before provider work changes behavior.

### Required work

Record the current known-good Ollama behavior:

- OpenClaw version;
- CogentNexus-OpenClaw plugin/build identity;
- branch/commit;
- current provider configuration shape;
- current Ollama model configuration;
- Web Chat behavior;
- session identity behavior;
- streaming behavior;
- tool behavior if currently exercised;
- relevant logs/telemetry;
- clean reproduction steps.

Capture the current repository/runtime boundaries:

- where Web Chat stores or sends model selection;
- where OpenClaw resolves provider;
- where model identity is resolved;
- where session metadata is stored;
- where responses are persisted;
- where CogentNexus-OpenClaw intercepts or participates in execution.

### Deliverables

- baseline runtime map;
- baseline evidence report;
- known-good Ollama acceptance script;
- list of relevant source modules;
- list of runtime configuration sources;
- initial sequence diagram.

### Exit gate

Proceed only when the team can reproduce one real Ollama Web Chat turn and identify the major modules involved.

### Failure rule

If the current Ollama path cannot be reproduced reliably, provider generalization stops and baseline repair becomes the priority.

---

## Phase 1 — Trace the Real Ollama Vertical Slice

### Objective

Build an exact source/runtime trace from user selection to model response.

### Trace

Follow:

```text
Web Chat selection
 -> outbound request/message
 -> session lookup
 -> model/provider resolution
 -> agent execution
 -> provider invocation
 -> streaming callbacks/events
 -> assistant result
 -> session persistence
 -> next turn
```

### Questions to answer

- Does Web Chat already transmit a provider/model pair?
- Is model selection stored in conversation/session metadata?
- Is selection stored globally?
- Does OpenClaw infer provider from model ID?
- Does CogentNexus-OpenClaw alter selection?
- Where is provider authentication resolved?
- Where is streaming normalized?
- Where are tool calls normalized?
- What state is retained across turns?
- What changes when the user changes model today?
- Does the existing OpenClaw UI already support most of the required behavior when CogentNexus-OpenClaw is absent?

### Deliverables

- exact call graph;
- sequence diagram;
- state ownership table;
- provider/model resolution table;
- list of CogentNexus-OpenClaw interception points;
- list of OpenClaw-native mechanisms that should be reused.

### Exit gate

No provider abstraction work begins until the current path can be described without major unknown ownership gaps.

---

## Phase 2 — Extract and Lock the Provider Contract

### Objective

Define the smallest common contract required by the actual Agent Core.

### Method

Start from Ollama behavior.

Then compare the expected OpenAI path.

Do not add capability fields or lifecycle methods without a concrete consumer.

### Contract areas

#### Identity

- provider ID;
- model ID;
- optional provider profile/config reference.

#### Availability

- provider configured/unconfigured;
- model resolvable/unresolvable;
- credentials/config valid enough to attempt execution.

#### Request

- normalized conversation input;
- execution options;
- tools/capabilities requested;
- cancellation signal;
- tracing/correlation ID.

#### Response

- stream events;
- final result;
- tool call events;
- usage metadata where available;
- normalized finish reason.

#### Failure

Normalize at least:

- provider unavailable;
- authentication/configuration failure;
- model unavailable;
- rate/usage limitation;
- timeout;
- transport failure;
- malformed provider response;
- cancellation;
- unsupported capability.

### Contract tests

Create provider-neutral tests that both Ollama and future OpenAI paths must satisfy.

### Exit gate

Ollama passes the contract tests without breaking its existing real-use path.

---

## Phase 3 — Define Session and Selection Semantics

### Objective

Make provider/model switching behavior explicit.

### Decisions required

Define:

- whether provider selection is sticky within a session;
- whether model selection is sticky within a session;
- whether a selection can apply to one turn only;
- persistence across Gateway restart;
- behavior when the previously selected model disappears;
- behavior when provider credentials become invalid;
- inheritance from agent/default configuration.

### Required invariant

A selection change must not mutate session identity.

### Suggested state model

Conceptually:

```text
SessionExecutionPreference
  selectedProviderId
  selectedModelId
  source = ui | session | agent-default | system-default
  updatedAt
```

Do not store secrets here.

### Compatibility rule

If OpenClaw already has an equivalent state model, extend/reuse it instead of creating a CogentNexus-OpenClaw duplicate.

### Tests

- same session ID before/after model switch;
- same session ID before/after provider switch;
- conversation history remains addressable;
- CogentNexus-OpenClaw state references remain stable;
- tool/session state remains stable unless explicitly provider-scoped.

### Exit gate

Selection semantics are documented and represented by tests before UI behavior is expanded.

---

## Phase 4 — Provider/Model Discovery and Web Chat Selection

### Objective

Expose provider and model selection through the normal user workflow.

### UI behavior

Web Chat should show:

- current provider;
- current model;
- available providers;
- available/configured models;
- unavailable/disabled state when relevant;
- capability warnings only when needed.

### Important distinction

`configured` is not always identical to `currently reachable`.

Avoid making the model selector block the whole UI on expensive provider probes.

### Selection flow

Conceptually:

```text
User selects Provider
 -> model list resolves for provider
 -> user selects Model
 -> selection stored/applied
 -> next normal message uses that target
```

### UI requirements

- no Gateway restart for normal switching;
- no manual config edit for normal switching;
- selection visible before sending;
- failure must not silently fall back to another provider unless an explicit policy says so;
- user can identify which provider/model generated a turn when useful.

### Exit gate

A user can switch between at least two configured models in the Web Chat and the backend observes the correct target selection.

At this phase, both models may still belong to Ollama.

---

## Phase 5 — Ollama Multi-Model Same-Session Qualification

### Objective

Prove switching semantics before introducing cross-provider complexity.

### Acceptance sequence

```text
Session S
 -> Ollama / Model A -> response A
 -> switch
 -> Ollama / Model B -> response B
 -> switch
 -> Ollama / Model A -> response C
```

### Must prove

- Session ID unchanged.
- Conversation context retained.
- CogentNexus-OpenClaw state retained.
- Model resolution changes correctly.
- Streaming still works.
- Tool path remains intact where supported.
- No stale model state leaks between turns.

### Why this phase exists

It isolates model-switching correctness from provider-specific authentication and transport differences.

### Exit gate

Repeated same-session model switching is stable and regression-tested.

---

## Phase 6 — OpenAI Real Chat Vertical Slice

### Objective

Add/qualify OpenAI through the same normal path.

### Required work

Trace and implement only what is missing for:

```text
Web Chat
 -> existing Session
 -> Provider Router
 -> OpenAI provider path
 -> selected OpenAI model
 -> streamed/final response
 -> persisted assistant turn
```

### Authentication/configuration

Use the existing OpenClaw provider configuration mechanism wherever possible.

CogentNexus-OpenClaw should not invent a second credential store unless the existing architecture cannot satisfy required security/ownership constraints.

### Security requirements

- never persist raw credentials in conversation history;
- never emit credentials in normal logs;
- redact provider secrets in diagnostic artifacts;
- distinguish provider profile identity from secret material.

### Initial scope

The first OpenAI vertical slice should prioritize:

- real normal chat;
- correct model selection;
- streaming if the ordinary Web Chat path depends on it;
- correct failure reporting;
- same session continuity.

Do not block this phase on every advanced model capability.

### Exit gate

A real OpenAI-backed message succeeds through the ordinary Web Chat/session path.

A standalone script or isolated API test is insufficient.

---

## Phase 7 — Cross-Provider Same-Session Switching

### Objective

Demonstrate the primary product goal.

### Canonical acceptance sequence

```text
Session S

Turn 1:
  Ollama / Model A

Turn 2:
  Ollama / Model B

Turn 3:
  OpenAI / Model C

Turn 4:
  OpenAI / Model D

Turn 5:
  Ollama / Model A
```

### Verify after every turn

- Session identity;
- conversation history;
- selected execution target;
- active provider;
- active model;
- CogentNexus-OpenClaw ticket/project/session references;
- tool state;
- persistence record;
- stream completion;
- no unintended reset.

### Context compatibility

Different models may support different context sizes.

The switching layer must define what happens when existing history exceeds the newly selected model's usable context.

Possible strategies must be explicit, for example:

- normal existing context compaction;
- summarization;
- bounded history selection;
- user-visible incompatibility error.

Provider switching must not silently destroy history.

### Exit gate

The operator can move Ollama -> OpenAI -> Ollama in one conversation through the normal UI.

This is the central product acceptance milestone.

---

## Phase 8 — Tool Execution and Capability Mapping

### Objective

Make provider/model differences compatible with one Agent Core.

### Capability matrix

For each qualified model/provider, record:

- chat;
- streaming;
- tool calls;
- parallel tool calls where relevant;
- structured output;
- multimodal inputs;
- cancellation;
- token/context limits;
- usage metadata;
- other execution controls.

### Routing rule

Before execution:

```text
Agent requirement
    +
Model capabilities
    ->
admit | adapt | reject with clear reason
```

### Important rule

Do not silently emulate unsupported critical behavior in ways that change semantics.

### Tool qualification

At minimum test:

- single tool call;
- tool result returned to model;
- multi-step tool sequence;
- provider/model switch after tool use;
- cancellation during tool-enabled turn;
- failure recovery without corrupting session state.

### Exit gate

The common tool path works across the providers/models declared capable.

---

## Phase 9 — Streaming, Cancellation, Timeout, and Failure Semantics

### Objective

Normalize lifecycle behavior sufficiently for ordinary use.

### Streaming

Define provider-neutral stream events such as conceptually:

```text
turn.started
content.delta
tool.call
tool.result
usage
turn.completed
turn.failed
turn.cancelled
```

Reuse existing OpenClaw event semantics if they already cover this.

### Cancellation

Cancellation should propagate:

```text
Web Chat cancel
 -> session execution
 -> provider adapter
 -> provider transport
```

The session must remain usable afterward.

### Timeout

Differentiate:

- connection timeout;
- first-token timeout;
- overall execution timeout;
- tool timeout.

### Failure recovery

After a failed turn:

- session remains valid;
- conversation history is not corrupted;
- target can be changed;
- next turn can execute;
- failed partial output is represented consistently.

### Exit gate

Provider failures do not require session recreation and do not corrupt continuity.

---

## Phase 10 — Persistence and Restart Qualification

### Objective

Prove that provider/model selection and session continuity behave correctly across process lifecycle events.

### Scenarios

- Gateway restart with existing session;
- application restart;
- provider previously selected still available;
- provider previously selected no longer available;
- model renamed/removed;
- credential/config removed;
- fallback/default rules;
- explicit re-selection.

### Required behavior

The session must remain identifiable even when the previous execution target is unavailable.

An unavailable provider/model is an execution problem, not a reason to erase the conversation.

### Exit gate

Restart/recovery semantics are deterministic and documented.

---

## Phase 11 — Provider N Extensibility Proof

### Objective

Validate the architecture by integrating or mocking a third provider boundary without changing Session/Core semantics.

### Why

An architecture that supports only Ollama and OpenAI may still contain hidden special cases.

### Proof

A new provider should require changes primarily within:

- provider registration/configuration;
- provider adapter;
- capability metadata;
- provider-specific tests.

It should not require redesigning:

- session identity;
- conversation persistence;
- Web Chat conversation semantics;
- CogentNexus-OpenClaw ticket/project state;
- Agent Core lifecycle.

### Exit gate

A third provider or a controlled fake provider can satisfy the provider contract without structural changes to Session/Core.

---

## Phase 12 — Full Acceptance and Release Readiness

### Objective

Turn the implementation into a stable user-facing capability.

### Final acceptance matrix

#### Web Chat

- provider selector works;
- model selector works;
- current selection is visible;
- selection updates correctly;
- errors are visible and actionable.

#### Ollama

- existing baseline still works;
- multi-model switching works;
- tools still work where supported.

#### OpenAI

- real chat works;
- model selection works;
- streaming works as required;
- tools work where declared;
- failures recover cleanly.

#### Cross-provider

- Ollama -> OpenAI;
- OpenAI -> Ollama;
- repeated switching;
- switching after tool calls;
- switching after a failed turn;
- switching after restart where semantics allow.

#### Session continuity

- same session identity;
- history retained;
- CogentNexus-OpenClaw state retained;
- no unnecessary reset.

#### Reliability

- timeout;
- cancellation;
- unavailable model;
- unavailable provider;
- authentication/config failure;
- transport error;
- recovery.

### Release gate

Do not call the feature complete until the canonical real Web Chat acceptance scenario passes on the intended Windows production/runtime environment.

---

# 9. Test Strategy

Testing should form a pyramid with a mandatory real-runtime top layer.

## Level 1 — Unit tests

Test:

- provider/model parsing;
- execution target resolution;
- precedence rules;
- capability matching;
- normalized errors;
- state transitions.

## Level 2 — Provider contract tests

Run the same behavioral contract against each adapter.

## Level 3 — Integration tests

Exercise:

- router + adapter;
- session + selection state;
- streaming;
- cancellation;
- tool lifecycle.

## Level 4 — Web Chat integration tests

Exercise:

- selector state;
- message dispatch target;
- visible target;
- switching.

## Level 5 — Real provider qualification

Use real Ollama.

Use real OpenAI in an explicitly authorized qualification environment.

## Level 6 — Production/runtime acceptance

Use the actual installed/runtime path and ordinary Web Chat.

This is the final authority for “usable in practice”.

---

# 10. Observability Requirements

Provider switching will be difficult to debug without explicit correlation.

For each turn, diagnostics should make it possible to correlate:

```text
session ID
turn/request ID
provider ID
model ID
provider adapter
selection source
capability decision
start/end status
stream lifecycle
tool lifecycle
failure category
```

Do not log raw credentials.

Do not rely on model response text to infer which provider handled the request.

Where possible, diagnostics should distinguish:

- requested target;
- resolved target;
- actually invoked target.

This prevents silent fallback or stale-selection bugs from being misdiagnosed.

---

# 11. State Transition Model

A useful conceptual model:

```text
IDLE
  |
  | user sends turn with target T1
  v
RESOLVING_TARGET
  |
  +-- unavailable ------> TURN_FAILED -> IDLE
  |
  v
EXECUTING(T1)
  |
  +-- cancel -----------> CANCELLING -> TURN_CANCELLED -> IDLE
  |
  +-- provider failure -> TURN_FAILED -> IDLE
  |
  v
TURN_COMPLETED
  |
  v
IDLE
  |
  | user changes target to T2
  v
IDLE_WITH_NEW_SELECTION
  |
  | next message
  v
RESOLVING_TARGET
  |
  v
EXECUTING(T2)
```

Changing the selection while idle should not itself recreate the session.

Changing the selection during an active turn needs an explicit policy. A safe default is:

- current turn keeps the target with which it started;
- new selection applies to the next turn.

This avoids mid-stream provider mutation.

---

# 12. Migration and Backward Compatibility

Existing sessions may not contain explicit provider/model selection metadata.

Define migration behavior.

A safe compatibility pattern is:

```text
existing session without explicit target
 -> resolve using existing OpenClaw/default behavior
 -> optionally persist selection after the user explicitly changes it
```

Avoid bulk rewriting historical sessions unless required.

Existing Ollama-only configurations must continue to work without requiring the user to configure OpenAI.

---

# 13. Security Model

Provider expansion introduces secret and account boundaries.

The design must preserve:

- credentials outside conversation history;
- credentials outside normal logs;
- redaction in reports;
- explicit provider/config ownership;
- no secret propagation into tool prompts unless intentionally required;
- no accidental cross-provider credential reuse.

Provider selection metadata may be session-visible.

Provider secrets must not be session content.

---

# 14. Performance Considerations

Provider/model switching should not require:

- Gateway restart;
- full plugin reload;
- clearing model cache globally;
- rebuilding session context from disk on every selector interaction.

Model-list discovery should avoid blocking normal chat unnecessarily.

Caching may be used, but cache ownership and invalidation must be explicit.

A stale model catalog must fail safely when execution resolves the actual target.

---

# 15. Risk Register

## R1 — Duplicating OpenClaw provider architecture

**Risk:** CogentNexus-OpenClaw creates a parallel provider system.

**Consequence:** lifecycle drift, duplicated bugs, incompatible UI/runtime behavior.

**Mitigation:** reuse OpenClaw-native machinery whenever it satisfies the invariant.

---

## R2 — Provider becomes session identity

**Risk:** session state is keyed to provider/model.

**Consequence:** switching destroys continuity.

**Mitigation:** explicit session continuity tests.

---

## R3 — UI owns backend semantics

**Risk:** provider switching works only through UI-local state.

**Consequence:** API/automation/recovery paths disagree.

**Mitigation:** backend execution target is authoritative.

---

## R4 — Silent fallback

**Risk:** requested provider/model fails and another target is used silently.

**Consequence:** user cannot trust execution provenance.

**Mitigation:** requested/resolved/invoked target observability; explicit fallback policy only.

---

## R5 — Capability mismatch

**Risk:** a model lacking tool support is selected during tool-dependent work.

**Consequence:** broken execution or semantic drift.

**Mitigation:** capability admission before turn execution.

---

## R6 — Context-size mismatch

**Risk:** switching to a smaller-context model invalidates current history.

**Consequence:** unexpected truncation or failure.

**Mitigation:** explicit context-management policy and user-visible behavior.

---

## R7 — Regression of Ollama

**Risk:** generalization breaks the already working provider.

**Mitigation:** Ollama baseline gate at every major phase.

---

## R8 — Credential leakage

**Risk:** provider secrets appear in diagnostics/session artifacts.

**Mitigation:** credential boundary + redaction tests.

---

## R9 — Over-abstraction

**Risk:** development stalls building a universal provider framework.

**Mitigation:** add abstraction only when required by Ollama + OpenAI real paths.

---

## R10 — Investigation never reaches real use

**Risk:** repeated lifecycle studies continue without user-facing acceptance.

**Mitigation:** every phase has a vertical exit gate tied to the final Web Chat scenario.

---

# 16. Recommended Execution Order

The work should normally proceed in this order:

```text
0. Baseline freeze
1. Ollama vertical trace
2. Provider contract extraction
3. Session/selection semantics
4. Web Chat selector path
5. Ollama same-session multi-model switch
6. OpenAI real chat vertical slice
7. Ollama <-> OpenAI same-session switch
8. Tool/capability qualification
9. Streaming/cancel/failure/recovery
10. Restart/persistence qualification
11. Provider N extensibility proof
12. Full acceptance and release readiness
```

Avoid skipping directly to a large provider framework.

---

# 17. Suggested Coordination Task Slicing

When the active coordination state authorizes new tasks, slice work into bounded evidence-producing tasks.

Do not preassign CNX numbers here.

A useful sequence is:

### Task Type A — Baseline / archaeology

Read-only.

Output:

- exact source/runtime map;
- report;
- no production repair.

### Task Type B — Contract characterization

Tests/documentation first.

Output:

- provider contract;
- RED tests where behavior is missing.

### Task Type C — Minimal implementation

TDD:

```text
RED
 -> minimal repair
 -> GREEN
 -> integration
 -> runtime qualification
```

### Task Type D — Real provider acceptance

Explicitly authorized live provider traffic.

Output:

- evidence;
- exact provider/model;
- session continuity proof;
- PASS/FAIL.

### Task Type E — Regression/release gate

Output:

- Ollama regression;
- OpenAI regression;
- switching matrix;
- hard-fence review;
- release recommendation.

Each task should define:

- objective;
- authoritative branch/HEAD;
- allowed mutations;
- prohibited mutations;
- exact evidence required;
- exit classification;
- rollback/recovery boundary.

---

# 18. Milestone Map

## Milestone M1 — Known-Good Ollama Baseline

Complete when:

- Ollama real Web Chat path is reproduced;
- architecture trace exists;
- baseline tests exist.

## Milestone M2 — Explicit Runtime Selection

Complete when:

- provider/model target is explicit;
- selection semantics are documented;
- Web Chat can change models without session recreation.

## Milestone M3 — OpenAI Real Chat

Complete when:

- real OpenAI response traverses the ordinary session path;
- no provider-specific side channel is required.

## Milestone M4 — Cross-Provider Continuity

Complete when:

- Ollama -> OpenAI -> Ollama succeeds in the same conversation.

## Milestone M5 — Common Agent/Tool Path

Complete when:

- supported providers use one Agent Core/tool lifecycle.

## Milestone M6 — Reliability Qualification

Complete when:

- timeout, cancellation, unavailable target, auth/config failure, and recovery are stable.

## Milestone M7 — Extensible Provider Boundary

Complete when:

- a third provider can fit without Session/Core redesign.

## Milestone M8 — Release-Ready User Experience

Complete when:

- the production Web Chat workflow satisfies the full acceptance matrix.

---

# 19. Definition of Done

The overall provider/model runtime project is done only when all of the following are true:

1. The user can select a provider in Web Chat.
2. The user can select a model for that provider.
3. The user can send a real message through Ollama.
4. The user can switch Ollama models and continue in the same session.
5. The user can send a real message through OpenAI.
6. The user can switch OpenAI models and continue in the same session.
7. The user can switch Ollama -> OpenAI -> Ollama without creating a new conversation.
8. Conversation history remains coherent.
9. CogentNexus-OpenClaw session/ticket/project continuity remains coherent.
10. Provider/model selection is observable and auditable.
11. Tool execution uses the common Agent Core path where supported.
12. Failure/cancellation does not corrupt the session.
13. Restart behavior is deterministic.
14. Ollama baseline has not regressed.
15. OpenAI qualification is repeatable.
16. Provider-specific credentials remain outside session content and logs.
17. A future provider has a clear integration boundary.
18. Real production/runtime acceptance passes through the ordinary Web Chat path.

The decisive user-facing statement remains:

> I can use CogentNexus-OpenClaw like normal OpenClaw: choose a provider, choose a model, chat, change provider/model, and continue working in the same conversation.

---

# 20. Relationship to Current Coordination State

This plan is intentionally separate from active coordination control.

It does not:

- create a new CNX task;
- authorize production mutation;
- override `ACTIVE.md`;
- override `STATUS.md`;
- bypass a reviewer gate;
- bypass a hard fence;
- authorize provider traffic;
- authorize credential/config changes;
- authorize release/tag/main changes.

When the current coordination state permits the next work item, the next task should reference:

- this development plan;
- the real provider/model runtime usage goal;
- the latest accepted coordination report;
- the exact authoritative branch/HEAD.

---

# 21. First Authorized Work Item Recommendation

When a new coordination task is permitted, the first provider-runtime task should be a bounded read-only archaeology task:

**Working title:**

`Real Provider Runtime Baseline — Ollama Web Chat End-to-End Trace`

### Objective

Trace the current known-good Ollama path from Web Chat provider/model selection through session execution, model invocation, streaming, result persistence, and the next turn.

### Required outputs

- exact call graph;
- state ownership map;
- current provider/model selection lifetime;
- Web Chat request shape;
- session persistence behavior;
- CogentNexus-OpenClaw interception points;
- provider-resolution path;
- streaming path;
- tool path;
- minimum candidate boundary for OpenAI;
- identified unknowns;
- recommendation for the smallest RED test that proves missing runtime switching behavior.

### Mutation boundary

Prefer read-only repository/runtime evidence.

Do not change provider behavior during the archaeology task unless a later explicitly authorized task permits it.

### Why this should be first

The project already has a working Ollama path.

The fastest route to a correct multi-provider architecture is to understand and preserve that path, then make OpenAI follow it.

---

# 22. Design Compass

For every implementation decision, ask these questions:

### Continuity

Does this preserve the user's session and intent when the execution model changes?

### Ownership

Is this logic located in the layer that actually owns it?

### Reuse

Are we reusing OpenClaw behavior that already works instead of duplicating it?

### Evidence

Do we know this from the real runtime path, or are we assuming it?

### Capability

Are model/provider differences explicit rather than hidden?

### Recoverability

Can the user continue after a failed provider turn?

### Extensibility

Would Provider N fit without redesigning Session/Core?

### Practicality

Does this move the system closer to the actual Web Chat acceptance scenario?

If an implementation improves local elegance but makes any of these materially worse, it should be reconsidered.
