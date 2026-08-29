# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_DASHBOARD_DURABLE_DELIVERY_REACCEPTANCE_ONLY`
Current authorization: `CNX-20260829-137_FINAL_DASHBOARD_DURABLE_DELIVERY_REACCEPTANCE`
Task ID: `CNX-20260829-137`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-137-final-dashboard-durable-delivery-reacceptance.md`](tasks/CNX-20260829-137-final-dashboard-durable-delivery-reacceptance.md)

Task 137 is one new clean real-Dashboard durable-delivery re-acceptance. It does not repair production source. It preserves Task-136 history and creates a fresh semantic ledger with one new nonce and maximum one new Dashboard submission activation.

## Task-136 disposition

Task-136 report:

`docs/operations/coordination/reports/CNX-20260829-136-final-dashboard-durable-delivery-acceptance.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-136-final-dashboard-durable-delivery-acceptance-review.md`

Task 136 is accepted as an acceptance FAIL but invalidated for product-root-cause conclusions because the run contained:

- one accidentally interrupted Hermes execution disclosed by the operator;
- a Dashboard composer/user-bubble duplication anomaly;
- a written 10-minute observation bound shorter than the run's own approximately 14m10s model call and shorter than known local `qwen3.5:9b` first-response behavior.

Task-136 Send ledger remains consumed `1 / 1`; its nonce/Ticket must never be resent, deleted, retried, cleaned, or normalized.

## Accepted candidate

Accepted source candidate:

`1424d6fbee2c458c8c30440616783d2fa1bc1201`

Accepted installed payload/plugin fingerprint:

`3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

No production reinstall/source repair is authorized before Task 137.

## Task-137 execution contract

Before Send, use the explicit installed launcher/root and a fresh read-only delta baseline. Historical Task-136 failed records are allowed and must remain intact; require no active/nonterminal/pending semantic work and require managed/Ollama, recovery READY, delivery READY, SQLite integrity `ok`, healthy Gateway/Ollama, exact plugin fingerprint, and unchanged accepted runtime identity.

Generate a fresh Task-137 nonce and prove it is absent from historical durable state.

In the real OpenClaw Dashboard composer:

- clear stale draft text if needed;
- compose exactly one intended Task-137 message;
- verify immediately before Send that the full message is not duplicated;
- perform exactly one deliberate Send activation;
- consume the Task-137 ledger `1 / 1` immediately;
- never resend or use alternate semantic transport.

After Send, ordinary local-model slowness is not failure. Read-only observation is allowed up to **45 minutes from activation** unless a clear durable terminal result arrives earlier. Do not stop Hermes because the first response is slow.

If Hermes/Codex is externally interrupted after Send, classify `INVALIDATED_AFTER_SEND`; do not call that product failure from this run alone and never resend. If interruption occurs before Send, classify `BLOCKED_BEFORE_SEND` with the ledger unconsumed.

A clean PASS still requires exactly one new Ticket, Ticket-before-inference, one coherent execution/result/validator chain, requested ACK semantics, one durable delivered/acknowledged logical delivery, no duplicate external side effect, zero pending/nonterminal residue after success, and coherent final runtime/recovery/delivery/SQLite/model state.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-137-final-dashboard-durable-delivery-reacceptance.md`

Then stop for independent ChatGPT review.

Do not merge, tag, create a GitHub Release, or automatically open release/finalization work.

## Hard fence

Other than the one explicitly authorized Task-137 Dashboard semantic submission: no second Send/resend; no alternate semantic injection; no source/runtime/plugin edit; no install/install-over/reset/uninstall/reinstall; no start/stop/restart/enable/disable; no recovery/crash injection; no provider/model/OpenClaw/config mutation; no manual Ticket/workflow/outbox/ack/delivery mutation; no SQLite write/cleanup; no process kill; no task/service mutation; no normalization; no reboot; no credentials/secrets; no merge/tag/release; no force push.
