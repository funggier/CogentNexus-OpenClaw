# Active Coordination Task

Status: `BLOCKED`
State: `CNX364_PATH_BOUND_RUNTIME_PROVENANCE`
Execution mode: `SUCCESSOR_TASK_CREATION_AND_READ_ONLY_PATH_BOUND_PREFLIGHT_ONLY`
Task ID: `CNX-20260915-364`
Parent: `CNX-20260915-363`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260915-364-path-bound-runtime-provenance-report.md`

## Current position

CNX-359 through CNX-363 are preceding historical task records. CNX-364 established that historical CNX-361/CNX-362 controller-path identity is not proven, that multiple Host roots can coexist, and that the current canonical root can be identified without normalizing runtime state. CNX-364 remains `BLOCKED`.

CNX-360 is no longer the current task. No runtime semantic test is authorized at this boundary. A successor diagnostic/requalification task may be created, but its execution remains gated by its own path-bound preflight and a later explicit semantic-test authorization.

## Next authorized task

`CNX-365_PATH_BOUND_CONTROLLED_REQUALIFICATION`

Authorization is limited to creating the successor task and, after that task is separately accepted as current authority, performing read-only path-bound preflight. It does not authorize a Dashboard request, model request, semantic test, runtime mutation, lifecycle action, reinstall, controller edit, provider/auth/routing change, hook/main change, or release/tag change.

## Hard fences

- Do not open Dashboard or send any model request.
- Do not run a runtime semantic test or claim OpenAI PASS, CURRENT_RED, or runtime repair.
- Do not enable, start, restart, disable, stop, reinstall, or normalize runtime state.
- Do not edit controller.json, provider/auth/routing, hooks, main, the v0.9.5 tag/release, or historical task/report records.
- Do not force-push or rewrite history.
