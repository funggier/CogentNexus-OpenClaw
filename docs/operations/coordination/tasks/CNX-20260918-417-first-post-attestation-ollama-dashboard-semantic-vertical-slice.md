# CNX-20260918-417 — First Post-Attestation Ollama Dashboard Semantic Vertical Slice

Status: `READY_FOR_HERMES`

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260918-416`
- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`
- Parent review: `docs/operations/coordination/reviews/CNX-20260918-416-chatgpt-review.md`
- Parent report: `docs/operations/coordination/reports/CNX-20260918-416-repaired-installer-reentry-live-runtime-attestation-report.md`
- Installed source candidate: `c1baa815d6894f0d619d4d3695c61a442e206e38`

GitHub remote is authoritative for coordination state.

## Objective

Perform exactly one real semantic owner turn through the normal authenticated OpenClaw Dashboard/WebChat surface using the already-selected Ollama model.

Prove the user-facing vertical slice:

```text
fresh authenticated Dashboard/WebChat session
  -> one owner message
  -> live CogentNexus before_agent_run
  -> exactly one durable Ticket accepted/routed
  -> accepted/routed before provider model call
  -> exactly one Ollama qwen3.8:27b inference
  -> exactly one assistant result
  -> durable delivery settlement
  -> exactly one visible nonce reply
```

This is not a provider-switch task yet.

Do not change provider or model.

## Why this task is now authorized

CNX-416 proved on the current installed runtime:

- exact repaired candidate installed;
- plugin enabled and loaded;
- controller active/managed generation 107;
- Gateway healthy;
- Recovery/Delivery READY;
- SQLite integrity OK;
- current OpenClaw route remains `ollama/qwen3.8:27b`;
- live `cogentnexus.runtimeAttestation` returned:
  - `runnerReady=true`;
  - `globalHookCount=7`;
  - `latestRegistryPluginHookCount=7`;
  - `classification=PRESENT`.

Therefore the remaining question is no longer hook visibility. It is real semantic behavior through the normal owner surface.

## Absolute semantic budget

Exactly one semantic user message is authorized.

Semantic send count for CNX-417:

`1 maximum`

No resend, retry, alternate transport, direct provider probe, or second user message is allowed under any result.

Normal runtime effects caused by this one message are allowed.

## Forbidden semantic substitutes

Do not use:

- `openclaw agent`;
- CLI `--session-key` as an owner substitute;
- `chat.inject`;
- `sessions_send`;
- Discord/channel send;
- direct Ollama HTTP/API/CLI inference;
- synthetic/manual Ticket creation;
- manual hook invocation;
- a second Dashboard message;
- a second model call initiated manually.

The semantic turn must enter through the normal authenticated Dashboard/WebChat composer.

## Phase A — fresh authority and production re-proof

Before touching Dashboard session controls:

1. fetch current remote coordination state;
2. re-read ACTIVE, STATUS, this task, CNX-416 report/review;
3. require CNX-417 remains `READY_FOR_HERMES`;
4. verify installed OpenClaw remains `2026.7.1-2`;
5. verify controller remains `active/managed`;
6. record generation; expected predecessor generation is 107 but use live state;
7. verify exactly one canonical CogentNexus plugin is enabled/loaded;
8. verify installed plugin fingerprint remains:
   `fa7243b4b88fea0b3467a42bc917b1241540c9710ebf495dc04ac1d1963bd41c`;
9. verify Gateway healthy and record PID;
10. verify Supervisor healthy/recent successful state;
11. verify maintenance marker absent;
12. verify Recovery READY;
13. verify Delivery READY;
14. verify pending outbox = 0;
15. verify SQLite integrity = `ok`;
16. verify no actionable recovery/delivery work;
17. verify no active model/provider call;
18. verify selected OpenClaw provider/model is still:
    `ollama/qwen3.8:27b`;
19. read current CogentNexus config relevant to admission without exposing secrets and require the effective semantic path remains enabled:
    - Ticket-first admission enabled;
    - pre-inference admission enabled;
    - enforced/managed authority enabled as applicable;
20. call no attestation RPC unless needed for read-only preflight; CNX-416's accepted PRESENT result is the current baseline. If a new attestation is used because process identity changed, it must be read-only and occur before nonce generation.

If live state has materially drifted, stop before any semantic send:

`BLOCKED_SEMANTIC_PREFLIGHT_DRIFT`

