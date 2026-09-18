# CNX-20260918-406 — Real Provider Runtime Baseline: Ollama Web Chat End-to-End Trace

Status: `READY_FOR_HERMES`

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260918-405`
- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`
- Product goal: `docs/architecture/goals/REAL_PROVIDER_MODEL_RUNTIME_USAGE_GOAL.md`
- Development plan: `docs/architecture/goals/REAL_PROVIDER_MODEL_RUNTIME_DEVELOPMENT_PLAN.md`

The Operator explicitly authorized continued work toward the real provider/model runtime goal after CNX-405. This task is the first authorized work item from the new development plan.

## Objective

Map the current known-good Ollama Web Chat path end-to-end so that the next implementation task can add/qualify runtime provider and model selection without inventing a parallel provider architecture.

Trace the real path:

```text
Web Chat
 -> provider/model selection or current model state
 -> outbound message/request
 -> session/conversation lookup
 -> provider/model resolution
 -> Agent Core execution
 -> Ollama invocation
 -> streaming/result lifecycle
 -> assistant turn persistence
 -> next turn in the same session
```

The task is complete when the repository/runtime ownership boundary is explicit enough to answer:

1. Where does Web Chat obtain and transmit the selected model/provider?
2. Where is that selection stored, if anywhere?
3. Is provider inferred from model identity, explicitly selected, or globally configured?
4. Which OpenClaw modules own model/provider resolution?
5. Which CogentNexus modules intercept or alter the path?
6. Where is session continuity maintained?
7. Where is the provider request actually dispatched?
8. Where are stream events normalized and returned to Web Chat?
9. Where is assistant output persisted?
10. What exactly happens on the next turn?
11. Which existing OpenClaw mechanisms should be reused for runtime switching?
12. What is the smallest missing behavior that prevents the target experience:
    `Ollama -> another model -> OpenAI -> Ollama` inside one session?

## Context

CNX-405 completed the production registry lifecycle mapping. That investigation established mechanism boundaries but did not provide additional user-facing provider capability.

The project direction is now explicitly:

> Make CogentNexus-OpenClaw usable like ordinary OpenClaw: select provider, select model, chat normally, change provider/model, and continue in the same conversation/session.

Ollama is the known working baseline. Therefore abstraction must be derived from the working Ollama vertical slice rather than designed independently.


## Reviewer preliminary evidence

Before Hermes execution, ChatGPT performed a read-only repository surface check and found existing v0.9.5 material that must be treated as prior evidence rather than reinvented:

- `docs/PROVIDERS.md` states that managed lifecycle is Ollama-only while Cloud routes are OpenClaw-owned pass-through. OpenClaw owns Cloud authentication, provider/model selection, routing, runtime, lifecycle, probing, and recovery.
- `docs/operations/acceptance/V095_PROVIDER_SWITCH_ACCEPTANCE.md` already defines the intended live acceptance sequence `Ollama -> Cloud A -> Cloud B -> Ollama` through normal Web Chat while preserving CNX session/Ticket/generation/policy continuity.
- `plugins/cogentnexus-openclaw/src/v090-model-selection-boundary.test.ts` proves that `sessions.patch` model selection is passed through without creating or mutating CNX Ticket state.
- `tests/test_v095_provider_switch_matrix.py` encodes provider switching as OpenClaw-owned metadata that must not mutate CNX mode/generation/provider ownership state.
- `docs/operations/coordination/reports/CNX-20260910-315-provider-cli-ownership-matrix.md` explicitly forbids CNX lifecycle commands from becoming provider/model routing authority.
- `docs/operations/coordination/reports/CNX-20260910-315-provider-independent-capabilities-update.md` removed providerMode as a capability kill-switch so CNX capabilities can remain active in pass-through.
- CNX-357 and CNX-367 already prove a real Dashboard OpenAI model path: OpenAI / GPT-5.6 Luna produced a visible and runtime-recorded response.
- CNX-375 and CNX-376 prove the current blocker is not basic OpenAI model availability. The user-visible OpenAI request succeeds, while CNX Ticket-first continuity is bypassed because `before_agent_run` is absent from the live composed hook registry and dispatch is skipped.

