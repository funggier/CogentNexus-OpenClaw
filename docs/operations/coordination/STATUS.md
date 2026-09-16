# Coordination Channel Status

Status: `WAITING_FOR_CHATGPT_REVIEW`
State: `CNX374_PLUGIN_HOOK_REGISTRY_WIRING_DIAGNOSIS`
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

CNX-367 completed as `CURRENT_RED`, with the Dashboard path proven to bypass Ticket-first admission. CNX-368 completed as `REPAIRED / VERIFIED` at source/test/build level and fixed the schema-v2 Host authority compatibility mismatch that suppressed plugin registration. CNX-369 activated and verified the repaired artifact in the live Gateway process. CNX-370 completed as `FAIL / NOT REQUALIFIED`. CNX-371 established the Dashboard Gateway → embedded selection path but could not prove the runtime hook-registry condition. CNX-372 established that supported runtime diagnostics expose the plugin as loaded/enabled but do not expose the process-local selection-runner hook registry or `runBeforeAgentRun` invocation state. CNX-373 proved `allowConversationAccess=true`, `ticketFirst=true`, `preInferenceAdmission=true`, and `enforcedMode=true` in the authoritative live config without mutation. CNX-374 diagnosed `REGISTRY_WIRING_BROKEN` and repaired it: added `hooks: { allowConversationAccess: true }` to the `definePluginEntry` object so the host conversation-hook gate passes for the non-bundled plugin. Focused regression test PASS. Gateway restarted to load the patched artifact.

## Authorization boundary

Current task: `CNX-20260916-374` — COMPLETE. Awaiting ChatGPT review.

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
