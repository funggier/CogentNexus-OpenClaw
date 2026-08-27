# CNX-20260827-099 — Final Authenticated Fresh-Session Semantic Acceptance

Status: `READY_FOR_HERMES`

Execution mode: `LIVE_FINAL_AUTHENTICATED_FRESH_SESSION_SEMANTIC_ACCEPTANCE`

Current authorization: `TASK098_ACCEPTED_ONE_FRESH_DASHBOARD_SESSION_ONE_SEMANTIC_MESSAGE_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Perform the final end-to-end semantic acceptance through the already-authenticated OpenClaw Dashboard/WebChat owner surface using the fresh staged Dashboard session accepted by Task 098.

Prove the complete chain:

`fresh authenticated Dashboard session -> durable Ticket accepted/routed before provider -> one correlated Ollama inference -> durable final payload staged before native delivery -> exact visible nonce once -> response_ready -> delivery_confirmed -> completed`

Then, after successful completion only, prove another New Session transition can be entered without a second semantic/provider effect. The post-completion New Session action may use the operator-approved state-gated bounded retry policy; the semantic send itself may not be retried.

## Accepted predecessor state

Task 096 live deployment accepted exact installed source:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Installed plugin fingerprint:

`df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`

Live baseline:

- MANAGED generation `24`;
- one canonical candidate-exact plugin generation;
- startup/Supervisor/Gateway/SQLite/Ollama healthy;
- Task-092 failed semantic evidence preserved and retired;
- `NO_FLASH_MULTI_TICK_REPROVEN`.

Task 098 report:

`bd068ca94e10525bd0a0743b6c1916cb56de78a0`

Task 098 independent disposition:

`ACCEPT_STATE_GATED_DASHBOARD_FRESH_SESSION_READY_NO_SEND`

Readiness token:

`DASHBOARD_OWNER_FRESH_SESSION_READY_NO_SEND`

Task 098 selected an authenticated empty/staged Dashboard session without creating another session and with zero semantic/provider effect.

## Retry policy v1 carried forward

Read-only operations may use up to 3 attempts total.

Low-impact state-changing session-management actions may use up to 2 attempts total only when a bounded grace interval and fresh state prove attempt 1 had no effect. `unverifiable` means state unknown, not not-executed.

The semantic action in this task is **single-attempt only**:

- one brand-new nonce;
- one exact user send;
- no resend;
- no retry;
- no alternate channel/CLI/provider probe if it fails.

---

# Absolute semantic and mutation fence

Exactly one semantic user message is authorized, only through the authenticated Dashboard/WebChat target session.

Forbidden before, during and after the semantic turn:

- `openclaw agent`;
- CLI `--session-key agent:main:main` as an owner substitute;
- `chat.inject`;
- `sessions_send`;
- channel sends;
- synthetic/manual Ticket creation;
- direct Ollama/provider probes;
- second semantic message or resend;
- reuse of Task-076 or Task-092 nonce/session/run/Ticket;
- install/install-over/uninstall/reset/cleanup;
- manual plugin-generation mutation;
- controller/startup/Supervisor/AGENTS/ownership/runtime/config mutation;
- SQLite edits or repair of prior evidence;
- provider/model/timeout changes;
- restart/reboot to make the test pass;
- merge/tag/release/force push.

Normal runtime effects of the one authorized semantic turn are allowed.

After successful durable completion only, one post-completion New Session transition is allowed, with at most one state-gated retry under retry policy v1 and with zero semantic content.

If the semantic send fails, times out, duplicates, or produces ambiguous durable state, capture evidence and stop. Do not resend.

---

# Phase A — final preflight before nonce generation

Before generating any nonce:

1. Record coordination execution HEAD.
2. Verify Task 098 report/review are ancestors and publication fence is valid.
3. Verify exact OpenClaw build remains `2026.7.1-2 (0790d9f)`.
4. Verify controller remains MANAGED generation 24.
5. Verify exactly one canonical loaded/enabled CogentNexus plugin and installed fingerprint equals `df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`.
6. Verify Gateway healthy.
7. Verify Supervisor healthy/recent successful natural tick.
8. Verify SQLite integrity `ok`.
9. Snapshot exact pre-test counts for tickets, ticket events, ticket outbox, direct-run/delivery/workflow tables that exist in the current schema.
10. Snapshot current Dashboard sessions through authenticated read-only state.
11. **Record the exact currently selected readiness target session ID/key.** It must be a Dashboard session, distinct from Main Session, distinct from Task-092 retired semantic session/history, and have empty/staged transcript before first send.
12. Prove authenticated Dashboard owner/control surface is active without exposing token/password values.
13. Prove no active semantic/provider operation.

If exact selected target identity is ambiguous, transcript is non-empty, target falls back to Main/old history, live state drifted, or a credential must be re-entered by the executor, stop before nonce generation.

Required blocker token for this condition:

`BLOCKED_FINAL_PREFLIGHT_OR_FRESH_TARGET_IDENTITY`

---

# Phase B — generate nonce and perform the single semantic send

Only after Phase A passes, generate a fresh execution-time nonce:

`CNXSEM3-<UTC compact timestamp>-<random uppercase/hex suffix>`

The nonce must not pre-exist in current sessions/logs/Tickets and must not reuse any historical nonce.

Send exactly this one user message through the selected authenticated Dashboard composer:

`ตอบกลับข้อความนี้เพียงว่า <NEW_NONCE>`

Semantic send count must remain exactly `1` for the entire task.

Record non-secret correlation metadata immediately after send, including target session ID/key, request/run identifiers and send timestamp when available.

---

# Phase C — prove fresh-session isolation

After first send, prove:

1. the exact session ID/key used is the Phase-A selected Dashboard target;
2. it is distinct from Main Session and Task-092/Task-076 historical sessions;
3. no inherited user/assistant semantic transcript existed before the one authorized prompt;
4. the nonce prompt is the first semantic user message in that target;
5. no fallback/unknown-parent/stale-parent/reconnect substitution occurred;
6. only one semantic send is present.

If session identity changes unexpectedly, falls back, or inherited transcript is detected, stop without resend:

`BLOCKED_FRESH_SESSION_NOT_ISOLATED`

---

# Phase D — prove durable Ticket-before-provider ordering

Correlate the exact Dashboard session/message/run to durable CogentNexus state.

Durable DB evidence is mandatory; logs alone are insufficient.

Require exactly one new Ticket for the one authorized semantic message.

Required ordering:

1. owner Dashboard message enters normal pre-inference admission;
2. exactly one Ticket is accepted;
3. exactly one durable route event is committed;
4. Ticket accepted/routed evidence exists before correlated Ollama inference begins;
5. no duplicate Ticket or duplicate route event exists;
6. direct/provider continuation occurs only after admission/routing.

Blockers:

`BLOCKED_TICKET_BEFORE_PROVIDER_ORDERING`

`BLOCKED_DUPLICATE_TICKET_OR_ROUTE`

---

# Phase E — correlated provider inference

No direct readiness probe is allowed.

Prove exactly one normal provider inference correlated to this session/run/Ticket.

Expected provider/model:

`ollama/qwen3.5:9b`

Record start/end timing and correlation IDs without secrets.

If the provider fails/times out, capture durable state and stop. No resend, no model/timeout mutation, no direct probe.

Blocker:

`BLOCKED_CORRELATED_PROVIDER_INFERENCE`

---

# Phase F — durable payload staging before native delivery

This is the defect repaired by Task 093 and must be proven live.

Require durable assistant-delivery evidence bound to the exact owner/session/run before native visible delivery is accepted.

Prove:

1. exactly one final assistant payload is staged durably for the exact owner/session/run;
2. staged payload text normalizes exactly to the nonce and is not empty;
3. staging occurs before or at the native delivery boundary required by the repaired implementation;
4. no second competing staged payload exists;
5. no fallback fail-closed recovery message replaces the expected payload.

A visible correct nonce without durable staged payload fails acceptance.

Blocker:

`BLOCKED_DURABLE_FINAL_PAYLOAD_STAGING`

---

# Phase G — visible reply and durable settlement

Require the visible Dashboard assistant reply to equal the nonce exactly, allowing whitespace normalization only.

Require durable lifecycle for the same Ticket/run/session:

`accepted -> routed -> response_ready -> delivery_confirmed -> completed`

Prove:

- exactly one `response_ready`;
- exactly one visible nonce response;
- exact owner/session/run settlement;
- exactly one `delivery_confirmed`;
- Ticket terminal state `completed`;
- no Ticket left at accepted/routed/response_ready after visible delivery;
- no duplicate outbox delivery;
- no generic `cogent-resume-*` promotion;
- no workflow/durable duplicate promotion;
- no second provider inference;
- no duplicate visible nonce.

A visible correct reply without durable `delivery_confirmed` and `completed` is a failure.

Blockers:

`BLOCKED_VISIBLE_NONCE_RESPONSE`

`BLOCKED_RESPONSE_DELIVERY_COMPLETION`

`BLOCKED_DUPLICATE_SEMANTIC_EFFECT`

---

# Phase H — post-completion New Session continuity

Only after the exact Ticket is durably `completed`, use the Dashboard New Session control with zero semantic content.

State-gated retry policy applies to this low-impact action:

### Attempt 1

1. Snapshot current completed session identity, session inventory, Ticket/event/outbox/provider counts.
2. Issue New Session once.
3. If immediately unverifiable, do not re-issue.
4. Wait at least 5 seconds and re-read UI/session state.

### Retry decision

- If one new clean fresh/staged session appears: attempt 1 succeeded; no retry.
- If fresh evidence proves no effect at all: one attempt-2 retry is allowed.
- If effect appears late, more than one session appears, state is ambiguous/partial, or any semantic/provider activity appears: no retry; stop.

### Required final proof

- UI is in a clean empty/staged fresh state;
- completed semantic session remains addressable in history;
- no fallback into just-completed transcript;
- no stale/unknown/missing parent error;
- no new Ticket/event/outbox semantic row;
- no provider inference/call;
- semantic send count remains exactly 1.

Blocker:

`BLOCKED_POST_COMPLETION_NEW_SESSION_CONTINUITY`

---

# Phase I — final preservation/accounting

Verify after all allowed activity:

- controller MANAGED generation 24;
- one canonical candidate-exact plugin;
- Supervisor/Gateway healthy;
- SQLite integrity ok;
- exact new rows/events attributable to the one semantic turn documented;
- semantic sends = 1;
- direct provider probes = 0;
- normal provider inferences for task = 1;
- no install/reset/manual repair;
- no provider/model/timeout mutation;
- no secret disclosure;
- Task-092 retired evidence unchanged;
- Task-097 duplicate empty sessions not manually deleted/normalized;
- post-completion New Session produced zero additional semantic/provider effects.

A new five-minute no-flash observation is not required unless runtime drift/recovery churn appears; Task 096 `NO_FLASH_MULTI_TICK_REPROVEN` remains accepted baseline.

---

# Publication fence

No product source commit is expected.

Publish exactly one report-only commit:

`docs/operations/coordination/reports/CNX-20260827-099-final-authenticated-fresh-session-semantic-acceptance.md`

Report must include:

- execution HEAD and report HEAD;
- exact Phase-A selected session ID/key;
- fresh nonce;
- semantic send count;
- Ticket/session/run/request IDs;
- Ticket acceptance/routing timestamps and provider start timing;
- provider/model and one-call proof;
- durable staged-payload evidence and ordering relative to native delivery;
- visible exact nonce evidence;
- response_ready/delivery_confirmed/completed evidence;
- duplicate accounting;
- post-completion New Session attempt/retry accounting;
- final live health/counts;
- explicit zero-secret statement;
- publication fence statement.

## Required success token

`PASS_FINAL_AUTHENTICATED_FRESH_SESSION_SEMANTIC_ACCEPTED`

## Required blocker tokens

- `BLOCKED_FINAL_PREFLIGHT_OR_FRESH_TARGET_IDENTITY`
- `BLOCKED_FRESH_SESSION_NOT_ISOLATED`
- `BLOCKED_TICKET_BEFORE_PROVIDER_ORDERING`
- `BLOCKED_DUPLICATE_TICKET_OR_ROUTE`
- `BLOCKED_CORRELATED_PROVIDER_INFERENCE`
- `BLOCKED_DURABLE_FINAL_PAYLOAD_STAGING`
- `BLOCKED_VISIBLE_NONCE_RESPONSE`
- `BLOCKED_RESPONSE_DELIVERY_COMPLETION`
- `BLOCKED_DUPLICATE_SEMANTIC_EFFECT`
- `BLOCKED_POST_COMPLETION_NEW_SESSION_CONTINUITY`
- `BLOCKED_LIVE_HEALTH_REGRESSION`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Final gate

Only independent review of a valid report with:

`PASS_FINAL_AUTHENTICATED_FRESH_SESSION_SEMANTIC_ACCEPTED`

and a valid report-only publication fence may close the OpenClaw final semantic acceptance. Do not claim final acceptance from a visible reply alone.
