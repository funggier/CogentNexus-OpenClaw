# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Updated:** 2026-08-25 18:58 ICT
**Transport:** GitHub repository history
**Human authority:** operator authorized definitive owned-runtime/flash repair and subsequent clean uninstall/fresh reinstall
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Task 063 review

Task 063 report result:

`PASS_OWNED_RUNTIME_AND_FLASH_FIX_IMPLEMENTED`

Implementation/report commit:

`5962383ac8e16b1336e0af78f659e2f5fa29dd97`

Independent review decision:

`REWORK`

Disposition:

`REWORK_WINDOWS_RUNTIME_AUTHORITY_INTEGRATION_DEFECTS`

Review commit:

`ba4e03ca7d5719075daba23a9dad3a2f89a76bc7`

### Accepted Task 063 evidence

The bounded live process trace is accepted as:

`FLASH_CHILD_PROCESS`

The currently installed Hermes/uv venv `pythonw.exe` path produces console-subsystem child/base-Python transitions and `conhost.exe` on natural PT1M supervisor ticks. Task 063 did not mutate the live installation.

### Blocking implementation findings

Task 063 source cannot be installed live yet:

1. Windows `runtime_authority._interpreter_paths()` divides a `Path` by the tuple `("pythonw.exe",)`, which breaks real Windows background-interpreter provisioning.
2. installer passes an already-complete `%LOCALAPPDATA%\CogentNexus-OpenClaw` root to a CLI surface that treats the value as `LOCALAPPDATA` and appends `CogentNexus-OpenClaw` again; fresh provisioning and installer validation target different directories.
3. `startup.py::python_background()` silently falls back to registration-time `sys.executable`/sibling `pythonw.exe` on owned-runtime failure, recreating the original Hermes/Codex/agent-venv persistence defect.
4. focused tests relied too heavily on source-string assertions and did not execute the failing Windows provisioning/startup integration paths. The full unittest environment also lacked `pytest` imports.

Therefore the pre-authorized clean reinstall gate is not satisfied yet.

## Active Task 064

[`tasks/CNX-20260825-064-correct-windows-runtime-authority-integration.md`](tasks/CNX-20260825-064-correct-windows-runtime-authority-integration.md)

Status: `READY_FOR_HERMES`

Authorization: `RUNTIME_AUTHORITY_REWORK_AUTHORIZED`

Execution mode: `SOURCE_REWORK_TDD_WINDOWS_INTEGRATION`

Task 064 must correct B1-B4 with strict RED/GREEN TDD and real temporary Windows runtime provisioning outside the live product root. It must prove the exact product-root contract, valid foreground/background interpreters, manifest ancestry validation, startup fail-closed behavior, exact owned task/launcher command generation, and a non-mutating CogentNexus CLI/control start/import under the owned runtime.

Developer dependencies from `requirements-dev.txt` must be installed only in an isolated test environment; focused and complete repository tests/canonical validators must be rerun fresh.

Implementation/tests must be committed separately from a final report-only commit.

## Live hard fence

No current install/install-over/uninstall/reset, `cnxclaw` lifecycle mutation, Scheduled Task create/update/delete/run/end, Gateway/Ollama/provider/plugin/config/AGENTS/ownership/SQLite mutation, process termination, primary workspace Git mutation, merge/tag/release, or HermesAgent project change is authorized in Task 064.

## Next gate

If Task 064 reports `PASS_WINDOWS_RUNTIME_AUTHORITY_REWORK_VERIFIED`, ChatGPT must independently inspect the source diff, executable Windows integration evidence, focused/full tests, and report-only publication fence.

Only after that acceptance does the operator's pre-authorization permit the next bounded task to clean-uninstall the current CogentNexus-OpenClaw and fresh-install the reviewed corrected build, then verify no Hermes dependency and no recurring visible console flash across natural supervisor ticks.
