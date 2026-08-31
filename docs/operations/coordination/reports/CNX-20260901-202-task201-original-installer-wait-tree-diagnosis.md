# CNX-20260901-202 — Task 201 Original Installer Wait-Tree Diagnosis

- **Task:** `CNX-20260901-202`
- **Parent:** `CNX-20260901-201`
- **Authority branch:** `agent/v0.9.3-full-stabilization`
- **Fresh authority SHA:** `eee050f641878c63ba64250b86ff11102fe28cf6`
- **Frozen product candidate:** `9f4eaa429b2540540e7d6f6c2af99067960e45fb`
- **Expected installed plugin fingerprint:** `f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`
- **Evidence root:** `C:/Users/CDQ-P/AppData/Local/Temp/cnx202-wait-tree-20260901T`
- **Final outcome:** `EVIDENCE_ROOT_IDLE_NO_EXEC_DESCENDANT`

## Scope and authority

Fresh synchronization of `funggier/CogentNexus-OpenClaw` confirmed the live coordination state:

- `ACTIVE.md`: `READY_FOR_HERMES`
- `STATUS.md`: `READY_FOR_HERMES`
- active task: `CNX-20260901-202`
- Task-201 accepted disposition: `BLOCKED_INSTALLER_STILL_RUNNING`
- Task-201 report/review are present on the fresh authority
- published v0.9.3 remains immutable at `26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task 202 is read-only process-tree diagnosis. No process termination, lifecycle control, installer replay, state/config/SQLite mutation, provider/model change, Discord Send, source edit, diagnostic software installation, Release/tag mutation, or force push was performed.

## Phase A — identity and retained stream boundary

The original Task-200 installer identity was:

```text
root PowerShell PID: 11704
known conhost PID: 11588
retained PID 11704 creation time: \/Date(1788193889192)\/
```

At sample 1, PID 11704 was:

```text
pid: 11704
ppid: 3448
name: powershell.exe
exe: C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe
cmdline: ["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"]
create_time: 1788193889.192804
status: running
num_threads: 9
num_handles: 620
cpu_times: user 0.15625, system 0.25
```

At sample 2, PID 11704 remained:

```text
pid: 11704
ppid: 3448
name: powershell.exe
exe: C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe
cmdline: ["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"]
create_time: 1788193889.192804
status: running
num_threads: 9
num_handles: 620
cpu_times: user 0.15625, system 0.25
```

The creation time exactly matches the retained identity. This is the same original process, not PID reuse.

The known console process was:

```text
pid: 11588
ppid: 11704
name: conhost.exe
exe: C:\\Windows\\System32\\conhost.exe
cmdline: ["\\\\??\\\\C:\\Windows\\system32\\conhost.exe", "0x4"]
create_time: 1788193889.2027566
status: running
num_threads: 3
num_handles: 271
cpu_times: user 0.078125, system 0.140625
```

Retained installer streams were unchanged from the Task-201 adjudication:

```text
stdout length: 7824
stdout sha256: 6a00dbca75456b46d256ba452b5a4fd48df31502f712d57d72b24faea8e47ff2
stdout mtime UTC: 2026-08-31T17:09:43.945230+00:00

