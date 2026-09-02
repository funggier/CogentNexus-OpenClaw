# CNX-20260902-230 — Scheduler Identity Recovery, Bounded Retry, and Installer Re-entry

- **Task:** `CNX-20260902-230`
- **Parent:** `CNX-20260902-229`
- **Execution date:** 2026-09-02 (UTC evidence)
- **Executor:** Hermes / authenticated Windows forensic operator
- **Disposition:** `PASS_INSTALLER_TERMINAL_AND_MANAGED_CONVERGENCE`
- **Discord sends:** `0`

## Authority and boundaries

Fresh authority was fetched from `origin/agent/v0.9.3-full-stabilization` before execution. The accepted repaired source was `9a8510f1317c8e53c01c233b080ec20357cd22df`; public `v0.9.3` remained immutable at `26ce64a624255278a3a0266ad38746e0e6ed2e31`.

The bounded retry contract was followed:

- canary registration: at most 4; used 1
- installer-task registration: at most 2; used 1
- installer task start/invocation: at most 1; used 1
- no retry after installer start
- no override flags, manual rollover/finalize, stale-evidence cleanup, Gateway restart, SQLite writes, provider/model substitution, process termination, Release/tag/asset mutation, force-push, or Discord traffic

## Identity recovery and canary

Canonical Windows identity evidence:

- `WindowsIdentity.Name`: `CDQ-P\\CDQ-P`
- canonical SID: `S-1-5-21-1723981734-2946015581-220292090-1001`
- Task-215 qualified principal: `CDQ-P`, `Interactive`, `Limited`

A unique canary task, `CogentNexus-OpenClaw-Task230-Canary-1`, was registered using the Task-215-qualified settings, then started once and removed. Readback proved:

- terminal marker present
- intended exit code `23`
- task returned to `Ready`
- `LastTaskResult=23`
- cleanup readback: `TaskPresent=false`

The first immediate pre-start probe failed locally because its evidence directory had not yet been created. It failed before installer start. An accidentally included canary-helper token was not reached because shell execution stopped at that missing-directory error; a deterministic task inspection immediately afterward proved the canary was absent and the installer task was still unstarted. This was recorded as a probe/tooling anomaly, not product evidence.

## Exact-first installer re-entry

Fresh pre-start evidence selected the exact candidate before materialization and verified:

```text
candidate/source commit: 9a8510f1317c8e53c01c233b080ec20357cd22df
installed version: 0.9.3
source version: 0.9.3
installed fingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
source fingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
mode: upgrade
pendingRollover: false
pluginAlreadyExact: true
installPlugin: false
rolloverPlugin: false
```

The unique task `CogentNexus-OpenClaw-Task230-Installer-1` was registered and read back as:

- direct Windows PowerShell action
- principal `CDQ-P`, `Interactive`, `Limited`
- `ExecutionTimeLimit=PT45M`
- `RestartCount=0`
- demand start enabled

The task was started exactly once. Terminal evidence from the runner:

```text
INSTALLER_INVOCATION_START utc=2026-09-02T15:38:30.4864500Z
CNXCLAW_INSTALL_STAGE_COMPLETE stage=ticket-db-bootstrap ... exit_code=0
CNXCLAW_INSTALL_STAGE_COMPLETE stage=owned-runtime-ensure ... exit_code=0
CogentNexus-OpenClaw validation: PASS
CogentNexus-OpenClaw v0.9.3 installation completed successfully.
INSTALLER_INVOCATION_END utc=2026-09-02T15:44:34.4043723Z exit_code=0
```

The installer task readback was `Ready`, `LastTaskResult=0`. Stage evidence proves:

```text
installer invocation: 1
plugin install: 0
rollover-prepare: 0
rollover-finalize: 0
installer exit code: 0
```

The temporary installer task was unregistered once. Final task readback was absent. An independent filtered process probe found no `cnx230-installer-runner.ps1` or installer process; the cleanup artifact's apparent matches were command-line self-matches from the probe itself and were not treated as residue.

## Post-install managed convergence

Read-only postflight status proved:

- host mode: `managed`
- generation: `38`
- selected/healthy provider: `ollama`
- Gateway: healthy, loopback `127.0.0.1:18789`, exit code `0`
- startup policy: `enabled`
- startup adapter: installed, `Ready`, enabled, `LastTaskResult=0`
- policy source: `registered`
- Delivery: `READY`, pending outbox `0`
- Recovery: `READY`
- SQLite integrity: `ok`
- tickets: `cancelled=2`, `completed=9`

Installed plugin identity remained exact:

```text
root: c:\\users\\cdq-p\\.openclaw\\extensions\\cogentnexus-openclaw
version: 0.9.3
fingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
```

The live repaired `namespace_ownership.py` matched the accepted repair source hash and retained the fail-closed attestation contract. The installer-owned ownership state transition was observed as managed convergence; no manual ownership edit was performed.

## Retained evidence preservation

The historical Task-223 evidence remained unchanged:

```text
transaction SHA-256: ec1b32ec2813e1b4e2c220679f39c6922789b7d77e88ec9ca4ad6ba82ccac510
inventory SHA-256:   1a7299f926cda4e3f936577204c50059e0e4e716f8594535d4b3c40c40e51477
backup tree SHA-256: 7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a
backup fingerprint:  f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
```

The rollover directory still contained only the four pre-existing retained transaction files, including the historical `8469daf...` transaction; no new rollover transaction was created by this already-exact re-entry.

## Evidence locations

Primary evidence root:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx230-installer-reentry-20260902T
```

Relevant artifacts include `stage-summary.txt`, `runner-stage.log`, `installer-transcript.txt`, `terminal-readback.json`, `cleanup-readback.json`, `post-status.json`, `post-plugin-fingerprint.json`, `post-ownership-verify.json`, `post-rollover-files.json`, and the pre-start classification/action/stale-hash files.

## Final decision

Task-229 was blocked before installer execution by scheduler registration. Task-230 recovered the qualified direct Scheduled Task identity, proved the terminal boundary with a canary, performed exactly one authorized already-exact installer invocation, and verified terminal success plus managed convergence. The installer PASS is therefore accepted for Task-230. No Discord action was simulated or sent, and the published release remained untouched.
