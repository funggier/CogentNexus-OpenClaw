# CNX-344 — OpenAI GPT-5.6 Luna Dashboard Ticket Routing Report

## Outcome

`BLOCKED — DURABLE_ADMISSION_UNOBSERVED_AFTER_SINGLE_UI_SEND`

This is not a self-acceptance. Execution stops for independent ChatGPT review. No retry, resend, recovery, fallback, manual dispatch, second session, or second semantic request was performed.

## Authority and execution boundary

- Task: `CNX-344`
- Remote execution branch: `agent/v0.9.6-openai-gpt56-luna-ticket-routing`
- Remote authority observed before execution: `95988dd1c942061fd567639d93b67e382ccfa9b2`
- Execution mode: `HUMAN_ASSISTED_ONE_BOUNDED_LIVE_REQUEST`
- Human setup was reported complete before preflight.
- Firefox window already open was reused; Hermes did not click `New session` and did not select a model.

## Observed facts

### Dashboard/session preflight

- Browser: Firefox (`firefox.exe`), PID `17040`, native window ID `3736650`.
- Dashboard URL observed:
  `http://127.0.0.1:18789/chat?session=agent%3Amain%3Adashboard%3A0874c9ea-7020-428f-ad66-cb5edbc18a53`
- Current Dashboard session:
  `agent:main:dashboard:0874c9ea-7020-428f-ad66-cb5edbc18a53`
- Durable `cnx_sessions` row:
  - `session_id=819c2940-1983-42b5-97c7-b94bae2ea7df`
  - `state=active`
  - `generation=0`
  - `created_at=2026-09-14T14:25:46.477Z`
- Prior CNX-343 session was different:
  `agent:main:dashboard:945504d3-42f1-497a-b635-9975561e4bd5`
  - `session_id=211d524d-63d7-49c5-8260-af4fc9a4132d`
  - `created_at=2026-09-14T08:29:00.259Z`
- Visible UI selector before the request showed `GPT-5.6 Luna · Medium`.
- The selector's visible label did not independently expose the provider string; internal configuration separately contained `openai/gpt-5.6-luna`.

### Read-only runtime/config evidence

- `/c/Users/CDQ-P/.openclaw/openclaw.json` contained `openai/gpt-5.6-luna` in the configured model allow-list.
- The CogentNexus plugin configuration contained `ticketFirst=true`, `preInferenceAdmission=true`, `enforcedMode=true`, and `providerMode=passthrough`.
- No configuration, provider, controller, timeout, database, production code, or test mutation was made.

### Durable baseline immediately before the request

Read-only SQLite database:
`C:/Users/CDQ-P/.openclaw/workspace/.cogentnexus-openclaw/runtime/cogentnexus-openclaw.sqlite3`

Observed at `2026-09-14T14:30:55Z`:

| Table | Count |
|---|---:|
| `tickets` | 23 |
| `ticket_events` | 864 |
| `cnx_inference_attempt` | 3 |
| `cnx_assistant_delivery` | 14 |
| `ticket_outbox` | 0 |
| `cnx_direct_model_call` | 20 |

### Single UI request

The exact semantic request was typed once into the already-open Firefox Dashboard composer for session `0874...`:

`CNX-344-OPENAI-TICKET-ROUTING: Reply exactly with DONE.`

A single Enter/send activation was issued. No further input was issued after that activation.

## Durable read-back after the single send

After a 60-second read-only observation window:

- Query for a Ticket owned by session `agent:main:dashboard:0874c9ea-7020-428f-ad66-cb5edbc18a53` with the CNX-344 prompt returned no row.
- Query for any Ticket with prompt prefix `CNX-344-` returned `0` rows.
- Total durable counts remained observable as `tickets=23`, `ticket_events=864`, `cnx_inference_attempt=3`, `cnx_assistant_delivery=14`, `ticket_outbox=0`, and `cnx_direct_model_call=20`.
- The newest Ticket remained the prior CNX-343 Ticket, not a CNX-344 Ticket.
- No Ticket ID, Run ID, Call ID, inference-attempt ID, Result, or Delivery ID exists for CNX-344 in the observed database.

## Required lifecycle correlation

| Lifecycle stage | CNX-344 evidence |
|---|---|
| Dashboard session | Observed: `agent:main:dashboard:0874c9ea-7020-428f-ad66-cb5edbc18a53` |
| Ticket/admission | **Not observed** |
| Run | Not available because no Ticket was observed |
| OpenAI call | Not observed |
| Inference attempt | Not observed |
| Result | Not observed |
| Delivery | Not observed |
| Final Ticket status | Not applicable; no CNX-344 Ticket row |
| Outbox | Global count observed as `0`; no CNX-344 outbox row |
| Duplicate-owner check | No CNX-344 owner/call rows to compare; no duplicate CNX-344 durable effect observed |

## Deductions and limitations

1. The fresh-session identity is durable and distinct from CNX-343.
2. The Dashboard visibly displayed `GPT-5.6 Luna · Medium`; the UI label alone does not prove the provider string.
3. Runtime configuration allowed `openai/gpt-5.6-luna` and enabled Ticket-first admission, but configuration is not proof that this request entered the Ticket path.
4. Because no corresponding durable Ticket appeared after the one UI send, the requested end-to-end lifecycle cannot be correlated or accepted.
5. This evidence does **not** establish `FAIL — OPENAI_REQUEST_BYPASSED_TICKET_LIFECYCLE`; no OpenAI provider call or result was observed either. The correct classification is a post-send durable-admission observation blocker.
6. The request must not be sent again. The missing Ticket may indicate UI send/transport/admission uncertainty, but this report does not speculate beyond the observed boundary.

## Protected-state and hard-fence accounting

- Human New Session action: one, performed by the operator.
- Human model selection: one, performed by the operator.
- Hermes New Session clicks: zero.
- Hermes model-selection actions: zero.
- Semantic request activations: one.
- Second session: none.
- Second request/retry/resend/recovery/fallback/manual dispatch: none.
- Provider/model/config/timeout/controller/database mutation: none.
- Install/reinstall/rebuild/restart: none.
- Production code/test changes: none.
- Force-push/history rewrite: none.

## Stop condition

Stop here for independent ChatGPT review. CNX-344 is not self-accepted.
