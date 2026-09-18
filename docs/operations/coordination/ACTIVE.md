# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX424_READY_FOR_HERMES`
Execution mode: `DUAL_SESSION_CROSS_ADAPTER_RUN_IDEMPOTENCY_REPAIR`
Task ID: `CNX-20260919-424`
Parent: `CNX-20260919-423`
Executor: `ChatGPT via LConnect / authorized repository executor`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Parent report: `docs/operations/coordination/reports/CNX-20260919-423-reply-dispatch-provenance-and-acp-identity-semantics-repair-report.md`
Parent review: `docs/operations/coordination/reviews/CNX-20260919-423-chatgpt-review.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260919-424-dual-session-cross-adapter-run-idempotency-repair.md`
Expected report: `docs/operations/coordination/reports/CNX-20260919-424-dual-session-cross-adapter-run-idempotency-repair-report.md`

## Current position

CNX-423 review decision:

`REJECT_READY__DUAL_SESSION_ADAPTER_IDEMPOTENCY_REPAIR_REQUIRED`

The provenance and ACP source/effective identity repairs are accepted, but one residual cross-adapter defect remains:

- bound ACP `reply_dispatch` admits with source owner session A;
- later `before_agent_run` can observe effective target session B;
- TicketStore persistent idempotency uses `ownerSessionKey + runId`;
- the same host run can therefore create two Tickets.

Reviewer RED observed:

`tickets = 2`

where the invariant requires:

`tickets = 1`

## Authorization

CNX-424 may begin immediately.

Authorized:

- RED characterization;
- minimal source repair;
- focused/broad regressions;
- OpenClaw 2026.9.4 target isolated qualification;
- report/coordination publication.

Not authorized:

- semantic provider sends;
- live OpenClaw upgrade/migration;
- live provider/model mutation;
- live plugin lifecycle mutation for upgrade;
- manual live Ticket/outbox/recovery/SQLite mutation;
- release/tag/main;
- force push/history rewrite.

## Required invariant

`ONE HOST RUN -> ONE TICKET -> ONE ROUTE EVENT`

even when source-owner and effective ACP dispatch sessions differ.
