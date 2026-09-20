# CNX-20260920-438 — Recovery-Triggered Qwen Memory Pressure and Safe Context Cap

Status: `COMPLETE`

Parent: `CNX-20260919-427`

## Trigger

After the operator deleted the Discord owner session in preparation for the final CNX-427 acceptance, OpenClaw main-session restart recovery reconstructed the interrupted Discord turn and resumed it automatically.

The recovered prompt contained the queued final acceptance message:

`CNX427_FINAL_20260920_0933 — ตอบว่า CNX427_FINAL_OK`

plus OpenClaw's interrupted-turn recovery instruction.

This recovery path created a new CNX Ticket and started Ollama `qwen3.8:27b` with a 262144-token context.

## Exact recovery lineage

Session:

`agent:main:discord:channel:1391855033993138217`

Physical session:

`38ef9799-a8ed-49fb-963c-aad35519a771`

Admission run:

`9000715c-c8db-4d2c-b040-6663f8235d33`

Ticket:

`CNXT-26e773e3-9506-4bfb-8ee0-4ec16fea9661`

Timeline:

- 02:45:37.014Z — admission trace started;
- 02:45:37.035Z — Ticket persisted;
- 02:45:37.112Z — direct model call started;
- 02:45:37.126Z — inference attempt started;
- 02:45:37.254Z — Ollama llama-server started;
- 02:45:37.733Z — OpenClaw logged `started interrupted main session`;
- recovery startup summary: `started=1 settled=0 failed=0 skipped=0`.

## Memory-pressure proof

The recovery-launched llama-server used:

- model: `qwen3.8:27b`;
- quantization: Q4_K_M;
- context: `-c 262144`;
- KV cache: q8_0 K/V;
- batch: 2048.

Observed during the failed recovery:

- llama-server working set reached about 15.5 GB;
- private memory reached about 28.2 GB;
- free physical RAM fell to about 3.9 GB;
- free virtual memory fell to about 6.3 GB.

At the same time OpenClaw Gateway event-loop health degraded:

- utilization = 1.0;
- P99 delay about 11.5 seconds;
- CPU ratio about 0.91.

The Dashboard HTTP root still answered 200, but WebSocket/UI responsiveness was effectively starved.

## Supported recovery cancellation

The active recovered run was stopped through OpenClaw's supported RPC:

`sessions.abort`

with:

- exact Discord session key;
- `clearQueued=true`.

RPC result:

- status: `aborted`;
- aborted run id: `3157ac3e-2699-412b-a47a-e9eedc79241b`.

The llama-server exited after cancellation.

Post-abort:

- free physical RAM recovered to about 19.7–21.9 GB;
- Gateway event loop returned to `degraded=false`;
- Discord returned ready/connected with `activeRuns=0`;
- local Dashboard HTTP 200;
- Tailscale Dashboard HTTPS 200.

## Context-cap diagnosis

OpenClaw live config explicitly defined qwen3.8 as:

- `contextWindow=262144`;
- `params.num_ctx=262144`.

This was not merely model metadata; Ollama received the full 262144 context on load.

A backup of the pre-change OpenClaw config was written to:

`T:\CogentNexus\CogentNexus-OpenClaw\diagnostics\CNX-20260920-438\context-cap-20260920T095225\openclaw.json`

with source/backup SHA-256 parity.

## 64k qualification

The live config was first reduced to 65536 without Gateway restart.

An isolated Ollama load test outside OpenClaw/CNX confirmed `-c 65536`.

However, during load:

- free physical RAM fell as low as about 0.6 GB;
- this breached the safety threshold.

The isolated test was terminated and `ollama stop qwen3.8:27b` unloaded the model.

Conclusion:

`65536` remains too aggressive for this 32 GB / iGPU host.

## 32k qualification

The live qwen3.8 config was reduced again to:

- `contextWindow=32768`;
- `params.num_ctx=32768`.

The change hot-reloaded without Gateway restart.

An isolated Ollama test used:

- model `qwen3.8:27b`;
- `num_ctx=32768`;
- `num_predict=1`;
- `keep_alive=0`.

Result:

- exit code 0;
- total duration about 22.46 s;
- model load duration about 21.02 s;
- exactly one generated token;
- llama-server unloaded after the request.

Observed during the early load phase:

- llama-server working set about 7.8 GB;
- free physical RAM about 15.4 GB.

After completion/unload, free physical RAM recovered to about 16.9–21.4 GB.

This qualifies 32768 as the current safe operational context cap for qwen3.8:27b on this host.

## Recovery-session cleanup

The recovered Discord session was deleted through supported OpenClaw lifecycle:

`openclaw sessions delete <exact-key>`

Dry-run result:

`would_delete`

Actual result:

`deleted`

The transcript was archived by OpenClaw.

CNX session-delete hook evidence:

- Ticket `CNXT-26e773e3-9506-4bfb-8ee0-4ec16fea9661` -> `cancelled`;
- event `cancelled_by_session_delete` persisted as event 1101;
- CNX owner session -> state `deleted`, generation 6;
- `cnx_direct_recovery` row absent after deletion.

The historical direct-model-call and inference-attempt rows still carry `active` state, but they are safely fenced:

- owning Ticket status is `cancelled`;
- Host stall claim query requires `t.status='accepted'` before it can claim an active/recovering model-call row.

Therefore these historical rows cannot authorize another inference recovery.

## Fresh post-repair baseline

Target Discord session is absent from OpenClaw.

Current model configuration:

- provider: Ollama;
- model: qwen3.8:27b;
- context: 32768.

CNX counters:

- Tickets: 46;
- max event id: 1101;
- direct model-call rows: 34;
- inference attempts: 32;
- assistant deliveries: 26.

Two non-terminal historical Tickets remain, both unrelated to the target channel:

- channel `1531199905673252946`, created 2026-09-03;
- channel `1366635842554036314`, created 2026-09-06.

Current runtime:

- Gateway health ok;
- event loop degraded=false;
- Discord ready/connected;
- activeRuns=0;
- target Discord session absent;
- free physical RAM about 21.4 GB.

## Classification

`RECOVERY_TRIGGERED_QWEN_MEMORY_PRESSURE_REPAIRED_GREEN`

## Next gate

Repeat the CNX-427 final genuine Discord acceptance from this fresh baseline.

Do not restart the Gateway between baseline capture and the single operator send.
