# CNX-20260905-252 — Task-251 Scheduled Execution-Limit Timeout Forensic

Status: `READY_FOR_HERMES`  
Executor: Hermes / authenticated Windows operator  
Coordinator / independent reviewer: ChatGPT  
Parent task: `CNX-20260904-251`  
Parent review commit: `24df69a9d23f8e2b072587109d72f85ac201d674`  
Parent review verdict: `ACCEPT_BLOCKED_EVIDENCE__ONE_SHOT_BOUNDARY_RESPECTED__SCHEDULER_EXECUTION_LIMIT_TERMINATION_PROVEN__INSTALLER_CHILD_STAGE_UNPROVEN__READ_ONLY_TIMEOUT_FORENSIC_REQUIRED`  
Exact candidate under investigation: `9c3c4e0fe0afbedf9233c25c0dd36e4209fb9d96`  
Parent umbrella: `CNX-20260831-188`

## Objective

Determine the last provable installer/runner stage reached by the single Task-251 execution and why it remained running until the Windows Scheduled Task execution limit terminated it.

Task 252 is forensic/read-only with respect to live product state. It MUST NOT retry the installer, start the Task-251 Scheduled Task, invoke rollover prepare/finalize, repair/cleanup product state, or submit semantic messages.

The Task-251 report proves:

```text
installer task registration = 1 successful
installer start = 1
installer invocation = 1
retry after start = 0
runner child start = 2026-09-04T17:22:05.7455411Z
terminal task state = Ready
LastTaskResult = 267014 (0x41306)
runner result = absent
child stdout/stderr = absent
complete transcript = absent
postflight = predecessor plugin, passthrough generation 39
```

Do not infer an installer stage from missing output.

## Phase A — fresh GitHub authority

Before Windows evidence collection:

1. fetch branch HEAD and re-read Task251 report/review plus ACTIVE/STATUS;
2. require Task252 is the active task before any task-specific evidence write;
3. verify candidate `9c3c4e0...` remains in ancestry and public `v0.9.3` remains `26ce64a624255278a3a0266ad38746e0e6ed2e31`;
4. require no unexpected product/source/test/workflow drift.

Unexpected authority drift: `BLOCKED_PREFLIGHT_DRIFT`.

## Phase B — evidence preservation and exact Task-251 runner identity

Locate the Task-251 durable evidence root and the detached candidate checkout used by Task251. Do not modify either.

Create only a separate Task-252 forensic evidence root under:

`%LOCALAPPDATA%/CogentNexus-OpenClaw/forensics/CNX-20260905-252/`

Capture hashes/metadata for all surviving Task-251 artifacts, including where present:

- runner source;
- runner SHA-256;
- launch manifest + SHA-256;
- task-registration helper/script;
- pre-start readback;
- runner-started marker;
- child-start marker/PID/identity;
- observer log;
- transcript/stdout/stderr/result paths, including explicit absence;
- Task Scheduler task XML/export;
- exact detached checkout path/HEAD and installer SHA-256.

If Task-251 artifacts have disappeared, report exactly what is missing; do not recreate them.

## Phase C — Scheduled Task termination proof

Read only the registered Task-251 task and relevant Windows event records.

Record:

- exact task action, arguments, working directory;
- principal/logon type/run level;
- `ExecutionTimeLimit` and all other termination/restart settings;
- task start and terminal timestamps;
- exact elapsed duration;
- `LastTaskResult` in decimal/hex;
- TaskScheduler Operational events around the Task-251 window;
- Windows PowerShell/Application/System events relevant to the runner/child;
- whether the terminal result is temporally consistent with the configured execution limit.

Do not change, disable, delete, start, or re-register the task.

## Phase D — runner observability semantics

Statically inspect the exact Task-251 runner source and manifest.

Determine, with line-level evidence:

1. whether child stdout/stderr are streamed durably while the child is running or buffered in memory until child completion;
2. when transcript/result files are opened/written/flushed;
3. whether `finally`/cleanup can execute if the outer runner process is forcibly terminated by Task Scheduler;
4. whether a forced outer-process termination can explain the exact absence pattern observed in Task251 without implying a child exit code;
5. whether Task251 runner bytes/topology differ materially from the previously successful diagnostic runner path in Task248/Task245/Task243, using retained runner hashes/source where available.

This phase is static/read-only. Do not execute the runner.

## Phase E — reconstruct the last installer stage from residue

Using the exact candidate `9c3c4e0...`, map filesystem residues and timestamps back to installer stage order without invoking installer commands.

Inspect read-only:

### Detached candidate checkout

- whether `plugins/cogentnexus-openclaw/node_modules` exists and its bounded timestamp/inventory evidence;
- evidence consistent with `npm ci` starting/completing;
- plugin validation/generated artifact timestamps where diagnostically useful;
- any candidate-checkout temp/output residue created by the one installer invocation.

