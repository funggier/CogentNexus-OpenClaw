# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `WINDOWS_REPAIRED_CANDIDATE_INSTALL_OVER_PROVENANCE_HEALTH_HERMES`
Current authorization: `CNX-20260830-165_HERMES_WINDOWS_REPAIRED_CANDIDATE_INSTALL_OVER_PROVENANCE_HEALTH`
Task ID: `CNX-20260830-165`
Updated: 2026-08-30 ICT
Executor: Hermes
Coordinator / final reviewer: ChatGPT
Review type at completion: ChatGPT review required before any Dashboard semantic reacceptance

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260830-165-hermes-windows-install-over-provenance-health.md`](tasks/CNX-20260830-165-hermes-windows-install-over-provenance-health.md)

Task 165 is the repaired-candidate Windows install-over + provenance/health checkpoint required after Task-164 repository repair acceptance.

## Accepted parent checkpoint

Task 164 is accepted by ChatGPT as:

`PASS — REPOSITORY_NATIVE_TRANSCRIPT_AUTHORITY_REPAIR_ACCEPTED`

Accepted production repair SHA:

`80b87dfbe0d9176e421f3748b4cee0827db12d0c`

Task-164 report publication SHA:

`a9eccaba3d3acd46530cd59d256a6b13702b29ef`

Task-164 ChatGPT review publication SHA:

`3a8caf12f8d7fc2cd03687ce088d01ccf790a5c0`

Review:

`reviews/CNX-20260830-164-hermes-native-transcript-authority-red-to-green-review.md`

Pinned intended OpenClaw target remains:

`0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c` (`v2026.7.1-2`)

## Current gate

Hermes must re-read current GitHub state, prove the exact candidate/package lineage, capture pre-install provenance, perform the supported install-over path, then prove post-install provenance and non-semantic health.

Task 165 must not perform semantic Dashboard acceptance.

If the candidate/package cannot be proven to derive from the accepted repair, or install-over reveals a product/installer defect, stop and report `FAIL`/`BLOCKED` rather than improvising a lifecycle change.

## Hard fence

Task 165 may perform only the supported repaired-candidate install-over and the runtime transitions inherently required by that installer, plus provenance/status/health inspection.

No Dashboard semantic Send; no semantic input through any other OpenClaw surface; no uninstall/reinstall/reset without separate authorization; no manual Ticket/workflow/result/outbox/delivery/database mutation; no arbitrary live-state deletion; no OpenClaw source patch or upgrade; no unrelated product change; no release/promotion; no merge to default/release branch; no force push.

Even Task-165 PASS does not itself authorize a Dashboard Send. ChatGPT review is required first. Only after Task-165 acceptance may a separate exactly-one-Send Dashboard durable-delivery reacceptance task be opened.
