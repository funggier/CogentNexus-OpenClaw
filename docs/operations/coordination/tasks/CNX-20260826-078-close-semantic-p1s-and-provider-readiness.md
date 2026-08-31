# CNX-20260826-078 — Close Semantic P1s and Prove Provider Readiness

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_TDD_SEMANTIC_P1_REPAIR_AND_BOUNDED_PROVIDER_DIAGNOSTICS`

Current authorization: `SEMANTIC_P1_REPAIR_AND_PROVIDER_READINESS_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Close every currently known P0/P1 blocker in the CogentNexus/OpenClaw direct semantic path before authorizing another real user message.

This is intentionally a heavy source/test/diagnostic pass. Do not stop after the first GREEN fix. Work through the complete gate below, preserving least privilege and one durable recovery authority per semantic turn.

The intended final path remains:

`authenticated owner surface`
`-> before_agent_run`
`-> one durable Ticket + one routed event`
`-> provider may start only after durable admission`
`-> agent_end response_ready or one durable recovery authority`
`-> correctly owner-bound final delivery`
`-> one delivery_confirmed + one completed`

No real OpenClaw owner semantic message is authorized in Task 078.

## Accepted predecessor findings

Task 077 report HEAD:

`b252879bdbc8cba8f187f883f943d9a913199204`

Task 077 partial implementation/test HEAD:

`6867af2cad75cb4ee8e70206d70b0ba5bd5abeea`

Independent review:

Decision: `REWORK`

Disposition:

`REWORK_UNRESOLVED_SEMANTIC_P1S_AND_PROVIDER_READINESS`

Preserve these accepted findings:

1. `openclaw agent --session-key agent:main:main` is not owner-authenticated merely because it targets an owner-looking session key.
2. Do not broaden arbitrary CLI/channel/subagent admission.
3. Dashboard/WebChat control-UI is the next owner-surface candidate; exact OpenClaw `2026.7.1-2` metadata must remain the authority.
4. The canonical installed v0.9.3 plugin/source identity and dynamic hook registration were materially verified.
5. The Task-077 registered-hook positive owner and negative CLI/subagent tests are useful and must remain green.
6. The Task-076 nonce/run are retired and must never be reused.

Accepted live production source remains:

`79b51ed06363f6e8862c491ee0a313ddb412c806`

Task 078 source changes are not live until a later supported install-over gate.

## Absolute live fences

Do NOT in Task 078:

- send any OpenClaw user/owner semantic message;
- use Dashboard/WebChat to generate a new semantic turn;
- call `openclaw agent ...` as a semantic acceptance or provider test;
- reuse the Task-076 nonce;
- mutate live Ticket/session/SQLite data;
- install/install-over/uninstall/reset/cleanup;
- edit live OpenClaw/CogentNexus config;
- change configured provider/model;
- restart Gateway/Ollama/Supervisor merely to obtain a passing result;
- edit AGENTS/plugin registration;
- reboot, merge, tag or release;
- implement in the primary/live workspace.

Allowed live diagnostics are read-only except for the explicitly bounded direct-Ollama probes in Provider Gate P below. Those probes must not enter OpenClaw or CogentNexus, must not write product durable state, and must use an inert echo-style prompt.

All source/test work must use a fresh isolated worktree from the current coordination HEAD.

---

# Phase A — execution fence and exact source map

1. Fetch the current coordination branch and record exact execution HEAD.
2. Verify Task-077 review is an ancestor and Task 078 is ACTIVE.
3. Create a fresh isolated worktree/branch from execution HEAD.
4. Record clean `git status --short`.
5. Re-read:
   - Task 077 base task and comprehensive addendum;
   - final amended Task-077 report;
   - Task-077 review;
   - exact production files below.
6. Build a small source map before editing:
   - `plugins/cogentnexus-openclaw/src/index.ts`
   - `plugins/cogentnexus-openclaw/src/ticket-store.ts`
   - `plugins/cogentnexus-openclaw/src/delivery-continuity.ts`
   - `plugins/cogentnexus-openclaw/src/v091-direct-model-call-lease.ts`
   - relevant direct-delivery/recovery tests.

No implementation edit before focused RED reproduction for each defect.

---

# Gate M — delivery marker must be owner/session bound and fail closed

## M1 — RED: wrong-session ticket marker

Create a production-facing registered-hook test with isolated SQLite:

1. create Ticket A owned by `agent:main:dashboard:owner-a` and a pending terminal outbox row using normal TicketStore transitions;
2. generate its real `ticketDeliveryMarker(outboxId)`;
3. invoke registered `before_agent_run` with that marker from `agent:main:dashboard:owner-b`;
4. prove current source can bind or otherwise passes the marker without validating owner session;
5. prove no state belonging to owner A may be bound/settled by owner B in the fixed behavior.

