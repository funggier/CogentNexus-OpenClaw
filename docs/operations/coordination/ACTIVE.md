# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_DASHBOARD_SINGLE_SEND_DURABLE_DELIVERY_REACCEPTANCE`
Current authorization: `CNX-20260830-160_DASHBOARD_SINGLE_SEND_DURABLE_DELIVERY_REACCEPTANCE`
Task ID: `CNX-20260830-160`
Updated: 2026-08-30 ICT
Owner / coordinator / reviewer: ChatGPT
Executor: Hermes on the operator's real Windows/OpenClaw environment

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260830-160-dashboard-single-send-durable-delivery-reacceptance.md`](tasks/CNX-20260830-160-dashboard-single-send-durable-delivery-reacceptance.md)

## Accepted prerequisite

Task 159 is durably reviewed `ACCEPT`:

`docs/operations/coordination/reviews/CNX-20260830-159-windows-diagnostic-install-over-retry-review.md`

Task-159 review commit:

`138b5d3f9509ec42ec00b6fa701a7c2b02e2ab3f`

The repaired candidate is proven installed with matching provenance and healthy managed/plugin/gateway state. Task-159 Dashboard semantic Sends were `0`.

## Task-160 execution contract

Hermes must:

1. fresh-check installed candidate provenance and live health before semantic interaction;
2. if the pre-Send gate fails, stop `BLOCKED` with semantic Sends = `0`;
3. if the gate passes, submit exactly one benign Dashboard semantic message specified by Task 160;
4. never retry or submit a second semantic message, even on timeout/failure/ambiguity;
5. correlate the one Send to its durable Ticket/run/generation/result/delivery evidence using read-only tooling;
6. reconcile visible Dashboard output with durable authoritative result and settlement state;
7. collect bounded relevant logs and post-send health;
8. publish the Task-160 report/evidence and STOP for ChatGPT review.

## Exactly-one Send fence

Maximum authorized semantic Dashboard Sends after a valid pre-Send gate: `1`.

No second Send, semantic retry, follow-up, replay, duplicate callback injection, manual Ticket/workflow/result/outbox/delivery/database mutation, reset, install-over, uninstall, reinstall, source patch, dependency upgrade, OpenClaw patch, release/promotion, or force push.

## Required report

`docs/operations/coordination/reports/CNX-20260830-160-dashboard-single-send-durable-delivery-reacceptance.md`

After report/evidence publication Hermes must STOP. Task-160 PASS is not final until ChatGPT fresh-reads and reviews the durable evidence.
