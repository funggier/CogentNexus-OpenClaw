# CNX-20260914-333 — Dashboard Web Session Lifecycle Architecture / Implementation Trace

## Executive conclusion

**DASHBOARD_INTEGRATION_GAP**

The repository and installed plugin contain a Ticket-first direct Dashboard lifecycle, including durable Ticket, result, delivery, recovery, idempotency, and ownership primitives. The CNX-332 Dashboard request did not appear in that durable lifecycle database: its OpenClaw agent run was present only in the host OpenClaw audit ledger, while no matching Ticket, direct model-call, inference-attempt, or assistant-delivery record existed.

This is not evidence that the TicketStore implementation is absent or that the v0.9.5 model/timeout path failed. It is evidence that the specific Dashboard execution did not cross the installed CogentNexus durable-admission boundary, or that the boundary's hook was not active for that Dashboard path. The exact runtime hook-registration/dispatch failure still needs a separately authorized diagnostic task; this task performed no mutation.

## Investigation scope and fences

- Repository: `funggier/CogentNexus-OpenClaw`
- Repository checkout inspected: `c70552801ddbb9dc0a49c9cfc64368b9f4820f07`
- Published release tag verified locally: `v0.9.5 -> 50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`
- Installed plugin inspected read-only: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\`
- Installed runtime configuration inspected read-only: `C:\Users\CDQ-P\.openclaw\openclaw.json`
- Ticket database inspected read-only: `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\runtime\cogentnexus-openclaw.sqlite3`
- No Dashboard send, semantic test, retry, fallback, recovery, restart, reset, configuration change, database write, release mutation, tag movement, merge, or force-push was performed.

## Actual durable stores

There are two different SQLite authorities and they must not be conflated:

1. `C:\Users\CDQ-P\.openclaw\state\openclaw.sqlite` — OpenClaw host state/audit database. It contains the CNX-332 `agent.run.started` and `agent.run.finished` audit rows, but no CogentNexus `tickets` table.
2. `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\runtime\cogentnexus-openclaw.sqlite3` — CogentNexus Ticket/Delivery database. It contains `tickets`, `ticket_events`, `ticket_outbox`, `cnx_sessions`, `cnx_direct_model_call`, `cnx_assistant_delivery`, `cnx_direct_recovery`, and related tables.

The CNX-332 identifiers were absent from the second database:

- Dashboard session key: `agent:main:dashboard:2fefcfd2-6819-4c21-a190-842ebc133f57`
- Session ID: `59e80ea8-6151-4fc1-9de4-4d8c46ebcd9a`
- Run ID: `46a1470c-47f9-41dc-9f41-bade8742a24c`

The CogentNexus database did contain prior Dashboard Tickets and prior durable direct results/deliveries, proving that the schema and persistence path are implemented and have been used by other executions.

## Source trace

| Boundary | Source | Function / hook | Durable artifact | Identifier |
|---|---|---|---|---|
| Dashboard ingress | OpenClaw Control UI / WebChat | OpenClaw Dashboard chat send; host emits agent run lifecycle | Host `audit_events` only at this boundary | Dashboard session key; OpenClaw session ID; OpenClaw run ID |
| Session admission | `plugins/cogentnexus-openclaw/src/index.ts` lines 728–760 | `before_agent_run` | In-memory `runWorkspaces`, `runSessions`, `ticketedRuns`; then Ticket DB when enabled | `ctx.sessionKey`, `ctx.runId` |
| Owner eligibility | `src/index.ts` and admission helpers | `durableAdmissionEligible({sessionKey, senderIsOwner})`; `ticketIntakeEligible(prompt)` | No row when excluded | Session shape and owner bit; internal-marker exclusions |
| Ticket creation | `src/index.ts` lines 761–775 | `new TicketStore(databasePath).accept(...)` | `tickets`; `ticket_events(event_type='accepted')` | `ticket_id`, `request_key=sha256(sessionKey + NUL + runId)`, `run_id`, `owner_session_key` |
| Ticket routing | `src/index.ts` lines 776–783 | `store.route(ticketId, decision.lane === 'durable')` | `tickets.workflow_eligible`; `ticket_events(event_type='routed')` | `ticket_id`, `workflowEligible` |
| Direct model call | Installed `dist/index.js` direct-run lifecycle and TicketStore integration | OpenClaw agent execution; plugin retains `runId` in `runSessions`/`ticketedRuns` | Installed DB `cnx_direct_model_call` when direct-call lifecycle is entered | `ticket_id`, `run_id`, `call_id`, provider, model, start/end/outcome |
| Response ready | `src/ticket-store.ts` lines 196–216, 229–239 | `finalizeDirectRun({runId,...})` then `confirmDirectDelivery` | `tickets.result_json`, `tickets.response_ready_at`; `ticket_events('response_ready')` | `run_id`, `ticket_id`, result payload |
| Durable result | `src/ticket-store.ts` lines 77–80 and 196–216 | `finalizeDirectRun` | `tickets.result_json`, `response_ready_at` | `ticket_id`, `run_id`; result contains direct/expectation metadata |
| Delivery target binding | `src/index.ts` lines 732–741; `src/delivery-continuity.ts` lines 136–155 | `parseDeliveryMarker`, `bindDeliveryRun` | `ticket_outbox.delivery_run_id` for Ticket target, or workflow `completion.json` | `outbox_id`/workflow target, `delivery_run_id`, owner session |
| Dashboard final delivery observation | `src/index.ts` lines 814–846 | `reply_dispatch` `appendBeforeDeliver`; fallback `message_sent` | Ticket delivery settlement; in-memory delivery target/run maps | `run_id`, dispatcher receipt, session key |
| Delivery confirmation | `src/index.ts` lines 714–725; `src/ticket-store.ts` lines 229–240 | `settleRunDelivery` -> `store.confirmDirectDelivery` | `tickets.delivery_confirmed_at`; `ticket_events('delivery_confirmed')`, `ticket_events('completed')` | `ticket_id`, `run_id`, confirmation timestamp |
| Ticket terminal completion | `src/ticket-store.ts` lines 196–216 / 229–240 | Direct success or confirmed delivery | `tickets.status='completed'` | `ticket_id`, `run_id` |
| Ticket outbox | `src/ticket-store.ts` lines 95–109, 526–565, 600–605 | `enqueueTerminal`, `pendingOutbox`, `markOutboxDelivered` | `ticket_outbox` | `outbox_id`, `ticket_id`, `delivery_run_id`; direct Dashboard success may have no outbox row when delivery is settled through direct fields |
| Direct recovery | `src/index.ts` lines 930–962; `src/ticket-store.ts` lines 243–284 | `recoverUndeliveredDirect`, `recoverExpired`; `failDirectDelivery` | `cnx_direct_recovery` in installed runtime lineage plus Ticket status/events | `ticket_id`, original `run_id`, recovery run/attempt, owner generation |
| Retry/ownership/idempotency | `src/ticket-store.ts` lines 385–435, 471–510; `src/delivery-continuity.ts` lines 113–186 | Unique request key; leases; generation; owner/session checks; idempotent delivery binding | `tickets.request_key`, lease columns, `ticket_events`, delivery idempotency fields | `request_key`, `lease_generation`, worker/owner, delivery run ID |

## Durable schema facts

The repository `TicketStore` schema defines:

- `tickets.ticket_id` primary key;
- unique `tickets.request_key` for duplicate admission suppression;
- `tickets.run_id` and `owner_session_key` for run/session correlation;
- `result_json`, `response_ready_at`, and `delivery_confirmed_at`;
- `ticket_events` for accepted/routed/response-ready/delivery-confirmed/completed and failure transitions;
- unique `ticket_outbox.ticket_id` with pending/delivered state;
- delivery attempt, scheduled time, delivery run, and delivered timestamp;
- lease worker, token, expiration, generation, attempt count, and failure fields.

The installed runtime additionally contains the normalized direct-lifecycle tables:

- `cnx_sessions(session_key, session_id, state, generation, ...)`;
- `cnx_direct_model_call(ticket_id, run_id, call_id, state, provider, model, started_at, ended_at, outcome, duration_ms, recovery_attempt_count, ...)`;
- `cnx_assistant_delivery(delivery_id, ticket_id, owner_session_key, owner_generation, idempotency_key, status, delivered_at, run_id, surface, delivery_state, evidence_type, ...)`;
- `cnx_direct_recovery(ticket_id, mode, state, attempt_count, active_run_id, owner_generation, ...)`.

`cnx_inference_attempt` exists in the installed schema but had zero rows at inspection time. It is not the only model-call authority; `cnx_direct_model_call` is populated by prior direct executions.

## State-machine diagram

### Implemented Ticket-first direct path

```text
Firefox Dashboard/WebChat send
  -> OpenClaw agent run admission (`before_agent_run`)
  -> owner/session eligibility and internal-marker fence
  -> TicketStore.accept()
  -> tickets.status=accepted + ticket_events.accepted
  -> TicketStore.route()
  -> tickets.workflow_eligible=false + ticket_events.routed
  -> OpenClaw model execution
  -> agent_end finalization
  -> TicketStore.finalizeDirectRun()
  -> tickets.result_json + response_ready_at + ticket_events.response_ready
  -> Dashboard reply_dispatch/message_sent settlement
  -> TicketStore.confirmDirectDelivery()
  -> tickets.delivery_confirmed_at + ticket_events.delivery_confirmed
  -> tickets.status=completed + ticket_events.completed
  -> optional ticket_outbox terminal delivery settlement
  -> idle
