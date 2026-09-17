# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX394_PRODUCTION_PLUGIN_ID_PROJECTION_TRACE`
Execution mode: `PRODUCTION_PLUGIN_ID_PROJECTION_TRACE`
Task ID: `CNX-20260917-394`
Parent: `CNX-20260917-393`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-393-global-discovery-config-entry-association-trace-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-394-production-plugin-id-inventory-projection-trace.md`

## Current position

CNX-393 was reviewed and accepted as `GLOBAL_CONFIG_ENTRY_ASSOCIATION_DIAGNOSTICALLY_BLOCKED`. Exact source tracing proved:

`candidate.rootDir → manifestByRoot.get(candidate.rootDir) → manifestRecord.id → normalized.entries[pluginId] → entry?.hooks → createApi(hookPolicy) → registerTypedHook`

The remaining uncertainty is whether the production `openclaw plugins list --json` record's displayed `id` is a direct projection of that same loader `pluginId`, or whether an intermediate registry/inventory projection can alter or detach the identity. The production record currently reports `id=cogentnexus-openclaw`, `origin=global`, `status=loaded`, `hookCount=0`, `hookNames=[]` while production config contains `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true`.

## Current authorization

CNX-394 is READY for Hermes execution.

Trace the production plugin-ID projection path from loader `manifestRecord.id` / `pluginId` to the record returned by `openclaw plugins list --json`. Determine whether the inventory `id` is the exact identity used for `normalized.entries[pluginId]`, and whether `hookCount` / `hookNames` are projected from the same registry state that receives `registerTypedHook`.

Use read-only production evidence and disposable isolated/source-level probes only.

No production restart/reload.
No production configuration mutation.
No environment mutation.
No Scheduled Task mutation.
No production global extension installation/mutation.
No OpenClaw dependency patch.
No CogentNexus source repair.
No artifact deployment/rebuild.
No debugger/inspector attachment.
No semantic/model/provider/Dashboard request.

## Hard fences

- No TicketStore/admission/provider/model/auth/routing/Dashboard UI changes.
- No speculative workaround.
- No production global extension installation/mutation.
- No semantic probe or retry.
- No permanent instrumentation.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-393.
- Do not start CNX-395 yourself.

## Closeout

After report publication, set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop. Do not start CNX-395.
