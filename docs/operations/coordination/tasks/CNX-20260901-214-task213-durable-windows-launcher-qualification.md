# CNX-20260901-214 — Task-213 Durable Windows Launcher Qualification

Status: `READY_FOR_HERMES`
Date: 2026-09-01 ICT
Parent: `CNX-20260901-213`
Repair parent: `CNX-20260831-198`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Qualify a Windows process-launch topology that remains alive independently of the Hermes executor/session and provides durable stdout/stderr plus a trustworthy terminal result.

This task is **harness-only**. It must not run the CogentNexus installer, `cnxclaw`, OpenClaw plugin lifecycle, Gateway lifecycle, model inference, or Discord traffic.

The intended topology to qualify is a temporary, uniquely named Windows Scheduled Task owned only by this evidence run.

## Accepted parent result

Task-213 report:

`docs/operations/coordination/reports/CNX-20260901-213-task212-installer-source-and-detached-launch-root-cause-adjudication.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260901-213-task212-installer-source-and-detached-launch-root-cause-adjudication-review.md`

Accepted disposition:

`ACCEPT_PASS_DETACHED_LAUNCH_HARNESS_DEFECT_PROVEN__QUALIFY_DURABLE_WINDOWS_LAUNCHER_BEFORE_INSTALLER`

Task 213 proved that the Task-212 `Popen(... DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP ...)` topology is defective/incompatible in this executor environment: a harmless PowerShell child expected to live >=65 seconds disappeared before 10 seconds with zero-byte stdout/stderr and no terminal markers.

## Product authority — read-only reference only

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-207 repository-GREEN candidate remains:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Task-207 candidate fingerprint remains:

`d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b`

Task 214 does not install or mutate this candidate.

## Hard fence

Task 214 authorizes only:

- creation of one external evidence directory under `%LOCALAPPDATA%\Temp`;
- creation of harmless synthetic PowerShell/wrapper scripts inside that evidence directory;
- registration/start/observation/deletion of **one uniquely named temporary Scheduled Task** for harness qualification;
- read-only product/runtime verification before and after the harmless test.

Task 214 does **not** authorize:

- CogentNexus installer/install-over;
- `cnxclaw enable/disable/start/stop/restart/reset/uninstall`;
- OpenClaw plugin install/enable/disable/config mutation;
- Gateway restart;
- ownership/staging/transaction/backup mutation;
- SQLite writes;
- provider/model/config substitution;
- source/test/workflow product edits;
- Release/tag/asset mutation;
- force push;
- Discord Send/API/bot/injected traffic;
- killing unrelated processes.

## Phase A — fresh authority and live preservation

Fresh-fetch branch HEAD, `ACTIVE.md`, `STATUS.md`, Task 213 report/review, and this Task 214.

Confirm no Task-214 report already exists.

Capture read-only live state sufficient to prove the harness test does not change product state:

- controller mode/generation;
- OpenClaw exact version;
- live CogentNexus plugin fingerprint/inventory;
- Gateway health;
- selected provider/Ollama readiness;
- delivery/recovery state;
- Task-205 cancelled/inert recovery state;
- SQLite `PRAGMA integrity_check` and key durable counts;
- relevant product lifecycle/process residue.

Expected starting state remains the Task-213 preservation boundary:

```text
controller = passthrough
startup adapter = absent/disabled
live plugin fingerprint = f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
Gateway = healthy
Delivery = READY
Recovery = READY
Task-205 historical recovery = cancelled/inert
SQLite integrity = ok
```

If product state drifted materially, report `BLOCKED_PREFLIGHT_DRIFT`; do not create the temporary task.

## Phase B — build harmless scheduled-task harness

Create a unique evidence root, for example:

`%LOCALAPPDATA%\Temp\cnx214-launcher-qualification-<timestamp>`

Create a harmless synthetic child script inside that root. It must:

1. immediately write a deterministic `CHILD_START` line to stdout;
2. immediately write a deterministic `CHILD_STDERR_START` line to stderr;
3. record `$PID`, UTC timestamp, process path if available, and arguments/context into an evidence file;
4. sleep for at least **65 seconds**;
5. write deterministic terminal markers to stdout and stderr;
6. exit with the known non-zero code **23**.

The child must not reference CogentNexus, OpenClaw, Ollama, the workspace, plugin directories, or product state.

Create a harness wrapper inside the same evidence root. The wrapper must:

- invoke the synthetic child with explicit absolute `powershell.exe` path;
- redirect child stdout and stderr to separate evidence files;
- wait for the direct synthetic child to terminate;
- persist the child exit code to a dedicated file;
- exit with the same child exit code;
- avoid detached-process flags;
- avoid `Start-Process -Wait` semantics involving product descendants; this harmless child has no descendants besides ordinary shell infrastructure.

