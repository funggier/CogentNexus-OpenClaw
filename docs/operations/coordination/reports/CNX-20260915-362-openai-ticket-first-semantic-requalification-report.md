# CNX-20260915-362 — OpenAI Ticket-first semantic requalification report

## Classification

`BLOCKED`

The required fresh live semantic requalification was not started. The pre-test runtime identity gate did not match the accepted CNX-361 candidate state, so no Dashboard session was opened and no Dashboard request was sent.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Remote HEAD at preflight: `830f6b9aa7e34bf88535f6a2d7152d6ba9752faa`
- Source checkout: `C:\Users\CDQ-P\cnx362-checkout`
- Working tree: clean before report creation

## CNX-361 accepted candidate identity required by this task

- Candidate source identity: CNX-361 repaired candidate
- Required installed payload fingerprint: `3a889d6ef3bd0ba0f957cac00ff86868c315527bde0d3d87607eb91daca089e5`
- Required controller state: `cnxMode=active`, `desiredGateway=running`, `generation=103`

## Fresh read-only runtime evidence

Captured before any Dashboard action:

```text
plugin id       = cogentnexus-openclaw
plugin version  = 0.9.5
installed root  = C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw
entry module    = C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js
enabled         = true
status          = loaded
hookCount       = 0
configSchema    = false
entry SHA-256   = da8e810e88547ef866e2279fde86195f02557a9ca0a35a8771a0e646a1f6a7ef
```

The live controller read-only contents were:

```json
{
  "schemaVersion": 1,
  "mode": "passthrough",
  "desiredGateway": "running",
  "desiredProvider": "unchanged",
  "generation": 1,
  "updatedAt": "2026-08-29T01:36:31.541994+00:00"
}
```

This does not match the required accepted CNX-361 controller identity. In particular, the expected canonical `cnxMode=active` and generation `103` were not present. The installed payload fingerprint and Gateway health were not treated as sufficient to override this failed identity gate.

## Source/test implementation inspected

The exact source implementation was inspected read-only at `plugins/cogentnexus-openclaw/src/index.ts`:

- `AdmissionTraceState` defines the expected states:
  `admission.trace.started`, `admission.trace.input`, `admission.trace.eligible`, `admission.trace.ticket-decision`, `admission.trace.ticket-persisted`, `admission.trace.blocked`, and `admission.trace.completed`.
- `admissionTraceFields` preserves correlation fields and adds an ISO timestamp.
- `before_agent_run` creates a `traceId`, carries `runId`, `sessionKey`, and optional `sessionId`, emits `started`, `input`, and `eligible`, classifies the request, emits `ticket-decision`, persists a Ticket when Ticket-first intake is eligible, emits `ticket-persisted`, and emits terminal blocked/completed events.
- Ticket persistence is performed through `TicketStore.accept({ runId, ownerSessionKey, prompt, maxAttempts })`, followed by routing.
- The implementation was not changed.

## Dashboard and semantic evidence

- New Dashboard session: **not opened**
- Operator UI action: **not requested**
- Dashboard request count: `0`
- Request text sent: **none**
- Session key / session ID / run ID / trajectory trace ID: **N/A — no fresh run**
- Visible response: **N/A**
- Admission trace events: **N/A — no semantic request was admitted**
- Ticket, Ticket Events, Run, Direct Model Call / Inference Attempt, Result, Assistant Delivery, Outbox: **N/A for this task run**

The `hookCount=0` and `configSchema=false` observations are recorded without interpreting them as success or failure. No hook-registration repair was attempted.

## First divergence

The first divergence is the **pre-test runtime identity gate**: the live controller does not match the accepted CNX-361 runtime identity. Because that gate failed, this task cannot distinguish hook activation, admission trace, Ticket persistence, provider routing, or downstream durable-lineage behavior.

## Hard-fence compliance

- `main` and tag `v0.9.5`: not modified
- force-push/history rewrite: none
- reinstall: none
- provider routing/auth/admission semantics: unchanged
- Dashboard requests: zero
- old Dashboard sessions/results: not reused
- source changes: none
- hook registration patch: none

## Success classification

`BLOCKED` — repaired candidate identity cannot be proven active in the required state. No CURRENT_RED product conclusion is made, and no PASS claim is made.

## Successor repair task

No product repair task is authorized or required from this evidence. A separate runtime-identity restoration/reconciliation task is required before semantic requalification can resume; it must establish the accepted CNX-361 candidate identity without silently reinstalling in this task.

## Publication

This report is the only intended repository change for CNX-362. Final commit and remote report verification are recorded in the closeout response after push.
