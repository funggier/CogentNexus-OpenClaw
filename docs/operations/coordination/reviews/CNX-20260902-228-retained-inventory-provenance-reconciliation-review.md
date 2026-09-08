# Independent Review — CNX-20260902-228 Retained Inventory Provenance Reconciliation

Date: 2026-09-02 ICT  
Coordinator / final reviewer: ChatGPT

## Verdict

`ACCEPT_PASS_HISTORICAL_TASK223_ARTIFACT_RECONCILED__ONE_CONTROLLED_ALREADY_EXACT_INSTALLER_REENTRY_AUTHORIZED`

Task 228 is accepted as sufficient read-only reconciliation of the Task-227 stale-evidence blocker.

The retained matching inventory is accepted as a historical Task-223 artifact, not as evidence of a later Task-227/228 mutation. This review does not claim to reconstruct why Task 224 observed it as absent; that historical false-negative mechanism remains unproven and is not required to proceed because current provenance evidence independently binds the file to the original Task-223 finalization interval.

## Fresh repository authority

Task-228 report HEAD:

`11f788159aadb943bedb8a65ada8f1d0670c5756`

Fresh compare from accepted production repair:

`9a8510f1317c8e53c01c233b080ec20357cd22df -> 11f788159aadb943bedb8a65ada8f1d0670c5756`

shows no product/source/test/workflow drift after the repair; only coordination/report/review/task lineage changed.

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Accepted provenance reconciliation

The matching inventory:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\install-staging\plugin-inventory-8469daf5669242189f18e8c87ed9a86c.json`

was proved with the following independent properties:

- `CreationTimeUtc == LastWriteTimeUtc == 2026-09-01T23:00:31.5875911Z`;
- that instant equals the historical Task-223 `plugin-rollover-finalize` stage start;
- current installer source order writes the matching inventory immediately before starting the finalizer stage;
- the file is a normal file, not reparse/link storage;
- SHA-256 remains `1a7299f926cda4e3f936577204c50059e0e4e716f8594535d4b3c40c40e51477`;
- parsed product registration binds the exact canonical Task-223 replacement at `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`;
- parsed fingerprint is the accepted candidate `e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`;
- no later write/copy/restore evidence was found.

Together these are sufficient to classify the file as:

`HISTORICAL_TASK223_ARTIFACT`

The Task-224 statement that the file was absent is retained as an observation limitation. No invented actor or false-negative mechanism is accepted.

## Obsolete transaction boundary remains unchanged

The historical transaction is still internally inconsistent:

```text
backupProjectTreeSha256  = 7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a
retiredProjectTreeSha256 = ca74a262293d49b058fce6221db2fa5311214cde567ebb331ff845670c5a2cab
```

Therefore the historical transaction remains obsolete producer-defect evidence. The presence of the historical inventory does not make it valid.

A successor must not finalize, edit, move, rename, delete, archive, or reuse the Task-223 transaction, inventory, or backup.

## Already-exact re-entry accepted

Task 227 and Task 228 independently proved current classification:

```text
mode=upgrade
pendingRollover=false
pluginAlreadyExact=true
```

and production action resolution:

```text
installPlugin=false
rolloverPlugin=false
```

Current installer control flow initializes its transaction path per invocation and does not enumerate or auto-resume historical rollover transactions. Therefore the stale Task-223 transaction is not selected by an already-exact re-entry.

## Exact live installer source authority

The successor must use exact repaired source commit:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

not the older Task-223 source `a812f278...`.

Reason: even when plugin installation is skipped, `scripts/install.ps1` later stages/copies the candidate skill tree into the live workspace. The repaired source must therefore become the installed skill authority; using the older source would republish the pre-Task-226 producer implementation.

The plugin payload identity remains:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

because the Task-226 repair changed the skill-side Python ownership implementation, not the plugin payload.

## Fresh CI verification

All required workflows on Task-228 report HEAD `11f788159...` completed successfully:

```text
Validate:                      33646023883  SUCCESS
Windows Installer Pack Smoke: 33646023869  SUCCESS
PS5.1 Acceptance Smoke:        33646023697  SUCCESS
```

Validate includes successful Python test/compile/self-test gates, Windows PowerShell syntax/smoke gates, npm test/evaluation/audit/plugin validation, and package dry-run.

## Authorization boundary

A successor Task 229 may authorize exactly one controlled Windows installer re-entry using the exact repaired source `9a8510f...`, but only after fresh preflight re-proves:

```text
installed plugin fingerprint == e3bcce04...
classification == upgrade + pendingRollover=false + pluginAlreadyExact=true
actions == installPlugin=false + rolloverPlugin=false
stale Task-223 transaction/inventory/backup identities unchanged
controller/runtime state remains safe for the documented installer lifecycle
```

The successor may allow the installer itself to perform its documented non-plugin install/ownership/policy/host lifecycle. It must not allow manual lifecycle repair outside that one installer invocation.

Still prohibited until separately authorized:

- any stale transaction/inventory/backup cleanup or finalize;
- installer retry after one terminal attempt;
- manual plugin installation or rollover;
- manual Gateway/lifecycle repair outside the installer;
- provider/model substitution;
- Discord Send/API semantic traffic;
- public Release/tag/asset mutation;
- force push/history rewrite.

Discord budget remains `0 Sends`.

## Final disposition

`ACCEPT_PASS_HISTORICAL_TASK223_ARTIFACT_RECONCILED__ONE_CONTROLLED_ALREADY_EXACT_INSTALLER_REENTRY_AUTHORIZED`
