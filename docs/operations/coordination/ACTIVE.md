# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_RECOVERY_ACCEPTANCE_ONLY`
Current authorization: `CNX-20260829-128_V093_REAL_WINDOWS_RECOVERY_REACCEPTANCE`
Task ID: `CNX-20260829-128`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-128-v093-real-windows-recovery-reacceptance.md`](tasks/CNX-20260829-128-v093-real-windows-recovery-reacceptance.md)

Task 128 authorizes one new real-Windows recovery-reality suite execution against the repaired and independently accepted Task-127 harness. It authorizes no installer replay and no standalone lifecycle replay.

## Task 127 closure

Task-127 report:

`docs/operations/coordination/reports/CNX-20260829-127-recovery-harness-failclosed-contract-and-ci-proof.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-127-recovery-harness-failclosed-contract-and-ci-proof-review.md`

Review verdict:

`ACCEPTED PASS — RECOVERY HARNESS CONTRACT IS BEHAVIORALLY EXERCISED THROUGH THE REAL POWERSHELL ENTRYPOINT, THE PROVIDER-WARNING EXCEPTION IS FAIL-CLOSED, THE DEDICATED RECOVERY V3 SMOKE PASSES ON THE EXACT CANDIDATE SHA, AND THE REPAIRED CANDIDATE MAY ADVANCE TO A NEW, SEPARATELY AUTHORIZED REAL-WINDOWS RECOVERY ACCEPTANCE.`

Accepted exact candidate:

`1b922bf400fdbccb1f9c7019b89b69fd67f44070`

Exact harness:

- path `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- Git blob `622f70b339fea0f2ef7c564253aa3c6bf90ffc97`

Exact package proof:

- artifact `9706878201`
- digest `sha256:c5dcbda0858a08362daa3218c2912ddd4a36c259e61a05be28d7b1d4114b104c`
- payload count `178`
- fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

Exact-SHA workflows passed:

- Validate `33226001453`
- Recovery V3 Smoke `33226001456`
- PS5.1 Acceptance Smoke `33226001472`
- Windows Installer Pack Smoke `33226001471`

## Task 128 authorization

Task 128 creates exactly one new recovery-suite authorization because Task 125 used the old defective harness and Task 127 produced a repaired accepted harness.

Required execution discipline:

- read-only preflight first;
- verify no installed runtime/plugin/installer production deployment change requires reinstall;
- verify exact harness blob before launch;
- use true interactive PowerShell PTY;
- run the exact harness once with `-Scenario all -RunDisruptive`;
- enter exactly one lowercase `y` only after `Type y to continue:` appears;
- permit only the exact harness's gateway-crash, provider-crash, and operator-stop actions;
- fail-stop/no rerun;
- final deterministic read-only snapshot after PASS;
- publish the Task-128 report and stop for independent review.

## Historical consumed ledger

Remain consumed and forbidden outside the new exact Task-128 suite:

- Task-121 install-over `1 / 1`;
- Task-124 reset `1 / 1`;
- Task-124 uninstall `1 / 1`;
- Task-124 fresh reinstall `1 / 1`;
- Task-124 standalone stop/start/restart `1 / 1` each;
- Task-125 old-harness recovery suite `1 / 1`;
- Task-125 gateway-crash `1 / 1 PASS`;
- Task-125 provider-crash `1 / 1 old-harness convergence FAIL`.

Task 128 grants one new exact repaired-harness suite execution only.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-128-v093-real-windows-recovery-reacceptance.md`

Then stop for independent ChatGPT review. Do not open the Dashboard durable-delivery acceptance automatically.

## Hard fence

No install/install-over/reset/uninstall/reinstall, no standalone lifecycle commands outside the exact harness, no source/harness edits, no alternate confirmation mechanism, no provider/OpenClaw/config/model mutation, no manual normalization, no reboot, no generic process-tree kill, no credential access, no Dashboard semantic Send, no merge/tag/release, and no force push.