# Active Coordination Task

Status: `WAITING_FOR_CHATGPT_REVIEW`
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

## Current position

CNX-384 confirmed that the projection owner is the OpenClaw loader dependency, but the repository has no existing tracked, clean-install-reproducible host dependency patch/vendor/override mechanism. The repair is blocked without inventing a new broad dependency architecture. Report: `docs/operations/coordination/reports/CNX-20260917-384-host-hook-policy-projection-repair-report.md`.

## Next authorized task

No successor task is started. Await ChatGPT review of CNX-384.

The repair must preserve the existing host conversation-hook policy gate. No bypass, second registration path, or admission/TicketStore change is allowed.

## Authorization boundary

Diagnosis is complete. Bounded host-side repair is authorized.

No provider/auth/routing/model changes.
No TicketStore/admission redesign.
No Dashboard UI changes.
No unrelated OpenClaw changes.
No broad refactor.
No force-push/history rewrite.
No main/release/tag.
No historical edits to CNX-360 through CNX-383.
Do not start CNX-385 yourself.

## TDD / validation

Hermes must establish RED at the exact host projection boundary, implement the smallest justified host-side repair, then establish GREEN.

If the repair requires OpenClaw dependency changes, the chosen mechanism must be repository-tracked and reproducible by clean install. Hand-editing node_modules alone is not acceptable.

After GREEN, run relevant existing/plugin tests, build, and validation. Runtime activation is allowed only after source/build/test evidence is green and only when needed to verify effective runtime hook visibility.

At most one Dashboard semantic probe is permitted only if supported runtime evidence cannot verify hook visibility. No retry.

## Closeout

Create:
`docs/operations/coordination/reports/CNX-20260917-384-host-hook-policy-projection-repair-report.md`

Then set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop.
