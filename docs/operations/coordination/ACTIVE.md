# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `REPOSITORY_SOURCE_TDD_REPAIR`
Current authorization: `CNX-20260829-127_RECOVERY_HARNESS_FAILCLOSED_CONTRACT_AND_CI_PROOF`
Task ID: `CNX-20260829-127`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-127-recovery-harness-failclosed-contract-and-ci-proof.md`](tasks/CNX-20260829-127-recovery-harness-failclosed-contract-and-ci-proof.md)

Task 127 repairs only the remaining Task-126 acceptance-harness review defects:

- replace test-local/source-grep regression with a real behavioral test of harness-owned convergence logic;
- make `READY_WITH_WARNINGS` provider-crash acceptance fail-closed so only the sole expected open/circuit-closed Provider recovery incident WARN is allowed;
- ensure the dedicated PS5.1 v0.9.3 Ollama Recovery V3 Smoke runs and passes on the exact direct-push candidate SHA;
- rerun full validation and package proof.

## Task 126 closure

Task-126 report:

`docs/operations/coordination/reports/CNX-20260829-126-provider-crash-recovery-convergence-root-cause-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-126-provider-crash-recovery-convergence-root-cause-repair-review.md`

Review verdict:

`REJECTED CANDIDATE ADVANCEMENT — ROOT-CAUSE CLASSIFICATION IS ACCEPTED, BUT THE HARNESS REPAIR IS NOT YET FAIL-CLOSED OR BEHAVIORALLY PROVEN, AND THE AFFECTED RECOVERY-SPECIFIC SMOKE DID NOT RUN ON THE EXACT CANDIDATE SHA.`

Accepted Task-126 root cause:

- Task-125 provider recovery itself was coherent;
- provider recovery incident intentionally remained open pending stable model-success evidence;
- recovery check therefore remained `READY_WITH_WARNINGS`;
- the mismatch belongs to the acceptance harness;
- provider recovery policy must not be weakened by treating process/listener health as stable success.

Rejected Task-126 candidate:

`69a3efa1feb7711f22c83055a8571035240ec81c`

Its Validate, Windows Installer Pack Smoke, and PS5.1 Acceptance Smoke runs passed, but candidate advancement was rejected because the focused regression did not execute the real harness contract, warning acceptance was too broad, and the dedicated recovery-v3 smoke had no exact-SHA run.

## Consumed live-operation ledger

All remain consumed/forbidden during Task 127:

- Task-121 install-over `1 / 1`;
- Task-124 reset `1 / 1`;
- Task-124 uninstall `1 / 1`;
- Task-124 fresh reinstall `1 / 1`;
- Task-124 stop `1 / 1`;
- Task-124 start `1 / 1`;
- Task-124 restart `1 / 1`;
- Task-125 recovery suite `1 / 1`;
- Task-125 gateway-crash `1 / 1 PASS`;
- Task-125 provider-crash `1 / 1 FAIL at old harness convergence`;
- operator-stop `0`, not reached.

Task 127 authorizes no live replay.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-127-recovery-harness-failclosed-contract-and-ci-proof.md`

Then stop for independent ChatGPT review. Do not open a live recovery acceptance task automatically.

## Hard fence

No live provider crash, recovery-suite replay, install/reset/uninstall/reinstall, stop/start/restart, provider/OpenClaw mutation, process kill/reboot, manual normalization, credentials/secrets, Dashboard semantic Send, merge/tag/release, or force push.
