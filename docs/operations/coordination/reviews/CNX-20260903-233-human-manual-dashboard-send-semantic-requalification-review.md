# CNX-20260903-233 — Human-Manual Dashboard Send Semantic Requalification Review

Disposition: `ACCEPT_FAIL_DURABLE_SEMANTIC_TRACE__DASHBOARD_ORIGIN_ON_DISCORD_ASSOCIATED_SESSION_STAGING_SCOPE_DEFECT_PROVISIONALLY_PROVEN__TDD_REPAIR_REQUIRED`
Reviewer: ChatGPT independent coordination review
Date: 2026-09-03 ICT

## Scope

Review the Task-233 live Windows acceptance evidence after the user performed exactly one physical Dashboard `Send message` activation on the existing session:

`agent:main:discord:channel:1531199905673252946`

Task-233 is materially different from Tasks 231 and 232. The Task-233 submission entered OpenClaw/CogentNexus, produced a new Ticket/run/model lineage, and produced visible assistant content in the Dashboard. The failure is therefore inside the runtime durable-delivery contract, not at the UI-actuation boundary.

## Evidence reviewed

- Task-233 report:
  `docs/operations/coordination/reports/CNX-20260903-233-human-manual-dashboard-send-semantic-requalification.md`
- Task-233 activation authority:
  `7de9e248de86758f62340e456c2dd836ad9f5ab6`
- Task-233 report HEAD:
  `827577a053979517a46f419a6f63564bd7420570`
- accepted production repair authority:
  `9a8510f1317c8e53c01c233b080ec20357cd22df`
- accepted plugin payload fingerprint:
  `e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`
- Task-233 report-head Actions and failing Validate job logs
- exact accepted-source delivery implementation in:
  - `plugins/cogentnexus-openclaw/src/v090.ts`
  - `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`
  - `plugins/cogentnexus-openclaw/src/v092-durable-delivery-boundary.ts`
  - `plugins/cogentnexus-openclaw/src/v162-dashboard-transcript-authority.test.ts`

## Findings

### 1. The human Dashboard submission entered runtime exactly once

Task 233 proved the prior UI-tooling ambiguity is gone.

The one user action produced a new accepted Direct Ticket and correlated OpenClaw/model activity:

```text
Ticket: CNXT-57ab3fb4-930e-43a6-bd16-90f5b84620e3
run:    e225362a-8872-45f8-a914-c90d835880c0
owner:  agent:main:discord:channel:1531199905673252946
```

A logical assistant result was visible in the Dashboard. No second user Send, Enter fallback, Discord-origin test message, direct operator Discord/API Send, or recovery replay was performed.

Result: `PASS_SUBMISSION_PROVEN`.

### 2. Durable semantic delivery failed after model/result generation

The Ticket reached `response_ready`, but no attributable `cnx_assistant_delivery` `direct_result` row was committed and no delivery confirmation settled the Ticket.

The eventual failure event was:

`direct_redelivery_timeout`

with message:

`Direct response delivery was not confirmed before deadline`

The Ticket remained outside a successful durable settlement even though the native Dashboard displayed assistant content.

Visible UI output is not equivalent to durable CogentNexus delivery proof. Task 233 therefore correctly fails the durable semantic acceptance contract.

Result: `FAIL_DURABLE_SEMANTIC_TRACE` accepted as a real product/runtime acceptance failure.

### 3. Discord negative-control and exactly-once fences were preserved

No product/runtime Discord reply was attributed to the Dashboard-origin Task-233 turn, and direct operator Discord/API Sends remained zero.

No semantic resubmission was performed after the one human Dashboard Send.

Result: `PASS_FENCE_PRESERVATION`.

### 4. Post-failure runtime remained coherent

Task 233 preserved the managed runtime and reported healthy read-only post-state, including managed controller state, healthy Gateway/Ollama, Delivery READY with no pending `ticket_outbox`, Recovery READY, and SQLite integrity `ok`.

Historical Task-223 retained evidence remained unchanged.

This failure does not authorize manual DB repair, recovery replay, stale-evidence cleanup, lifecycle repair, reinstall, or a second semantic test.

Result: `PASS_FAIL_CLOSED_PRESERVATION`.

### 5. Accepted source contains a staging-scope mismatch matching the live failure

The accepted source defines Dashboard ownership narrowly:

```text
isDashboardSession(key) => /^agent:[^:]+:dashboard:/
```

In `v091-dashboard-verified-delivery.ts`:

1. `before_agent_finalize` explicitly recognizes both:
   - a `dashboardTicket(...)`, and
   - a `discordOwnerTicket(...)` whose session key is `agent:<agent>:discord:channel:<id>`;
