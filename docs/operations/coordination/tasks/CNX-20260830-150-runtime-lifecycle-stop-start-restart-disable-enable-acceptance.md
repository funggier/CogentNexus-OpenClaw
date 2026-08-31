# CNX-20260830-150 — Runtime Lifecycle Stop/Start/Restart/Disable/Enable Acceptance

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_RUNTIME_LIFECYCLE_TRANSITION_ACCEPTANCE`
Owner: ChatGPT
Executor: Hermes/Codex on the operator's real Windows machine

## Purpose

Prove the accepted fresh installation's normal operator-facing runtime transitions on the real Windows machine, in one bounded ordered sequence:

1. `cnxclaw.cmd stop`
2. `cnxclaw.cmd start`
3. `cnxclaw.cmd restart`
4. `cnxclaw.cmd disable`
5. `cnxclaw.cmd enable`

This task does not test reset/uninstall/install, crash recovery, Ticket inference, or Dashboard semantic delivery.

## Accepted source and starting boundary

Accepted production SHA:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

Task 149 review disposition: **ACCEPT**.

Task 149 last proved a fresh reset state with:

- controller `MANAGED`;
- desired Gateway/provider `running` / `running`;
- selected provider `ollama`;
- singular canonical non-reparse plugin, version `0.9.3`, enabled/loaded;
- accepted plugin fingerprint and ownership-helper hash exact;
- ownership verification PASS;
- Gateway healthy on `127.0.0.1:18789`;
- Ollama healthy/ready;
- recovery/delivery `READY`, pending `0`;
- SQLite `ok`;
- semantic counts all `0`;
- Dashboard semantic Sends `0`.

Re-verify material state read-only before the first transition. Do not normalize drift.

## Remote authority

Before mutation:

1. fetch `agent/v0.9.3-full-stabilization` from GitHub;
2. verify `ACTIVE.md` and `STATUS.md` still authorize this exact Task 150;
3. verify no matching Task-150 report already exists;
4. preserve uncertain local checkouts; GitHub remote is authority;
5. do not merge, rebase, tag, release, or force-push.

## General execution rules

Use the installed launcher at:

`C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd`

Use the Task-147-proven Windows command form:

`cmd.exe /d /c C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd <command>`

Each lifecycle command is authorized **exactly once** and only in the required order. There is no retry.

After each successful command, capture read-only state and verify that phase's contract before proceeding. If a command exits nonzero or the resulting state is incoherent, stop immediately and report the first failing phase. Do not attempt later commands to repair or normalize it.

No manual `openclaw gateway ...`, `ollama ...`, Task Scheduler lifecycle, plugin enable/disable, controller edit, config edit, or process kill/start is allowed outside what the CNX product command itself performs.

## Phase A — preflight

Capture read-only evidence for:

- `cnxclaw status`;
- ownership verify;
- OpenClaw plugin inventory/runtime state;
- plugin root non-reparse attestation;
- accepted plugin fingerprint and ownership-helper hash;
- Gateway process/listener/health and PID where available;
- OpenClaw version;
- selected provider and Ollama health/process evidence;
- supervisor/Gateway scheduled-task state;
- recovery and delivery checks;
- SQLite read-only integrity and semantic counts;
- managed/native OpenClaw route evidence sufficient to compare disable/enable;
- managed-policy presence in `AGENTS.md` and watchdog compatibility snapshot/value where safely inspectable;
- Dashboard semantic Send count `0`.

If material drift makes the sequence unsafe, publish `BLOCKED` and stop before mutation.

## Phase B — STOP

Invoke exactly once:

`cmd.exe /d /c C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd stop`

Expected product contract:

- exit code `0`;
- controller mode `maintenance`;
- `desiredGateway=stopped`;
- `desiredProvider=stopped`;
- runtime maintenance marker active/manual;
- Gateway verified stopped/not healthy and loopback listener absent;
- Ollama verified stopped/not healthy because normal `stop` requests provider shutdown;
- supervisor does not autonomously restart runtime while intentional maintenance is active;
- plugin/program/ownership files remain installed;
- semantic DB remains intact with no new Ticket/model/delivery/session rows;
- Dashboard Sends remain `0`.

If any STOP criterion fails, report `FAIL_STOP` and stop. Do not run START.

## Phase C — START

Only after STOP passes, invoke exactly once:

`cmd.exe /d /c C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd start`

Expected contract:

- exit code `0`;
- controller returns to `managed`;
- `desiredGateway=running`;
- `desiredProvider=running`;
- intentional maintenance marker clears only after runtime health verification;
- Ollama is started/recovered by the product and becomes healthy/ready;
- Gateway becomes healthy and loopback-only on `127.0.0.1:18789`;
- plugin remains canonical and enabled/loaded;
- selected provider remains Ollama;
- recovery/delivery return/remain `READY`, pending `0`;
- SQLite remains `ok` and semantic counts remain unchanged;
- Dashboard Sends remain `0`.

If START fails, report `FAIL_START` and stop. Do not run RESTART.

## Phase D — RESTART

Only after START passes, record the pre-restart Gateway PID/process identity, then invoke exactly once:

`cmd.exe /d /c C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd restart`

Expected contract:

- exit code `0`;
- controller remains/returns `managed` with desired Gateway running;
- a real Gateway restart boundary occurs; prove by PID/process-start identity change or equivalent authoritative process evidence;
- Gateway becomes healthy on loopback after the boundary;
- Ollama remains healthy/ready;
- maintenance/restart marker does not remain stale after health verification;
- plugin remains enabled/loaded and exact;
- recovery/delivery `READY`, pending `0`;
- semantic counts unchanged and Dashboard Sends `0`.

If RESTART fails, report `FAIL_RESTART` and stop. Do not run DISABLE.

## Phase E — DISABLE

Only after RESTART passes, invoke exactly once:

`cmd.exe /d /c C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd disable`

Expected contract from the installed source:

- exit code `0`;
- controller mode `passthrough`;
- `desiredGateway=running`;
- CNX plugin is disabled/not activated;
- CNX managed policy block is removed from active `AGENTS.md` while the registered policy snapshot remains preserved;
- CNX-managed OpenClaw route/watchdog/compat fields are restored to their native/operator-owned boundary where applicable;
- provider-event adapter is stopped/released;
- native OpenClaw Gateway is restarted/reloaded and healthy;
- OpenClaw remains usable without CNX interception;
- Ollama/provider installation is not uninstalled or destructively altered;
- CNX state/database remains present and structurally valid;
- semantic counts unchanged and Dashboard Sends `0`.

If DISABLE fails, report `FAIL_DISABLE` and stop. Do not run ENABLE.

## Phase F — ENABLE

Only after DISABLE passes, invoke exactly once:

`cmd.exe /d /c C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd enable`

Expected contract:

- exit code `0`;
- controller mode `managed`;
- desired Gateway/provider `running` / `running`;
- selected provider Ollama;
- CNX managed policy block is applied again;
- plugin becomes enabled/activated/loaded;
- CNX managed route/watchdog compatibility is applied without overwriting unexpected operator drift;
- startup/supervisor integration is enabled and coherent;
- Gateway has a verified process boundary and is healthy loopback-only;
- Ollama healthy/ready;
- ownership/provenance remain exact accepted candidate;
- recovery/delivery `READY`, pending `0`;
- SQLite `ok`, semantic counts unchanged;
- no stale transition/maintenance residue;
- Dashboard semantic Sends remain `0`.

If ENABLE fails, report `FAIL_ENABLE` and stop.

## PASS criteria

`PASS` requires all five transitions to execute once and verify in order:

- STOP → intentional MAINTENANCE with Gateway/Ollama stopped;
- START → healthy MANAGED Gateway/Ollama operation;
- RESTART → real healthy Gateway process boundary;
- DISABLE → healthy native PASSTHROUGH with CNX interception disabled;
- ENABLE → healthy MANAGED CNX operation restored.

Across the full sequence:

- no manual repair/retry/alternate lifecycle path;
- installed accepted provenance remains exact;
- durable database integrity is preserved;
- no unintended semantic Ticket/model/delivery activity;
- Dashboard semantic Sends remain `0`.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260830-150-runtime-lifecycle-stop-start-restart-disable-enable-acceptance.md`

The report must include:

- exact remote authority HEAD;
- exact command/count/exit for each phase;
- before/after controller state;
- Gateway/Ollama process and health evidence;
- maintenance marker evidence;
- plugin/policy/route/watchdog/startup evidence for disable/enable;
- ownership/provenance evidence;
- recovery/delivery/SQLite/semantic-count evidence;
- side-effect accounting;
- verdict exactly one of `PASS`, `FAIL_STOP`, `FAIL_START`, `FAIL_RESTART`, `FAIL_DISABLE`, `FAIL_ENABLE`, `BLOCKED`;
- unproven items.

Then stop for independent ChatGPT review.

## Hard fence

No Dashboard semantic Send/resend; no Ticket/workflow/outbox/delivery/recovery semantic mutation; no reset/uninstall/install/reinstall; no crash/recovery injection; no manual OpenClaw/Ollama/process/task lifecycle; no manual plugin/config/controller/ownership normalization; no lifecycle retry; no unrelated service/process/task mutation; no reboot; no credentials/secrets; no merge/tag/release; no force push.
