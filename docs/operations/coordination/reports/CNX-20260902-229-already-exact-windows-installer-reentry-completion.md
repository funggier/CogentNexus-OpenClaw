# CNX-20260902-229 — Already-Exact Windows Installer Re-entry Completion

Date: 2026-09-02 ICT  
Primary disposition: `FAIL_TASK_REGISTRATION`  
Parent: `CNX-20260902-228`  
Repair parent: `CNX-20260902-226`  
Failure parent: `CNX-20260902-223`

## Decision

Task 229 was authorized to perform exactly one already-exact installer re-entry, but only after a temporary direct Windows Scheduled Task could be registered and read back. Registration failed closed on this Windows host before a Task-229 task was created. Therefore:

```text
installer invocations: 0
Task-229 registrations: 0 successful
Task-229 starts: 0
```

Primary disposition:

```text
FAIL_TASK_REGISTRATION
```

The installer was not invoked, no retry was attempted, and no product/live mutation was performed.

## Fresh authority and preflight

Fresh remote branch authority was read before execution:

```text
branch: agent/v0.9.3-full-stabilization
initial authority HEAD: 28dde7b978180a863c3d39458d2c93e94dc31103
repair ancestor: 9a8510f1317c8e53c01c233b080ec20357cd22df
public v0.9.3: 26ce64a624255278a3a0266ad38746e0e6ed2e31
```

The source/product drift gate found no product/source/test/workflow drift beyond coordination files relative to the accepted repair. Exact-first candidate checkout was created at:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx229-source-exact-20260902T
```

The checkout was detached at:

```text
9a8510f1317c8e53c01c233b080ec20357cd22df
```

It was clean and passed:

```text
npm.cmd ci
npm.cmd run plugin:validate
packedFileCount: 192
```

Fresh Actions at the preflight snapshot had Windows Installer Pack Smoke and PS5.1 Acceptance Smoke successful; Validate was still in progress. No CI claim was used to override the task's local registration gate.

## Live preflight

Read-only live state before registration:

```text
controller mode: passthrough
generation: 33
startup adapter: installed=false
Gateway: healthy at 127.0.0.1:18789
provider: ollama
Delivery: READY, pending=0, readOnly=true, stateChanged=false
Recovery: READY, readOnly=true, stateChanged=false
SQLite integrity: ok, tickets=11, ticket_events=86
Task-229 temporary task: absent
```

Already-exact truth table passed:

```text
mode=upgrade
pendingRollover=false
pluginAlreadyExact=true
installPlugin=false
rolloverPlugin=false
skipPlugin=false
```

Source and installed fingerprints both matched:

```text
e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
```

The candidate source contained the Task-226 repaired contract:

```text
pre-install backup project-tree attestation mismatch
```

## Historical evidence preservation

The Task-223 forensic evidence was hashed before and after the attempted registration:

```text
transaction:
ec1b32ec2813e1b4e2c220679f39c6922789b7d77e88ec9ca4ad6ba82ccac510

matching inventory:
1a7299f926cda4e3f936577204c50059e0e4e716f8594535d4b3c40c40e51477

ownership manifest:
081961df81f9bced0e4e72cf0bb4144e518e741ea9c010b4d7674404a1f247b6

backup project-tree:
7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a

backup payload fingerprint:
f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
```

All retained evidence hashes remained unchanged. The obsolete transaction was not finalized, edited, deleted, moved, renamed, archived, replaced, or reused.

## Registration attempts and exact failures

A unique temporary task name was used:

```text
CogentNexus-OpenClaw-Task229-Installer-Reentry-20260902T
```

Required direct action was prepared as:

```text
Execute:
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe

Arguments:
-NoLogo -NoProfile -ExecutionPolicy Bypass -File "C:\Users\CDQ-P\AppData\Local\Temp\cnx229-runner.ps1"

Principal:
CDQ-P / Interactive / Limited

ExecutionTimeLimit:
PT45M

RestartCount:
0
```

PowerShell Scheduled Task registration failed twice before task creation:

```text
New-ScheduledTaskSettingsSet : parameter AllowDemandStart not found
Register-ScheduledTask: no task created
```

and then:

```text
Register-ScheduledTask : The parameter is incorrect.
(15,8):UserId:
HRESULT 0x80070057
```

A native `schtasks.exe` equivalent was then attempted once after inspecting the qualified Task-215 identity/topology. It also failed before task creation:

```text
ERROR: The parameter is incorrect.
(40,4):UserId:
```

The final scheduler readback proved:

```text
TaskPresent=false
```

The registration helper itself was syntax-checked/written separately. No successful task registration, task start, runner process, or installer process occurred. Process matches observed during diagnostic probes were probe command lines themselves and no installer PID was started or terminated.

## Installer boundary

Not reached. Consequently there is no installer transcript, terminal completion evidence, cleanup action, or post-install lifecycle result for Task 229. The exact repaired `scripts/install.ps1` was not invoked.

The following mutation counts are therefore zero:

```text
openclaw plugins install: 0
rollover-prepare: 0
rollover-finalize: 0
rollover-plan/apply: 0
```

## Final preservation

After the failed registration attempts:

```text
controller: passthrough
generation: 33
Gateway: healthy
provider: ollama
Delivery: READY
Recovery: READY
SQLite integrity: ok
Task-229 temporary task: absent
retained evidence: unchanged
```

No manual cleanup was needed because no Task-229 task was created.

## Mutation ledger

```text
installer invocations: 0
Task-229 registrations: 0 successful
Task-229 starts: 0
Task-229 deletions: 0
openclaw plugins install: 0
rollover-prepare: 0
rollover-finalize: 0
manual cnxclaw lifecycle actions: 0
manual Gateway restarts: 0
manual stale-evidence writes/deletes/moves: 0
manual SQLite writes: 0
process terminations: 0
provider/model substitutions: 0
Discord Sends/API semantic traffic: 0
Release/tag/asset mutations: 0
product/source/test/workflow edits: 0
force pushes/history rewrites: 0
```

Disposable candidate validation and temporary helper/evidence files were external harness artifacts, not product/live mutations.

## Evidence paths

```text
candidate:
C:\Users\CDQ-P\AppData\Local\Temp\cnx229-source-exact-20260902T

preflight:
C:\Users\CDQ-P\AppData\Local\Temp\cnx229-preflight-20260902T

re-entry evidence:
C:\Users\CDQ-P\AppData\Local\Temp\cnx229-already-exact-reentry-20260902T

runner:
C:\Users\CDQ-P\AppData\Local\Temp\cnx229-runner.ps1

registration helper:
C:\Users\CDQ-P\AppData\Local\Temp\cnx229-register.ps1
```

## Stop boundary

```text
FAIL_TASK_REGISTRATION
```

Stop for independent review. Do not retry registration, invoke installer, repair scheduler identity, clean historical evidence, perform lifecycle/Gateway actions, or send Discord traffic without a new explicit authority.
