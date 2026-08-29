# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_READONLY_DIAGNOSIS_ONLY`
Current authorization: `CNX-20260829-129_MANAGED_STATE_STATE_ROOT_AUTHORITY_READONLY_DIAGNOSIS`
Task ID: `CNX-20260829-129`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-129-managed-state-state-root-authority-readonly-diagnosis.md`](tasks/CNX-20260829-129-managed-state-state-root-authority-readonly-diagnosis.md)

Task 129 is a live-Windows **read-only forensic diagnosis** of the Task-128 Phase-0 state discontinuity. It must prove the installed launcher → explicit `--root` → controller/runtime/ownership/SQLite authority chain and classify whether the observed `passthrough` / null provider is genuine authoritative drift, a launcher/root mismatch, a SQLite/status probe defect, mixed authority, or indeterminate.

## Task 128 closure

Task-128 report:

`docs/operations/coordination/reports/CNX-20260829-128-v093-real-windows-recovery-reacceptance.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-128-v093-real-windows-recovery-reacceptance-review.md`

Review verdict:

`ACCEPTED BLOCKED — Task 128 stopped at the required read-only safety fence before launching the newly authorized recovery suite. No Task-128 disruptive scenario, lifecycle replay, confirmation input, provider mutation, or Dashboard semantic Send occurred. The observed PASSTHROUGH/null-provider state is a precondition failure requiring separate read-only state-root/authority diagnosis; it is not a recovery-product failure.`

Task-128 repaired-harness suite remains `0 / 1 launched`; confirmation and all scenarios remain `0`.

## Accepted repository candidate

Task-127 accepted source candidate remains:

`1b922bf400fdbccb1f9c7019b89b69fd67f44070`

Exact recovery harness:

- `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- Git blob `622f70b339fea0f2ef7c564253aa3c6bf90ffc97`

Package proof:

- artifact `9706878201`
- digest `sha256:c5dcbda0858a08362daa3218c2912ddd4a36c259e61a05be28d7b1d4114b104c`
- payload fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

## Task 129 required work

Read-only only:

- capture exact installed `cnxclaw.cmd` bytes/hash/content;
- parse and verify its owned Python, installed `cnxclaw_v093.py`, and explicit `--root` target;
- inventory authoritative controller/runtime/ownership/SQLite files and metadata;
- enumerate bounded competing `.cogentnexus-openclaw` roots;
- invoke status/provider/recovery only through the explicit installed launcher path with argument-safe direct calls;
- inspect scheduled-task/service executable/arguments/working-directory authority without running or changing them;
- compare current controller generation/mode/provider/timestamps against Task-125 cleanup evidence and relevant durable logs/events;
- classify `AUTHORITATIVE_STATE_DRIFT`, `LAUNCHER_OR_ROOT_MISMATCH`, `SQLITE_PATH_OR_STATUS_PROBE_DEFECT`, `MIXED_AUTHORITY`, or `INDETERMINATE`;
- publish the Task-129 report and stop for independent review.

## Historical consumed ledger

Remain consumed/forbidden:

- Task-121 install-over `1 / 1`;
- Task-124 reset/uninstall/fresh reinstall/standalone stop/start/restart `1 / 1` each;
- Task-125 old-harness recovery suite `1 / 1`;
- Task-125 gateway-crash `1 / 1 PASS`;
- Task-125 provider-crash `1 / 1 old-harness convergence FAIL`;
- Task-128 repaired-harness recovery suite `0 / 1 launched`.

Task 129 authorizes zero recovery/lifecycle mutations.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-129-managed-state-state-root-authority-readonly-diagnosis.md`

Then stop for independent ChatGPT review.

## Hard fence

No recovery suite/crash scenario, install/install-over/reset/uninstall/reinstall, start/stop/restart, enable/disable, provider/model/config mutation, state/database edit or initialization, process kill, task/service run/change, cleanup/normalization, reboot, credential/secret access, Dashboard semantic Send, merge/tag/release, or force push.
