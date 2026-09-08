# CNX-20260901-215 — Task-214 Direct Scheduled Task Terminal-Propagation Qualification

Status: `READY_FOR_HERMES`
Date: 2026-09-01 ICT
Parent: `CNX-20260901-214`
Repair parent: `CNX-20260831-198`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Determine whether Windows Task Scheduler itself provides a durable, terminally observable execution boundary in the Hermes Windows environment by removing Task-214's nested wrapper -> child process boundary.

Task 215 is **harness-only**. It must not run the CogentNexus installer or any product lifecycle/semantic operation.

## Accepted parent result

Task-214 report:

`docs/operations/coordination/reports/CNX-20260901-214-task213-durable-windows-launcher-qualification.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260901-214-task213-durable-windows-launcher-qualification-review.md`

Accepted disposition:

`ACCEPT_PARTIAL__SCHEDULED_TASK_LAUNCH_PROVEN__TERMINAL_PROPAGATION_NOT_QUALIFIED`

Task 214 proved that Scheduled Task registration/start can create a harmless PowerShell process and persist `CHILD_START`, but it did not prove >=65-second lifetime, terminal marker, exit-code file, or Scheduler result 23. The nested wrapper/child boundary remains a confounder.

## Product authority — read-only reference only

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-207 repository-GREEN candidate remains:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Candidate plugin fingerprint:

`d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b`

Known live old generation:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

## Hard fence

Authorized only:

- one external evidence directory under `%LOCALAPPDATA%\Temp`;
- one harmless direct PowerShell script;
- one uniquely named temporary Task-215 Scheduled Task;
- exact registration/readback/start/observation/unregister of that task;
- read-only product/runtime verification;
- read-only Windows Task Scheduler Operational event-log capture scoped to the exact temporary task if needed.

Not authorized:

- CogentNexus installer/install-over;
- `cnxclaw` lifecycle actions;
- OpenClaw plugin/config mutation;
- Gateway restart;
- ownership/staging/transaction/backup mutation;
- SQLite writes;
- provider/model substitution;
- product source/test/workflow edits;
- Release/tag/asset mutation;
- force push;
- Discord traffic;
- killing unrelated processes.

## Phase A — fresh authority and preservation gate

Fresh-fetch branch HEAD, `ACTIVE.md`, `STATUS.md`, Task 214 report/review, and this Task 215.

Confirm no Task-215 report already exists.

Capture read-only live state:

- controller mode/generation;
- OpenClaw exact version;
- live plugin fingerprint/inventory;
- Gateway health;
- selected provider/Ollama state;
- delivery/recovery state;
- Task-205 cancellation/inert state;
- SQLite `PRAGMA integrity_check` and key durable counts;
- relevant product/lifecycle process residue.

Expected preserved shape:

```text
controller = passthrough
generation = 33
startup adapter = absent/disabled
live fingerprint = f82674172...
Gateway = healthy
Delivery = READY
Recovery = READY
Task-205 recovery = cancelled/inert
SQLite integrity = ok
```

If materially different, stop `BLOCKED_PREFLIGHT_DRIFT`.

## Phase B — direct harmless script

Create a uniquely named evidence root and a **single direct PowerShell script**. There must be no nested PowerShell child, wrapper, `Start-Process`, `Popen`, detached process, or shell relay.

The script itself must use direct file I/O to persist durable evidence independent of stdout handles.

Required behavior:

1. immediately write `DIRECT_START` with `$PID`, UTC timestamp, executable/process path and available command-line/context to a durable JSON/text file;
2. write a heartbeat file at start;
3. sleep for at least 65 seconds, preferably in small intervals that append heartbeat timestamps at approximately 10s, 30s, and 55s;
4. write `DIRECT_END` with final UTC timestamp;
5. write a dedicated `intended-exit-code.txt` containing `23` **before** process exit;
6. flush/close durable files;
7. execute `exit 23` as the final action.

The script must reference only its Task-215 evidence root and standard Windows/PowerShell facilities. It must not reference product paths.

Record SHA-256 and exact bytes before task registration.

## Phase C — register one direct Scheduled Task

Generate a unique task name such as:

`CogentNexus-OpenClaw-Task215-Direct-<suffix>`

Register exactly one temporary task whose action is directly:

```text
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
-NoLogo -NoProfile -ExecutionPolicy Bypass -File "<Task215 evidence root>\direct.ps1"
```

No wrapper script is allowed.

Use the same principal/logon model that successfully registered Task 214 unless fresh evidence requires otherwise. Record exact principal, action, arguments, settings, execution-time limit, trigger, retry/restart settings and task XML/readback.

Requirements:

- demand/manual start supported;
- no recurrence/repetition;
- no automatic restart/retry;
- execution time limit comfortably >65 seconds (>=5 minutes);
- no product task/path mutation.

Read the task back before execution. If mismatch, remove only the exact temporary task and stop `FAIL_TASK_REGISTRATION`.

## Phase D — exactly one direct run

Start the task exactly once.

Observe independently without owning the task process.

Required evidence samples:

- immediate/start;
- ~10–20 seconds;
- ~35–45 seconds;
- ~55–65 seconds;
- terminal sample after expected completion.

For each applicable running sample capture:

- Scheduled Task state;
- `Get-ScheduledTaskInfo` fields;
- exact PowerShell PID if discoverable;
- PID creation time;
- executable path;
- full command line;
- durable marker/heartbeat file sizes and hashes.

If observer command reconnects/timeouts, continue observing the same task. Do not start it again.

### Required PASS shape

All must hold:

```text
task start count = 1
DIRECT_START = present
process/task remains running beyond 10 seconds
heartbeat evidence reaches at least ~55 seconds
DIRECT_END = present
intended-exit-code.txt = 23
Scheduled Task terminal/non-running state = proven
LastTaskResult = 23, or an exactly documented equivalent representation proven from the observed task/event evidence
no second run/retry
```

If `DIRECT_END` and exit-code file exist but `LastTaskResult` is not 23, capture the exact Task Scheduler Operational events for this task and stop `FAIL_SCHEDULER_RESULT_PROPAGATION`.

If the direct script itself dies early or markers stop before intended lifetime, capture task events and stop `FAIL_DIRECT_SCHEDULED_TASK_LIFETIME`.

If terminal evidence is incomplete for another reason: `BLOCKED_TERMINAL_EVIDENCE`.

## Phase E — exact cleanup

After terminal evidence is captured, unregister only the exact Task-215 temporary task.

Prove:

- task absent;
- no Task-215 direct process remains;
- evidence directory retained;
- no unrelated task changed.

If cleanup is ambiguous: `FAIL_TASK_CLEANUP`.

## Phase F — product preservation

Repeat Phase A read-only checks and require no product/semantic mutation from Task 215.

Specifically:

- controller/generation unchanged absent independently explained external activity;
- live plugin fingerprint unchanged;
- Gateway healthy;
- delivery/recovery healthy;
- Task-205 cancellation inert;
- SQLite integrity `ok` and semantic counts unchanged by Task 215;
- no Discord traffic.

## Allowed dispositions

- `PASS_DIRECT_SCHEDULED_TASK_TERMINAL_PROPAGATION_QUALIFIED`
- `BLOCKED_PREFLIGHT_DRIFT`
- `FAIL_TASK_REGISTRATION`
- `FAIL_DIRECT_SCHEDULED_TASK_LIFETIME`
- `FAIL_SCHEDULER_RESULT_PROPAGATION`
- `BLOCKED_TERMINAL_EVIDENCE`
- `FAIL_TASK_CLEANUP`
- `FAIL_PRODUCT_PRESERVATION`
- `BLOCKED_EVIDENCE`

## Successor rule

Even on PASS, Task 215 does not run the CogentNexus installer.

Only after independent review of Task-215 PASS may a separate successor authorize the exact Task-207 installer through a topology derived from the qualified direct Scheduled Task execution model, with explicit installer stream/stage/exit-code persistence.

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260901-215-task214-direct-scheduled-task-terminal-propagation-qualification.md`

Include exact task registration, script hash, start count, process identity samples, heartbeat/marker timeline, intended exit-code file, Scheduler terminal fields/events, cleanup proof, before/after product state and mutation ledger.
