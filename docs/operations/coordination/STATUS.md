# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `LIVE_WINDOWS_RECOVERY_ACCEPTANCE_ONLY`  
**Updated:** 2026-08-29 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 134 grants one new exact sequenced-harness real-Windows recovery-suite execution only  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260829-134-v093-real-windows-recovery-final-reacceptance-sequenced.md`](tasks/CNX-20260829-134-v093-real-windows-recovery-final-reacceptance-sequenced.md)

Task ID:

`CNX-20260829-134`

## Task 133 accepted proof closeout

Report:

`docs/operations/coordination/reports/CNX-20260829-133-recovery-sequencing-behavioral-matrix-and-package-proof-closeout.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-133-recovery-sequencing-behavioral-matrix-and-package-proof-closeout-review.md`

Accepted result:

- exact candidate `1424d6fbee2c458c8c30440616783d2fa1bc1201`;
- exact harness blob `a4138e00e2056db89b0a9eceed1b54e001c4e319`;
- executable fail-closed provider→operator behavioral matrix complete;
- all four exact-SHA workflows success;
- fresh package artifact `9709798190` with outer digest `sha256:e8dbb2f742bfeffc93a80a7cda62a8c273ced9e2b1e9b47a3962dead52ccfeef`;
- payload count `178` and fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- no live operations under Task 133.

## Task 134 live gate

Fresh preflight must use the explicit installed launcher and its parsed `.cogentnexus-openclaw` root. Never probe the workspace parent as controller root.

Require an already-safe managed/Ollama/READY state, exact ownership/fingerprint/OpenClaw/plugin identity, healthy Gateway/Ollama, and authoritative SQLite `integrity_check=ok`. Unsafe preflight => BLOCKED without normalization.

If safe, run exactly one true-PTY harness process:

`-Scenario all -RunDisruptive`

Enter exactly one lowercase `y` after the literal prompt. No rerun after launch.

Require baseline PASS, Gateway crash PASS, provider crash PASS, exact carried provider incident accepted only at the immediate operator-before boundary, operator intentional stop/no-auto-recovery PASS, harness-owned start, and strict post-start READY PASS.

## Historical live ledger

Consumed/closed:

- install-over `1 / 1`;
- Task-124 reset/uninstall/fresh reinstall/standalone stop/start/restart `1 / 1` each;
- Task-125 old-harness recovery suite `1 / 1`;
- Task-128 suite `0 / 1`, closed blocked;
- Task-131 suite `1 / 1` consumed; baseline/Gateway/provider PASS; operator-stop not reached.

Task 134 creates a new suite maximum `1 / 1` only.

## Prohibited

No install/install-over/reset/uninstall/reinstall, no standalone lifecycle outside the exact harness, no source/harness edits, no alternate confirmation, no provider/OpenClaw/model/config mutation, no manual normalization, no generic process-tree kill, no task/service mutation outside observation, no reboot, no credential/secret access, no Dashboard semantic Send, no merge/tag/release, and no force push.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-134-v093-real-windows-recovery-final-reacceptance-sequenced.md`

Then stop for independent ChatGPT review. Final Dashboard durable-delivery acceptance remains unopened and prohibited.
