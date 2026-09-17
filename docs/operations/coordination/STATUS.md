# Coordination Channel Status

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

## Current authorization

CNX-382 diagnoses the exact metadata/policy projection path from the loaded CogentNexus plugin definition to the `hookPolicy` consumed by `registerTypedHook`.

Diagnosis only; no repair.

## Evidence target

Determine where `hooks.allowConversationAccess=true` is preserved, transformed, omitted, or replaced between plugin definition load and the host conversation-hook gate.

CNX-382 result: `HOOK_POLICY_PROJECTION_LOSS_PROVEN`. The exact loader uses `normalized.entries[pluginId]?.hooks` as `hookPolicy`; executable `releaseEntry.hooks` is not projected into that object.

## Hard fences

No production runtime or configuration mutation. No source/dependency patch. No artifact rebuild. No semantic/model requests. No speculative repair. No permanent or committed instrumentation. No broad refactor. No release/tag/main. No force-push/history rewrite. No historical edits to CNX-360 through CNX-381. Do not start CNX-383 yourself.

## Closeout

Required classification:
`HOOK_POLICY_PROJECTION_LOSS_PROVEN`
`HOOK_POLICY_PROJECTION_PRESERVED_GATE_SOURCE_MISMATCH`
`HOOK_POLICY_PROJECTION_PATH_NOT_REPRODUCED`
`HOOK_POLICY_PROJECTION_DIAGNOSTICALLY_UNRESOLVED`

After report publication, set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop.
