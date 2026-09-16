# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX376_DASHBOARD_HOOK_DISPATCH_BOUNDARY_DIAGNOSIS`
Execution mode: `SUPPORTED_RUNTIME_HOOK_DISPATCH_DIAGNOSIS`
Task ID: `CNX-20260917-376`
Parent: `CNX-20260917-375`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-375-dashboard-ticket-first-semantic-requalification-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-376-dashboard-hook-dispatch-boundary-diagnosis.md`

## Current position

CNX-367 proved the Dashboard Ticket-first bypass as `CURRENT_RED`. CNX-368 repaired the schema-v2 Host authority compatibility gate. CNX-369 activated and verified the repaired artifact. CNX-370 reproduced the bypass semantically. CNX-371 established the Dashboard Gateway → embedded selection path. CNX-372 established that supported diagnostics did not expose process-local selection-runner hook state. CNX-373 proved live `allowConversationAccess=true`, `ticketFirst=true`, `preInferenceAdmission=true`, and `enforcedMode=true`. CNX-374 proved and repaired the plugin-definition conversation-hook registry gate. CNX-375 performed exactly one controlled Dashboard semantic request and confirmed `FAIL / TICKET_FIRST_STILL_BYPASSED`: direct model inference occurred with no Ticket or admission trace evidence.

## Next authorized task

`CNX-20260917-376` is authorized to diagnose the exact runtime boundary between the repaired plugin hook registration and actual Dashboard/WebChat hook dispatch. It must distinguish registration, registry membership, runner attachment, hook dispatch, handler invocation, and admission decision.

## Authorization boundary

CNX-376 is diagnosis-first. Supported read-only/runtime observation must be attempted before semantic traffic. If static and supported runtime evidence cannot distinguish the dispatch hypotheses, up to **2 additional Dashboard semantic requests** are authorized, but only when each request has a distinct diagnostic purpose:

1. one dispatch probe to establish whether `before_agent_run` reaches the selected runner/handler;
2. one conditional admission probe only if handler invocation is proven but Ticket-first behavior still cannot be explained.

If the first probe proves the boundary, do not send the second. No identical retry is authorized.

No source repair is authorized unless a concrete causal defect is proven and the smallest justified repair is documented.

After evidence capture, publish the report and stop at `WAITING_FOR_CHATGPT_REVIEW`. Do not start CNX-377 yourself.

## Hard fences

- Maximum 2 additional Dashboard semantic requests, only when required to distinguish dispatch hypotheses.
- No repeated identical semantic traffic.
- No provider/auth/routing/model changes.
- No semantic-contract changes.
- No Dashboard UI/provider-layer redesign.
- No TicketStore redesign.
- No admission redesign.
- No controller normalization.
- No speculative source patch.
- No unrelated runtime mutation.
- No release/tag/main changes.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-375.
- If the dispatch boundary remains unproven, stop and report the exact uncertainty.
- Do not start CNX-377 yourself.
