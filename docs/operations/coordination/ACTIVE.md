# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX375_DASHBOARD_TICKET_FIRST_SEMANTIC_REQUALIFICATION`
Execution mode: `CONTROLLED_DASHBOARD_SEMANTIC_REQUALIFICATION`
Task ID: `CNX-20260917-375`
Parent: `CNX-20260916-374`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260916-374-plugin-hook-registration-registry-wiring-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-375-dashboard-ticket-first-semantic-requalification.md`

## Current position

CNX-367 proved the Dashboard Ticket-first bypass as `CURRENT_RED`. CNX-368 repaired the schema-v2 Host authority compatibility gate. CNX-369 activated and verified the repaired artifact. CNX-370 reproduced the bypass semantically. CNX-371 established the Dashboard Gateway → embedded selection path. CNX-372 established that supported diagnostics did not expose the process-local selection-runner hook state. CNX-373 proved `allowConversationAccess=true`, `ticketFirst=true`, `preInferenceAdmission=true`, and `enforcedMode=true` in authoritative live config. CNX-374 proved the host registry wiring root cause and repaired it by exposing the plugin definition's `hooks.allowConversationAccess=true`; focused regression passed and the Gateway was restarted with the repaired artifact.

## Next authorized task

`CNX-20260917-375` is authorized to perform exactly one controlled Dashboard semantic requalification request against the repaired runtime. The purpose is to verify the complete `before_agent_run` → Ticket-first admission → Ticket persistence/routing → pre-inference block lifecycle and establish whether the original CNX-370 bypass is resolved end-to-end.

The request must be deterministic and must not depend on provider choice, model quality, or response content beyond the required runtime/admission evidence. Use existing tracing/diagnostic surfaces; do not redesign admission or TicketStore.

## Authorization boundary

CNX-375 may issue one controlled semantic Dashboard request. It may restart the Gateway only if required to ensure the already-verified repaired artifact is active. No additional source repair is authorized unless the observed failure identifies a new concrete defect and a minimal repair is explicitly justified in the report; do not patch speculatively during this task.

After the single request and evidence capture, publish the report and stop at `WAITING_FOR_CHATGPT_REVIEW`. Do not start CNX-376 yourself.

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
