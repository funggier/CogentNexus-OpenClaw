# Coordination Channel Status

Status: `READY_FOR_HERMES`
State: `CNX377_COMPOSED_HOOK_REGISTRY_WIRING_REPAIR`
Task ID: `CNX-20260917-377`
Parent: `CNX-20260917-376`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-376-dashboard-hook-dispatch-boundary-diagnosis-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-377-composed-registry-wiring-repair.md`

## Current position

CNX-367 completed as `CURRENT_RED`; CNX-368 repaired the schema-v2 Host authority gate; CNX-369 activated the repaired artifact; CNX-370 reproduced the Dashboard bypass; CNX-371 established the Gateway → embedded selection path; CNX-372 showed supported diagnostics did not expose process-local runner hook state; CNX-373 proved live admission configuration; CNX-374 repaired the plugin-definition conversation-hook gate; CNX-375 confirmed Ticket-first remained bypassed end-to-end; CNX-376 proved the next dispatch boundary: plugin-level hook registration is present but host composed-registry visibility is absent (`hookCount: 0`, `hookNames: []`), causing `hasHooks("before_agent_run")` to return false and skip dispatch.

## Authorization boundary

Current task: `CNX-20260917-377` — COMPOSED HOOK REGISTRY WIRING REPAIR.

Diagnosis-first. Hermes must prove the concrete registry instance/composition lifecycle defect before source repair. Minimal TDD regression and smallest justified repair are authorized. Runtime activation may follow green source/build evidence when necessary.

No Dashboard semantic request is authorized by default. At most one semantic probe may be used only when read-only/runtime evidence cannot verify the repaired composed registry and the report documents why it is necessary. No retry.

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
- Stop and report if the composed-registry mechanism remains unproven.
- Do not start CNX-378 yourself.
