# CNX-20260826-079 — Finish Workflow Delivery Atomicity

Result: `PASS_WORKFLOW_DELIVERY_ATOMICITY_CLOSED`

Executor: Hermes, after the operator's explicit instruction to continue Task 079

## Scope and hard fence

Task 079 was executed as a source/test-only repair in a fresh isolated worktree.
No OpenClaw semantic/user message, Dashboard/WebChat turn, `openclaw agent` semantic
run, direct Ollama probe, live Ticket/session/SQLite mutation, install/install-over,
uninstall/reset/cleanup, provider/model/config/plugin/AGENTS change, restart, reboot,
merge, tag, or release was performed.

The accepted live production source remains pre-Task-078 baseline
`79b51ed06363f6e8862c491ee0a313ddb412c806`. Task-078/079 source remains non-live.

## Heads and provenance

- Fresh execution HEAD: `3cc88370dafea1f06d39f0e1915c6e1b218bb0f7`.
- Target branch HEAD at preflight matched the remote branch.
- Isolated worktree branch: `hermes/task-079-atomicity`.
- Implementation commit 1: `3c5c637d7299435bd1fef614d399f9a7017cb358`.
- Implementation/test commit 2: `ef22d03ae2b2cc68da76640c2108944d01bc9524`.
- Final report-only commit follows these implementation commits.
- Task-078 report/review lineage and the Task-078 implementation were verified as
  ancestors before work began.
- No Task-079 report existed before execution.

## Gate F — stale scheduling-failure rollback

### RED

A real completion-file test created a pending revision, retained the scheduled claim,
settled the same completion through production settlement to `delivered`, and then
called `markWorkflowDeliveryScheduleFailed()` with the stale scheduled object.
The pre-fix implementation rewrote the file to pending and returned a notice, proving
the stale rollback defect.

### GREEN

`markWorkflowDeliveryScheduleFailed()` now uses the same completion lock/CAS protocol
as scheduling and settlement. It re-reads current disk state and requires exact match
of:

- task id;
- state revision;
- owner session;
- pending delivery status;
- delivery attempt count;
- scheduled timestamp;
- last-attempt timestamp;
- delivery run identity.

If any field changed, including a transition to `delivered`, it returns an explicit
no-op (`undefined`) and leaves the newer state untouched. A genuine schedule failure
still clears scheduling fields and returns the same revision to retryable pending.

The fixed test verifies `deliveredAt`, delivery status, attempt count, and terminal
error state remain unchanged after stale rollback.

## Gate B — atomic workflow bind/settle

### RED

A deterministic live-lock test placed a valid lock artifact for the completion path and
attempted workflow binding. The pre-fix unlocked `bindDeliveryRun()` ignored the lock
and wrote `deliveryRunId`, proving that bind was outside the serialized state protocol.

### GREEN

Workflow binding now executes under the shared completion lock, re-reads the completion
file, validates pending/task/revision/owner state, and rejects a different existing
`deliveryRunId`. Same-run rebind is idempotent. Settlement already uses the same lock
and now validates the run identity when one is present.

Coverage includes:

- bind after delivered returns false;
- same run can bind idempotently;
- different run cannot overwrite the first run;
- stale run cannot settle the completion;
- correct owner/run can settle normally;
- delivered state and `deliveredAt` remain immutable.

## Gate L — bounded abandoned-lock recovery

### RED

A completion `.lock` artifact with a dead PID and old acquisition timestamp suppressed
a legitimate retryable scheduling operation in the pre-fix implementation, proving that
an abandoned lock could block delivery indefinitely.

### GREEN design

The lock now contains a JSON owner record:

- current process PID;
- unique random owner token;
- acquisition timestamp.

Acquisition is exclusive with `openSync(..., "wx")`. If the path already exists:

1. valid metadata whose PID is alive is never stolen;
2. valid metadata whose PID is demonstrably dead may be removed once;
3. acquisition is retried once after bounded abandoned-lock recovery;
4. malformed/unverifiable lock metadata is not stolen fail-open;
5. release closes the descriptor and removes the lock only when PID and owner token
   still match the caller's lock.

