# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX369_RUNTIME_ACTIVATION_VERIFICATION`
Execution mode: `SUPPORTED_RUNTIME_ACTIVATION_AND_READ_ONLY_EFFECTIVE_REGISTRATION_VERIFICATION`
Task ID: `CNX-20260916-369`
Parent: `CNX-20260916-368`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260916-368-ticket-first-admission-root-cause-repair-report.md`

## Current position

CNX-367 proved the Dashboard Ticket-first bypass as `CURRENT_RED`. CNX-368 proved the root cause at `Host authority decision → plugin registration` and completed the minimal schema-v2 compatibility repair with TDD and full validation. CNX-368 did not reload, reinstall, or otherwise activate the repaired artifact in the live Gateway process.

## Next authorized task

`CNX-20260916-369` is the successor runtime activation verification task. It may use the supported bounded runtime lifecycle needed to make the already-verified repaired entrypoint active, then verify that the actual Gateway process is using the repaired artifact and that the downstream `before_agent_run` registration path is effective.

No semantic Dashboard/model request is authorized in CNX-369. Live semantic requalification remains a separate later authorization after CNX-369 stops.

## Hard fences

- Do not send a Dashboard/model request or semantic test.
- Do not retry CNX-367 or generate another reproduction request.
- Use only supported bounded activation/reload/install mechanisms; no manual controller normalization.
- Do not modify provider/auth/routing, hooks/main, release/tag, or historical CNX-360 through CNX-368 records.
- Any runtime lifecycle mutation must be recorded with exact action and before/after process identity.
- Do not force-push or rewrite history.
