# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX374_PLUGIN_HOOK_REGISTRY_WIRING_DIAGNOSIS`
Execution mode: `SUPPORTED_PLUGIN_REGISTRY_WIRING_DIAGNOSIS`
Task ID: `CNX-20260916-374`
Parent: `CNX-20260916-373`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260916-373-conversation-hook-access-gate-repair-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260916-374-plugin-hook-registration-registry-wiring.md`

## Current position

CNX-367 proved the Dashboard Ticket-first bypass as `CURRENT_RED`. CNX-368 repaired the schema-v2 Host authority compatibility gate and verified source/test/build behavior. CNX-369 activated and verified the repaired artifact in the live Gateway process. CNX-370 reproduced the bypass semantically. CNX-371 established the Dashboard Gateway → embedded selection path but could not prove the runtime hook-registry condition. CNX-372 established that supported runtime diagnostics expose the plugin as loaded/enabled but do not expose the process-local hook registry or `runBeforeAgentRun` invocation state. CNX-373 proved `allowConversationAccess=true`, `ticketFirst=true`, `preInferenceAdmission=true`, and `enforcedMode=true` in the authoritative live config without mutation.

## Next authorized task

`CNX-20260916-374` is authorized to diagnose the exact plugin hook registration → host hook registry wiring boundary. It must determine whether the dynamically registered `before_agent_run` handler reaches the registry consumed by the Dashboard selection runner, whether registration timing/reference identity is broken, or whether the host requires additional registration metadata/declaration.

Only after a concrete cause is proven may the task implement the smallest justified source repair and focused regression coverage.

## Authorization boundary

This task explicitly authorizes diagnosis, and conditional minimal source repair only after diagnosis proves the causal registration/registry mechanism. Supported runtime activation may be used after validated repair if required. Semantic Dashboard requalification is not authorized by default and should be deferred to a separate successor task.

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
