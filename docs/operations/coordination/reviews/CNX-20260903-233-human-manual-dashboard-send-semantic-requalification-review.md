# CNX-20260903-233 — Human-Manual Dashboard Send Semantic Requalification Review

Disposition: `ACCEPT_FAIL_DURABLE_SEMANTIC_TRACE__DASHBOARD_ORIGIN_ON_DISCORD_ASSOCIATED_SESSION_STAGING_SCOPE_DEFECT_PROVISIONALLY_PROVEN__TDD_REPAIR_REQUIRED`
Reviewer: ChatGPT independent coordination review
Date: 2026-09-03 ICT

## Scope

Review the Task-233 live Windows acceptance after the user performed exactly one physical Dashboard `Send message` action on:

`agent:main:discord:channel:1531199905673252946`

Unlike Tasks 231 and 232, Task 233 proves the semantic submission entered OpenClaw/CogentNexus. A new Ticket/run/model lineage was created and assistant content became visible in Dashboard. The failure is therefore inside durable result staging/settlement, not UI actuation.

## Exact authoritative lineage

Task-233 report HEAD:

`827577a053979517a46f419a6f63564bd7420570`

Exact live lineage from that report:

```text
Ticket: CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4
run:    e225013e-8d50-4479-b227-ca9a10b89a46
owner:  agent:main:discord:channel:1531199905673252946
prompt: ช่วยสรุปงานที่ฉันควรโฟกัสวันนี้จาก context ล่าสุด และบอกเหตุผลสั้น ๆ
```

The run recorded four internal Ollama `qwen3.5:9b` call records inside this one attributable run. Hermes performed no semantic, Ticket, model, delivery, or recovery retry.

## Findings

### 1. Submission and model execution are proven

The one human manual Dashboard Send produced one runtime-accepted Direct Ticket and one attributable OpenClaw run. The event sequence included accepted, routed, four started/ended Ollama call records, then `response_ready`.

Dashboard later displayed assistant content.

No second user Send, Enter fallback, automated Send, Discord-origin test message, direct operator Discord/API Send, or recovery replay occurred.

Result: `PASS_SUBMISSION_AND_MODEL_LINEAGE_PROVEN`.

### 2. Durable semantic delivery failed

For the exact Ticket:

```text
cnx_assistant_delivery rows: 0
ticket_outbox rows: 0
delivery_confirmed_at: null
failure_message: Direct response delivery was not confirmed before deadline
```

The durable sequence ended with `direct_redelivery_timeout` after `response_ready`.

UI-visible assistant content is presentation evidence, not a substitute for CogentNexus durable delivery proof.

Result: Task-233 primary disposition `FAIL_DURABLE_SEMANTIC_TRACE` is accepted as a real product/runtime acceptance failure.

### 3. Routing and mutation fences were preserved

Task 233 observed zero attributable Discord replies and zero direct operator Discord/API Sends. Semantic resubmissions, recovery replays, manual Ticket/outbox/recovery/SQLite writes, lifecycle mutations, process kills, provider/model substitutions, plugin/installer operations, and historical-evidence mutations were all zero.

Post-failure runtime remained managed and healthy: Gateway/Ollama healthy, Delivery READY with pending 0, Recovery READY, SQLite integrity `ok`.

Result: `PASS_FAIL_CLOSED_PRESERVATION`.

### 4. Accepted source contains a staging-scope mismatch matching the live failure

The accepted source defines Dashboard session ownership narrowly with:

```text
isDashboardSession(key) => /^agent:[^:]+:dashboard:/
```

In `v091-dashboard-verified-delivery.ts`:

1. `before_agent_finalize` can recognize either `dashboardTicket(...)` or a Discord-associated owner through `discordOwnerTicket(...)`;
2. a Discord-associated owner can therefore become a `nativeTranscriptCandidates` entry;
3. `before_message_write` later routes that candidate through `stageDashboardDirectResult(...)`;
4. `stageDashboardDirectResult(...)` re-resolves through `dashboardTicket(...)`;
5. `dashboardTicket(...)` rejects `agent:*:discord:channel:*` owners;
6. no durable `direct_result` row/marker is staged by that path;
7. `v092-durable-delivery-boundary.ts` later sees response-ready work without durable result confirmation and fails closed through the redelivery-timeout path.

That source shape closely matches Task 233: native Dashboard content exists while `cnx_assistant_delivery` does not.

Result: `SOURCE_STAGING_SCOPE_DEFECT_PROVISIONALLY_PROVEN`.

`Provisionally` is intentional. Task 234 must correlate retained delivery-observe telemetry for the **exact lineage above** and prove the trusted ingress-surface contract before production modification.

### 5. A naive session-key broadening is forbidden

The owner session key is ownership identity, not necessarily ingress surface.

The environment intentionally supports both:

```text
Dashboard-origin turn on a Discord-associated session -> Dashboard result
Discord-origin turn on that same Discord owner        -> Discord result
```

Therefore the repair must not:

- broaden `isDashboardSession()` to every Discord owner;
- assume Discord-associated owner means Dashboard ingress;
- infer ingress from `@Ce`, prompt text, browser URL, or session syntax alone;
- change the owner session key merely to force Dashboard staging.

A trustworthy OpenClaw ingress/correlation signal is required. If OpenClaw 2026.7.1-2 exposes none at the needed boundary, the successor must stop `BLOCKED_INGRESS_SURFACE_CONTRACT` rather than guess.

### 6. Regression coverage misses the production topology

Existing native Dashboard transcript tests use `agent:main:dashboard:*` owner keys. They do not cover Dashboard-origin input operating on a Discord-associated owner while preserving different semantics for a true Discord-origin turn on the same owner-key shape.

Task 233 therefore proves a production-shaped test gap.

Result: `TEST_GAP_PROVEN`.

### 7. Task-233 report-head CI is mixed and must be rechecked

Task-233 report publication is docs-only relative to its activation authority.

Report-head workflows:

- Windows Installer Pack Smoke — `SUCCESS`
- PS5.1 Acceptance Smoke — `SUCCESS`
- Validate `33706153188` — `FAILURE`

Validate failed only in `validate (windows-latest, 3.14)` at `npm test` because:

```text
src/v093-response-ready-boundary.test.ts
never refreshes response_ready_at after a durable direct_result exists
Test timed out in 15000ms
```

That job still passed Python (`506 passed, 3 skipped, 4 subtests passed`) and reported `1 failed / 279 passed` plugin tests. Other matrix jobs, including Windows/Python 3.11, passed; both dedicated Windows workflows passed.

This is not evidence that the docs-only report introduced source drift. It remains a timing anomaly that Task 234 must reproduce/recheck without blindly increasing timeouts or rerunning deterministic failures until green.

Result: `CI_RECHECK_REQUIRED`, non-blocking for opening the bounded root-cause/TDD repair.

## Independent disposition

`ACCEPT_FAIL_DURABLE_SEMANTIC_TRACE__DASHBOARD_ORIGIN_ON_DISCORD_ASSOCIATED_SESSION_STAGING_SCOPE_DEFECT_PROVISIONALLY_PROVEN__TDD_REPAIR_REQUIRED`

Task 234 must:

1. correlate the exact Task-233 Ticket/run above read-only;
2. identify a trusted Dashboard-vs-Discord ingress signal in OpenClaw 2026.7.1-2;
3. create a genuine production-shaped RED before production repair;
4. preserve actual Discord-origin delivery semantics on the same owner-key shape;
5. make the smallest repair and obtain targeted/full GREEN including Actions;
6. stop before live install or another semantic test.

No additional Dashboard/Discord semantic message is authorized by this review.
