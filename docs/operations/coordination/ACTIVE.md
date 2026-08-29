# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_REPAIRED_CANDIDATE_INSTALL_OVER_AND_HEALTH_PROOF_ONLY`
Current authorization: `CNX-20260829-139_REPAIRED_CANDIDATE_INSTALL_OVER_AND_HEALTH_PROOF`
Task ID: `CNX-20260829-139`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-139-repaired-candidate-install-over-and-health-proof.md`](tasks/CNX-20260829-139-repaired-candidate-install-over-and-health-proof.md)

Task 139 performs one controlled supported install-over of the independently accepted Task-138 repair and proves installed provenance plus post-install health. It does **not** authorize any new Dashboard semantic Send.

## Task-138 disposition

Task-138 report:

`docs/operations/coordination/reports/CNX-20260829-138-dashboard-direct-result-durable-capture-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-138-dashboard-direct-result-durable-capture-repair-review.md`

Review disposition: **ACCEPT**.

Task 138 proved the Task-137 root cause at the registered Dashboard final-delivery callback boundary. A legitimate current final may observe `getQueuedCounts().final == 0`; the old `finalCount !== 1` filter skipped durable staging. The minimal repair accepts `0` or `1` and still rejects true multi-final ambiguity `>1`.

Accepted repaired source candidate:

`16f5c396e9be0af8d1bd34824fe2993613501a6f`

Offline evidence is GREEN: deterministic RED before production edit, targeted regression GREEN, existing boundary tests GREEN, full plugin suite 269/269 GREEN, build/plugin validation GREEN, and exact-repair-SHA GitHub Actions GREEN.

## Installed baseline before Task 139

Task 138 performed no live install or runtime mutation.

Pre-repair installed payload/plugin fingerprint remains the Task-137 baseline until Task 139 proves otherwise:

`3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

Historical Task-136 and Task-137 failed Tickets are immutable acceptance evidence and must remain preserved. Task-137 Send ledger remains permanently consumed `1 / 1`.

## Task-139 execution contract

Task 139 must:

1. fresh-verify authority and a safe no-pending live baseline;
2. build/package from exact repaired source `16f5c396e9be0af8d1bd34824fe2993613501a6f` and capture artifact/package SHA-256;
3. prove the current installed fingerprint before mutation;
4. use exactly one established supported install-over/update path, with no clean uninstall/reset/normalization;
5. prove the effective installed payload originates from the exact repaired candidate and record its new fingerprint;
6. prove managed/Ollama, Gateway/Ollama, recovery, delivery, plugin identity, SQLite integrity, `pendingOutbox=0`, and `nonterminalTickets=0` after convergence;
7. prove historical Task-136/137 evidence is preserved and installation itself creates no semantic Ticket/delivery/recovery work;
8. publish the matching report and stop for independent review.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-139-repaired-candidate-install-over-and-health-proof.md`

Then stop for independent ChatGPT review.

No final Dashboard semantic re-acceptance is automatic.

## Hard fence

No Dashboard semantic Send/resend; no Task-136/137 semantic reuse; no alternate semantic injection; no clean uninstall/reset; no manual cleanup/normalization; no manual Ticket/workflow/outbox/ack/delivery/recovery/database mutation; no recovery/crash injection; no provider/model/OpenClaw config mutation; no unrelated process/task/service mutation; no reboot; no credentials/secrets; no merge/tag/release; no force push.
