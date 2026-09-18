# CNX-20260918-407 — Pre-Inference Admission Hook Strategy Review Report

## Classification

`BEFORE_AGENT_RUN_RETAINED_WITH_RUNTIME_ATTESTATION_NEXT`

CogentNexus should retain OpenClaw's `before_agent_run` typed hook as the canonical Ticket-first pre-inference enforcement boundary.

The exact OpenClaw 2026.7.1-2 source identity (`0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c`) defines `before_agent_run` as a lifecycle gate that runs after session resolution and workspace preparation and before model inference. It has the session/run context, loaded prompt/history, trusted owner metadata, and a native pass/block result. The hook runner defaults this hook to fail-closed.

The alternative hooks are useful for other purposes but are not superior Ticket-first enforcement boundaries. No admission-hook migration is justified.

The next implementation boundary is therefore runtime attestation: prove, before semantic traffic, that the active OpenClaw global hook runner actually contains CogentNexus `before_agent_run` registrations in the installed runtime.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Task: `CNX-20260918-407`
- Parent: `CNX-20260918-406`
- Executor/reviewer: ChatGPT
- Operator final authority
- OpenClaw installed version baseline: `2026.7.1-2 (0790d9f)`
- Exact upstream source commit used for architecture ordering: `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c`

This task is repository/source architecture review only. No production runtime mutation and no semantic/provider request occurred.

## Historical reconciliation

The review intentionally does not repeat CNX-380 through CNX-405.

Important predecessor results:

| Task | Accepted relevance |
|---|---|
| CNX-380 | Exact isolated loader/global-runner lifecycle reproduced missing `before_agent_run` under one fixture. |
| CNX-381 | Real loader invoked plugin `register(api)`; `api.on("before_agent_run")` reached host registration and could be rejected by hook policy. |
| CNX-385 | Runtime config `plugins.entries.<id>.hooks.allowConversationAccess=true` is a supported host contract and normalization preserves it. |
| CNX-391 | Exact production-shaped true-policy replay accepted `before_agent_run` into the real registry; false-policy control did not. |
| CNX-394/395 | `plugins list --json` hook count/name projection is not live Gateway typed-hook registry proof. |
| CNX-399–401 | Cache/re-registration/registry replacement mechanisms are real, but production occurrence remains unproven. |
| CNX-404/405 | Available read-only production evidence cannot bind loader invocation/cache/registry identity/typed-hook acceptance to the live PID. |

Therefore another hook-policy projection test or another static cache-lifecycle trace would duplicate stronger existing evidence.

## Exact OpenClaw boundary comparison

### 1. `before_model_resolve`

Exact source:
`src/agents/embedded-agent-runner/run/setup.ts`

`resolveHookModelSelection()` calls `before_model_resolve` before runtime-model resolution so plugins can override provider/model.

Properties:

- early enough to precede model selection;
- receives prompt and agent/session context;
- does not receive the loaded session-history payload that `before_agent_run` receives;
- is a modifying hook for provider/model selection, not an input gate;
- call site catches errors and logs a warning, then execution continues.

Decision:

`NOT_SUITABLE_AS_CANONICAL_TICKET_FIRST_GATE`

Using it for Ticket-first would mix CNX admission with OpenClaw-owned provider/model routing and would weaken the existing separation of ownership.

### 2. `before_prompt_build`

Exact source:
`src/agents/embedded-agent-runner/run/attempt.prompt-helpers.ts`

It runs after queued-turn context preparation and allows prompt/system-context modification.

Properties:

- sees prompt and messages;
- useful for context injection;
- executed through `runBeforePromptBuild`;
- errors are explicitly caught and converted to `undefined`;
- its result contract is prompt mutation, not block/pass admission.

Decision:

`NOT_SUITABLE_AS_CANONICAL_TICKET_FIRST_GATE`

It is intentionally fail-open for prompt assembly.

### 3. `before_agent_reply`

Exact source:
`src/auto-reply/reply/get-reply.ts`

It runs before ordinary LLM execution and may return `{ handled: true, reply }` to short-circuit the model.

Properties:

- early enough for some Web Chat/auto-reply flows;
- has session identity and cleaned body;
- uses first-claim-wins semantics;
- intended for synthetic reply interception;
- does not expose loaded history in the event;
- belongs to reply-resolution/auto-reply semantics rather than the universal embedded-agent inference gate;
- moving Ticket-first here would risk surface-specific behavior and duplicate handling when other agent entry points reach the embedded runner directly.

Decision:

`NOT_SUITABLE_AS_CANONICAL_TICKET_FIRST_GATE`

It may be useful as an optional early observation/interception surface, but not as the authoritative Ticket-first enforcement boundary.

### 4. `before_agent_run`

Exact source:
- `src/plugins/hook-types.ts`
- `src/plugins/hooks.ts`
- `src/agents/embedded-agent-runner/run/attempt.ts`

OpenClaw source explicitly documents:

> Fires after session resolution and workspace preparation, before model inference.

The event contains:

- user prompt;
- loaded session history;
- active system prompt;
- channel/account/sender identity;
- trusted `senderIsOwner` bit.

The hook context contains:

- run ID;
- session key;
- session ID;
- workspace;
- provider/model context where available;
- trigger/channel identity.

The runner:

- treats it as a lifecycle gate;
- merges decisions with block dominance;
- stops remaining handlers when a block wins;
- sets the default failure policy for `before_agent_run` to `fail-closed`;
- applies a modifying-hook timeout.

The embedded runner executes it immediately before the provider stream preparation/call path. If it blocks or throws, `skipPromptSubmission` is set and inference does not proceed.

Decision:

`CANONICAL_TICKET_FIRST_GATE — RETAIN`

