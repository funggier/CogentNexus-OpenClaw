# Active Coordination Task

Status: `READY_FOR_HERMES_RESUME`
Execution mode: `LIVE_CLEAN_REINSTALL_WITH_PRESERVATION_AND_MULTI_TICK_ACCEPTANCE`
Current authorization: `CLEAN_REINSTALL_AND_LIVE_RUNTIME_ACCEPTANCE_AUTHORIZED`
Task ID: `CNX-20260825-066`
Updated: 2026-08-25 23:08 ICT
Owner: ChatGPT
Executor: fresh Hermes session after the operator's continuation signal

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

## Executor-context interruption

The prior Hermes session stopped during Task 066 after its model context became too large for the primary provider (`Request too large for gpt-5.6-luna in organization`). The configured local fallback `qwen3.5:9b` also stalled under the oversized session. No Task 066 report was published before the interruption.

The last operator-visible Hermes progress was successful Task 066 preflight followed by entry into Phase A evidence gathering. Do **not** infer from that message alone that no later side effect occurred.

A fresh Hermes session must resume from durable coordination truth, not from the exhausted conversational context. Before any uninstall/install/lifecycle side effect, it must independently inspect the current live machine and determine which Task 066 phase, if any, actually completed. Never repeat an already-completed disruptive effect.

## Current live condition

The operator previously reported the periodic visible window flash before Task 066. Tasks 063-065 were source/tests only, so this was classified as `PRE_REINSTALL_BASELINE`.

On resume, re-observe current Scheduled Task/runtime binding first; do not assume the old installation still exists and do not assume the fresh installation exists.

## Authorized Task 066 operation

Task 066 remains authorized to perform the bounded live repair once current phase is re-established:

- fresh preservation/preflight evidence where still needed;
- supported clean CogentNexus-OpenClaw uninstall using the product's normal confirmation, only if not already completed;
- prove unrelated OpenClaw/Ollama/user/plugin/config state is preserved;
- fresh install from exact reviewed implementation commit `21686f70520c5e0263e8aea4d644d2c87324e872`, only if not already completed;
- prove launcher and Scheduled Task bind exact CogentNexus-owned `python.exe` / `pythonw.exe`, with no Hermes/Codex/agent interpreter path;
- observe at least three natural PT1M supervisor ticks with bounded process-start evidence and require no causal `conhost.exe`/console trampoline;
- verify final MANAGED/Gateway/Ollama/plugin/ownership/AGENTS/SQLite health.

No separate confirmation is required for this exact successor because the operator already authorized clean removal and fresh installation.

## Mutation fence

No manual broad deletion, source patching, reboot/power-cycle, provider/model changes, HermesAgent mutation, merge/tag/release, or unrelated OpenClaw/Ollama mutation is authorized.

If supported uninstall/install reveals a product defect, stop and report instead of masking it with manual cleanup.

## Next gate

Hermes publishes only the matching Task 066 report. ChatGPT independently reviews preservation evidence, uninstall/install behavior, exact runtime binding, multi-tick no-flash evidence, post-install health, and publication fence before live repair is accepted.
