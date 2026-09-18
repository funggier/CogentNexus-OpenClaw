# CNX-20260918-418 — Preserved Fresh Dashboard Session Ollama Semantic Vertical Slice

Status: `READY_FOR_HERMES`

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260918-417`
- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`
- Parent review: `docs/operations/coordination/reviews/CNX-20260918-417-chatgpt-review.md`
- Parent report: `docs/operations/coordination/reports/CNX-20260918-417-first-post-attestation-ollama-dashboard-semantic-vertical-slice-report.md`
- Installed source candidate: `c1baa815d6894f0d619d4d3695c61a442e206e38`

GitHub remote is authoritative for coordination state.

## Objective

Reuse the exact fresh, empty Dashboard/WebChat session preserved by CNX-417 after the Operator changed its execution selection to Ollama, then perform exactly one semantic owner turn and prove the full Ticket-first Ollama vertical slice.

Do **not** create another New Session.

Target session from CNX-417:

- session key: `agent:main:dashboard:6e96fece-c6ad-47b9-bfb4-680dd8a3a75b`
- session ID: `18fab7b9-2fb1-409f-9aed-d79168aaffdc`

CNX-417 proved this target originally materialized fresh/empty but inherited `openai/gpt-5.6-luna`.

After CNX-417 closeout, the Operator explicitly changed the model selection to:

`qwen3.8:27b`

CNX-418 must independently re-prove that the exact preserved target now resolves to:

`ollama/qwen3.8:27b`

before any semantic send.

## Product invariant under observation

This task should preserve evidence for:

```text
same session identity
  -> execution selection changed
  -> no Ticket/model semantic effect from selection itself
  -> first semantic turn executes through selected Ollama model
  -> CogentNexus continuity remains intact
```

Provider/model choice is execution state, not session identity.

## Absolute semantic budget

Dashboard/WebChat semantic sends:

`maximum 1`

Semantic retry/resend:

`0`

Do not create a second session, alternate channel, CLI owner substitute, direct provider probe, or synthetic Ticket.

## Phase A — fresh authority and live runtime re-proof

Before touching the composer:

1. fetch current remote coordination state;
2. re-read ACTIVE, STATUS, this task, CNX-417 report/review, CNX-416 accepted report/review;
3. require CNX-418 remains `READY_FOR_HERMES`;
4. verify OpenClaw remains `2026.7.1-2`;
5. verify controller remains active/managed;
6. record current generation;
7. verify exactly one canonical CogentNexus plugin remains enabled/loaded;
8. verify installed fingerprint remains:
   `fa7243b4b88fea0b3467a42bc917b1241540c9710ebf495dc04ac1d1963bd41c`;
9. verify Gateway healthy and record PID;
10. verify Supervisor healthy;
11. verify maintenance marker absent;
12. verify Recovery READY;
13. verify Delivery READY;
14. verify pending outbox = 0;
15. verify SQLite integrity = `ok`;
16. verify no actionable recovery/delivery work;
17. verify no active provider/model call.

If runtime health materially drifted:

`BLOCKED_SEMANTIC_PREFLIGHT_DRIFT`

Stop without repair.

## Phase B — exact preserved-session integrity

Re-prove the exact CNX-417 target:

- session key exactly:
  `agent:main:dashboard:6e96fece-c6ad-47b9-bfb4-680dd8a3a75b`;
- session ID exactly:
  `18fab7b9-2fb1-409f-9aed-d79168aaffdc`;
- same Dashboard/WebChat owner surface;
- transcript remains semantically empty:
  - user messages = 0;
  - assistant messages = 0;
- no inherited semantic content appeared after CNX-417;
- no Ticket belongs to this session;
- no model/provider call belongs to this session;
- no assistant delivery belongs to this session;
- no outbox row belongs to this session;
- no reset/delete/compact/new-generation transition occurred;
- the UI still targets this exact session or can safely navigate back to it without creating a new session.

Do not create another session to recover from a mismatch.

