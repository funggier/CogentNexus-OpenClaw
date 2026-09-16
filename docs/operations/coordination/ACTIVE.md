# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX378_LIVE_REGISTRY_IDENTITY_CORRELATION_DIAGNOSIS`
Execution mode: `LIVE_REGISTRY_IDENTITY_CORRELATION_DIAGNOSIS`
Task ID: `CNX-20260917-378`
Parent: `CNX-20260917-377`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-377-composed-registry-wiring-repair-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-378-live-registry-identity-correlation-diagnosis.md`

## Current position

CNX-376 proved the Dashboard dispatch boundary, but CNX-377 could not reconcile the live `hookCount: 0` observation with the current OpenClaw source's live registry composition model. No speculative repair was made.

## Next authorized task

`CNX-20260917-378` is authorized to correlate the exact live OpenClaw process/build, effective CogentNexus artifact, plugin load/registration event, registry object identity, global hook-runner state, and composed registry queried by the Dashboard selection runner.

The purpose is diagnosis only. A concrete source defect or repair must not be claimed without direct evidence.

## Authorization boundary

No Dashboard semantic request.
No production Gateway restart/reload by default.
No OpenClaw dependency patch.
No plugin source patch unless a new explicit authorization extends this task.

Use supported process-local/passive diagnostics where available. A disposable reproduction may be used only when clearly separated from the production runtime.

## Hard fences

- No TicketStore/admission/provider/model/auth/routing/Dashboard UI changes.
- No speculative patch.
- No production configuration changes.
- No production Gateway restart/reload by default.
- No semantic request.
- No broad refactor.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-377.
- Do not start CNX-379 yourself.

## Closeout

Required classification:
`LIVE_REGISTRY_IDENTITY_CORRELATED`, `LIVE_REGISTRY_IDENTITY_CONTRADICTION_UNRESOLVED`, or `DIAGNOSTIC_ACCESS_BLOCKED`.

After report publication, set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop.
