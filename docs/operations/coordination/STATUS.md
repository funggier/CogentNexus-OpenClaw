# Coordination Channel Status

Status: `IN_PROGRESS`
State: `CNX427_STORAGE_RELOCATION_GREEN_FINAL_DISCORD_ACCEPTANCE_PENDING`
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
- Gateway PID 29604, health ok;
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
