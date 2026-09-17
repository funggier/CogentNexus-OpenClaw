# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX385_NORMALIZED_HOOK_POLICY_INPUT_PATH_DIAGNOSIS`
Execution mode: `NORMALIZED_HOOK_POLICY_INPUT_PATH_DIAGNOSIS`
Task ID: `CNX-20260917-385`
Parent: `CNX-20260917-384`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-384-host-hook-policy-projection-repair-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-385-normalized-hook-policy-input-path-diagnosis.md`

## Current position

CNX-382 proved the executable definition declares `hooks.allowConversationAccess=true` while the loader passes `normalized.entries[pluginId]?.hooks` to `createApi` as `hookPolicy`. CNX-383/384 established that the plugin repository does not own the normalization/projection implementation and has no existing tracked, clean-install-reproducible host dependency patch mechanism.

## Next authorized task

`CNX-20260917-385` is authorized to diagnose the exact raw-config/schema/normalization path producing `normalized.entries[pluginId]` and determine whether the configured `plugins.entries.<id>.hooks.allowConversationAccess=true` is intentionally stripped, transformed, or otherwise not part of the supported normalized entry contract.

The task must also determine whether an existing supported plugin/configuration or installation extension point can preserve the policy without patching OpenClaw or inventing a new dependency architecture.

Diagnosis only. No repair is authorized.

## Authorization boundary

No production Gateway restart/reload.
No production configuration mutation.
No OpenClaw dependency patch.
No CogentNexus source repair.
No artifact deployment/rebuild.
No semantic or model request.
Temporary instrumentation is allowed only in a disposable isolated process and must not be committed except for a narrowly justified permanent regression documenting the proven normalization boundary.

## Hard fences

- No TicketStore/admission/provider/model/auth/routing/Dashboard UI changes.
- No speculative workaround.
- No new dependency architecture.
- No permanent or committed instrumentation unless it is a focused regression required to document the proven boundary.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-384.
- Do not start CNX-386 yourself.

## Closeout

Required classification:
`NORMALIZED_HOOK_POLICY_STRIPPING_PROVEN`
`NORMALIZED_HOOK_POLICY_PRESERVED_HOST_CONTRACT_FOUND`
`NORMALIZED_HOOK_POLICY_INPUT_PATH_UNRESOLVED`
`NORMALIZED_HOOK_POLICY_DIAGNOSTICALLY_BLOCKED`

After report publication, set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop.
