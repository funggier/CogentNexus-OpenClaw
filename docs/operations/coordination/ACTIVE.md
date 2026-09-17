# Active Coordination Task

Status: `WAITING_FOR_CHATGPT_REVIEW`
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

CNX-385 proved the raw-config → normalization → `normalized.entries[pluginId]` → `entry.hooks` → `createApi(hookPolicy)` → `registerTypedHook` gate path **preserves** `plugins.entries.<id>.hooks.allowConversationAccess=true` end-to-end. Classification: `NORMALIZED_HOOK_POLICY_PRESERVED_HOST_CONTRACT_FOUND`.

## Next authorized task

Awaiting ChatGPT review.

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