stderr length: 1902
stderr sha256: 703f465b6f4a5d82deb55f085f44fc50c4dfc794f359c6491df8963bd4ec94fa
stderr mtime UTC: 2026-08-31T17:09:35.418339+00:00
```

## Phase B — complete recursive process tree

The process table was captured read-only and the descendant tree was built recursively from parent PID relationships. Both samples produced the same complete tree:

```json
{
  "rootPid": 11704,
  "treePids": [11704, 11588],
  "root": 11704,
  "descendants": [11588]
}
```

No surviving descendant matched any of the task's execution-boundary patterns:

```text
candidate-owned Python: none
cnxclaw_v093.py: none
cnxclaw.py: none
host_control*.py: none
host_v*.py: none
node.exe/openclaw: none
cmd.exe: none
Gateway-related child: none
Scheduled Task helper child: none
```

The only descendant was console infrastructure (`conhost.exe`). No Python, Node, OpenClaw, Host, Gateway, CLI, or nested command process survived below the original PowerShell root at either sample.

Raw complete sample files:

```text
sample-1.json
sample-2.json
```

## Phase C — two bounded progress samples

The samples were captured by a read-only `psutil` collector with a 35-second sleep between captures. Actual timestamps:

```text
sample 1: 2026-08-31T17:54:55.506419+00:00
sample 2: 2026-08-31T17:55:32.038541+00:00
interval: 36.532122 seconds
```

The terminal-to-terminal wall interval was approximately 37.53 seconds including collection time.

| Field | Sample 1 | Sample 2 | Delta |
|---|---:|---:|---:|
| Root PID | 11704 | 11704 | unchanged |
| Root creation time | 1788193889.192804 | 1788193889.192804 | unchanged |
| Root status | running | running | unchanged |
| Root threads | 9 | 9 | 0 |
| Root handles | 620 | 620 | 0 |
| Root CPU user | 0.15625 | 0.15625 | 0 |
| Root CPU system | 0.25 | 0.25 | 0 |
| conhost PID | 11588 | 11588 | unchanged |
| Tree PIDs | `[11704,11588]` | `[11704,11588]` | unchanged |
| stdout length | 7824 | 7824 | 0 |
| stdout SHA-256 | `6a00dbca75456b46d256ba452b5a4fd48df31502f712d57d72b24faea8e47ff2` | same | unchanged |
| stderr length | 1902 | 1902 | 0 |
| stderr SHA-256 | `703f465b6f4a5d82deb55f085f44fc50c4dfc794f359c6491df8963bd4ec94fa` | same | unchanged |
| stdout/stderr mtimes | unchanged | unchanged | unchanged |

The root's memory values changed only by a small observation-level amount while the recorded CPU, handles, thread count, process identity, tree membership, and streams remained unchanged. This does not establish a deadlock and no deadlock claim is made.

### Collector harness issues

Two collector attempts failed before producing sample evidence:

1. PowerShell collector used `$pid`, which collides case-insensitively with PowerShell's read-only automatic `$PID` variable.
2. The corrected PowerShell collector then hit `Argument types do not match` during its generic collection construction and timed out without writing a sample.

These are harness errors only. They did not mutate live state, kill processes, or alter installer streams. The final Python/psutil collector was written as a read-only replacement and completed both bounded samples successfully.

## Phase D — source-boundary correlation

The exact authoritative installer source contains the next command after the completed `owned-runtime-ensure` boundary:

```text
scripts/install.ps1:486-489