```

### Workflow-eligible path

```text
Firefox Dashboard/WebChat send
  -> before_agent_run
  -> TicketStore.accept()
  -> TicketStore.route(workflowEligible=true)
  -> TicketDispatcher.claim()
  -> lease generation/worker ownership
  -> compileDurableIntake()
  -> startBoundWorkflow()
  -> tickets.workflow_id + manifest_path
  -> workflow completion.json pending
  -> owner-session delivery marker
  -> bindDeliveryRun()/settleDeliveryTarget()
  -> completion.json delivered
  -> terminal Ticket/outbox settlement
```

### Recovery path (not executed here)

```text
accepted/running or response_ready without confirmed delivery
  -> recovery scanner
  -> lease expiry or direct-delivery timeout classification
  -> waiting / durable recovery state
  -> bounded retry or same-generation recovery
  -> owner/generation/idempotency checks
  -> durable completion or terminal failure
```

## Installed configuration trace

Read-only inspection of `C:\Users\CDQ-P\.openclaw\openclaw.json` found:

- CogentNexus plugin enabled;
- `ticketFirst: true`;
- `preInferenceAdmission: true`;
- `autoWorkflowCompletion: true`;
- `enforcedMode: true`;
- `autoResume: true`;
- workspace directory set to `C:\Users\CDQ-P\.openclaw\workspace`;
- dispatch/recovery/outbox poll values configured;
- `providerMode: "passthrough"`;
- primary model `ollama/qwen3.8:27b`;
- Ollama provider API `ollama` and timeout `2700`;
- agent timeout `2700`.

In the installed `dist/index.js`, the `before_agent_run` hook performs a special `providerMode === 'passthrough'` check only for requests classified as durable workflows. Ordinary eligible owner messages still enter the `ticketFirst` branch and call `TicketStore.accept` when that hook executes.

Therefore `providerMode=passthrough` alone does not explain absence of a Ticket for an ordinary CNX-332 prompt. The evidence points more narrowly to the Dashboard run not invoking the active installed hook for that path, the event context failing the owner/session eligibility test, or the runtime writing/using a different plugin database path. The exact alternative is not resolvable from repository source alone and must not be guessed.

## CNX-332 mapping

Observed host audit:

| Item | CNX-332 value | Mapping result |
|---|---|---|
| Dashboard session key | `agent:main:dashboard:2fefcfd2-6819-4c21-a190-842ebc133f57` | Present in OpenClaw host audit; absent from CogentNexus `cnx_sessions` and `tickets` |
| CogentNexus/OpenClaw session ID | `59e80ea8-6151-4fc1-9de4-4d8c46ebcd9a` | Present in host `audit_events.session_id`; no durable CogentNexus parent found |
| OpenClaw run ID | `46a1470c-47f9-41dc-9f41-bade8742a24c` | Present in host `audit_events.run_id`; absent from `tickets.run_id`, `cnx_direct_model_call.run_id`, and delivery records |
| Ticket ID | None observed | Cannot map |
| model-call ID | None observed | Cannot map |
| delivery ID | None observed | Cannot map |
| generation/owner | None for this run | Cannot prove from CogentNexus lifecycle |

Host audit contained exactly two matching rows: one `agent.run.started` and one `agent.run.finished` with status `succeeded`. That proves an OpenClaw agent run, not a CogentNexus Ticket lifecycle.

## Boundary-by-boundary answers

### Is Ticket creation required?

Yes for an eligible owner message when installed `ticketFirst=true` and the active `before_agent_run` hook is reached. The implementation calls `accept` before conversational inference. Internal delivery/continuation markers are intentionally excluded. Durable-workflow classification has a separate admission branch; passthrough mode blocks that workflow branch rather than creating a workflow Ticket.

### Is durable result required?

For a direct Ticket that expects visible delivery, yes. `finalizeDirectRun` writes `result_json` and `response_ready_at`, then leaves the Ticket accepted until delivery confirmation. The result is not equivalent to the transient UI response.

### Is durable delivery required?

For `expectsDelivery=true`, yes. Direct delivery is represented by `delivery_confirmed_at` and terminal Ticket events; the implementation also supports `cnx_assistant_delivery` in the installed normalized runtime lineage. A direct success with `expectsDelivery=false` explicitly marks delivery confirmed without an external delivery row, but that is not the expected visible Dashboard path.

### Is delivery confirmation required?

Yes for a visible Dashboard direct result. The code separates model completion from `confirmDirectDelivery`; completion without confirmation remains accepted/response-ready and is eligible for direct-delivery recovery.

### Is `outbox=0` sufficient?

No. Direct Dashboard success can legitimately settle without a `ticket_outbox` row. The authoritative proof is the correlated Ticket/result/delivery state. `outbox=0` with no matching Ticket/delivery record is ambiguous and was correctly insufficient in CNX-332.

### Where should first-token timing come from?

The inspected durable schemas persist model start/end and duration (`cnx_direct_model_call.started_at`, `ended_at`, `duration_ms`) but no first-token column or first-visible-token event was found. The repository's Dashboard delivery hooks observe final dispatch and `message_sent`, not first token. Exact first-token timing therefore requires an authoritative streaming event/log collector or a separately authorized instrumentation change; it cannot be reconstructed from the CNX-332 two audit timestamps.

### Can duplicate/recovery exclusion be proven from current telemetry?

For a Ticketed run, the design provides the mechanisms: unique request key, one Ticket, lease generation/owner checks, delivery idempotency, and recovery state. For CNX-332 specifically, the required durable Ticket was absent, so those exclusions cannot be proven for that request. The host audit's one start/finish pair rules out only an additional host agent-run pair in that ledger; it does not prove no hidden provider/model attempt or bypass execution.

### Was CNX-332 blocked because the system failed or because evidence collection was incomplete?

Both layers must be distinguished. The UI/model execution visibly succeeded and the host agent run completed. The durable lifecycle evidence was absent because the Dashboard execution did not appear in the CogentNexus durable path. Thus CNX-332 was not merely a reporting omission over an existing correlated Ticket: the expected Ticket/result/delivery records were not present for that run. The primary architecture classification is `DASHBOARD_INTEGRATION_GAP`, pending a focused runtime hook/database-path diagnosis.

## Why this is not currently classified as a generic durable-state defect

`TicketStore`, schema migrations, direct result finalization, delivery confirmation, outbox handling, and recovery/idempotency code are present. The same installed database contains prior Dashboard Ticket and durable delivery rows. The observed defect is at the boundary between a real Dashboard agent run and the active CogentNexus admission/persistence path. No source patch is authorized or justified by this trace alone.

## Next decision

The next task should be a **targeted read-only runtime hook/database-path diagnostic**, not another semantic send and not a source change. It should establish, without mutating state:

1. which plugin artifact is loaded by the active Gateway;
2. whether the active Dashboard run reaches `before_agent_run`;
3. the exact `ctx.sessionKey`, `ctx.runId`, `ctx.workspaceDir`, owner decision, and database path seen by that hook;
4. whether the hook returns `pass` or `block` and why;
5. whether the installed runtime database path is the same path inspected here;
6. whether the normalized `cnx_direct_model_call`/`cnx_assistant_delivery` writers are active for Dashboard runs.

No next semantic acceptance should be attempted until that boundary is explained.
