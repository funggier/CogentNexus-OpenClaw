# Coordination Channel Status

Status: `READY_FOR_HERMES`
State: `CNX374_PLUGIN_HOOK_REGISTRY_WIRING_DIAGNOSIS`
Task ID: `CNX-20260916-374`
Parent: `CNX-20260916-373`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260916-373-conversation-hook-access-gate-repair-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260916-374-plugin-hook-registration-registry-wiring.md`

## Current position

CNX-367 completed as `CURRENT_RED`, with the Dashboard path proven to bypass Ticket-first admission. CNX-368 completed as `REPAIRED / VERIFIED` at source/test/build level and fixed the schema-v2 Host authority compatibility mismatch that suppressed plugin registration. CNX-369 activated and verified the repaired artifact in the live Gateway process. CNX-370 completed as `FAIL / NOT REQUALIFIED`. CNX-371 established the Dashboard Gateway → embedded selection path but could not prove the runtime hook-registry condition. CNX-372 established that supported runtime diagnostics expose the plugin as loaded/enabled but do not expose the process-local hook registry or `runBeforeAgentRun` invocation state. CNX-373 proved `allowConversationAccess=true`, `ticketFirst=true`, `preInferenceAdmission=true`, and `enforcedMode=true` in the authoritative live config without mutation.

## Authorization boundary

Current successor: `CNX-20260916-374` — PLUGIN HOOK REGISTRATION / REGISTRY WIRING DIAGNOSIS. This task is explicitly authorized to diagnose the exact plugin hook registration → host hook registry wiring boundary and, only after a concrete causal mechanism is proven, implement the smallest justified source repair and focused regression coverage. Supported runtime activation may be used after validated repair if required.

Semantic Dashboard requalification is not authorized by default and should be deferred to a separate successor task.

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
- If diagnosis remains inconclusive, stop and report the uncertainty.
- Do not start CNX-375 yourself.
