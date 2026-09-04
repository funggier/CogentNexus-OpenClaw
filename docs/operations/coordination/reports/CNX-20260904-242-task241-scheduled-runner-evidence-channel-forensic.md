# CNX-20260904-242 — Task-241 Scheduled Runner Evidence-Channel Forensic

## Authority and scope

- Task: `CNX-20260904-242`
- Mode: `TASK242_TASK241_SCHEDULED_RUNNER_EVIDENCE_CHANNEL_FORENSIC`
- Fresh authority before publication: `76976b744dcc9985db27b9e67f4359dd467ad68d`
- Parent report: `docs/operations/coordination/reports/CNX-20260904-241-task240-exact-candidate-windows-install-over-requalification.md`
- Scope: forensic/tooling-only
- Product installer invocation: `0` in Task 242
- No production/source/test/workflow changes were made.

## Question and retained Task-241 evidence

Task 241 registered and started exactly one Scheduled Task. Its terminal state was `LastTaskResult=1`, but no fresh runner result or installer transcript was present. The retained Task-241 evidence roots were preserved and not rewritten.

Fresh forensic root:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx242-forensic-20260904T
```

Retained Task-241 runner:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx241-installer-runner.ps1
```

Runner metadata:

- bytes: `879`
- SHA-256: `fca3d96a6152dde72d35ff240d8ad71df28838e29a2452b977a07e54d886cbaa`
- PowerShell parser: `PASS`
- ACL grants `CDQ-P` Modify/FullControl on the runner path.

Task-241 evidence root:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx241-install-evidence
```

It existed and was writable by `CDQ-P`, but contained only `registration.json` and `start.json`; no `runner-result.json` or fresh installer transcript.

## Exact launch-chain reconstruction

```text
Task Scheduler
  -> C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe
  -> -NoLogo -NoProfile -ExecutionPolicy Bypass -File "C:/Users/CDQ-P/AppData/Local/Temp/cnx241-installer-runner.ps1"
  -> runner absolute source path:
     C:/Users/CDQ-P/AppData/Local/Temp/cnx241-exact-source/scripts/install.ps1
  -> child invocation via call operator:
     & powershell.exe ... -File $source -Workspace $workspace
  -> result write only after child returns:
     .../cnx241-install-evidence/runner-result.json
```

Scheduled Task definition readback:

- state: `Ready`
- LastTaskResult: `1`
- principal: `CDQ`, Interactive, Limited
- execution limit: `PT45M`
- restart count: `0`
- working directory: unset/null
- all runner paths: absolute

The forward-slash native paths are not sufficient to explain the failure because the harmless canary used the same PowerShell executable/path style and completed successfully.

The runner has no durable startup marker before the child call, no `Start-Transcript`, and no `finally` fallback result. Its only result write occurs after the child process returns. Therefore an early runner/child launch boundary or host termination can leave exactly the observed zero-artifact state, but the retained evidence cannot distinguish those sub-boundaries.

## Harmless canary

Phase A/B could not fully distinguish scheduler action binding from runner/evidence behavior, so the single authorized harmless canary was used.

Canary files:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx242-canary-runner.ps1
C:/Users/CDQ-P/AppData/Local/Temp/cnx242-canary-20260904T/canary-result.json
```

Canary runner SHA-256:

```text
e69be0fc1c08da9083616b1fe20e03c8d51b3140a44ac5e3418f2ed6852fc26a
```

Canary result:

```text
registration count = 1
start count = 1
retry after start = 0
Task state = Ready
LastTaskResult = 0
marker = CNX242_CANARY_SUCCESS
PowerShell = 5.1.19041.6456
identity = CDQ-P\CDQ-P
cwd = C:\Windows\system32
artifact = present
```

The canary performed only scheduler-to-PowerShell-to-script-to-file capture. It made no installer, OpenClaw, Gateway, provider, database, network, semantic, or recovery calls.

This excludes:

- a general Scheduled Task action launch failure;
- the PowerShell executable/path format as a sufficient cause;
- principal inability to write to the dedicated temp evidence path;
- insufficient disk space;
- a general PowerShell 5.1 startup failure.

It does not prove that Task 241's child installer was invoked.

## Event and filesystem findings

- Task Scheduler Operational event query produced no usable matching event artifact.
- Windows PowerShell event collection was available, but no event record was found that durably binds the Task-241 child installer invocation.
- Dedicated Task-241 evidence root ACL was writable by the task principal.
- Task-241 runner and source paths were absolute; no current-working-directory dependency was found.
- No fresh Task-241 transcript/result artifact exists.
- The retained Task-237 orphan backup token `c6aaf93db7c34f718d01302477a292e1` was not changed.

## Root-cause classification

`PASS_HARMLESS_CANARY_PROVES_EXECUTION_CHANNEL`

The evidence channel from an equivalent Scheduled Task through Windows PowerShell 5.1 to a durable artifact is functional. The narrowest supported conclusion is an unresolved Task-241-specific runner/child evidence boundary, not a product installer defect and not a general scheduler action defect.

The exact Task-241 child installer invocation remains unproven. No product-stage classification is assigned and no installer retry is authorized.

## Preserved live-state proof

Fresh read-only post-checks after the canary all returned `READY`, exit code `0`, and `stateChanged=false`:

```text
gateway
provider
model
storage
recovery
delivery
```

The preserved controller remained `passthrough`, generation `39`; no candidate install, managed-state normalization, plugin mutation, Ticket/outbox/recovery/SQLite write, or semantic action occurred.

## Effect and retry ledger

```text
scripts/install.ps1 invocations in Task 242: 0
installer Scheduled Task starts in Task 242: 0
rollover-prepare/finalize: 0
openclaw plugins install: 0
manual plugin mutation: 0
controller/Gateway/lifecycle mutation: 0
manual Ticket/outbox/recovery/SQLite writes: 0
Dashboard semantic submissions: 0
Discord semantic submissions: 0
direct Discord/API sends: 0
recovery replay/resend: 0
provider/model substitution: 0
process termination: 0
Task-241/Task-237 evidence cleanup: 0
installer retry: 0

harmless canary registrations: 1
harmless canary starts: 1
canary retries after start: 0
```

## Successor recommendation

Before another live installer requalification, create a separate reviewed task to repair the operator runner/evidence harness, not the installer product code. The smallest safe correction should:

1. create and verify the evidence root before any child call;
2. write a durable `runner-started` record before invoking the child;
3. capture child stdout/stderr and exit status;
4. write a `runner-result` record from a `finally` path even when child launch fails;
5. use an explicit transcript/fallback log path;
6. preserve the exact source, argument vector, working directory, identity, and timestamps;
7. remain separate from any installer retry authorization.

Task 242 itself does not implement that correction and does not start a new installer attempt.

STOP for independent review.
