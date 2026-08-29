# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `OFFLINE_SOURCE_TDD_DIAGNOSIS_AND_REPAIR_ONLY`
Current authorization: `CNX-20260829-138_DASHBOARD_DIRECT_RESULT_DURABLE_CAPTURE_REPAIR`
Task ID: `CNX-20260829-138`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-138-dashboard-direct-result-durable-capture-repair.md`](tasks/CNX-20260829-138-dashboard-direct-result-durable-capture-repair.md)

Task 138 is an offline source TDD diagnosis-and-repair task for the clean Task-137 Dashboard direct-result durable-capture failure. It does not authorize another live Dashboard semantic Send or any live Windows runtime mutation.

## Task-137 disposition

Task-137 report:

`docs/operations/coordination/reports/CNX-20260829-137-final-dashboard-durable-delivery-reacceptance.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-137-final-dashboard-durable-delivery-reacceptance-review.md`

Task 137 is independently **ACCEPTED as a clean `FAIL_PRODUCT_OR_RUNTIME`**. It proved one exact Dashboard Send, Ticket-first admission, one completed direct model call, an exact visible ACK, durable `response_ready`, then terminal `failed` plus `failure_delivery_suppressed` because the final payload was not durably captured.

The Task-137 Send ledger is permanently consumed `1 / 1`. Its nonce/Ticket must never be resent, retried, deleted, cleaned, or normalized.

The defect class is confirmed at the Dashboard direct final-payload durable capture / delivery-verification boundary. The exact source-level root cause remains unproven until Task 138 obtains a deterministic offline RED reproducer.

## Accepted baseline before repair

Accepted source candidate before Task 138:

`1424d6fbee2c458c8c30440616783d2fa1bc1201`

Accepted installed payload/plugin fingerprint before Task 138:

`3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

Branch history after the accepted candidate through the Task-137 report changed coordination documentation only; no production source drift was identified before Task 138 opened.

## Task-138 execution contract

Task 138 must use TDD and the narrowest justified repair:

1. fresh-fetch authority and record exact starting HEAD;
2. inspect the registered Dashboard delivery hook/callback path and existing tests;
3. create a deterministic regression reproducer through the registered runtime delivery boundary;
4. capture genuine **RED** evidence before editing production source;
5. identify the exact source-level root cause from that reproducer rather than preselecting a hypothesis;
6. apply the minimum production fix while preserving Ticket-first, session generation fencing, durable-before-transport, stable idempotency, exactly-once delivery semantics, and fail-closed duplicate prevention;
7. obtain **GREEN** on the new regression, existing Dashboard verified-delivery and response-ready boundary tests, directly affected delivery/recovery tests, full plugin tests, build, plugin validation, and relevant CI;
8. publish the exact Task-138 report and stop for independent ChatGPT review.

If a deterministic RED reproducer cannot be established, do not guess a source fix. Report `BLOCKED_DIAGNOSTIC_EVIDENCE_GAP` with the narrowest additional diagnostic recommendation.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-138-dashboard-direct-result-durable-capture-repair.md`

Then stop for independent ChatGPT review.

Do not automatically install the repaired candidate, retry the Dashboard acceptance, merge, tag, or create a GitHub Release.

## Hard fence

Task 138 authorizes repository/source/test/CI work only.

Forbidden: live Dashboard semantic Send/resend; Task-136/137 semantic reuse; alternate live semantic injection; install/install-over/reset/uninstall/reinstall; live start/stop/restart/enable/disable; recovery/crash injection; provider/model/OpenClaw/config mutation; manual Ticket/outbox/delivery/ack mutation; live SQLite cleanup/normalization/write; process kill; scheduled-task/service mutation; reboot; credentials/secrets; merge/tag/release; force push.
