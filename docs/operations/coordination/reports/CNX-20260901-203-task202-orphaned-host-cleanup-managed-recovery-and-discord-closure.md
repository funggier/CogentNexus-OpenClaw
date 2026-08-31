# CNX-20260901-203 — Task 202 Orphaned Host Cleanup, Managed Recovery, and Discord Closure

- **Task:** `CNX-20260901-203`
- **Parent:** `CNX-20260901-202`
- **Authority branch:** `agent/v0.9.3-full-stabilization`
- **Fresh authority SHA:** `f3be4a03b2058e3f8f53d0d35f12d809b9dfd255`
- **Frozen product candidate:** `9f4eaa429b2540540e7d6f6c2af99067960e45fb`
- **Expected installed fingerprint:** `f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`
- **Evidence root:** `C:/Users/CDQ-P/AppData/Local/Temp/cnx203-recovery-20260901T`
- **Final disposition:** `FAIL_PRE_ENABLE_HEALTH`

## Summary

Task 203 completed the authorized exact orphan cleanup, then stopped at the pre-enable health gate. The stale Task-200/202 PowerShell root PID `11704` was revalidated against retained creation-time identity and idle/no-executable-descendant evidence, then terminated once. PID `11704` and its associated console host `11588` were subsequently absent.

The post-cleanup pre-enable read-only scan discovered a separate active historical reset lifecycle tree:

```text
PID 9840  python.exe -> host_control_v092.py reset --provider ollama
└── PID 17360 python.exe -> host_control_v092.py reset --provider ollama
```

This is not the stale PID authorized for cleanup. Task 203 does not authorize broad process termination or cleanup of this reset tree. Because a live lifecycle process is present, the pre-enable state is not sufficiently coherent/safe for the one-shot `enable` transition. Enable was not invoked and no Discord message was sent.

No product root cause is claimed for the remaining reset tree.

## Authority and hard-fence compliance

Fresh GitHub sync confirmed:

- `ACTIVE.md`: `READY_FOR_HERMES`;
- `STATUS.md`: `READY_FOR_HERMES`;
- active task: `CNX-20260901-203`;
- Task-202 accepted result: `EVIDENCE_ROOT_IDLE_NO_EXEC_DESCENDANT`;
- Task-203 allows one exact stale-root cleanup, one enable only after a coherent pre-enable gate, and one human Discord Send only after managed convergence;
- public v0.9.3 remains immutable at `26ce64a624255278a3a0266ad38746e0e6ed2e31`.

Forbidden actions not performed:

```text
installer replay: 0
reset/uninstall/reinstall/install-over: 0
second enable: 0
disable/start/stop/restart: 0
broad process kill: 0
reset-process cleanup: 0
provider/model/config/SQLite manual mutation: 0
source/test/workflow edit: 0
Release/tag/asset mutation: 0
force push: 0
Discord Send: 0 / 1
retry/regenerate/injection/second message: 0
```

Authorized orphan cleanup performed exactly once:

```text
Stop-Process -Id 11704 -Force
```

## Phase A — final stale-root fence

Fresh pre-kill samples were captured at:

```text
2026-08-31T18:16:43.769191+00:00
2026-08-31T18:17:05.227395+00:00
```

The process tree at both samples was:

```text
11704 powershell.exe
└── 11588 conhost.exe
```

PID `11704` matched the accepted identity:

```text
PID: 11704
PPID: 3448
name: powershell.exe
exe: C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe
command line: C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe
creation time: 1788193889.192804
status: running
threads: 9
handles: 620
CPU: user 0.15625, system 0.25
```

The retained installer streams were unchanged in both samples:

```text
stdout length: 7824
stdout SHA-256: 6a00dbca75456b46d256ba452b5a4fd48df31502f712d57d72b24faea8e47ff2
stdout mtime UTC: 2026-08-31T17:09:43.945230+00:00

stderr length: 1902
stderr SHA-256: 703f465b6f4a5d82deb55f085f44fc50c4dfc794f359c6491df8963bd4ec94fa
stderr mtime UTC: 2026-08-31T17:09:35.418339+00:00
```

The root CPU time, thread count, handle count, creation time, tree membership, and stream values did not change. No Python, Node, OpenClaw, Host, Gateway, installer, `cnxclaw`, or other executable work descendant was present.

The exact repaired installed fingerprint and ownership passed before cleanup:

```text
fingerprint: f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
installed version: 0.9.3
plugin ID: cogentnexus-openclaw
```

Host was still `passthrough`, startup/plugin disabled, Gateway/Ollama healthy, delivery/recovery ready, and SQLite integrity `ok`.

## Phase B — exact orphan cleanup

Cleanup began at:

```text
2026-08-31T18:17:44Z
```