Record SHA-256 hashes of both scripts before registration.

## Phase C — temporary Scheduled Task registration

Generate a globally unique task name containing Task 214 and a random/timestamp suffix, for example:

`CogentNexus-OpenClaw-Task214-Harness-<suffix>`

Use Windows Task Scheduler supported PowerShell cmdlets/API to register a one-shot/manual-start task whose action is the absolute PowerShell wrapper path from the Task-214 evidence root.

Requirements:

- no product task name may be reused;
- do not alter CogentNexus startup task/adapter;
- task action/arguments/working directory must be captured exactly;
- task principal/run level must be recorded;
- task settings including execution time limit must be recorded;
- execution time limit must comfortably exceed the 65-second child lifetime;
- the task must not auto-repeat/retry;
- no trigger recurrence is permitted;
- the temporary task must be clearly identifiable as Task-214 harness state.

Immediately read the registered task back and prove exact name/action/arguments/settings before starting it.

If registration/readback differs: delete only the exact temporary task if safely identifiable, report `FAIL_TASK_REGISTRATION`, and stop.

## Phase D — harmless run qualification

Start the temporary task exactly once.

Observe using read-only calls that are independent of the task process:

- Task Scheduler state and `Get-ScheduledTaskInfo`;
- task `LastRunTime` and `LastTaskResult`;
- synthetic PowerShell process PID + creation time + executable + full command line while running;
- stdout/stderr size/hash growth;
- child identity evidence file;
- persisted child exit-code file.

Required samples:

1. immediate/start sample;
2. a sample around 10–20 seconds proving the child is still alive/running;
3. a sample around 40–55 seconds proving continued lifetime;
4. terminal sample after >=65 seconds.

Observer command timeout/reconnect must not stop or restart the Scheduled Task.

Do not start the task a second time.

### Required PASS shape

All of the following must hold:

- task invocation count = 1;
- child process is observed alive after at least 10 seconds;
- child process remains alive long enough to reach the intended >=65-second lifetime;
- stdout contains `CHILD_START` and terminal marker;
- stderr contains `CHILD_STDERR_START` and terminal marker;
- child identity file binds PID + creation time + executable/argv/context;
- wrapper persists child exit code `23`;
- Scheduled Task reaches a terminal non-running state;
- `LastTaskResult` equals `23` (or, if Task Scheduler wraps the value, the exact documented/observed representation is proven equivalent to process exit 23; do not guess);
- no task retry/second run occurred;
- no product process/state changed.

If the task disappears early, streams remain empty, terminal result is unavailable, or child exit code cannot be reconciled: `FAIL_DURABLE_LAUNCHER_QUALIFICATION`.

## Phase E — exact cleanup

After terminal evidence is fully captured, unregister **only the exact Task-214 temporary task**.

Prove:

- exact task no longer exists;
- no Task-214 synthetic child/wrapper process remains;
- evidence files remain available;
- no product startup task/adapter was modified;
- no unrelated Scheduled Task was changed.

Do not delete the evidence directory before report publication.

## Phase F — final product-state preservation

Repeat the read-only product checks from Phase A.

Require no semantic/product change caused by the harness qualification:

- controller mode/generation unchanged unless unrelated external activity is independently proven and explained;
- live plugin fingerprint unchanged;
- Gateway still healthy;
- delivery/recovery unchanged/healthy;
- Task-205 cancellation remains inert;
- SQLite integrity remains `ok` and no Task-214 semantic Ticket/model/delivery/recovery rows were created;
- no Discord traffic occurred.

## Allowed dispositions

- `PASS_DURABLE_SCHEDULED_TASK_LAUNCHER_QUALIFIED`
- `BLOCKED_PREFLIGHT_DRIFT`
- `FAIL_TASK_REGISTRATION`
- `FAIL_DURABLE_LAUNCHER_QUALIFICATION`
- `FAIL_TASK_CLEANUP`
- `FAIL_PRODUCT_PRESERVATION`
- `BLOCKED_EVIDENCE`

## Successor authorization rule

Even if Task 214 passes, **do not run the CogentNexus installer in Task 214**.

A separate Task 215 must be opened/reviewed to use the exact qualified Scheduled Task wrapper topology with a freshly verified Task-207 candidate extraction/package boundary and a new uniquely named temporary installer task.

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260901-214-task213-durable-windows-launcher-qualification.md`

The report must include:

- fresh authority/preflight;
- task name and complete registered action/settings/principal;
- child/wrapper script hashes;
- exact run count;
- process identity samples with creation times;
- stdout/stderr sizes/hashes and markers over time;
- child exit-code proof;
- Task Scheduler terminal state and `LastTaskResult`;
- exact cleanup proof;
- before/after product-state preservation;
- mutation ledger;
- final disposition.

Stop after publishing the report for ChatGPT review.
