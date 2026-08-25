# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_REWORK_TDD_WINDOWS_INTEGRATION`
Current authorization: `RUNTIME_AUTHORITY_REWORK_AUTHORIZED`
Task ID: `CNX-20260825-064`
Updated: 2026-08-25 18:58 ICT
Owner: ChatGPT
Executor: Hermes after the operator's manual continuation signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains project narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260825-064-correct-windows-runtime-authority-integration.md`](tasks/CNX-20260825-064-correct-windows-runtime-authority-integration.md)

## Predecessor review

Task 063 reported:

`PASS_OWNED_RUNTIME_AND_FLASH_FIX_IMPLEMENTED`

Implementation/report commit:

`5962383ac8e16b1336e0af78f659e2f5fa29dd97`

Independent review decision:

`REWORK`

Disposition:

`REWORK_WINDOWS_RUNTIME_AUTHORITY_INTEGRATION_DEFECTS`

Review commit:

`ba4e03ca7d5719075daba23a9dad3a2f89a76bc7`

The accepted Task 063 diagnosis remains `FLASH_CHILD_PROCESS`, but live reinstall is blocked because the source implementation contains Windows runtime-authority defects: invalid `pythonw.exe` Path construction, duplicated application-data-root semantics, and a startup fallback that can re-persist an executor venv.

## Authorized Task 064 operation

Task 064 is source/tests only. It must use strict TDD and executable Windows/temp-boundary integration tests to correct the runtime authority before any live installation change.

Required outcomes include:

- exact `%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python` ownership with no duplicated product directory;
- valid owned `python.exe` and `pythonw.exe` provisioning from a verified non-venv base interpreter;
- Windows startup registration fails closed when owned runtime is missing/corrupt and never falls back to Hermes/Codex/agent `sys.executable`;
- generated launcher and task-definition contracts execute/reference the exact owned interpreters;
- normal non-mutating CogentNexus CLI/control import/start path runs successfully under the owned runtime;
- developer test dependencies are installed only in an isolated test venv and full canonical tests are rerun;
- implementation commit(s) and a separate report-only publication commit.

## Live hard fence

No current CogentNexus lifecycle mutation, install/install-over/uninstall/reset, Scheduled Task change/run/end, Gateway/Ollama/provider/plugin/config/AGENTS/ownership/SQLite write, process termination, primary-workspace Git mutation, merge, tag, or release.

All provisioning tests must use temporary application-data roots outside the live product root.

## Pre-authorized successor

The operator explicitly requested a definitive repair followed by clean removal and fresh installation.

If Task 064 is independently reviewed and accepted as `PASS_WINDOWS_RUNTIME_AUTHORITY_REWORK_VERIFIED`, a separate successor may clean-uninstall the current installation and fresh-install the reviewed corrected build without asking for additional confirmation, while preserving unrelated OpenClaw/Ollama/user state and verifying no Hermes dependency or recurring console flash across natural supervisor ticks.
