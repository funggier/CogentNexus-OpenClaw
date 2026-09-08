# CNX-20260907-310 — Periodic supervisor process-chain repair

Status: `READY_FOR_HERMES`
Parent: `CNX-20260907-309`
Executor: `Hermes`
Baseline: `aac898f18395b3a05b290e5d547c40306a4fe5a4`

## Authority

The operator explicitly authorized continuous improvement through a verified release. Task309 is complete. This successor authorizes source-only TDD repair of the every-minute Windows supervisor process-chain/cursor-busy defect, independent review, and exact-SHA CI. It does not authorize live installer/activation, semantic transport, protected-state mutation, tag/version/release mutation, or force push.

## Evidence and root cause to reproduce

Read-only live evidence is retained at:

- `C:\Users\CDQ-P\AppData\Local\Temp\cnx-spinner-checkpoint-20260907T171744Z.md`
- `C:\Users\CDQ-P\AppData\Local\Temp\cnx-spinner-evidence-20260907T\process-samples.jsonl`
- `C:\Users\CDQ-P\AppData\Local\Temp\cnx-spinner-evidence-20260907T\controlled-disable.jsonl`

The Windows task `\CogentNexus-OpenClaw-Supervisor` runs every minute with `InteractiveToken`. A healthy tick spawned a nested `pythonw.exe` chain through `host_control_v092.py`, `host_v092.py`, the base Host supervisor, `runtime.py supervisor tick`, and `openclaw.cmd gateway status`. A reversible 90-second disable produced no matching supervisor process and the task was restored enabled/Ready with result 0.

## Required procedure

1. Fresh-fetch and bind ACTIVE/STATUS/task/baseline; require clean tree and exact baseline.
2. Trace the production dispatch graph and add deterministic RED tests proving a healthy periodic tick avoids redundant wrapper/probe process boundaries while preserving quiescence, provider-event recovery, stall recovery, workflow/context supervision, and fail-closed recovery behavior.
3. Implement the smallest source repair. Do not merely hide a window or disable supervision. Preserve supported Windows/POSIX startup semantics and no-overlap behavior.
4. Run focused RED/GREEN, full Python/plugin suites, build/schema/bootstrap/package validation, production audit, and independent fail-closed review.
5. Commit RED separately where practical, commit minimal repair, push without force, and require all exact-SHA workflows terminal-successful.
6. Publish the matching Task310 report and stop. A separate successor must authorize supported exact-candidate install/activation and live no-spinner requalification.

## Acceptance

- deterministic RED observed before production change;
- healthy tick process boundary is materially reduced without weakening supervision;
- no regression to quiescence/recovery/provider/workflow authority;
- independent review has empty security/logic blocker lists;
- exact-SHA required CI terminal-successful;
- no live install/enable/restart, protected-state mutation, semantic action, or release metadata mutation.

## Hard fences

No installer, `enable`, Gateway/provider restart, semantic send, replay/redelivery/disposition, session Delete/cancel, manual SQLite/Ticket/session/transcript/config mutation, permanent Scheduled Task disable, version/tag/release mutation, force push, or live code edit.

Report: `docs/operations/coordination/reports/CNX-20260907-310-periodic-supervisor-process-chain-repair.md`