If the session is no longer exact/empty:

`BLOCKED_PRESERVED_SESSION_DRIFT`

Stop.

## Phase C — prove operator model-selection result

Read current OpenClaw session metadata and Dashboard UI selection for the exact preserved target.

Require:

- `modelProvider=ollama` or exact equivalent route metadata;
- model = `qwen3.8:27b`;
- any provider/model override fields are coherent with Ollama selection;
- Dashboard UI displays the Ollama/qwen3.8:27b selection or an exact equivalent label;
- default/global OpenClaw route may be recorded separately but must not override the actual target-session evidence.

Also prove the operator selection itself caused no semantic effect since CNX-417:

- Ticket delta attributable to this session = 0;
- direct model-call delta attributable to this session = 0;
- provider semantic request count attributable to this session = 0;
- user/assistant transcript delta = 0;
- delivery/outbox delta = 0.

This is evidence that native provider/model selection is execution-state mutation rather than Ticket intake.

If the exact target is not currently Ollama/qwen3.8:27b:

`BLOCKED_OPERATOR_MODEL_SELECTION_NOT_APPLIED`

Stop.

Do not change model/provider inside CNX-418.

## Phase D — durable baseline immediately before semantic send

After the exact target and route are proven, capture a fresh read-only baseline:

- Ticket count/state counts;
- ticket-event count;
- outbox count/pending count;
- assistant-delivery count/status;
- direct model-call count/status;
- recovery count/status;
- CNX session row and generation for the target;
- OpenClaw session metadata;
- target transcript hash/line/message counts;
- relevant Gateway/CNX log cursor or UTC boundary.

No SQLite writes.

## Phase E — one nonce and one Dashboard semantic send

Only after Phases A-D are GREEN, generate one fresh nonce:

`CNX418-<UTC compact timestamp>-<random uppercase/hex suffix>`

Verify it does not already exist in the target transcript/Ticket evidence.

Enter exactly:

`ตอบกลับข้อความนี้เพียงว่า <NEW_NONCE>`

into the exact preserved Dashboard/WebChat composer.

Visually verify the full text in the intended composer before Send.

Send exactly once.

After Send, semantic budget is consumed.

Record:

- nonce;
- exact send UTC;
- session key/ID;
- current UI target;
- displayed provider/model;
- any request/run ID surfaced by supported evidence.

No resend under any result.

## Phase F — Ticket-first ordering

Correlate the exact preserved session, nonce prompt, run ID, Ticket ID, and provider call using durable evidence.

Require:

1. exactly one new Ticket for the nonce;
2. Ticket owner session equals the preserved target;
3. exactly one `accepted` request lifecycle;
4. exactly one initial `routed` event;
5. admission trace exists;
6. Ticket accepted/routed state is durably committed before the correlated model call begins;
7. no duplicate Ticket;
8. no duplicate initial route;
9. no inference bypasses Ticket admission.

If model inference begins without prior durable Ticket admission:

`BLOCKED_TICKET_FIRST_ORDERING`

If duplicate admission exists:

`BLOCKED_DUPLICATE_ADMISSION`

Stop without resend.

## Phase G — exactly one Ollama inference

Require exactly one model inference attributable to the nonce.

Expected:

- provider = `ollama`;
- model = `qwen3.8:27b`;
- same session/run/Ticket;
- one start;
- one terminal end;
- no retry;
- no second call.

Do not call Ollama directly.

If provider/model differs from the proven Phase-C selection:

`BLOCKED_SELECTED_ROUTE_NOT_HONORED`

If the one normal inference fails:

`BLOCKED_OLLAMA_INFERENCE`

Stop.

## Phase H — exact result and durable completion

Require:

- exactly one assistant result;
- normalized assistant text equals the nonce;
- exactly one visible Dashboard/WebChat reply;
- exactly one result-ready/response-ready durable event or current equivalent;
- durable delivery confirmation/settlement for the exact session/run/Ticket;
- Ticket terminal status `completed`;
- no pending outbox attributable to result;
- no recovery-generated duplicate;
- no competing assistant payload;
- no second model call;
- no duplicate visible nonce.

