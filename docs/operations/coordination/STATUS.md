# Coordination Channel Status

Status: `READY_FOR_HERMES`
State: `CNX420_OPERATOR_FRESH_SESSION_ROUTE_TICKET_FIRST_DISCRIMINATION`
Execution mode: `OPERATOR_ASSISTED_TWO_STAGE_SEMANTIC_ACCEPTANCE`
Task ID: `CNX-20260918-420`
Parent: `CNX-20260918-419`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Parent report: `docs/operations/coordination/reports/CNX-20260918-419-preserved-draft-enter-submit-ollama-ticket-first-report.md`
Parent review: `docs/operations/coordination/reviews/CNX-20260918-419-chatgpt-review.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260918-420-operator-fresh-session-ollama-route-ticket-first-discrimination.md`

## Current position

CNX-419 is reviewed and accepted as failed with:

- primary: `BLOCKED_TICKET_FIRST_ORDERING`;
- secondary: `BLOCKED_SELECTED_ROUTE_NOT_HONORED`.

The Operator observed that after refreshing the browser, the UI showed `openai/gpt-5.6-luna`, raising a plausible stale-browser/session-presentation hypothesis for the earlier pre-send Ollama label.

The Operator has explicitly authorized one new diagnostic semantic turn using a completely fresh Operator-created Dashboard session.

## Required interaction model

Hermes must first perform Stage-1 read-only preflight and baseline capture.

If preflight is GREEN, Hermes must **stop and tell the Operator** to:

1. refresh the Dashboard page;
2. click New Session;
3. select Ollama / `qwen3.8:27b`;
4. enter the exact nonce prompt supplied by Hermes;
5. verify the UI shows `qwen3.8:27b`;
6. send exactly once manually;
7. return to Hermes and say `ส่งแล้ว`.

Hermes must not perform any browser mutation and must not continue to post-send inspection until the Operator explicitly says `ส่งแล้ว`.

While waiting, coordination may be moved to `WAITING_FOR_OPERATOR_ACTION`.

## Current authorization

CNX-420 is READY for Hermes Stage 1 only.

The Operator is **not yet instructed to send** until Hermes reports preflight GREEN and supplies the fresh nonce.

## Hard fences

- Hermes browser mutation: 0.
- Hermes New Session: 0.
- Hermes provider/model selection: 0.
- Hermes typing/send/key action: 0.
- Operator New Session: exactly 1 after Hermes instruction.
- Operator semantic send: max 1 after Hermes instruction.
- semantic retry/resend: 0.
- direct provider/model probes: 0.
- provider/model config mutation by executor: 0.
- manual Ticket/outbox/recovery/SQLite mutation: 0.
- Gateway restart/reload/repair: 0.
- plugin lifecycle mutation: 0.
- installer/install-over: 0.
- lifecycle start/stop/restart: 0.
- production source repair: 0.
- release/tag/main: 0.
- force push/history rewrite: 0.
- do not create/start CNX-421.

## Closeout

After the Operator says `ส่งแล้ว`, collect read-only post-send evidence, publish the CNX-420 report, set ACTIVE.md and STATUS.md to `WAITING_FOR_CHATGPT_REVIEW`, verify local HEAD equals remote HEAD and clean publication worktree, and stop.
