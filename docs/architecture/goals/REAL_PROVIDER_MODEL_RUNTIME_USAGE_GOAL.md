# Real Provider and Model Runtime Usage Goal

Status: `PRODUCT / ARCHITECTURE GOAL`  
Owner: `Operator`  
Scope: `CogentNexus-OpenClaw`  
Applies to: Web Chat, session execution, provider routing, model selection, and future provider adapters

## Purpose

CogentNexus-OpenClaw must be usable in normal day-to-day operation in the same practical way that ordinary OpenClaw is used: the operator opens the Web Chat, selects a provider and model, sends messages, changes provider or model when needed, and continues working in the same conversation/session.

The target is not merely to prove that an OpenAI API call, an Ollama request, or another provider adapter can return a response in isolation.

The target is a complete user-visible execution path in which provider and model selection are runtime choices rather than permanent properties of a session.

## Primary User Goal

The operator must be able to:

1. Open the CogentNexus/OpenClaw Web Chat.
2. Select an available provider.
3. Select a model exposed by that provider.
4. Send a message and receive a real response.
5. Continue working in the existing session.
6. Change the model without creating a new session.
7. Change the provider without creating a new session.
8. Continue the same conversation with its existing context after that change.
9. Keep the same agent/tool execution semantics as far as the selected provider supports them.
10. Add future providers without redesigning the session/core architecture.

A representative acceptance scenario is:

```text
Open Web Chat
    |
    v
Provider: Ollama
Model: <local model>
    |
    v
User sends messages
    |
    v
Conversation/context develops
    |
    v
Operator changes Provider: OpenAI
Operator selects an OpenAI model
    |
    v
User sends the next message
    |
    v
The same session continues with the existing conversation/context
```

The provider/model switch itself must not require a new conversation.

## Core Architectural Principle

Provider and model are execution choices, not the identity of the session.

The intended boundary is:

```text
HUMAN INTENT
    |
    v
SESSION / CONVERSATION
    |
    v
AGENT CORE
    |
    v
PROVIDER ROUTER
    |
    +--> Ollama Adapter ----> Selected Ollama Model
    |
    +--> OpenAI Adapter ----> Selected OpenAI Model
    |
    +--> Provider N Adapter -> Selected Provider-N Model
    |
    v
EXECUTION / TOOLS / RESULT
```

The session owns continuity.

The provider router owns selection of an execution backend.

A provider adapter owns provider-specific transport, authentication/configuration, model discovery/selection semantics, streaming translation, cancellation, and provider-specific error normalization.

The Web UI must expose provider/model selection but must not become the architectural owner of provider-routing logic.

## Session Continuity Invariant

Changing provider or model must not, by itself:

- create a new session;
- discard conversation history;
- silently reset CogentNexus state;
- discard ticket/project context;
- change agent identity;
- clear tool state that is defined as session-scoped;
- require the user to repeat prior conversation context.

Conceptually:

```text
Session S
  conversation = C
  state        = X

Execution 1:
  provider = Ollama
  model    = A

Execution 2:
  provider = OpenAI
  model    = B

Execution 3:
  provider = Ollama
  model    = C

Session remains S.
Conversation remains C.
Session-scoped state remains X.
Only the execution target changes.
```

Provider-specific limitations may affect individual turns, but they must not redefine session identity.

## User Experience Target

Provider and model selection should be available through the normal Web Chat workflow.

The intended interaction is approximately:

```text
[Provider: Ollama v] [Model: model-a v]

User: ...
Assistant: ...

[Provider: OpenAI v] [Model: model-b v]

User: continue from the previous analysis...
Assistant: ...
```

The operator should not need to:

- edit configuration files for each switch;
- restart the Gateway merely to change model;
- create another conversation merely to change provider;
- manually reconstruct conversation context;
- invoke a provider-specific CLI for normal chat usage.

Administrative configuration may still be needed to make a provider available initially, such as credentials or endpoint configuration. Once admitted and available, normal provider/model selection should be a runtime Web Chat operation.

## Provider Contract Direction

All providers should converge on a common execution contract sufficiently expressive for the Agent Core.

The contract should cover, as applicable:

- provider identity;
- available/configured state;
- model identity;
- model listing or configured model resolution;
- request submission;
- streaming response events;
- non-streaming response;
- cancellation;
- timeout handling;
- normalized errors;
- usage/accounting metadata when available;
- capability declaration;
- tool/function calling capability;
- structured output capability where supported;
- context/window constraints;
- provider-specific metadata without leaking provider-specific behavior into Session/Core.

Provider-specific details should remain behind the adapter/router boundary whenever practical.

## Ollama as the Baseline

Ollama already represents the known working real-use path and should be treated as the behavioral baseline during provider generalization.

Work on additional providers must not regress normal Ollama operation.

The useful development sequence is:

