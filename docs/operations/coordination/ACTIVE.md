# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `REPOSITORY_SOURCE_TDD_REPAIR`
Current authorization: `CNX-20260829-133_RECOVERY_SEQUENCING_BEHAVIORAL_MATRIX_AND_PACKAGE_PROOF_CLOSEOUT`
Task ID: `CNX-20260829-133`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-133-recovery-sequencing-behavioral-matrix-and-package-proof-closeout.md`](tasks/CNX-20260829-133-recovery-sequencing-behavioral-matrix-and-package-proof-closeout.md)

Task 133 is repository/test/CI/package proof closeout only. It authorizes no live recovery or lifecycle operation.

## Task 132 review status

Task-132 report:

`docs/operations/coordination/reports/CNX-20260829-132-provider-to-operator-recovery-suite-sequencing-contract-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-132-provider-to-operator-recovery-suite-sequencing-contract-repair-review.md`

Review verdict:

`REJECTED CANDIDATE ADVANCEMENT — the sequencing repair direction and TDD order are accepted, but Task 132 does not yet satisfy its own required behavioral negative-case matrix, and the published artifact digest does not match GitHub's exact-SHA artifact metadata. Complete a repository-only proof closeout before any new live recovery acceptance.`

Task-132 proposed candidate `b7074c8cb5b10c77624cfe7b5223e3bae338c80d` is not yet accepted for live advancement.

## Task 133 required work

Complete executable `-ContractSelfTest` proof for the remaining fail-closed cases:

- adapter `expected=true` rejects;
- host provider mismatch rejects;
- provider-status selection mismatch rejects;
- missing Gateway listener rejects;
- missing Ollama listener rejects;
- post-operator-start/ordinary convergence remains strict and cannot inherit the carried provider-warning exception.

Keep all existing provider→operator carried-incident positive and negative cases green. Do not broaden provider recovery policy or warning semantics.

Then run full established validation and require exact-SHA success for:

- Validate;
- PS5.1 v0.9.3 Ollama Recovery V3 Smoke;
- PS5.1 Acceptance Smoke;
- Windows Installer Pack Smoke.

Produce a fresh exact-SHA package proof and publish the GitHub **outer artifact digest** separately from inner ZIP/tar hashes. Do not reuse the stale digest from Task 132.

## Historical live ledger

Remain consumed/closed:

- Task-121 install-over `1 / 1`;
- Task-124 reset/uninstall/fresh reinstall/standalone stop/start/restart `1 / 1` each;
- Task-125 old-harness recovery suite `1 / 1`;
- Task-128 suite `0 / 1`, closed blocked;
- Task-131 suite `1 / 1` consumed;
- Task-131 gateway-crash PASS;
- Task-131 provider-crash PASS;
- Task-131 operator-stop `0`, not reached.

Task 133 authorizes zero live operations.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-133-recovery-sequencing-behavioral-matrix-and-package-proof-closeout.md`

Then stop for independent ChatGPT review. Do not open a live recovery task automatically.

## Hard fence

No live recovery suite/crash injection, no install/install-over/reset/uninstall/reinstall, no live start/stop/restart/enable/disable, no live provider/OpenClaw/model/config mutation, no process kill, no task/service mutation, no cleanup/normalization, no reboot, no credentials/secrets, no Dashboard semantic Send, no merge/tag/release, and no force push.
