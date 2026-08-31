# CNX-20260830-158 — Windows Install-Over Observability + Recovery Diagnosis

Status: `IN_PROGRESS_CHATGPT`

Execution mode: `REPOSITORY_WINDOWS_INSTALL_OVER_OBSERVABILITY_DIAGNOSIS`

Owner / executor / reviewer: ChatGPT (self-review allowed; must be labeled as self-review and not independent)

## Trigger

Task 157 is durably reviewed `BLOCKED` because the real Windows install-over exceeded the executor's 420-second window without a proven installer completion/exit boundary. The repaired plugin fingerprint was not installed, while the live system remained safely in `passthrough` with the existing plugin disabled.

Task 157's raw installer capture remained local to the Windows executor and was not published into GitHub. The durable report proves that execution progressed through native handoff, skill backup/replacement, validation, host initialization, and database snapshot, but does not prove which later installer substage consumed the remaining execution window.

Repository inspection also shows that the production Windows installer invokes important external substages, including `openclaw plugins install`, without a stable installer-owned stage-start/stage-complete/elapsed marker contract. A process interrupted while an external command is running therefore cannot be localized precisely from durable installer output alone.

## Objective

Improve **diagnosability only** for the established Windows install-over path so a later live retry can identify the active installer substage and elapsed duration without changing installation behavior or safety semantics.

Use TDD:

1. RED — add a minimal regression contract that fails because required installer-owned diagnostic markers/timing are absent around the late install-over substages implicated by Task 157.
2. Verify RED on CI / authoritative test execution.
3. GREEN — add the smallest production observability change needed to satisfy the contract.
4. Re-run the focused tests and relevant repository validation/workflows.
5. Publish a Task 158 report and explicit ChatGPT self-review checkpoint.

## Required diagnostic contract

The installer must emit machine-searchable, stable diagnostic records for the critical late install-over substages beginning at the database bootstrap and continuing through plugin rollover/replacement and runtime provisioning. Each instrumented external substage must provide enough information to determine:

- stable stage identifier;
- UTC start timestamp;
- successful/returned completion boundary;
- elapsed duration;
- returned exit code when the child command returns.

At minimum the contract must cover:

1. ticket database bootstrap;
2. npm package creation used for plugin replacement;
3. rollover prepare when applicable;
4. local-package `openclaw plugins install` replacement;
5. post-install plugin disable;
6. rollover finalize when applicable;
7. owned-runtime provisioning (`ensure-runtime`).

A hard external termination may prevent a completion record; in that case the final durable `START` record must identify the command/stage that was active when termination occurred.

## Semantic preservation fence

Task 158 is **not** an installer behavior repair unless a separate proven defect is discovered and durably re-scoped.

Do not change under this task:

- classification semantics;
- native handoff / `passthrough` semantics;
- `--force` behavior;
- plugin install/replacement ordering;
- plugin enable/disable policy;
- rollover prepare/finalize semantics;
- fresh-install rollback semantics;
- upgrade rollback semantics;
- ownership creation/verification semantics;
- runtime provisioning semantics;
- dependency versions;
- OpenClaw source;
- Dashboard delivery/runtime behavior.

Do not add retries, timeouts, rollback, sleeps, process killing, or alternate package-install mechanisms merely to address the Task 157 timeout.

## Evidence-retention requirement for successor live task

Task 158 must also document the evidence contract for the later live retry: the executor must publish enough of the raw installer/subprocess capture (or a faithful durable text artifact/excerpt with hashes and timestamps) into GitHub coordination evidence so ChatGPT can inspect the actual boundary rather than relying only on a prose summary.

## No live actions

Task 158 performs repository/source/test/docs/CI work only.

No Windows live install mutation, Dashboard semantic Send, Dashboard click/focus/type/paste, reset, uninstall, reinstall, runtime state mutation, DB mutation, semantic mutation, merge, tag, release, promotion, or force push is authorized.

## Acceptance

PASS requires all of the following:

1. RED regression test is demonstrated against the pre-fix production installer.
2. Minimal observability change passes the focused regression.
3. Existing installer transaction/ownership tests remain green.
4. Relevant Windows installer/validation workflows are green on the exact repair commit.
5. Diff review confirms no installer semantic change beyond diagnostics/timing/output capture.
6. Task 158 report is committed.
7. ChatGPT self-review is committed and explicitly labeled non-independent.

After Task 158 ACCEPT, stop repository work and create a separate Hermes live-retry task. That successor remains fenced from Dashboard semantic Send until repaired-candidate installation and health are accepted.
