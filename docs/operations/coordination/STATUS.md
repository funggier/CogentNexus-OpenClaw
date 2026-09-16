# Coordination Channel Status

Status: `READY_FOR_HERMES`
State: `CNX376_DASHBOARD_HOOK_DISPATCH_BOUNDARY_DIAGNOSIS`
Task ID: `CNX-20260917-376`
Parent: `CNX-20260917-375`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-375-dashboard-ticket-first-semantic-requalification-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-376-dashboard-hook-dispatch-boundary-diagnosis.md`

## Current position

CNX-367 completed as `CURRENT_RED`, establishing the original Dashboard Ticket-first bypass. CNX-368 repaired the schema-v2 Host authority compatibility gate. CNX-369 activated the repaired artifact. CNX-370 reproduced the bypass. CNX-371 established the Dashboard Gateway → embedded selection path. CNX-372 showed supported diagnostics did not expose the process-local runner hook state. CNX-373 proved the live admission configuration values. CNX-374 proved and repaired the plugin-definition conversation-hook registry gate. CNX-375 then performed exactly one controlled Dashboard semantic request on the repaired runtime and confirmed `FAIL / TICKET_FIRST_STILL_BYPASSED`: direct model inference occurred with no Ticket or admission trace evidence.

## Authorization boundary

Current successor: `CNX-20260917-376` — DASHBOARD HOOK DISPATCH BOUNDARY DIAGNOSIS. Diagnosis-first. Supported read-only/runtime observation comes first. If that evidence cannot distinguish the dispatch hypotheses, up to **2 additional Dashboard semantic requests** are authorized, each only for a distinct diagnostic purpose: one dispatch probe and, conditionally, one admission probe if handler invocation is proven but the Ticket-first decision remains unexplained. No identical retry is authorized.

No source repair is authorized unless a concrete causal defect is proven and the smallest justified repair is documented.

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
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-375.
- Stop and report if the dispatch boundary remains unproven.
- Do not start CNX-377 yourself.
