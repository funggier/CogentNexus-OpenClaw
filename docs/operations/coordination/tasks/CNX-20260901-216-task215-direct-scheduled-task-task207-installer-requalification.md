# CNX-20260901-216 — Task-215 Direct Scheduled Task Task-207 Installer Requalification

Status: `READY_FOR_HERMES`
Date: 2026-09-01 ICT
Parent: `CNX-20260901-215`
Repair parent: `CNX-20260831-198`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Install the exact repository-GREEN Task-207 candidate on the Windows host exactly once using the direct Windows Scheduled Task execution model proven by Task 215, then prove exact installed provenance and healthy managed runtime convergence.

Task 216 is installer/provenance/health only. It authorizes **0 Discord Sends**. Semantic Discord acceptance remains a separate successor after independent Task-216 PASS review.

## Immutable authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-207 repaired candidate:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Accepted package proof:

```text
artifact ID: 9790881384
artifact digest: sha256:1733897690890f9adcb12176b79db2b43e27799a4022743c4597fad44d2d5a34
candidate plugin fingerprint: d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b
payload files: 192
zip SHA-256: 0321028fc6214e18dbc965ad79a6d04328a05a84dce6a9efc058fb1122237986
tar.gz SHA-256: 0ab3884621a518b4cfd46949e3c8e3e7f9f52995bee257743960dd7636794dcf
```

Accepted OpenClaw baseline:

`2026.7.1-2 (0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c)`

Known preserved live old generation before Task 216:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

## Parent launcher authority

Task-215 report:

`docs/operations/coordination/reports/CNX-20260901-215-task214-direct-scheduled-task-terminal-propagation-qualification.md`

Task-215 review:

`docs/operations/coordination/reviews/CNX-20260901-215-task214-direct-scheduled-task-terminal-propagation-qualification-review.md`

Accepted disposition:

`ACCEPT_WITH_DURATION_DEVIATION__DIRECT_TERMINAL_PROPAGATION_PROVEN__INSTALLER_REQUALIFICATION_AUTHORIZED`

The direct Scheduled Task-owned PowerShell topology is accepted for installer execution. Do **not** reuse Task-215's `PT3M` duration. Task 216 requires a task execution limit of at least **30 minutes**.

## Hard fences

Task 216 authorizes:

- one fresh exact candidate preparation/provenance verification;
- one uniquely named temporary Scheduled Task for the Task-207 installer;
- exactly one invocation of the exact candidate installer;
- installer-owned normal effects only;
- read-only observation and post-install verification;
- deletion of only the exact temporary Task-216 installer task after terminal evidence.

Task 216 does **not** authorize:

- a second installer attempt;
- manual `cnxclaw enable/disable/start/stop/restart/reset/uninstall` workaround;
- manual plugin enable/disable/install/uninstall outside the installer;
- manual ownership/manifest/transaction/backup normalization;
- raw SQLite writes;
- provider/model substitution;
- OpenClaw upgrade;
- product source/test/workflow edits;
- Release/tag/asset mutation;
- force push;
- Discord Send/API/bot/injected traffic.

## Phase A — fresh coordination/provenance/replay gate

Fresh-fetch branch HEAD, ACTIVE.md, STATUS.md, Task-215 report/review and this Task 216.

Confirm:

- no Task-216 report already exists;
- no existing Task-216 temporary installer task exists;
- no installer/lifecycle process from Tasks 210–215 remains;
- repository product candidate remains `27fe0181...` with no unexplained product source/test/workflow drift.

Prepare a **fresh isolated checkout/source tree** exactly at `27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`. Do not use retained ignored/generated `dist` from a coordination checkout as candidate provenance.

Before mutation, prove:

- checkout HEAD exact `27fe0181...`;
- worktree clean;
- exact `scripts/install.ps1` SHA-256 matches candidate bytes;
- Task-207 repair source file matches candidate bytes;
- `npm ci`/plugin validation/package preparation needed to compute the repository-supported plugin fingerprint succeeds;
- computed candidate fingerprint equals `d0677581...`;
- retained artifact/archive hashes match the accepted Task-207 authority.

If candidate/source/package identity is ambiguous: `BLOCKED_AUTHORITY`, no task registration/start.

