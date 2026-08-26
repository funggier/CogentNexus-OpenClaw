# Review — CNX-20260826-078 Close Semantic P1s and Provider Readiness

Decision: `REWORK`

Disposition: `REWORK_WORKFLOW_DELIVERY_ATOMICITY_INCOMPLETE`

Reviewed branch/report HEAD: `b934eea6a9df91e1aa6602730c00c66d995ff62e`
Execution HEAD: `9e66983d58a703ceb7ae9bfae29f82931f274737`
Implementation HEAD: `e25fbd5ab0c2773ee65d98782ecba942cbe36d58`
Report lineage after implementation: two report-only commits; current report content only, no hidden source change.

## Accepted Task-078 evidence to preserve

The following findings/repairs are independently accepted and MUST NOT be redone unless a new regression is demonstrated:

- Delivery-marker handling is now fail-closed at the registered `before_agent_run` boundary for invalid/unbindable markers and the production hook passes the current session identity into delivery binding.
- Ticket outbox binding/settlement gained owner-session and run fencing on the production path.
- `TicketStore.route()` now records exactly one initial `routed` event and treats repeated same-lane routing as an idempotent no-op; conflicting reroute is rejected.
- Ticketed direct timeout handling suppresses the legacy generic interrupted-resume path so Ticket/Host recovery is the single intended authority; generic auto-resume remains for non-Ticket runs.
- The direct model-call lease/Host race candidate was exercised through deterministic ordering tests. Current durable state fences cover the tested interleavings; no production lease patch was justified. Preserve those tests and the downgraded disposition unless a new RED is found.
- The registered direct lifecycle test materially covers trusted owner admission through `accepted -> routed -> response_ready -> delivery_confirmed -> completed`, with duplicate callback convergence and negative owner/CLI/subagent cases.
- Full npm 11/Node 24 and npm 12/Node 22 plugin tests/validation, Python suite, baseline checks and targeted installer/recovery suites were reported green.
- Provider diagnosis is accepted as `PROVIDER_READY_WITH_FRESH_OWNER_SESSION`: exactly two bounded direct-Ollama probes produced first stream chunks at approximately 7.7 s and 0.2 s, well inside the relevant 120 s/300 s first-event windows. No additional provider probe is required for the Gate-W rework.
- Task-076 `agent:main:main` remains retired as an acceptance surface. A fresh authenticated Dashboard/WebChat owner session remains the required future live surface.

## Publication fence

`9e66983... -> e25fbd5...` contains only justified semantic-path source/tests.

`e25fbd5... -> b934eea...` contains only the Task-078 report across two report-only commits.

No source mutation is hidden after the implementation commit.

## Blocking finding — workflow delivery atomicity remains incomplete

Task 078 Gate W explicitly required:

- never rewrite `delivered` to `pending`;
- duplicate/concurrent callers converge;
- failed scheduling must return the notice to retryable pending **without overwriting a newer terminal result**;
- settlement must not be performed by a stale/non-owning delivery run.

The implementation closes the original stale scheduling claim, but two production read-modify-write paths remain outside the atomic protection and the lock itself is not crash-recoverable.

### W-A — schedule-failure rollback can resurrect a newer delivered completion

`delivery-continuity.ts::markWorkflowDeliveryScheduleFailed(path, notice, error)` still builds a new object from the caller's stale `notice` and calls `writeCompletion()` directly. It does not acquire the completion lock and does not re-read/validate the current file.

`deliverWorkflowCompletion()` calls it from the `catch` path after a scheduling claim has already been made.

Therefore this deterministic interleaving is still possible:

1. caller A claims pending notice A and holds stale `scheduled` object;
2. another valid delivery path advances the authoritative completion file to `delivered`;
3. caller A later observes a scheduling error and calls `markWorkflowDeliveryScheduleFailed(path, scheduled, error)`;
4. the stale object is written back with `deliveryStatus='pending'`, resurrecting terminal delivery.

This violates Gate W verbatim.

### W-B — workflow delivery-run binding is still an unlocked read/write

`bindDeliveryRun()` uses owner/revision/status checks, but for workflow targets it performs `readCompletion(path)` followed by `writeCompletion(path, {...notice, deliveryRunId})` without `withCompletionLock()`.

A concurrent settlement can therefore advance the file after the bind-side read but before its write. The stale bind write can overwrite the newer terminal state. Owner checking does not solve this interleaving.

Workflow binding, scheduling claims, scheduling-failure rollback and settlement must participate in one coherent atomic state protocol.

### W-C — exclusive `.lock` can become a permanent delivery blocker after process death

`withCompletionLock()` creates `<completion>.lock` with `openSync(..., 'wx')` and deletes it only in a `finally` block in the same process. If the Node process exits/crashes after the lock is created and before cleanup, future callers simply return `undefined` forever because no bounded stale-lock recovery/lease mechanism exists.

For a crash-recovery product, replacing stale-state resurrection with a permanent orphan-lock blocker is not sufficient. Task 079 may retain a file lock only if it has deterministic bounded abandonment recovery, or may replace it with another local CAS/claim design that cannot permanently strand terminal delivery.

## Test gaps confirming the review finding

The new Gate-W tests cover:

- a stale notice attempting to reschedule after delivery;
- normal binding/settlement;
- wrong-owner Ticket binding.

They do not reproduce:

- schedule-failure rollback after a newer delivered state;
- workflow bind versus settlement interleaving;
- abandoned lock recovery.

These must receive focused RED tests before production edits.

## Review decision

Do not install `e25fbd5...` live yet and do not authorize a new semantic message.

Open a narrow source-only successor preserving all accepted Task-078 repairs/provider evidence and close Gate-W atomicity with strict RED/GREEN tests. After that source is independently accepted, proceed to the already-required supported install-over/source-live parity/health/no-flash gate before final semantic acceptance.
