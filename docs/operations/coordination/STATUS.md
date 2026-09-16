# Coordination Channel Status

Status: `READY_FOR_HERMES`
State: `CNX373_CONVERSATION_HOOK_ACCESS_GATE_REPAIR`
Task ID: `CNX-20260916-373`
Parent: `CNX-20260916-372`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260916-372-selection-runner-hook-registry-runtime-observation-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260916-373-conversation-hook-access-gate-repair.md`

## Current position

CNX-367 completed as `CURRENT_RED`, with the Dashboard path proven to bypass Ticket-first admission. CNX-368 completed as `REPAIRED / VERIFIED` at source/test/build level and fixed the schema-v2 Host authority compatibility mismatch that suppressed plugin registration. CNX-369 activated and verified the repaired artifact in the live Gateway process. CNX-370 completed as `FAIL / NOT REQUALIFIED`. CNX-371 established the Dashboard Gateway → embedded selection path but could not prove the runtime hook-registry condition. CNX-372 established that supported runtime diagnostics expose the plugin as loaded/enabled but do not expose the process-local hook registry or `runBeforeAgentRun` invocation state.

Existing repository evidence shows `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true` was a managed lifecycle configuration requirement in prior managed operation. CNX-373 must verify the current live effective value before any change.

## Authorization boundary

Current successor: `CNX-20260916-373` — CONVERSATION HOOK ACCESS GATE VERIFICATION AND MINIMAL REPAIR. This task is explicitly authorized for bounded live configuration diagnosis and, only if the live effective configuration proves that conversation-hook access is denied or missing under current host defaults, the smallest supported configuration repair to set `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true`, deterministic validation, and supported runtime activation if required.

A semantic Dashboard request is not authorized by default. If the permission is already granted, no configuration change is authorized by this task and Hermes must publish the negative finding and stop.

## Hard fences

- No provider/auth/routing/model changes.
- No semantic-contract changes.
- No Dashboard UI or provider-layer changes.
- No changes to `durableAdmissionEligible()` or TicketStore merely to affect the result.
- No duplicate Ticket admission path.
- No manual controller normalization.
- No broad refactor.
- No historical edits to CNX-360 through CNX-372.
- No release/tag/main changes.
- No force-push or history rewrite.
- No guessed repair.
- No semantic requalification by default.
- If `allowConversationAccess=true` is proven, do not alter it and stop with the evidence.
- If the effective value cannot be proven, stop as `INCONCLUSIVE`.
- After publishing the CNX-373 report, transition to `WAITING_FOR_CHATGPT_REVIEW` and stop.
