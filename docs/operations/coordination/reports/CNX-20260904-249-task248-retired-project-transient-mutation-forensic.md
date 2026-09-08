# CNX-20260904-249 — Task-248 Retired Project Transient-Mutation Forensic

## Classification

`BLOCKED_TRANSIENT_MUTATION_ACTOR_UNPROVEN__TDD_MISMATCH_INSTRUMENTATION_REQUIRED`

Task 249 performed read-only forensic work only. It did not invoke the installer, rollover code, lifecycle operations, semantic surfaces, recovery, or any repair. The historical changed path and actor cannot be proven from the available retained evidence. The Task-226 full-tree fail-closed attestation remains unchanged and must not be weakened.

## Fresh authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Fresh authority HEAD before execution: `5fc7ebaab6a4be042518246d7e6ef96e9319ff03`
- Task: `CNX-20260904-249`
- Parent report HEAD: `06b7bc01161efe2c8bbb97fe0e0511d79ff8d62b`
- Parent review commit: `061ba41bb10e89c97fa94debf5fdec7665d275da`
- Public tag: `v0.9.3` still points to `26ce64a624255278a3a0266ad38746e0e6ed2e31`

The task report did not exist at the fresh authority HEAD before this publication.

## Scope and evidence root

Task-248 execution window:

```text
2026-09-04T15:34:42.0554329Z
```

Task-248 retained external rollover backup:

```text
C:/Users/CDQ-P/AppData/Local/CogentNexus-OpenClaw/plugin-generation-rollover-backups/cogentnexus-openclaw-fc6fb357dd4a4c9688e4eb0116c10033
```

Current retired project resolved from the live ownership manifest:

```text
C:/Users/CDQ-P/.openclaw/extensions/cogentnexus-openclaw
```

Task-249 evidence root, separate from both protected trees:

```text
C:/Users/CDQ-P/AppData/Local/CogentNexus-OpenClaw/forensics/CNX-20260904-249
```

Retained evidence manifest:

```text
files = 8
manifest SHA-256 = 71e26057f1aa32758bc3a4726fc62f05fcda779e36bbe6172ec0d640111c30bd
```

No credentials or secrets were copied into the evidence root.

## Current tree and per-path comparison

The same producer helper `_project_tree_sha256()` from the exact Task-248 source checkout was used for both full-tree digests. Both trees currently have:

```text
retired project tree SHA-256 = 900ac13f85a6de75e40a632a534f2b0ceef53def1e8387fc3530c02a7413de58
backup tree SHA-256            = 900ac13f85a6de75e40a632a534f2b0ceef53def1e8387fc3530c02a7413de58
```

Complete inventories were captured as:

- `retired-inventory.json`
- `backup-inventory.json`
- `inventory-summary.json`
- `comparison-classified.json`

Inventory counts:

```text
retired entries = 35,693
backup entries  = 35,693
```

Comparison classification:

```text
regular-file/symlink/object content differences = 0
missing or extra object paths = 0
directory metadata differences = 2,037
```

The 2,037 directory metadata differences are supporting metadata from the copy operation (directory size/creation metadata); they are not regular-file content or symlink differences and are not included in the full-tree digest contract. The current post-failure equality does not prove equality at the historical failed comparison.

The digest implementation hashes path/type/size/content/symlink state and does not hash mtime. Therefore mtime-only drift is not offered as an explanation for the Task-248 mismatch.

The Task-248 backup and retired tree remained present. Neither protected tree was written, deleted, renamed, or cleaned by Task 249.

## Historical evidence queried

### NTFS/USN

A bounded `fsutil usn readdata` query was retained in `usn-query.json`. It returned only a directory record for `cogentnexus-openclaw`:

```text
Reason: 0x0
Time Stamp: 1/1/1601 12:00:00 AM
```

It did not provide per-file historical changes or a usable actor association. A bounded per-file USN history was therefore not available from this query path.

### Windows event logs

A bounded query covered `2026-09-04T15:20:00Z` through `2026-09-04T15:50:00Z` for:

- `Microsoft-Windows-TaskScheduler/Operational`
- `Windows PowerShell`
- `System`
- `Application`
- `Microsoft-Windows-Windows Defender/Operational`

Raw result: `windows-events-bounded.json`.

