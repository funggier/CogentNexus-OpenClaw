# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_REPAIR_TDD_INSTALL_REPRODUCIBILITY_AND_RECOVERY`
Current authorization: `INSTALL_REPRODUCIBILITY_AND_RECOVERY_REPAIR_AUTHORIZED`
Task ID: `CNX-20260825-067`
Updated: 2026-08-25 23:25 ICT
Owner: ChatGPT
Executor: Hermes after the operator's continuation signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains project narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260825-067-repair-install-reproducibility-and-partial-recovery.md`](tasks/CNX-20260825-067-repair-install-reproducibility-and-partial-recovery.md)

## Task 066 accepted blocker

Task 066 report:

`BLOCKED_FRESH_INSTALL_FAILURE`

Report commit:

`d6812dd90a6ca28557cf18b6008a88dbfe5fe926`

Independent review decision:

`ACCEPT`

Disposition:

`ACCEPT_BLOCKER_FRESH_INSTALL_REPRODUCIBILITY_AND_PARTIAL_RECOVERY`

Review commit:

`21971ff01142ac98c166dc196c47df7cec60f434`

## Accepted live condition

The supported clean uninstall completed and removed the old Hermes-bound PT1M supervisor task. OpenClaw Gateway and Ollama remain healthy and unrelated state was preserved. CogentNexus is NOT freshly installed.

The failed fresh-install attempt left exactly the reported partial workspace residues without `ownership.json`; no supervisor task, launcher, or plugin registration is currently active. Do not clean or adopt those residues during Task 067.

## Root causes to repair

1. The plugin lockfile is rejected by npm 12 because nested `p-retry@4.6.2` requires exact `@types/retry@0.12.0` while the lock records `openclaw/node_modules/@types/retry` at `0.12.5`.
2. A fresh install can create new-namespace state/skill artifacts before ownership is committed; `classify_install()` then treats any such inventory as upgrade and requires `ownership.json`, creating a supported-recovery dead end after a mid-install failure.

## Authorized Task 067 operation

Task 067 is source/tests only. It must use strict TDD to make the lock reproducible under npm 11.16.0 and npm 12.0.2 and add a durable, bounded fresh-install transaction/recovery mechanism that survives caught failure and process interruption without weakening ownership safety.

## Live hard fence

No cleanup of the current Task-066 residues, install/install-over/uninstall/reset, lifecycle mutation, Scheduled Task change, Gateway/Ollama/plugin/config/AGENTS/SQLite mutation, process termination, primary workspace mutation, reboot, merge/tag/release, or HermesAgent mutation.

All recovery tests use isolated temp roots.

## Pre-authorized successor

If Task 067 is independently accepted, Task 068 may re-prove and remove only the two Task-066-created residue roots, fresh-install the accepted source, then complete exact owned-runtime binding, three-plus natural PT1M no-flash observation, and final MANAGED health acceptance.
