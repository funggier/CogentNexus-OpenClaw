# CNX-20260918-420 — Operator-Created Fresh Session Ollama Route and Ticket-First Discrimination

Status: `READY_FOR_HERMES`

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260918-419`
- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`
- Parent report: `docs/operations/coordination/reports/CNX-20260918-419-preserved-draft-enter-submit-ollama-ticket-first-report.md`
- Parent review: `docs/operations/coordination/reviews/CNX-20260918-419-chatgpt-review.md`

GitHub remote is authoritative.

## Operator authorization after CNX-419 review

The CNX-419 review originally held further semantic requests pending more characterization.

After that review, the Operator supplied new direct authority and a concrete diagnostic hypothesis:

- the browser may have held stale provider/model presentation state;
- after refreshing the browser, the UI showed `openai/gpt-5.6-luna`;
- the Operator wants to abandon the reused CNX-417/418/419 target;
- the Operator will personally create a fresh session, select `qwen3.8:27b`, enter the test prompt, and send it;
- Hermes must first tell the Operator when to do this;
- after sending, the Operator will tell Hermes: **`ส่งแล้ว`**.

This task is the explicit successor authority for exactly one fresh semantic turn.

It does **not** authorize a production repair.

## Objective

Discriminate three cases with one Operator-owned fresh-session turn:

1. fresh session routes to `ollama/qwen3.8:27b` and CogentNexus Ticket-first lineage exists;
2. fresh session routes correctly to Ollama but still bypasses CogentNexus Ticket-first admission;
3. fresh session still executes through another provider/model, reproducing a real selected-route persistence/runtime-routing defect beyond stale browser presentation.

Do not reuse the CNX-419 session.

## Absolute browser ownership

Hermes must **not**:

- click New Session;
- refresh the browser;
- select provider/model;
- focus/type in the composer;
- click Send;
- press Enter/Ctrl+Enter;
- use UI Automation to perform any browser mutation.

The Operator owns all browser actions for the semantic turn.

Hermes may use read-only local/runtime/browser evidence where available, but may not perform browser mutations.

## Semantic budget

- fresh sessions created by Operator: exactly 1;
- semantic messages sent by Operator: maximum 1;
- semantic retries/resends: 0;
- Hermes semantic sends: 0;
- direct Ollama/OpenAI probes: 0.

## Stage 1 — Hermes preflight before asking the Operator

Before telling the Operator to act, Hermes must perform read-only preflight and capture a durable baseline.

Require:

- current remote branch/coordination authority;
- CNX-420 remains `READY_FOR_HERMES`;
- OpenClaw version remains `2026.7.1-2`;
- controller healthy and expected mode recorded;
- canonical CogentNexus plugin enabled/loaded;
- installed plugin fingerprint recorded;
- Gateway healthy and PID recorded;
- Supervisor healthy;
- maintenance/recovery hazard absent;
- Recovery READY;
- Delivery READY;
- pending outbox = 0;
- SQLite integrity = `ok`;
- no active provider/model call;
- no active semantic acceptance run that would contaminate cardinality;
- durable baseline counts captured for:
  - Tickets;
  - ticket events;
  - model calls;
  - assistant deliveries;
  - outbox;
  - recoveries;
  - CNX sessions.

Also record read-only current configured/default route facts for agent `main` when available, but do not mutate them.

If runtime health is not safe for a single semantic acceptance:

`BLOCKED_OPERATOR_TEST_PREFLIGHT`

Stop without asking the Operator to send.

## Stage 2 — explicit WAIT for Operator action

If Stage 1 is GREEN, Hermes must stop execution and send the Operator a clear instruction in chat.

Hermes must provide one fresh nonce in this format:

`CNX420-<UTC compact timestamp>-<random uppercase/hex suffix>`

Then Hermes must tell the Operator, in substance:

> Preflight ผ่านแล้วครับ ตอนนี้กรุณาทำเองดังนี้:
> 1. Refresh หน้า Dashboard หนึ่งครั้ง
> 2. กด New Session
> 3. เลือก Ollama / `qwen3.8:27b`
> 4. ใส่ข้อความ `ตอบกลับข้อความนี้เพียงว่า <NONCE>`
> 5. ตรวจให้แน่ใจว่า UI แสดง `qwen3.8:27b` ก่อนส่ง
> 6. ส่งข้อความเองเพียง 1 ครั้ง
> 7. กลับมาบอกผมว่า `ส่งแล้ว`
>
> ผมจะยังไม่ตรวจ post-send จนกว่าคุณจะบอกว่า `ส่งแล้ว`

At this point:

- do not continue automatically;
- do not inspect post-send state prematurely;
- do not create another nonce;
- do not send anything on the Operator's behalf;
- wait for the explicit Operator message `ส่งแล้ว`.

Coordination may be marked `WAITING_FOR_OPERATOR_ACTION` while paused.

## Stage 3 — resume only after Operator says “ส่งแล้ว”

Only after receiving the explicit Operator confirmation `ส่งแล้ว`, resume read-only evidence collection.

