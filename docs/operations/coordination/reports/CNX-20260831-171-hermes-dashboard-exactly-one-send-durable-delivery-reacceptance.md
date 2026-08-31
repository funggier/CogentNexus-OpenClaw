# CNX-20260831-171 — Hermes Dashboard Exactly-One-Send Durable Delivery Reacceptance

- **Disposition:** `PASS`
- **Executor:** Hermes/Codex
- **Authority:** GitHub branch `agent/v0.9.3-full-stabilization`
- **Observed:** 2026-08-31 ICT
- **Evidence root:** `C:\Users\CDQ-P\AppData\Local\Temp\cnx171-evidence-20260831T020231Z`

## Authority and starting state

Fresh GitHub readback identified `CNX-20260831-171` as the active task. The accepted installed checkpoint was preserved:

- Product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`
- Installed candidate fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- Package SHA-256: `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`
- Pinned OpenClaw: `2026.7.1-2`
- Active mode: `WINDOWS_DASHBOARD_EXACTLY_ONE_SEND_DURABLE_DELIVERY_REACCEPTANCE_HERMES`
- Executor authorization: exactly one Dashboard semantic Send, read-only observation, and Task-171 report publication.

## Preflight

Read-only preflight completed before the semantic action. The managed controller, Gateway, provider, recovery fence, delivery fence, installed provenance, and SQLite store were healthy. Baseline database counts were:

- `tickets=3`
- `ticket_events=21`
- `cnx_assistant_delivery=0`
- `cnx_direct_model_call=3`
- `cnx_direct_recovery=0`
- `ticket_outbox=0`
- SQLite `integrity_check=ok`

The existing Firefox Dashboard was used without creating a replacement session. Exact session key:

`agent:main:dashboard:13b27c98-c09c-431e-928f-446175ed1937`

The composer was empty and focused before input. The unique nonce was absent from the pre-send durable search.

## Exactly-one semantic action

Frozen prompt:

`CNX-171 acceptance T171-20260831T020446Z-3142A528. Reply with exactly: CNX-171-ACK-T171-20260831T020446Z-3142A528`

Expected response:

`CNX-171-ACK-T171-20260831T020446Z-3142A528`

The prompt was typed once and one Send click was issued at the Dashboard Send control. No Enter key, second click, alternate semantic surface, `chat.inject`, manual inference, recovery invocation, or retry was used. The UI screenshot immediately after the click still displayed the composer text; this was treated as an unverified render state, not as permission to retry. Native persistence was used as authority.

## Native transcript and model proof

Native transcript readback established:

- Session file: `7d2ca55f-ecda-4e24-b924-5f61e75a13b3.jsonl`
- Native user message ID: `750be5ac`
- Native assistant message ID: `e682c442`
- Run ID: `8b69bede-030f-4c20-8bb8-0aa99e12422c`
- Trajectory: `prompt.submitted` → `model.completed` → `session.ended`
- Session ended with `status=success`, `aborted=false`, `timedOut=false`
- Provider/model: `ollama` / `qwen3.5:9b`
- Exactly one new native user message and one assistant response for the nonce
- Assistant response began with the exact expected response; the only appended content was the native delivery marker
- Exactly one direct model call: `...:model:1`, outcome `completed`, duration `21957ms`

## Durable delivery and Ticket settlement

The new Ticket and delivery row were read back from SQLite:

- Ticket: `CNXT-b5bf2532-d35d-47db-8951-fcf9f4729abf`
- Ticket status: `completed`
- Ticket run ID: `8b69bede-030f-4c20-8bb8-0aa99e12422c`
- `response_ready_at`: `2026-08-31T02:14:45.052Z`
- `delivery_confirmed_at`: `2026-08-31T02:14:45.082Z`
- `delivery_last_error`: `null`
- Delivery rows for this action: exactly `1`
- Delivery ID: `1`
- Delivery status: `delivered`
- Delivery text: exact expected response
- Delivery identity: `cnxclaw-direct-result:CNXT-b5bf2532-d35d-47db-8951-fcf9f4729abf:g0`
- Delivery target bound to the same Ticket and run ID
- `attempt_count=0`, `claim_token=null`, `claim_expires_at=null`

Final event order for the Ticket was:

1. `accepted`
2. `routed` (`workflowEligible=false`)
3. `direct_model_call_started`
4. `direct_model_call_ended` (`outcome=completed`)
5. `response_ready` (`durableDelivery=true`)
6. `direct_response_durable`
7. `delivery_confirmed` (`source=native-dashboard-marker`)
8. `completed` (`deliveryConfirmed=true`, `durablePayload=true`)

Post-action database counts were:

- `tickets=4` (+1)
- `ticket_events=29` (+8)
- `cnx_assistant_delivery=1` (+1)
- `cnx_direct_model_call=4` (+1)
- `cnx_direct_recovery=0` (+0)
- `ticket_outbox=0`
- SQLite `integrity_check=ok`

The native session search found the nonce only in the corresponding transcript and trajectory files. No duplicate nonce, duplicate delivery, second model call, recovery reinjection, or conflicting outbox row was found.

## Post-health and provenance

Read-only postflight checks returned `READY`:

- Controller: `managed`, generation `36`
- Gateway: healthy, reachable, loopback `127.0.0.1:18789`
- Ollama: reachable/healthy/ready; selected model `qwen3.5:9b`
- Recovery fence: no maintenance marker; no active provider recovery incident
- Delivery fence: no pending terminal deliveries
- Startup adapter: `Ready`, enabled, `LastTaskResult=0`
- OpenClaw: remains `2026.7.1-2`
- Installed plugin remains loaded/enabled at version `0.9.3`
- Installed fingerprint remains the accepted Task-170 fingerprint

No installer, lifecycle, dependency, OpenClaw, release, merge, force-push, product-source, database, transcript, or durable-state mutation was performed by this task.

## Anomalies and handling

- The first postflight wrapper used an unset PowerShell evidence variable and failed to tee output. It changed no product or runtime state. The same probes were rerun with explicit absolute paths and returned `exitCode=0`.
- The immediate UI capture did not clear the composer after the Send click. Because the hard fence prohibits retry, no retry was attempted. Native transcript, trajectory, Ticket, model-call, delivery, and settlement records independently proved successful completion.

## Evidence index

- `b01-send-ledger.json` — frozen nonce, exact prompt, session, expected response, prompt hash, and send budget
- `c01-post-send-nonce-search.json` — post-send nonce correlation
- `c02-post-db.json` — post-send counts and integrity
- `c03-check-delivery.txt` — read-only delivery readiness
- `c04-check-recovery.txt` — read-only recovery readiness
- `c05-status.txt` — managed host/provider/ticket status
- `c06-gateway.txt` — Gateway readback
- `c07-active-remote.md` — fresh GitHub ACTIVE.md
- `c08-status-remote.md` — fresh GitHub STATUS.md
- `c09-native-settlement.json` — native transcript-linked Ticket/event/delivery settlement
- `computer_use_62d4556da8b54a7daf82c6d7d8c67de3.png` — post-action Dashboard capture

## Publication and successor fence

This report is the only repository artifact authorized for publication by Task-171. After publication, execution stops for ChatGPT review. No successor action is authorized by this report.
