# CNX-20260904-245 — Manifest-Bound Exact-Candidate Windows Install-Over Requalification

## Disposition

`FAIL_INSTALLER_TERMINAL`

The fresh manifest-bound Task-245 installer started exactly once, invoked the exact detached candidate, and terminated nonzero at `plugin-rollover-prepare`. No retry or manual repair was performed. Semantic requalification was not attempted.

## Fresh authority and candidate gates

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Fresh authority before registration and before report publication: `36f04ab85a97c64c80a925c526d7cccfa025c0e1`
- Task: `CNX-20260904-245`
- Parent: `CNX-20260904-244`
- Reviewed Task-244 report HEAD: `2da9be61abd1da7ea36c508af640e1732853e2b1`
- Exact candidate: `18a51b15768fb3d2196e65f1ef470c34aeef7f36`
- Candidate fingerprint: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Fresh exact-candidate Actions:

- PS5.1 Acceptance Smoke `33832755287`: `completed / success`
- Windows Installer Pack Smoke `33832755300`: `completed / success`
- Validate `33832755313`: `completed / success`

Fresh detached source:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx244-exact-source-20260904T
```

- HEAD exact candidate
- detached and clean
- VERSION `0.9.3`
- plugin `npm run plugin:validate`: PASS
- packed file count: `196`
- source fingerprint: exact authority fingerprint above

## Fresh live preflight

Evidence root:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx244-evidence-20260904T
```

Before registration, read-only checks for gateway, provider, model, storage, recovery, delivery, and CogentNexus-OpenClaw were all `READY`, exit `0`. Controller remained `passthrough`, generation `39`, selected provider `ollama`; candidate was not installed. Installed canonical plugin fingerprint was the predecessor:

```text
e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
```

Source-owned read-only classification returned:

```text
mode=upgrade
pendingRollover=false
pluginAlreadyExact=false
installPlugin=true
rolloverPlugin=true
```

The retained Task-241 task was unchanged (`Ready`, `LastTaskResult=1`). Historical Task-237/241/242/243/244 evidence was not cleaned or mutated.

## Fresh frozen runner and manifest

Runner:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx245-runner-20260904T/manifest-runner.ps1
```

Frozen runner SHA-256:

```text
0c2da0cb5877ca9493e4921c3a7b5492dd884841a2bd68c3fb63032b6e42eb98
```

Direct harmless qualification passed before registration:

- synthetic nonzero child: stdout/stderr, transcript, started/result artifacts; child and runner exit `37`
- nonexistent child: `child_launch_exception`, exception captured, `finally` result and fallback artifacts present

Production manifest:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx245-install-evidence-20260904T/launch-manifest.json
```

Manifest SHA-256:

```text
d00e5061aaf73ca902f63f2aa367dfbc88a0064551e13b017f61d83a0b68869a
```

Decoded manifest child vector:

```text
[
  -NoLogo,
  -NoProfile,
  -ExecutionPolicy,
  Bypass,
  -File,
  C:/Users/CDQ-P/AppData/Local/Temp/cnx244-exact-source-20260904T/scripts/install.ps1,
  -Workspace,
  C:/Users/CDQ-P/.openclaw/workspace
]
```

There was exactly one `-File`; its value matched the exact detached candidate installer path. The manifest and runner hashes were re-read at pre-start and matched the frozen values.

## Task registration and start

Task:

```text
CogentNexus-OpenClaw-Task245-Installer-1
```

- successful registration: `1`
- starts: `1`
- child installer invocations: `1`
- retries after start: `0`
- principal: `CDQ-P`, Interactive, Limited
- action executable: `C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe`
- action arguments contained only the runner path, manifest path, and evidence root
- execution limit: `PT45M`
- restart count: `0`
- pre-start binding gate: PASS

The retry gate closed immediately after start. No second start, direct installer fallback, task update, process termination, or manual repair was performed.

## Hardened terminal evidence

Evidence root:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx245-install-evidence-20260904T
```

- `runner-started.json`: present, 1,470 bytes
- `child-stdout.txt`: present, 3,431 bytes
- `child-stderr.txt`: present, 1,281 bytes
- `runner-transcript.txt`: present, 4,741 bytes
- `runner-result.json`: present, 985 bytes
- fallback log: not needed; transcript write succeeded

Runner result:

```text
outcome = child_nonzero_exit
childStarted = true
childExitCode = 1
```

Scheduler terminal readback:

```text
state = Ready
LastTaskResult = 1
```

The runner and scheduler terminal codes are coherent.

## Installer stage classification

Captured stdout proves these stages completed:

```text
ticket-db-bootstrap: exit 0
plugin-npm-pack: exit 0
```

The next stage started:

```text
CNXCLAW_INSTALL_STAGE_START stage=plugin-rollover-prepare
```

The child then emitted a Python traceback beginning at `scripts/install.ps1:401`, and exited `1`. The bounded captured diagnostic does not contain enough of the Python traceback to assert a more specific exception or sub-operation. Therefore the narrow supported classification is terminal installer failure at `plugin-rollover-prepare`; no claim is made about the exact underlying Python exception.

No new rollover transaction JSON was found in the staging directory after this attempt. A new workspace backup was observed:

```text
C:/Users/CDQ-P/.openclaw/workspace/.cogentnexus-openclaw/install-backups/cogentnexus-openclaw-20260904-195413
```

The canonical plugin remained disabled and at the predecessor fingerprint. The installer-owned partial state is preserved as evidence; no recovery or repair was attempted.

## Postflight preservation

Fresh read-only checks after terminal failure remained `READY`, exit `0` for gateway, provider, model, storage, recovery, and delivery. The controller remained `passthrough`, generation `39`, and selected provider `ollama`. The canonical installed plugin remained:

```text
fingerprint = e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
status = disabled
```

The live plugin project tree hash remained:

```text
900ac13f85a6de75e40a632a534f2b0ceef53def1e8387fc3530c02a7413de58
```

No PASS postflight is claimed because the candidate fingerprint, rollover finalization, and managed convergence were not achieved.

## Effect and retry ledger

```text
installer Scheduled Task registrations: 1
installer Scheduled Task starts: 1
installer child invocations: 1
installer retries after start: 0
manual installer invocations: 0
manual rollover prepare/finalize: 0
manual plugin replacement: 0
manual controller/Gateway/lifecycle mutation: 0
manual Ticket/outbox/recovery/SQLite writes: 0
Dashboard semantic submissions: 0
Discord semantic submissions: 0
direct Discord/API sends: 0
semantic retries: 0
recovery replay/resend: 0
provider/model substitution: 0
process termination: 0
historical evidence cleanup: 0
release/tag/asset mutation: 0
force-push/history rewrite: 0
```

The `ticket-db-bootstrap` operation was performed by the authorized installer child and reported exit `0`; no manual database operation was performed.

## Recommendation and stop gate

Do not retry from Task 245. A separately reviewed successor is required to diagnose or repair the `plugin-rollover-prepare` boundary and to decide whether another bounded installer attempt is safe. Semantic durable-delivery requalification remains forbidden here and requires a separate successor.

STOP for independent ChatGPT review.