2. a qualifying Discord-associated owner can therefore be stored in `nativeTranscriptCandidates`;
3. `before_message_write` then routes that candidate through `stageDashboardDirectResult(...)`;
4. `stageDashboardDirectResult(...)` immediately re-resolves the run through `dashboardTicket(...)`;
5. `dashboardTicket(...)` rejects the Task-233 owner because its key is Discord-associated rather than `agent:*:dashboard:*`;
6. no durable direct-result row/marker is therefore established by that path;
7. `v092-durable-delivery-boundary.ts` later observes `response_ready` without a durable result and fails closed through the direct-redelivery timeout path.

This source shape closely matches the Task-233 evidence: native Dashboard assistant content exists, but `cnx_assistant_delivery` does not.

Result: `SOURCE_STAGING_SCOPE_DEFECT_PROVISIONALLY_PROVEN`.

The word `provisionally` is intentional. The successor must correlate live delivery-observe telemetry for the exact Task-233 run and identify the trusted ingress-surface signal before changing production behavior.

### 6. The defect must not be repaired by broadening all Discord-associated sessions into Dashboard sessions

The owner session key is an ownership/routing identity, not a reliable ingress-surface discriminator.

The user's normal environment intentionally supports:

```text
Dashboard-origin turn on a Discord-associated session -> Dashboard result
Discord-origin turn on that same Discord channel       -> Discord result
```

Existing tests also preserve external-channel/Discord receipt-confirmed behavior.

Therefore these are forbidden repair strategies:

- changing `isDashboardSession()` to accept every Discord session key;
- assuming a Discord-associated owner implies Dashboard ingress;
- inferring ingress from presence/absence of `@Ce`;
- inferring ingress solely from prompt text, current browser URL, or session-key syntax.

The repair needs a trusted production ingress-surface/correlation signal, or must stop blocked if OpenClaw 2026.7.1-2 exposes no trustworthy discriminator at the required hook boundary.

Result: `CROSS_SURFACE_ROUTING_FENCE_REQUIRED`.

### 7. Existing regression coverage misses the real Task-233 topology

`v162-dashboard-transcript-authority.test.ts` proves the native transcript/durable marker contract only with a Dashboard-form session key such as:

`agent:main:dashboard:v162-native`

It does not exercise a Dashboard-origin turn that intentionally reuses:

`agent:main:discord:channel:<id>`

while preserving different semantics for a real Discord-origin turn on the same owner key.

Task 233 therefore identifies a missing production-shaped regression topology.

Result: `TEST_GAP_PROVEN`.

### 8. Task-233 report-head CI is mixed, but the failure is isolated from Task-233 docs-only drift

Task-233 report HEAD `827577a...` differs from activation HEAD only by the report file; no product/source/test/workflow file changed.

Report-head workflows:

- Windows Installer Pack Smoke — `SUCCESS`
- PS5.1 Acceptance Smoke — `SUCCESS`
- Validate `33706153188` — `FAILURE`

The Validate failure is isolated to `validate (windows-latest, 3.14)` during `npm test`:

```text
src/v093-response-ready-boundary.test.ts
never refreshes response_ready_at after a durable direct_result exists
Test timed out in 15000ms
```

That job still passed the Python suite (`506 passed, 3 skipped, 4 subtests passed`) and all other plugin files except the timed-out test. The same source tree passed the other OS/Python matrix jobs, including Windows/Python 3.11, and the two dedicated Windows workflows passed.

Because Task-233 report publication is docs-only, this is not evidence that the Task-233 report introduced source regression. It remains a CI timing anomaly that the successor must recheck/reproduce rather than silently dismiss.

Result: `CI_RECHECK_REQUIRED`, non-blocking for opening the bounded root-cause/TDD repair task.

## Independent disposition

`ACCEPT_FAIL_DURABLE_SEMANTIC_TRACE__DASHBOARD_ORIGIN_ON_DISCORD_ASSOCIATED_SESSION_STAGING_SCOPE_DEFECT_PROVISIONALLY_PROVEN__TDD_REPAIR_REQUIRED`

Task 233 is accepted as a genuine product/runtime acceptance failure at the durable Dashboard-result staging/settlement boundary.

The successor must:

1. perform read-only correlation of the exact Task-233 run;
2. identify a trusted ingress-surface discriminator available in the real OpenClaw 2026.7.1-2 contract;
3. create a production-shaped RED reproducing Dashboard-origin use of a Discord-associated session while protecting real Discord-origin behavior;
4. make the smallest production repair;
5. obtain targeted and full GREEN, including clean Actions;
6. stop before live install/retest.

No additional Dashboard/Discord semantic message is authorized by this review.
