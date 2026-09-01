# CNX-20260901-213 — Task-212 Installer Source + Detached-Launch Root-Cause Adjudication

Date: 2026-09-01 ICT  
Task: `CNX-20260901-213`  
Parent: `CNX-20260901-212`  
Branch: `agent/v0.9.3-full-stabilization`

## Disposition

`PASS_DETACHED_LAUNCH_HARNESS_DEFECT_PROVEN`

This is diagnostic closure only. It is not product acceptance and does not authorize another installer, lifecycle action, or Discord Send.

The strongest supported claim is that the detached Python/PowerShell launch mechanics used by Task 212 are incompatible with this Windows executor environment: a harmless PowerShell child launched with the same `Popen`/creation flags disappeared before 10 seconds, emitted zero stdout/stderr, and never reached its 65-second sleep or terminal markers. The result reproduces the Task-212 empty-stream/rapid-disappearance shape without accessing CogentNexus/OpenClaw paths.

The executed Task-212 installer source path is source-code-equivalent to the Task-207 candidate at the installer/repair-file boundary, but its ignored generated `dist/` tree had a different fingerprint. This isolates source-boundary ambiguity from the proven generic detached-launch defect; it does not prove that Task-212 installed the candidate.

## Evidence root

`C:/Users/CDQ-P/AppData/Local/Temp/cnx213-task212-launch-source-diagnosis-20260901T`

Key artifacts:

- `a00-captured-at-utc.txt`
- `a01-status.json`, `a02-delivery.json`, `a03-recovery.json`, `a04-live-fingerprint.json`, `a05-process-scan.json`
- `b01-source-binding.json`, `b02-executed-tree-fingerprint.json`, `b03-candidate-tree-fingerprint.json`, `b04-source-relation.json`
- `c01-launch-installer.py`, `c02-monitor-installer.py`, `c03-harness-hashes.txt`, `c04-harness-analysis.json`
- `synthetic-child.ps1`, `synthetic-launch.py`, `synthetic-launch.json`, `synthetic-samples.json`
- `candidate/` detached source checkout at Task-207 candidate
- `candidate-payload/` extracted retained package proof

## Phase A — live preservation

Fresh read-only state remained consistent with the accepted Task-212 boundary:

```text
controller mode: passthrough
generation: 33
startup policy: disabled
startup adapter: installed=false
Gateway: healthy
selected provider: ollama
Delivery: READY
Recovery: READY
live plugin fingerprint: f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
SQLite integrity: ok
relevant lifecycle/installer residue after self-match exclusion: 0
```

No live product process was terminated. Task-205 cancellation remained preserved and inert. No installer, lifecycle, ownership, database, provider, Gateway, or Discord mutation occurred.

## Phase B — executed installer source binding

The exact path recorded by Task 212 was:

`C:/Users/CDQ-P/AppData/Local/Temp/cnx-successor-204-authority-20260901T/scripts/install.ps1`

The executed-tree checkout was at:

```text
HEAD: 6f4543f05449b26f74ccbc1ffcb167512c84d945
candidate: 27fe0181b3b65d555a3b0cc8354f6f7945c21c0b
candidate is ancestor of executed HEAD: true
```

Exact byte comparisons:

```text
scripts/install.ps1
  executed bytes: 30637
  candidate bytes: 30637
  executed SHA-256: 8cb713b7ddfe5be113530298fe3195094c0055a78ff63cdb393a483debc47e56
  candidate SHA-256: 8cb713b7ddfe5be113530298fe3195094c0055a78ff63cdb393a483debc47e56

plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts
  executed bytes: 35291
  candidate bytes: 35291
  executed SHA-256: 157460ee24a37472830b30dd19fec06172e3245b0f25447ddc0db1280b43473a
  candidate SHA-256: 157460ee24a37472830b30dd19fec06172e3245b0f25447ddc0db1280b43473a

plugins/cogentnexus-openclaw/openclaw.plugin.json
  executed bytes: 8230
  candidate bytes: 8230
  executed SHA-256: 1f35d3a2a8ed2550f4afc906a2f9a339e3e0e0f1a44e240994aab9a4fbaf771e
  candidate SHA-256: 1f35d3a2a8ed2550f4afc906a2f9a339e3e0e0f1a44e240994aab9a4fbaf771e
```

