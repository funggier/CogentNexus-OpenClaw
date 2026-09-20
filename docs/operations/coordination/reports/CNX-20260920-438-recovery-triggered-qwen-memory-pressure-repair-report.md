# CNX-20260920-438 — Recovery-Triggered Qwen Memory Pressure Repair Report

Classification:

`RECOVERY_TRIGGERED_QWEN_MEMORY_PRESSURE_REPAIRED_GREEN`

## Summary

The apparent Dashboard outage and failed qwen3.8 load were caused by OpenClaw main-session restart recovery resuming the interrupted final Discord acceptance turn.

The recovered turn created one valid CNX Ticket-first lineage, then loaded qwen3.8:27b with the configured 262144-token context. On this 32 GB/iGPU host the resulting Ollama memory pressure starved the OpenClaw Gateway event loop and made the Dashboard effectively unusable.

The recovered run was cancelled through supported `sessions.abort`, the model unloaded, and Dashboard/Gateway responsiveness returned immediately.

## Live context repair

qwen3.8 was tested at two lower context caps:

- 65536: still unsafe; free physical RAM dropped to about 0.6 GB;
- 32768: isolated one-token load completed successfully in about 22.46 seconds and unloaded cleanly.

Current live OpenClaw model config:

- `contextWindow=32768`;
- `params.num_ctx=32768`.

The model remains exactly:

`ollama/qwen3.8:27b`

## Session/Ticket cleanup

The recovery-created Discord session was deleted through OpenClaw's supported session lifecycle.

CNX persisted:

- Ticket terminal state `cancelled`;
- `cancelled_by_session_delete` event;
- deleted session authority generation 6;
- no remaining direct-recovery row.

Historical active call/attempt rows are terminal-Ticket fenced and cannot be claimed by Host recovery because the claim query requires Ticket status `accepted`.

## Dashboard proof

After abort/unload:

- local Dashboard HTTP: 200;
- Tailscale Dashboard HTTPS: 200;
- Gateway event loop: degraded=false;
- Discord: ready/connected;
- activeRuns=0.

## Evidence directory

`T:\CogentNexus\CogentNexus-OpenClaw\diagnostics\CNX-20260920-438`

contains:

- pre-change config backup;
- 64k load-test script;
- 32k load-test script;
- recovery Ticket inspection;
- recovery cleanup verification;
- fresh baseline probe.

## Final state

The target Discord session is absent and the host is ready for a new one-turn CNX-427 acceptance using qwen3.8:27b at a memory-safe 32768 context cap.
