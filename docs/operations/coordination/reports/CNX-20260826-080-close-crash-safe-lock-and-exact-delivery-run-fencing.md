# CNX-20260826-080 — Close Crash-Safe Lock Publication and Exact Delivery-Run Fencing

Result: `PASS_CRASH_SAFE_DELIVERY_FENCING_CLOSED`

Executor: Hermes after explicit operator continuation

## Scope and hard live fence

Task 080 was executed as source/test-only work in a fresh isolated worktree from the
coordination branch HEAD. No OpenClaw semantic/user message, Dashboard/WebChat live
turn, CLI semantic test, direct Ollama probe, live Ticket/session/SQLite mutation,
install/install-over/uninstall/reset/cleanup, provider/model/config/plugin/AGENTS
change, restart/reboot, merge, tag, or release was performed.

Accepted live production remains Task-075 baseline:

`79b51ed06363f6e8862c491ee0a313ddb412c806`

The combined Task-078/079/080 candidate remains non-live pending the separately
authorized install-over/source-live parity/health/no-flash task.

## Provenance and heads

- Fresh execution HEAD: `a77fb2ea76d3e0a03f814da9f0f446dc9a60c534`.
- Remote branch matched this execution HEAD at preflight.
- Isolated worktree branch: `hermes/task-080-crash-safe-fencing`.
- Task-079 report and REWORK review were verified as ancestors.
- Task-080 implementation commit: `70d02e76233ca1084da445d488f88b628455f4aa`.
- Final report-only commit follows this implementation commit.
- Final implementation worktree was clean before report publication.

## Gate P — crash-safe canonical lock publication

### P1 RED/root-cause proof

The predecessor production sequence used `openSync(canonicalLock, "wx")` and then
wrote owner metadata separately. The deterministic lower-level proof reproduced the
acquisition boundary: the canonical `.lock` path became visible while its contents
were empty, exactly the state a process death between create and metadata write would
leave. That malformed canonical artifact cannot be classified by the predecessor
`readCompletionLock()` and suppresses subsequent acquisition.

The focused Task-080 suite also exercised the real lock API path and retained the
predecessor live-lock and dead-owner tests. The two other focused RED tests exposed the
independent workflow and Ticket unbound-settlement defects against the predecessor
source.

### P2 GREEN design

The implementation adds `publishCompletionLock()` and changes the production lock
path to:

1. construct a complete owner record containing `pid`, a random unique `token`, and
   `acquiredAt`;
2. write that complete record to a unique same-directory temporary path;
3. atomically publish it into the canonical path with `linkSync(temp, canonical)`;
4. remove the temporary link after successful publication or in a `finally` block.

`linkSync` is atomic create-if-absent on the supported Windows same-filesystem path
used by the evidence worktree. A second publisher receives `EEXIST` and cannot replace
the canonical record. A failure before publication leaves no canonical lock and no
temporary record. A failure after publication leaves the complete parseable owner
record visible.

The lock acquisition loop retains bounded recovery from a complete lock whose PID is
demonstrably dead. A valid live PID is never stolen. Invalid/unverifiable metadata is
fail-closed rather than guessed as abandoned, preserving PID-reuse safety. Release
removes a lock only when the current canonical record still has the caller's exact PID
and token.

### P3 evidence

Focused tests prove:

- publication interruption before canonical link leaves both canonical and temp paths
  absent;
- successful publication is parseable with complete PID/token/acquisition metadata;
- metadata is complete while the critical section is visible;
- a live lock is not stolen;
- a complete dead-PID lock is recovered once and progress resumes;
- a replacement lock with a different token is not removed by the original releaser;
- delivered terminal state remains immutable across stale scheduling/lock behavior.

The atomic publication primitive and lock behavior were executed on the Windows Hermes
host under Node 22/24. Both Node runs passed the complete lock suite.

## Gate R — exact workflow delivery-run settlement

### R1 RED

A real completion file was created with a retryable pending workflow state. Without
calling `bindDeliveryRun()`, settlement was attempted with `runId="unbound-run"` and
correct owner metadata. The predecessor returned `true` and allowed terminal
settlement, proving that a supplied run identity did not require a durable binding.
The stale-rollback predecessor test was corrected so its legitimate success path binds
`run-new` before settling.

### R2 GREEN

When `runId` is supplied, workflow settlement now requires
`notice.deliveryRunId === runId` exactly. A missing binding is not ownership; a
 different run, wrong owner, stale notice, or terminal state is rejected. Same-run
settlement remains idempotent and cannot resurrect delivered state. Existing explicit
no-run compatibility/admin call sites remain separate behavior because they do not
supply a marker delivery run identity.

Coverage includes unbound success/failure, wrong run, wrong owner, exact bound run,
same-run duplicate, stale rollback, and delivered-state immutability.

## Gate T — exact Ticket outbox delivery-run settlement

### T1 call-site audit

Production and test call sites were enumerated for `bindOutboxRun()`,
`markOutboxDelivered()`, `markOutboxFailed()`, and the Ticket branch of
`settleDeliveryTarget()`. Marker-driven paths pass a delivery run identity through the
bind and settlement predicates. Existing omitted-run calls are explicit compatibility
paths and were preserved.

