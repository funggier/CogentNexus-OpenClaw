# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_REWORK_TDD_FRESH_TRANSACTION_FAILURE_COVERAGE`
Current authorization: `FRESH_TRANSACTION_FAILURE_COVERAGE_REWORK_AUTHORIZED`
Task ID: `CNX-20260826-069`
Updated: 2026-08-26 05:57 ICT
Owner: ChatGPT
Executor: Hermes after the operator's continuation signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260826-069-close-fresh-transaction-failure-coverage.md`](tasks/CNX-20260826-069-close-fresh-transaction-failure-coverage.md)

## Task 068 review

Task 068 reported:

`PASS_PRODUCTION_INSTALLER_TRANSACTION_WIRED`

Implementation HEAD:

`2a0ca9fd9abda07765e3da222f7fc4d7730d3d30`

Report HEAD:

`3fc596a394fa2167d6c50e1672294c355120e809`

Independent review decision:

`REWORK`

Disposition:

`REWORK_CAUGHT_FAILURE_AND_APPLICATION_DATA_TRANSACTION_GAPS`

Review commit:

`ad914838420028b4170cab9fc1e6d466dc7d444f`

## Accepted Task 068 portions

Preserve:

- fresh-only transaction begin after classification and before first fresh workspace mutation;
- transaction record call sites for state/skill/launcher/application-data;
- commit after ownership create + exact verify;
- exact-root rollback no longer removes shared `<workspace>\skills` parent;
- accepted Task 067 npm 11/npm 12 lockfile fix;
- separate report-only publication fence.

## Blocking findings

1. Caught fresh failures before ownership create/verify still bypass rollback; P3 only proves the rollback helper exists rather than injecting a real early production-path failure.
2. Fresh installer records `%LOCALAPPDATA%\CogentNexus-OpenClaw`, but marker validation does not allow the exact application-data product root, so a legitimate marker can reject its own rollback/recovery.
3. Any unavoidable pre-commit product external effect, especially fresh plugin registration, must be reordered post-commit where safe or have a supported bounded inverse so rerun does not dead-end.

## Current live condition

Preserve the accepted Task-066 native state:

- no CogentNexus Supervisor task;
- no launcher/plugin registration;
- OpenClaw Gateway native/healthy;
- Ollama healthy;
- Task-066 partial workspace residue remains intentionally untouched and has no valid ownership manifest;
- AGENTS managed block absent.

## Authorized Task 069 operation

Source/tests only. Establish one fresh pre-commit caught-failure boundary, make exact application-data ownership/validation consistent, reject unsafe paths at record time, and prove recovery of product-owned external effects without weakening ownership safety.

## Live hard fence

No live residue cleanup, install/uninstall/reset/lifecycle operation, Scheduled Task mutation, Gateway/Ollama/plugin/config/AGENTS/SQLite mutation, process termination, reboot, primary workspace mutation, HermesAgent mutation, merge/tag/release.

## Pre-authorized successor

If Task 069 is independently accepted, Task 070 may perform bounded one-time Task-066 residue cleanup and fresh install, then exact owned-runtime/no-Hermes binding, at least three natural PT1M no-flash ticks, and final MANAGED health acceptance without another confirmation.
