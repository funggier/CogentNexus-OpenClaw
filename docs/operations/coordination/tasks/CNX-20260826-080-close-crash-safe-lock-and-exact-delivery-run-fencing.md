# CNX-20260826-080 — Close Crash-Safe Lock Publication and Exact Delivery-Run Fencing

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_TDD_CRASH_SAFE_DELIVERY_FENCING`

Current authorization: `CRASH_SAFE_DELIVERY_FENCING_REPAIR_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Close the final two independently confirmed delivery-integrity gaps before any supported install-over:

1. completion-lock acquisition must not be able to leave a product-created empty/partial canonical lock that blocks workflow delivery indefinitely after process death; and
2. Ticket/workflow settlement with a run identity must require the exact durable run binding rather than treating an unbound delivery as owned.

Preserve all accepted Task-078/079 semantic, recovery, security and provider evidence.

The intended durable delivery transition is:

`pending -> scheduling claim -> exact owner/session + deliveryRunId bind -> exact bound run settlement -> delivered`

A process crash may delay this transition, but it must not create an unrecoverable product lock or permit an unbound/stale run to complete another durable delivery.

## Accepted predecessor lineage

Task 078 implementation:

`e25fbd5ab0c2773ee65d98782ecba942cbe36d58`

Task 079 implementation/test commits:

- `3c5c637d7299435bd1fef614d399f9a7017cb358`
- `ef22d03ae2b2cc68da76640c2108944d01bc9524`

Task 079 report HEAD:

`a5228f65cf5da0b40831703d49e234ae585d5fde`

Independent Task-079 review:

Decision: `REWORK`

Disposition:

`REWORK_CRASH_SAFE_LOCK_PUBLICATION_AND_EXACT_RUN_FENCING`

Preserve these accepted results:

- stale schedule-failure rollback CAS does not overwrite newer delivered state;
- workflow binding/scheduling/settlement are serialized under one completion-state mechanism;
- same-run bind is idempotent and different already-bound run is rejected;
- repeated scheduling / rollback / retry convergence is covered;
- valid dead-PID lock recovery and live-PID non-steal behavior are useful and must remain safe;
- Task-078 owner/session marker hardening, admission/routing idempotency, one timeout recovery authority, lease ordering, direct lifecycle integration and security tests remain accepted candidate behavior;
- provider readiness remains `PROVIDER_READY_WITH_FRESH_OWNER_SESSION`; the two Task-078 Ollama probes are already consumed and MUST NOT be repeated.

Accepted live production remains:

`79b51ed06363f6e8862c491ee0a313ddb412c806`

The Task-078/079/080 candidate is not live until a later supported install-over gate.

## Absolute live fence

Task 080 is source/test only.

Do NOT:

- send an OpenClaw semantic/user message;
- use Dashboard/WebChat for a live turn;
- call `openclaw agent` for semantic/provider testing;
- call Ollama directly;
- mutate live Ticket/session/SQLite state;
- install/install-over/uninstall/reset/cleanup;
- change provider/model/config/plugin/AGENTS;
- restart Gateway/Ollama/Supervisor for testing;
- reboot;
- merge/tag/release;
- edit in the primary/live workspace.

Use a fresh isolated worktree from the current coordination HEAD.

---

# Phase A — execution and source fence

1. Fetch the current coordination branch.
2. Verify Task-079 report and REWORK review are ancestors.
3. Create a fresh isolated worktree/branch from the exact coordination execution HEAD.
4. Record worktree path, branch, execution HEAD and clean `git status --short`.
5. Inspect at minimum:
   - `plugins/cogentnexus-openclaw/src/delivery-continuity.ts`
   - `plugins/cogentnexus-openclaw/src/delivery-continuity.test.ts`
   - `plugins/cogentnexus-openclaw/src/ticket-store.ts`
   - `plugins/cogentnexus-openclaw/src/ticket-store.test.ts`
   - `plugins/cogentnexus-openclaw/src/index.ts`
   - all current call sites of `bindDeliveryRun`, `settleDeliveryTarget`, `bindOutboxRun`, `markOutboxDelivered`, and `markOutboxFailed`.
6. Preserve `e25fbd5...`, `3c5c637...`, and `ef22d03...` behavior unless a focused Task-080 RED proves a necessary correction.

