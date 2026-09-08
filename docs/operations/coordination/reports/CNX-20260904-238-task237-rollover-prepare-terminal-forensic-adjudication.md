# CNX-20260904-238 — Task237 Rollover-Prepare Terminal Forensic Adjudication

## Final disposition

`BLOCKED_EXACT_PREPARE_ERROR_UNPROVEN`

Observability classification:

`OBSERVABILITY_DEFECT_PROVEN`

Task 238 was read-only forensic work. No installer, rollover prepare/finalize,
plugin lifecycle, managed re-enable, semantic delivery, recovery replay, or
manual durable-state mutation was performed.

The retained evidence proves that Task 237 created a backup during
`plugin-rollover-prepare` and that the backup currently matches the retired
project exactly. It does not preserve the Python diagnostic output that would
identify the exception raised during the original prepare call. Therefore the
exact runtime failing invariant cannot be adjudicated conclusively without
rerunning the forbidden operation.

## Fresh authority and preservation gate

Remote branch was fetched immediately before forensic work.

- Remote authority HEAD: `f38bcbcb31f07751a610ed106d7f4f88b41667e4`
- Active task: `CNX-20260904-238`
- Status: `READY_FOR_HERMES`
- Parent: `CNX-20260904-237`
- Task-237 disposition accepted by authority:
  `FAIL_INSTALLER_TERMINAL`
- Task-237 review:
  `ACCEPT_FAIL_INSTALLER_TERMINAL__ROLLOVER_PREPARE_EXACT_INVARIANT_UNPROVEN__READ_ONLY_FORENSIC_SUCCESSOR_REQUIRED`
- Accepted candidate remains:
  `ffb0dd4ed47affe2e496c17b74ca74d358905bd7`
- Expected candidate fingerprint:
  `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- Public `v0.9.3` remains immutable:
  `26ce64a624255278a3a0266ad38746e0e6ed2e31`

Fresh live preservation capture remained consistent with the required
post-failure boundary:

- controller: `passthrough`
- generation: `39`
- Gateway healthy at `127.0.0.1:18789`
- provider: `ollama`, healthy/ready
- Delivery: `READY`, pending outbox `0`
- Recovery: `READY`, no active incident/replay
- SQLite integrity: `ok`
- candidate plugin not installed; predecessor remains effective
- semantic submissions remain `0`

No unexplained live mutation was observed during forensic capture.

## Preserved Task-237 evidence

Evidence root used for forensic artifacts:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx238-forensic-20260904T
```

The following Task-237 evidence roots/files were inventoried and hashed without
editing originals:

| Evidence | File count | Tree SHA-256 |
|---|---:|---|
| `cnx237-preflight-20260904T` | 7 | `7e4825f9bf61b3c48ac0837c74c93b4ddc8fd7bc95231ea43ab7cdb59cc1d35f` |
| `cnx237-install-evidence-20260904T` | 3 | `d10d970b25e8e750f62c59479294160f09ed4002b0c6e61fc2c15d201b424de7` |
| `cnx237-post-20260904T` | 8 | `a7e9ec3b3203640c33e2d0c974adab808115278cfe97504d5a2974f54504a0ab` |
| `cnx237-registration.json` | 1 | `3d4e366c4f7d6954266dd65cbbae48950e0d251ae14b49369efb8b922a9be550` |
| `cnx237-registration-readback.json` | 1 | `4b669e7a5862d42838d310e11dc227e9839af24f8ab10a968fc3fcc32919e065` |
| `cnx237-installer-runner.ps1` | 1 | `ba5051832ccb24baf2f8a3c9032e865c74bbb67ee3cc479d602c51f2955c27a4` |

The complete application-data backup root contained `201,910` files and
`12,228` directories; its forensic tree hash was:

```text
fbfaa6ad277ccc98335550faed8dd56292f3a1a5292bce34192c2b3f7abaf0e2
```

Task-237 installer transcript and terminal record showed:

- invocation: `2026-09-04T00:46:05.8009488+00:00`
- prepare start: `2026-09-04T00:49:12.1697303+00:00`
- prepare terminal: `2026-09-04T00:53:07.7339796+00:00`
- wrapper error: `ownership-safe plugin generation rollover pre-install proof failed`
- installer exit: `1`
- scheduled task `LastTaskResult`: `1`

No Python traceback or actionable `RuntimeError` was present in the retained
transcript/terminal output.

## Recovered rollover identity and artifact inventory

Recovered backup token / rollover ID:

```text
c6aaf93db7c34f718d01302477a292e1
```

Backup path:

```text
C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\plugin-generation-rollover-backups\cogentnexus-openclaw-c6aaf93db7c34f718d01302477a292e1
```

Directory metadata:

- Creation time: `2026-09-04T00:49:12.2851993Z`
- Last-write time: `2026-09-01T23:00:14.2787063Z` (source file timestamps were
  preserved by the copy operation and are not used as creation proof)
- files: `33,656`
- directories: `2,037`

The creation timestamp is inside the Task-237 prepare window and immediately
follows the prepare start, proving this backup belongs to Task 237 rather than
the older retained rollover artifacts.

No matching transaction file named for token `c6aaf...` exists in:

```text
C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\install-staging
```

The staging directory remained a small retained set of eight historical files;
no Task-237 transaction was persisted.

Task-237's separate skill backup was also preserved:

