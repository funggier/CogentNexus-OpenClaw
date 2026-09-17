# Coordination Channel Status

Status: `READY_FOR_HERMES`
State: `CNX385_NORMALIZED_HOOK_POLICY_INPUT_PATH_DIAGNOSIS`
Execution mode: `NORMALIZED_HOOK_POLICY_INPUT_PATH_DIAGNOSIS`
Task ID: `CNX-20260917-385`
Parent: `CNX-20260917-384`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-384-host-hook-policy-projection-repair-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-385-normalized-hook-policy-input-path-diagnosis.md`

## Current authorization

CNX-385 is authorized for diagnosis only. Trace the raw `plugins.entries.<id>.hooks` configuration through schema validation and normalization into `normalized.entries[pluginId].hooks`, then into `createApi(hookPolicy)`. Determine whether the field is intentionally stripped/transformed and whether an existing supported plugin/configuration/install extension point can preserve it without patching OpenClaw or inventing a new dependency architecture.

No production mutation. No repair.

## Hard fences

- No production Gateway restart/reload.
- No production configuration mutation.
- No OpenClaw dependency patch.
- No CogentNexus source repair.
- No artifact deployment/rebuild.
- No semantic/model requests.
- No TicketStore/admission/provider/model/auth/routing/Dashboard UI changes.
- No speculative workaround.
- No new dependency architecture.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-384.
- Do not start CNX-386 yourself.

## Closeout

Required report:
`docs/operations/coordination/reports/CNX-20260917-385-normalized-hook-policy-input-path-diagnosis-report.md`

Classification:
`NORMALIZED_HOOK_POLICY_STRIPPING_PROVEN`
`NORMALIZED_HOOK_POLICY_PRESERVED_HOST_CONTRACT_FOUND`
`NORMALIZED_HOOK_POLICY_INPUT_PATH_UNRESOLVED`
`NORMALIZED_HOOK_POLICY_DIAGNOSTICALLY_BLOCKED`

After report publication, set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop.
