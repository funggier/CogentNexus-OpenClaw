# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Updated:** 2026-08-26 18:29 ICT
**Transport:** GitHub repository history
**Human authority:** operator authorized definitive repair through final live/semantic acceptance
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Task 073 report/review

Task 073 reported:

`PASS_CLEAN_FRESH_RECOVERY_PREFLIGHT_CORRECTED`

Implementation HEAD:

`79b51ed06363f6e8862c491ee0a313ddb412c806`

Report HEAD:

`ba4a04825fb7396617fa0fe17c62f84f5f5e1507`

Independent review:

Decision `REWORK`

Disposition:

`REWORK_FULL_SUITE_LIVE_APPDATA_FIXTURE_COUPLING`

Review commit:

`6fc24cc44b66afa8411cafb2c2e31d34c7572dce`

### Accepted production correction candidate

Independent source inspection accepts the Task-073 production behavior as the current correction candidate:

- clean markerless/no-inventory preflight returns `CLEAN_FRESH`;
- unmarked partial residue remains fail-closed;
- valid incomplete recovery and ownership-present semantics remain intact;
- installer captures recovery-preflight exit/output and stops before classification on nonzero;
- successful status is explicitly allowlisted and unknown success fail-closes;
- recovery preflight remains before classification and fresh transaction begin.

Publication fence also passed: implementation scope is production correction plus focused tests; report publication is report-only.

### Blocking regression-suite issue

Task 073 explicitly required full `pytest tests/ -q`, but its report records four failures. The failures reproduce on the predecessor checkout as well and are caused by older temp-workspace tests omitting an isolated application-data boundary. Production therefore uses the real `%LOCALAPPDATA%\CogentNexus-OpenClaw` default, which now exists because Task 072 validly installed the product.

This is test-environment coupling, not evidence that the new recovery semantics are wrong, but the full-suite acceptance gate is not green and cannot be waived.

## Current live baseline

Task 072 remains accepted and healthy:

- controller MANAGED;
- durable launcher/Supervisor use CogentNexus-owned runtime under `%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python`;
- no durable Hermes/Codex/temp binding;
- five natural PT1M ticks already proved `NO_FLASH_MULTI_TICK_PROVEN`;
- Gateway/Ollama/plugin/config/ownership/AGENTS/SQLite healthy;
- no semantic product smoke has been run yet.

## Active Task 074

[`tasks/CNX-20260826-074-isolate-recovery-tests-from-live-appdata.md`](tasks/CNX-20260826-074-isolate-recovery-tests-from-live-appdata.md)

Status: `READY_FOR_HERMES`

Authorization: `RECOVERY_TEST_ISOLATION_AUTHORIZED`

Execution mode: `TEST_ONLY_TDD_LIVE_APPDATA_ISOLATION`

Task 074 must isolate affected recovery/transaction tests from the real user application-data root, preserve the accepted Task-073 production correction, and restore full pytest to zero failures while the live Task-072 installation remains present and untouched.

## Live hard fence

No install/install-over/uninstall/reset/lifecycle action, Scheduled Task/Gateway/Ollama/plugin/config/AGENTS/SQLite mutation, process termination, reboot, HermesAgent mutation, semantic LLM smoke, merge/tag/release.

## Next gates

After Task 074 acceptance, Task 075 may perform one supported install-over from the exact accepted Task-073 production correction and re-prove source/live parity, owned runtime/MANAGED health and >=3 natural PT1M no-flash ticks.

After Task 075 acceptance, Task 076 performs the final semantic flow:

`user message -> durable Ticket -> Ollama LLM -> durable result/delivery -> user-visible response`.
