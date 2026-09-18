# CNX-20260918-413 — ChatGPT Review

## Decision

`ACCEPTED_FAILED`

Accepted classification:

`FAIL_INSTALLER_TERMINAL`

## Independent verification

The authoritative branch and CNX-413 report were re-read from GitHub.

Verified:

- remote HEAD: `991403dd0f042fa3b89573da960c8a82efeb0816`;
- report blob: `8df7b5d7d36efdddd13fa6d7e4f44df1d8ca1532`;
- ACTIVE/STATUS: `WAITING_FOR_CHATGPT_REVIEW`;
- bootstrap lifecycle-start calls: 1;
- bootstrap retries: 0;
- installer invocations: 1;
- installer retries: 0;
- attestation RPC calls: 0;
- semantic/model/provider requests: 0;
- no manual durable-state or Gateway repair occurred.

Stopping after the terminal installer failure was correct.

## What CNX-413 successfully proved

The CNX-411 maintenance-convergence direction is valid in production context.

The one supported old-runtime bootstrap call:

`runtime.py lifecycle start`

without `--provider`:

- returned exit 0;
- retired the stale `healthy-runtime` marker;
- left Gateway healthy;
- produced Recovery `READY`;
- produced Delivery `READY`;
- kept pending outbox at 0;
- kept SQLite integrity `ok`;
- kept provider/model selection unchanged at `ollama/qwen3.8:27b`.

Therefore the previous delivery-hazard bootstrap deadlock is closed.

## Installer failure root cause

The installer failed at:

`scripts/install.ps1:443`

inside the `ticket-db-bootstrap` diagnostic stage.

Current source directly invokes:

```powershell
node (Join-Path $pluginDir "scripts\bootstrap-ticket-db.mjs") --workspace $Workspace
$ticketDbExit = $LASTEXITCODE
```

The installer runs with `$ErrorActionPreference = "Stop"`.

On Windows PowerShell 5.1, native stderr can be promoted to a PowerShell `NativeCommandError` before the script reaches the `$LASTEXITCODE` classification boundary.

The Node child emitted the normal Node SQLite warning on stderr:

`ExperimentalWarning: SQLite is an experimental feature and might change at any time`

while the bootstrap itself emitted a successful database result with pending outbox 0.

This is therefore an installer PowerShell/native-stderr boundary defect, not a Ticket DB bootstrap failure.

## Existing repair primitive already in the installer

This repository already contains the production helper:

`Invoke-NativeInstallerDiagnostic`

created for the same Windows PowerShell 5.1 failure class.

The helper:

1. saves `$ErrorActionPreference`;
2. temporarily changes it to `Continue`;
3. invokes the native executable with merged stdout/stderr capture;
4. snapshots `$LASTEXITCODE`;
5. restores the caller preference in `finally`;
6. returns `Output` and `ExitCode`.

Existing tests already prove this helper handles native stderr with both nonzero and zero child exit codes on Windows PowerShell 5.1.

The installer already routes `npm ci` and `npm run plugin:validate` through this helper.

The `ticket-db-bootstrap` call is an uncovered direct native invocation of the same unsafe class.

## Required repair

Do not suppress Node warnings globally.

Do not set `NODE_NO_WARNINGS` or alter Node runtime behavior.

Do not weaken installer fail-closed semantics.

Instead, route only the ticket DB bootstrap native child through the existing helper:

```text
Invoke-NativeInstallerDiagnostic
  executable = node
  arguments  = bootstrap-ticket-db.mjs --workspace <workspace>
```

Then:

- print captured output for diagnostics;
- use the helper's captured `ExitCode`;
- complete the existing installer diagnostic stage with that exact exit code;
- throw only when the native child exit code is nonzero;
- include bounded captured child output in a true failure diagnostic.

This is the minimal owning-boundary repair.

## Current production state consequence

The failed installer intentionally left production in installer-owned safe partial state:

- controller passthrough/disabled, generation 106;
- plugin disabled;
- Gateway healthy;
- Recovery/Delivery READY;
- pending outbox 0;
- SQLite integrity OK;
- durable counts unchanged.

Do not manually enable or repair this state before the installer fix is validated.

The next production install-over must begin from this observed partial state under a newly authorized task.

## Reviewer

ChatGPT

Human final authority: Operator