A correct visible reply without durable completion is not PASS.

Use:

- `BLOCKED_VISIBLE_NONCE_RESPONSE`;
- `BLOCKED_DURABLE_DELIVERY_COMPLETION`;
- `BLOCKED_DUPLICATE_SEMANTIC_EFFECT`

as appropriate.

## Phase I — preserve successful session

If PASS, keep this exact session intact for the next same-session selection-switch task.

Do not:

- create New Session;
- send second message;
- reset;
- delete;
- compact;
- change provider/model again;
- manually edit session metadata.

Capture final:

- session key/ID;
- CNX session generation;
- Ticket ID;
- run/model-call ID;
- exact event sequence;
- provider/model;
- transcript hash/message counts;
- controller mode/generation;
- plugin identity;
- Gateway PID/health;
- Recovery/Delivery;
- pending outbox;
- SQLite integrity;
- semantic-send count = 1;
- normal model-call count attributable to task = 1;
- direct probe count = 0;
- manual mutation count = 0.

## PASS classification

Only if all required evidence is complete:

`PASS_PRESERVED_SESSION_OLLAMA_TICKET_FIRST_VERTICAL_SLICE`

## Blocker classifications

- `BLOCKED_SEMANTIC_PREFLIGHT_DRIFT`
- `BLOCKED_PRESERVED_SESSION_DRIFT`
- `BLOCKED_OPERATOR_MODEL_SELECTION_NOT_APPLIED`
- `BLOCKED_TICKET_FIRST_ORDERING`
- `BLOCKED_DUPLICATE_ADMISSION`
- `BLOCKED_SELECTED_ROUTE_NOT_HONORED`
- `BLOCKED_OLLAMA_INFERENCE`
- `BLOCKED_VISIBLE_NONCE_RESPONSE`
- `BLOCKED_DURABLE_DELIVERY_COMPLETION`
- `BLOCKED_DUPLICATE_SEMANTIC_EFFECT`
- `BLOCKED_EVIDENCE`

## Hard fences

- New Session/New Chat actions: 0.
- Dashboard semantic sends: max 1.
- Semantic retry/resend: 0.
- Direct Ollama/model probes: 0.
- OpenAI semantic requests: 0.
- Provider/model selection changes by executor: 0.
- Provider/model/auth config mutation: 0.
- Installer/install-over: 0.
- Plugin lifecycle mutation: 0.
- Gateway restart/reload/repair: 0.
- Lifecycle start/stop/restart: 0.
- Manual Ticket/outbox/recovery/SQLite mutation: 0.
- Manual durable replay/delivery: 0.
- Session reset/delete/compact: 0.
- OpenClaw dependency patch/version change: 0.
- Release/tag/main: 0.
- Force push/history rewrite: 0.
- Do not create/start CNX-419 yourself.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260918-418-preserved-session-ollama-semantic-vertical-slice-report.md`

Include:

- fresh GitHub authority;
- runtime health preflight;
- exact preserved-session identity;
- proof transcript remained empty;
- proof operator model selection is now Ollama/qwen3.8:27b;
- zero semantic side effect from selection itself;
- durable baseline;
- nonce/send count;
- Ticket/run/model-call IDs;
- admission trace;
- accepted/routed/model-start ordering;
- selected route vs actual inference route;
- assistant/visible reply evidence;
- durable completion evidence;
- duplicate accounting;
- final preserved-session evidence;
- exact cardinality ledger;
- final classification.

Then:

1. set ACTIVE.md = `WAITING_FOR_CHATGPT_REVIEW`;
2. set STATUS.md = `WAITING_FOR_CHATGPT_REVIEW`;
3. verify local HEAD == remote HEAD;
4. verify clean publication worktree;
5. if PASS, preserve the exact session intact;
6. stop;
7. do not create/start CNX-419.