Do not run `npm ci`, validation, or any build command in this task.

### Workspace/app-data installer residue

Inventory and hash relevant artifacts created/changed in the Task-251 window:

- `.cogentnexus-openclaw/install-backups`;
- `.cogentnexus-openclaw/install-staging`;
- `%LOCALAPPDATA%/CogentNexus-OpenClaw/plugin-generation-rollover-backups`;
- rollover transactions/inventories;
- fresh-install transaction residue if any;
- installer/classification temporary inventory residue if still present;
- ownership manifest identity;
- canonical plugin tree identity.

For every new Task-251 artifact, record path, type, creation/last-write timestamps, bounded inventory, and SHA-256 where applicable.

If a new Task-251 generation rollover backup exists, classify it read-only as:

- absent;
- partial/incomplete;
- complete relative to the current retired tree;

and record the evidence. Do not delete, rename, complete, or repair it.

Map each residue to the earliest/latest exact installer stage that could have created it by reading candidate source. Produce a monotonic stage table:

```text
stage
required predecessor evidence
Task251 evidence present/absent
classification: proven reached / proven not reached / unresolved
```

Do not infer success from timestamps alone.

## Phase F — historical process/event evidence

Use bounded read-only sources available on the host, such as:

- TaskScheduler Operational;
- Windows PowerShell logs;
- Security 4688 process creation if auditing retained it;
- Sysmon if installed and historical events exist;
- Application/System/WER events;
- Defender Operational where relevant;
- current process inventory to determine whether any Task-251 child survived termination.

Record exact limitations. Post-event absence is not proof a process never existed.

Do not terminate any surviving process in this task. If a Task-251 installer/child is unexpectedly still active, classify `BLOCKED_LIVE_CHILD_STILL_ACTIVE` and STOP after read-only evidence capture.

## Phase G — bounded read-only performance context (only if needed)

Only if Phases B–F establish a likely copy/hash boundary but cannot distinguish ordinary duration from pathological stall, one bounded read-only timing probe of `_project_tree_sha256()` against the current retired tree is allowed.

- maximum one logical timing probe;
- no copytree;
- no installer/prepare invocation;
- no source/backup mutation;
- treat current timing only as context, never as proof of historical timing.

Skip this phase if it does not materially reduce uncertainty.

## Required causal discipline

Distinguish these layers explicitly:

```text
scheduler termination mechanism
runner evidence-loss mechanism
last provable installer stage
underlying reason child failed to return before limit
```

Proving the scheduler timeout does NOT by itself prove why the child was still running.

Do not propose increasing `ExecutionTimeLimit`, changing installer semantics, excluding tree paths, or retrying the installer unless the evidence supports the corresponding root cause.

## Hard fences / effect budget

```text
scripts/install.ps1 invocations = 0
Task-251 Scheduled Task starts = 0
new installer Scheduled Task registrations = 0
rollover prepare/finalize invocations = 0
plugin install/copy/delete/rename = 0
retired-project writes = 0
Task248/Task251 rollover-backup writes/deletes/renames = 0
controller/Gateway/provider/model lifecycle mutation = 0
Ticket/outbox/recovery/SQLite mutation = 0
Dashboard semantic sends = 0
Discord semantic sends = 0
direct API semantic sends = 0
recovery replay/resend = 0
manual process termination = 0
production/source/test/workflow edits = 0
release/tag/history mutation = 0
```

Evidence-only writes under the separate Task-252 forensic root and report publication are authorized.

## Allowed dispositions

- `PASS_TASK251_LAST_STAGE_AND_TIMEOUT_ROOT_CAUSE_PROVEN`
- `PASS_TASK251_LAST_STAGE_PROVEN__RUNNER_EXTERNAL_TERMINATION_EVIDENCE_LOSS_PROVEN__UNDERLYING_CHILD_STALL_CAUSE_UNPROVEN`
- `BLOCKED_TASK251_CHILD_STAGE_UNPROVEN__STREAMING_DIAGNOSTIC_HARNESS_REQUIRED`
- `BLOCKED_TASK251_EVIDENCE_LOST`
- `BLOCKED_LIVE_CHILD_STILL_ACTIVE`
- `BLOCKED_PREFLIGHT_DRIFT`

A PASS here means forensic question answered to the stated level; it does not authorize live installer retry by itself.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260905-252-task251-scheduled-execution-limit-timeout-forensic.md`

Include fresh authority, exact task settings/XML evidence, runner/manifest hashes, artifact inventory, event/process evidence, residue-to-stage table, explicit uncertainty boundaries, hard-fence ledger, final disposition, and recommendation for the smallest next step.

Then STOP for independent ChatGPT review. Installer retry and semantic acceptance remain unauthorized.
