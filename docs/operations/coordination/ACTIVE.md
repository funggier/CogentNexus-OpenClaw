# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_RECOVERY_ACCEPTANCE_ONLY`
Current authorization: `CNX-20260829-131_V093_REAL_WINDOWS_RECOVERY_REACCEPTANCE_AUTHORITATIVE_ROOT`
Task ID: `CNX-20260829-131`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-131-v093-real-windows-recovery-reacceptance-authoritative-root.md`](tasks/CNX-20260829-131-v093-real-windows-recovery-reacceptance-authoritative-root.md)

Task 131 authorizes one new real-Windows recovery suite against the exact Task-127 repaired harness after Task 129/130 proved Task 128 was blocked by a wrong external preflight root.

## Task 129/130 closure

Task-130 report:

`docs/operations/coordination/reports/CNX-20260829-130-task129-readonly-evidence-publication-closeout.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-130-task129-readonly-evidence-publication-closeout-review.md`

Accepted verdict:

`ACCEPTED PASS — TASK 129/130 NOW PROVIDE SUFFICIENT READ-ONLY EVIDENCE THAT TASK 128 WAS BLOCKED BY AN EXECUTOR/PREFLIGHT ROOT MISMATCH, NOT BY AUTHORITATIVE MANAGED-STATE DRIFT; THE AUTHORITATIVE INSTALLED ROOT IS COHERENT, SQLITE PASSES READ-ONLY INTEGRITY, AND A NEW SEPARATELY AUTHORIZED REAL-WINDOWS RECOVERY RE-ACCEPTANCE MAY BE OPENED.`

Accepted classification:

- `LAUNCHER_OR_ROOT_MISMATCH`;
- `SQLITE_PATH_OR_STATUS_PROBE_DEFECT` limited to Task-128 preflight.

Authoritative installed launcher:

`C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd`

Authoritative state root:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw`

Task 128 incorrectly probed the workspace parent and never launched its recovery suite.

## Accepted candidate

Task-127 exact source candidate:

`1b922bf400fdbccb1f9c7019b89b69fd67f44070`

Exact repaired harness:

- `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- Git blob `622f70b339fea0f2ef7c564253aa3c6bf90ffc97`

Package proof:

- artifact `9706878201`;
- digest `sha256:c5dcbda0858a08362daa3218c2912ddd4a36c259e61a05be28d7b1d4114b104c`;
- payload fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`.

## Task 131 execution discipline

Before disruption:

- fresh-check coordination and exact harness provenance;
- use the explicit installed launcher for all authoritative CNX preflight probes;
- freshly parse launcher Python/CLI/explicit `.cogentnexus-openclaw` root;
- never manually pass the workspace parent as `--root`;
- require managed/Ollama/recovery READY, exact ownership/plugin/OpenClaw identity, healthy Gateway/Ollama, and authoritative SQLite `integrity_check=ok`;
- stop BLOCKED without normalization if the live preflight is not already safe.

Then use a true interactive PowerShell PTY and run the exact repaired harness once with `-Scenario all -RunDisruptive`. Enter exactly one lowercase `y` only after the literal prompt. No suite/scenario rerun is permitted after launch.

After PASS only, collect a final read-only snapshot through the same installed launcher/root authority.

## Historical ledger

Remain consumed/forbidden outside Task 131:

- Task-121 install-over `1 / 1`;
- Task-124 reset/uninstall/fresh reinstall/standalone stop/start/restart `1 / 1` each;
- Task-125 old-harness recovery suite `1 / 1`;
- Task-128 repaired-harness suite `0 / 1 launched`, closed.

Task 131 creates one new exact repaired-harness recovery-suite authorization only.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-131-v093-real-windows-recovery-reacceptance-authoritative-root.md`

Then stop for independent ChatGPT review. Do not open Dashboard durable-delivery acceptance automatically.

## Hard fence

No install/install-over/reset/uninstall/reinstall, no standalone lifecycle outside the exact harness, no source/harness edits, no alternate confirmation, no provider/OpenClaw/model/config mutation, no manual normalization, no reboot, no generic process-tree kill, no credentials/secrets, no Dashboard semantic Send, no merge/tag/release, and no force push.
