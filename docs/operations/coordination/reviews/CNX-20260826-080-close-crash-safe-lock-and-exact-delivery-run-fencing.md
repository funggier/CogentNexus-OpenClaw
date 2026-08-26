# Review — CNX-20260826-080 Crash-Safe Lock Publication and Exact Delivery-Run Fencing

Decision: `ACCEPT`

Disposition: `ACCEPT_CRASH_SAFE_DELIVERY_FENCING_CLOSED`

Reviewed report HEAD: `1798bfd4bb2ef69fb579b151f5d0423f0fc196f8`

Execution HEAD: `a77fb2ea76d3e0a03f814da9f0f446dc9a60c534`

Implementation HEAD: `70d02e76233ca1084da445d488f88b628455f4aa`

## Publication fence

Independent comparison confirms:

- execution HEAD -> implementation HEAD is one source/test commit;
- implementation changes are limited to `delivery-continuity.ts/.test.ts` and `ticket-store.ts/.test.ts`;
- implementation HEAD -> report HEAD is one report-only commit;
- no installer, runtime, config, coordination, provider, model, AGENTS or live-state mutation is hidden in the implementation fence.

## Accepted Gate P — crash-safe canonical lock publication

The predecessor malformed-canonical crash window is closed.

The accepted design writes a complete `{pid, token, acquiredAt}` record to a unique same-directory temporary path and atomically publishes that complete record into the canonical lock path with a create-if-absent hard-link operation. The canonical path therefore does not become visible before complete owner metadata exists.

Independent source inspection confirms:

- `publishCompletionLock()` pre-writes the complete record;
- canonical publication uses `linkSync(temp, canonical)`;
- `EEXIST` cannot replace an existing lock;
- a complete lock owned by a demonstrably dead PID can be removed and acquisition retried once;
- a currently live PID remains non-stealable;
- release re-reads the canonical record and unlinks it only when both PID and unique owner token match the releaser.

The Windows/Node evidence reported both Node 22 and Node 24 lock suites green on the supported host.

A process death after canonical publication but before temporary-link cleanup could leave a unique orphan temporary hardlink. This does not occupy the canonical lock path, does not create ambiguous owner state, and does not block future acquisition. It is cleanup debt rather than a P0/P1 semantic-integrity blocker.

## Accepted Gate R — exact workflow run settlement

When a workflow settlement carries `runId`, production now requires authoritative `notice.deliveryRunId === runId` exactly.

Independent source/test inspection confirms:

- unbound supplied-run success and failure settlement return false;
- wrong run is rejected;
- owner mismatch remains rejected;
- a normal marker-driven path binds the exact owner/run before settlement;
- the stale rollback fixture was corrected to bind its legitimate run before terminal settlement;
- delivered state remains immutable and duplicate terminal settlement converges without re-opening the completion.

Omitted-run compatibility paths remain distinct from marker-driven run settlement and do not weaken the supplied-run fence.

## Accepted Gate T — exact Ticket outbox run settlement

The predecessor `(delivery_run_id IS NULL OR delivery_run_id=?)` behavior is removed from supplied-run terminal settlement.

Production now requires exact `delivery_run_id=?` whenever a run id is supplied. Independent tests cover:

- unbound supplied-run success rejected;
- unbound supplied-run failure rejected;
- same-run bind idempotent;
- different run cannot replace an existing binding;
- wrong run and wrong owner cannot settle;
- exact bound owner/run succeeds;
- duplicate terminal settlement is a no-op.

`bindOutboxRun()` also preserves existing bound-run ownership rather than overwriting a different run.

## Preserved semantic candidate evidence

Task 080 reran and preserved the accepted Task-078/079 candidate behavior:

- trusted-owner Ticket-first admission and one routed event;
- CLI/subagent negative admission security;
- delivery-marker owner/session fail-closed behavior;
- one Ticket/Host timeout recovery authority;
- direct model-call lease ordering/fencing;
- direct `accepted -> routed -> response_ready -> delivery_confirmed -> completed` lifecycle and duplicate convergence;
- workflow schedule-failure CAS, scheduling/binding/settlement serialization and retry convergence;
- provider readiness disposition `PROVIDER_READY_WITH_FRESH_OWNER_SESSION` from the already-consumed Task-078 probes.

No new semantic message or provider probe occurred in Task 080.

## Verification accepted

Reported deterministic verification is internally consistent with the implementation fence:

- Node 24.18.0 / npm 11.16.0: 49 files, 257 tests passed;
- Node 22.23.2 / npm 12.0.2: 49 files, 257 tests passed;
- plugin validation passed under both compatibility paths;
- Python full suite: 356 passed, 2 skipped, 4 subtests passed;
- Task-069–074 targeted installer/recovery suite: 52 passed;
- baseline consistency passed;
- `git diff --check` passed;
- implementation worktree clean before report publication.

## Successor authorization

The combined Task-078/079/080 production candidate is accepted for the next live gate at exact source commit:

`70d02e76233ca1084da445d488f88b628455f4aa`

The next task may perform exactly one supported install-over/source-live parity/health/no-flash acceptance on the existing MANAGED installation and may prepare/verify a fresh authenticated Dashboard/WebChat owner surface.

It must not send a real semantic owner message, reuse the Task-076 session/nonce, or consume the final semantic acceptance nonce. Final semantic acceptance remains a separate task after live parity is accepted.