```text
Trace known-good Ollama path
        |
        v
Extract/confirm common provider contract
        |
        v
Qualify provider/model selection boundary
        |
        v
Add/qualify OpenAI real chat path
        |
        v
Switch Ollama <-> OpenAI inside one session
        |
        v
Qualify tools, streaming, failure handling, and recovery
        |
        v
Generalize for Provider N
```

This sequence is intended to derive abstraction from a known working path rather than inventing an abstraction disconnected from real execution.

## Practical Milestones

### M1 — Ollama Real Chat Baseline

The Web Chat can use Ollama and a selected local model in real operation.

This milestone is the behavioral reference and must remain functional.

### M2 — OpenAI Real Chat

The Web Chat can select an admitted OpenAI provider/model, send a real message, and receive the real response through the normal session path.

A standalone provider test or isolated API request does not satisfy this milestone.

### M3 — Model Switching in the Same Session

The operator can change from one model to another compatible model and continue the same conversation without creating a new session or losing context.

### M4 — Provider Switching in the Same Session

The operator can switch, for example:

```text
Ollama -> OpenAI -> Ollama
```

while retaining the same session and conversation continuity.

### M5 — Common Agent/Tool Path

The same CogentNexus agent/tool execution architecture is used regardless of provider, subject to declared provider/model capabilities.

Provider-specific code must not create separate incompatible agent architectures.

### M6 — Provider Qualification

Each provider can be qualified against a common test matrix covering at least:

- provider availability;
- model selection;
- normal chat;
- streaming;
- session continuity;
- model switching;
- provider switching;
- tool execution where supported;
- authentication/configuration failure;
- unavailable model;
- timeout;
- cancellation;
- transport/provider error;
- recovery after a failed turn.

### M7 — Extensible Provider Boundary

A new provider can be added through the provider contract/adapter boundary without redesigning Session, Agent Core, or Web Chat conversation semantics.

## Acceptance Criteria for the Main Goal

The main goal is considered achieved only when a real user can demonstrate all of the following through the ordinary product path:

1. Open Web Chat.
2. Use Ollama with a selected model.
3. Exchange real messages.
4. Change to another Ollama model and continue the same conversation.
5. Change to OpenAI and select an available OpenAI model.
6. Exchange a real OpenAI-backed message in the same session.
7. Change back to Ollama or another admitted provider.
8. Continue the same conversation without reconstructing context.
9. Observe no unintended session reset caused solely by the provider/model change.
10. Use the common CogentNexus execution path rather than a provider-specific side channel.

The strongest representative end-to-end acceptance statement is:

> I can open Web Chat, converse through Ollama, switch to OpenAI from the normal model/provider selector, and continue the same conversation in the same session.

## Non-Goals

This document does not require every provider to expose identical capabilities.

It does not require:

- pretending that all models support the same context size;
- pretending that all providers support tool/function calling;
- pretending that all providers support identical streaming events;
- silently emulating unsupported capabilities;
- binding session identity to a specific provider;
- duplicating Agent Core for each provider.

Differences should be surfaced through capabilities and normalized behavior rather than hidden by false equivalence.

## Relationship to CogentNexus Direction

This goal supports the broader CogentNexus invariant:

```text
Human intent
    -> coherent session/context
    -> agent reasoning/execution
    -> selectable intelligence provider/model
    -> tools/actions/results
```

Changing the source of intelligence must not unnecessarily break the continuity of the intent being carried through the system.

The provider is a replaceable execution resource.

The session and the preserved direction of the user's work are the higher-level continuity boundary.

## Relationship to Coordination Tasks

This document is a durable product/architecture goal, not an authorization to execute a coordination task.

It does not create, start, or modify a CNX task.

In particular, creating this document must not be interpreted as bypassing any active hard fence, production mutation restriction, review boundary, or task-number sequencing requirement recorded in `docs/operations/coordination/ACTIVE.md` and `STATUS.md`.

Future coordination tasks should reference this document when planning provider/model runtime work, qualification, implementation, or acceptance.

## Implementation Guidance

When this goal becomes an authorized implementation task, the preferred first step is repository/runtime archaeology rather than immediate redesign:

1. Trace the current real Ollama path from Web Chat selection through session dispatch, routing, provider invocation, streaming, and response persistence.
2. Identify which parts are OpenClaw-native behavior and which parts CogentNexus intercepts or owns.
3. Identify the existing provider/model selection state and its lifetime.
4. Determine whether provider/model selection is already session-scoped, turn-scoped, or globally configured.
5. Preserve the known-good path wherever possible.
6. Introduce only the minimum architectural changes required for runtime provider/model switching.
7. Qualify OpenAI through the same end-to-end path.
8. Prove continuity through real Web Chat acceptance before broadening to additional providers.

## Design Test

For every future provider-related architectural decision, ask:

> If the user changes provider or model now, can the same human intent continue through the same session without forcing unrelated state to restart?

If the answer is no, the design should explain why that discontinuity is intrinsically required rather than an accidental consequence of provider coupling.
