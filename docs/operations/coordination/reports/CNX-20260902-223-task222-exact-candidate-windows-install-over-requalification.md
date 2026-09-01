# CNX-20260902-223 — Exact Candidate Windows Install-Over Requalification

Date: 2026-09-02 ICT  
Primary disposition: `FAIL_INSTALLER_TERMINAL`  
Parent: `CNX-20260901-222`  
Executor: Hermes / authenticated Windows operator  
Coordinator / final reviewer: ChatGPT

## Executive result

Task 223 consumed the single authorized Windows installer invocation through a direct PowerShell Scheduled Task topology. The candidate package was proven exact before launch and the installer successfully reached plugin installation, but the final ownership-safe plugin generation rollover finalization failed.

The task therefore fails closed as:

```text
FAIL_INSTALLER_TERMINAL
```

The installer was not retried. No manual lifecycle repair, manual finalize, uninstall, reset, fresh reinstall, Gateway restart, or Discord traffic was performed.

## Authority and exact candidate

Fresh remote authority was read from `agent/v0.9.3-full-stabilization` before execution.

Task 223 authority:

```text
Task ID: CNX-20260902-223
Execution mode: TASK223_EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFICATION
Status: READY_FOR_HERMES
```

Exact source candidate:

```text
a812f27815b3c87b7ca748dc2dea88f987601f70
```

Accepted package identity:

```text
artifact: 9810139538
artifact digest: sha256:3164b7770e7d8991691d7bbedced092866c208add72b0c03b4aa3d39d1b50ff0
payload files: 192
payload fingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
tar.gz: 88f1c81d5c68da11e7420388a215bf8b72c55a30e7924f24cf6a83b8912a7494
zip: 011aaff51462c47440d973a348b938b12a3c2aadcbbe436acf5d54d9f2ad003d
```

Public `v0.9.3` remained immutable at `26ce64a624255278a3a0266ad38746e0e6ed2e31`.

## Phase A — preflight

Fresh read-only preflight before candidate materialization showed:

```text
controller mode: passthrough
generation: 33
selected provider: ollama
desired provider: unchanged
startup adapter: installed=false
Gateway: healthy, loopback 127.0.0.1:18789, exitCode=0
Ollama: reachable/healthy/ready
Delivery: READY, pending terminal deliveries 0, readOnly=true, stateChanged=false
Recovery: READY, no active maintenance marker or provider recovery incident
SQLite: integrity_check = ok
Task-223 temporary task: absent
```

The historical Task-205 cancelled/inert state remained represented by the preflight ticket counts (`cancelled=2`, `completed=9`) and no new Discord/API semantic traffic was emitted.

No source/product/test/workflow drift was found newer than the accepted Task-222 candidate other than coordination files.

## Phase B/C — exact-first candidate provenance

Disposable candidate root:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx223-candidate-exact-ac2v1jud\repo
```

The candidate was selected before working-tree materialization:

```text
git clone --no-tags --no-checkout https://github.com/funggier/CogentNexus-OpenClaw.git <root>\repo
git checkout --detach a812f27815b3c87b7ca748dc2dea88f987601f70
```

Immediate checkout had the inherited Windows Git policy (`core.autocrlf=true`), guarded attributes `text eol=lf`, LF working-tree bytes for all four static identity files, and clean status.

Candidate preparation passed:

```text
npm ci: PASS
npm run plugin:validate: PASS
packedFileCount: 192
plugin payload identity: {"fileCount":192,"fingerprint":"e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386","version":"0.9.3"}
second dist canonicalizer pass: canonicalized 0 dist text files to LF
```

The installer path was read from this exact candidate root:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx223-candidate-exact-ac2v1jud\repo\scripts\install.ps1
```

## Phase D — Scheduled Task registration

External evidence root:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx223-install-over-20260902T
```

Runner:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx223-runner.ps1
```

Temporary task:

```text
CogentNexus-OpenClaw-Task223-Installer-c829c321
```

Readback before start proved:

```text
Execute: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
Arguments: -NoLogo -NoProfile -ExecutionPolicy Bypass -File "C:\Users\CDQ-P\AppData\Local\Temp\cnx223-runner.ps1"
Principal: CDQ-P / Interactive / Limited
ExecutionTimeLimit: PT45M
AllowDemandStart: true
RestartCount: 0
```

Two registration attempts failed before task creation due Windows PowerShell parameter resolution (`InteractiveToken` unsupported, then unresolved short UserId). The successful registration used `Interactive` and `CDQ-P\CDQ-P`; these pre-registration failures consumed no installer invocation and created no task.

## Phase E — single installer invocation and terminal evidence

The temporary task was started exactly once. An initial wrapper command failed before `Start-ScheduledTask` because it did not pass the task-name environment variable; no start occurred in that attempt. The subsequent direct `Start-ScheduledTask` command started the task once.

Observer evidence:

