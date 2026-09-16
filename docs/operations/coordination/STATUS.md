# Coordination Channel Status

Status: `WAITING_FOR_CHATGPT_REVIEW`
State: `CNX371_DASHBOARD_RUNNER_ADMISSION_BOUNDARY_REPAIR`
Task ID: `CNX-20260916-371`
Parent: `CNX-20260916-370`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260916-370-live-semantic-requalification-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260916-371-dashboard-runner-admission-boundary-repair.md`

## Current position

CNX-367 completed as `CURRENT_RED`, with the Dashboard path proven to bypass Ticket-first admission. CNX-368 completed as `REPAIRED / VERIFIED` at source/test/build level and fixed the schema-v2 Host authority compatibility mismatch that suppressed plugin registration. CNX-369 activated and verified the repaired artifact in the live Gateway process and established effective downstream registration. CNX-370 completed as `FAIL / NOT REQUALIFIED`. CNX-371 inspected the installed Dashboard Gateway/embedded selection path but classification remained `BLOCKED / DIAGNOSIS INCONCLUSIVE` because the runtime hook-registry condition at the dispatch boundary was not proven; no repair or runtime mutation was performed. Report: `docs/operations/coordination/reports/CNX-20260916-371-dashboard-runner-admission-boundary-repair-report.md`.

## Authorization boundary

Current successor: `CNX-20260916-371` — DASHBOARD RUNNER ADMISSION BOUNDARY DIAGNOSIS AND MINIMAL REPAIR. This task is explicitly authorized to diagnose the exact OpenClaw Dashboard runner/invocation boundary responsible for the missing `before_agent_run` invocation and, only after the concrete cause is proven, implement the smallest justified source repair, focused regression tests, and supported runtime activation if needed.

The repair must restore the existing intended lifecycle rather than creating a parallel Dashboard-only admission path. A semantic Dashboard request is not the default action; prefer handing the repaired runtime to a separate later requalification task unless one minimum-necessary bounded proof request is genuinely required.

## Hard fences

- No provider/auth/routing changes.
- No model/provider substitution.
- No manual controller normalization.
- No unrelated Dashboard traffic.
- No historical edits to CNX-360 through CNX-370.
- No release/tag/main changes.
- No force-push or history rewrite.
- Do not change the semantic contract merely to make a test pass.
- Do not duplicate admission logic in the Dashboard UI or provider layer.
- Do not introduce a competing Ticket admission path.
- Do not broad-refactor unrelated code.
- Do not claim Ticket-first restoration without lifecycle-ordering evidence.
- If diagnosis is inconclusive, publish evidence and stop rather than guessing a repair.
- After publishing the CNX-371 report, transition to `WAITING_FOR_CHATGPT_REVIEW` and stop.