No `PAYLOAD_IDENTITY.json` or `PACKAGE_IDENTITY.json` existed in the executed source tree. Its Git HEAD was clean and is a descendant of the Task-207 candidate. Source classification:

```text
EXECUTED_SOURCE_EXACT_TASK207
```

This classification is limited to the source/installer and repair-file boundary. It does not upgrade the ignored generated payload or Task-212 installation result to candidate provenance.

The exact candidate fingerprint tool produced:

```text
d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b
```

The executed checkout's existing generated plugin tree produced:

```text
3b86b13f6d39996f18687510ab65aa4bba46bdf8d80b1aaeef14fe8d199eb3ed
```

The differing generated-tree fingerprint is recorded as stale/other ignored build output in the checkout; it was not treated as proof of the package that Task 212 would have rebuilt.

## Phase C — retained Task-212 launcher mechanics

The exact retained `launch-installer.py` was copied byte-for-byte into the evidence root and hashed. Its mechanics are:

```text
Popen: yes
executable: powershell.exe
argv: -NoProfile -ExecutionPolicy Bypass -File <installer> -Workspace <workspace>
stdin: subprocess.DEVNULL
stdout: opened as binary file and passed to Popen
stderr: opened as binary file and passed to Popen
shell: not specified (false by default)
cwd: not specified (inherits launcher cwd)
close_fds: true
creationflags: DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
creationflags hex: 0x208
start_new_session: not used
PATH: prepends C:\Program Files\nodejs
launcher waits for child: no
launcher exits immediately after Popen/metadata write: yes
```

The launcher records PID/start timestamp/stream paths in JSON, but does not immediately capture the child's executable path, creation time, or full OS command-line tuple. It also does not retain a child exit code because it intentionally does not wait.

The retained `monitor-installer.py` performs later `psutil` snapshots and hashes streams, but it cannot recover a PowerShell exit code once the detached child is gone. It records process existence, executable, command line, parent, creation time, CPU/thread/memory fields when available, and stream sizes/hashes at intervals.

Task-212 launch metadata recorded PID `21836` and start `2026-09-01T10:52:23.957+00:00`. Its streams remained zero bytes and no stage marker or terminal line was retained. The later broad scan showed PID reuse as an observer bash process; a clean scan excluded observer ancestry/evidence-root self matches.

## Phase D — harmless synthetic reproduction

The synthetic child was an explicit PowerShell script in the external evidence root only. It:

1. writes distinct stdout/stderr start markers;
2. records its PowerShell PID/timestamp in both streams;
3. sleeps 65 seconds;
4. writes terminal markers;
5. exits with code 23.

It did not reference any CogentNexus/OpenClaw path.

