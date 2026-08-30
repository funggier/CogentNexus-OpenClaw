# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `WINDOWS_TASK167_ACCEPTED_CANDIDATE_INSTALL_OVER_PROVENANCE_HEALTH_HERMES`
Current authorization: `CNX-20260831-170_HERMES_WINDOWS_INSTALL_OVER_PROVENANCE_HEALTH`
Task ID: `CNX-20260831-170`
Updated: 2026-08-31 ICT
Executor: Hermes/Codex
Coordinator / final reviewer: ChatGPT
Review model: executor-heavy / reviewer-light

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260831-170-hermes-windows-install-over-provenance-health.md`](tasks/CNX-20260831-170-hermes-windows-install-over-provenance-health.md)

Task 170 is the bounded Windows install-over/provenance/health checkpoint for the accepted Task-167 repair.

## Accepted frozen product candidate

Exact repair SHA:

`231761fca24c315e90536955d3e384f55e2e232e`

Disposition:

`PASS — NATIVE_DELIVERY_STAGING_REPAIR_ACCEPTED`

Pinned OpenClaw remains:

`0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c` (`2026.7.1-2`).

## Accepted validation

- Task 168 local/build/package/Python/evaluation verification: complete except for the then-cancelled Validate run.
- Task 169 exact-SHA Validate rerun: `PASS`.
- Validate run `33330458434`, attempt 2: `completed/success`, 7/7 jobs.
- PS5.1 Acceptance Smoke `33330458475`: `success`.
- Windows Installer Pack Smoke `33330458470`: `success`.

Task-169 review:

`reviews/CNX-20260831-169-hermes-task167-exact-sha-validate-rerun-review.md`

## Current gate

Hermes/Codex must build/package from exact accepted SHA `231761f...`, record package SHA/fingerprint, perform exactly one supported Windows install-over, then independently prove installed fingerprint equality and healthy controller/Gateway/provider/plugin/recovery/delivery/storage state.

No semantic Dashboard Send is authorized.

## Hard fence

Exactly one supported install-over only.

No second installer attempt; no uninstall/reinstall/reset; no Dashboard semantic Send or semantic input; no `chat.inject`; no intentional model inference/regeneration; no manual Ticket/result/outbox/delivery/database/transcript mutation; no OpenClaw/dependency upgrade; no production repair; no release/promotion; no default/release merge; no force push.

If install-over/provenance/health cannot be proven, report and stop. Task 170 does not authorize semantic reacceptance.
