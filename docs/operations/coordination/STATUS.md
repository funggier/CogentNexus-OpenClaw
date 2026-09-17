# Coordination Channel Status

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

## Current authorization

CNX-392 is reviewed and accepted as `PRODUCTION_ORIGIN_REPLAY_DIAGNOSTICALLY_BLOCKED`. Exact source tracing showed `global` and `config` are discovery-origin labels and both use the same non-bundled conversation-hook policy branch; `registrationMode` is derived from `registrationPlan.mode`, not directly from origin. A safe exact global-origin isolated replay could not be constructed without mutating the production global extension/discovery state. CNX-391 already proved that the production-shaped `allowConversationAccess=true` configuration can be accepted through the exact loader/API path in isolation.

CNX-393 is READY for Hermes execution. Trace how a globally discovered candidate (`origin=global`) is associated with the normalized runtime configuration entry used for `hookPolicy`: `discovery candidate → pluginId → normalized.entries[pluginId] → entry.hooks → createApi(hookPolicy) → registerTypedHook`. Determine whether global discovery can cause the candidate to miss, diverge from, or otherwise change its normalized config-entry association despite the same `plugins.entries.cogentnexus-openclaw` key being present in production configuration. Use read-only production evidence and disposable isolated/source-level probes only. Do not touch the production global extension tree.

## Hard fences

- No production Gateway restart/reload.
- No production configuration mutation.
- No environment mutation.
- No Scheduled Task mutation.
- No production global extension installation/mutation.
- No OpenClaw dependency patch.
- No CogentNexus source repair.
- No artifact deployment/rebuild.
- No debugger/inspector attachment.
- No semantic/model/provider/Dashboard request.
- No TicketStore/admission/routing/auth changes.
- No speculative workaround.
- No semantic probe or retry.
- No permanent instrumentation.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-392.
- Do not start CNX-394 yourself.

## Closeout

After report publication, set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop. Do not start CNX-394.
