# CNX-20260915-359 — Admission Trace Instrumentation

Status: `READY_FOR_HERMES`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Parent: `CNX-358`
Execution mode: `TDD_DIAGNOSTIC_INSTRUMENTATION`
Base release: `v0.9.5`

## Objective

Add the smallest non-secret, correlation-preserving diagnostic trace around the existing `before_agent_run` admission boundary so a fresh operator-run OpenAI Dashboard request can distinguish:

A. hook not dispatched;
B. hook dispatched but ineligible;
C. eligible but Ticket-first not entered or persistence failed;
D. Ticket persisted but lineage correlation was lost;
E. OpenClaw executed outside CogentNexus.

## Hard fences

- Preserve provider routing and all existing admission semantics.
- No new behavior beyond diagnostic evidence.
- Do not log prompts, credentials, API keys, tokens, or secrets.
- Do not add undocumented Gateway APIs.
- Do not control or automate the Dashboard.
- Do not mutate `main`, the `v0.9.5` tag, or history; no force-push.
- Do not claim live PASS; fresh Dashboard action remains human-gated.

## Required trace contract

Emit structured, non-secret events through the existing plugin logging surface with a correlation object containing `traceId`, `runId` when available, `sessionKey`, `sessionId` when available, and timestamp. Required states are:

- `admission.trace.started`
- `admission.trace.input`
- `admission.trace.eligible`
- `admission.trace.ticket-decision`
- `admission.trace.ticket-persisted` when a Ticket exists
- `admission.trace.blocked` when admission blocks
- `admission.trace.completed`

The instrumentation must not alter return values, persistence semantics, routing, or prompt contents.

## TDD gates

1. Add a focused RED test proving the required admission trace evidence is absent before instrumentation.
2. Run the focused test and retain the genuine RED result.
3. Implement minimal instrumentation.
4. Run focused tests, then relevant plugin regression tests and build/validation.
5. Prepare/install/reload only through the supported normal path after code verification; record exact candidate identity and activation evidence.
6. Stop before any fresh Dashboard interaction and give the Operator the exact UI steps.

## Required report

Publish `docs/operations/coordination/reports/CNX-20260915-359-admission-trace-instrumentation-report.md` with exact SHA/branch, RED and GREEN outputs, changed paths, trace schema, activation evidence, no-secret/hard-fence accounting, and the precise human Dashboard handoff.

## Completion boundary

This task completes only when the diagnostic candidate is tested and prepared/activated, not when a fresh Dashboard request is run. If a future fresh trace proves a defect, create a separate repair task before changing semantics.