## Phase B — live ordinary-upgrade preflight

Immediately before installer task registration/start, capture read-only:

- OpenClaw exact version;
- controller mode/generation;
- Gateway health;
- selected provider/Ollama readiness;
- startup adapter state;
- delivery/recovery checks;
- SQLite `PRAGMA integrity_check` and key counts;
- live plugin inventory/fingerprint;
- ownership manifest/verification;
- install-staging/rollover transaction inventory;
- Task-205 cancelled recovery and any current emittable residue;
- relevant installer/lifecycle process inventory.

Run exact candidate attested `classify-install` with live plugin inventory and expected replacement fingerprint `d0677581...`.

Required safe shape:

```text
controller = passthrough
startup adapter = absent/disabled
live fingerprint = f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
candidate fingerprint = d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b
mode = upgrade
pendingRollover = false
pluginAlreadyExact = false
replacementPluginPath = null
legacy = []
Gateway = healthy
Delivery = READY
Recovery = READY
Task-205 recovery = cancelled/inert
SQLite integrity = ok
no candidate-bound active/pending rollover transaction
no current installer/lifecycle process
```

If material drift exists, stop `BLOCKED_PREFLIGHT_DRIFT`; do not install.

## Phase C — durable same-process installer runner

Create a unique external evidence root under `%LOCALAPPDATA%\Temp`.

Create one Task-216 runner PowerShell script in the evidence root. This runner is the **top-level Scheduled Task-owned PowerShell process**. It must not spawn another PowerShell process.

The runner must:

1. persist `RUNNER_START`, PID, UTC, executable path, exact candidate installer path/hash and workspace;
2. start a transcript and/or six-stream durable log inside the evidence root;
3. invoke the exact candidate `scripts/install.ps1 -Workspace C:/Users/CDQ-P/.openclaw/workspace` exactly once using same-process PowerShell script invocation (`& <exact-install.ps1> ...`), not `Start-Process`, not nested `powershell.exe`, not Popen/detached execution;
4. preserve installer Write-Host diagnostic stage markers in durable log/transcript;
5. on normal return persist `installer-result=0`;
6. on PowerShell exception persist the exception and `installer-result=1` (or exact nonzero harness result) without starting another installer;
7. persist `RUNNER_END` and close/flush logs;
8. exit with the same runner result so Task Scheduler receives terminal success/failure.

Record runner SHA-256 and exact contents before registration.

The runner itself is harness-only; it must not perform compensating lifecycle/plugin/database actions after installer failure.

## Phase D — one temporary installer Scheduled Task

Register one uniquely named temporary task such as:

`CogentNexus-OpenClaw-Task216-Installer-<suffix>`

Action:

```text
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
-NoLogo -NoProfile -ExecutionPolicy Bypass -File "<Task216 evidence root>\installer-runner.ps1"
```

Required settings:

- same proven interactive principal model unless fresh evidence requires otherwise;
- `ExecutionTimeLimit >= PT30M`;
- `RestartCount = 0`;
- no recurrence/repetition;
- demand/manual start allowed;
- one start only;
- no automatic retry.

Read back exact task action/principal/settings/XML before starting. If mismatch, unregister only that exact temporary task and stop `FAIL_TASK_REGISTRATION`.

## Phase E — exactly one installer execution

Start the Task-216 temporary task exactly once.

Observe independently from Hermes using bounded read-only samples. Do not own, kill or restart the Scheduled Task process.

Capture at minimum:

- initial/start sample;
- ~30–60 second samples while running;
- current installer stage from durable transcript/log;
- stream/log size/hash growth;
- Task Scheduler state and `Get-ScheduledTaskInfo`;
- exact top-level PowerShell PID + creation time + executable + argv;
- process tree showing expected installer child commands only;
- terminal sample after completion.

Historical successful install-over took roughly 13–14 minutes and `plugin-rollover-prepare` roughly 430–434 seconds. Runtime alone is not failure while evidence progresses.

Do not declare timeout before 25 minutes. The Scheduler execution limit must be >=30 minutes. If still running near the limit, capture process tree/CPU/log growth/current stage and stop `BLOCKED_INSTALLER_STILL_RUNNING` without starting another installer or killing it.

