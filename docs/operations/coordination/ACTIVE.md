# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `CONTROLLED_ACCEPTED_CANDIDATE_INSTALL_OVER_RETRY_AND_HEALTH_PROOF`
Current authorization: `CNX-20260829-142_ACCEPTED_CANDIDATE_INSTALL_OVER_RETRY_AND_HEALTH_PROOF`
Task ID: `CNX-20260829-142`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-142-accepted-candidate-install-over-retry-and-health-proof.md`](tasks/CNX-20260829-142-accepted-candidate-install-over-retry-and-health-proof.md)

Task 142 authorizes exactly one controlled supported live install-over retry from the independently accepted exact candidate, followed by provenance and read-only health proof. It does **not** authorize a Dashboard semantic Send.

## Task-141 disposition

Task-141 report:

`docs/operations/coordination/reports/CNX-20260829-141-direct-retired-storage-indirection-safety-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-141-direct-retired-storage-indirection-safety-repair-review.md`

Review disposition: **ACCEPT**.

Accepted exact deployment candidate:

`138759d111fe27a0cda75f59ad108d11caf19120`

That candidate is a descendant of the accepted Dashboard durable-capture repair `16f5c396e9be0af8d1bd34824fe2993613501a6f` and contains the accepted Task-140/141 installer ownership repairs.

## Task-142 execution contract

Task 142 must:

1. begin with fresh authority and read-only live-state capture;
2. stop before mutation on material drift from Task-139's accepted post-failure boundary;
3. build/package from a detached exact `138759d...` source tree and record provenance;
4. compute the exact candidate plugin fingerprint and candidate `namespace_ownership.py` hash;
5. invoke the supported `scripts/install.ps1` path exactly once, with no manual pre-normalization;
6. if install fails, stop without retry/cleanup/reset;
7. if install succeeds, prove installed plugin fingerprint and installed ownership-script hash match the exact candidate;
8. prove singular ownership/plugin identity and installer-restored managed operating state;
9. prove Gateway/provider/recovery/delivery/database health and semantic preservation;
10. publish the matching report and stop for independent review.

## Live-state starting boundary

Task 139 recorded the last accepted live state after its fail-closed install-over attempt:

- controller `passthrough`;
- one existing CogentNexus-OpenClaw plugin identity, disabled;
- old installed plugin fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- Gateway/Ollama healthy;
- recovery/delivery read-only checks READY;
- SQLite integrity `ok`;
- pending outbox `0`;
- historical Task-136/137 evidence preserved.

Tasks 140/141 were offline-only and did not normalize that state. Task 142 must verify the actual live state before mutation rather than assume it is unchanged.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-142-accepted-candidate-install-over-retry-and-health-proof.md`

Then stop for independent ChatGPT review.

## Hard fence

No uninstall/reset/clean-reinstall; no manual controller normalization; no manual plugin enable/disable/delete/replace; no alternate plugin installation path; no Dashboard semantic Send/resend; no Task-136/137 semantic reuse; no alternate semantic injection; no manual Ticket/workflow/outbox/ack/delivery/recovery/database mutation; no crash/recovery injection; no provider/model/OpenClaw config mutation except what the supported installer itself owns; no unrelated process/task/service mutation; no reboot; no credentials/secrets; no merge/tag/release; no force push.
