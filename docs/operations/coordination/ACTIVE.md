# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_RUNTIME_LIFECYCLE_TRANSITION_ACCEPTANCE`
Current authorization: `CNX-20260830-150_RUNTIME_LIFECYCLE_STOP_START_RESTART_DISABLE_ENABLE_ACCEPTANCE`
Task ID: `CNX-20260830-150`
Updated: 2026-08-30 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative. A stale local checkout must not be used as coordination truth.

## Active task

[`tasks/CNX-20260830-150-runtime-lifecycle-stop-start-restart-disable-enable-acceptance.md`](tasks/CNX-20260830-150-runtime-lifecycle-stop-start-restart-disable-enable-acceptance.md)

Task 150 is the real-Windows acceptance of the normal operator-facing runtime transition sequence `stop → start → restart → disable → enable` on the accepted fresh installation.

## Task-149 disposition

Task-149 report:

`docs/operations/coordination/reports/CNX-20260830-149-proven-launcher-product-reset-fresh-state-retry.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260830-149-proven-launcher-product-reset-fresh-state-retry-review.md`

Review disposition: **ACCEPT**.

Task 149 proved one real `cnxclaw.cmd reset` + one `y`, exit `0`, with changed controller/SQLite file identities proving fresh state recreation while launcher/skill/plugin accepted provenance remained installed and exact. Runtime returned to healthy fresh `MANAGED` Ollama operation with semantic counts `0` and Dashboard Sends `0`.

Accepted production implementation remains:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

## Task-150 execution contract

Use the installed launcher with the proven command shape only:

`cmd.exe /d /c C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd <command>`

Execute exactly once each, in order:

1. `stop`
2. `start`
3. `restart`
4. `disable`
5. `enable`

Verify the expected state after each command before proceeding. Stop on the first command/state failure; no retry or manual repair.

Expected high-level states:

- STOP: `maintenance`, Gateway stopped, Ollama stopped;
- START: `managed`, Gateway/Ollama running and healthy;
- RESTART: `managed`, real Gateway process boundary then healthy;
- DISABLE: `passthrough`, CNX plugin/interception disabled, native OpenClaw healthy;
- ENABLE: `managed`, CNX plugin/policy/route restored, Gateway/Ollama healthy.

Across all phases preserve accepted provenance, database integrity, semantic counts and Dashboard semantic Send count `0`.

## Required completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260830-150-runtime-lifecycle-stop-start-restart-disable-enable-acceptance.md`

Then stop for independent ChatGPT review.

## Hard fence

No Dashboard semantic Send/resend; no reset/uninstall/install/reinstall; no crash/recovery injection; no manual semantic/database mutation; no manual OpenClaw/Ollama/process/task lifecycle; no manual plugin/config/controller/ownership normalization; no lifecycle retry; no unrelated service/process/task mutation; no reboot; no credentials/secrets; no merge/tag/release; no force push.
