# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX393_GLOBAL_CONFIG_ENTRY_ASSOCIATION_TRACE`
Execution mode: `GLOBAL_CONFIG_ENTRY_ASSOCIATION_TRACE`
Task ID: `CNX-20260917-393`
Parent: `CNX-20260917-392`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-392-production-vs-config-origin-hook-policy-replay-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-393-global-discovery-config-entry-association-trace.md`

## Current position

CNX-392 was reviewed and accepted as `PRODUCTION_ORIGIN_REPLAY_DIAGNOSTICALLY_BLOCKED`. Exact source tracing showed `global` and `config` are discovery-origin labels and both use the same non-bundled conversation-hook policy branch; `registrationMode` is derived from `registrationPlan.mode`, not directly from origin. A safe exact global-origin isolated replay could not be constructed without mutating the production global extension/discovery state. CNX-391 already proved that the production-shaped `allowConversationAccess=true` configuration can be accepted through the exact loader/API path in isolation.

## Current authorization

CNX-393 is READY for Hermes execution.

Trace how a globally discovered candidate (`origin=global`) is associated with the normalized runtime configuration entry used for `hookPolicy`:

`discovery candidate → pluginId → normalized.entries[pluginId] → entry.hooks → createApi(hookPolicy) → registerTypedHook`

Determine whether global discovery can cause the candidate to miss, diverge from, or otherwise change its normalized config-entry association despite the same `plugins.entries.cogentnexus-openclaw` key being present in production configuration.

Use read-only production evidence and disposable isolated/source-level probes only. Do not touch the production global extension tree.

No production restart/reload.
No production configuration mutation.
No environment mutation.
No Scheduled Task mutation.
No OpenClaw dependency patch.
No CogentNexus source repair.
No artifact deployment/rebuild.
No debugger/inspector attachment.
No semantic/model/provider request.

## Hard fences

- No TicketStore/admission/provider/model/auth/routing/Dashboard UI changes.
- No speculative workaround.
- No production global extension installation/mutation.
- No semantic probe or retry.
- No permanent instrumentation.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-392.
- Do not start CNX-394 yourself.

## Closeout

After report publication, set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop. Do not start CNX-394.