Expected fixed behavior: the hook must fail closed for an invalid/wrong-owner internal marker. It must not treat it as ordinary inference and must not bind a delivery run.

## M2 — RED: forged/stale marker bypass

Test at least:

- nonexistent ticket outbox id;
- already-delivered ticket outbox id;
- workflow marker whose `completion.json.ownerSessionKey` differs from current `ctx.sessionKey`;
- workflow marker whose task/revision is stale.

A parsed but unbindable marker must not silently return ordinary `pass` into model inference.

## M3 — GREEN: least-privilege binding

Implement the smallest safe contract. Preferred shape:

- ticket outbox binding accepts an expected owner session and updates only when `outbox_id`, `delivery_status='pending'`, and `owner_session_key` all match;
- workflow binding verifies `completion.json.ownerSessionKey === current sessionKey` in addition to task/revision/status;
- `before_agent_run` passes the current session identity into binding;
- valid internally scheduled marker for its true owner still passes and binds;
- invalid/forged/wrong-owner marker returns `outcome='block'` with a bounded internal-delivery-integrity reason/category rather than proceeding to inference.

Do not grant owner authority from marker text itself.

## M4 — settle fence

Where practical, carry the expected owner/session identity through settlement too so a stale in-memory target cannot later settle a different owner's delivery after session succession. Preserve legitimate `rebindSessionOwner()` behavior by using the current authoritative owner stored in durable state.

---

# Gate R — repeated admission must be fully idempotent

## R1 — RED: repeated registered hook same run

Using the real registered `before_agent_run` handler:

1. same owner session;
2. same `runId`;
3. same direct prompt;
4. invoke hook twice.

Prove current behavior yields one Ticket but duplicate `routed` events.

## R2 — GREEN: exactly-once route transition

Make `TicketStore.route()` idempotent without losing the first direct-lane `routed` event even though `workflow_eligible=0` is the schema default.

Required semantics:

- first route call writes exactly one `routed` event;
- repeated route with same desired lane returns an idempotent/no-op result and writes no event;
- an attempted conflicting reroute after a route already exists must fail closed or return an explicit conflict, not silently rewrite durable intent;
- direct and durable lanes both work;
- repeated `before_agent_run` same run produces exactly one `accepted` and one `routed` event.

Use one SQLite transaction (`BEGIN IMMEDIATE`) for route-state/event decision.

Do not add duplicate Tickets merely to solve event idempotency.

---

# Gate T — one timeout/recovery authority for a Ticketed direct run

## T1 — RED: current `agent_end(timeout)` ordering

Create a registered-hook integration fixture that:

1. admits one direct Ticket;
2. drives a resumable timeout/error through `agent_end`;
3. records calls to `scheduleSessionTurn` and durable Ticket state/events;
4. demonstrates whether generic `cogent-resume-*` scheduling can occur before/alongside direct Ticket promotion.

The RED must represent actual current hook registration/order; do not test helper functions only.

## T2 — GREEN: Ticket/Host recovery wins

For a Ticketed direct run:

- finalize/classify durable Ticket recovery before deciding generic resume;
- if `finalizeDirectRun()` promotes the Ticket to durable `waiting`, do not schedule generic legacy `cogent-resume-*` for the same run;
- if Host direct-model recovery already owns the run (`recovering`), do not schedule generic resume and do not override Host classification;
- generic auto-resume remains available for resumable non-Ticket runs;
- internal delivery continuation failures retain their specialized delivery path rather than becoming fresh owner work.

Prove one semantic turn -> one recovery authority.

## T3 — no duplicate continuation after timeout

Assert after timeout fixture:

- one Ticket identity;
- no fresh owner Ticket from internal recovery prompt;
- at most one scheduled continuation authority appropriate to the state;
- no response/delivery `completed` event is fabricated;
- later dispatcher/recovery can observe the promoted Ticket deterministically.

---

# Gate L — direct model-call lease/Host classification ordering

This finding is a hypothesis until executable ordering proves a failure. Do not force a patch merely because Task 077 named it P1.

## L1 — deterministic ordering matrix

Build tests for at least:

1. `model_call_started -> Host claims recovering -> failing agent_end`;
2. `model_call_started -> failing agent_end -> Host expiry/claim attempt`;
3. `model_call_started -> model_call_ended -> agent_end`;
4. successful `agent_end` racing with Host claim;
5. active lease + Ticket timeout promotion from Gate T.

For each record final:

- `cnx_direct_model_call.state/outcome`;
- Ticket status/lane;
- recovery events;
- scheduled resume calls;
- whether Host or Gateway is the authoritative classifier.

## L2 — disposition

If all interleavings are already safe because SQLite fencing and existing Host fences produce one authority, explicitly downgrade the candidate and add tests only.

