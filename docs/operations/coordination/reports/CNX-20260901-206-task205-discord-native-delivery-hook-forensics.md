# CNX-20260901-206 — Task 205 Discord Native Delivery / Hook Forensics

- **Task:** `CNX-20260901-206`
- **Parent:** `CNX-20260901-205`
- **Authority branch:** `agent/v0.9.3-full-stabilization`
- **Fresh authority SHA:** `f022f58b64d6069fd46b651b551785dc2bdb0893`
- **Evidence root:** `C:/Users/CDQ-P/AppData/Local/Temp/cnx206-discord-forensics-20260901T`
- **Primary classification:** `EVIDENCE_REPLY_DISPATCH_SETTLEMENT_FAILED`

## Executive result

Task 206 was read-only. It found a live, directly recorded `reply_dispatch` observer shape in the exact Task-205 time window with:

```text
hasEventRunId=false
hasContextRunId=false
hasDispatcher=true
hasAppendBeforeDeliver=false
```

The installed CogentNexus delivery hook then recorded:

```text
handler-skip: missing-run-correlation
```

The Task-205 session subsequently completed a direct model call whose assistant result was `NO_REPLY`; its trajectory recorded `didSendViaMessagingTool=false` and no messaging-tool target. OpenClaw then recorded:

```text
visible channel turn dispatched with no queued reply payloads:
channel=discord messageId=unknown
sessionKey=agent:main:discord:channel:1531199905673252946
```

The Ticket reached `response_ready`, but no delivery confirmation occurred. At the direct-delivery deadline it entered `direct_redelivery_timeout`, with a pending redelivery record and no attempt made by this task.

This proves a reply-dispatch settlement/correlation boundary failure. It does **not** prove whether a Discord REST/native send was attempted and rejected, because no native Discord message ID, success receipt, failure response, or outbound send record for this run was retained.

## Immutable authorities

```text
published v0.9.3 target: 26ce64a624255278a3a0266ad38746e0e6ed2e31
frozen repaired candidate: 9f4eaa429b2540540e7d6f6c2af99067960e45fb
expected installed fingerprint: f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
channel ID: 1531199905673252946
owner session: agent:main:discord:channel:1531199905673252946
```

Task-205 correlation identity:

```text
nonce: CNX205-20260831T190442Z-8cdbed
Ticket: CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6
request_key: 09c9121cdac5dec9cb1fdea1a37aeafdacb098ce2e89f26a1b2a2f103fd5ed9f
run_id: b79dbb65-15eb-4b3e-8ffb-4084125e6cb5
call_id: b79dbb65-15eb-4b3e-8ffb-4084125e6cb5:model:1
```

## Time window and retained files

The required log window was inspected as UTC:

```text
2026-08-31T19:05:00Z through 2026-08-31T19:09:00Z
```

The OpenClaw log records the same period in local `+07:00` representation. The relevant log lines are at `2026-08-31T19:05:14.549Z` through `2026-08-31T19:06:52.399Z` as rendered by the runtime's local clock representation.

Before extraction, retained file identity was captured:

| File | Bytes | SHA-256 |
|---|---:|---|
| `C:/Users/CDQ-P/AppData/Local/Temp/openclaw/openclaw-2026-09-01.log` | 417378 | `94fcc4ac340bf3cf94353f159ba7752cb2691a52a7bc50acaa06247bde7c6032` |
| `C:/Users/CDQ-P/.openclaw/agents/main/sessions/119ef92d-271f-4d6f-ada6-ae7504bb35b3.jsonl` | 2232 | `0246514b6c8316e8de251dbc0b6ab369e9f209d000d0a2e784fb6a19174f06dc` |
| `C:/Users/CDQ-P/.openclaw/agents/main/sessions/119ef92d-271f-4d6f-ada6-ae7504bb35b3.trajectory.jsonl` | 161416 | `3affe85c846d6da9a468665229b25e638a196f83fcf319c102371e3c4c9973d6` |
| `C:/Users/CDQ-P/.openclaw/extensions/cogentnexus-openclaw/dist/v091-dashboard-verified-delivery.js` | 34762 | `7bc817ed75598ce721dd85bbc2b92818d3cd5c30aee9f438bfd52b56fcf97be0` |

