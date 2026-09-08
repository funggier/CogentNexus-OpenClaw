# CNX-20260904-244 — Hardened-Runner Exact-Candidate Windows Install-Over Requalification

## Disposition

`BLOCKED_INSTALLER_TASK_REGISTRATION`

The installer Scheduled Task was registered but failed the mandatory pre-start action-binding gate. It was **not started**. No installer child invocation occurred.

## Fresh authority and exact candidate

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Fresh coordination HEAD before live registration and before report publication: `edc44bb6a03f573aa715bc04281dcb65a0f9fc41`
- Task: `CNX-20260904-244`
- Parent: `CNX-20260904-243`
- Reviewed Task-243 report HEAD: `ad94e992fec3cbf414bf82a3dd5073b229e6b5b8`
- Exact candidate: `18a51b15768fb3d2196e65f1ef470c34aeef7f36`
- Candidate fingerprint: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Exact-candidate GitHub Actions, queried fresh:

- PS5.1 Acceptance Smoke `33832755287`: `completed / success`
- Windows Installer Pack Smoke `33832755300`: `completed / success`
- Validate `33832755313`: `completed / success`

## Exact detached source gate

Fresh detached checkout:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx244-exact-source-20260904T
```

- HEAD: `18a51b15768fb3d2196e65f1ef470c34aeef7f36`
- detached: true
- clean: true
- VERSION: `0.9.3`
- installer: `scripts/install.ps1`
- plugin validation: PASS
- packed file count: `196`
- source plugin fingerprint: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

The root checkout has no root-level `package.json`; the candidate plugin project is `plugins/cogentnexus-openclaw`, where `npm run plugin:validate` passed. This was corrected as a repository-layout inspection only; no source was edited.

## Fresh live preflight

Evidence root:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx244-evidence-20260904T
```

Read-only checks returned `READY`, exit code `0` for gateway, provider, model, storage, recovery, delivery, and the canonical CogentNexus-OpenClaw check.

Status boundary:

```text
controller mode = passthrough
controller generation = 39
selected provider = ollama
candidate plugin = not installed
installed plugin fingerprint = e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
pendingRollover = false
classification mode = upgrade
pluginAlreadyExact = false
installPlugin = true
rolloverPlugin = true
```

The installed plugin was read from:

```text
C:/Users/CDQ-P/.openclaw/extensions/cogentnexus-openclaw
```

The retained Task-241 task remained `Ready`, `LastTaskResult=1`. Historical Task-237/241/242/243 evidence was not changed.

## Fresh runner gate

New disposable runner:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx244-runner-20260904T/hardened-runner.ps1
```

Frozen runner SHA-256:

```text
f7287251437688cc7ff529d2810e8f2af12a1f2ce922d8c50da2a0e5fa5fc706
```

The runner was directly qualified before registration:

- synthetic child nonzero: stdout/stderr captured, `runner-result.json` present, outcome `child_nonzero_exit`, child/runner exit `37`
- synthetic missing child: `runner-started.json` present, outcome `child_launch_exception`, exception captured, `runner-result.json` and fallback log present

The runner hash was rechecked after qualification and remained identical. It was not edited after freeze.

## Derived installer state machine

The source-owned read-only classifier returned:

```text
mode = upgrade
pendingRollover = false
pluginAlreadyExact = false
installPlugin = true
rolloverPlugin = true
```

Therefore the intended child invocation had to execute:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx244-exact-source-20260904T/scripts/install.ps1
```

with workspace:

```text
C:/Users/CDQ-P/.openclaw/workspace
```

Expected installer stages included candidate package validation, a new unique rollover prepare/transaction, local package installation, plugin disable, and rollover finalize. No stage was reached.

## Installer Scheduled Task registration/readback

Task name:

```text
CogentNexus-OpenClaw-Task244-Installer-1
```

- registration: `1`
- successful start: `0`
- installer child invocations: `0`
- retries after start: `0`
- pre-start state: `Ready`
- principal: `CDQ-P`, Interactive, Limited
- executable: `C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe`
- execution limit: `PT45M`
- restart count: `0`
- frozen runner SHA readback: `F7287251437688CC7FF529D2810E8F2AF12A1F2CE922D8C50DA2A0E5FA5FC706`

The exact readback exposed the blocker. The action launched the frozen runner, but the nested `-ChildArguments` value was constructed incorrectly: its nested `-File` value pointed to `powershell.exe` rather than the exact candidate installer path. Consequently the registered action did **not** satisfy the required exact-source binding and must not be started.

This was detected before start. No second registration, task update, unregister, direct installer invocation, or manual repair was performed.

## Terminal classification

`BLOCKED_INSTALLER_TASK_REGISTRATION`

This is a pre-start harness/action-binding failure. It is not evidence of an installer, rollover, plugin, runtime, or product failure. There is no runner-started artifact for an installer execution because the task was deliberately not started after the invalid readback.

## Live-state preservation

The post-registration action was limited to read-only verification. No installer start occurred. No candidate installation, rollover prepare/finalize, plugin mutation, lifecycle normalization, controller/Gateway mutation, database write, semantic operation, or process termination occurred.

## Effect ledger

```text
scripts/install.ps1 invocations: 0
installer Scheduled Task registrations: 1
installer Scheduled Task starts: 0
installer child invocations: 0
rollover-prepare/finalize: 0
openclaw plugins install: 0
manual plugin mutation: 0
controller/Gateway/lifecycle mutation: 0
manual Ticket/outbox/recovery/SQLite writes: 0
Dashboard submissions: 0
Discord submissions: 0
direct Discord/API sends: 0
semantic retries: 0
recovery replay/resend: 0
provider/model substitution: 0
process termination: 0
historical evidence cleanup: 0
release/tag/asset mutation: 0
force-push/history rewrite: 0
```

## Recommendation

A separately reviewed successor should correct only the disposable Task-244 registration argument construction, then regenerate and re-qualify a fresh runner/task definition. It must re-read the exact nested child argument vector and prove the `-File` target equals the detached candidate `scripts/install.ps1` before any start. This task's registered task was not repaired or retried, and Task 244 provides no further installer authority.

STOP for independent ChatGPT review.