If RED exposes an unsafe interleaving, implement the smallest explicit state transition. Requirements:

- an `agent_end` fallback must never close/erase a lease already owned by Host recovery;
- Host must never regenerate model work after a successful response-ready result;
- Gateway timeout classification must not strand an active lease that later spawns a second recovery;
- lease closure/classification must be explainable from durable state after crash/restart.

Avoid a broad lease-state redesign.

---

# Gate W — workflow completion scheduling must not resurrect delivered state

## W1 — RED: stale notice

Create a deterministic test:

1. read pending completion notice A;
2. settle the same completion to `delivered` using production delivery code;
3. call `deliverWorkflowCompletion()` or the scheduling primitive with stale notice A;
4. prove current code can rewrite delivery state to `pending`.

## W2 — RED: concurrent/repeated scheduling

Drive two scheduling attempts for the same task/revision and prove only one claim may advance attempts/scheduling identity. Include retry-after semantics.

## W3 — GREEN: bounded atomic claim/CAS

Implement the smallest concurrency-safe mechanism consistent with the current file-backed workflow completion design.

Requirements:

- never rewrite `delivered` to `pending`;
- scheduling claim validates the current on-disk task id, state revision, owner, pending status and expected retry state;
- duplicate/concurrent callers converge;
- delivery attempt count increments once per successful scheduling claim;
- failed scheduling returns the same notice to pending without overwriting a newer terminal result;
- settlement cannot be performed by a stale/non-owning delivery run when a run identity is present;
- existing retry-after behavior remains intact.

A small lock/CAS helper is acceptable if local and bounded. Do not move workflow delivery into a new database subsystem in this task.

---

# Gate D — coherent direct-lane lifecycle integration

After M/R/T/L/W are green, add one integrated source test using the registered production hooks and isolated durable state.

Required sequence for a successful trusted owner turn:

1. invoke `before_agent_run` with exact supported Dashboard/WebChat owner metadata;
2. assert one Ticket + one `accepted` + one direct `routed` event before provider stub is released;
3. release a fake provider boundary only after durable assertions pass;
4. invoke successful `agent_end` with visible assistant output;
5. assert exactly one `response_ready`, Ticket still awaiting confirmed delivery;
6. invoke the appropriate production delivery hook/dispatcher callback for the same owner/run;
7. assert exactly one `delivery_confirmed` and one `completed`;
8. invoke duplicate callbacks and prove no duplicate terminal events/side effects.

Negative matrix in the same suite:

- wrong owner session marker;
- untrusted CLI metadata;
- subagent metadata;
- internal continuation prompt;
- same owner/run `before_agent_run` twice;
- different run/session cannot complete another Ticket.

The provider must be a fake/stub in this source integration test; no Ollama call.

---

# Provider Gate P — prove next-run readiness without OpenClaw semantic mutation

Task 076 provider failure remains a real P1 acceptance risk. Resolve it now as far as possible without sending another OpenClaw user message.

## P1 — exact OpenClaw 2026.7.1-2 timeout source

Read the installed exact dist/package and record concrete functions/values for:

- default LLM idle timeout;
- provider/model `requestTimeoutMs` derivation;
- Ollama stream/fetch timeout precedence;
- static-catalog vs explicit provider-model resolution;
- run/agent timeout ceilings;
- `diagnostics.stuckSessionAbortMs` or equivalent stuck-run abort;
- retry count/behavior after first idle timeout.

Do not trust current documentation over installed source.

Cross-check the local findings against known upstream issue classes where useful, especially local-Ollama 120-second idle timeout and static-catalog timeout propagation, but local `2026.7.1-2` source is authoritative for this task.

## P2 — exact current read-only config

Record effective relevant settings without exposing secrets in the report:

- selected provider/model;
- provider timeout fields;
- whether `models.providers.ollama.models[]` explicitly contains `qwen3.5:9b` or resolution falls back to a static catalog;
- agent/default run timeout;
- diagnostics stuck-session threshold;
- Ollama keep-alive/runtime settings visible without mutation;
- model context window and configured `num_ctx`/equivalent.

Redact tokens/keys.

## P3 — Task-076 session pressure

Read-only inspect the failed session `f829224b-064f-4bb4-a845-2955be2a2c7f` / `agent:main:main` and record, where OpenClaw exposes them:

- transcript bytes/messages;
- context/token count;
- compaction count/state;
- system/tool prompt overhead where measurable;
- whether the old session was already near a context/latency threshold.

Determine whether reuse of this session materially contributed to no-token TTFT.

## P4 — bounded direct Ollama diagnostics — explicitly authorized

You may perform at most **two** direct local Ollama diagnostic requests to the already configured `qwen3.5:9b`, bypassing OpenClaw and CogentNexus entirely.

Rules:

