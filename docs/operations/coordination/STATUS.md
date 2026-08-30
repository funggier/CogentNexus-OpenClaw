# Coordination Channel Status

**State:** `READY_HERMES`  
**Execution mode:** `WINDOWS_TASK167_ACCEPTED_CANDIDATE_INSTALL_OVER_PROVENANCE_HEALTH_HERMES`  
**Updated:** 2026-08-31 ICT  
**Transport:** GitHub repository history  
**Active task:** `CNX-20260831-170`

## Active work

[`tasks/CNX-20260831-170-hermes-windows-install-over-provenance-health.md`](tasks/CNX-20260831-170-hermes-windows-install-over-provenance-health.md)

Executor: Hermes/Codex. Coordinator / final reviewer: ChatGPT.

Standing model: executor-heavy / reviewer-light. Hermes/Codex owns primary investigation/execution/evidence packaging; ChatGPT reviews critical claims and final disposition.

## Task 167 — repair accepted

Accepted product repair SHA:

`231761fca24c315e90536955d3e384f55e2e232e`

Final disposition:

`PASS — NATIVE_DELIVERY_STAGING_REPAIR_ACCEPTED`

Task 168 supplied the required local/build/package/Python/evaluation evidence and risk/verification packet. Task 169 closed the only remaining exact-SHA CI gap.

## Task 169 — accepted CI completion

Report:

`reports/CNX-20260831-169-hermes-task167-exact-sha-validate-rerun.md`

Review:

`reviews/CNX-20260831-169-hermes-task167-exact-sha-validate-rerun-review.md`

Disposition:

`ACCEPTED_PASS`

Exact-SHA workflows for repair `231761f...`:

- Validate `33330458434`, attempt 2: `completed/success`, 7/7 jobs;
- Windows Installer Pack Smoke `33330458470`: `success`;
- PS5.1 Acceptance Smoke `33330458475`: `success`.

Pinned OpenClaw remains:

`0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c` (`2026.7.1-2`).

## Task 170 objective

Perform one bounded Windows install-over from the exact accepted candidate and prove:

1. exact package SHA/fingerprint provenance before installation;
2. exactly one supported install-over execution;
3. installed fingerprint equals frozen candidate fingerprint;
4. OpenClaw pin is preserved;
5. plugin/controller/Gateway/provider/startup/recovery/delivery/storage health is acceptable;
6. database integrity and durable-state reconciliation pass;
7. zero semantic Dashboard Sends/inference requests/manual semantic mutations occur.

Only after Task 170 reports PASS and ChatGPT accepts it may coordination consider a separate exactly-one-Send semantic durable-delivery reacceptance.

## Hard fence

Task 170 does not authorize semantic acceptance.

No second installer attempt, uninstall, clean reinstall, reset, Dashboard semantic Send, `chat.inject`, intentional model inference/regeneration, manual Ticket/result/outbox/delivery/database/transcript mutation, OpenClaw/dependency upgrade, production repair, release/promotion, default/release merge, or force push.