### T2 RED

Two normal terminal Ticket outboxes were created through the production worker path
(`claim -> complete`) with `delivery_run_id = NULL`. Supplied-run success and supplied-
run failure settlement both exposed the predecessor SQL condition
`delivery_run_id IS NULL OR delivery_run_id=?`, proving that NULL was incorrectly
accepted as ownership.

### T3 GREEN

Ticket settlement now adds an exact `delivery_run_id=?` predicate whenever a run id is
supplied. NULL is no longer accepted. Owner-session predicates remain enforced. Ticket
binding also refuses to replace a different existing run while allowing same-run
idempotent bind.

The final Ticket matrix proves:

- unbound supplied-run success is rejected and leaves pending/null/unmodified;
- unbound supplied-run failure is rejected and leaves pending/null/unmodified;
- same-run bind is idempotent;
- different bound run cannot replace the first run;
- wrong run and wrong owner cannot settle;
- exact bound owner/run can settle;
- duplicate terminal settlement is a no-op.

## Gate I — integrated durable delivery invariant

The registered direct/workflow tests preserve the durable sequence:

`trusted owner -> Ticket accepted/routed -> response_ready -> delivery marker scheduled -> exact owner/run bind -> exact bound settlement -> delivery_confirmed/completed`

Workflow coverage preserves:

`pending -> one scheduling claim -> exact owner/run bind -> delivered`

and:

`pending -> one claim -> genuine same-claim schedule failure -> retryable pending`

The negative matrix includes unbound settlement, wrong run, wrong owner, stale notice,
live lock contention, dead-owner lock recovery, duplicate same-run callbacks, and
terminal-state non-resurrection. No provider call is used by these tests.

## Accepted predecessor behavior preserved

Task-078/079 candidate behavior was rerun and preserved:

- owner/session-bound delivery-marker fail-closed behavior;
- repeated Ticket admission/routing idempotency;
- one Ticket/Host timeout recovery authority;
- direct model-call lease/Host ordering;
- registered direct lifecycle and duplicate callback convergence;
- stale schedule-failure rollback CAS;
- workflow scheduling/binding/settlement serialization;
- repeated scheduling/retry convergence;
- valid dead-PID recovery and live-PID non-steal behavior;
- owner/CLI/subagent negative security behavior;
- provider disposition `PROVIDER_READY_WITH_FRESH_OWNER_SESSION` from exactly the two
  already-consumed Task-078 probes.

No Task-078 Ollama probe was repeated.

## RED/GREEN evidence

- Pre-fix focused run: 2 production defects failed — unbound workflow settlement and
  unbound Ticket settlement — while predecessor coverage passed. The lock boundary was
  independently reproduced at the lower-level canonical-create sequence.
- Focused GREEN run after implementation: 71 tests passed, then 70/71-count changes
  were rerun after the final P3/T3 additions; final focused source suites passed.
- Final focused source suites: 3 files, 71 tests passed.
- TypeScript build: passed.

## Full verification

| Gate | Result |
|---|---|
| Node 24.18.0 / npm 11.16.0 `npm ci` + `npm test` | 49 files, 257 tests passed |
| Node 24/npm 11 `npm run plugin:validate` | PASS; schema/bootstrap/package checks passed |
| Node 22.23.2 / npm 12.0.2 `npm ci` + `npm test` | 49 files, 257 tests passed |
| Node 22/npm 12 `npm run plugin:validate` | PASS; 45 config properties, 5 tools, 176 packed files |
| Python full pytest | 356 passed, 2 skipped, 4 subtests passed |
| Task 069–074 targeted installer/recovery suites | 52 passed |
| `python scripts/check_baseline_consistency.py` | PASS (Bridge v0.9.3) |
| `git diff --check` | PASS |
| Final implementation diff | 4 justified delivery-fencing files only |
| Final implementation worktree | clean before report publication |

## Live mutation accounting

- OpenClaw semantic/user messages: **0**.
- Dashboard/WebChat live turns: **0**.
- CLI semantic tests: **0**.
- Direct Ollama probes: **0**.
- Live Ticket/session/SQLite writes: **0**.
- Provider/model/config/plugin/AGENTS changes: **0**.
- Install/install-over/uninstall/reset/cleanup: **0**.
- Gateway/Ollama/Supervisor restart or process termination: **0**.
- Reboot/merge/tag/release: **0**.
- Temporary worktree `npm ci`, build and tests were isolated evidence activity only.

## Publication fence and successor

Source/tests were committed before report publication. The report is published as a
separate report-only commit under:

`docs/operations/coordination/reports/CNX-20260826-080-close-crash-safe-lock-and-exact-delivery-run-fencing.md`

If independent review accepts `PASS_CRASH_SAFE_DELIVERY_FENCING_CLOSED`, the next task
is the supported install-over/source-live parity/health/no-flash gate using the combined
Task-078/079/080 candidate. That task may prepare and verify a fresh authenticated
Dashboard/WebChat owner session, but it must not send the final semantic acceptance
message or consume its nonce. Only a later final semantic task may authorize exactly
one new owner message.