Therefore CNX-406 must distinguish two questions:

1. **OpenClaw provider/model switching path:** likely substantially native/already present.
2. **CogentNexus continuity across that path:** currently impaired by the live hook-registry/admission boundary.

Do not propose a new CNX provider router unless evidence proves the OpenClaw-owned route cannot satisfy the target.

## Required Inputs

Read before execution:

1. `docs/architecture/goals/REAL_PROVIDER_MODEL_RUNTIME_USAGE_GOAL.md`
2. `docs/architecture/goals/REAL_PROVIDER_MODEL_RUNTIME_DEVELOPMENT_PLAN.md`
3. `docs/operations/coordination/reports/CNX-20260918-405-production-repeated-registration-caller-lifecycle-correlation-report.md`
4. current `ACTIVE.md`
5. current `STATUS.md`
6. current branch HEAD from GitHub, treated as authoritative

Do not trust an embedded SHA if GitHub has moved.

## Work Package A — Repository Surface Inventory

Identify the current source modules responsible for:

- Web Chat / Dashboard message submission;
- Web Chat model/provider selector or model state;
- session/conversation identity;
- message persistence;
- agent invocation;
- model/provider resolution;
- provider configuration;
- Ollama provider integration;
- streaming/event delivery;
- tool dispatch integration;
- CogentNexus before/after hooks or execution interception relevant to normal chat.

For each module, record:

- path;
- primary symbol/function;
- role;
- caller/callee relationship;
- whether it is OpenClaw-owned or CogentNexus-owned.

## Work Package B — Web Chat Selection Trace

Determine current UI behavior.

Answer with source evidence:

- Is there currently a model selector?
- Is there a provider selector, or is provider derived from model/config?
- What data structure represents the selection?
- What request/RPC/message carries the selected model/provider?
- Does selection persist per session, globally, per agent, or only in UI state?
- Does switching a model today create/change a session?
- Is the selection applied immediately or only on the next turn?

If Web Chat source is not present in this repository because it comes from the installed OpenClaw package, identify the exact installed/source artifact and line/symbol ownership instead of guessing.

## Work Package C — Session and Persistence Trace

Map:

```text
incoming Web Chat message
 -> session identifier
 -> history/context retrieval
 -> execution request
 -> assistant output
 -> persisted session/history
 -> next turn
```

Record exactly:

- session ID source;
- session storage owner;
- model/provider metadata stored with session/turn, if any;
- whether historical turns are provider-neutral;
- whether tool state is session-scoped;
- what survives model/provider changes today.

## Work Package D — Provider/Model Resolution Trace

Map the current resolution logic from selected/default model to actual Ollama execution.

Identify:

- model identifier format;
- provider identifier format;
- model-to-provider resolution;
- default model resolution;
- agent-specific override;
- session-specific override, if any;
- turn-specific override, if any;
- configured endpoint/profile ownership;
- capability metadata ownership;
- actual provider dispatch function.

Distinguish observed source behavior from assumptions.

## Work Package E — Ollama Invocation Trace

Trace one real or source-defined Ollama execution path:

```text
resolved target
 -> Ollama adapter/client
 -> request construction
 -> endpoint invocation
 -> response/stream handling
 -> normalized event/result
```

Record:

- transport/library;
- request payload boundary;
- cancellation signal;
- timeout behavior if visible;
- stream callbacks/events;
- tool-call handling if present;
- error normalization.

Do not expose secrets.

## Work Package F — CogentNexus Intersection Map

Identify every CogentNexus interception point on the normal chat path.

For each point answer:

