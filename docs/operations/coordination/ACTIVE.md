# Active Coordination Task

Status: `WAITING_FOR_CHATGPT_REVIEW`
State: `CNX396_GLOBAL_CANDIDATE_NORMALIZED_CONFIG_PROVENANCE`
Execution mode: `GLOBAL_CANDIDATE_NORMALIZED_CONFIG_PROVENANCE`
Task ID: `CNX-20260917-396`
Parent: `CNX-20260917-395`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-395-installed-plugin-index-population-freshness-provenance-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-396-global-candidate-normalized-config-provenance-trace.md`

## Current position

CNX-395 was reviewed and accepted as `INSTALLED_INDEX_PROVEN_STALE_OR_PREEXISTING`. Exact read-only evidence proved the production installed-plugin index row is persisted in SQLite and predates the current gateway process by approximately 21 hours. Its `pluginId`, root, origin, and source match the current inventory/effective artifact, but the index can also be refreshed by policy/install/migration/discovery lifecycles without receiving the live loader record. Therefore installed-index provenance cannot establish what the running global loader supplied as `hookPolicy` during registration.

CNX-391 proved exact config-origin acceptance of `hooks.allowConversationAccess=true` through the loader/API lifecycle. CNX-392 proved candidate origin is not itself the direct selector for the downstream conversation-hook policy branch. CNX-393 traced `candidate.rootDir → manifestRecord.id → normalized.entries[pluginId]` but could not observe the historical live values. CNX-394 and CNX-395 established that supported inventory/index output is a separate persisted/derived projection and is not live typed-hook registry state.

## Current authorization

CNX-396 is READY for Hermes execution.

Trace how the loader constructs/selects `normalized` configuration before `entry = normalized.entries[pluginId]`, specifically comparing `origin=config` and `origin=global` for the same plugin and production-shaped config.

Determine whether global discovery can diverge from config-origin before `createApi({ hookPolicy })` through any difference in normalized entry presence, plugin ID, enablement, policy, registration plan, config object, or candidate filtering.

Use read-only production evidence and disposable exact-source/isolated probes only.

No production mutation is authorized.

## Hard fences

- No production Gateway restart/reload.
- No production configuration mutation.
- No environment mutation.
- No Scheduled Task mutation.
- No production global extension installation/mutation.
- No production artifact replacement/deploy.
- No OpenClaw dependency patch.
- No CogentNexus source repair.
- No debugger/inspector attachment.
- No semantic/model/provider/Dashboard request.
- No TicketStore/admission/routing/auth changes.
- No production retry.
- No speculative workaround.
- No permanent instrumentation.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-395.
- Do not create or start CNX-397 yourself.

## Closeout

After report publication, set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop. Do not create/start CNX-397.
