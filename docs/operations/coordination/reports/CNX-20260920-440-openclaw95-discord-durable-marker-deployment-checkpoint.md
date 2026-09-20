# CNX-20260920-440 — OpenClaw 9.5 Discord Durable Marker Deployment Checkpoint

Status: `DEPLOYED_AWAITING_LIVE_DISCORD_REQUALIFICATION`

Source classification:

`OPENCLAW95_DISCORD_DURABLE_MARKER_SETTLEMENT_SOURCE_GREEN`

## Candidate and deployment

- CNX-440 implementation commit: `a4f27ad097e721edfe566a7495864b7e15ae88e8`
- deployment candidate HEAD including CNX-441 repair:
  `5263b6aed9acf77a4db39be47c4d96fecfe8a431`
- local HEAD = remote HEAD
- supported install session: `proc-1789885920190-35`
- installer PID: `10220`
- installer exit: `0`
- live/candidate v095 adapter SHA-256:
  `7809B18C4BAE1209624D5E69112722EF9AD7F5E39A92A2815C6889DFF6C646A1`

## Runtime qualification

- CNX controller: active/managed generation `111`
- Gateway health: ok
- event loop: `degraded=false`
- Discord: ready/connected
- supervisor: Enabled/Ready, Last Result `0`
- Ollama resident models: none

qwen3.8 policy:

- primary model: `ollama/qwen3.8:27b`
- `contextWindow=24576`
- `params.num_ctx=24576`
- `OLLAMA_CONTEXT_LENGTH=24576`
- `OLLAMA_KEEP_ALIVE=2h`

## Fresh pre-acceptance baseline

Target Discord channel:

`1391855033993138217`

CNX DB:

- Tickets: `47`
- max Ticket event ID: `1109`
- direct model-call rows: `35`
- inference attempts: `33`
- assistant-delivery rows: `26`
- target non-terminal Tickets: `0`
- target prior CNX session: `deleted`, generation `7`

Two unrelated historical Tickets remain `accepted` on channels `1531199905673252946` and `1366635842554036314`. Their redelivery recovery rows are pending with `active_run_id=null`; neither belongs to the target channel.

## Remaining live gate

Exactly one human-originated Discord message is required. After the operator confirms it was sent, verify:

- one new physical target session;
- one authoritative run;
- one Ticket, persisted before model-call authority;
- one direct model call;
- one inference attempt;
- one durable `cnx_assistant_delivery` row staged before transport;
- the unique CNX marker is present in native outbound content;
- runId-less `message_sent` settles only by exact marker + session + generation ownership;
- delivery becomes confirmed;
- Ticket becomes completed;
- exactly one delivery-confirmed event;
- exactly one completed event;
- no duplicate Ticket;
- no recovery inference;
- no stale-generation settlement;
- exactly one visible Discord response.

Final live classification is intentionally not assigned yet.
