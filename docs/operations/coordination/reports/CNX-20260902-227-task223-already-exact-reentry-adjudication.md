# CNX-20260902-227 — Task-223 Already-Exact Re-entry Adjudication

Date: 2026-09-02 ICT  
Primary disposition: `BLOCKED_STALE_EVIDENCE_DRIFT`  
Parent: `CNX-20260902-226`  
Failure parent: `CNX-20260902-223`

## Decision

Task 227 was authorized as read-only adjudication. It did not invoke the installer, rollover prepare/finalize, lifecycle actions, Gateway restart, SQLite write, process termination, provider/model substitution, or Discord traffic.

The task is blocked because retained evidence changed materially relative to the accepted Task-224/Task-227 baseline. The matching retained inventory file, previously observed absent, is now present:

```text
C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\install-staging\plugin-inventory-8469daf5669242189f18e8c87ed9a86c.json
```

Task-227 requires stopping with `BLOCKED_STALE_EVIDENCE_DRIFT` when transaction/backup evidence changes. The file was not opened, consumed, edited, moved, renamed, deleted, or treated as authority. No actor is inferred from its appearance.

## Fresh authority and drift gate

Fresh remote branch:

```text
branch: agent/v0.9.3-full-stabilization
remote HEAD: 7ac15110fc1a1cc43ec6945dfd60f2973c3fb843
```

Active authority:

```text
Task: CNX-20260902-227
Status: READY_FOR_HERMES
Execution mode: TASK227_TASK223_ALREADY_EXACT_REENTRY_ADJUDICATION
accepted repair: 9a8510f1317c8e53c01c233b080ec20357cd22df
expected fingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
```

The coordination `STATUS.md` still described Task 226 while `ACTIVE.md` described Task 227. This coordination inconsistency was recorded and not overridden by assumption; the Task-227 task file and ACTIVE authority were used for the bounded read-only inspection.

Accepted public release remained immutable:

```text
v0.9.3: 26ce64a624255278a3a0266ad38746e0e6ed2e31
```

Product/source drift gate: no product/source/test/workflow changes were made by this executor. Current source after the accepted repair contains only coordination/task/report/review changes relative to the repair commit.

## Evidence root

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx227-already-exact-reentry-20260902T142252Z\
```

Fresh inventory capture:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx227-already-exact-reentry-20260902T142252Z\plugin-inventory.json
bytes: 151428
SHA-256: 7ea6fd65583cda80b8456fd745e41b6f0fb00ac2c8ce1b0b6c775d318ccae5a3
```

The first capture attempt timed out without a valid artifact; after the process disappeared, one supported `openclaw.cmd plugins list --json` capture completed and was saved above. No second successful capture was used.

## Phase B — live preservation

Fresh read-only state:

```text
controller mode: passthrough
generation: 33
startup adapter: installed=false
Gateway: healthy, loopback 127.0.0.1:18789
provider: ollama
Delivery: READY, pending=0, readOnly=true, stateChanged=false
Recovery: READY, readOnly=true, stateChanged=false
SQLite: integrity=ok, tickets=11, ticket_events=86
Task-223 temporary task: absent
```

Canonical installed plugin identity was observed through the supported fingerprint helper:

```text
root: c:\users\cdq-p\.openclaw\extensions\cogentnexus-openclaw
version: 0.9.3
fingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
```

## Phase C — retained transaction and backup

Transaction:

```text
path: C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\install-staging\plugin-rollover-transaction-8469daf5669242189f18e8c87ed9a86c.json
bytes: 2124
SHA-256: ec1b32ec2813e1b4e2c220679f39c6922789b7d77e88ec9ca4ad6ba82ccac510
```

The transaction SHA remained exactly equal to the Task-224 accepted value.

Retained backup, recomputed with current repaired helper read semantics:

```text
path: C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\plugin-generation-rollover-backups\cogentnexus-openclaw-8469daf5669242189f18e8c87ed9a86c
project-tree SHA-256: 7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a
payload file count: 190
payload fingerprint: f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
```

The transaction still contains the known obsolete mismatch:

