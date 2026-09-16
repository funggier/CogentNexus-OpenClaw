# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX377_COMPOSED_HOOK_REGISTRY_WIRING_REPAIR`
Execution mode: `ROOT_CAUSE_TDD_COMPOSED_REGISTRY_REPAIR`
Task ID: `CNX-20260917-377`
Parent: `CNX-20260917-376`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-376-dashboard-hook-dispatch-boundary-diagnosis-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-377-composed-registry-wiring-repair.md`

## Current position

CNX-367 proved the Dashboard Ticket-first bypass. CNX-368 repaired the schema-v2 Host authority gate. CNX-369 activated the repaired artifact. CNX-370 reproduced the bypass. CNX-371 established the Dashboard Gateway → embedded selection path. CNX-372 showed supported diagnostics did not expose process-local runner hook state. CNX-373 proved live admission configuration. CNX-374 repaired the plugin-definition conversation-hook access gate. CNX-375 confirmed the Dashboard bypass remained end-to-end. CNX-376 proved the dispatch boundary: plugin-level registration exists, but the host composed registry exposes `hookCount: 0`, causing `hasHooks("before_agent_run")` to return false and skip dispatch.

## Next authorized task

`CNX-20260917-377` is authorized to diagnose and minimally repair the exact composed-registry wiring defect proven by CNX-376.

The task must identify the concrete registry instance/composition lifecycle mechanism before changing source. It may add a focused RED/GREEN regression and the smallest justified repair. Runtime activation may follow validated source/build evidence if needed.

## Authorization boundary

No Dashboard semantic request is authorized by default. At most one semantic probe may be used only when read-only/runtime evidence cannot verify the repaired registry composition and the report documents the specific reason. No retry.

No TicketStore, admission, provider/auth/routing/model, or Dashboard UI repair is authorized.

## Hard fences

- Root-cause investigation before repair.
- No speculative patch.
- No TicketStore redesign.
- No admission redesign.
- No provider/auth/routing/model changes.
- No Dashboard UI/provider-layer changes.
- No controller normalization.
- No unrelated runtime mutation.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-376.
- Do not start CNX-378 yourself.
