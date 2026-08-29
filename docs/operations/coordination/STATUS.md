# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `LIVE_WINDOWS_RECOVERY_ACCEPTANCE_ONLY`  
**Updated:** 2026-08-29 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 128 grants one new repaired-harness real-Windows recovery-suite execution only  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260829-128-v093-real-windows-recovery-reacceptance.md`](tasks/CNX-20260829-128-v093-real-windows-recovery-reacceptance.md)

Task ID:

`CNX-20260829-128`

## Task 127 accepted candidate

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-127-recovery-harness-failclosed-contract-and-ci-proof-review.md`

Verdict:

`ACCEPTED PASS — RECOVERY HARNESS CONTRACT IS BEHAVIORALLY EXERCISED THROUGH THE REAL POWERSHELL ENTRYPOINT, THE PROVIDER-WARNING EXCEPTION IS FAIL-CLOSED, THE DEDICATED RECOVERY V3 SMOKE PASSES ON THE EXACT CANDIDATE SHA, AND THE REPAIRED CANDIDATE MAY ADVANCE TO A NEW, SEPARATELY AUTHORIZED REAL-WINDOWS RECOVERY ACCEPTANCE.`

Exact source candidate:

`1b922bf400fdbccb1f9c7019b89b69fd67f44070`

Exact harness:

- `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- Git blob `622f70b339fea0f2ef7c564253aa3c6bf90ffc97`

Exact package proof:

- artifact ID `9706878201`
- artifact digest `sha256:c5dcbda0858a08362daa3218c2912ddd4a36c259e61a05be28d7b1d4114b104c`
- payload file count `178`
- payload fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- tar.gz `9a4634e41d21271b92d0c6ce69f4931bca11455808a9e1b8567e48db85bb432d`
- ZIP `526ca264db77b960d2d81d3f6cf7c100e8c45f2d6243eaab00801da9ee293c3e`

Exact-SHA workflows:

- Validate `33226001453` — success;
- PS5.1 Recovery V3 Smoke `33226001456` — success;
- PS5.1 Acceptance Smoke `33226001472` — success;
- Windows Installer Pack Smoke `33226001471` — success.

## Task 128 scope

Task 128 is live recovery re-acceptance only. It does not authorize reinstalling or replaying the already-passed lifecycle phases.

Before disruption:

- fresh-check Task 128 authority;
- prove the accepted candidate does not require installed runtime redeployment;
- use an isolated exact-candidate harness copy and verify its blob/provenance;
- perform deterministic read-only runtime/ownership/OpenClaw/Ollama/SQLite/service preflight;
- stop BLOCKED if the current live state is not already safe.

Then, in a true interactive PowerShell TTY, run exactly one repaired-harness suite with `-Scenario all -RunDisruptive`. Enter exactly one lowercase `y` only after the exact confirmation prompt appears.

The suite may exercise only its reviewed baseline, gateway-crash, provider-crash, and operator-stop sequence. No scenario or suite rerun is allowed after launch.

After a PASS/exit 0, collect a final read-only snapshot. No standalone lifecycle command may be used to repair the final state.

## Historical consumed ledger

Outside the new Task-128 repaired-harness suite, these remain consumed/forbidden:

- install-over `1 / 1`;
- reset `1 / 1`;
- uninstall `1 / 1`;
- fresh reinstall `1 / 1`;
- standalone stop `1 / 1`;
- standalone start `1 / 1`;
- standalone restart `1 / 1`;
- Task-125 old-harness recovery suite `1 / 1`;
- Task-125 gateway-crash `1 / 1 PASS`;
- Task-125 provider-crash `1 / 1 old-harness convergence FAIL`.

## Prohibited

No install/install-over/reset/uninstall/reinstall, no standalone lifecycle outside the exact suite, no source/harness edits, no alternate/piped/synthetic confirmation, no provider/OpenClaw/config/model mutation, no manual cleanup/normalization, no reboot, no generic process-tree kill, no credential/secret access, no Dashboard semantic Send, no merge/tag/release, and no force push.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-128-v093-real-windows-recovery-reacceptance.md`

Then stop for independent ChatGPT review. Final Dashboard durable-delivery acceptance remains unopened and prohibited.