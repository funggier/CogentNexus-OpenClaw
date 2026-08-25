# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_FIX_WITH_READ_ONLY_FLASH_DIAGNOSIS`
Current authorization: `OWNED_RUNTIME_AND_FLASH_FIX_AUTHORIZED`
Task ID: `CNX-20260825-063`
Updated: 2026-08-25 18:15 ICT
Owner: ChatGPT
Executor: Hermes after the operator's manual continuation signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains project narrative and is not a Task 063 execution gate.

## Active task

[`tasks/CNX-20260825-063-own-supervisor-runtime-and-eliminate-console-flash.md`](tasks/CNX-20260825-063-own-supervisor-runtime-and-eliminate-console-flash.md)

## Accepted predecessor

Task 062 result:

`DIAGNOSIS_COMPLETE_ROOT_CAUSE_BOUND`

Task 062 report commit:

`13ee5ddb5d88a9deb657f325026611286b1b2e33`

Task 062 review disposition:

`ACCEPT_DIAGNOSIS_ROOT_CAUSE_BOUND_WITH_MULTI_REBOOT_SCOPE_CORRECTION`

Task 062 review commit:

`28947721cb002304d638536c5c143e919116ad77`

Task 062 bound F1 to managed-block blank-line strip verification and F2 to `CONFIG_READ_SURFACE_MISMATCH`. No live AGENTS/config repair is required.

## Current defect

The live Windows supervisor task is durably coupled to:

`C:\Users\CDQ-P\AppData\Local\hermes\hermes-agent\venv\Scripts\pythonw.exe`

because startup registration persists registration-time `sys.executable` semantics. The operator also reports a recurring visible window/console flash correlated with the periodic supervisor cadence.

CogentNexus must not depend on Hermes/another executor venv for durable runtime ownership, and periodic supervision must be genuinely background/no-console.

## Authorized Task 063 operation

Task 063 may:

- observe at least two natural supervisor intervals with a bounded read-only process-start trace to bind the flashing process;
- edit only a fresh isolated repository clone;
- use strict TDD to implement a CogentNexus-owned Python runtime authority under the product application-data boundary;
- update installer/launcher/startup ownership so durable execution does not use ambient bare `python` or registration-time arbitrary venv paths;
- harden Windows subprocess creation on the healthy supervisor path where evidence/source audit requires it;
- add/update tests for runtime provisioning, launcher/startup binding, no-console semantics, uninstall/reset/install-over ownership;
- run focused/full tests and validations;
- publish only the matching Task 063 report.

## Live hard fence

Task 063 must not modify the current installation, Scheduled Task, Gateway, Ollama, plugin/config, AGENTS, ownership, SQLite, or lifecycle state. No install-over/uninstall/reinstall occurs until ChatGPT reviews the source report.

## Pre-authorized successor

The operator explicitly requested a definitive repair followed by clean removal and fresh installation.

If Task 063 source implementation is reviewed and accepted, a separate successor is already authorized to perform a bounded supported clean uninstall and reinstall of the reviewed fixed release path, then verify:

- no Hermes/agent venv dependency;
- CogentNexus-owned launcher and supervisor runtime;
- no recurring visible console/window flash across multiple natural supervisor ticks;
- preserved unrelated OpenClaw/Ollama/user state;
- healthy MANAGED/plugin/Gateway/Ollama/ownership/SQLite state.

No additional operator confirmation is required for that exact bounded successor.
