# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX422_READY_FOR_HERMES`
Execution mode: `REPLY_DISPATCH_TICKET_FIRST_REPAIR_AND_ISOLATED_OPENCLAW_2026_9_4_QUALIFICATION`
Task ID: `CNX-20260918-422`
Parent: `CNX-20260918-421`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Parent report: `docs/operations/coordination/reports/CNX-20260918-421-openclaw-current-upgrade-qualification-and-harness-agnostic-ticket-first-admission-report.md`
Parent review: `docs/operations/coordination/reviews/CNX-20260918-421-chatgpt-review.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260918-422-reply-dispatch-ticket-first-repair-and-openclaw-2026-9-4-isolated-qualification.md`
Expected report: `docs/operations/coordination/reports/CNX-20260918-422-reply-dispatch-ticket-first-repair-and-openclaw-2026-9-4-isolated-qualification-report.md`

## Current position

CNX-421 is accepted as:

`ACCEPTED_BLOCKED_CONTINUE_QUALIFICATION`

The blocker was incomplete execution, not a proven architectural dead end.

ChatGPT review independently re-checked the OpenClaw hook contracts and corrected one material interpretation:

- `reply_dispatch.event.runId` supplies the real dispatch run ID;
- `reply_dispatch.event.ctx` is `FinalizedMsgContext`;
- the context exposes inbound message text and Gateway trust/session identity;
- OpenClaw v2026.9.4 additionally exposes `InboundAccessAuthorized`, an explicit ingress authorization proof.

Therefore `reply_dispatch` is now the leading harness-agnostic, run-correlated pre-model Ticket admission seam.

Target:

`reply_dispatch -> shared Ticket admission kernel -> Ticket accept/route -> OpenClaw-selected harness/provider/model`

Retain `before_agent_run` as defense-in-depth/idempotency for supported runners.

## Current authorization

Hermes may begin CNX-422 immediately.

Authorized:

- RED characterization tests;
- minimal repository source repair after RED;
- GREEN/regression tests;
- plugin build/typecheck;
- isolated OpenClaw v2026.9.4 SDK/runtime qualification;
- fresh and copied-state migration characterization;
- repository commits/pushes on the working branch.

Not authorized:

- semantic provider sends;
- browser mutation;
- live OpenClaw upgrade;
- live state/session migration;
- live provider/model mutation;
- live plugin install-over/uninstall;
- live Gateway restart for upgrade;
- manual live Ticket/outbox/recovery/SQLite mutation;
- release/tag/main;
- force push/history rewrite.

## Required invariant

For eligible external owner turns:

`NO TICKET = NO MODEL EXECUTION`

OpenClaw remains authoritative for provider, model, fallback, session overrides, and harness selection.

## Closeout

Publish the CNX-422 report, set ACTIVE.md and STATUS.md to `WAITING_FOR_CHATGPT_REVIEW`, verify local HEAD equals remote HEAD and a clean publication worktree, then stop. Do not perform the live upgrade or create its successor before ChatGPT review.