No matching Task Scheduler event was found. The PowerShell results were query/helper activity and did not identify a writer under the retired project. No bounded event result identified a file path plus causal actor for the mismatch. Event-log retention/filtering is an evidence limitation, not proof that no historical event occurred.

### Process evidence

`process-snapshot.json` preserved a read-only post-event process snapshot. It showed the long-lived OpenClaw gateway and the current forensic/query shell processes, but no surviving Task-248 installer child or historical writer with a causal association to the retired project. Process snapshots taken after termination cannot reconstruct a historical actor.

### Retained Task-248 evidence

Task-248 runner, transcript, stdout/stderr, manifest, and postflight evidence were already retained under:

```text
C:/Users/CDQ-P/AppData/Local/CogentNexus-OpenClaw/forensics/CNX-20260904-248
```

That evidence proves the exact exception and terminal stage, but contains no source-vs-backup per-path delta recorded at the failed attestation boundary and no writer identity.

No additional OpenClaw/npm/Defender evidence available through the bounded queries identified a path/actor pair.

## Passive observation

A strictly passive read-only observation ran for approximately 120 seconds. It computed the retired-project full-tree digest six times and did not launch or stimulate any product operation.

Evidence: `passive-hash-observation.json`.

Samples:

```text
2026-09-04T16:07:06.626414Z  900ac13f...
2026-09-04T16:07:28.828960Z  900ac13f...
2026-09-04T16:07:51.049611Z  900ac13f...
2026-09-04T16:08:13.216344Z  900ac13f...
2026-09-04T16:08:35.431229Z  900ac13f...
2026-09-04T16:08:57.644318Z  900ac13f...
```

All six full digests were identical. No spontaneous mutation occurred during this observation. This absence does not prove that no mutation occurred during Task 248.

## Candidate mutable paths and actors

| Candidate | Payload classification | Current comparison | Historical evidence | Actor | Confidence |
|---|---|---|---|---|---|
| Retired project regular files/symlinks | Payload and non-payload mixed | No current content/object difference from backup | No per-file USN/event delta retained | Unresolved | None |
| Retired project directories | Non-payload metadata | 2,037 copy-related metadata differences; no content/object difference | No causal historical event | Unresolved | None |
| `node_modules` subtree | Non-payload/package dependency tree | No regular-file/symlink difference; directory metadata differs | No historical writer evidence | Unresolved | None |

These are candidate classes only, not a claim that any listed path caused the mismatch. Filename, directory metadata, and current equality are insufficient to infer an actor.

## Required adjudication

The historical evidence is insufficient to identify either the transient changed path or its process/actor. The result is therefore:

```text
BLOCKED_TRANSIENT_MUTATION_ACTOR_UNPROVEN__TDD_MISMATCH_INSTRUMENTATION_REQUIRED
```

A separate repository-only TDD successor is recommended. It should augment the mismatch diagnostic with source-vs-backup per-path digest differences captured immediately before raising the existing exception, while preserving:

```text
RuntimeError: pre-install backup project-tree attestation mismatch
```

and the existing Task-226 fail-closed behavior. It must not ignore the mismatch, reduce the proof to package payloads, exclude a path merely to make installation pass, retry until equality, or delete the retained backup. Task 249 did not implement this instrumentation.

## Effect ledger

```text
scripts/install.ps1 invocations = 0
installer Scheduled Task registrations/starts = 0
prepare_plugin_rollover_transaction invocations = 0
rollover prepare/finalize = 0
plugin install/copy/delete/rename = 0
retired-project writes = 0
Task248 rollover-backup writes/deletes/renames = 0
controller/Gateway/provider/model lifecycle mutation = 0
Ticket/outbox/recovery/SQLite mutation = 0
Dashboard semantic sends = 0
Discord semantic sends = 0
direct API semantic sends = 0
recovery replay/resend = 0
process termination = 0
production/source/test/workflow edits = 0
release/tag/history mutation = 0
```

Allowed actions were limited to read-only hashing, enumeration, evidence queries, passive observation, and writing evidence below the separate Task-249 evidence root.

## Conclusion and stop boundary

Task-248's intentional fail-closed attestation detected a historical mismatch, but the available post-failure state and bounded forensic evidence cannot reconstruct the transient path or actor. The safety invariant remains intact. No installer retry, cleanup, repair, or semantic acceptance is authorized by Task 249.

Report-only publication is complete only after remote verification below. STOP for independent ChatGPT review.