if (-not $SkipGatewayRestart) {
    & $ownedPython $cliScript --root $cogentNexusOpenClawRoot enable
    if ($LASTEXITCODE -ne 0) { throw "CogentNexus-OpenClaw Host enable failed" }
}
```

The retained stdout proves `owned-runtime-ensure` completed, launcher write completed, and passthrough policy output was emitted. It does not contain an `enable` result or final installer completion line.

The current process tree contains no surviving `$ownedPython`, `cnxclaw_v093.py`, Host, OpenClaw, Node, Gateway, or command-shell descendant. Therefore the deepest evidence-supported statement is:

```text
Original PowerShell remains alive after the retained passthrough-policy boundary;
no executable descendant remains to identify an active enable/Host/OpenClaw wait boundary.
```

The evidence does **not** prove whether PowerShell is waiting to invoke `enable`, waiting on an internal stream/process primitive, or in another unobservable internal state. No such internal cause is claimed. The prior Windows wait-API hypothesis remains only a hypothesis.

## Phase E — independent current health snapshot

All current probes were read-only and returned exit code `0`.

### Host and installed identity

```text
Host mode: passthrough
Desired Gateway: running
Selected provider: ollama
Generation: 28
Startup policy: disabled
Startup adapter installed: false
Plugin inventory: cogentnexus-openclaw 0.9.3, enabled=false/status=disabled
Installed plugin root: C:\\Users\\CDQ-P\\.openclaw\\extensions\\cogentnexus-openclaw
```

The installed fingerprint probe returned the expected repaired candidate fingerprint:

```text
f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
```

### Gateway and provider

```text
OpenClaw: 2026.7.1-2 (0790d9f)
Gateway: healthy
Gateway bind: 127.0.0.1:18789
Connectivity probe: ok
Ollama: installed/reachable/healthy/ready
Models: qwen3.5:9b, muse-glimmer:30b, qwen3.6:27b, qwen3.8:27b
```

### Delivery, recovery, and SQLite

```text
delivery verdict: READY
pending terminal deliveries: 0
recovery verdict: READY
maintenance marker: none
active Ollama recovery incident: false
recovery attempts: 0
SQLite integrity_check: ok
```

Read-only SQLite counts:

```text
tickets: 10
ticket_events: 79
cnx_direct_model_call: 10
cnx_direct_recovery: 0
cnx_assistant_delivery: 7
ticket_outbox: 0
cnx_sessions: 19
```

No new Ticket, model call, delivery, recovery record, outbox row, or Discord action was created by Task 202.

## Analysis matrix

| Required outcome | Result | Evidence |
|---|---|---|
| Exact original PID identity | PASS | PID/PPID/executable/command line/creation time match |
| Complete recursive tree | PASS | `[11704,11588]` at both samples |
| Python/Node/OpenClaw descendant | NOT FOUND | no matching descendant in either sample |
| Two bounded samples | PASS | 36.532-second sample timestamp interval |
| Root CPU progress | NONE OBSERVED | CPU times unchanged |
| Tree progress | NONE OBSERVED | same PIDs and identities |
| Stream progress | NONE OBSERVED | same size/hash/mtime |
| Specific child boundary | NOT IDENTIFIED | no execution descendant remains |
| Current Gateway/Ollama health | PASS | all read-only probes exit 0 and semantic checks pass |
| Current managed convergence | NOT READY | passthrough/startup disabled/plugin disabled |
| Discord Send | NOT PERFORMED | Task 202 forbids it; budget remains 0/1 |

The correct allowed final outcome is:

```text
EVIDENCE_ROOT_IDLE_NO_EXEC_DESCENDANT
```

This establishes an orphaned/root-wait shape: the exact original PowerShell remains alive, the streams are unchanged, and no meaningful execution descendant remains besides console infrastructure. It does **not** prove the internal PowerShell wait primitive or establish a product root cause.

## Mutation ledger

```text
process kill/termination/suspend: 0
installer replay: 0
enable/disable/start/stop/restart: 0
reset/uninstall/reinstall/install-over: 0
Gateway/provider/OpenClaw/Ollama lifecycle: 0
state/config/Scheduled Task/SQLite mutation: 0
provider/model selection change: 0
Discord Send: 0 / 1
Discord injection/synthetic traffic: 0
source/test/workflow edit: 0
diagnostic software installation: 0
Release/tag/asset mutation: 0
force push: 0
```

Evidence-only files created outside live deletion roots:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx202-wait-tree-20260901T/sample-1.json
C:/Users/CDQ-P/AppData/Local/Temp/cnx202-wait-tree-20260901T/sample-2.json
C:/Users/CDQ-P/AppData/Local/Temp/cnx202-wait-tree-20260901T/health-*.{stdout,stderr,exit}
C:/Users/CDQ-P/AppData/Local/Temp/cnx202-capture-psutil.py
```

No credentials, tokens, passwords, or connection strings were recorded.

## Final disposition

```text
EVIDENCE_ROOT_IDLE_NO_EXEC_DESCENDANT
```

Per the Task-202 stop rule, no cleanup, live repair, Discord requalification, or source diagnosis was attempted. Further action requires a separate reviewed successor task.
