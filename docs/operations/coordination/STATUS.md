# Coordination Channel Status

Status: `READY_FOR_HERMES`
State: `CNX375_DASHBOARD_TICKET_FIRST_SEMANTIC_REQUALIFICATION`
Task ID: `CNX-20260917-375`
Parent: `CNX-20260916-374`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260916-374-plugin-hook-registration-registry-wiring-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-375-dashboard-ticket-first-semantic-requalification.md`

## Current position

CNX-367 completed as `CURRENT_RED`, with the Dashboard path proven to bypass Ticket-first admission. CNX-368 completed as `REPAIRED / VERIFIED` at source/test/build level and fixed the schema-v2 Host authority compatibility mismatch that suppressed plugin registration. CNX-369 activated and verified the repaired artifact in the live Gateway process. CNX-370 completed as `FAIL / NOT REQUALIFIED`. CNX-371 established the Dashboard Gateway → embedded selection path but could not prove the runtime hook-registry condition. CNX-372 established that supported runtime diagnostics expose the plugin as loaded/enabled but do not expose the process-local selection-runner hook registry or `runBeforeAgentRun` invocation state. CNX-373 proved `allowConversationAccess=true`, `ticketFirst=true`, `preInferenceAdmission=true`, and `enforcedMode=true` in the authoritative live config without mutation. CNX-374 diagnosed `REGISTRY_WIRING_BROKEN` and repaired it at the plugin definition boundary by exposing `hooks.allowConversationAccess=true`; focused regression passed and the Gateway was restarted with the patched artifact. CNX-374 is accepted for its authorized diagnosis/repair scope. End-to-end Dashboard semantic restoration remains unproven.

## Authorization boundary

Current successor: `CNX-20260917-375` — DASHBOARD TICKET-FIRST SEMANTIC REQUALIFICATION. Exactly one controlled Dashboard semantic request is authorized to determine whether `before_agent_run` now reaches the Ticket-first admission lifecycle in the repaired runtime. No additional semantic traffic is authorized.

## Hard fences

- Exactly one controlled Dashboard semantic request.
- No repeated Dashboard traffic.
- No provider/auth/routing/model changes.
- No semantic-contract changes.
- No Dashboard UI/provider-layer changes.
- No TicketStore redesign or admission redesign.
- No controller normalization.
- No speculative source patch.
- No unrelated runtime mutation.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-374.
- Stop and report if evidence is insufficient or contradictory.
- Do not start CNX-376 yourself.