Do not repair live state in CNX-417.

## Phase B — baseline durable and UI state

Before creating the fresh semantic target capture read-only baselines:

- Ticket count and state counts;
- ticket-event count;
- ticket-outbox count/pending count;
- assistant-delivery count/status where applicable;
- direct model call count/status;
- recovery count/status;
- current active session ownership rows/generations;
- current OpenClaw session inventory;
- current Dashboard/WebChat session/transcript identity;
- relevant Gateway/CogentNexus log cursor or timestamp boundary.

No SQLite writes are allowed.

## Phase C — enter one clean fresh Dashboard/WebChat target

Use the existing authenticated OpenClaw Dashboard/WebChat Control UI through the normal browser/profile.

Invoke the supported New Session / New Chat UI control at most once before the semantic send.

A staged pre-send session that is not yet persisted in `sessions.list` is acceptable if exact installed OpenClaw behaves that way.

Before nonce generation require:

- the composer is visible and empty;
- the active UI is not displaying inherited semantic transcript as the target;
- no Ticket/event/provider count changed due to New Session alone;
- no provider inference began;
- no stale/unknown/missing-parent error occurred;
- authenticated owner/operator control remains established;
- provider/model shown for the target remains `ollama/qwen3.8:27b`.

If a safe authenticated fresh target cannot be proven, stop before semantic send:

`BLOCKED_FRESH_DASHBOARD_TARGET`

Do not fall back to CLI or another channel.

## Phase D — one nonce and one semantic send

Only after Phase C is GREEN, generate one fresh execution-time nonce:

`CNX417-<UTC compact timestamp>-<random uppercase/hex suffix>`

Prove the nonce does not already occur in current session/Ticket evidence.

Send exactly:

`ตอบกลับข้อความนี้เพียงว่า <NEW_NONCE>`

through the authenticated Dashboard/WebChat composer.

Record:

- nonce;
- exact send UTC time;
- current browser/window/session identity;
- provider/model displayed at send time;
- request/run/session identifiers exposed by supported evidence.

After the Send action occurs, the semantic budget is consumed.

Do not resend under any outcome.

## Phase E — fresh session materialization and owner identity

After the send, prove:

1. exact materialized session ID/key;
2. the session is attributable to the authenticated Dashboard/WebChat owner surface;
3. it was not present as an existing semantic target before Phase C, unless exact OpenClaw staged-session semantics prove the pre-materialized identity;
4. it does not inherit an earlier semantic transcript;
5. the nonce prompt is the first semantic user message in the new target;
6. there was exactly one user semantic send.

If session identity/freshness cannot be proven:

`BLOCKED_FRESH_SESSION_IDENTITY`

Stop without resend.

## Phase F — Ticket-first admission before provider

Correlate the exact owner session, prompt/nonce, run ID, Ticket ID, and model call using durable evidence.

Require:

- exactly one new Ticket attributable to the nonce prompt;
- Ticket owner session equals the Phase-E materialized session;
- exactly one `accepted` lifecycle for the request;
- exactly one `routed` event;
- admission trace exists for the live turn;
- Ticket acceptance/routing is durably committed before the correlated provider/model call begins;
- no duplicate Ticket;
- no duplicate initial route;
- no provider inference occurs for the semantic request without Ticket-first admission.

Use DB/event timestamps plus model-call/runtime evidence sufficient to establish ordering.

If no Ticket exists or provider begins first:

`BLOCKED_TICKET_FIRST_ORDERING`

If duplicates exist:

`BLOCKED_DUPLICATE_ADMISSION`

## Phase G — exactly one correlated Ollama inference

Require one and only one normal model inference caused by the semantic message.

Expected:

- provider: `ollama`;
- model: `qwen3.8:27b`.

Prove correlation to the same session/run/Ticket using available direct-model-call/OpenClaw runtime evidence.

Record:

- model call start/end;
- provider/model;
- run/call correlation IDs;
- outcome;
- no second call/retry.

Do not call Ollama separately.

If the normal inference fails or times out:

`BLOCKED_OLLAMA_INFERENCE`

Capture evidence and stop.

## Phase H — assistant result, durable delivery, and visible reply

Require the single assistant result to normalize exactly to the nonce.

Prove the current v0.9.5 durable lifecycle for the same Ticket/session/run.

At minimum require:

