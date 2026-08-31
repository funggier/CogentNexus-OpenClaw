# CNX-20260826-079 — Finish Workflow Delivery Atomicity

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_TDD_WORKFLOW_DELIVERY_ATOMICITY_REPAIR`

Current authorization: `WORKFLOW_DELIVERY_ATOMICITY_REPAIR_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Finish the one remaining independently confirmed Gate-W defect from Task 078 without repeating already accepted semantic/provider work.

The invariant is:

`pending completion -> one scheduling claim -> one owner-bound delivery run -> delivered`

or, on a genuine scheduling/delivery failure:

`pending completion -> retryable pending`

At no time may stale/concurrent state resurrect `delivered` back to `pending`, bind a stale/non-owning run over a newer state, or leave an abandoned lock that blocks future delivery forever.

## Accepted predecessor evidence — preserve, do not redo

Task 078 report HEAD:

`b934eea6a9df91e1aa6602730c00c66d995ff62e`

Task 078 implementation HEAD:

`e25fbd5ab0c2773ee65d98782ecba942cbe36d58`

Independent review:

Decision: `REWORK`

Disposition:

`REWORK_WORKFLOW_DELIVERY_ATOMICITY_INCOMPLETE`

Preserve these accepted Task-078 results:

1. delivery-marker fail-closed behavior and owner/run fencing on the production hook path;
2. repeated owner admission/routing idempotency;
3. one Ticket/Host timeout-recovery authority for Ticketed direct runs;
4. direct model-call lease/Host ordering tests and no-production-fix disposition;
5. registered direct lifecycle coverage through `accepted -> routed -> response_ready -> delivery_confirmed -> completed`;
6. owner/CLI/subagent negative security coverage;
7. full npm/Python/baseline regression evidence;
8. provider readiness disposition `PROVIDER_READY_WITH_FRESH_OWNER_SESSION` from exactly two already-consumed direct Ollama probes.

Do NOT run further direct Ollama probes unless a new provider regression is independently discovered; none are authorized by Task 079.

Accepted live production remains the pre-078 source:

`79b51ed06363f6e8862c491ee0a313ddb412c806`

Task-078/079 source remains non-live until a later supported install-over gate.

## Absolute live fence

Task 079 is source/test only.

Do NOT:

- send any OpenClaw semantic/user message;
- use Dashboard/WebChat for a live turn;
- call `openclaw agent` for semantic/provider testing;
- call Ollama directly;
- mutate live Ticket/session/SQLite state;
- install/install-over/uninstall/reset/cleanup;
- change provider/model/config/plugin/AGENTS;
- restart Gateway/Ollama/Supervisor merely for testing;
- reboot;
- merge/tag/release;
- edit in the primary/live workspace.

Use a fresh isolated worktree from the current coordination HEAD.

---

# Phase A — execution and source fence

1. Fetch the current coordination branch.
2. Verify the Task-078 report and independent REWORK review are ancestors.
3. Create a fresh isolated worktree/branch from the exact execution HEAD.
4. Record worktree path, branch and clean `git status --short`.
5. Inspect at minimum:
   - `plugins/cogentnexus-openclaw/src/delivery-continuity.ts`
   - `plugins/cogentnexus-openclaw/src/delivery-continuity.test.ts`
   - `plugins/cogentnexus-openclaw/src/index.ts`
   - workflow completion delivery tests/callers.
6. Preserve `e25fbd5...` semantic source changes; do not revert or redesign unrelated direct/Ticket logic.

No production edit before RED reproduction.

---

# Gate F — scheduling-failure rollback must not overwrite newer terminal state

## F1 — RED stale rollback

Create a deterministic production-unit test using a real completion file:

1. create completion revision R owned by session A in `pending`;
2. call the real scheduling claim primitive and retain returned scheduled object S;
3. advance the authoritative file to `delivered` through the production settlement path;
4. invoke `markWorkflowDeliveryScheduleFailed(path, S, 'synthetic schedule error')`;
5. current pre-fix source must demonstrate the defect by rewriting the newer terminal state or otherwise failing the required invariant;
6. capture the RED failure before editing production.

Required fixed assertions:

- file remains `deliveryStatus='delivered'`;
- existing `deliveredAt` remains unchanged;
- delivery attempts are not decremented/replayed;
- stale error is not written over the delivered terminal record;
- function returns an explicit no-op/unchanged result that callers can tolerate.

## F2 — GREEN rollback CAS

Implement the smallest atomic rollback behavior:

- acquire the same completion-state atomic protocol used for scheduling/settlement;
- re-read current state inside the atomic section;
- only clear scheduling fields / record `lastDeliveryError` when current state still represents the exact scheduling claim being rolled back;
- compare task id, state revision, owner session, pending status and scheduling identity/attempt metadata sufficient to reject stale caller state;
- never rewrite `delivered` or a newer claim;
- keep the completion retryable after a genuine schedule failure.

Update `deliverWorkflowCompletion()` call-site behavior only as needed to consume the new explicit result safely.

---

# Gate B — workflow delivery-run binding must be atomic with settlement

## B1 — RED bind/settle interleaving

Create a deterministic test/harness that forces this sequence around the workflow completion file:

1. binder reads valid pending completion state for run A;
2. before binder writes `deliveryRunId`, another operation settles that same completion to `delivered`;
3. binder continues;
4. pre-fix behavior must demonstrate that an unlocked stale bind can overwrite the newer terminal file, or the test must otherwise prove the production primitive lacks a serialized transition.

Do not rely on sleep timing. Add a narrow test seam/helper only if necessary to make the interleaving deterministic; do not ship a general concurrency framework.

Fixed behavior must prove:

- bind and settlement serialize through one atomic protocol;
- a bind after delivered returns false/no-op;
- a stale binder cannot resurrect `pending` or alter `deliveredAt`;
- wrong owner, wrong task/revision or wrong run identity remains rejected;
- normal owner-bound pending -> bound run path still succeeds.

## B2 — GREEN atomic bind

Move workflow-target binding into the same bounded atomic state mechanism used by scheduling/settlement.

Within the atomic section, re-read and validate:

- current delivery status is `pending`;
- task id and state revision match;
- owner session matches the current delivery session;
- if a different `deliveryRunId` is already authoritative, reject rather than overwrite it;
- terminal state is immutable.

Do not weaken Ticket outbox owner/run fences.

---

# Gate L — lock/CAS mechanism must recover from process death

The current `.lock` implementation uses `openSync(path+'.lock','wx')` and deletes only in-process `finally`. A crash can leave the lock forever.

## L1 — RED abandoned lock

Create a deterministic test that places an abandoned/stale lock artifact representing a process that no longer owns the critical section, then attempts a legitimate retryable completion transition.

Current pre-fix behavior should prove the operation is permanently suppressed while the artifact remains.

The test must not kill the real test runner. Simulate abandonment using the chosen lock metadata/recovery contract.

## L2 — GREEN bounded abandonment recovery

Use the narrowest reliable design. Acceptable options include:

- a lock file containing a unique owner token + process id + acquisition timestamp, with bounded stale-owner recovery only when ownership is demonstrably dead/expired according to a conservative rule; or
- another local atomic/CAS primitive that removes the persistent orphan-lock failure mode.

Requirements:

1. a live/valid lock is never stolen merely because a second caller wants progress;
2. an abandoned lock cannot block completion forever;
3. breaking/recovering a stale lock is deterministic and testable;
4. lock release only removes the caller's own lock/token where applicable;
5. terminal `delivered` state remains immutable through recovery;
6. no broad database migration or controller redesign.

If Windows process-liveness is used, handle PID reuse conservatively; time alone must not create an unsafe split-brain lock while a demonstrably live owner may still be in the critical section.

---

# Gate C — repeated/concurrent workflow scheduling convergence

Strengthen tests beyond the stale-notice case.

Prove:

- first eligible scheduling claim increments `deliveryAttempts` exactly once;
- second immediate caller for the same revision cannot claim concurrently;
- after legitimate retry-after expiry, exactly one new claim may advance attempts;
- scheduling failure rollback makes the same authoritative revision retryable exactly once without touching newer/terminal state;
- delivered state is never selected by `pendingWorkflowCompletions()` or claim primitives;
- normal scheduling + binding + settlement still completes.

Use deterministic fake times; avoid wall-clock sleeps.

---

# Gate I — preserve Task-078 direct semantic integration

Rerun the Task-078 focused semantic suites unchanged and confirm no workflow-delivery atomicity change regresses:

- trusted owner registered hook;
- exactly one `accepted` / one `routed`;
- direct `response_ready`;
- owner-bound final `delivery_confirmed` / `completed`;
- duplicate callback convergence;
- wrong-owner/forged delivery marker fail-closed;
- timeout recovery authority;
- model-call lease ordering matrix.

No real provider call.

---

# Full verification

Required after GREEN fixes:

1. focused new F/B/L/C tests;
2. all workflow/delivery-continuity tests;
3. Task-078 semantic focused tests;
4. complete plugin `npm test` under Node 24/npm 11 compatibility path;
5. `npm run plugin:validate` under Node 24/npm 11;
6. complete plugin `npm test` under npm 12-compatible path;
7. `npm run plugin:validate` under npm 12 path;
8. full Python `pytest tests/ -q` with zero failures;
9. Task-069–074 targeted installer/recovery suites remain green;
10. `python scripts/check_baseline_consistency.py` PASS;
11. `git diff --check` PASS;
12. final source diff contains only justified workflow-delivery atomicity source/tests plus preserved Task-078 lineage;
13. isolated worktree clean after implementation commit.

No additional Ollama provider probe is required.

---

# Publication fence

1. Commit implementation/tests first.
2. Record implementation HEAD.
3. Verify execution HEAD -> implementation HEAD contains only Task-079 justified files.
4. Publish a separate final report-only commit:

`docs/operations/coordination/reports/CNX-20260826-079-finish-workflow-delivery-atomicity.md`

Report must include:

- execution/implementation/report HEADs;
- RED/GREEN evidence for F, B and L;
- concurrency/retry convergence evidence for C;
- exact chosen lock/CAS design and crash-recovery invariant;
- preserved Task-078 semantic/provider evidence statement;
- full verification counts;
- live mutation accounting (all zero);
- implementation -> report-only publication fence.

## Result tokens

Use exactly one:

- `PASS_WORKFLOW_DELIVERY_ATOMICITY_CLOSED`
- `BLOCKED_STALE_SCHEDULE_FAILURE_ROLLBACK`
- `BLOCKED_WORKFLOW_BIND_SETTLEMENT_RACE`
- `BLOCKED_ABANDONED_LOCK_RECOVERY`
- `BLOCKED_WORKFLOW_RETRY_CONVERGENCE`
- `BLOCKED_SECURITY_REGRESSION`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Successor logic

If independent review accepts `PASS_WORKFLOW_DELIVERY_ATOMICITY_CLOSED`, Task-078 provider readiness and all other accepted semantic P1 repairs become eligible as one combined source candidate.

The next task MUST be a supported install-over/source-live parity/health/no-flash gate using the accepted combined implementation source. It may prepare a fresh authenticated Dashboard/WebChat owner session but MUST NOT send the final semantic nonce yet.

Only after that live parity gate is independently accepted may a separate final semantic acceptance task authorize one new real Dashboard/WebChat owner message.
