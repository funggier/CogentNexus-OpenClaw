# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK223_EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFICATION`  
**Updated:** 2026-09-02 ICT  
**Transport:** GitHub repository + authenticated Windows install evidence through Hermes  
**Active task:** `CNX-20260902-223`  
**Parent:** `CNX-20260901-222`  
**Repair parent:** `CNX-20260831-198`  
**Parent umbrella:** `CNX-20260831-188`  
**Completed publication:** `CNX-20260831-197`  
**Disposition:** `TASK222_PACKAGE_PROVENANCE_ACCEPTED__TASK223_WINDOWS_INSTALL_OVER_READY`

## Publication authority

Published public `v0.9.3` remains untouched at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Task 222 accepted boundary

Task-222 report disposition:

`PASS_STATIC_BYTE_GUARD__CI_WINDOWS_PAYLOAD_IDENTITY_EQUAL`

Independent review disposition:

`ACCEPT_PASS_STATIC_BYTE_GUARD__CI_WINDOWS_PAYLOAD_IDENTITY_EQUAL__WINDOWS_INSTALLER_REQUALIFICATION_AUTHORIZED`

Exact installer candidate:

`a812f27815b3c87b7ca748dc2dea88f987601f70`

Exact accepted package proof:

```text
artifact 9810139538
digest sha256:3164b7770e7d8991691d7bbedced092866c208add72b0c03b4aa3d39d1b50ff0
file count 192
fingerprint e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
```

Exact candidate CI:

```text
Validate 33532084137 success
Windows Installer Pack Smoke 33532084225 success
PS5.1 Acceptance Smoke 33532084092 success
```

Task 222 independently closes the prior cross-platform package identity blocker: fresh Windows exact-first materialization and authoritative CI had the same 192 payload paths, zero byte differences, exact same fingerprint, and clean tracked state.

## Active Task 223

Hermes must execute:

`docs/operations/coordination/tasks/CNX-20260902-223-task222-exact-candidate-windows-install-over-requalification.md`

Key execution rules:

- fresh exact-first candidate source materialization only;
- reprove candidate package identity before installer;
- use the direct Scheduled Task PowerShell terminal topology qualified by Task 215;
- never use the failed detached Popen launcher;
- one unique temporary Task-223 Scheduled Task;
- at least 30-minute execution limit;
- exactly one installer invocation and no retry;
- passive observation until terminal evidence;
- installed fingerprint/source must bind exactly to `a812f278...` / `e3bcce04...`;
- post-install controller/startup/Gateway/Ollama/delivery/recovery/SQLite health must be coherent;
- stop after report for independent review.

If Task 223 passes independent review, a later successor may authorize the final bounded one-Send Discord semantic/durable-delivery requalification.

## Discord / mutation boundary

`0 Discord Sends`.

No installer retry, reset/uninstall/fresh reinstall, manual lifecycle repair, manual Gateway restart, manual plugin/config/SQLite write, provider/model substitution, unrelated process termination, product/source edit, Release/tag mutation, or force push is authorized.
