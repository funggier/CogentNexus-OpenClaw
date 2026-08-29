# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_RECOVERY_ACCEPTANCE_ONLY`
Current authorization: `CNX-20260829-134_V093_REAL_WINDOWS_RECOVERY_FINAL_REACCEPTANCE_SEQUENCED`
Task ID: `CNX-20260829-134`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-134-v093-real-windows-recovery-final-reacceptance-sequenced.md`](tasks/CNX-20260829-134-v093-real-windows-recovery-final-reacceptance-sequenced.md)

Task 134 authorizes exactly one new real-Windows recovery suite against the Task-133 accepted sequenced harness. It does not authorize installer/lifecycle replay outside the harness and does not open Dashboard durable-delivery acceptance.

## Task 133 accepted closure

Task-133 report:

`docs/operations/coordination/reports/CNX-20260829-133-recovery-sequencing-behavioral-matrix-and-package-proof-closeout.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-133-recovery-sequencing-behavioral-matrix-and-package-proof-closeout-review.md`

Accepted verdict:

`ACCEPTED PASS — Task 133 closes the remaining Task-132 proof gaps. The provider→operator sequencing exception is exercised through the real harness-owned PowerShell self-test with the required fail-closed structural negatives, all four required workflows passed on the exact candidate SHA, and the fresh package artifact metadata/identity are coherent. Candidate 1424d6fbee2c458c8c30440616783d2fa1bc1201 may advance to a new separately authorized one-shot real-Windows recovery acceptance.`

## Accepted candidate

- source: `1424d6fbee2c458c8c30440616783d2fa1bc1201`
- harness blob: `a4138e00e2056db89b0a9eceed1b54e001c4e319`
- artifact: `9709798190`
- outer digest: `sha256:e8dbb2f742bfeffc93a80a7cda62a8c273ced9e2b1e9b47a3962dead52ccfeef`
- payload count: `178`
- fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

Exact-SHA workflows passed: Validate `33235544556`, Recovery V3 Smoke `33235544569`, Acceptance Smoke `33235544559`, Windows Installer Pack Smoke `33235544603`.

## Task 134 execution discipline

Before disruption, use the explicit installed launcher `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd`, parse/verify its explicit `.cogentnexus-openclaw` root, and require an already-safe managed/Ollama/READY baseline, exact fingerprint/OpenClaw/plugin identity, healthy Gateway/Ollama, and authoritative SQLite read-only integrity `ok`.

Then use a true interactive PowerShell PTY and run the exact candidate harness once with `-Scenario all -RunDisruptive`. Enter exactly one lowercase `y` only after the literal prompt. No suite/scenario rerun is permitted after launch.

The critical repaired acceptance boundary is provider-crash PASS → exact carried incident at operator-before → intentional operator stop/no-auto-recovery → harness start → strict ordinary READY.

## Historical live ledger

Remain consumed/closed:

- Task-121 install-over `1 / 1`;
- Task-124 reset/uninstall/fresh reinstall/standalone stop/start/restart `1 / 1` each;
- Task-125 old-harness recovery suite `1 / 1`;
- Task-128 suite `0 / 1`, closed blocked;
- Task-131 suite `1 / 1` consumed; baseline/Gateway/provider PASS; operator-stop not reached.

Task 134 creates one new suite authorization: maximum `1 / 1`.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-134-v093-real-windows-recovery-final-reacceptance-sequenced.md`

Then stop for independent ChatGPT review. Do not open Dashboard acceptance automatically.

## Hard fence

No install/install-over/reset/uninstall/reinstall, no standalone lifecycle outside the exact harness, no source/harness edit, no alternate confirmation, no provider/model/OpenClaw/config mutation, no manual normalization, no generic process-tree kill, no task/service mutation outside observation, no reboot, no credentials/secrets, no Dashboard semantic Send, no merge/tag/release, and no force push.
