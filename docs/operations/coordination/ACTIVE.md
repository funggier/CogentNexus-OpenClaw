# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX370_LIVE_SEMANTIC_REQUALIFICATION`
Execution mode: `SUPPORTED_LIVE_SEMANTIC_REQUALIFICATION`
Task ID: `CNX-20260916-370`
Parent: `CNX-20260916-369`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260916-369-runtime-activation-verification-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260916-370-live-semantic-requalification.md`

## Current position

CNX-367 proved the Dashboard Ticket-first bypass as `CURRENT_RED`. CNX-368 proved the root cause at `Host authority decision → plugin registration` and completed the minimal schema-v2 compatibility repair with TDD and full validation. CNX-369 activated and verified the repaired artifact in the live Gateway process and established the effective registration path without performing a semantic Dashboard request.

## Next authorized task

`CNX-20260916-370` is the successor live semantic requalification task. It may perform one minimum-necessary controlled Dashboard semantic request against the already-activated repaired runtime to determine whether Ticket-first admission is restored. It must capture fresh lifecycle evidence showing Ticket admission and `before_agent_run` ordering relative to model execution.

If semantic requalification fails, Hermes must publish the evidence and stop. Repair is a separate later authorization.

## Hard fences

- One minimum-necessary controlled Dashboard semantic request only; do not retry CNX-367 verbatim or generate unrelated traffic.
- No source-code changes during CNX-370.
- No provider/auth/routing changes.
- No configuration redesign or manual controller normalization.
- Do not modify hooks/main, release/tag, or historical CNX-360 through CNX-369 records.
- Any runtime lifecycle mutation, if genuinely required, must be recorded with exact action and before/after process identity.
- Do not force-push or rewrite history.
- After publishing the CNX-370 report, stop and hand off with `WAITING_FOR_CHATGPT_REVIEW`.
