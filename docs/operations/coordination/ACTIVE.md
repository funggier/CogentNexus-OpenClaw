# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_CLEAN_REINSTALL_WITH_PRESERVATION_AND_MULTI_TICK_ACCEPTANCE`
Current authorization: `CLEAN_REINSTALL_AND_LIVE_RUNTIME_ACCEPTANCE_AUTHORIZED`
Task ID: `CNX-20260825-066`
Updated: 2026-08-25 20:47 ICT
Owner: ChatGPT
Executor: Hermes after the operator's continuation signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains project narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260825-066-clean-reinstall-owned-runtime-live-acceptance.md`](tasks/CNX-20260825-066-clean-reinstall-owned-runtime-live-acceptance.md)

## Accepted predecessor

Task 065 report result:

`PASS_INSTALLER_RUNTIME_AUTHORITY_GAPS_CLOSED`

Implementation HEAD:

`21686f70520c5e0263e8aea4d644d2c87324e872`

Report HEAD:

`8c74686dfe4c6817e2dcc9cbe27e2a8670c24c76`

Independent review decision:

`ACCEPT`

Disposition:

`ACCEPT_INSTALLER_RUNTIME_AUTHORITY_GAPS_CLOSED`

Review commit:

`f45f3c2c55828114026d07813ad447a5e4048b8e`

## Current live condition

The operator reports the periodic visible window flash still occurs. This is expected at this boundary because Tasks 063-065 were source/tests only and the current live Scheduled Task has not yet been replaced. Treat this as `PRE_REINSTALL_BASELINE`.

## Authorized Task 066 operation

Task 066 may perform the already-authorized bounded live repair:

- fresh preservation/preflight evidence;
- supported clean CogentNexus-OpenClaw uninstall using the product's normal confirmation;
- prove unrelated OpenClaw/Ollama/user/plugin/config state is preserved;
- fresh install from exact reviewed implementation commit `21686f70520c5e0263e8aea4d644d2c87324e872` using the normal Windows installer;
- prove launcher and Scheduled Task bind exact CogentNexus-owned `python.exe` / `pythonw.exe`, with no Hermes/Codex/agent interpreter path;
- observe at least three natural PT1M supervisor ticks with bounded process-start evidence and require no causal `conhost.exe`/console trampoline;
- verify final MANAGED/Gateway/Ollama/plugin/ownership/AGENTS/SQLite health.

No separate confirmation is required for this exact successor because the operator already authorized clean removal and fresh installation.

## Mutation fence

No manual broad deletion, source patching, reboot/power-cycle, provider/model changes, HermesAgent mutation, merge/tag/release, or unrelated OpenClaw/Ollama mutation is authorized.

If supported uninstall/install reveals a product defect, stop and report instead of masking it with manual cleanup.

## Next gate

Hermes publishes only the matching Task 066 report. ChatGPT independently reviews preservation evidence, uninstall/install behavior, exact runtime binding, multi-tick no-flash evidence, post-install health, and publication fence before live repair is accepted.
