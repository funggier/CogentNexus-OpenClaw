# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX379_DISPOSABLE_REGISTRY_TRACE_HARNESS`
Execution mode: `DISPOSABLE_REGISTRY_IDENTITY_DIAGNOSIS`
Task ID: `CNX-20260917-379`
Parent: `CNX-20260917-378`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-378-live-registry-identity-correlation-diagnosis-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-379-disposable-registry-trace-harness.md`

## Current position

CNX-376 proved the Dashboard dispatch boundary. CNX-377 found the current OpenClaw source model dynamically composes live registries but could not reproduce the observed divergence as a proven repository-side defect. CNX-378 correlated the same production PID, OpenClaw build, effective CogentNexus artifact, loaded plugin record, and `hookCount: 0` inventory, but supported diagnostics could not expose JavaScript object identity. No speculative repair has been made.

## Next authorized task

`CNX-20260917-379` is authorized to build and run a disposable, non-production trace harness that directly records registry object identity and hook visibility across plugin registration, active registry initialization, live plugin collection, composed facade evaluation, and `hasHooks("before_agent_run")`.

This task is diagnosis-only. The purpose is to resolve the contradiction without mutating the production runtime.

## Authorization boundary

No Dashboard semantic request.
No production Gateway restart/reload.
No production configuration mutation.
No production OpenClaw dependency patch.
No permanent CogentNexus source patch.
Temporary instrumentation is allowed only inside a clearly disposable isolated reproduction and must not be committed.

## Hard fences

- No TicketStore/admission/provider/model/auth/routing/Dashboard UI changes.
- No production runtime mutation.
- No production configuration mutation.
- No production Gateway restart/reload.
- No semantic request.
- No speculative repair.
- No permanent source patch.
- No broad refactor.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-378.
- Do not start CNX-380 yourself.

## Closeout

Required classification:
`REGISTRY_LIFECYCLE_CAUSE_PROVEN`, `REGISTRY_INVENTORY_PROJECTION_CONTRADICTION_PROVEN`, or `DIAGNOSTIC_HARNESS_INSUFFICIENT`.

After report publication, set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop.
