# CNX-20260920-440 — OpenClaw 9.5 Discord Durable Marker Deployment Checkpoint

Status: `COMPLETE`

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

## Final Discord acceptance — GREEN

The operator sent exactly one genuine Discord turn on channel `1391855033993138217`:

`@Ce CNX427_FINAL_ACCEPTANCE_20260920_A1 Reply exactly: CNX427_FINAL_OK_20260920_A1`

Observed lineage:

- physical OpenClaw session: `06e736f1-01e5-45b7-8c0b-bbaa9ed6f700`;
- authoritative run: `e683efcf-b00e-4ee9-bb11-cac0da94a840`;
- CNX Ticket: `CNXT-d6ed7093-5440-435d-91f7-77caaac7ffb3`;
- inference attempt: `cnx-attempt-8004886f-cf61-468d-8dd3-e7649a374398`;
- durable delivery: `27`;
- owner generation: `7`.

Ordering and cardinality from the clean pre-send baseline:

- Tickets: `47 -> 48` (+1);
- direct model calls: `35 -> 36` (+1);
- inference attempts: `33 -> 34` (+1);
- assistant deliveries: `26 -> 27` (+1);
- exactly one new target-channel Ticket;
- exactly one Ticket for the authoritative run;
- Ticket accepted at `2026-09-20T07:04:19.655Z`;
- model call started at `2026-09-20T07:04:19.714Z`;
- inference attempt started at `2026-09-20T07:04:19.726Z`;
- Ticket persistence therefore preceded model-call authority by about 59 ms;
- no direct-recovery row exists for the accepted Ticket;
- no duplicate Ticket, duplicate model call, duplicate inference attempt, or stale-generation settlement occurred.

Terminal delivery proof:

- model call ended `completed` at `2026-09-20T07:22:51.387Z`;
- inference attempt ended `completed` at `2026-09-20T07:22:51.396Z`;
- `response_ready` at `2026-09-20T07:22:51.460Z`;
- durable delivery row 27 was created at `2026-09-20T07:22:51.578Z`;
- durable idempotency key:
  `cnx-discord:CNXT-d6ed7093-5440-435d-91f7-77caaac7ffb3:g7:cnx-attempt-8004886f-cf61-468d-8dd3-e7649a374398`;
- delivery settled as `delivered / confirmed`;
- receipt evidence type:
  `discord-message-receipt-marker`;
- `delivery_confirmed` event count = `1`;
- `completed` event count = `1`;
- Ticket terminal status = `completed`;
- exact delivered text:
  `CNX427_FINAL_OK_20260920_A1`.

OpenClaw trajectory independently recorded:

- finalStatus = `success`;
- timedOut = `false`;
- provider/model = `ollama / qwen3.8:27b`;
- input tokens = `12105`;
- output tokens = `19`;
- compaction count = `0`;
- assistant text = `CNX427_FINAL_OK_20260920_A1`;
- target session status = `done`.

The operator supplied visual Discord screenshots confirming exactly one visible assistant response with the exact expected text.

Current local-model policy remains intentionally unchanged:

- primary model `ollama/qwen3.8:27b`;
- `contextWindow=24576`;
- `num_ctx=24576`;
- `OLLAMA_CONTEXT_LENGTH=24576`;
- `OLLAMA_KEEP_ALIVE=2h`.

The live acceptance used 24K context successfully. During execution llama-server private memory reached about 21.4 GB and free physical RAM was observed as low as about 1.3 GB, so 24K remains the operator-approved default unless future workload proves insufficient.

Final classifications:

`CNX427_EXTERNAL_INGRESS_TICKET_FIRST_DURABLE_DISCORD_GREEN`

`OPENCLAW95_DISCORD_DURABLE_MARKER_SETTLEMENT_GREEN`