```text
C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\install-backups\cogentnexus-openclaw-20260904-074902
```

It was created at `2026-09-04T00:49:02.5279003Z` and contained 125 files.

## Exact tree/payload comparison

The source helper's own `_project_tree_sha256` and `plugin_fingerprint`
functions were used for the comparison. No hashing algorithm was reimplemented.

| Object | Project-tree SHA-256 | Payload fingerprint | Payload version |
|---|---|---|---|
| Current retired plugin tree `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw` | `900ac13f85a6de75e40a632a534f2b0ceef53def1e8387fc3530c02a7413de58` | `e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386` | `0.9.3` |
| Task-237 backup `...\\cogentnexus-openclaw-c6aaf...` | `900ac13f85a6de75e40a632a534f2b0ceef53def1e8387fc3530c02a7413de58` | `e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386` | `0.9.3` |

The full project-tree hash and package payload fingerprint both match. This
rules out a persistent post-copy mismatch in the retained artifacts. It does
not prove that the two hashes matched at the instant of the original prepare
comparison; a transient file/access/race condition during that execution
remains possible, but is not proven.

## Source-order invariant elimination

The exact candidate source implements `prepare_plugin_rollover_transaction` in
this order:

1. require passthrough mode;
2. verify ownership manifest;
3. resolve the manifest-owned retired plugin payload;
4. validate the expected replacement fingerprint format;
5. validate the external application-data boundary;
6. validate the backup token safety;
7. resolve the retired managed project root;
8. reject an existing/unsafe backup destination;
9. create the backup directory and copy the retired project;
10. hash retired and backup trees;
11. reject if those hashes differ;
12. return the transaction object;
13. atomically write the transaction path in the CLI command handler.

Retained evidence proves:

- passthrough handoff succeeded;
- manifest and candidate plugin validation completed before prepare;
- a safe-looking token produced a backup inside the expected external
  application-data boundary;
- the backup was created during prepare;
- current and backup tree/payload identities match;
- no transaction was written.

Therefore the evidence excludes a persistent failure at the finalization or
post-install stages and strongly localizes the original failure to the
prepare/copy/hash interval before transaction persistence. It cannot select
between a transient hash mismatch and another exception in that interval,
because the child diagnostic was not retained.

It is not valid to label this specifically
`pre-install backup project-tree attestation mismatch`: the retained artifacts
currently match, and the original child error was not preserved.

It is also not valid to label this a recurrence of Task-140/Task-226/Task-223
solely from the generic wrapper. Those lineages remain historical comparisons,
not proven causes of Task 237.

## Observability adjudication

The exact candidate installer contains:

```powershell
$prepareOutput = (& python ... rollover-prepare ... | Out-String)
$rolloverPrepareExit = $LASTEXITCODE
Complete-InstallerDiagnosticStage ... -ExitCode $rolloverPrepareExit
if ($rolloverPrepareExit -ne 0) { throw "ownership-safe plugin generation rollover pre-install proof failed" }
```

The captured `$prepareOutput` is not emitted or persisted on nonzero exit. The
transcript therefore retains only the generic PowerShell wrapper message and
stage timing/exit code, not the actionable Python exception. This conclusively
proves:

```text
OBSERVABILITY_DEFECT_PROVEN
```

A later repository task should add a bounded, redacted diagnostic preservation
path for prepare failure, without weakening fail-closed semantics or changing
rollover behavior. Task 238 made no source edit.

## Retry / tooling ledger

| Logical operation | Attempt | Method/result | Could product state change? | Retry classification |
|---|---:|---|---|---|
| Fresh authority | 1 | fetch/read exact remote authority | No | no retry needed |
| Live preservation checks | 1 | status/delivery/recovery/plugin/SQLite read-only queries | No | no retry needed |
| Evidence inventory/hash | 1 | initial inline inventory script quoting error | No | changed to file-based script |
| Evidence inventory/hash | 2 | background file-based inventory completed | No | effective |
| Directory metadata | 1 | file-based PowerShell read-only query completed | No | no retry needed |
| Tree/payload comparison | 1 | source helper functions completed in background | No | no retry needed |
| Installer/rollover execution | 0 | explicitly forbidden by Task 238 | N/A | product boundary stopped it |

Final retry classification:

`RETRY_POLICY_EFFECTIVE`

The only retry was a tooling/evidence collection retry with a materially
changed method. No product operation was retried.

## Zero-mutation ledger

```text
installer registration/start/invocation during Task 238: 0
direct rollover-prepare/finalize during Task 238: 0
manual plugin lifecycle mutation: 0
manual managed re-enable/lifecycle/Gateway repair: 0
manual Ticket/outbox/recovery/SQLite writes: 0
Dashboard semantic submissions: 0
Discord semantic submissions: 0
direct operator Discord/API Sends: 0
recovery replay/resend: 0
process termination: 0
provider/model substitution: 0
Task-237/Task-223/Task-233 evidence mutation: 0
reset/uninstall/reinstall: 0
Release/tag/asset mutation: 0
force push/history rewrite: 0
```

## Stop boundary

Task 238 cannot prove the exact original prepare invariant from retained
artifacts. The required next step, if desired, is a separately authorized
source observability repair and a new explicitly gated installation task. Do
not rerun the installer, call rollover prepare directly, manually re-enable
managed mode, repair plugin identity, or replay any semantic lineage from this
report.
