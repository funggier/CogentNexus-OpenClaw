# CNX-20260904-241 — Independent Review

## Scope

Independent review of:

`docs/operations/coordination/reports/CNX-20260904-241-task240-exact-candidate-windows-install-over-requalification.md`

Report commit / reviewed HEAD:

`36490e1f70da7096054f96f33898a6d9577a9187`

Task authority immediately before execution:

`47aaf053b685ee9db82b3f8e121ce170dfb216db`

Exact candidate source:

`18a51b15768fb3d2196e65f1ef470c34aeef7f36`

Expected plugin fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

## Independent findings

### 1. Exact source binding was established

The report records a fresh detached checkout at the exact candidate SHA, clean worktree state, direct invocation path to that checkout's `scripts/install.ps1`, presence of the accepted Task-239 diagnostic repair and Task-240 portability test, and source plugin validation yielding the expected candidate fingerprint.

No later product/source/test/workflow drift was introduced by the Task-241 report commit. Fresh compare from `47aaf053...` to `36490e1...` contains only the Task-241 report file.

### 2. Preflight matched the preserved live boundary

The preflight remained:

```text
controller = passthrough
generation = 39
provider = ollama
candidate plugin not installed
Gateway/provider/model/storage/recovery/delivery = READY
SQLite integrity = ok
ticket_outbox = 0
```

The retained Task-237 backup token remained present and unchanged.

### 3. One-shot execution budget was respected

The report proves:

```text
Scheduled Task registrations = 1
Scheduled Task starts = 1
second start = 0
installer retry after start = 0
```

The retry gate closed immediately after the single start. This satisfies the Task-241 one-shot fence.

### 4. The terminal nonzero result is real, but its product meaning is not established

The disposable Scheduled Task transitioned from `Running` to `Ready` with:

```text
LastTaskResult = 1
```

However, the Task-241 runner result and installer transcript were absent from the dedicated evidence root. Read-only search found no new Task-241 transcript and the Task Scheduler operational-event query yielded no usable event artifact.

Therefore the available evidence does **not** prove any of the following:

- that the child installer process was actually invoked;
- the installer stage reached;
- a `plugin-rollover-prepare` or later failure;
- the Task-239 bounded child diagnostic;
- a new rollover ID / backup token / transaction;
- a precise product-side exception.

`LastTaskResult=1` alone cannot be promoted to `FAIL_INSTALLER_TERMINAL`, `FAIL_ROLLOVER_PREPARE`, or another product-specific failure classification.

### 5. Post-state stayed coherent and fail-closed

After the terminal task result:

```text
controller = passthrough
generation = 39
candidate plugin = not installed
Gateway/provider/model/storage/recovery/delivery = READY
pending outbox = 0
SQLite integrity = ok
```

No manual plugin, lifecycle, rollover, database, semantic, recovery, evidence-cleanup, release, tag, asset, or history mutation was performed.

### 6. This is an execution/evidence-channel boundary, not yet a product diagnosis

The important defect exposed by Task 241 is that the scheduled runner did not retain enough durable evidence to distinguish:

```text
scheduler/action launch failure
runner startup failure
runner pre-installer failure
child installer launch failure
actual installer/product failure
```

The runner passing a static PowerShell parser check is useful but does not establish successful Scheduled Task launch semantics, argument binding, working-directory behavior, output-path accessibility, or early-failure capture under the registered principal.

A materially different, side-effect-free forensic method is therefore required before another installer attempt is considered.

## CI state at review time

On report HEAD `36490e1f70da7096054f96f33898a6d9577a9187`:

```text
PS5.1 Acceptance Smoke 33836092345 = SUCCESS
Windows Installer Pack Smoke 33836092320 = SUCCESS
Validate 33836092302 = IN_PROGRESS at fresh review check
```

The reviewed report commit itself changes documentation only. The exact executable candidate `18a51b15768fb3d2196e65f1ef470c34aeef7f36` had already passed the required candidate validation gate under Task 240.

## Verdict

`ACCEPT_BLOCKED_EVIDENCE__ONE_SHOT_BUDGET_RESPECTED__PRODUCT_FAILURE_UNCLASSIFIED__RUNNER_EXECUTION_EVIDENCE_FORENSIC_REQUIRED`

Task-241 `BLOCKED_EVIDENCE` is accepted.

No installer retry is authorized from this review.

## Authorized successor direction

Open a separate read-only / harmless-canary forensic task whose purpose is to determine why the Task-241 Scheduled Task runner produced `LastTaskResult=1` without the required result/transcript artifacts.

The successor may:

- inspect the exact Task-241 Scheduled Task definition/action/principal/settings;
- inspect/hash the exact runner file used by Task 241;
- inspect path existence, quoting, environment, working-directory assumptions and filesystem permissions relevant to its evidence root;
- inspect available Task Scheduler operational/history channels read-only;
- execute PowerShell parser/static checks;
- use at most one **harmless canary Scheduled Task** that performs no installer/product/runtime/semantic action, solely to prove scheduler-to-runner invocation and durable artifact capture under an equivalent principal/action shape;
- use evidence-driven observer/tool retries that cannot produce product or semantic side effects.

The successor must not:

- start or invoke `scripts/install.ps1`;
- run rollover prepare/finalize;
- mutate plugin/controller/Gateway/lifecycle state;
- write Ticket/outbox/recovery/SQLite state;
- send Dashboard/Discord/API semantics;
- replay recovery;
- clean Task-237/Task-241 evidence;
- modify production/source/test/workflow code;
- mutate releases/tags/assets;
- force-push or rewrite history.

Only after the execution/evidence channel is independently proven should a later authority decide whether one new bounded installer attempt is justified.