The exact Task-205 database evidence was also retained under the Task-205 evidence root, including `discord-post-send.json`, `discord-correlation-final.json`, `settlement-final-series.json`, and `final-health.json`.

## Phase A — runtime continuity

Fresh read-only continuity capture at `2026-08-31T22:35:29.895960Z` showed:

```text
Host: managed
startup adapter: installed=true, State=Ready, Enabled=true, LastTaskResult=0
delivery verdict: READY
recovery verdict: READY
SQLite integrity: ok
lifecycle residue: []
```

The durable counts at that point were:

```text
tickets: 11
ticket_events: 85
cnx_direct_model_call: 11
cnx_direct_recovery: 1
cnx_assistant_delivery: 7
ticket_outbox: 0
cnx_sessions: 19
```

The direct-recovery count reflects the later Task-205 deadline redelivery record; this task did not create it.

## Phase B — exact log findings

The exact OpenClaw log window contains the following relevant records.

### Hook registration

At startup the installed dashboard delivery hook logged:

```text
CogentNexus-OpenClaw delivery-observe {
  "event":"hook-registered",
  "registrationCount":2,
  "hasReplyDispatch":true,
  "hasReplyPayloadSending":true
}
```

### Reply-dispatch entry and skip

At `2026-08-31T19:05:14.549Z`:

```text
CogentNexus-OpenClaw delivery-observe {
  "event":"handler-entry",
  "hasEventRunId":false,
  "hasContextRunId":false,
  "hasDispatcher":true,
  "hasAppendBeforeDeliver":false,
  "correlation":"29c3198f66a0"
}
```

At `2026-08-31T19:05:14.552Z`:

```text
CogentNexus-OpenClaw delivery-observe {
  "event":"handler-skip",
  "reason":"missing-run-correlation"
}
```

The event is from the installed `v091-dashboard-verified-delivery.js` `reply_dispatch` handler. The handler computes a run only from `event.runId` or `ctx.runId`; it returns before installing a delivery callback when neither is present. Its second gate also requires `ctx.dispatcher.appendBeforeDeliver`.

The record has no run ID and occurs approximately 0.85 seconds before the Task-205 session start. Therefore it is strong evidence of the live reply-dispatch event shape and the skip mechanism, but the log's correlation digest alone cannot bind that particular handler invocation to the Task-205 run. The later same-session no-queued-payload record and durable timeout bind the delivery failure boundary to Task 205, while the exact handler invocation is retained as the live mechanism evidence.

### Final channel turn

At `2026-08-31T19:06:52.399Z`:

```text
visible channel turn dispatched with no queued reply payloads:
channel=discord messageId=unknown
sessionKey=agent:main:discord:channel:1531199905673252946
```

No `messageId` was recorded. No `message_sent` success/failure line for the Task-205 run was found in the retained window. No Discord outbound REST result or native receipt was retained for the run.

The Discord application startup warning about the maximum application-command count is outside the Task-205 send boundary and is explicitly a slash-command deployment warning, not a message-send result. It is not used as the failure classification.

## Phase C — transcript and trajectory

The exact session file is:

```text
C:/Users/CDQ-P/.openclaw/agents/main/sessions/119ef92d-271f-4d6f-ada6-ae7504bb35b3.jsonl
```

It contains the owner message:

```text
@Ce ตอบกลับข้อความนี้เพียงว่า CNX205-20260831T190442Z-8cdbed
```

and the assistant result:

```text
NO_REPLY
```

The trajectory for the same run records:

```text
session.started
prompt.submitted
model.completed
trace.artifacts
session.ended
```

The `model.completed` and `trace.artifacts` data show:

```text
runId: b79dbb65-15eb-4b3e-8ffb-4084125e6cb5
model: qwen3.5:9b
provider: ollama
final status: success
assistantTexts: ["NO_REPLY"]
didSendViaMessagingTool: false
messagingToolSentTargets: []
```

This proves the model/session layer completed without a messaging-tool send. It does not by itself distinguish the final native channel dispatcher failure from a missing queued payload upstream; that distinction is supplied by the OpenClaw channel log and hook-shape evidence.

## Phase D — durable timeline and deadline

Task-205's durable event sequence was:

```text
accepted                    2026-08-31T19:05:15.427Z
routed                      2026-08-31T19:05:15.431Z
direct_model_call_started  2026-08-31T19:05:15.546Z
direct_model_call_ended    2026-08-31T19:06:52.235Z outcome=completed
a response_ready            2026-08-31T19:06:52.333Z
```

The Ticket initially remained accepted with no delivery confirmation. After the configured direct-delivery deadline, the final read-only adjudication at `2026-08-31T22:35:46.688514Z` showed:

```text
Ticket status: accepted
failure_class: interrupted
failure_message: Direct response delivery was not confirmed before deadline
response_ready_at: null in the post-timeout Ticket row
 delivery_confirmed_at: null
delivery_last_error: Direct response delivery was not confirmed before deadline
```

The event added by the runtime was:

```text
direct_redelivery_timeout 2026-08-31T19:08:52.400Z
```

The matching direct-recovery row was:

```text
ticket_id: CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6
mode: redeliver
state: pending
attempt_count: 0
active_run_id: null
last_error: Direct response delivery was not confirmed before deadline
```

The `response_ready_at=null` in the later Ticket read-back is a runtime timeout-state rewrite; the earlier event and model-call evidence still prove the response-ready transition occurred before timeout.

No delivery row matched the Task-205 Ticket/run. No recovery attempt was made by Hermes; the pending record was observed only.

## Phase E — source-to-live mapping

The installed source at `dist/v091-dashboard-verified-delivery.js` contains this `reply_dispatch` behavior:

```js
const hasEventRunId = typeof event?.runId === "string";
const hasContextRunId = typeof ctx?.runId === "string";
const hasDispatcher = Boolean(ctx?.dispatcher);
const hasAppendBeforeDeliver = typeof ctx?.dispatcher?.appendBeforeDeliver === "function";
const runId = hasEventRunId ? event.runId : hasContextRunId ? ctx.runId : undefined;
if (!runId) return;
if (!hasDispatcher) return;
if (!hasAppendBeforeDeliver) {
  // diagnostic fallback may arm only if a dashboard Ticket is already found
  return;
}
```

The retained live log exactly matches the first correlation gate: no event/context run ID, then `missing-run-correlation`. The task-205 run itself produced no queued final payload at channel dispatch time. The evidence therefore supports a reply-dispatch settlement failure at the event/callback boundary, without asserting a native API outcome that was not retained.

## Primary classification

```text
EVIDENCE_REPLY_DISPATCH_SETTLEMENT_FAILED
```

Rationale:

1. A live `reply_dispatch` observer entry retained the exact missing-correlation and missing-callback shape.
2. The installed handler's source maps that shape to an early return and no callback registration.
3. The same Task-205 owner session ended with `NO_REPLY`, `didSendViaMessagingTool=false`, and no messaging target.
4. OpenClaw recorded no queued reply payloads for the Discord channel turn and `messageId=unknown`.
5. The Ticket reached model completion/response readiness but never reached delivery confirmation and later timed out into pending redelivery.
6. No native send success/failure receipt was retained, so `EVIDENCE_NATIVE_SEND_FAILED` and `EVIDENCE_NATIVE_SEND_SUCCEEDED_RECEIPT_UNCORRELATED` are not claimed.

This is a boundary classification, not a product root-cause claim beyond the observed reply-dispatch settlement path.

## Required negatives