- exactly one `response_ready` or current equivalent durable result-ready event;
- exactly one visible Dashboard/WebChat assistant response;
- visible text equals the nonce after surrounding-whitespace normalization;
- durable delivery confirmation/settlement through the current Dashboard/WebChat delivery contract;
- Ticket reaches terminal `completed`;
- no pending outbox remains for this result;
- no competing assistant payload;
- no recovery-generated duplicate result;
- no second model call;
- no duplicate visible nonce.

Do not require a historical table/row shape if current v0.9.5 legitimately settles through a newer equivalent contract; document the exact current durable path used.

A visible nonce alone is insufficient if durable settlement cannot be proven.

Blockers:

- `BLOCKED_VISIBLE_NONCE_RESPONSE`
- `BLOCKED_DURABLE_DELIVERY_COMPLETION`
- `BLOCKED_DUPLICATE_SEMANTIC_EFFECT`

## Phase I — preservation and handoff state

Do **not** create another New Session after success.

Preserve the successfully completed CNX-417 Dashboard/WebChat session for the next same-session model/provider-switch task.

Capture final read-only state:

- exact session ID/key;
- Ticket ID;
- run ID/model-call ID;
- Ticket event sequence;
- controller mode/generation;
- plugin identity;
- Gateway health/PID;
- Recovery verdict;
- Delivery verdict;
- pending outbox;
- SQLite integrity;
- provider/model remains `ollama/qwen3.8:27b`;
- semantic send count = 1;
- provider inference count attributable to task = 1;
- direct provider probes = 0;
- manual repair/mutation count = 0.

Do not reset/delete/compact the accepted session.

## Success classification

Use only if all mandatory evidence is proven:

`PASS_OLLAMA_DASHBOARD_TICKET_FIRST_VERTICAL_SLICE`

## Blocker classifications

Use the narrowest applicable:

- `BLOCKED_SEMANTIC_PREFLIGHT_DRIFT`
- `BLOCKED_FRESH_DASHBOARD_TARGET`
- `BLOCKED_FRESH_SESSION_IDENTITY`
- `BLOCKED_TICKET_FIRST_ORDERING`
- `BLOCKED_DUPLICATE_ADMISSION`
- `BLOCKED_OLLAMA_INFERENCE`
- `BLOCKED_VISIBLE_NONCE_RESPONSE`
- `BLOCKED_DURABLE_DELIVERY_COMPLETION`
- `BLOCKED_DUPLICATE_SEMANTIC_EFFECT`
- `BLOCKED_EVIDENCE`

## Hard fences

- Semantic Dashboard/WebChat sends: max 1.
- Semantic resend/retry: 0.
- Direct Ollama/model probes: 0.
- OpenAI requests: 0.
- Provider/model selection changes: 0.
- Provider/model/auth config mutation: 0.
- Installer/install-over: 0.
- Plugin enable/disable/install/remove: 0.
- Gateway restart/reload/repair: 0.
- Lifecycle start/stop/restart: 0.
- Manual Ticket/outbox/recovery/SQLite mutation: 0.
- Manual durable replay/delivery: 0.
- Session reset/delete/compact: 0.
- Post-completion New Session: 0.
- OpenClaw dependency patch/version change: 0.
- Release/tag/main: 0.
- Force push/history rewrite: 0.
- Do not create/start CNX-418 yourself.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260918-417-first-post-attestation-ollama-dashboard-semantic-vertical-slice-report.md`

Include:

- fresh GitHub authority;
- live preflight;
- config/admission gate evidence;
- baseline durable counts;
- fresh Dashboard target proof;
- nonce and exact send count;
- exact materialized session ID/key;
- Ticket/run/model-call IDs;
- admission trace;
- accepted/routed vs provider-start ordering;
- provider/model and exactly-one-call proof;
- assistant result/visible nonce evidence;
- durable delivery/completion evidence;
- duplicate accounting;
- final health/durable-state preservation;
- explicit semantic/provider/mutation cardinality ledger;
- final classification.

Then:

1. set ACTIVE.md = `WAITING_FOR_CHATGPT_REVIEW`;
2. set STATUS.md = `WAITING_FOR_CHATGPT_REVIEW`;
3. verify local HEAD == remote HEAD;
4. verify clean publication worktree;
5. preserve the successful semantic session if PASS;
6. stop;
7. do not create/start CNX-418.
