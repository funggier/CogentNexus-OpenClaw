# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_SUPPORTED_INSTALL_OVER_SOURCE_PARITY_OWNED_RUNTIME_NO_FLASH`
Current authorization: `SUPPORTED_INSTALL_OVER_PARITY_ACCEPTANCE_AUTHORIZED`
Task ID: `CNX-20260826-075`
Updated: 2026-08-26 18:29 ICT
Owner: ChatGPT
Executor: Hermes after the operator's continuation signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260826-075-install-over-source-live-parity-no-flash.md`](tasks/CNX-20260826-075-install-over-source-live-parity-no-flash.md)

## Task 074 review

Task 074 reported:

`PASS_RECOVERY_TESTS_ISOLATED_FROM_LIVE_APPDATA`

Test-only implementation HEAD:

`8fc2f4640a761204e9614d2a2fbcfb55cc23d311`

Report HEAD:

`545fc3e6f989e8423ba4e94acc3fe9c60b0fa827`

Independent review decision:

`ACCEPT`

Disposition:

`ACCEPT_RECOVERY_TESTS_ISOLATED_AND_TASK073_PRODUCTION_CORRECTION_RELEASED`

Review commit:

`7a28292007b96d972e4aa71bc1f0f31f23d5da11`

## Accepted production source for live install-over

`79b51ed06363f6e8862c491ee0a313ddb412c806`

Task 074 changed tests only and closes the sole full-suite blocker on the Task-073 production correction.

Accepted verification now includes:

- recovery semantics/fail-closed installer correction;
- full pytest `356 passed, 2 skipped, 0 failed` while the real Task-072 live app-data root remains present and unchanged;
- npm 11/npm 12 gates;
- exact OpenClaw `2026.7.1-2`, plugin `0.9.3`;
- upgrade/legacy/fresh transaction regressions.

## Current live baseline

Preserve the accepted Task-072 healthy MANAGED installation until Task 075 preflight proves it:

- CogentNexus-owned runtime;
- no durable Hermes/Codex/temp binding;
- Supervisor PT1M;
- five natural ticks already proved no flash;
- Gateway/Ollama/plugin/config/ownership/AGENTS/SQLite healthy.

## Authorized Task 075 operation

Exactly one supported install-over from exact production source `79b51ed...`; no uninstall, reset or manual cleanup. Then prove upgrade-path/source-live parity, canonical plugin generation/ownership, owned runtime, final MANAGED health and at least three natural PT1M no-flash ticks.

## Hard fences

No uninstall/reset/manual cleanup, no reboot, no provider/model/OpenClaw change, no source edits, no HermesAgent mutation, no semantic product LLM smoke, no merge/tag/release. Never repeat a completed install-over after interruption; inspect actual live state first.

## Pre-authorized successor

If Task 075 is independently accepted, Task 076 may perform the final semantic Ticket -> Ollama -> durable result/delivery -> response acceptance.
