# Active Coordination Task

Status: `WAITING_FOR_CHATGPT_REVIEW`
State: `WAITING_FOR_CHATGPT_REVIEW`
Execution mode: `SUPPORTED_READ_ONLY_RUNTIME_HOOK_BOUNDARY_OBSERVATION`
Task ID: `CNX-20260916-372`
Parent: `CNX-20260916-371`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260916-371-dashboard-runner-admission-boundary-repair-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260916-372-selection-runner-hook-registry-runtime-observation.md`

## Current position

CNX-367 proved the Dashboard Ticket-first bypass as `CURRENT_RED`. CNX-368 repaired the schema-v2 Host authority compatibility gate and verified source/test/build behavior. CNX-369 activated and verified the repaired artifact in the live Gateway process. CNX-370 reproduced the bypass semantically. CNX-371 established the installed Dashboard → Gateway agent → embedded selection runner path and the runner's `before_agent_run` dispatch site, but could not determine the runtime hook-registry condition at that site; no repair was performed.

## Next authorized task

`CNX-20260916-372` is authorized for a bounded **read-only runtime observation** at the selection-runner dispatch boundary. It must distinguish whether the hook registry is absent, lacks `before_agent_run`, a different runner/path executes, dispatch is suppressed despite registration, or the hook is actually invoked. No source repair is authorized by this task.

## Authorization boundary

Observation only. A semantic Dashboard request is not authorized by default. One minimum-necessary controlled request may be used only if a supported observation mechanism requires a live execution trigger; it must not be treated as semantic requalification.

## Hard fences

- No source changes.
- No provider/auth/routing/model changes.
- No configuration redesign or manual controller normalization.
- No plugin reinstall/reload/restart unless an approved diagnostic attachment intrinsically requires it; justify and record any such lifecycle mutation.
- No semantic requalification.
- No repeated Dashboard requests.
- No historical edits to CNX-360 through CNX-371.
- No release/tag/main changes.
- No force-push or history rewrite.
- No guessed repair.
- Do not modify Dashboard UI or provider layer.
- If the observation remains inconclusive, report the exact uncertainty and stop.
- After publishing the CNX-372 report, transition to `WAITING_FOR_CHATGPT_REVIEW` and stop.
