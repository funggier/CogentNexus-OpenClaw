# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_DASHBOARD_DURABLE_DELIVERY_ACCEPTANCE_ONLY`
Current authorization: `CNX-20260829-136_FINAL_DASHBOARD_DURABLE_DELIVERY_ACCEPTANCE`
Task ID: `CNX-20260829-136`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-136-final-dashboard-durable-delivery-acceptance.md`](tasks/CNX-20260829-136-final-dashboard-durable-delivery-acceptance.md)

Task 136 is the final real OpenClaw Dashboard durable-delivery acceptance. It authorizes exactly one new benign semantic Dashboard message and exactly one submission activation. After that single Send, no resend or alternate semantic transport is permitted; durable Ticket/event/result/outbox/delivery evidence becomes authoritative.

## Accepted prerequisite chain

Accepted source candidate:

`1424d6fbee2c458c8c30440616783d2fa1bc1201`

Accepted payload/plugin fingerprint:

`3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

Task 134 independently accepted the complete one-shot real-Windows recovery suite. Its live ledger is consumed and must never be replayed.

Task 135 independently accepted the post-recovery zero delivery baseline:

- managed/Ollama;
- recovery `READY`;
- delivery `READY`;
- SQLite integrity `ok`;
- `pendingOutbox=0`;
- `nonterminalTickets=0`;
- no unresolved workflow/direct-recovery/assistant-delivery/outbound-send residue;
- no Dashboard semantic Send under Tasks 134/135.

Task-135 independent review:

`docs/operations/coordination/reviews/CNX-20260829-135-post-recovery-delivery-residue-readonly-closeout-review.md`

## Task 136 single-send rule

Before Send, require a fresh already-safe zero baseline through the explicit installed launcher/root and SQLite URI `mode=ro`. Unsafe or ambiguous preflight => `BLOCKED`; do not normalize.

Generate one fresh non-secret nonce and verify it does not already exist in durable records. Compose one short benign message asking for `ACK <nonce>`.

Use the real OpenClaw Dashboard conversation UI only. Perform exactly one submission activation. Immediately consume the Task-136 Send ledger `1 / 1`.

**Never resend after the first activation**, including when UI is ambiguous, reconnecting, stalled, or missing an immediate reply. No CLI/Gateway/API/database semantic injection is allowed.

After Send, prove read-only:

- exactly one new Ticket for the nonce;
- durable Ticket commit precedes inference/model execution;
- one coherent execution/workflow chain;
- successful terminal Ticket/result/validator state;
- one logical outbox/delivery chain;
- terminal acknowledged/delivered state;
- no duplicate external delivery/side effect;
- final `pendingOutbox=0` and `nonterminalTickets=0`;
- final managed/Ollama recovery+delivery READY and SQLite integrity `ok`.

If the one message fails to converge within the task's bounded observation window, fail-stop. No resend, retry, cleanup, lifecycle/recovery, or normalization is authorized.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-136-final-dashboard-durable-delivery-acceptance.md`

Then stop for independent ChatGPT review.

Do not merge, tag, create a GitHub Release, or automatically open a finalization task.

## Hard fence

Other than the one explicitly authorized Dashboard semantic submission: no second Send/resend; no alternate semantic injection; no source/runtime/plugin edit; no install/install-over/reset/uninstall/reinstall; no start/stop/restart/enable/disable; no recovery/crash injection; no provider/model/OpenClaw/config mutation; no manual Ticket/workflow/outbox/ack mutation; no SQLite write/cleanup; no process kill; no task/service mutation; no normalization; no reboot; no credentials/secrets; no merge/tag/release; no force push.
