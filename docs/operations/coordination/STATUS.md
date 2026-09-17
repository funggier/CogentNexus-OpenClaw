# Coordination Channel Status

Status: `READY_FOR_HERMES`
State: `CNX384_HOST_HOOK_POLICY_PROJECTION_REPAIR`
Execution mode: `ROOT_CAUSE_TDD_HOST_HOOK_POLICY_PROJECTION_REPAIR`
Task ID: `CNX-20260917-384`
Parent: `CNX-20260917-383`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-383-hook-policy-projection-repair-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-384-host-hook-policy-projection-repair.md`

## Outcome to date

CNX-383 was blocked because the proven projection owner is the OpenClaw loader dependency. CNX-382 established the projection loss: executable `releaseEntry.hooks.allowConversationAccess=true` is not the object used by the loader's `entry?.hooks` policy path.

## Current authorization

CNX-384 is authorized for the smallest reproducible host-side repair at the proven hook-policy projection boundary. A dependency change is permitted only at this boundary and only through a repository-tracked, clean-install-reproducible mechanism.

The existing host policy gate must remain intact. No bypass, second registration path, or admission/TicketStore redesign is authorized.

## TDD / validation

Establish RED at the exact projection boundary, implement the minimal host-side repair, then establish GREEN. After GREEN run relevant tests, plugin suite, build, and validation. Runtime activation is permitted only after green evidence and only if required to verify effective hook visibility.

At most one Dashboard semantic probe may be used only if supported runtime evidence cannot verify hook visibility. No retry.

## Hard fences

No provider/auth/routing/model changes.
No TicketStore/admission redesign.
No Dashboard UI changes.
No unrelated OpenClaw changes.
No broad refactor.
No speculative changes outside the proven boundary.
No bypass of host policy gate.
No second registration path.
No force-push/history rewrite.
No release/tag/main.
No historical edits to CNX-360 through CNX-383.
Do not start CNX-385 yourself.

## Closeout

Required report:
`docs/operations/coordination/reports/CNX-20260917-384-host-hook-policy-projection-repair-report.md`

Classification:
`HOST_HOOK_POLICY_PROJECTION_REPAIRED`
`HOST_HOOK_POLICY_REPAIR_BLOCKED`
`HOST_HOOK_POLICY_REPAIR_INCONCLUSIVE`

After report publication, set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop.
