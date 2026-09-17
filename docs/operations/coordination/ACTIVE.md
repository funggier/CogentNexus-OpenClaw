# Active Coordination Task

Status: `WAITING_FOR_CHATGPT_REVIEW`
State: `CNX383_HOOK_POLICY_PROJECTION_REPAIR_BLOCKED`
Execution mode: `ROOT_CAUSE_TDD_HOOK_POLICY_PROJECTION_REPAIR`
Task ID: `CNX-20260917-383`
Parent: `CNX-20260917-382`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-382-plugin-hook-policy-projection-trace-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-383-hook-policy-projection-repair.md`

## Current position

CNX-383 is blocked at the proven host projection boundary. The focused regression reproduced the loss, but the required projection owner is the OpenClaw loader dependency, not plugin source. No prohibited dependency patch or gate bypass was made. See `docs/operations/coordination/reports/CNX-20260917-383-hook-policy-projection-repair-report.md`.

CNX-382 proved `HOOK_POLICY_PROJECTION_LOSS_PROVEN`: the executable CogentNexus definition contains `hooks.allowConversationAccess=true`, but `definePluginEntry` does not preserve that property and the loader's `entry = normalized.entries[pluginId]` supplies `entry?.hooks` to `createApi` instead of the executable definition's hooks. The host non-bundled conversation-hook gate therefore rejects `before_agent_run` before registry storage.

## Next authorized task

`CNX-20260917-383` is authorized to make the smallest source repair that preserves/projects the already-declared hook policy into the host `hookPolicy` path consumed by `registerTypedHook`.

Repair is authorized only at the proven boundary. The repair must not bypass the host gate, add a second registration path, or alter TicketStore/admission semantics.

## Authorization boundary

Diagnosis is complete. Minimal source repair is authorized.

No provider/auth/routing/model changes.
No TicketStore/admission redesign.
No Dashboard UI changes.
No broad refactor.
No force-push/history rewrite.
No main/release/tag.
No historical edits to CNX-360 through CNX-382.
Do not start CNX-384 yourself.

## TDD / validation

Hermes must establish RED with a focused regression reproducing CNX-382, implement the smallest justified repair, then establish GREEN.

After GREEN run relevant existing tests, plugin tests, build, and validation. Runtime activation may occur only after source/build evidence is green and only as needed to verify the effective artifact.

A single Dashboard semantic probe is permitted only when runtime hook visibility cannot otherwise be verified and the report explicitly justifies it. No retry.

## Closeout

Create:
`docs/operations/coordination/reports/CNX-20260917-383-hook-policy-projection-repair-report.md`

Then set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop.
