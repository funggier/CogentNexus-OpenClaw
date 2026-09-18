# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX423_READY_FOR_HERMES`
Execution mode: `REPLY_DISPATCH_PROVENANCE_AND_ACP_IDENTITY_SEMANTICS_REPAIR`
Task ID: `CNX-20260919-423`
Parent: `CNX-20260918-422`
Executor: `Hermes / authorized repository executor`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Parent report: `docs/operations/coordination/reports/CNX-20260918-422-reply-dispatch-ticket-first-repair-and-openclaw-2026-9-4-isolated-qualification-report.md`
Parent review: `docs/operations/coordination/reviews/CNX-20260918-422-chatgpt-review.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260919-423-reply-dispatch-provenance-and-acp-identity-semantics-repair.md`
Expected report: `docs/operations/coordination/reports/CNX-20260919-423-reply-dispatch-provenance-and-acp-identity-semantics-repair-report.md`

## Current position

CNX-422 review decision:

`REJECT_READY__ADMISSION_SEMANTICS_REPAIR_REQUIRED`

The v2026.9.4 migration/rollback/build evidence remains useful, but controlled live-upgrade readiness is withdrawn pending two narrow admission repairs:

1. classify `InputProvenance` / internal control paths before trust fallback so restart recovery, inter-session and subagent completion are not admitted as new owner intent;
2. distinguish source owner session from effective ACP dispatch session so legitimate bound ACP retargeting is not treated as contradictory identity.

## Authorization

CNX-423 may begin immediately.

Authorized:

- RED characterization tests;
- minimal repository source repair after RED;
- focused and broad regression tests;
- OpenClaw v2026.9.4 target build/isolated fresh runtime qualification;
- report/coordination commits and fast-forward push on the working branch.

Not authorized:

- semantic provider sends;
- external provider probes;
- live OpenClaw upgrade or migration;
- live provider/model mutation;
- live plugin lifecycle mutation for upgrade;
- manual live Ticket/outbox/recovery/SQLite mutation;
- release/tag/main;
- force push/history rewrite.

## Required invariant

For eligible external owner turns:

`NO TICKET = NO MODEL EXECUTION`

Internal/control/recovery/inter-session turns must preserve host authority and must not become fresh owner Tickets.

## Closeout

Publish the CNX-423 report, set ACTIVE.md and STATUS.md to `WAITING_FOR_CHATGPT_REVIEW`, verify exact local/remote HEAD and clean worktree, then stop before any live upgrade.
