# CNX-20260918-419 — ChatGPT Review

## Decision

`ACCEPTED_FAILED`

Accepted primary classification:

`BLOCKED_TICKET_FIRST_ORDERING`

Accepted secondary classification:

`BLOCKED_SELECTED_ROUTE_NOT_HONORED`

## Independent verification

The authoritative branch and CNX-419 report were re-read from GitHub.

Verified from the published report:

- exactly one authenticated owner WebChat user message materialized;
- exactly one visible assistant response materialized;
- the assistant response text exactly matched the nonce;
- no semantic resend occurred;
- CogentNexus Ticket count for the turn = 0;
- accepted events = 0;
- routed events = 0;
- admission trace = absent;
- CogentNexus direct-model-call rows = 0;
- CogentNexus delivery/outbox rows = 0;
- actual native provider = `openai`;
- actual native model = `gpt-5.6-luna`;
- actual native API = `openai-chatgpt-responses`;
- post-run agent runtime = `codex`, source = `implicit`;
- no Ollama inference occurred;
- global durable CNX counts remained unchanged.

A correct visible nonce response does not satisfy Ticket-first or selected-route acceptance.

## Coordination-history reconciliation

The CNX-419 task file was temporarily marked `DRAFT_WAITING_FOR_PARENT_REPORT` after an earlier coordination race while CNX-418 reporting was still being finalized.

That stale task-file status does not invalidate the execution evidence.

The actual CNX-419 execution authority is established by:

- the published CNX-419 report;
- its recorded authoritative execution HEAD;
- the one-shot hard-fence ledger;
- ACTIVE/STATUS closeout to `WAITING_FOR_CHATGPT_REVIEW`;
- the Operator's explicit confirmation that the message was manually sent.

This review treats CNX-419 as executed and reported.

## Ticket-first root cause — source boundary proven

The Ticket-first failure is no longer a registry-visibility mystery.

CNX-416 already proved that the live composed registry contains CogentNexus `before_agent_run` hooks.

Exact OpenClaw source at:

`2026.7.1-2 (0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c)`

shows that `before_agent_run` is executed inside the built-in OpenClaw embedded attempt path:

```text
createOpenClawAgentHarness()
  -> runAttempt = runEmbeddedAttempt
  -> embedded-agent-runner/run/attempt.ts
  -> getGlobalHookRunner()
  -> runBeforeAgentRun(...)
```

However, native/plugin harness execution uses:

```text
runAgentHarnessAttempt()
  -> select harness
  -> runAgentHarnessLifecycleAttempt(harness, params)
  -> harness.runAttempt(params)
```

and `runAgentHarnessLifecycleAttempt` does not execute `before_agent_run` itself.

For a plugin harness such as Codex, the call therefore enters that plugin harness directly instead of entering the built-in `attempt.ts` gate.

CNX-419's authoritative post-run metadata says:

`agent runtime = codex, source = implicit`

This exactly explains the otherwise contradictory evidence:

```text
live registry before_agent_run = PRESENT
actual owner turn = successful
CNX admission.trace.started = absent
CNX Ticket = absent
```

The hook exists, but the selected plugin-harness execution path does not pass through the host location that invokes it.

### Accepted root-cause classification

`PLUGIN_HARNESS_BYPASSES_BUILTIN_BEFORE_AGENT_RUN_GATE`

Do not return to registry/cache/activation forensics for this defect.

## Candidate universal pre-model compatibility seam

Exact OpenClaw `dispatch-from-config.ts` executes `reply_dispatch` before normal model dispatch.

For Dashboard `chat.send`, exact `server-methods/chat.ts` establishes:

```text
clientRunId = chat.send idempotencyKey
replyOptions.runId = clientRunId
```

and exact `reply_dispatch` event construction passes:

`event.runId = params.replyOptions?.runId`

Therefore a Dashboard-specific compatibility admission bridge at `reply_dispatch` can use the same runId later emitted by provider/model-call hooks.

This is important because the existing CogentNexus Direct model-call lease joins by:

`tickets.run_id = model_call_started.runId`

No synthetic run binding is required if the early Ticket uses `reply_dispatch.event.runId`.

## Trust boundary for an early compatibility bridge

Do not reuse `durableAdmissionEligible(...)` blindly at `reply_dispatch`.

That predicate treats a missing `senderIsOwner` as eligible for non-subagent sessions, while `reply_dispatch` does not expose the same `senderIsOwner` field as `before_agent_run`.

Exact Dashboard `chat.send` does, however, place authenticated Gateway client scopes into the finalized message context:

`FinalizedMsgContext.GatewayClientScopes`

A future compatibility bridge must therefore be narrowly fenced at minimum by:

- canonical Dashboard session namespace;
- exact runId;
- finalized authenticated operator scope, e.g. `operator.admin`;
- normal direct WebChat context;
- no internal continuation/delivery marker;
- existing Ticket-intake exclusions.

Do not generalize this bridge to every channel until equivalent owner-trust mapping is proven for those surfaces.

## Duplicate safety

`TicketStore.accept()` is idempotent by:

`request_key = hash(ownerSessionKey + "\0" + runId)`

Therefore, if a built-in OpenClaw turn receives early compatibility intake at `reply_dispatch` and later reaches the existing `before_agent_run` handler with the same runId/session, a second `accept()` returns the existing Ticket as `duplicate=true`.

A production repair must still explicitly characterize route-event cardinality and `ticketedRuns` bookkeeping; idempotent Ticket creation alone is not enough to claim the whole dual-gate path is duplicate-safe.

## Selected-route mismatch — narrowed, not yet final

Exact OpenClaw source shows two distinct model-selection views.

### Gateway pre-dispatch view

`resolveSessionModelRef()` uses:

1. `providerOverride/modelOverride`;
2. otherwise runtime identity `modelProvider/model`;
3. otherwise agent/global default.

CNX-419 pre-send session metadata exposed:

`modelProvider=ollama, model=qwen3.8:27b`

so the Gateway pre-dispatch view can legitimately report Ollama/qwen.

### Reply model-selection view

`getReplyFromConfig()` begins from the resolved configured default and then `createModelSelectionState()` restores persisted session model choice through:

`resolveStoredModelOverride()`

The exact stored-override resolver reads:

- `providerOverride/modelOverride` from the session;
- or parent-session override fields.

It does not use `modelProvider/model` runtime identity as a persisted override.

CNX-418 recorded:

- `providerOverride=null`;
- `modelOverride=null`.

This creates a concrete possible discontinuity between the Gateway's pre-dispatch route view and the reply resolver's actual execution selection.

### Why this is not yet a final route root cause

Before assigning a production fix, capture the exact live facts that decide the remaining branches:

- resolved configured default provider/model for agent `main`;
- `liveModelSwitchPending`;
- `modelOverrideSource`;
- parent/model-parent session keys;
- parent-session provider/model override fields;
- fallback/auto-fallback provenance fields;
- any one-turn/directive override state relevant to the preserved session.

Do not infer those facts from the UI label.

### Route-discrepancy classification

`SESSION_ROUTE_STATE_DISCONTINUITY_NARROWED_NEEDS_READ_ONLY_LIVE_FACTS`

CogentNexus must not solve this by becoming a provider router or silently forcing Ollama.

## Successor direction

No further semantic request is authorized until two things are complete:

1. repository characterization of a harness-safe, Dashboard-specific Ticket-first compatibility bridge;
2. read-only live characterization of the exact route-selection fields that caused the Ollama-to-OpenAI discrepancy.

The next task should not mutate provider/model/session state and should not send a model request.

## Reviewer

ChatGPT

Human final authority: Operator
