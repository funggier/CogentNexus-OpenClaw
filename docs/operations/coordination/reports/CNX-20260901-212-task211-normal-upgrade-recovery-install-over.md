# CNX-20260901-212 — Task-211 Normal-Upgrade Recovery Install-Over

Date: 2026-09-01 ICT  
Task: `CNX-20260901-212`  
Parent: `CNX-20260901-211`  
Branch: `agent/v0.9.3-full-stabilization`

## Disposition

`BLOCKED_INSTALLER_TERMINAL`

The exact Task-207 candidate passed the package/fingerprint preflight. The newly authorized installer was launched exactly once in a detached native PowerShell process and the recorded root PID later disappeared naturally. However, stdout and stderr remained empty, no installer stage marker was emitted, and no terminal exit code or success/failure line was retained. This is an unproven installer terminal boundary, not PASS and not a proven installer failure. The installer launch is consumed; no retry or compensating lifecycle action was performed.

## Evidence root

`C:/Users/CDQ-P/AppData/Local/Temp/cnx212-task211-normal-upgrade-install-20260901T`

Key artifacts:

- `a00-captured-at-utc.txt`
- `a01-status.json`, `a02-delivery.json`, `a03-recovery.json`
- `a04-live-fingerprint.json`
- `a05-preflight-summary.json`
- `b05-installer-launch.json`
- `b03-installer.stdout`, `b04-installer.stderr`
- `b06-installer-samples.json`
- `c01-post-status.json`, `c02-post-delivery.json`, `c03-post-recovery.json`
- `c04-post-live-fingerprint.json`
- `c05-post-process.json`, `c06-clean-process-scan.json`, `c07-sqlite-ro.json`
- `launch-installer.py`, `monitor-installer.py`

## Authority and candidate gate

Fresh coordination authority was read from remote branch tip:

```text
0e6f8042e86fcffdffe2cc7b6828686624dbe660
```

The immutable product candidate was:

```text
commit: 27fe0181b3b65d555a3b0cc8354f6f7945c21c0b
artifact: 9790881384
artifact digest: sha256:1733897690890f9adcb12176b79db2b43e27799a4022743c4597fad44d2d5a34
candidate plugin fingerprint: d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b
payload files: 192
zip SHA-256: 0321028fc6214e18dbc965ad79a6d04328a05a84dce6a9efc058fb1122237986
tar.gz SHA-256: 0ab3884621a518b4cfd46949e3c8e3e7f9f52995bee257743960dd7636794dcf
```

The exact candidate fingerprint was computed from the verified package payload and matched the authority value. The live pre-install fingerprint was independently captured as:

```text
f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
```

## Preflight

Fresh read-only preflight reproduced the accepted Task-211 ordinary same-version upgrade boundary:

```text
controller mode: passthrough
generation: 33
startup policy: disabled
startup adapter installed: false
Gateway: healthy
selected provider: ollama
Delivery: READY
Recovery: READY
live plugin fingerprint: f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
```

Task-205 cancelled recovery remained inert. No unrelated installer/lifecycle process was proven after excluding the current observer ancestry and evidence-root self matches.

## One-shot installer launch

The installer was launched exactly once by a detached Python child using native absolute paths:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:/Users/CDQ-P/AppData/Local/Temp/cnx-successor-204-authority-20260901T/scripts/install.ps1 -Workspace C:/Users/CDQ-P/.openclaw/workspace
```

Launch record:

```text
root PID: 21836
started: 2026-09-01T10:52:23.957+00:00
stdout: C:\Users\CDQ-P\AppData\Local\Temp\cnx212-task211-normal-upgrade-install-20260901T\b03-installer.stdout
stderr: C:\Users\CDQ-P\AppData\Local\Temp\cnx212-task211-normal-upgrade-install-20260901T\b04-installer.stderr
detached: true
```

The detached launcher watcher returned successfully after persisting the launch record. A separate monitor observed the exact PID. The PID was no longer present on the first bounded sample approximately 27 seconds later. The process was not killed.

Terminal evidence:

```text
stdout bytes: 0
stderr bytes: 0
stage START markers: 0
stage COMPLETE markers: 0
terminal success line: absent
terminal failure line: absent
installer exit code: unavailable
natural PID disappearance: observed
```

Because the installer emitted no stage or terminal evidence at all, natural PID disappearance alone cannot prove that the documented installer body ran or completed. The PID was subsequently observed as reused by a bash observer shell in a separate broad scan; that self-match was excluded from the clean scan and is recorded as harness evidence, not installer residue.

## Post-install read-only state

The live plugin fingerprint remained the old value:

```text
f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
```

There is no evidence that the Task-207 candidate fingerprint became installed. Read-only controller state remained:

```text
mode: passthrough
generation: 33
startup adapter: installed=false
Gateway: healthy
Delivery: READY
Recovery: READY
```

The exact OpenClaw/plugin/ownership/managed convergence postconditions were not claimed because the installer terminal boundary was unproven and the effective fingerprint did not advance.

## SQLite and durable preservation

Independent `file:<path>?mode=ro` verification reported:

```text
integrity_check: ok
tickets: 11
ticket_events: 86
cnx_direct_model_call: 11
cnx_direct_recovery: 1
cnx_assistant_delivery: 7
ticket_outbox: 0
cnx_sessions: 19
```

No Discord traffic, new semantic Ticket, model call, recovery attempt, or outbox activity was created by Task 212. The historical Task-205 cancellation remained preserved.

## Issue register

1. **Task-210 terminal gap carried forward — installer boundary.** The previous install attempt ended at `plugin-rollover-prepare` with no terminal result. Task 212 was explicitly authorized as one fresh normal-upgrade attempt; it was not replayed after the new attempt became unproven.
2. **Broad preflight process scan self-matched observer shells — harness issue.** The scan included its own bash command lines because they contained `cnxclaw_v093.py`. This was excluded using ancestry/evidence-root binding; clean process scan returned zero relevant matches. No product impact.
3. **Detached installer had no output — completion evidence gap.** The exact root PID disappeared naturally, but zero-byte streams and absent stage markers leave the documented installer body and exit result unproven. No product root cause is inferred.
4. **PID reuse observed during broad post-scan — harness evidence.** PID `21836` later appeared as a bash observer shell, not as the installer executable. The clean scan excluded the observer and found no installer/lifecycle residue. No process was terminated.
5. **Post-status parser summary was initially shallow — harness issue.** The status JSON is nested under `host`; raw status was retained and inspected directly. Product status was not inferred from the failed shallow summary.

## Mutation ledger

```text
Task-212 installer launches: 1
installer retries: 0
cnxclaw enable/disable/start/stop/restart/reset/uninstall: 0
Gateway restart: 0
OpenClaw plugin mutation outside installer: 0
ownership/staging/transaction/backup mutation: 0
manual SQLite writes: 0
provider/model/config mutation: 0
process termination: 0
Discord traffic: 0
source/test/workflow edit: 0
Release/tag/asset mutation: 0
force push: 0
```

## Required next action

Stop for coordinator review. Do not retry the installer, run `enable`, restart Gateway, normalize ownership, or send Discord traffic in Task 212. A future successor must explicitly resolve the empty-stream/terminal boundary with a supported, sufficiently durable installer observer before any semantic acceptance is considered.
