# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_REWORK_TDD_PRODUCTION_INSTALLER_TRANSACTION`
Current authorization: `INSTALLER_TRANSACTION_WIRING_REWORK_AUTHORIZED`
Task ID: `CNX-20260826-068`
Updated: 2026-08-26 03:16 ICT
Owner: ChatGPT
Executor: Hermes after the operator's continuation signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260826-068-wire-installer-transaction-and-tighten-rollback-boundary.md`](tasks/CNX-20260826-068-wire-installer-transaction-and-tighten-rollback-boundary.md)

## Task 067 review

Task 067 reported:

`PASS_INSTALL_REPRODUCIBILITY_AND_PARTIAL_RECOVERY_FIXED`

Implementation HEAD:

`ec51d7b20c228070a95a6cf0987cebd7e71cbfaf`

Report HEAD:

`30075a3a3e646f24e0144f74aac9104c0ce1e888`

Independent review decision:

`REWORK`

Disposition:

`REWORK_INSTALLER_TRANSACTION_NOT_WIRED_AND_ROLLBACK_PARENT_BOUNDARY`

Review commit:

`38b46a4e78a9a2a2bcfc2c2cbaa230d888f7312c`

## Accepted Task 067 evidence

The D1 lock/package correction is accepted and must be preserved:

- exact OpenClaw devDependency `2026.7.1-2`;
- clean npm 11.16.0 and npm 12.0.2 install/validate/test/pack evidence;
- plugin v0.9.3 unchanged.

The transaction/recovery Python API is useful but not accepted as production-complete.

## Blocking findings

1. Production `scripts/install.ps1` adds `recovery-preflight` only; it never invokes `transaction-begin`, `transaction-record`, `transaction-commit`, or caught-failure rollback.
2. Current R1/R1b tests call the transaction Python API directly and therefore do not prove production installer ordering.
3. Rollback/recovery can walk upward and remove the shared `<workspace>\skills` parent when empty; deletion authority must stop at exact CNX-owned roots.

## Current live condition

Preserve the accepted Task-066 state:

- no CogentNexus Supervisor task;
- no launcher/plugin registration;
- OpenClaw Gateway native/healthy;
- Ollama healthy;
- Task-066 partial workspace residue remains intentionally untouched and has no valid ownership manifest.

## Authorized Task 068 operation

Source/tests only. Wire the transaction into the actual installer before fresh residue-capable mutation, record fresh-created paths, rollback caught failures, commit only after ownership verification, and tighten deletion boundaries so shared parents are never removed. Add production installer-facing RED/GREEN coverage and preserve the accepted npm 11/12 D1 fix.

## Live hard fence

No live residue cleanup, install/uninstall/reset/lifecycle operation, Scheduled Task mutation, Gateway/Ollama/plugin/config/AGENTS/SQLite mutation, process termination, reboot, primary workspace mutation, HermesAgent mutation, merge/tag/release.

## Pre-authorized successor

If Task 068 is independently accepted, Task 069 may perform the bounded one-time Task-066 residue cleanup and fresh install, then exact owned-runtime/no-Hermes binding, at least three natural no-flash PT1M ticks, and final MANAGED health acceptance without another confirmation.
