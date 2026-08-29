# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `LIVE_WINDOWS_RUNTIME_LIFECYCLE_TRANSITION_ACCEPTANCE`  
**Updated:** 2026-08-30 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator requested continuation; Task 149 reset acceptance is independently ACCEPTed and the next narrow live gate is normal runtime lifecycle transition acceptance  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260830-150-runtime-lifecycle-stop-start-restart-disable-enable-acceptance.md`](tasks/CNX-20260830-150-runtime-lifecycle-stop-start-restart-disable-enable-acceptance.md)

Task ID:

`CNX-20260830-150`

## Task-149 accepted result

Report:

`docs/operations/coordination/reports/CNX-20260830-149-proven-launcher-product-reset-fresh-state-retry.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260830-149-proven-launcher-product-reset-fresh-state-retry-review.md`

Disposition: **ACCEPT**.

Accepted production implementation SHA:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

Task 149 proved:

- exactly one real reset invocation with one `y`, exit `0`;
- state/database recreation by changed Windows file identity/creation evidence;
- launcher/skill/plugin release payload preserved exactly;
- fresh `MANAGED` controller with Ollama selected/running;
- healthy Gateway/Ollama/recovery/delivery/SQLite;
- pending `0`, semantic rows `0`, Dashboard Sends `0`.

## Task-150 authority

Task 150 exercises the installed operator-facing runtime controls in one ordered bounded sequence:

`stop → start → restart → disable → enable`

Each command is authorized exactly once and only after the previous phase's read-only verification passes.

Expected boundaries:

- STOP: intentional `maintenance`; Gateway and Ollama verified stopped;
- START: healthy `managed`; product restarts Ollama/Gateway and clears maintenance after verification;
- RESTART: healthy `managed` after a real Gateway process boundary;
- DISABLE: healthy `passthrough`; plugin/interception disabled and native OpenClaw route active;
- ENABLE: healthy `managed`; CNX plugin/policy/route/startup ownership restored.

The installed launcher must be used via:

`cmd.exe /d /c C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd <command>`

If any command or post-state fails, stop immediately. No later phase may be used as a repair path.

## Semantic fence

Task 150 authorizes **zero Dashboard semantic Sends** and no manual Ticket/workflow/outbox/delivery/recovery/database mutation.

## Security maintenance note

The npm audit output observed in Task 147 remains separate maintenance. Do not broaden Task 150 into dependency remediation.

## Prohibited

No reset/uninstall/install/reinstall; no Dashboard Send/resend; no crash/recovery injection; no manual OpenClaw/Ollama/process/task lifecycle; no manual plugin/config/controller/ownership normalization; no lifecycle retry; no unrelated service/process/task mutation; no reboot; no credentials/secrets; no merge/tag/GitHub Release; no force push.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260830-150-runtime-lifecycle-stop-start-restart-disable-enable-acceptance.md`

Then stop for independent ChatGPT review. Final Dashboard durable-delivery acceptance remains a later explicit gate.
