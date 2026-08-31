# Review — CNX-20260826-079 Finish Workflow Delivery Atomicity

Decision: `REWORK`

Disposition: `REWORK_CRASH_SAFE_LOCK_PUBLICATION_AND_EXACT_RUN_FENCING`

Reviewed report HEAD: `a5228f65cf5da0b40831703d49e234ae585d5fde`

Execution HEAD: `3cc88370dafea1f06d39f0e1915c6e1b218bb0f7`

Implementation HEADs:

- `3c5c637d7299435bd1fef614d399f9a7017cb358`
- `ef22d03ae2b2cc68da76640c2108944d01bc9524`

## Accepted Task-079 work to preserve

The following work is materially correct and should not be redone unless a focused regression proves otherwise:

- `markWorkflowDeliveryScheduleFailed()` now re-reads authoritative state under the completion lock and rejects stale rollback over a newer delivered state.
- Workflow `bindDeliveryRun()` was moved under the same completion lock as scheduling and settlement.
- Same-run bind is idempotent and a different already-bound run is rejected.
- Repeated scheduling / rollback / retry convergence is improved and attempt increments are covered.
- A valid well-formed lock owned by a demonstrably dead PID can be recovered, while a live PID lock is not stolen.
- Task-078 semantic/security/provider evidence was preserved and no new semantic or provider probe was performed.
- Full npm 11/12, plugin validation, Python, targeted installer/recovery, baseline and diff gates were reported green.
- Publication lineage is clean: execution HEAD -> two implementation/test commits -> report-only commit. Task 079 changed only `delivery-continuity.ts` and its tests.

## Why Task 079 is still incomplete

Task 079's invariant is stronger than the reported GREEN suite: an abandoned lock must not be able to suppress workflow completion indefinitely, and settlement must be fenced to the exact durable delivery-run owner rather than merely relying on the in-memory caller path.

### 1. Canonical lock publication still has a process-death crash window

Current `withCompletionLock()` does:

1. `openSync(lockPath, "wx")`, which creates the canonical `.lock` file;
2. then `writeFileSync(fd, JSON.stringify({pid,token,acquiredAt}))`.

If the process terminates between those operations, or during the metadata write, the canonical lock can remain empty/partial/malformed.

`readCompletionLock()` returns `undefined` for that artifact. On every later acquisition, `withCompletionLock()` sees `!existing` and returns `undefined` without removing or repairing the canonical lock. Therefore a product-created crash artifact can permanently suppress later delivery.

This directly violates Task-079 Gate L requirement:

> an abandoned lock cannot block completion forever

The next source repair must remove the malformed canonical-lock publication window, preferably by preparing a complete owner record first and publishing it atomically with create-if-absent semantics, or an equivalently narrow design. A crash before publication must leave no canonical lock; a crash after publication must leave a complete recoverable owner record.

Do not solve this by stealing arbitrary malformed/live locks on time alone.

### 2. Workflow settlement currently accepts an unbound run

Current workflow settlement checks:

```ts
if (input.runId && notice.deliveryRunId && notice.deliveryRunId !== input.runId) return false;
```

If `input.runId` is supplied but `notice.deliveryRunId` is absent, settlement is allowed.

The Task-079 test `does not let stale schedule failure overwrite delivered state` explicitly calls settlement with `runId: "run-new"` before binding that run and expects success. This makes the primitive accept a run that never acquired durable delivery ownership.

For marker-driven production delivery, successful `before_agent_run` binding is supposed to establish the durable run identity first. The durable primitive should enforce that invariant too:

- when a run id is supplied for workflow settlement, authoritative `notice.deliveryRunId` must already equal that run id;
- an unbound run must not be able to settle;
- wrong owner/session must remain rejected;
- normal bind -> settle succeeds;
- duplicate same-run settlement converges without terminal duplication.

Do not rely solely on `deliveryTargets` / `runSessions` in-memory maps for correctness after crash/restart.

### 3. Ticket outbox settlement has the same nullable-run fence shape

Task-078 changed Ticket outbox settlement to use:

```sql
(delivery_run_id IS NULL OR delivery_run_id=?)
```

when a run id is supplied. This preserves an unbound-run settlement path analogous to the workflow issue.

The successor must inspect all current call sites and prove the intended contract. For marker-driven Ticket delivery, if a run id is supplied, settlement should require the exact previously bound `delivery_run_id`; NULL must not count as ownership. Preserve any legitimate non-run administrative API only if it is explicitly separate and executable-tested.

## PID reuse note

The existing valid-lock recovery is conservative: if the stored PID is alive, it does not steal the lock. Preserve that safety behavior. Do not introduce a time-only steal while a potentially live owner may still execute a stale write. The primary required repair is to ensure the product cannot create an unparsable canonical lock during acquisition.

## Required successor proof

Before install-over, add focused RED/GREEN coverage for:

1. crash-safe canonical lock publication with no empty/partial canonical lock window;
2. recoverable complete dead-owner lock after publication;
3. live valid lock remains non-stealable;
4. workflow settlement before bind is rejected;
5. workflow bind -> exact run settlement succeeds;
6. wrong/stale run settlement is rejected;
7. Ticket outbox settlement with supplied run id rejects NULL/different binding and accepts exact binding;
8. existing Task-078/079 semantic, recovery, delivery and full regression suites remain green.

No new semantic message, provider probe or live mutation is authorized by this review.

## Publication decision

Do not authorize supported install-over yet.

Open one narrow source-only successor using the accepted Task-078/079 implementation lineage. If that successor passes independent review, then proceed to the supported install-over/source-live parity/health/no-flash gate.