```text
Task start count: 1
Running observations: polls 1 through 17
Terminal observation: poll 18, State=Ready
LastTaskResult: 1
```

Runner stage evidence:

```text
RUNNER_START utc=2026-09-01T22:52:05.2010906+00:00 pid=5960
RUNNER_FAILURE utc=2026-09-01T23:00:36.5046815+00:00 pid=5960
error=ownership-safe plugin generation rollover finalization failed
```

PowerShell transcript:

```text
Host: Windows PowerShell 5.1.19041.6456
Process ID: 5960
Start: 2026-09-02 05:52:05 local / 2026-09-01T22:52:05Z-ish evidence timestamp
Terminal: 2026-09-02 06:00:36 local
```

Installer stage ledger:

```text
 ticket-db-bootstrap: START + COMPLETE, exit_code=0
 plugin-npm-pack: START + COMPLETE, exit_code=0
 plugin-rollover-prepare: START + COMPLETE, exit_code=0
 plugin-install-local-package: START + COMPLETE, exit_code=0
 plugin-disable-post-install: START + COMPLETE, exit_code=0
 plugin-rollover-finalize: START + COMPLETE, exit_code=1
```

The transcript contains no final `installation completed successfully` marker. Therefore the required installer terminal success condition was not met.

The installer log also records:

```text
Installed plugin: cogentnexus-openclaw
Restart the gateway to load plugins.
```

The rollover transaction created by this attempt recorded:

```text
expectedReplacementFingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
retiredFingerprint: f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
controllerMode: passthrough
createdAt: 2026-09-01T22:59:52.821454+00:00
```

The finalization failure is preserved as the first and only installer failure. No retry was attempted.

## Phase F — temporary task cleanup

After terminal evidence, only the exact temporary Task-223 task was unregistered:

```text
UNREGISTER_REQUESTED=true
TaskPresent=false
```

No product startup task was altered. Known installer/runner PIDs (`5960`, observer `3392`) were absent on the bounded PID check. No process was terminated.

The external evidence root and installer transcript were retained.

## Phase G — post-install read-only state

Installed plugin identity readback showed:

```text
plugin id: cogentnexus-openclaw
version: 0.9.3
installed fingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
plugin path: C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw
```

Ownership verification returned exit 0 and the installed plugin payload fingerprint matched the accepted candidate. However, the installer did not reach successful rollover finalization, and its latest transaction JSON remains in the install-staging area. This is unresolved transaction evidence, not a basis for PASS and not something this task may manually repair.

Post-install read-only health remained:

```text
controller: passthrough, generation 33
startup adapter: installed=false
Gateway: healthy, exitCode=0, PID 9696, listener 127.0.0.1:18789
provider: ollama, reachable/healthy/ready
Delivery: READY, pending 0, readOnly=true, stateChanged=false
Recovery: READY, no active provider recovery incident
SQLite: integrity_check = ok
```

The installed fingerprint match is recorded separately from the failed installer terminal result. Runtime health being healthy does not override the missing installer success/finalization evidence.

## Mutation ledger

```text
installer invocations: 1
Task-223 registrations: 1
Task-223 starts: 1
Task-223 deletions: 1
manual cnxclaw lifecycle actions: 0
manual Gateway restarts: 0
manual plugin/config mutations outside installer: 0
manual SQLite/ownership/staging writes: 0
process terminations: 0
provider/model substitutions: 0
Discord Sends/API semantic traffic: 0
Release/tag/asset mutations: 0
product/source/test/workflow commits during Task 223: 0
```

The installer itself performed the authorized install-over mutations before the finalization failure. No additional mutation was performed by Hermes after the failure.

## Evidence paths

```text
Preflight:
C:\Users\CDQ-P\AppData\Local\Temp\cnx223-preflight-20260902T.txt

Candidate source:
C:\Users\CDQ-P\AppData\Local\Temp\cnx223-candidate-exact-ac2v1jud\repo

Runner:
C:\Users\CDQ-P\AppData\Local\Temp\cnx223-runner.ps1

Observer:
C:\Users\CDQ-P\AppData\Local\Temp\cnx223-observer.ps1

Install evidence:
C:\Users\CDQ-P\AppData\Local\Temp\cnx223-install-over-20260902T\runner-stage.log
C:\Users\CDQ-P\AppData\Local\Temp\cnx223-install-over-20260902T\installer-transcript.txt
C:\Users\CDQ-P\AppData\Local\Temp\cnx223-install-over-20260902T\observer.log

Latest rollover transaction:
C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\install-staging\plugin-rollover-transaction-8469daf5669242189f18e8c87ed9a86c.json
```

## Final decision

```text
FAIL_INSTALLER_TERMINAL
```

This report intentionally stops without retry or manual recovery. A successor task must explicitly adjudicate the unresolved rollover-finalization state before any further installer, lifecycle, or Discord action. Discord remains at zero Sends.
