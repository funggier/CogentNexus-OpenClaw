# CNX-20260915-357 — OpenAI Dashboard Ticket-First Live Requalification

Status: `READY_FOR_HERMES`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Parent: `CNX-356`
Execution mode: `READ_ONLY_LIVE_REQUALIFICATION`
Base release: `v0.9.5`

## Objective

Requalify the actual installed OpenClaw + CogentNexus v0.9.5 runtime for the original OpenAI Dashboard Ticket-first defect boundary.

The immediate goal is narrow and operational:

```text
Dashboard request using OpenAI
-> effective admission boundary
-> durable Ticket acceptance
-> durable Run/Call/inference evidence
-> OpenAI inference
-> canonical delivery settlement
```

Do not expand the task into current-upstream OpenClaw compatibility work. The installed runtime and the published v0.9.5 implementation are the target.

## Why this task exists

Historical CNX-344 demonstrated a response from OpenAI while no durable Ticket/Run/Call/inference/Result/Delivery lifecycle was observed. CNX-356 could not prove or disprove the effective Gateway process-local `before_agent_run` registration because the supported read-only Gateway surface did not expose that runtime registry state.

The v0.9.5 release documentation says the OpenAI provider path was required and live-tested successfully, but that statement does not by itself prove that the current Dashboard Ticket-first path is healthy for the exact defect boundary.

Therefore this task tests the live behavior directly rather than continuing to infer process-local hook state.

## Hard fences

- No production source modification.
- No OpenClaw source modification.
- No plugin reinstall, enable, disable, restart, stop, or start.
- No provider/model/auth/routing configuration mutation.
- No credential extraction, display, persistence, or rotation.
- No Ticket/SQLite/session/transcript/delivery mutation outside the normal result of the one semantic test request.
- No CNX-344 replay/resend.
- No repeated semantic requests.
- Exactly one controlled OpenAI Dashboard semantic request.
- Do not probe undocumented mutating Gateway methods.
- Do not mutate `main`, the immutable `v0.9.5` tag, or published release history.
- No force-push/history rewrite.

## Required execution

1. Verify the task branch is descended from the current `main` tip recorded by GitHub.
2. Verify installed OpenClaw/Gateway identity using already-supported non-secret status surfaces.
3. Verify CogentNexus v0.9.5 is the loaded/installed plugin identity using existing supported diagnostics only.
4. Record the minimum pre-test state needed to distinguish new durable rows/events from prior history.
5. In the normal Dashboard, select the OpenAI provider/model already configured and issue exactly one controlled semantic request whose expected content is unambiguous. Use a fresh session/run for this task; do not reuse CNX-344 identifiers.
6. Capture the exact resulting Dashboard session identity and runtime run identity exposed by supported status/log/artifact surfaces without copying credentials.
7. Inspect the authoritative durable lifecycle evidence for that exact run/request:
   - Ticket identity/admission event;
   - session identity and generation;
   - Run identity/ownership;
   - Call/inference attempt evidence;
   - Result persistence;
   - Delivery attempt/receipt and canonical settlement.
8. Classify the observed behavior using the decision rules below.
9. Publish:
   `docs/operations/coordination/reports/CNX-20260915-357-openai-dashboard-ticket-first-requalification-report.md`
10. Verify the final remote branch tip and report blob from GitHub.
11. Stop for independent ChatGPT review. A production repair must not be bundled into this task.

## Decision rules

### PASS / BOUNDARY_CLOSED

Use only when the exact fresh OpenAI Dashboard request demonstrates the durable Ticket-first path and canonical lifecycle through delivery settlement, with no direct conversational inference bypass.

### DEFECT / CURRENT_RED

Use only when the exact fresh OpenAI Dashboard request receives/attempts OpenAI inference or a user-visible response while the authoritative durable Ticket-first lifecycle is bypassed or materially incomplete for that same request.

A current exact-run reproduction is required before any repair task is created.

### UNRESOLVED / BLOCKED

Use when the live request cannot be executed or exact-run durable evidence cannot be correlated with sufficient confidence through supported interfaces. Missing observability alone is not a defect.

## Required report contents

- exact starting and final GitHub SHAs;
- exact branch and ancestry;
- installed OpenClaw/Gateway identity, limited to non-secret data;
- installed CogentNexus identity/version;
- exact OpenAI Dashboard request timestamp and fresh session/run identifiers as available;
- durable lifecycle evidence correlated to that request;
- evidence for Ticket admission or bypass;
- evidence for Run/Call/inference/Result/Delivery states;
- no-secret accounting;
- hard-fence accounting;
- changed-path list;
- remote read-back verification;
- final classification using the decision rules above.

## Non-authorizations

This task does **not** authorize a production fix. If and only if `CURRENT_RED` is proven, a separate successor task must define the minimal TDD repair from the demonstrated failing boundary.