- inert prompt such as `Reply only: CNX-PROVIDER-PROBE`;
- no tools/files/network requests;
- first request measures current/cold-ish state, second measures immediate warm state;
- use streaming if available to record time-to-first-token/chunk;
- record total duration, load duration, prompt-eval duration/count, eval duration/count when Ollama returns them;
- do not alter model/provider configuration;
- do not unload/load other models deliberately;
- no more than two probes.

This diagnostic is not semantic product acceptance and creates no CogentNexus Ticket.

## P5 — readiness disposition

Classify exactly one:

### `PROVIDER_READY_WITH_FRESH_OWNER_SESSION`

Use only if evidence shows the model itself produces a first token comfortably inside the effective OpenClaw watchdog and Task-076 likely suffered from session/context pressure or a surface-specific path avoidable by a fresh Dashboard session.

### `PROVIDER_READY_AFTER_SUPPORTED_CONFIG_REMEDY`

Use only if exact OpenClaw source proves a supported configuration shape can carry a sufficient request/idle timeout in this build. State the exact minimal future live config change; do not apply it in Task 078.

### `PROVIDER_NOT_READY_OPENCLAW_2026_7_1_LIMITATION`

Use if exact source/diagnostics show the current OpenClaw/Ollama path cannot reliably produce the next acceptance inside its effective watchdog without a code/version/config change not yet authorized live.

### `PROVIDER_READINESS_UNPROVEN`

Use if evidence remains ambiguous.

No final semantic live task may be opened while readiness is `NOT_READY` or `UNPROVEN`.

---

# Full verification

After all source fixes/tests:

1. all new focused RED/GREEN tests;
2. complete plugin `npm test`;
3. `npm run plugin:validate`;
4. npm 11 / Node 24 compatible `npm ci`, test, validate;
5. npm 12 compatible path `npm ci`, test, validate;
6. package/tarball verification where existing project gates require it;
7. full Python `pytest tests/ -q` with zero failures;
8. Task-069 fresh transaction coverage;
9. Task-070/071 nonfresh mode isolation;
10. Task-073/074 recovery preflight/isolation;
11. baseline consistency;
12. `git diff --check`;
13. final diff review proving changes are limited to justified semantic-path source/tests;
14. isolated worktree clean after implementation commit(s).

If tests expose another P0/P1 in the same semantic path, investigate with the same root-cause + focused RED/GREEN discipline rather than deferring automatically. The operator explicitly authorized a heavy pass. Do not refactor unrelated installer/runtime code.

---

# Publication fence

1. Commit source/tests first.
2. Record implementation HEAD.
3. Verify execution HEAD -> implementation HEAD contains only Task-078 justified source/tests.
4. Add report in a **separate final report-only commit**:

`docs/operations/coordination/reports/CNX-20260826-078-close-semantic-p1s-and-provider-readiness.md`

Report must include:

- execution/implementation/report HEADs;
- RED/GREEN evidence for M/R/T/W and L if defect proven;
- explicit L disposition if tests show no production defect;
- exact successful direct lifecycle event sequence and duplicate counts;
- owner/session marker negative-security evidence;
- exact OpenClaw timeout/config/session findings;
- both allowed direct Ollama probe timings/results if used;
- Provider Gate P disposition;
- full verification counts;
- live mutation accounting;
- implementation -> report publication fence.

## Result tokens

Use exactly one:

- `PASS_SEMANTIC_P1S_REPAIRED_PROVIDER_READY`
- `PASS_SEMANTIC_P1S_REPAIRED_PROVIDER_CONFIG_REMEDY_REQUIRED`
- `BLOCKED_DELIVERY_OWNER_BINDING`
- `BLOCKED_ADMISSION_IDEMPOTENCY`
- `BLOCKED_RECOVERY_AUTHORITY`
- `BLOCKED_MODEL_CALL_LEASE_AUTHORITY`
- `BLOCKED_WORKFLOW_DELIVERY_IDEMPOTENCY`
- `BLOCKED_PROVIDER_READINESS`
- `BLOCKED_SECURITY_REGRESSION`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Successor logic

If independent review accepts `PASS_SEMANTIC_P1S_REPAIRED_PROVIDER_READY`, production source changed and therefore the next task must be a supported install-over/source-live parity/health/no-flash gate. It may also prepare the exact fresh Dashboard owner session for the subsequent semantic task, but must not consume the final semantic nonce unless separately authorized.

If independent review accepts `PASS_SEMANTIC_P1S_REPAIRED_PROVIDER_CONFIG_REMEDY_REQUIRED`, the next live task must combine the supported source install-over with the exact narrowly proven provider/config remedy, re-prove source/live/config/health/no-flash, then only afterward may a final semantic acceptance task be opened.

No new real semantic message is authorized by Task 078 itself.