No production edit before focused RED evidence.

---

# Gate P — crash-safe canonical lock publication

## P1 — root-cause reproduction

Current acquisition creates the canonical `.lock` path with `openSync(..., "wx")` before owner JSON is durably complete.

Add a deterministic focused test/proof showing why a process death at this acquisition boundary can leave an unparsable canonical lock that later acquisitions cannot classify/recover.

Do not kill the actual test runner. Acceptable deterministic approaches include:

- a narrow acquisition test seam that interrupts between canonical creation and owner-record publication; or
- a lower-level lock-publication primitive whose pre-fix absence/behavior demonstrates that canonical visibility precedes complete metadata.

The proof must correspond to the real production sequence, not merely assert that arbitrary external malformed files exist.

## P2 — GREEN atomic publication design

Implement the narrowest local mechanism such that:

- a complete owner record exists before the canonical lock becomes visible;
- canonical publication is atomic create-if-absent;
- crash before publication leaves no canonical lock;
- crash after publication leaves a complete parseable owner record;
- a second caller cannot replace an existing canonical lock;
- release removes only the caller's exact token/owner lock;
- a valid live lock remains non-stealable;
- a complete valid lock whose owner PID is demonstrably dead remains recoverable;
- PID reuse remains conservative: do not steal merely because a timeout elapsed while the recorded PID is currently alive;
- no broad database/controller migration is introduced.

A pre-written unique owner record atomically published into the canonical path is preferred. For example, an atomic same-filesystem create-if-absent link/publish primitive is acceptable if verified on the supported Windows filesystem and by deterministic tests. An equivalent design is acceptable if it removes the malformed canonical publication window.

Do not rely on `openSync(canonical, 'wx')` followed by a separate metadata write as the final design.

## P3 — lock recovery tests

At minimum prove:

1. canonical lock observed inside the critical section contains complete parseable PID/token/acquisition metadata;
2. pre-publication interruption leaves no canonical lock and does not suppress the next acquisition;
3. a valid live lock is not stolen;
4. a valid complete dead-owner lock is recovered once and normal progress resumes;
5. release cannot delete a replacement lock with a different token;
6. delivered terminal state remains immutable across lock recovery.

If platform-specific filesystem behavior is relied upon, record exact Node/Windows behavior and keep a fail-closed fallback for unsupported semantics.

---

# Gate R — exact workflow delivery-run settlement

## R1 — RED unbound workflow run

Using a real completion file and production `settleDeliveryTarget()`:

1. create/claim a retryable pending workflow completion;
2. do NOT call `bindDeliveryRun()`;
3. call settlement with `runId='unbound-run'` and correct owner/session metadata;
4. prove current pre-fix source incorrectly permits terminal settlement while no durable `deliveryRunId` is bound.

Fixed result must be a no-op/false and completion must remain pending.

The existing Task-079 stale-rollback test that currently settles an unbound `run-new` must be corrected to bind the run before settlement.

## R2 — GREEN exact workflow fence

For marker-driven workflow settlement:

- when `runId` is supplied, authoritative `notice.deliveryRunId` must exist and equal it exactly;
- missing binding does not count as ownership;
- different run is rejected;
- owner session mismatch is rejected;
- exact owner + exact bound run succeeds;
- same-run duplicate/late settlement converges without terminal resurrection or duplicate durable effects.

If a legitimate non-run administrative settlement mode exists, keep it as an explicit separate contract; do not infer administrative authority merely from omitted metadata on a marker-driven path.

---

# Gate T — exact Ticket outbox delivery-run settlement

Task-078 Ticket outbox settlement currently accepts a supplied run id when `delivery_run_id IS NULL OR delivery_run_id=?`.

## T1 — inspect all call sites

Before editing, enumerate current production/test call sites for:

- `TicketStore.bindOutboxRun()`;
- `TicketStore.markOutboxDelivered()`;
- `TicketStore.markOutboxFailed()`;
- `settleDeliveryTarget()` ticket branch.

Classify which paths are marker-driven delivery-run settlement versus any explicit administrative/non-run operation.

## T2 — RED unbound Ticket run

Create a normal terminal Ticket/outbox owned by session A.

Without binding the outbox to a delivery run:

- attempt success settlement with `runId='unbound-ticket-run'` and owner A;
- attempt failure settlement with the same supplied run identity.

Current source should expose that NULL binding can satisfy the run fence.

Fixed behavior: supplied run identity requires exact prior durable binding; both operations return false/no-op while outbox remains pending/unmodified.

## T3 — GREEN exact Ticket run fence

For run-bound settlement:

- `delivery_run_id` must equal the supplied run id exactly;
- NULL is not exact ownership;
- owner session must match when supplied;
- wrong run or wrong owner cannot deliver/fail the outbox;
- bind exact owner/run -> settle succeeds;
- same terminal callback is idempotent and cannot duplicate delivery effects.

Preserve any intentional non-run administrative API only if it is explicit and covered separately. Do not weaken owner fencing.

---

# Gate I — integrated durable delivery invariant

Rerun/strengthen the registered direct and workflow delivery integration so the following is executable evidence:

`trusted owner -> Ticket accepted/routed -> response_ready -> delivery marker scheduled -> exact owner/run bind -> exact bound settlement -> delivery_confirmed/completed`

For workflow completion prove:

`pending -> one scheduling claim -> exact owner/run bind -> delivered`

and failure path:

`pending -> one claim -> genuine same-claim schedule failure -> retryable pending`

Negative matrix must include:

- unbound settlement;
- wrong run;
- wrong owner;
- stale notice;
- live lock contention;
- dead-owner lock recovery;
- duplicate same-run callbacks;
- delivered state cannot be resurrected.

No provider call is allowed in these tests.

---

# Full verification

After focused RED/GREEN tests, run all relevant gates:

1. delivery continuity focused tests;
2. TicketStore/outbox focused tests;
3. registered owner/admission/direct-lifecycle tests;
4. Task-078 timeout/recovery/lease/security tests;
5. complete plugin `npm test` under Node 24 / npm 11;
6. `npm run plugin:validate` under Node 24 / npm 11;
7. complete plugin `npm test` under the accepted npm 12 compatibility path;
8. `npm run plugin:validate` under that npm 12 path;
9. full Python `pytest tests/ -q` with zero failures;
10. Task-069 through Task-074 targeted installer/recovery suites;
11. `python scripts/check_baseline_consistency.py`;
12. `git diff --check`;
13. final diff review proving only justified delivery-fencing source/tests changed;
14. implementation worktree clean after implementation commit(s).

Do not repeat the two Task-078 Ollama probes.

If another P0/P1 is exposed inside this exact delivery-fencing path, diagnose and RED/GREEN it in Task 080 rather than silently deferring, unless safe source repair is impossible under the hard fence.

---

# Publication fence

1. Commit source/tests first.
2. Record exact implementation HEAD(s).
3. Verify execution HEAD -> implementation HEAD contains only Task-080 justified source/tests.
4. Publish the report in a separate report-only commit:

`docs/operations/coordination/reports/CNX-20260826-080-close-crash-safe-lock-and-exact-delivery-run-fencing.md`

The report must include:

- execution / implementation / report HEADs;
- P/R/T RED evidence against predecessor source;
- exact atomic lock publication design and supported Windows filesystem evidence;
- live/dead/replacement-token lock tests;
- workflow unbound/wrong/exact run tests;
- Ticket outbox unbound/wrong/exact run tests;
- integrated delivery sequence and duplicate counts;
- full npm/Python/baseline results;
- live mutation accounting;
- publication fence.

## Result tokens

Use exactly one:

- `PASS_CRASH_SAFE_DELIVERY_FENCING_CLOSED`
- `BLOCKED_LOCK_PUBLICATION_RECOVERY`
- `BLOCKED_WORKFLOW_RUN_FENCING`
- `BLOCKED_TICKET_RUN_FENCING`
- `BLOCKED_DELIVERY_SECURITY_REGRESSION`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Successor logic

If independent review accepts `PASS_CRASH_SAFE_DELIVERY_FENCING_CLOSED`, the combined accepted Task-078/079/080 source must next pass a supported install-over/source-live parity/health/no-flash gate.

That live parity task may prepare/verify a fresh authenticated Dashboard/WebChat owner session, but must not send the final semantic acceptance message or consume its nonce.

Only after install-over parity is accepted may a separate final semantic acceptance task authorize exactly one new owner message.