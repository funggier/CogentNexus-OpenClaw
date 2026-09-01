# CNX-20260901-214 — Task 213 Durable Windows Launcher Qualification

## Disposition

`PASS_DURABLE_SCHEDULED_TASK_LAUNCH__TERMINAL_PROPAGATION_UNPROVEN`

This task qualified only a harmless temporary Windows Scheduled Task launcher. It did not run the CogentNexus installer, OpenClaw lifecycle commands, Gateway actions, SQLite writes, or Discord traffic.

## Authority and scope

- Task: `CNX-20260901-214`
- Parent: `CNX-20260901-213`
- Branch: `agent/v0.9.3-full-stabilization`
- Scope: register one uniquely named temporary Scheduled Task, launch one harmless child through a synchronous wrapper, collect evidence, and unregister that exact task.
- Discord budget: `0`
- Installer/lifecycle budget: `0`

## Evidence root

`C:/Users/CDQ-P/AppData/Local/Temp/cnx214-durable-scheduled-launcher-20260901T/`

The initial registration probe failed before registration because Windows PowerShell rejected `InteractiveToken` as an invalid logon-type enum. The script was corrected to `Interactive`; no task existed from the failed attempt. A separate monitor probe also had a Bash/PowerShell quoting error (`$i` expansion); its output was discarded as harness evidence.

## Product preservation gate

Read-only preflight and post-state were unchanged:

- controller mode: `passthrough`
- generation: `33`
- startup adapter: `installed=false`
- live plugin fingerprint: `f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`
- Gateway: healthy, exit code `0`
- Delivery: `READY`, read-only, state unchanged
- Recovery: `READY`, read-only, state unchanged
- product process matches: `[]`
- selected provider: `ollama`
- SQLite integrity/mutation: no write performed

## Temporary task registration

One task was registered after the corrected script succeeded:

```text
CogentNexus-OpenClaw-Task214-Harness-20260901-1142-7f3c
```

Readback showed:

- state: `Ready`
- action executable: `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`
- action arguments: `-NoLogo -NoProfile -ExecutionPolicy Bypass -File "...cnx214...\wrapper.ps1"`
- execution limit: `PT5M`
- one-shot trigger, no repetition
- demand start allowed
- no product path or product command in the action

## Durable launch result

The task was started exactly once. The wrapper launched the harmless PowerShell child and waited for the child command using synchronous call syntax.

Observed child identity:

```text
pid: 19056
executable: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
start marker: CHILD_START
utc: 2026-09-01T12:09:33.9637999Z
```

Observed output:

- child identity JSON: written, `215` bytes
- child stdout: `114` bytes, UTF-16LE PowerShell output containing `CHILD_START`
- child stderr: `0` bytes
- child end marker: not found
- child exit-code file: not found
- Scheduler `LastTaskResult`: `1`
- Scheduler `NextRunTime`: `null`
- Scheduler `NumberOfMissedRuns`: `0`

The child was successfully created and produced its start marker, so the durable Scheduled Task launch boundary is proven. The child’s intended terminal marker and exit code were not captured. This is not evidence of installer failure or success, and it does not qualify Task 212’s installer terminal boundary.

## Cleanup

The exact temporary task was unregistered once and read back:

```text
UNREGISTER_REQUESTED=true
TASK_PRESENT=false
```

No broad task deletion or process termination was performed.

## Mutation ledger

```text
Temporary Scheduled Task registration: 1
Temporary Scheduled Task start: 1
Temporary Scheduled Task unregister: 1
Harmless child process: 1
CogentNexus installer: 0
OpenClaw lifecycle action: 0
Gateway restart: 0
Plugin/product mutation: 0
SQLite write: 0
Provider/model/config mutation: 0
Process termination: 0
Discord traffic: 0
Release/tag/asset mutation: 0
```

## Conclusion

Task 214 proves that a temporary Windows Scheduled Task can durably create the wrapper and child and can persist a start marker. It does not prove reliable terminal propagation, child exit-code collection, or a safe installer execution path. Any future installer qualification requires a separately authorized task with explicit terminal evidence requirements; no installer retry or Discord acceptance is authorized by this report.