```text
additional Discord Send: 0
probe Send: 0
retry/regenerate: 0
second message/second room: 0
API/bot/injected traffic: 0
lifecycle command: 0
process kill: 0
provider/model/config/SQLite mutation: 0
product/source/test/workflow edit: 0
Release/tag/asset mutation: 0
force push: 0
```

No state was repaired. The later `direct_redelivery_timeout` and pending recovery row were runtime consequences observed by read-only inspection, not actions performed by Task 206.

## Smallest next RED recommendation

Do not implement the fix in Task 206. The smallest deterministic RED for a follow-up repository task should exercise the live event shape and the safe invariant:

### RED-1 — reply dispatch with complete correlation and callback

Simulate one `reply_dispatch` event for a known direct Ticket with:

```text
event.runId = exact Ticket run ID
ctx.runId = absent or equal, but not conflicting
ctx.sessionKey = exact owner session key
ctx.dispatcher.appendBeforeDeliver = callable
ctx.dispatcher.waitForIdle = callable
ctx.dispatcher.getFailedCounts().final = 0
ctx.dispatcher.getCancelledCounts().final = 0
one final payload with non-empty text and no media
```

Expected pre-fix state:

```text
Ticket response-ready/accepted
Ticket delivery_confirmed_at is null
no delivery-confirmed event
```

Desired invariant:

```text
exactly one callback is registered;
exactly one final payload is observed;
waitForIdle completes;
failed/cancelled final counts are zero;
exactly one delivery_confirmed transition settles the same run;
Ticket reaches terminal completed state;
no duplicate delivery or recovery row is created.
```

### RED-2 — missing-correlation fail-closed case

Simulate the observed shape:

```text
event.runId absent
ctx.runId absent
ctx.dispatcher present
ctx.dispatcher.appendBeforeDeliver absent
```

Expected safe behavior:

```text
no Ticket is settled;
no unrelated run is selected;
no delivery-confirmed event is emitted;
no native payload is synthesized;
diagnostic record identifies missing correlation and missing callback.
```

### RED-3 — ambiguity fence

Simulate two active runs sharing the same owner session key. A `message_sent` event with no `runId` must not select the latest/any run unless the implementation has a deterministic, unique, time-bounded correlation proof. If ambiguity exists, fail closed and emit an explicit diagnostic. Never settle the wrong Ticket.

### Instrumentation requirement before production fix

A follow-up diagnostic should record, without sensitive payload bodies:

```text
hook name
exact event/context runId presence
sessionKey presence/hash
channel/target ID
message ID if native send returns one
reply_dispatch callback registration
reply_payload_sending entry
message_sent success/failure
waitForIdle result and failed/cancelled final counts
Ticket/run ID selected for settlement
```

The instrumentation must preserve credentials and full private content redaction. It should be added only under a new authorized source/test task after review of this report.

## Final health snapshot

Fresh final continuity remained:

```text
Host: managed
startup adapter: enabled/Ready
Gateway: healthy
Ollama: healthy/ready
delivery check: READY
provider recovery check: READY
SQLite integrity: ok
lifecycle residue: []
```

The Task-205-specific pending redelivery row is recorded separately above. The generic provider-recovery health verdict does not erase the Ticket-specific pending redelivery state.

## Mutation ledger

```text
Discord Sends by Hermes: 0
Human Sends in Task 206: 0
Runtime lifecycle mutations: 0
Process termination: 0
Provider/model changes: 0
Config/SQLite/session mutations: 0
Source/test/workflow changes: 0
Release/tag/assets changes: 0
Force push: 0
```

## Final disposition

```text
EVIDENCE_REPLY_DISPATCH_SETTLEMENT_FAILED
```

The live evidence identifies the reply-dispatch correlation/callback boundary as the primary failure mechanism. Native Discord API success or failure remains unproven because no native receipt was retained. The smallest next action is a new reviewed repository RED and instrumentation task; no fix was implemented here.