This boundary matches the CogentNexus invariant exactly:

```text
session/context prepared
      |
      v
CNX Ticket-first admission
      |
  pass / block
      |
      v
provider-independent model execution
```

### 5. `inbound_claim`

Exact source family:
`src/auto-reply/reply/dispatch-from-config*.ts`, hook runner claiming semantics.

Properties:

- ingress/channel ownership claim;
- first claim may take over message handling;
- tied to inbound dispatch/binding behavior;
- precedes Agent Core and therefore lacks the finalized inference context;
- not a universal embedded-agent provider-independent enforcement boundary.

Decision:

`NOT_SUITABLE_AS_CANONICAL_TICKET_FIRST_GATE`

Using it would couple CNX admission to transport/channel ingress.

### 6. `model_call_started`

Exact hook contract:
`src/plugins/hook-types.ts`, `src/plugins/hooks.ts`.

OpenClaw documents this hook in source as sanitized model-call metadata observation and executes it as a void hook.

Properties:

- provider/model/run/call identity is excellent for evidence correlation;
- handler returns `void`;
- runs through the void-hook path;
- observation semantics are fire-and-forget/fail-open;
- not an inference admission gate.

Decision:

`OBSERVABILITY_ONLY`

It is useful to prove that no model call occurred before a Ticket/admission record, but it cannot replace `before_agent_run`.

## CogentNexus handler review

Current source:
`plugins/cogentnexus-openclaw/src/index.ts:753+`.

The registered `before_agent_run` handler performs:

1. run/workspace/session bookkeeping;
2. creates an admission trace ID;
3. immediately emits `admission.trace.started`;
4. emits `admission.trace.input`;
5. only then evaluates delivery markers, post-compaction special paths, owner eligibility, classification, Ticket persistence, and pass/block disposition.

There is no silent eligibility return before `admission.trace.started`.

Therefore, for an execution where the active CNX handler actually runs, an admission-start trace should exist before ordinary eligibility/classification.

This materially narrows the interpretation of previous no-Ticket/no-trace semantic runs: a hidden `durableAdmissionEligible` early return before tracing is not the explanation.

## Architecture matrix

| Boundary | Session identity | Loaded history | Provider independent | Can synchronously prevent inference | Failure semantics | Canonical Ticket-first suitability |
|---|---:|---:|---:|---:|---|---|
| `before_model_resolve` | Yes | No | No — owns model override phase | No gate contract | fail-open at caller | No |
| `before_prompt_build` | Yes | Yes | Mostly | No gate contract | fail-open at caller | No |
| `before_agent_reply` | Yes | No | Mostly | Can short-circuit reply path | claiming/first-win | No |
| `before_agent_run` | Yes | Yes | Yes | **Yes** | **fail-closed** | **Yes** |
| `inbound_claim` | transport/session dependent | No | No — ingress surface | claims message handling | claiming | No |
| `model_call_started` | Yes | No raw conversation | Yes | No | observation/void | No |

## Provider/model switching implication

Retaining `before_agent_run` preserves the desired ownership split.

OpenClaw may change the selected provider/model via native session/model routing before an inference turn. CogentNexus does not need to route that selection.

At the admission boundary, CogentNexus only needs to preserve:

- session identity;
- Ticket/generation ownership;
- policy/admission;
- durable continuation/delivery semantics.

The provider/model selected for the turn can remain metadata.

This supports the target sequence:

```text
Session S
  Ollama A
  -> before_agent_run / CNX continuity
  OpenAI B
  -> before_agent_run / same CNX continuity
  Ollama C
  -> before_agent_run / same CNX continuity
```

No provider-specific admission fork is justified.

## Why runtime attestation is the next step

Existing evidence already proves both sides independently:

1. the exact OpenClaw mechanism accepts `before_agent_run` when the correct policy reaches the loader (CNX-391);
2. production semantic runs have historically completed model inference without corresponding CNX Ticket-first evidence.

The missing practical bridge is not another static source proof. It is a pre-semantic answer to:

> Does the active Gateway's actual global hook runner currently contain CogentNexus `before_agent_run` registrations?

OpenClaw 2026.7.1-2 publicly exports the hook-runner runtime through:

`openclaw/plugin-sdk/plugin-runtime`

whose source re-exports `../plugins/hook-runner-global.js`. The package export map also exposes `./plugin-sdk/plugin-runtime`.

This creates a candidate supported runtime-attestation mechanism that can be developed and tested in the CogentNexus repository without altering provider routing.

A follow-up implementation should prefer:

- read-only inspection of the active global runner;
- hook count / presence only;
- non-secret structured diagnostic;
- no attempt to mutate or re-register host hooks through the attestation path;
- no provider call;
- no TicketStore mutation.

The attestation must be timed after plugin registry activation, not during the early `register(api)` phase.

## Decision

Retain:

`before_agent_run` as the single canonical Ticket-first enforcement gate.

Do not migrate Ticket-first admission to:

- `before_model_resolve`;
- `before_prompt_build`;
- `before_agent_reply`;
- `inbound_claim`;
- `model_call_started`.

Use `model_call_started` only as a post-gate evidence correlation surface.

The next bounded implementation should add a supported, read-only runtime attestation of active `before_agent_run` visibility, with tests, before any further semantic provider/model requalification.

## Hard-fence accounting

- Production Gateway restart/reload: 0
- Production config mutation: 0
- Provider/model/auth mutation: 0
- Semantic/model request: 0
- TicketStore mutation: 0
- OpenClaw dependency patch: 0
- CogentNexus production deployment: 0
- Release/tag/main: 0
- Force push/history rewrite: 0

## Final classification

`BEFORE_AGENT_RUN_RETAINED_WITH_RUNTIME_ATTESTATION_NEXT`