The exact command was:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Stop-Process -Id 11704 -Force -ErrorAction Stop"
```

Result:

```text
exit code: 0
```

Read-only post-cleanup identity check at `2026-08-31T18:17:46Z`:

```json
{
  "11704": {"exists": false},
  "11588": {"exists": false}
}
```

The disappearance of `11588` is recorded as the associated console-host consequence. No separate console process was terminated. No unrelated process was targeted.

## Phase C — pre-enable health gate

Post-cleanup read-only probes returned exit code `0`:

```text
installed fingerprint: exact expected repaired candidate
ownership verify: PASS
Host mode: passthrough
startup policy: disabled
plugin state: disabled
Gateway: healthy/listening at 127.0.0.1:18789
Ollama: installed/reachable/healthy/ready
Delivery: READY; pending outbox 0
Recovery: READY; active incident false; recovery attempts 0
SQLite integrity: ok
```

Durable counts remained:

```text
tickets: 10
ticket_events: 79
cnx_direct_model_call: 10
cnx_direct_recovery: 0
cnx_assistant_delivery: 7
ticket_outbox: 0
cnx_sessions: 19
```

### Blocking process residue

The independent post-cleanup process scan found a separate historical reset lifecycle:

```text
PID 9840
PPID 10724
name: python.exe
exe: C:\\Users\\CDQ-P\\AppData\\Local\\CogentNexus-OpenClaw\\runtime\\python\\Scripts\\python.exe
creation time: 1788186963.6185184
status: running
threads: 1
handles: 57
command line:
C:\\Users\\CDQ-P\\AppData\\Local\\CogentNexus-OpenClaw\\runtime\\python\\Scripts\\python.exe C:\\Users\\CDQ-P\\.openclaw\\workspace\\skills\\cogentnexus-openclaw\\scripts\\host_control_v092.py --root C:\\Users\\CDQ-P\\.openclaw\\workspace\\.cogentnexus-openclaw reset --provider ollama
```

Its surviving child was:

```text
PID 17360
PPID 9840
name: python.exe
exe: C:\\Users\\CDQ-P\\AppData\\Roaming\\uv\\python\\cpython-3.11.15-windows-x86_64-none\\python.exe
creation time: 1788186963.6370635
status: running
threads: 1
handles: 135
command line:
C:\\Users\\CDQ-P\\AppData\\Roaming\\uv\\python\\cpython-3.11.15-windows-x86_64-none\\python.exe C:\\Users\\CDQ-P\\.openclaw\\workspace\\skills\\cogentnexus-openclaw\\scripts\\host_control_v092.py --root C:\\Users\\CDQ-P\\.openclaw\\workspace\\.cogentnexus-openclaw reset --provider ollama
```

The tree was captured read-only. Both processes were left untouched because Task 203 authorizes termination only of the exact stale root PID `11704` and explicitly forbids broad process kills. PID `9840`/`17360` are not relabeled as the Task-200 installer and are not claimed as a root cause.

The presence of an active lifecycle tree means the product is not a clean/coherent pre-enable boundary for Task 203. It is unsafe to invoke the one permitted enable while another lifecycle operation against the same state root remains live. The task therefore stops with:

```text
FAIL_PRE_ENABLE_HEALTH
```

## Phase D — enable

Not performed.

```text
enable invocation count: 0 / 1
```

No `cnxclaw.cmd enable` was invoked. No enable exit code, managed convergence, plugin activation, startup readiness, or post-enable state is claimed.

## Phase E/F/G — Discord and final convergence

Not performed because the pre-enable gate failed.

```text
nonce: not generated
Discord prompt: not issued
human Send: 0 / 1
Ticket/model/delivery correlation: not applicable
final managed health: not claimed
```

The existing Discord session budget remains unused:

```text
agent:main:discord:channel:1531199905673252946
human Send consumed: 0 / 1
```

## Issue register

### I-01 — Authorized stale orphan removed

- **Observed:** exact PID `11704` matched retained identity and idle/no-descendant evidence.
- **Action:** terminated once under Task 203 authorization.
- **Result:** PID `11704` absent; associated `conhost.exe` PID `11588` also absent.
- **Product impact:** stale executor boundary removed; no installer replay performed.

### I-02 — Separate historical reset lifecycle remains active

- **Observed:** PIDs `9840` and `17360` execute `host_control_v092.py ... reset --provider ollama` against the same CogentNexus state root.
- **Classification:** active process residue / pre-enable safety conflict.
- **Root cause:** not proven; no causal claim is made.
- **Action:** no kill, cleanup, or lifecycle interaction because Task 203 forbids broad process termination and authorizes only PID `11704`.
- **Consequence:** managed recovery was not started; Discord Send was not authorized.

### I-03 — Current Host is still passthrough

- **Observed:** Host mode `passthrough`, startup policy disabled, plugin disabled.
- **Classification:** expected pre-enable baseline, but not sufficient while the reset tree remains live.
- **Consequence:** no enable invocation under this task.

### I-04 — Health probes are green but do not override lifecycle conflict

- **Observed:** Gateway/Ollama/delivery/recovery/SQLite probes pass.
- **Classification:** healthy infrastructure baseline, not proof of a safe managed transition.
- **Consequence:** no upgrade of `FAIL_PRE_ENABLE_HEALTH` to enable or Discord acceptance.

## Final disposition

```text
FAIL_PRE_ENABLE_HEALTH
```

Task 203 performed exactly the authorized stale-root cleanup and then stopped before enable because an independent active historical reset lifecycle was present. No second process was killed, no enable was attempted, no Discord message was sent, and no source/config/product change was made.

## Evidence manifest

```text
cnx203-prekill.py
prekill-1.json
prekill-2.json
cleanup.exit
cleanup-post.json
pre-*.stdout
pre-*.stderr
pre-*.exit
read-only process scan captured in task execution output
```

No credentials, tokens, passwords, or connection strings were recorded.