- before or after provider resolution?
- before or after session context assembly?
- before or after model invocation?
- does it read/change provider/model?
- can it accidentally bind session behavior to a provider?
- does it need modification for runtime switching?

This map is important because the target should reuse OpenClaw provider machinery rather than replace it unless required.

## Work Package G — Baseline Acceptance Characterization

Without mutating production provider configuration, document the known-good Ollama baseline:

- normal Web Chat message path;
- selected/configured Ollama model;
- same-session next turn;
- streaming behavior;
- tool behavior already proven;
- relevant current runtime/config evidence available read-only.

If a live semantic request would be required to prove something not already available, mark it `REQUIRES_LIVE_AUTHORIZATION` rather than sending it during this task.

## Work Package H — Gap Analysis Against Target

Compare current behavior to the goal.

Classify each required target behavior:

- `ALREADY_NATIVE`
- `ALREADY_NATIVE_BUT_CNX_INTERFERES`
- `PARTIALLY_PRESENT`
- `MISSING`
- `UNKNOWN_NEEDS_LIVE_QUALIFICATION`

At minimum classify:

1. provider listing;
2. model listing;
3. model selection;
4. provider selection;
5. session-sticky selection;
6. per-turn override;
7. same-session model switching;
8. same-session provider switching;
9. Ollama real chat;
10. OpenAI real chat;
11. cross-provider context continuity;
12. tools across provider switch;
13. streaming;
14. cancellation;
15. failure recovery;
16. restart persistence.

## Work Package I — Smallest Next RED Test

End the task by specifying the smallest test that should fail today and whose GREEN state directly advances the user-visible goal.

Prefer a test near the real ownership boundary.

Examples of acceptable direction:

- same session ID with different requested execution targets on sequential turns;
- Web Chat-selected model reaches provider resolution without session recreation;
- provider/model selection resolves through OpenClaw-native model registry.

Do not implement the repair in CNX-406.

## Evidence Requirements

The final report must include:

- exact authoritative starting and ending branch HEAD;
- exact file paths and symbols;
- line/range references where practical;
- sequence diagram for the Ollama vertical slice;
- state ownership table;
- provider/model resolution table;
- CogentNexus interception table;
- target gap matrix;
- direct evidence vs inference section;
- unknowns requiring live qualification;
- smallest recommended RED test;
- recommendation for the next bounded implementation task.

## Allowed Actions

- Read repository source and documentation.
- Read current GitHub branch/ref state.
- Read installed/runtime source artifacts if available through the existing authorized environment.
- Read configuration with secrets redacted.
- Read existing logs/reports/evidence.
- Add/update the CNX-406 report and coordination documentation.
- Use local source analysis/search tools that do not mutate production.

## Hard Fences

- No production Gateway restart/reload.
- No production configuration mutation.
- No environment mutation.
- No Scheduled Task mutation.
- No provider credential changes.
- No provider/model selection mutation in production.
- No semantic/model/provider/Dashboard request unless separately authorized by the Operator after CNX-406.
- No OpenAI live request.
- No new Ollama semantic request solely for this task.
- No TicketStore/admission/routing/auth mutation.
- No production extension/artifact deploy.
- No OpenClaw dependency patch.
- No CogentNexus production repair.
- No release/tag/main.
- No force push/history rewrite.
- Do not create/start CNX-407 yourself.

## Exit Classification

Use one of:

- `OLLAMA_VERTICAL_SLICE_MAPPED_READY_FOR_RED_TEST`
- `OLLAMA_VERTICAL_SLICE_PARTIALLY_MAPPED`
- `BLOCKED_BY_MISSING_SOURCE_OR_RUNTIME_EVIDENCE`

The preferred success state is:

`OLLAMA_VERTICAL_SLICE_MAPPED_READY_FOR_RED_TEST`

## Closeout

Publish the CNX-406 report.

Set `ACTIVE.md` and `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`.

Verify branch HEAD and clean worktree.

Stop. Do not create/start CNX-407.
