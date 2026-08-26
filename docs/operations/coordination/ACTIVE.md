# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_REWORK_TDD_INSTALLER_MODE_ISOLATION`
Current authorization: `INSTALLER_MODE_ISOLATION_REWORK_AUTHORIZED`
Task ID: `CNX-20260826-070`
Updated: 2026-08-26 11:24 ICT
Owner: ChatGPT
Executor: Hermes after the operator's continuation signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260826-070-restore-nonfresh-installer-mode-isolation.md`](tasks/CNX-20260826-070-restore-nonfresh-installer-mode-isolation.md)

## Task 069 review

Task 069 reported:

`PASS_FRESH_TRANSACTION_FAILURE_COVERAGE_CLOSED`

Implementation HEAD:

`7f48bb803fe3ca46b7a786e50abe8df22da857fc`

Report HEAD:

`fee1a44b5e2212e3b21f627c57e943eb3154878c`

Independent review decision:

`REWORK`

Disposition:

`REWORK_NONFRESH_INSTALL_MODE_ABORT_REGRESSION`

Review commit:

`a9112161391a2696733f1c09d1721e8611ab843a`

## Accepted Task 069 portions

Preserve:

- fresh pre-commit caught-failure boundary concept;
- exact application-data transaction authority and preexisting-root preservation;
- record-time unsafe path rejection;
- supported fresh plugin inverse;
- AGENTS policy moved post-transaction-commit;
- exact-root/shared-parent rollback safety;
- npm 11/npm 12 reproducibility and exact OpenClaw `2026.7.1-2` pin;
- implementation/report publication fence.

## Blocking finding

Task 069 inserted a sentinel inside the shared installer try block:

`if (-not $isFreshTransaction) { throw "__UPGRADE_PASSTHROUGH__" }`

The catch converts that into `Non-fresh install cannot use the fresh transaction failure boundary.`

Therefore every coherent upgrade or legacy install aborts before the existing installer body can run. Fresh rollback behavior improved, but install-over/upgrade and legacy migration were regressed.

## Current live condition

Preserve the accepted Task-066 native state:

- no CogentNexus Supervisor task;
- no launcher/plugin registration;
- OpenClaw Gateway native/healthy;
- Ollama healthy;
- Task-066 partial unowned workspace residue remains intentionally untouched;
- no valid ownership manifest;
- AGENTS managed block absent.

## Authorized Task 070 operation

Source/tests only. Restore normal upgrade/legacy reachability while keeping fresh caught-failure rollback mode-scoped. Non-fresh failures must rethrow normally and must never invoke fresh transaction rollback. Add executable mode-isolation regression coverage and preserve all accepted transaction/npm safety work.

## Live hard fence

No live residue cleanup, install/uninstall/reset/lifecycle operation, Scheduled Task mutation, Gateway/Ollama/plugin/config/AGENTS/SQLite mutation, process termination, reboot, primary workspace mutation, HermesAgent mutation, merge/tag/release.

## Pre-authorized successor

If Task 070 is independently accepted, Task 071 may perform bounded one-time Task-066 residue cleanup and fresh install, then exact owned-runtime/no-Hermes binding, at least three natural PT1M no-flash ticks, and final MANAGED health acceptance without another confirmation.
