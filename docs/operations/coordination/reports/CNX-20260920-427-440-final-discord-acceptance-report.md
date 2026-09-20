# CNX-20260920 — CNX-427 / CNX-440 Final Discord Acceptance Report

Status: `COMPLETE`

Final classifications:

`CNX427_EXTERNAL_INGRESS_TICKET_FIRST_DURABLE_DISCORD_GREEN`

`OPENCLAW95_DISCORD_DURABLE_MARKER_SETTLEMENT_GREEN`

Related completed repair:

`INSTALLER_SUPERVISOR_HANDOFF_QUIESCENCE_GREEN`

## Environment

- branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- OpenClaw: `2026.9.5`
- CNX controller: active / managed generation `111`
- provider/model: `ollama/qwen3.8:27b`
- context: `24576`
- Ollama `num_ctx=24576`
- `OLLAMA_CONTEXT_LENGTH=24576`
- `OLLAMA_KEEP_ALIVE=2h`

## Clean pre-send baseline

Target Discord channel:

`1391855033993138217`

Before the operator message:

- Tickets: `47`
- max Ticket event ID: `1109`
- direct model calls: `35`
- inference attempts: `33`
- assistant deliveries: `26`
- target non-terminal Tickets: `0`
- target active OpenClaw session nodes: `0`
- target open session windows: `0`
- target pending inputs: `0`
- target active recovery: `0`

Gateway was healthy, event-loop degradation was false, Discord was ready/connected with activeRuns=0, and the CNX supervisor was Enabled/Ready with Last Result 0.

## Operator turn

Exactly one human-originated Discord message was sent:

`@Ce CNX427_FINAL_ACCEPTANCE_20260920_A1 Reply exactly: CNX427_FINAL_OK_20260920_A1`

Discord inbound message ID:

`1551126842604257321`

## Authoritative lineage

- physical OpenClaw session:
  `06e736f1-01e5-45b7-8c0b-bbaa9ed6f700`
- authoritative run:
  `e683efcf-b00e-4ee9-bb11-cac0da94a840`
- CNX Ticket:
  `CNXT-d6ed7093-5440-435d-91f7-77caaac7ffb3`
- inference attempt:
  `cnx-attempt-8004886f-cf61-468d-8dd3-e7649a374398`
- durable delivery:
  `27`
- owner generation:
  `7`

## Ticket-first ordering

Event order:

1. Ticket accepted:
   `2026-09-20T07:04:19.655Z`
2. Ticket routed:
   `2026-09-20T07:04:19.659Z`
3. direct model call started:
   `2026-09-20T07:04:19.714Z`
4. inference attempt started:
   `2026-09-20T07:04:19.726Z`

Ticket persistence preceded model-call authority by about 59 ms.

Cardinality from baseline:

- Tickets `47 -> 48`: +1
- direct model calls `35 -> 36`: +1
- inference attempts `33 -> 34`: +1
- assistant deliveries `26 -> 27`: +1

There was exactly one new target Ticket and exactly one Ticket for the authoritative run.

No direct-recovery row exists for the accepted Ticket.

## Model completion

The single local model call completed successfully:

- provider: `ollama`
- model: `qwen3.8:27b`
- model call outcome: `completed`
- inference outcome: `completed`
- duration: `1,111,674 ms`
- input tokens: `12,105`
- output tokens: `19`
- compaction count: `0`
- trajectory finalStatus: `success`
- timedOut: `false`

Expected assistant text:

`CNX427_FINAL_OK_20260920_A1`

OpenClaw trajectory recorded that exact assistant text.

## Durable Discord settlement

Terminal ordering:

1. model call ended:
   `2026-09-20T07:22:51.387Z`
2. inference attempt ended:
   `2026-09-20T07:22:51.396Z`
3. response ready:
   `2026-09-20T07:22:51.460Z`
4. durable delivery row 27 created:
   `2026-09-20T07:22:51.578Z`
5. delivery confirmed:
   `2026-09-20T07:22:52.433Z`
6. Ticket completed:
   `2026-09-20T07:22:52.433Z`

Delivery row 27:

- status: `delivered`
- delivery_state: `confirmed`
- surface: `discord`
- run_id:
  `e683efcf-b00e-4ee9-bb11-cac0da94a840`
- inference_attempt_id:
  `cnx-attempt-8004886f-cf61-468d-8dd3-e7649a374398`
- owner_generation: `7`
- evidence_type:
  `discord-message-receipt-marker`
- payload SHA-256:
  `70d369c5e50d594ff1a733e172099207aafee022d7240ec24f38c3bf87a0e320`
- idempotency key:
  `cnx-discord:CNXT-d6ed7093-5440-435d-91f7-77caaac7ffb3:g7:cnx-attempt-8004886f-cf61-468d-8dd3-e7649a374398`

Per-Ticket event counts:

- accepted: 1
- routed: 1
- direct_model_call_started: 1
- inference_attempt_started: 1
- direct_model_call_ended: 1
- inference_attempt_ended: 1
- response_ready: 1
- delivery_confirmed: 1
- completed: 1

There was no duplicate Ticket, duplicate model call, duplicate inference attempt, recovery inference, or stale-generation settlement.

## Visible Discord proof

The operator supplied Discord screenshots after completion.

They visually confirm one assistant response in the target channel with the exact text:

`CNX427_FINAL_OK_20260920_A1`

No duplicate visible assistant response was shown.

## Post-run runtime

After terminal settlement:

- Gateway health: ok
- event loop degraded: false
- Discord lifecycle: ready
- Discord running/connected: true
- Discord busy: false
- Discord activeRuns: 0
- supervisor: Enabled / Ready
- supervisor LastTaskResult: 0

The qwen model remains resident because keep-alive is intentionally `2h`.

Current 24K policy remains unchanged by operator decision.

Observed memory pressure during this run:

- llama-server private memory reached about `21.4 GB`
- free physical RAM was observed as low as about `1.3 GB`

Therefore 24K remains the current default. A larger context should be reconsidered only if real workloads demonstrate that 24K is insufficient.

## Result

PASS.

CNX-427 external Discord ingress, Ticket-first authority, single-run semantics, local qwen execution, durable Discord marker settlement, terminal Ticket completion, and exactly-one visible delivery are live-qualified end to end on OpenClaw 2026.9.5.
