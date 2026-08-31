# CNX-20260826-076 — Final Semantic Ticket → Ollama → Delivery Acceptance

Result: `BLOCKED_SEMANTIC_ENTRY_PATH`

## Execution identity

- Coordination branch: `agent/v0.9.3-recovery-reality-tests`
- Execution starting HEAD: `d9ac3ed08562cebcd2af69f19d110bf89cd41ab9`
- Accepted live source / parity reference: `79b51ed06363f6e8862c491ee0a313ddb412c806`
- Evidence directory: `C:\Users\CDQ-P\AppData\Local\Temp\cnx076-preflight-20260826T142341Z`
- Execution date: 2026-08-26 ICT

## Authorization and fence

`ACTIVE.md` and `STATUS.md` were fetched from the exact coordination branch and both reported `READY_FOR_HERMES`, execution mode `LIVE_BOUNDED_REAL_USER_MESSAGE_TICKET_OLLAMA_DELIVERY_ACCEPTANCE`, and authorization `FINAL...ZED` for CNX-20260826-076.

No install, install-over, uninstall, reset, cleanup, reboot, provider/model/config change, manual SQLite mutation, merge, tag, release, or duplicate semantic send was performed. The only product mutation attempted was the one authorized real OpenClaw agent message described below; all resulting state was observed read-only.

## Phase A — read-only preflight

The preflight passed materially against the Task-075 accepted state:

- `cnxclaw status`: mode `managed`; desired Gateway/provider `running`; selected provider `ollama`; generation `12`.
- Gateway: Scheduled Task registered/running, port `18789`, connectivity probe `ok`.
- Provider: Ollama reachable/healthy/ready at `http://127.0.0.1:11434`; configured model `qwen3.5:9b`; four-model inventory observed (`qwen3.5:9b`, `muse-glimmer:30b`, `qwen3.6:27b`, `qwen3.8:27b`).
- `cnxclaw check system`: `SYSTEM READINESS: READY`; Ticket DB integrity `ok`; Supervisor healthy; no pending terminal deliveries; no maintenance marker; no provider recovery incident.
- OpenClaw reported one active default session: `agent:main:main`, session id `f829224b-064f-4bb4-a845-2955be2a2c7f`.
- Plugin configuration was read-only inspected and showed `ticketFirst=true`, `preInferenceAdmission=true`, `enforcedMode=true`, `autoResume=true`, and `autoWorkflowCompletion=true`.
- Ownership verification passed with the installed v0.9.3 CogentNexus-owned runtime and plugin paths (`a04-ownership.txt`).
- The authoritative Ticket DB was resolved from the live runtime status, not guessed: `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\runtime\cogentnexus-openclaw.sqlite3`.

### BEFORE durable cursors

The read-only BEFORE snapshot (`a01-db-before.txt`) recorded:

- `tickets`: count `0`, maximum `created_at`: `NULL`;
- `ticket_events`: count `0`, maximum `event_id`: `NULL`;
- `ticket_outbox`: count `0`, maximum `outbox_id`: `NULL`;
- `cnx_direct_model_call`, `cnx_assistant_delivery`, and `cnx_direct_recovery`: empty;
- `cnx_sessions`: one active session row for `agent:main:main`, generation `0`.

There was no pre-existing unfinished Ticket for the selected session, so attribution was unambiguous before the send.

## Phase B/C — supported surface and exactly one message

Selected supported surface:

`openclaw.cmd agent --session-key agent:main:main --message-file ... --json --timeout 300`

This is the installed OpenClaw Gateway-backed agent/session CLI surface, targeting the real active owner session key. It was used once, with no direct TicketStore/SQLite call, no ticket CLI shortcut, no direct Ollama invocation, no internal hook/test harness, and no fabricated hook event.

Exact prompt text:

`ตอบกลับข้อความนี้เพียงว่า CNXSEM-20260826T212900Z-7F3A`

- Nonce: `CNXSEM-20260826T212900Z-7F3A`
- Prompt SHA-256 (UTF-8): `80ed32838099f31d3098237e596c002f7fbd5fdc56cd1ac8930d52ad03c9682e`
- Owner session key: `agent:main:main`
- OpenClaw run ID: `97b7e136-3258-415b-a595-02792d393ff9`
- Session id: `f829224b-064f-4bb4-a845-2955be2a2c7f`
- Prompt was prepared at approximately `2026-08-26T14:26:16Z`; OpenClaw logged run startup at `2026-08-26T14:26:32.939Z`.

The command was not resent after becoming slow. Its returned JSON was:

- `status`: `timeout`
- `summary`: `aborted`
- `stopReason`: `rpc`
- `timeoutPhase`: `provider`
- `providerStarted`: `true`
- `durationMs`: `245699`
- returned surface text: `LLM request timed out.` plus the OpenClaw model-idle-timeout explanation.

No user-visible response containing the nonce was received or delivered.

## Phase D/G — durable semantic result

The read-only AFTER snapshot (`c01-db-after.txt`) showed no durable semantic admission:

- `tickets`: count `0`;
- `ticket_events`: count `0`;
- `ticket_outbox`: count `0`;
- `cnx_direct_model_call`: empty;
- `cnx_assistant_delivery`: empty;
- `cnx_direct_recovery`: empty;
- `cnx_sessions`: still only the existing `agent:main:main` active row.

Therefore there is no `CNXT-` Ticket, no `accepted` event, no `routed` direct event, no response-ready transition, no delivery-confirmed transition, no completed event, and no duplicate Ticket/delivery side effect to account for. Ticket-first ordering and terminal delivery cannot be proven because the selected supported surface did not create a Ticket before entering the provider attempt.

The correlated OpenClaw log evidence (`c02-log-correlated.txt`) ties run `97b7e136-3258-415b-a595-02792d393ff9` to provider `ollama`, model `qwen3.5:9b`, and repeated `llm-idle-timeout` events, ending in `embedded_run_failover_decision` with `decision=surface_error`, `timedOut=true`, and `providerRuntimeFailureKind=timeout`. This proves a provider-stage timeout for the OpenClaw run, but it does not prove a CogentNexus Ticket-first semantic path; the empty authoritative Ticket tables are the decisive entry-path blocker.

The result is therefore `BLOCKED_SEMANTIC_ENTRY_PATH`, not a PASS and not an Ollama-success claim. The run was not repeated, and no manual state change was used to mask the failure.

## Phase H — post-semantic health

Post-run read-only checks remained healthy:

- `cnxclaw check system`: `SYSTEM READINESS: READY`;
- controller remained `managed`;
- Gateway remained reachable/Ready;
- provider remained Ollama with default model `ollama/qwen3.5:9b`;
- Ollama remained healthy with the same four-model inventory;
- Supervisor remained healthy and owned-runtime bound;
- Ticket DB integrity remained `ok`;
- `cnxclaw check delivery`: no pending terminal deliveries;
- no recovery/outbox residue was attributable to this run.

## Publication fence

This is a report-only publication. The report is the only intended repository change. No product/runtime source, configuration, database, or live installation state was edited.
