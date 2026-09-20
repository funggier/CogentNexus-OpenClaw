# Coordination Channel Status

Status: `IN_PROGRESS`
State: `CNX427_OPENCLAW95_LIVE_INSTALL_GREEN_FINAL_DISCORD_ACCEPTANCE_READY`
Task ID: `CNX-20260919-427`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`

## OpenClaw 9.5

Live version:

`OpenClaw 2026.9.5 (ec9c1a1)`

Current runtime:

- Gateway health GREEN;
- event loop settled, degraded=false;
- plugin errors 0;
- Discord ready/connected;
- Tailscale Serve active;
- remote HTTPS 200;
- CNX runtime runnerReady=true;
- supervisor Enabled / Last Result 0;
- shared DB v17 quick_check ok;
- agent DB v21 quick_check ok;
- CNX DB v0 quick_check ok.

## CNX-427 Track A

Two live Discord turns on 9.4 proved visible delivery without a CNX Ticket.

Acceptance #1:

- trace `343c6efbf788333b585d1160af9ed4e6`;
- run `a0660423-e586-4e89-a5c9-fca25d842e1d`;
- visible `CNX427_OK`;
- CNX Ticket absent.

Acceptance #2:

- trace `73bfcb525d0fbecc95372ddf49151c44`;
- run `77b8ed7a-f40c-4ac1-86f4-0884656b4e8e`;
- direct DB query: Tickets 0 / events 0 / CNX deliveries 0.

OpenClaw 9.5 contains upstream generation continuity fix `983782594807a23c006b49bd16172b1ba6980924`.

Final semantic acceptance on 9.5 is still pending.

## CNX-436 / CNX-437 final live repair state

The OpenClaw 9.5 post-install lifecycle path is now GREEN.

CNX-436:

- implementation commit `321fda1e5a2564973a9868141413fb73b8c26805`;
- readiness budget = bounded 180 seconds;
- live installer crossed 5 readiness attempts and completed;
- classification `OPENCLAW95_LIFECYCLE_START_READINESS_GREEN`.

CNX-437:

- implementation commit `d67e86ae212222e62bd6eba2e194c1fd78fcf785`;
- Windows subprocess capture now uses explicit UTF-8 + replacement;
- focused regression 5/5 PASS;
- affected Host/session regression 55 PASS with 2 unrelated cases deselected;
- supported install-over terminal exit = 0;
- controller `cnxMode=active`, generation 109;
- plugin loaded by Gateway;
- supervisor Enabled / hidden / Last Result 0;
- Gateway health ok;
- Discord ready/connected;
- no new UnicodeDecodeError / NoneType JSON / transactional rollback after install;
- classification `WINDOWS_UTF8_SUBPROCESS_AND_GATEWAY_TEMP_COMPAT_GREEN`.

OpenClaw's native restart-loop breaker self-recovered after its 300000 ms window drained. No OpenClaw state DB rows were manually deleted.

Current final acceptance baseline:

- Discord session key: `agent:main:discord:channel:1391855033993138217`;
- existing failed physical session: `8fc2e9fe-e413-4979-b7ce-e2baeb960418`;
- current model: `ollama/qwen3.8:27b`;
- CNX Tickets: 44;
- max Ticket event id: 1087;
- direct model calls: 32.

The failed Discord session must be removed before the final one-turn acceptance so the final evidence is unambiguous.

## CNX-428 supervisor cold-start repair

A live OpenClaw 9.5 cold start exposed a separate supervisor defect: the CNX external supervisor used two lightweight Gateway probes separated by one second and interpreted a valid slow cold start as a hard hang.

Measured service-owned 9.5 boot:

- HTTP listener after about 42.4 s;
- event-loop stall around 38 s during `sidecars.model-runtime`;
- `gateway ready` after about 90.7 s.

Repair commit:

`13dfba9a55f4d64ceb9aa8440670c9ee9792354a`

The repaired Host reads OpenClaw `gateway_boot_lifecycle` and applies a bounded 180-second startup/restart grace. A real live boot inside that window returned `gateway-starting`, `action=none`, `heavyPath=false`, and did not invoke restart.

Validation:

- focused Host: 8/8 PASS;
- expanded Python: 44/44 PASS;
- CNX-427 plugin tests: 5/5 PASS;
- full plugin suite: 381/382 PASS, with the sole failure the pre-existing intentional CNX-383 RED.

Recurring supervisor is restored Enabled / Last Result 0, the stale maintenance marker was reconciled, and no new post-repair restart request was observed.

Isolated PID-bound pre-acceptance probe:

- session `agent:main:cnx427-process-probe-1958`;
- run `62a61c83-8c61-446c-9a6d-20b4138dd857`;
- Ticket `CNXT-7a349016-6de3-4f20-bc7a-73c82cca6603`;
- exactly one user turn / one run / one Ticket / one model call;
- Ticket accepted at `12:59:26.475Z`;
- model call started at `12:59:26.521Z`;
- Ticket-first ordering therefore preceded model authority by about 46 ms;
- local `qwen3:1.7b` hit the explicit 90-second provider timeout and terminated `failed` without duplicate/recovery inference.

This proves the 9.5 execution-generation Ticket-first boundary before the genuine Discord final gate.

## OOM finding

The first live 9.5 start crashed because qwen3.8:27b remained loaded in Ollama and llama-server reserved ~22.94 GB private memory, filling the 20 GB pagefile and leaving ~2 GB free commit.

`ollama stop qwen3.8:27b` unloaded it without deleting the model.

After unload, free commit recovered to ~25 GB and live 9.5 became stable.

## Storage relocation

Operator-requested CNX backup relocation is GREEN.

Canonical destination:

`T:\CogentNexus\CogentNexus-OpenClaw`

Current state:

- C: `...\CogentNexus-OpenClaw\backups` -> T: `backups` via NTFS junction;
- C: `...\plugin-generation-rollover-backups` -> T: rollover tree via NTFS junction;
- main backup dry mirror: 509,383 files / 9.479 GiB, zero differences;
- rollover dry mirror: 159,271 files / 1.408 GiB, zero differences;
- authoritative manifest and critical backup hashes matched;
- authoritative reparse topology matched 10 -> 10;
- old rollback paths resolve through the original C: path;
- renamed C: source copies were removed only after fidelity verification and reparse-safe cleanup;
- C: free space recovered from ~13.43 GiB to ~25.48 GiB.

Post-relocation live runtime remains GREEN:

- OpenClaw 2026.9.5;
- Gateway service child PID 30416 after controlled handoff, health ok;
- Discord ready/connected;
- CNX runnerReady=true / globalHookCount=7;
- Tailscale Serve -> 127.0.0.1:12651;
- remote HTTPS 200;
- supervisor Last Result 0;
- `ollama ps` empty;
- free virtual/commit ~20.57 GiB.

Checkpoint:

`docs/operations/coordination/reports/CNX-20260919-427-storage-relocation-and-pre-acceptance-runtime-checkpoint.md`

## Handoff

Read:

`docs/operations/coordination/reports/CNX-20260919-427-full-session-handoff-openclaw-9.5-and-storage-relocation.md`

before continuing.