```text
backupProjectTreeSha256: 7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a
retiredProjectTreeSha256: ca74a262293d49b058fce6221db2fa5311214cde567ebb331ff845670c5a2cab
```

Matching inventory status changed during the adjudication window:

```text
Task-224 accepted observation: absent
Task-227 final observation: present
bytes: 156245
mtime: 2026-09-02 06:00:31.587591100 +0700
SHA-256: 1a7299f926cda4e3f936577204c50059e0e4e716f8594535d4b3c40c40e51477
```

The inventory file timestamp coincides with the historical Task-223 post-replacement stage interval, but no actor is attributed. This is sufficient to trigger stale-evidence blocking; it is not evidence of a new installer invocation by this executor.

## Phase D — candidate exactness

The exact current source candidate and installed direct plugin were independently fingerprinted using the candidate helper:

```text
source fingerprint:    e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
installed fingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
expected fingerprint:  e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
version: 0.9.3
```

The successful read-only classification performed before the stale-file discrepancy was adjudicated returned:

```json
{
  "mode": "upgrade",
  "pendingRollover": false,
  "pluginAlreadyExact": true,
  "manifestPluginPath": "c:\\users\\cdq-p\\.openclaw\\extensions\\cogentnexus-openclaw",
  "replacementPluginPath": "c:\\users\\cdq-p\\.openclaw\\extensions\\cogentnexus-openclaw"
}
```

This result is preserved as diagnostic evidence only. It cannot override the Phase-C stale-evidence gate.

## Phase E — production action resolver

Pure resolver input:

```text
Mode=upgrade
PluginAlreadyExact=true
SkipPlugin=false
```

Result:

```json
{
  "mode": "upgrade",
  "pendingRollover": false,
  "pluginAlreadyExact": true,
  "skipPlugin": false,
  "installPlugin": false,
  "rolloverPlugin": false
}
```

This confirms the supported already-exact branch, but Task 227 cannot grant re-entry authority after stale-evidence drift.

## Phase F — stale transaction non-selection

Current source inspection proves:

1. `$rolloverTransactionPath` is initialized to `$null` per installer invocation.
2. A new GUID path is generated only inside `classification.mode -eq "upgrade" -and $actions.rolloverPlugin`.
3. `rollover-prepare` is called only in that branch.
4. `rollover-finalize` is called only when that current invocation created `$rolloverTransactionPath`.
5. The installer does not enumerate or auto-resume arbitrary existing `plugin-rollover-transaction-*.json` files.
6. With `pluginAlreadyExact=true`, the resolver returns `installPlugin=false` and `rolloverPlugin=false`.

Therefore the obsolete Task-223 transaction is not selected by the current installer control flow. This source proof does not authorize invoking the installer.

## Phase G — final preservation

Final read-only checks:

```text
transaction SHA: unchanged at ec1b32ec2813e1b4e2c220679f39c6922789b7d77e88ec9ca4ad6ba82ccac510
ownership manifest: unchanged during classification/resolver reads
controller: passthrough, generation 33
Gateway: healthy
provider: ollama
Delivery: READY
Recovery: READY
SQLite integrity: ok
Task-223 temporary task: absent
```

The one matching process observation during a probe was the probe command's own PowerShell command line; it disappeared after the probe. No known installer/runner process remained. No process was terminated.

## Mutation ledger

```text
installer invocations: 0
rollover-prepare invocations: 0
rollover-finalize invocations: 0
manual lifecycle actions: 0
Gateway restarts: 0
plugin/config/ownership/transaction/backup writes: 0
SQLite writes: 0
process terminations: 0
provider/model substitutions: 0
Discord Sends/API semantic traffic: 0
Release/tag/asset mutations: 0
force pushes/history rewrites: 0
product/source/test/workflow edits by executor: 0
```

The only mutation authorized and performed is publication of this coordination report.

## Stop boundary

```text
BLOCKED_STALE_EVIDENCE_DRIFT
```

Do not delete, edit, move, rename, finalize, archive, or reuse the newly-present inventory or obsolete transaction. Do not invoke installer, rollover prepare/finalize, lifecycle actions, Gateway restart, or Discord traffic. Await independent review and a new bounded cleanup/re-entry authority.
