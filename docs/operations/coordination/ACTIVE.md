# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TEST_ONLY_TDD_LIVE_APPDATA_ISOLATION`
Current authorization: `RECOVERY_TEST_ISOLATION_AUTHORIZED`
Task ID: `CNX-20260826-074`
Updated: 2026-08-26 18:29 ICT
Owner: ChatGPT
Executor: Hermes after the operator's continuation signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260826-074-isolate-recovery-tests-from-live-appdata.md`](tasks/CNX-20260826-074-isolate-recovery-tests-from-live-appdata.md)

## Task 073 review

Task 073 reported:

`PASS_CLEAN_FRESH_RECOVERY_PREFLIGHT_CORRECTED`

Implementation HEAD:

`79b51ed06363f6e8862c491ee0a313ddb412c806`

Report HEAD:

`ba4a04825fb7396617fa0fe17c62f84f5f5e1507`

Independent review decision:

`REWORK`

Disposition:

`REWORK_FULL_SUITE_LIVE_APPDATA_FIXTURE_COUPLING`

Review commit:

`6fc24cc44b66afa8411cafb2c2e31d34c7572dce`

## Accepted Task-073 production correction candidate

Preserve unless a new executable test proves otherwise:

- markerless clean state returns `CLEAN_FRESH`;
- markerless partial residue remains fail-closed;
- incomplete transaction recovery remains bounded;
- ownership-present remains non-rollback state;
- installer stops immediately on nonzero recovery-preflight before classification;
- unknown successful recovery status fail-closes;
- ordering before classification/transaction begin remains intact.

## Blocking finding

The Task-073 full pytest regression gate recorded four failures. They are reproducible test-fixture coupling to the real `%LOCALAPPDATA%\CogentNexus-OpenClaw` root now legitimately present after Task 072. Older temp-workspace recovery tests omit an isolated `app_data` argument and therefore observe live product inventory.

The production correction is not rejected by this evidence, but Task 073 cannot be accepted while its explicitly required full-suite gate has failures.

## Current live condition

Preserve the accepted Task-072 healthy installation:

- MANAGED;
- CogentNexus-owned foreground/background runtime;
- no durable Hermes/Codex/temp binding;
- Supervisor PT1M healthy;
- no-flash already proven across five natural ticks;
- Gateway/Ollama/plugin/ownership/AGENTS/SQLite healthy.

## Authorized Task 074 operation

Tests/evidence only. Isolate affected recovery/transaction fixtures from real user application-data by using exact temp `.../CogentNexus-OpenClaw` roots consistently. Restore full pytest to zero failures without weakening production semantics or touching the live installation.

## Live hard fence

No live install/install-over/uninstall/reset/lifecycle action, Scheduled Task/Gateway/Ollama/plugin/config/AGENTS/SQLite mutation, process termination, reboot, HermesAgent mutation, semantic LLM smoke, merge/tag/release.

## Pre-authorized successors

If Task 074 is independently accepted, Task 075 may perform one supported install-over of the accepted Task-073 correction onto the current MANAGED installation and prove source/live parity plus >=3 natural PT1M no-flash ticks.

After Task 075 acceptance, Task 076 may perform the final semantic Ticket -> Ollama -> durable delivery -> response acceptance.
