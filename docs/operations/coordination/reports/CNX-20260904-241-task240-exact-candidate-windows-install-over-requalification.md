# CNX-20260904-241 — Exact-Candidate Windows Install-Over Requalification

## Authority and exact source

- Task: `CNX-20260904-241`
- Mode: `TASK241_TASK240_EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFICATION`
- Fresh authority before report publication: `47aaf053b685ee9db82b3f8e121ce170dfb216db`
- Exact candidate source commit: `18a51b15768fb3d2196e65f1ef470c34aeef7f36`
- Production diagnostic repair lineage: `ec29020632091aae3b50149b51303a36fde26310`
- Expected plugin fingerprint: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- Fresh detached checkout: `C:/Users/CDQ-P/AppData/Local/Temp/cnx241-exact-source`
- Detached checkout HEAD: exact candidate SHA
- Detached checkout clean: true
- Installer invoked from: `C:/Users/CDQ-P/AppData/Local/Temp/cnx241-exact-source/scripts/install.ps1`
- Task-239 bounded diagnostic helper and Task-240 portability test were present.
- Source plugin validation passed and computed the expected fingerprint.

## Fresh read-only preflight

Evidence root:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx241-preflight-20260904T
```

Observed controller state:

```text
mode = passthrough
generation = 39
selectedProvider = ollama
```

This matched the retained Task-237/238 boundary. The live plugin remained the predecessor and the candidate was not installed. The retained Task-237 backup token remained present and was not modified:

```text
c6aaf93db7c34f718d01302477a292e1
```

All read-only launcher checks returned `READY`, `exitCode=0`, `stateChanged=false`:

```text
gateway
provider
model
storage
recovery
delivery
```

SQLite read-only evidence:

```text
integrity = ok
tickets = 13
ticket_events = 106
ticket_outbox = 0
cnx_assistant_delivery = 8
cnx_direct_recovery = 2
cnx_direct_model_call = 13
cnx_sessions = 20
```

## Installer registration/start ledger

New disposable task:

```text
CogentNexus-OpenClaw-Task241-Installer-1
```

Registration evidence:

- registration attempts: `1`
- task state before start: `Ready`
- action: Windows PowerShell 5.1 invoking the Task-241 runner
- principal: `CDQ-P`, `Interactive`, `Limited`
- execution time limit: `PT45M`
- restart count: `0`

Start evidence:

- starts: `1`
- started UTC: `2026-09-04T04:01:24.4982851+00:00`
- retry gate: `CLOSED`
- second start: `0`
- installer retry after start: `0`

The Task Scheduler state transitioned from `Running` to `Ready` with:

```text
LastTaskResult = 1
```

## Terminal result and evidence limitation

The bounded installer execution ended with `LastTaskResult=1`. However, the fresh runner result and installer transcript were not present in the dedicated evidence root after completion. A read-only search did not find a new Task-241 transcript; only prior Task-237/230/223 transcripts were present.

The runner script itself passed an independent PowerShell parser check:

```text
RUNNER_SYNTAX=PASS
```

A Task Scheduler operational-event query produced no usable event artifact. Therefore the available evidence proves one scheduled-task start and a terminal nonzero task result, but does not reliably bind:

- the child installer invocation;
- an installer stage name;
- the bounded child diagnostic;
- a rollover ID/backup transaction allocated by this attempt;
- or the precise failure location.

No inference from `LastTaskResult=1` alone is promoted to a specific installer-stage failure.

## Post-failure read-only state

Evidence root:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx241-post-20260904T
```

Post-state remained coherent and unchanged:

```text
controller = passthrough
generation = 39
candidate plugin = not installed
Gateway = READY
provider = READY
model = READY
storage = READY
recovery = READY
delivery = READY
pending outbox = 0
SQLite integrity = ok
```

The historical Task-237 backup token and historical evidence were not cleaned or mutated. No manual repair was attempted.

## Disposition

`BLOCKED_EVIDENCE`

The one-shot scheduler execution consumed its permitted start budget and ended nonzero, but retained evidence is insufficient to assign `FAIL_INSTALLER_TERMINAL`, `FAIL_ROLLOVER_PREPARE`, or `FAIL_ROLLOVER_FINALIZE` with confidence. The exact candidate was not proven installed, so no PASS is claimed.

A successor authority is required before any new installer attempt, diagnostic replay, runner redesign, evidence repair, managed-state restoration, plugin repair, or requalification. The retry gate remains permanently closed for this Task-241 execution.

## Zero-effect ledger

```text
installer Scheduled Task registrations: 1
installer Scheduled Task starts: 1
installer invocations proven: 0 (not reliably evidenced)
installer retries after start: 0
manual rollover-prepare/finalize: 0
manual plugin mutation: 0
manual controller/Gateway/lifecycle mutation: 0
manual Ticket/outbox/recovery/SQLite writes: 0
Dashboard semantic submissions: 0
Discord semantic submissions: 0
direct Discord/API sends: 0
recovery replay/resend: 0
provider/model substitution: 0
process termination: 0
Task-237 orphan-backup cleanup: 0
historical evidence cleanup: 0
release/tag/asset mutation: 0
force-push/history rewrite: 0
```

STOP for independent review.