This is conservative against PID reuse: a live PID is not treated as abandoned merely
because a caller wants progress. Terminal completion state is still protected by the
read/modify/write lock and atomic temporary-file rename.

The tests cover both a live same-process lock that blocks binding and a dead-PID lock
that is recovered and removed after successful scheduling.

## Gate C — repeated/concurrent scheduling convergence

The final workflow delivery suite proves:

- first eligible claim increments `deliveryAttempts` exactly once;
- immediate repeated scheduling does not claim again;
- a genuine scheduling failure clears only its own claim and leaves the revision
  retryable;
- one retry after rollback increments attempts exactly once;
- stale notice cannot claim a newer or terminal state;
- a different delivery run cannot replace an existing bound run;
- delivered state is not selected for rescheduling;
- normal bind/settle completes successfully.

All times are deterministic; no wall-clock sleep or live delivery was used.

## Task-078 preservation

Task-078 accepted behavior was preserved and rerun unchanged:

- owner/session-bound delivery marker fail-closed behavior;
- repeated Ticket admission/routing idempotency;
- one Ticket/Host timeout-recovery authority;
- direct model-call lease/Host ordering tests and downgraded L disposition;
- registered direct lifecycle through `accepted -> routed -> response_ready ->
  delivery_confirmed -> completed`;
- wrong-owner/forged marker, CLI, subagent and duplicate callback negative coverage;
- provider disposition `PROVIDER_READY_WITH_FRESH_OWNER_SESSION` from exactly two
  already-consumed Task-078 probes.

No new provider diagnostic was run in Task 079.

## RED/GREEN evidence

- Focused pre-fix RED run: 3 new tests failed, covering stale rollback, unlocked bind,
  and abandoned lock suppression; 7 existing tests passed.
- Focused GREEN run after production fixes: 53 tests passed, then 54 tests passed after
  the final run-identity convergence test was added.
- Final workflow/delivery suite: 12 tests passed.
- Final registered integration suite: 42 tests passed.
- TypeScript build: passed.

## Full verification

| Gate | Result |
|---|---|
| Node 24.18.0 / npm 11.16.0 `npm ci` + `npm test` | 49 files, 251 tests passed |
| Node 24/npm 11 `npm run plugin:validate` | PASS; TypeScript/schema/bootstrap/package checks passed |
| Node 22.23.2 / npm 12.0.2 `npm ci` + `npm test` | 49 files, 251 tests passed |
| Node 22/npm 12 `npm run plugin:validate` | PASS; 45 config properties, 5 tools, 176 packed files |
| Python full pytest | 356 passed, 2 skipped, 4 subtests passed |
| Task 069–074 targeted installer/recovery suites | 52 passed |
| `python scripts/check_baseline_consistency.py` | PASS (Bridge v0.9.3) |
| `git diff --check` | PASS |
| Final implementation worktree before report | clean |

The Python full-suite and targeted-suite runs were source regressions only; no live
installer/runtime paths were invoked.

## Live mutation accounting

- OpenClaw semantic/user messages: **0**.
- Dashboard/WebChat live turns: **0**.
- Direct Ollama probes: **0** (Task-078's two probes were preserved, not repeated).
- Live Ticket/session/SQLite writes: **0**.
- Provider/model/config/plugin/AGENTS changes: **0**.
- Install/install-over/uninstall/reset/cleanup: **0**.
- Gateway/Ollama/Supervisor restart or process termination: **0**.
- Reboot/merge/tag/release: **0**.
- Worktree-only `npm ci`, build, and test artifacts were confined to the temporary
  evidence worktree and are not live product mutations.

## Publication fence and successor

Implementation commits are `3c5c637d7299435bd1fef614d399f9a7017cb358` and
`ef22d03ae2b2cc68da76640c2108944d01bc9524`. This report is published separately under
the required reports path.

If independent review accepts `PASS_WORKFLOW_DELIVERY_ATOMICITY_CLOSED`, the next task
must be the supported install-over/source-live parity/health/no-flash gate using the
combined accepted Task-078/079 source. That gate may prepare a fresh authenticated
Dashboard/WebChat owner session but must not send the final semantic nonce. Only a
separate final semantic acceptance task may authorize one new real owner message.
