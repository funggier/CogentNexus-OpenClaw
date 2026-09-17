# Active Coordination Task

Status: `WAITING_FOR_CHATGPT_REVIEW`
State: `CNX382_PLUGIN_HOOK_POLICY_PROJECTION_TRACE`
Execution mode: `EXACT_HOOK_POLICY_PROJECTION_DIAGNOSIS`
Task ID: `CNX-20260917-382`
Parent: `CNX-20260917-381`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-381-plugin-register-invocation-trace-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-382-plugin-hook-policy-projection-trace.md`

## Current position

CNX-381 executed the exact isolated OpenClaw lifecycle and proved that the real `register(api)` and repeated `api.on("before_agent_run")` calls reach host `registerTypedHook`, but the host rejects them because the effective non-bundled hook policy is not true. The executable plugin definition simultaneously contains `hooks.allowConversationAccess: true`.

CNX-382 proved `HOOK_POLICY_PROJECTION_LOSS_PROVEN`: the loader passes `normalized.entries[pluginId]?.hooks` to `createApi`, not the executable definition's `hooks`. Report: `docs/operations/coordination/reports/CNX-20260917-382-plugin-hook-policy-projection-trace-report.md`.

## Next authorized task

CNX-382 diagnosis is complete and awaiting ChatGPT review.

Diagnosis only; no repair. No successor task authorized.

## Authorization boundary

No semantic request.
No production Gateway restart/reload.
No production configuration mutation.
No OpenClaw dependency patch.
No CogentNexus source/artifact patch.
No artifact rebuild.
Temporary instrumentation is allowed only in a disposable isolated process and must not be committed.

## Hard fences

- No production runtime/configuration mutation.
- No source or dependency patch.
- No artifact rebuild.
- No semantic/model requests.
- No speculative repair.
- No permanent or committed instrumentation.
- No broad refactor.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-381.
- Do not start CNX-383 yourself.

## Closeout

Required classification:
`HOOK_POLICY_PROJECTION_LOSS_PROVEN`, `HOOK_POLICY_PROJECTION_PRESERVED_GATE_SOURCE_MISMATCH`, `HOOK_POLICY_PROJECTION_PATH_NOT_REPRODUCED`, or `HOOK_POLICY_PROJECTION_DIAGNOSTICALLY_UNRESOLVED`.

After report publication, set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop.
