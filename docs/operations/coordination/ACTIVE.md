# Active Coordination Task

Status: `WAITING_FOR_CHATGPT_REVIEW`
State: `CNX371_DASHBOARD_RUNNER_ADMISSION_BOUNDARY_REPAIR`
Execution mode: `SUPPORTED_HOST_RUNNER_DIAGNOSIS_AND_MINIMAL_REPAIR`
Task ID: `CNX-20260916-371`
Parent: `CNX-20260916-370`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260916-370-live-semantic-requalification-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260916-371-dashboard-runner-admission-boundary-repair.md`

## Current position

CNX-367 proved the Dashboard Ticket-first bypass as `CURRENT_RED`. CNX-368 repaired the schema-v2 Host authority compatibility gate and verified source/test/build behavior. CNX-369 activated and verified the repaired artifact in the live Gateway process. CNX-370 then performed one authorized live Dashboard semantic request and reproduced the bypass. CNX-371 inspected the installed Dashboard Gateway/embedded selection path but could not prove the runtime hook-registry condition at the dispatch boundary; no repair or runtime mutation was performed. Report: `docs/operations/coordination/reports/CNX-20260916-371-dashboard-runner-admission-boundary-repair-report.md`.

## Next authorized task

`CNX-20260916-371` is authorized to diagnose the exact OpenClaw Dashboard runner/invocation boundary responsible for the missing `before_agent_run` invocation and, only after the concrete host-boundary cause is proven, implement the smallest justified repair at that boundary. The task must preserve the existing CogentNexus admission policy and Ticket lifecycle rather than creating a parallel Dashboard-only path.

## Authorization boundary

This task explicitly authorizes bounded source repair after diagnosis, focused regression testing, supported runtime activation if needed to make the repaired artifact active, and the minimum read-only/live verification necessary to establish artifact identity. A semantic Dashboard request is not the default action of this task; prefer a separate later requalification task after repair unless one bounded proof request is genuinely required and recorded.

## Hard fences

- No provider/auth/routing changes.
- No model/provider substitution.
- No manual controller normalization.
- No unrelated Dashboard traffic.
- No historical edits to CNX-360 through CNX-370.
- No release/tag/main changes.
- No force-push or history rewrite.
- Do not change the semantic contract merely to make the test pass.
- Do not duplicate admission logic in the Dashboard UI or provider layer.
- Do not introduce a competing Ticket admission path.
- Do not broad-refactor unrelated code.
- Do not claim Ticket-first restoration without lifecycle-ordering evidence.
- If diagnosis is inconclusive, publish evidence and stop rather than guessing a repair.
- After publishing the CNX-371 report, transition to `WAITING_FOR_CHATGPT_REVIEW` and stop.
