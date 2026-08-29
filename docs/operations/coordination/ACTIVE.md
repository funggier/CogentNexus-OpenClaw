# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_READONLY_DELIVERY_BASELINE_ONLY`
Current authorization: `CNX-20260829-135_POST_RECOVERY_DELIVERY_RESIDUE_READONLY_CLOSEOUT`
Task ID: `CNX-20260829-135`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-135-post-recovery-delivery-residue-readonly-closeout.md`](tasks/CNX-20260829-135-post-recovery-delivery-residue-readonly-closeout.md)

Task 135 is a read-only Ticket/workflow/outbox/delivery baseline closeout. It authorizes zero semantic Sends and zero live lifecycle/recovery mutations.

## Task 134 accepted recovery closure

Report:

`docs/operations/coordination/reports/CNX-20260829-134-v093-real-windows-recovery-final-reacceptance-sequenced.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-134-v093-real-windows-recovery-final-reacceptance-sequenced-review.md`

Accepted result:

`ACCEPTED RECOVERY PASS — exact candidate 1424d6fbee2c458c8c30440616783d2fa1bc1201 completed the one-shot real-Windows recovery suite through baseline, Gateway crash, provider crash, the repaired provider→operator carried-incident boundary, intentional stop/no-auto-recovery, harness-owned start, and strict post-start READY. Dashboard advancement remains gated only by the missing read-only outbox/status residue publication item.`

Task-134 live ledger is consumed and must never be replayed:

- suite `1 / 1 PASS`;
- confirmation `1 / 1`;
- Gateway crash `1 / 1 PASS`;
- provider crash `1 / 1 PASS`;
- operator stop/start sequence `1 / 1 PASS`;
- reruns `0`.

## Task 135 required proof

Using the explicit installed launcher and parsed authoritative `.cogentnexus-openclaw` root only:

- read-only `status`, `check delivery`, and `check recovery`;
- authoritative SQLite URI `mode=ro` and `integrity_check=ok`;
- ticket counts by status and `nonterminalTickets=0`;
- ticket-outbox counts by delivery status and `pendingOutbox=0`;
- read-only classification of workflow/delivery/direct-recovery residue;
- no active work capable of contaminating a one-message Dashboard durable-delivery baseline;
- runtime remains managed/Ollama/READY.

Historical terminal rows may remain if clearly inert. If any active/ambiguous residue exists, fail closed and report it without cleanup.

Do not read/publish semantic payload bodies unless strictly unavoidable; prefer IDs/status/timestamps/hashes/lengths.

## Dashboard fence

Final Dashboard durable-delivery acceptance is still unopened. Task 135 must not send, create, dispatch, retry, cancel, ack, delete, or normalize anything.

Only after Task 135 PASS + independent ChatGPT review may a separate Dashboard task authorize exactly one new semantic nonce/message Send.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-135-post-recovery-delivery-residue-readonly-closeout.md`

Then stop for independent ChatGPT review.

## Hard fence

No Dashboard semantic Send; no Ticket/workflow/outbox mutation; no SQLite write; no install/install-over/reset/uninstall/reinstall; no start/stop/restart/enable/disable; no recovery suite/crash/process kill; no provider/OpenClaw/model/config mutation; no task/service mutation; no cleanup/normalization; no reboot; no credentials/secrets; no source/runtime repair; no merge/tag/release; no force push.