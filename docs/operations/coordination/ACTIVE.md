# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX381_PLUGIN_REGISTER_INVOCATION_TRACE`
Execution mode: `EXACT_PLUGIN_REGISTRATION_LIFECYCLE_DIAGNOSIS`
Task ID: `CNX-20260917-381`
Parent: `CNX-20260917-380`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-380-exact-isolated-openclaw-registry-trace-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-381-plugin-register-invocation-trace.md`

## Current position

CNX-380 executed the exact installed OpenClaw `2026.7.1-2` lifecycle in an isolated process. The same registry identity was observed through loader, active registry, and live collection, yet `before_agent_run` did not appear and `hasHooks("before_agent_run")` was false. No replacement, retirement, collection exclusion, or causal transition was proven. The next boundary is plugin register invocation itself.

## Next authorized task

`CNX-20260917-381` is authorized to diagnose whether the real CogentNexus plugin `register(api)` lifecycle is invoked and whether its `api.on("before_agent_run")` calls actually occur in the exact OpenClaw isolated lifecycle. The task must inspect the compatibility/delegation chain from the exported plugin entry through `index.ts`.

Diagnosis only. No repair is authorized.

## Authorization boundary

No Dashboard semantic request.
No production Gateway restart/reload.
No production configuration mutation.
No production OpenClaw dependency patch.
No CogentNexus source patch.
Temporary instrumentation is allowed only in a disposable isolated process and must not be committed.

## Hard fences

- No TicketStore/admission/provider/model/auth/routing/Dashboard UI changes.
- No production runtime mutation.
- No production configuration mutation.
- No production Gateway restart/reload.
- No OpenClaw dependency patch.
- No CogentNexus source patch.
- No semantic request or production model request.
- No speculative repair.
- No permanent instrumentation.
- No committed disposable harness changes.
- No broad refactor.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-380.
- Do not start CNX-382 yourself.

## Closeout

Required classification:
`PLUGIN_REGISTER_INVOCATION_PROVEN`, `PLUGIN_REGISTER_PATH_FAILURE_PROVEN`, `PLUGIN_REGISTRATION_ACCEPTED_REGISTRY_MUTATION_PROVEN`, or `PLUGIN_REGISTER_DIAGNOSTICALLY_UNRESOLVED`.

After report publication, set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop.
