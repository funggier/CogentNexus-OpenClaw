# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_FINAL_AUTHENTICATED_FRESH_SESSION_SEMANTIC_ACCEPTANCE`
Current authorization: `ONE_FRESH_DASHBOARD_SESSION_ONE_SEMANTIC_MESSAGE_AUTHORIZED`
Task ID: `CNX-20260827-092`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260827-092-final-fresh-session-semantic-acceptance.md`](tasks/CNX-20260827-092-final-fresh-session-semantic-acceptance.md)

## Task 091 acceptance

Task 091 reported:

`PASS_DASHBOARD_OWNER_SURFACE_READY_NO_SECRET_DISCLOSURE`

Report HEAD:

`7390ae46dd61686e8d704f93043ead7fe7b9ca1e`

Independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_DASHBOARD_OWNER_SURFACE_READY_NO_SECRET_DISCLOSURE`

Review path:

[`reviews/CNX-20260827-091-prove-dashboard-owner-surface-without-secret-disclosure.md`](reviews/CNX-20260827-091-prove-dashboard-owner-surface-without-secret-disclosure.md)

Publication fence is accepted: execution `4f707b14...` -> report `7390ae46...` is exactly one report-only commit.

## Accepted authenticated owner surface

Task 091 proved the real localhost Control UI/WebChat surface for exact installed OpenClaw `2026.7.1-2`:

- client `openclaw-control-ui`;
- mode `webchat`;
- role `operator`;
- effective scopes include `operator.admin` and `operator.read`;
- authenticated Gateway WebSocket connection proven by successful read-only `sessions.list` RPC;
- existing paired Firefox profile reused;
- no new pairing request;
- shared token/password value read/copied/entered/logged/persisted/reported: zero.

Accepted readiness token:

`DASHBOARD_OWNER_SURFACE_READY`

Installed UI behavior also proves a new Dashboard/WebChat session is materialized by the first non-command message:

`DASHBOARD_OWNER_SURFACE_READY_FIRST_SEND_CREATES_SESSION`

This is a readiness contract only. Final acceptance must prove fresh-session behavior live end-to-end.

## Accepted live state carried forward

From Task 090/091:

- exact installed accepted source `d6daf8f93fcd5578f267b2017c6cc82e5de20095`;
- controller MANAGED;
- startup enabled;
- Supervisor Ready;
- AGENTS managed block present;
- one canonical loaded/enabled source-exact CogentNexus plugin `0.9.3`;
- ownership/runtime/launcher/Supervisor accepted;
- Gateway healthy;
- Ollama accepted four-model inventory preserved;
- SQLite integrity `ok`;
- Tickets/outbox zero at accepted pre-semantic baseline;
- `NO_FLASH_MULTI_TICK_PROVEN` remains accepted;
- no semantic/provider activity occurred in Task 091.

Do not reinstall/reset/manually repair this state.

## Task 092 final authorization

Task 092 may send **exactly one semantic message** through the authenticated Firefox Dashboard/WebChat owner surface.

It must first use the real Control UI **New Session / New Chat** action and prove a clean fresh staged state before any nonce is generated or sent.

If the New Session action shows or logs an unknown/stale/missing parent, silently falls back to an old session, or cannot enter a clean fresh state, stop before semantic send.

Only after fresh-session entry passes:

1. generate a new execution-time nonce;
2. send exactly one first non-command message: `ตอบกลับข้อความนี้เพียงว่า <NEW_NONCE>`;
3. prove a genuinely new session ID/key materializes;
4. prove it is distinct from existing Main/history and Task-076 session;
5. prove the fresh transcript inherited no prior semantic history;
6. prove exactly one Ticket is accepted and exactly one routed event occurs before correlated Ollama inference begins;
7. prove correlated `ollama/qwen3.5:9b` inference from that one message only;
8. prove exactly one visible nonce response;
9. prove durable lifecycle reaches `response_ready -> delivery_confirmed -> completed` bound to exact owner/session/run;
10. reject visible-response-only success if the Ticket remains accepted/routed/response_ready;
11. prove no duplicate route/provider/resume/outbox effect;
12. after completion invoke New Session once more without sending and prove another clean staged fresh state with no stale-parent error and no additional Ticket/provider activity.

## Absolute one-message fence

Semantic sends in Task 092: exactly `1` maximum.

No resend/retry after timeout/failure. No second message for validation.

Forbidden:

- `openclaw agent`;
- CLI owner-looking session keys;
- `chat.inject`;
- `sessions_send`;
- channel send;
- direct Ollama probe;
- synthetic Ticket mutation;
- provider/model/timeout change;
- install/install-over/uninstall/reset/cleanup;
- manual CNX/plugin/controller/startup/Supervisor/AGENTS/ownership/runtime/config/SQLite repair;
- reboot/merge/tag/release.

Task-076 nonce `CNXSEM-20260826T212900Z-7F3A` and session `f829224b-064f-4bb4-a845-2955be2a2c7f` remain permanently retired.

## Success token

Only:

`PASS_FINAL_FRESH_SESSION_SEMANTIC_TICKET_OLLAMA_DELIVERY_ACCEPTED`

followed by independent review `ACCEPT` completes CogentNexus-OpenClaw v0.9.3 final semantic acceptance.
