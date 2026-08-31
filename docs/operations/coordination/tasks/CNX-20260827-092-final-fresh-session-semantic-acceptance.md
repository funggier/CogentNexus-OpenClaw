# CNX-20260827-092 — Final Fresh-Session Semantic Acceptance

Status: `READY_FOR_HERMES`

Execution mode: `LIVE_FINAL_AUTHENTICATED_FRESH_SESSION_SEMANTIC_ACCEPTANCE`

Current authorization: `ONE_FRESH_DASHBOARD_SESSION_ONE_SEMANTIC_MESSAGE_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Perform exactly one final authenticated Dashboard/WebChat owner semantic turn through a **fresh Control UI session**, proving that fresh-session creation works without stale/unknown-parent regressions and that the full CogentNexus semantic contract converges end-to-end:

`fresh authenticated owner session -> durable Ticket accepted/routed before provider inference -> correlated Ollama inference -> response_ready -> exact owner/run delivery_confirmed -> completed -> exactly one visible nonce response`

Then invoke New Session once more without sending content and prove the UI can return to another fresh staged session state without stale-parent failure or extra Ticket/provider activity.

This is the final semantic acceptance gate for CogentNexus-OpenClaw v0.9.3.

## Accepted predecessor state

Task 090 accepted live state:

- exact installed accepted source `d6daf8f93fcd5578f267b2017c6cc82e5de20095`;
- controller MANAGED;
- startup enabled;
- Supervisor Ready;
- AGENTS managed block present;
- one canonical loaded/enabled source-exact CogentNexus plugin `0.9.3`;
- ownership/runtime/launcher/Supervisor bindings accepted;
- Gateway healthy on loopback;
- Ollama accepted four-model inventory preserved;
- SQLite integrity `ok`;
- Tickets/outbox zero at accepted baseline;
- `NO_FLASH_MULTI_TICK_PROVEN` from five natural PT1M observations.

Task 091 independently accepted:

`ACCEPT_DASHBOARD_OWNER_SURFACE_READY_NO_SECRET_DISCLOSURE`

Accepted owner surface:

- actual localhost `openclaw-control-ui`;
- mode `webchat`;
- role `operator`;
- effective scope includes `operator.admin` and `operator.read`;
- authenticated Gateway connection proven by read-only RPC;
- existing paired Firefox profile reusable without shared-secret disclosure;
- exact installed OpenClaw `2026.7.1-2` creates a fresh Dashboard session on the first non-command message.

Review path:

`docs/operations/coordination/reviews/CNX-20260827-091-prove-dashboard-owner-surface-without-secret-disclosure.md`

## Fresh-session acceptance rationale

The final test must not reuse an existing semantic session merely because the owner surface is authenticated.

The operator explicitly requires fresh-session behavior to be tested because prior new-session testing exposed edge cases around parent/session identity and post-response lifecycle convergence.

Therefore Task 092 treats these as independent mandatory invariants:

- New Session can enter a clean staged state before first send;
- first send materializes a genuinely new session identity;
- the new session does not inherit old semantic history;
- no stale/unknown-parent Gateway error occurs;
- a visible reply is insufficient unless the Ticket reaches `completed`;
- after completion New Session can be entered again without another send or durable/provider side effect.

---

# Absolute one-message fence

Exactly **one semantic/user message** may be sent in Task 092.

The message must be sent only through the authenticated Dashboard/WebChat Control UI surface accepted by Task 091.

Forbidden alternatives:

- `openclaw agent`;
- CLI `--session-key agent:main:main`;
- `chat.inject`;
- `sessions_send`;
- channel send;
- synthetic Ticket creation;
- direct Ollama/provider probe;
- second semantic message;
- resend/retry after timeout/failure;
- reuse of Task-076 nonce `CNXSEM-20260826T212900Z-7F3A`;
- reuse of Task-076 session `f829224b-064f-4bb4-a845-2955be2a2c7f`.

If the one semantic turn fails or times out, capture evidence and stop. Do not resend.

## Product mutation fence

Do NOT:

- install/install-over/uninstall/reset/cleanup;
- mutate plugin generations;
- edit controller/startup/Supervisor/AGENTS/ownership/runtime/config;
- edit SQLite/Ticket/session transcript state manually;
- change provider/model/timeouts;
- direct-call Ollama;
- restart/reboot merely to obtain a passing result;
- merge/tag/release.

Normal runtime effects of the one authorized Dashboard semantic turn are allowed.

The authenticated browser may invoke the supported New Session/New Chat UI action before the message and once again after completion. Those New Session actions must not themselves submit semantic content.

---

# Phase A — execution and live re-proof

Before touching the Dashboard New Session control:

1. record current coordination execution HEAD;
2. prove Task-091 report + ACCEPT review are ancestors;
3. verify installed OpenClaw remains `2026.7.1-2 (0790d9f)`;
4. verify controller remains MANAGED;
5. verify one canonical loaded source-exact plugin;
6. verify Gateway healthy;
7. verify Supervisor healthy with recent natural successful tick;
8. verify SQLite integrity `ok`;
9. capture exact pre-test counts for `tickets`, `ticket_events`, `ticket_outbox`, direct-delivery/workflow state tables used by the product;
10. capture authenticated Control UI device identity/role/scopes without secret values;
11. capture `sessions.list` before New Session, including the current Main/existing session identities needed to prove freshness later;
12. verify no semantic/provider run is active.

If MANAGED/runtime/owner-surface state drifted, stop before sending with:

`BLOCKED_FINAL_LIVE_STATE_DRIFT`

No repair is authorized in Task 092.

---

# Phase B — pre-send fresh-session entry

Use the real authenticated Firefox Dashboard/WebChat Control UI accepted by Task 091.

Invoke the supported **New Session / New Chat** UI action exactly once before the semantic message.

Because exact installed OpenClaw materializes a Dashboard session on first non-command send, the pre-send UI may represent a staged empty session rather than a persisted `sessions.list` row. That is acceptable only if all of the following are proven:

- the UI is no longer displaying/reusing the prior semantic transcript as the active target;
- no user/assistant semantic content exists in the staged view;
- no Ticket/outbox/provider count changes;
- no provider inference begins;
- Gateway logs contain no `unknown parent session`, stale parent, missing parent, invalid parent, session-resolution error or equivalent New Session failure;
- no fallback silently targets the previous Main/history session;
- authenticated owner/admin scope remains intact.

If New Session cannot enter this clean staged state, stop **before generating/sending the nonce**.

Required blocker tokens include:

- `BLOCKED_FRESH_SESSION_ENTRY`
- `BLOCKED_UNKNOWN_OR_STALE_PARENT_SESSION`
- `BLOCKED_FRESH_SESSION_FALLBACK_TO_EXISTING_SESSION`

No semantic allowance is consumed if Phase B stops before send.

---

# Phase C — generate one fresh nonce and send exactly one message

Only after Phase B passes, generate a new execution-time nonce.

Required form:

`CNXSEM2-<UTC compact timestamp>-<random uppercase/hex suffix>`

The nonce must:

- be new;
- not exist in prior session history/logs/Tickets;
- not reuse Task-076 nonce;
- be generated only immediately before the one authorized send.

Send exactly this minimal owner message through the staged fresh Dashboard/WebChat composer:

`ตอบกลับข้อความนี้เพียงว่า <NEW_NONCE>`

Semantic send count becomes exactly `1`.

After this point no second semantic message is authorized under any outcome.

Record the authenticated Control UI client/device identity, send timestamp, request/run identifiers exposed by supported evidence, and all correlation identifiers without recording any bearer secret.

---

# Phase D — prove a genuinely new session materialized

After first send, prove the fresh staged state materialized a new semantic session.

Required evidence:

1. a new session ID/key is visible in `sessions.list` or equivalent supported read-only state;
2. the new session identity did not exist in Phase-A snapshot;
3. it is not the prior Main/existing semantic session;
4. it is not Task-076 session `f829224b-064f-4bb4-a845-2955be2a2c7f`;
5. it is not generic CLI `agent:main:main` used as an ownership substitute;
6. the session is attributable to the authenticated Dashboard/WebChat client;
7. transcript/history for the new session contains no inherited prior user/assistant semantic messages;
8. the one authorized user prompt is the first semantic user message in that session.

If the first send reuses an old semantic session or inherits prior transcript state, final acceptance fails even if the model later replies correctly.

Blocker:

`BLOCKED_FRESH_SESSION_NOT_ISOLATED`

---

# Phase E — Ticket-before-provider ordering

Correlate the new session, one user message, run ID, Ticket ID and provider execution.

Durable database evidence is mandatory; logs alone are insufficient.

Require exactly one new Ticket attributable to the one message.

Required ordering:

1. authenticated fresh owner message enters normal `before_agent_run` path;
2. Ticket accepted durably;
3. exactly one `routed` event occurs for that Ticket;
4. accepted/routed evidence exists **before correlated Ollama inference begins**;
5. direct lane/provider continuation occurs only after durable admission/routing.

Capture exact timestamps/event IDs sufficient to establish ordering.

Prohibited success interpretation:

- provider inference with zero Ticket;
- Ticket created only after provider begins;
- more than one Ticket for the one message;
- more than one routed event;
- uncorrelated provider evidence.

Blocker tokens:

- `BLOCKED_TICKET_BEFORE_PROVIDER_ORDERING`
- `BLOCKED_DUPLICATE_TICKET_OR_ROUTE`

---

# Phase F — correlated Ollama inference

The one Dashboard semantic message may cause the normal configured provider inference.

Do not call Ollama separately.

Require provider correlation to the same fresh session/run/Ticket using available OpenClaw/provider trace/runtime evidence.

Expected selected provider/model remains:

`ollama/qwen3.5:9b`

If provider stage times out or fails, capture exact stage and durable Ticket state and stop without resend or config change.

A timeout does not authorize a second message.

Blocker:

`BLOCKED_CORRELATED_PROVIDER_INFERENCE`

---

# Phase G — visible response and full durable delivery convergence

The assistant-visible response must equal the new nonce exactly, allowing only surrounding whitespace normalization if the UI itself renders it.

Require one correlated direct lifecycle for the Ticket:

`accepted -> routed -> response_ready -> delivery_confirmed -> completed`

Exact conditions:

- exactly one `response_ready` for the semantic result;
- exactly one visible nonce response in the fresh Dashboard session;
- delivery settlement is bound to the exact owner/session/run;
- exactly one `delivery_confirmed`;
- Ticket terminal state `completed`;
- no Ticket remains stuck merely at `accepted`, `routed` or `response_ready` after the visible response;
- no workflow/durable promotion for this successful direct result;
- no generic `cogent-resume-*` duplicate recovery;
- no duplicate Ticket outbox delivery;
- no second provider call caused by recovery/retry;
- no duplicate visible nonce.

A visible correct answer **does not pass** if durable completion is absent.

Blocker tokens:

- `BLOCKED_VISIBLE_NONCE_RESPONSE`
- `BLOCKED_RESPONSE_DELIVERY_COMPLETION`
- `BLOCKED_DUPLICATE_SEMANTIC_EFFECT`

---

# Phase H — post-completion fresh-session continuity

Only after the first Ticket is durably `completed`, invoke the authenticated Dashboard/WebChat **New Session / New Chat** control one more time.

Do **not** submit any message in this second fresh state.

Prove:

- UI enters a clean empty/staged fresh state;
- completed session remains independently addressable in history;
- the UI does not fall back into the just-completed transcript as the active fresh target;
- Gateway logs show no `unknown parent session`, stale parent, missing parent or equivalent session-resolution failure;
- no new Ticket/event/outbox row is created by this New Session action;
- no provider inference/call is started;
- semantic message count remains exactly `1` for Task 092.

This post-completion check is mandatory final acceptance evidence because it proves New Session remains usable after a successful CogentNexus-mediated turn.

Blocker:

`BLOCKED_POST_COMPLETION_NEW_SESSION_CONTINUITY`

---

# Phase I — final preservation and accounting

Before report publication capture:

- controller still MANAGED;
- single canonical loaded source-exact plugin;
- Supervisor still healthy;
- Gateway healthy;
- SQLite integrity `ok`;
- exact Ticket/event/outbox rows created by this task;
- semantic sends exactly `1`;
- direct provider probes `0`;
- normal provider inference attributable to semantic message only;
- no install/reset/manual repair;
- no provider/model/timeout mutation;
- no secret disclosure;
- first fresh semantic session ID/key;
- second post-completion staged New Session evidence.

Do not require another five-minute no-flash observation unless Task 092 evidence shows Supervisor/runtime drift. Task-090 `NO_FLASH_MULTI_TICK_PROVEN` remains accepted otherwise.

---

# Publication fence

No product source change is expected.

Publish exactly one report-only commit:

`docs/operations/coordination/reports/CNX-20260827-092-final-fresh-session-semantic-acceptance.md`

Execution HEAD -> report HEAD must be exactly one report-only commit.

The report must include:

- execution/report HEADs;
- authenticated owner surface/device/scopes without secrets;
- Phase-A existing session snapshot summary;
- first New Session staged-state proof;
- fresh nonce identifier;
- new materialized session ID/key and proof it is new/isolated;
- exact Ticket ID/run ID/session correlation;
- accepted/routed/provider ordering timestamps;
- provider/model correlation;
- visible exact nonce evidence;
- response_ready/delivery_confirmed/completed event evidence;
- duplicate/recovery/outbox accounting;
- second post-completion New Session continuity proof;
- final Ticket/provider/semantic counts;
- live MANAGED preservation;
- secret-disclosure count zero;
- publication fence.

## Required final success token

`PASS_FINAL_FRESH_SESSION_SEMANTIC_TICKET_OLLAMA_DELIVERY_ACCEPTED`

## Required blocker tokens

Use the most specific blocker if success cannot be proven:

- `BLOCKED_FINAL_LIVE_STATE_DRIFT`
- `BLOCKED_FRESH_SESSION_ENTRY`
- `BLOCKED_UNKNOWN_OR_STALE_PARENT_SESSION`
- `BLOCKED_FRESH_SESSION_FALLBACK_TO_EXISTING_SESSION`
- `BLOCKED_FRESH_SESSION_NOT_ISOLATED`
- `BLOCKED_TICKET_BEFORE_PROVIDER_ORDERING`
- `BLOCKED_DUPLICATE_TICKET_OR_ROUTE`
- `BLOCKED_CORRELATED_PROVIDER_INFERENCE`
- `BLOCKED_VISIBLE_NONCE_RESPONSE`
- `BLOCKED_RESPONSE_DELIVERY_COMPLETION`
- `BLOCKED_DUPLICATE_SEMANTIC_EFFECT`
- `BLOCKED_POST_COMPLETION_NEW_SESSION_CONTINUITY`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Completion meaning

Only independent acceptance of:

`PASS_FINAL_FRESH_SESSION_SEMANTIC_TICKET_OLLAMA_DELIVERY_ACCEPTED`

means CogentNexus-OpenClaw v0.9.3 has completed final semantic acceptance, including authenticated owner entry, fresh-session operation, Ticket-before-provider ordering, correlated Ollama inference, durable delivery convergence, visible response and repeatable New Session readiness.