### Required installer terminal PASS evidence

All of the following are required:

- task start count = 1;
- runner start identity proven;
- runner invoked exact candidate installer exactly once;
- runner result file = `0`;
- `RUNNER_END` present;
- Scheduled Task terminal/non-running;
- `LastTaskResult = 0`;
- durable installer log contains all seven matching stage pairs with exit code 0:
  - `ticket-db-bootstrap`
  - `plugin-npm-pack`
  - `plugin-rollover-prepare`
  - `plugin-install-local-package`
  - `plugin-disable-post-install`
  - `plugin-rollover-finalize`
  - `owned-runtime-ensure`
- durable log contains:
  `CogentNexus-OpenClaw v0.9.3 installation completed successfully.`
- no terminal exception/error contradicts success.

If the runner/Task Scheduler returns nonzero or a stage reports nonzero: `FAIL_INSTALLER`, no retry.

If terminal process evidence is incomplete despite apparent state change: `BLOCKED_INSTALLER_TERMINAL`, no retry.

## Phase F — independent post-install provenance

Only after terminal installer success, independently prove:

```text
installed fingerprint = d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b
plugin id = cogentnexus-openclaw
plugin version = 0.9.3
plugin enabled = true
plugin status = loaded
plugin error = null
OpenClaw = 2026.7.1-2
ownership verify = pass
```

Capture the new rollover transaction and prove its expected replacement fingerprint equals `d0677581...` and final ownership is coherent. Preserve historical transaction records; do not delete merely for cleanliness.

If provenance differs: `FAIL_PROVENANCE`.

## Phase G — managed health and stability

Require:

- controller mode `managed`;
- desired Gateway/provider `running`;
- selected provider `ollama`;
- Gateway healthy on expected loopback endpoint;
- Ollama ready/reachable;
- startup adapter installed/enabled/Ready with healthy last result;
- delivery `READY`, pending outbox `0`;
- recovery `READY`, no unexpected recovery incident;
- no active/recovering stale model call;
- Task-205 historical cancelled recovery remains inert;
- SQLite integrity `ok`;
- no Task-216 installer/lifecycle residue except the still-registered temporary task before cleanup.

Take a second read-only stability sample after convergence.

Do not issue compensating `enable`, restart, reset, uninstall or reinstall if managed health fails. Report exact state as `FAIL_MANAGED_HEALTH`.

## Phase H — exact temporary task cleanup

After terminal installer evidence and postflight capture, unregister only the exact Task-216 temporary installer task.

Prove:

- exact task absent;
- no Task-216 runner process remains;
- no unrelated Scheduled Task changed;
- evidence root/logs remain available.

If cleanup fails: `FAIL_TASK_CLEANUP`.

## Discord boundary

Task 216 authorizes:

`0 Discord Sends`

No human Send, bot/API/injected message, acceptance nonce or semantic model request. Discord requalification is a separate successor only after independent Task-216 PASS review.

## Allowed dispositions

- `PASS`
- `BLOCKED_AUTHORITY`
- `BLOCKED_PREFLIGHT_DRIFT`
- `FAIL_TASK_REGISTRATION`
- `BLOCKED_INSTALLER_STILL_RUNNING`
- `BLOCKED_INSTALLER_TERMINAL`
- `FAIL_INSTALLER`
- `FAIL_PROVENANCE`
- `FAIL_MANAGED_HEALTH`
- `FAIL_TASK_CLEANUP`
- `BLOCKED_EVIDENCE`

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260901-216-task215-direct-scheduled-task-task207-installer-requalification.md`

Include:

- fresh authority/provenance gate;
- exact preflight classifier output;
- candidate/live fingerprints;
- exact temporary task action/settings/principal;
- runner hash/content summary;
- task start count and top-level process identity samples;
- installer stage table with timestamps/exits;
- transcript/log hashes/sizes;
- runner result and Scheduler `LastTaskResult`;
- installed fingerprint and rollover transaction proof;
- plugin/OpenClaw/ownership/managed health;
- Task-205 inert-state proof;
- SQLite integrity and semantic-count preservation/reconciliation;
- exact task cleanup;
- mutation ledger;
- final disposition.

Stop after publishing the report for ChatGPT review.