The same launch options were used:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -File <synthetic-child.ps1>
stdin=DEVNULL
stdout/stderr=separate redirected binary files
close_fds=true
creationflags=DETACHED_PROCESS|CREATE_NEW_PROCESS_GROUP
hex=0x208
no shell
no cwd override
no start_new_session
PATH prepended with C:\Program Files\nodejs
```

Observed synthetic result:

```text
PID: 20760
creation time: 2026-09-01T11:41:10.688149+00:00
executable at immediate sample: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
immediate existence: true
10-second existence: false
30-second existence: false
60-second existence: false
post-exit existence: false
stdout bytes at all samples: 0
stderr bytes at all samples: 0
expected 65-second child lifetime: not observed
expected markers: absent
launcher_returncode: 0
```

This is materially the same as Task 212's rapid disappearance/zero-byte stream boundary. The synthetic run proves the generic detached launch/stream topology is defective or incompatible in this executor environment. It does not prove which Windows primitive caused the child termination, and it does not prove a CogentNexus product defect.

The known harmless child was not killed; it disappeared naturally. No product path was accessed.

## Phase E — Task-170 comparison

Retained Task-170 report/review proves a materially different successful observation outcome:

```text
wrapper PID: 18088
installer PID: 22052
installer natural lifetime: 2026-08-30T22:33:55.686Z -> 22:47:21.343Z
stdout: 93018 bytes
stderr: 928 bytes
seven installer stages: all START/COMPLETE paired, child exit 0
final provenance/health: PASS
```

Task-170 does not retain enough source for every launcher flag to assert whether it used `DETACHED_PROCESS`, `Start-Process`, or identical `Popen` options. Those details remain unavailable and are not guessed.

Directly supported material differences are:

- Task 170 retained nonempty installer streams and seven stage pairs; Task 212 retained zero-byte streams and no markers.
- Task 170 retained an installer PID that survived for roughly 13.4 minutes; Task 212's PID disappeared before the first ~30-second sample.
- Task 170 reached independent post-install provenance/health; Task 212 did not.
- Task 212's launcher source is explicitly known to use detached flags, `stdin=DEVNULL`, and immediate parent return; Task 170's exact flag/handle implementation is unavailable from retained report evidence.

The comparison supports the conclusion that Task-212's launch/observation boundary failed. It does not identify an internal PowerShell wait API or claim that Task-170 used a particular undocumented flag.

## Root-cause classification

Proven facts:

1. The installer path used by Task 212 was in a Git descendant of the Task-207 candidate, and its installer/repair/manifest source files matched candidate bytes exactly.
2. The checkout's existing ignored generated plugin tree had a different fingerprint; no package identity metadata existed in that tree.
3. Task-212's detached launcher returned immediately, did not wait, used `DETACHED_PROCESS|CREATE_NEW_PROCESS_GROUP`, redirected streams, used `stdin=DEVNULL`, and could not capture child exit code.
4. A harmless child using the same mechanics disappeared before 10 seconds with zero-byte streams and no markers despite a 65-second sleep.
5. Task 212 had the same zero-byte/rapid-disappearance shape.
6. Task 170 had a long-lived installer with nonempty streams, paired stages, and successful postflight.

Strongest supported claim:

```text
The Task-212 detached launcher/stream topology is defective or incompatible with this executor environment and is sufficient to explain the empty-stream/rapid-disappearance observation.
```

Not proven:

- the specific PowerShell internal termination/wait primitive;
- a CogentNexus installer source defect;
- successful execution or installation of the Task-207 candidate in Task 212;
- that the generated ignored dist fingerprint represented the bytes the installer would have rebuilt.

## Issue register

1. **Source-tree package metadata absent — evidence limitation.** The executed tree contained no payload/package identity metadata. Git ancestry and byte comparisons were used; package installation was not inferred from path/version.
2. **Generated dist mismatch — source/build distinction.** The executed checkout's ignored dist fingerprint was `3b86…`, neither candidate nor old live. This remains a build-output identity discrepancy, not proof of what a fresh installer build would produce.
3. **Immediate child OS identity was not persisted by Task 212 launcher — harness defect.** PID/start time and stream paths were retained, but executable/creation-time/full command line were not written immediately. Synthetic reproduction supplied the missing OS identity fields for the generic mechanics.
4. **Detached child exit code unavailable — harness limitation.** The launcher returns immediately and never waits. The synthetic child intentionally exited 23, but the launcher model returned 0 and did not recover the child exit code.
5. **Synthetic child rapid disappearance — proven harness incompatibility.** This reproduces Task 212 without product paths and is the decisive diagnostic evidence.
6. **Broad process scans self-match observer shells/PID reuse — harness issue.** Clean ancestry/evidence-root exclusion yielded zero relevant product processes. No process was terminated.
7. **Task-170 launcher flags unavailable — evidence limitation.** Only its successful PID/stream/stage outcome and documented report facts are retained; unavailable implementation flags were not guessed.

## Mutation ledger

```text
CogentNexus installer/lifecycle actions: 0
OpenClaw plugin mutation: 0
Ownership/staging/transaction/backup mutation: 0
SQLite writes: 0
Gateway restart: 0
Provider/model/config mutation: 0
Process termination: 0
Discord traffic: 0
Source/test/workflow edit: 0
Release/tag/asset mutation: 0
Harmless synthetic child launches: 1
```

## Required next action

Stop for coordinator review. Task 213 does not authorize another installer attempt. Any future requalification task must use a launcher that preserves immediate OS identity, drains redirected streams concurrently, waits/polls the exact child independently of executor timeout, and records the real child terminal result before claiming installation success.