First identify the one newly created Dashboard session from native OpenClaw state.

Capture:

- fresh session key;
- fresh session ID;
- creation/update timestamps;
- transcript path/hash;
- exact user message and nonce;
- exact assistant response if any;
- session provider/model metadata before/after where reconstructible;
- native assistant provider;
- native assistant model;
- native assistant API/runtime;
- run/idempotency IDs if available.

Do not rely on the UI label as authoritative for the actual execution route.

The native assistant transcript/provider metadata is authoritative for actual provider/model execution.

## Stage 4 — fresh-session route classification

Classify the actual execution route independently.

### Route correct

If native execution is exactly:

- provider = `ollama`;
- model = `qwen3.8:27b`;

then route result:

`FRESH_SESSION_ROUTE_OLLAMA_CONFIRMED`

### Route mismatch reproduced

If native execution is not `ollama/qwen3.8:27b`, record exact provider/model/API/runtime and classify:

`FRESH_SESSION_SELECTED_ROUTE_MISMATCH_REPRODUCED`

This is stronger evidence than CNX-419 because the browser was refreshed and the session was freshly created by the Operator.

Do not auto-correct or resend.

## Stage 5 — Ticket-first classification

For the exact fresh user turn, correlate durable CogentNexus evidence:

- exactly one Ticket;
- accepted event;
- routed event;
- admission trace;
- run/session correlation;
- model-call correlation;
- assistant-delivery/outbox lineage;
- terminal completion where applicable.

### Ticket-first present

If Ticket-first lineage precedes correlated model execution:

`FRESH_SESSION_TICKET_FIRST_CONFIRMED`

### Ticket-first bypass

If a native provider response exists but Ticket/admission lineage remains absent:

`FRESH_SESSION_TICKET_FIRST_BYPASS_REPRODUCED`

Do not repair or resend.

## Final combined classifications

Use the most precise combined result.

### Full PASS

If actual route is `ollama/qwen3.8:27b` and complete Ticket-first/durable lineage is present:

`PASS_OPERATOR_FRESH_SESSION_OLLAMA_TICKET_FIRST_VERTICAL_SLICE`

### Correct route, CNX admission still broken

If actual route is Ollama but Ticket-first is absent:

`FAIL_FRESH_SESSION_OLLAMA_ROUTE_TICKET_FIRST_BYPASS`

This isolates the remaining primary defect to CogentNexus admission/continuity.

### Route mismatch plus Ticket-first bypass

If actual route differs and Ticket-first is absent:

`FAIL_FRESH_SESSION_ROUTE_MISMATCH_AND_TICKET_FIRST_BYPASS`

### Route mismatch with Ticket-first present

If CNX Ticket-first exists but actual route differs:

`FAIL_FRESH_SESSION_ROUTE_MISMATCH_WITH_TICKET_FIRST_PRESENT`

### Evidence failure

`BLOCKED_FRESH_SESSION_EVIDENCE`

## Interpretation rule

Do not conclude “browser stale was the cause” merely because the fresh session behaves correctly.

Instead report:

- CNX-419 was consistent with stale presentation state;
- CNX-420 fresh-session route behavior either reproduced or did not reproduce the mismatch.

Similarly, if the fresh session reproduces the mismatch, browser staleness alone is insufficient to explain CNX-419.

## Hard fences

- Hermes browser mutation: 0.
- Hermes New Session action: 0.
- Hermes provider/model selection action: 0.
- Hermes typing/send/key action: 0.
- Operator New Session action: exactly 1 when instructed.
- Operator semantic send: max 1.
- semantic retry/resend: 0.
- direct provider/model probes: 0.
- manual Ticket/outbox/recovery/SQLite mutation: 0.
- Gateway restart/reload/repair: 0.
- plugin lifecycle mutation: 0.
- installer/install-over: 0.
- lifecycle start/stop/restart: 0.
- provider/model config mutation by executor: 0.
- production source repair: 0.
- release/tag/main: 0.
- force push/history rewrite: 0.
- do not create/start CNX-421.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260918-420-operator-fresh-session-ollama-route-ticket-first-discrimination-report.md`

Include:

- authoritative starting/ending HEAD;
- Stage-1 health and durable baseline;
- exact nonce supplied to Operator;
- exact text of the Operator instruction checkpoint;
- evidence Hermes performed zero browser mutation;
- Operator confirmation `ส่งแล้ว`;
- fresh session key/ID;
- native transcript evidence;
- actual provider/model/API/runtime;
- UI-selected route as observational evidence only;
- Ticket/admission/run/model/delivery correlation;
- durable deltas;
- route classification;
- Ticket-first classification;
- combined final classification;
- semantic cardinality ledger;
- hard-fence ledger;
- evidence paths.

Closeout:

1. set ACTIVE.md and STATUS.md to `WAITING_FOR_CHATGPT_REVIEW`;
2. verify local HEAD == remote HEAD;
3. verify clean publication worktree;
4. stop;
5. do not create/start CNX-421.
