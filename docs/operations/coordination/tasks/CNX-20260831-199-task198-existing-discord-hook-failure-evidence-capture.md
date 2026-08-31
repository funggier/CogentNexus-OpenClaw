# CNX-20260831-199 — Task 198 Existing Discord Hook-Failure Evidence Capture

Status: `READY_FOR_HERMES`
Date: 2026-08-31 ICT
Parent: `CNX-20260831-198`
Executor: Hermes
Coordinator / final reviewer: ChatGPT

## Purpose

Collect existing Windows/OpenClaw/SQLite evidence needed to identify the exact `before_agent_run` exception that blocked the older Discord session, without sending any new Discord message and without mutating runtime/product state.

This is a read-only diagnostic subtask. It exists because source tracing has already disproven two misleading interpretations from Task 196:

1. `missing-run-correlation` is emitted by the Dashboard verified-delivery observer when `reply_dispatch` has no run correlation; that observer simply returns and is not itself the `before_agent_run` blocker.
2. A successful non-Dashboard Direct Ticket can legitimately complete through native receipt-confirmed delivery (`message_sent` -> `confirmDirectDelivery`) without a `cnx_assistant_delivery` row. Therefore absence of that row for the successful Discord room is not sufficient evidence of a defect by itself.

The unresolved defect is the exact exception behind OpenClaw's fail-closed `before_agent_run hook failed; blocking request` for Session A.

## Sessions to correlate

### Session A — blocked

`agent:main:discord:channel:1531201432861282405`

Known log pattern:

- `handler-skip: missing-run-correlation`
- `before_agent_run hook failed; blocking request`
- `handler-skip: missing-append-before-deliver`

### Session B — completed and user-visible

`agent:main:discord:channel:1531199905673252946`

Known durable identities:

- Ticket: `CNXT-50d93e89-a04b-421d-bad2-b2c747f646da`
- Run: `65f3abad-9817-4c7a-aeb7-1feeafda5213`
- Model call: `65f3abad-9817-4c7a-aeb7-1feeafda5213:model:1`
- `response_ready_at`: `2026-08-31T14:56:33.668Z`
- `delivery_confirmed_at`: `2026-08-31T14:56:49.816Z`

## Hard fence

Do not:

- send any Discord message;
- retry/regenerate/inject any turn;
- restart Gateway/OpenClaw/Ollama/CogentNexus-OpenClaw;
- reset/uninstall/reinstall/install-over;
- edit config, SQLite, transcripts, logs, source, plugin files, or state;
- delete/rotate/compact a session;
- change provider/model;
- create synthetic evidence;
- force push.

All operations must be read-only except writing the coordination report/evidence copies under a temporary evidence directory and committing the report to GitHub.

## Evidence capture

### A. Establish live read-only baseline

Record:

- `openclaw --version`
- `cnxclaw status`
- Host mode / selected provider
- Gateway health
- Ollama health/readiness
- SQLite integrity check
- current installed plugin/facade provenance if available without mutation

Do not remediate any warning in this task.

### B. Locate the exact Session-A failure window

Search all retained OpenClaw log files and relevant CogentNexus diagnostic logs for:

- the exact Session A key;
- `before_agent_run hook failed`;
- `blocking request`;
- `missing-run-correlation`;
- `missing-append-before-deliver`;
- any nearby `CogentNexus-OpenClaw` error/warn lines;
- SQLite errors (`SQLITE_BUSY`, `SQLITE_LOCKED`, constraint/schema/open errors);
- hook timeout/error text;
- stack traces or registration/plugin identifiers if present.

For each matching failure occurrence, capture a bounded surrounding window large enough to preserve ordering and timestamps. Do not publish unrelated user message bodies or secrets; redact unrelated payload text while preserving structural fields, error names/messages, hook names, session/run IDs, timestamps, and correlation identifiers.

The key deliverable is the **exact exception/error string immediately associated with `before_agent_run hook failed`**, if retained.

### C. Session-A durable-state correlation

Query SQLite read-only for Session A and record:

- all Ticket rows owned by the session, ordered by creation;
- ticket IDs, run IDs, statuses, workflow eligibility, response/delivery timestamps, failure class/message;
- event types/timestamps for those Tickets;
- direct model-call rows;
- direct-recovery rows;
- assistant-delivery rows;
- pending/outbox rows;
- `cnx_sessions` state/generation for the session.

Determine whether each blocked user attempt:

- created no Ticket at all;
- created a Ticket under an actual OpenClaw run ID;
- created a Ticket under a synthetic/random run ID;
- created a Ticket and then failed in a later `before_agent_run` handler.

Do not infer from timestamps alone if the mapping is ambiguous; label ambiguity explicitly.

### D. Session-B native-delivery correlation

For the known successful Ticket/run, capture evidence around:

- `before_agent_run`;
- model call start/end;
- `agent_end`;
- `reply_dispatch`;
- `message_sent`;
- `response_ready`;
- `delivery_confirmed`;
- `completed`.

Determine whether logs support the expected native-channel path:

`Ticketed Direct -> agent_end/finalizeDirectRun -> native Discord send -> message_sent receipt/fallback -> confirmDirectDelivery -> completed`

Specifically record whether `reply_dispatch` lacked run correlation while `message_sent` carried or could recover session/run attribution.

### E. Compare Session A vs B

Produce a compact table comparing:

- session key;
- physical session/sessionId if available;
- `cnx_sessions` generation/state;
- before-agent runId presence if observable;
- Ticket created?;
- Ticket run ID;
- exact failing hook/error (A);
- model call started?;
- reply_dispatch runId/context-runId availability if logged;
- appendBeforeDeliver availability;
- message_sent correlation availability;
- terminal delivery evidence.

Do not state root cause unless the evidence proves it.

## Source-derived hypotheses to test against evidence

These are hypotheses, not conclusions:

1. Dashboard observer `missing-run-correlation` is benign telemetry on Discord and unrelated to Session-A admission failure.
2. Session-B lack of `cnx_assistant_delivery` is expected for native non-Dashboard Direct delivery.
3. Session-A failure came from a different fail-closed `before_agent_run` handler, likely an uncaught SQLite/runtime exception in Ticket admission, recovery-order, or context-guard processing.
4. If `before_agent_run` lacked `ctx.runId`, core Ticket admission can create a Ticket using a generated UUID; later lifecycle hooks use actual run IDs, creating an attribution seam. Prove or disprove this from Session-A rows/logs rather than assuming it occurred.

## Evidence directory

Use a new timestamped directory under:

`%LOCALAPPDATA%\Temp\cnx199-evidence-*`

Record file hashes for copied evidence where practical. Do not modify original logs/database.

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260831-199-task198-existing-discord-hook-failure-evidence-capture.md`

The report must include:

- exact evidence root;
- read-only baseline;
- exact Session-A exception/error text if recoverable;
- Session-A durable-state mapping;
- Session-B delivery-path mapping;
- A/B comparison table;
- hypotheses confirmed/rejected/unresolved;
- no-mutation attestation;
- final disposition.

Allowed dispositions:

- `PASS_ROOT_CAUSE_EVIDENCE_CAPTURED`
- `PARTIAL_EVIDENCE__EXACT_EXCEPTION_NOT_RETAINED`
- `BLOCKED_EVIDENCE_UNAVAILABLE`

Stop after publishing the report. Do not repair source and do not send a new Discord message in Task 199.
