# Coordination Channel Status

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

## Current authorization

CNX-383 is authorized for minimal repair at the proven hook-policy projection boundary.

The repair must preserve the already-declared policy and deliver it through the host `hookPolicy` path consumed by `registerTypedHook`.

No bypass of the host policy gate, no second registration path, and no admission/TicketStore redesign are authorized.

## TDD / validation

Establish RED with a focused regression reproducing CNX-382, implement the smallest justified repair, then establish GREEN.

Run relevant tests, plugin test suite, build, and validation after the fix. Runtime activation may follow only after source/build evidence is green and only to verify the effective artifact when necessary.

At most one Dashboard semantic probe is permitted only when supported runtime evidence cannot verify hook visibility and the report explicitly justifies it. No retry.

## Hard fences

No provider/auth/routing/model changes.
No TicketStore/admission redesign.
No Dashboard UI changes.
No controller normalization.
No speculative patch.
No broad refactor.
No bypass of host conversation-hook gate.
No second registration path.
No unrelated runtime mutation.
No release/tag/main.
No force-push/history rewrite.
No historical edits to CNX-360 through CNX-382.
Do not start CNX-384 yourself.

## Closeout

Required report:
`docs/operations/coordination/reports/CNX-20260917-383-hook-policy-projection-repair-report.md`

Classification:
`HOOK_POLICY_PROJECTION_REPAIRED`
`HOOK_POLICY_PROJECTION_REPAIR_BLOCKED`
`HOOK_POLICY_PROJECTION_REPAIR_INCONCLUSIVE`

After report publication, set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop.
