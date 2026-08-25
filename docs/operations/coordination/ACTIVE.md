# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_REWORK_TDD_INSTALLER_INTEGRATION`
Current authorization: `INSTALLER_RUNTIME_AUTHORITY_CLOSURE_AUTHORIZED`
Task ID: `CNX-20260825-065`
Updated: 2026-08-25 19:28 ICT
Owner: ChatGPT
Executor: Hermes after the operator's continuation signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains project narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260825-065-close-installer-runtime-authority-gaps.md`](tasks/CNX-20260825-065-close-installer-runtime-authority-gaps.md)

## Predecessor review

Task 064 reported:

`PASS_WINDOWS_RUNTIME_AUTHORITY_REWORK_VERIFIED`

Implementation HEAD:

`6e4245112a38dab3e6614e6f91d3e37ac85f2afe`

Report HEAD:

`f3a4731b87f8a530dd71eed3826a93f963a9de34`

Independent review decision:

`REWORK`

Disposition:

`REWORK_INSTALLER_RUNTIME_AUTHORITY_EXECUTION_GAPS`

Review commit:

`5fe706d89f41083fda37d2032c17bc0ba6e1d353`

Task 064's B1-B3 runtime/startup corrections and the accepted Task 063 `FLASH_CHILD_PROCESS` diagnosis remain useful, but live reinstall is still blocked by production installer integration defects.

## Current defects

Task 065 must close only these remaining runtime-authority gaps:

1. the committed `install.ps1` runtime-authority path contains a literal newline inside `scripts\runtime_authority.py`, which breaks fresh provisioning;
2. installer runtime validation currently runs only when `python.exe` is absent, so a stale runtime with a missing/corrupt manifest or broken background interpreter can bypass repair;
3. post-provision MANAGED enable/status and other stdlib-capable CogentNexus operations still use ambient bare `python` rather than the established owned runtime;
4. prior tests did not exercise the failing production installer-facing boundary.

## Authorized Task 065 operation

Task 065 is source/tests only. It must use strict TDD, correct the production installer path, make runtime ensure/validation unconditional before durable definitions, validate both foreground/background interpreters, transition safe post-provision product calls to `$ownedPython`, and add installer-facing regression coverage that fails against the current Task 064 source.

## Live hard fence

No current install/install-over/uninstall/reset, lifecycle mutation, Scheduled Task change/run/end, Gateway/Ollama/provider/plugin/config/AGENTS/ownership/SQLite write, process termination, primary-workspace Git mutation, merge, tag, or release.

All tests must use isolated/temp boundaries outside the live product root.

## Pre-authorized successor

The operator already authorized definitive repair followed by clean removal and fresh installation.

If Task 065 is independently reviewed and accepted as `PASS_INSTALLER_RUNTIME_AUTHORITY_GAPS_CLOSED`, proceed without another confirmation to a separate bounded clean uninstall/fresh reinstall task, then verify exact CogentNexus-owned launcher/supervisor runtime, no Hermes/agent path, multiple natural supervisor ticks with no recurring console flash, and healthy MANAGED/OpenClaw/Ollama/plugin/ownership/SQLite state.
