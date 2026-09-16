# Active Coordination Task

Status: `WAITING_FOR_CHATGPT_REVIEW`
State: `CNX373_CONVERSATION_HOOK_ACCESS_GATE_REPAIR`
Execution mode: `SUPPORTED_CONFIG_DIAGNOSIS_AND_MINIMAL_REPAIR`
Task ID: `CNX-20260916-373`
Parent: `CNX-20260916-372`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260916-372-selection-runner-hook-registry-runtime-observation-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260916-373-conversation-hook-access-gate-repair.md`

## Current position

CNX-367 proved the Dashboard Ticket-first bypass as `CURRENT_RED`. CNX-368 repaired the schema-v2 Host authority compatibility gate and verified source/test/build behavior. CNX-369 activated and verified the repaired artifact in the live Gateway process. CNX-370 reproduced the bypass semantically. CNX-371 established the Dashboard Gateway → embedded selection path but could not prove the runtime hook-registry condition. CNX-372 established that supported runtime diagnostics expose the plugin as loaded/enabled but do not expose the process-local hook registry or `runBeforeAgentRun` invocation state.

Existing repository evidence shows `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true` was a managed lifecycle configuration requirement in prior managed operation. CNX-373 must verify the current live effective value before any change.

## Next authorized task

`CNX-20260916-373` is authorized to diagnose whether OpenClaw's conversation-hook access gate is preventing the non-bundled CogentNexus plugin from participating in `before_agent_run`. If and only if the live effective configuration proves the access gate is denied/missing under the current host defaults, Hermes may apply the smallest supported configuration repair to set `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true`, validate it, and use the supported runtime activation mechanism if required.

If the permission is already granted, no configuration change is authorized by this task; publish the negative finding and stop.

## Authorization boundary

This task explicitly authorizes bounded live config diagnosis, conditional minimal config repair, deterministic validation, and supported runtime activation if required. It does not authorize semantic Dashboard requalification by default.

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
