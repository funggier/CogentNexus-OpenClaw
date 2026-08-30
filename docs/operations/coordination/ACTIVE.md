# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_REPAIRED_CANDIDATE_INSTALL_OVER_HEALTH_PROOF`
Current authorization: `CNX-20260830-157_REPAIRED_CANDIDATE_WINDOWS_INSTALL_OVER_HEALTH_PROOF`
Task ID: `CNX-20260830-157`
Updated: 2026-08-30 ICT
Owner / coordinator / reviewer: ChatGPT
Executor: Hermes on the operator's real Windows/OpenClaw environment

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260830-157-repaired-candidate-windows-install-over-health-proof.md`](tasks/CNX-20260830-157-repaired-candidate-windows-install-over-health-proof.md)

Task 157 authorizes the narrow live Windows checkpoint required after accepted Task-155 repair: install-over the repaired candidate, prove installed provenance, and collect live lifecycle/loader/health evidence.

## Accepted repair lineage

Accepted production repair:

`1ec8cfc81b8a21a178200c33816427f9abfd31b9`

Task-155 report:

`docs/operations/coordination/reports/CNX-20260830-155-dashboard-public-hook-duplicate-durable-authority-rework.md`

Task-155 review disposition: **ACCEPT**, recorded by commit:

`d4a4d6b0b14d18eee47d608edd66917eb27b9a68`

## Task-157 execution contract

Hermes must:

1. capture live pre-state and candidate provenance before mutation;
2. install-over the already-repaired candidate using the established repository process;
3. perform only lifecycle operations necessary for install-over and health proof;
4. prove installed identity/provenance and post-install lifecycle/loader/health state;
5. publish the required evidence report;
6. stop for ChatGPT review.

If provenance cannot be established before mutation, stop `BLOCKED` before install-over.

## Required completion signal

Publish exactly:

`docs/operations/coordination/reports/CNX-20260830-157-repaired-candidate-windows-install-over-health-proof.md`

Then stop for ChatGPT review. A separate explicit Task is required before any Dashboard semantic Send.

## Hard fence

No Dashboard semantic Send or Dashboard click/focus/type/paste for semantic testing; no new semantic user message; no manual Ticket/workflow/outbox/delivery/database mutation; no reset; no clean uninstall/fresh reinstall; no arbitrary live-state deletion; no manual production/source or OpenClaw patch; no dependency upgrade; no merge/tag/release/publish/promotion; no force push.

Task 157 authorizes install-over plus the minimum necessary lifecycle operations and read-only health/provenance/log inspection only.
