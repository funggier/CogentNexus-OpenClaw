# Active Coordination Task

Status: `WAITING_FOR_CHATGPT_REVIEW`
State: `CNX374_PLUGIN_HOOK_REGISTRY_WIRING_DIAGNOSIS`
Execution mode: `SUPPORTED_PLUGIN_REGISTRY_WIRING_DIAGNOSIS`
Task ID: `CNX-20260916-374`
Parent: `CNX-20260916-373`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260916-373-conversation-hook-access-gate-repair-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260916-374-plugin-hook-registration-registry-wiring.md`
Report: `docs/operations/coordination/reports/CNX-20260916-374-plugin-hook-registration-registry-wiring-report.md`

## Current position

CNX-367 proved the Dashboard Ticket-first bypass as `CURRENT_RED`. CNX-368 repaired the schema-v2 Host authority compatibility gate and verified source/test/build behavior. CNX-369 activated and verified the repaired artifact in the live Gateway process. CNX-370 reproduced the bypass semantically. CNX-371 established the Dashboard Gateway → embedded selection path but could not prove the runtime hook-registry condition. CNX-372 established that supported runtime diagnostics expose the plugin as loaded/enabled but do not expose the process-local hook registry or `runBeforeAgentRun` invocation state. CNX-373 proved `allowConversationAccess=true`, `ticketFirst=true`, `preInferenceAdmission=true`, and `enforcedMode=true` in the authoritative live config without mutation. CNX-374 diagnosed `REGISTRY_WIRING_BROKEN`: the host conversation-hook gate in `registry-B8eQDFB4.js` blocks dynamic `before_agent_run` registration for non-bundled plugins unless the DEFINITION's `hooks.allowConversationAccess` is `true` (distinct from runtime config, which only feeds pluginConfig). The fix adds `hooks: { allowConversationAccess: true }` to the `definePluginEntry` object, with focused regression test and Gateway restart activation.

## Next authorized task

None. Awaiting ChatGPT review of CNX-374 findings and fix.

## Authorization boundary

This task is complete. No further Hermes execution is authorized without a new task from ChatGPT.

## Hard fences

- No provider/auth/routing/model changes.
- No semantic-contract changes.
- No Dashboard UI/provider-layer changes.
- No speculative source patch.
- No TicketStore/admission redesign.
- No manual controller normalization.
- No repeated Dashboard traffic.
- No semantic requalification by default.
- No historical edits to CNX-360 through CNX-373.
- No release/tag/main.
- No force-push/history rewrite.
- Do not start CNX-375 yourself.
