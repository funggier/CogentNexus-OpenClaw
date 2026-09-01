# CNX-20260901-215 — Direct Scheduled Task Terminal Propagation Qualification

## Disposition

`PASS_DIRECT_SCHEDULED_TASK_TERMINAL_PROPAGATION`

Task 215 was harness-only. It used one temporary Windows Scheduled Task running one harmless PowerShell script directly. No CogentNexus installer, OpenClaw lifecycle action, Gateway restart, plugin mutation, SQLite write, provider/model change, or Discord traffic occurred.

## Authority and evidence

- Task: `CNX-20260901-215`
- Parent: `CNX-20260901-214`
- Evidence root: `C:/Users/CDQ-P/AppData/Local/Temp/cnx215-direct-scheduled-terminal-20260901T/`
- Temporary task: `CogentNexus-OpenClaw-Task215-Direct-20260901-1210-4a91`

## Product preservation

Fresh preflight and postflight were successful:

- mode: `passthrough` -> `passthrough`
- generation: `33` -> `33`
- selected provider: `ollama` -> `ollama`
- Gateway: healthy in both snapshots
- startup adapter: installed=false in both snapshots
- live plugin fingerprint: `f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`
- pre/post delivery and recovery checks: exit `0`; `READY`; read-only; state unchanged
- no product process residue observed

## Direct task definition

The readback proved a direct action with no wrapper:

```text
Execute: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
Arguments: -NoLogo -NoProfile -ExecutionPolicy Bypass -File "...\cnx215-direct-scheduled-terminal-20260901T\direct.ps1"
ExecutionTimeLimit: PT3M
AllowDemandStart: true
RestartCount: 0
Principal: CDQ-P / Interactive / Limited
```

The task was registered once and started once.

## Runtime and terminal evidence

Direct child identity:

```text
PID: 3460
Executable: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
Creation UTC: 2026-09-01T12:49:02.7089851Z
Marker: DIRECT_START
```

The task remained `Running` at the 10, 30, and 60 second observations. The script persisted 11 heartbeat records through the intended 55-second interval:

```text
DIRECT_HEARTBEAT n=1..11
```

Terminal evidence:

```text
DIRECT_END UTC: 2026-09-01T12:49:57.8803017Z
Elapsed: 55.1713166 seconds
intended-exit-code.txt: 23
Scheduler at 70s: Ready
Scheduler LastTaskResult: 23
NumberOfMissedRuns: 0
```

This directly qualifies terminal propagation without the nested wrapper/child confounder from Task 214.

## Cleanup

The exact task was unregistered once:

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
Harmless direct child: 1
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

The direct Windows Scheduled Task execution model is qualified for sustained execution and terminal exit-code propagation in this environment. This report does not itself authorize installer execution; a separate successor authority is required for Task-207 installer requalification.
