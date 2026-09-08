# CNX-20260904-246 — Task-245 Rollover-Prepare Terminal Forensic / Evidence Preservation

## Disposition

`BLOCKED_EXACT_EXCEPTION_UNPROVEN`

Task 245 evidence was preserved byte-identically before analysis. The retained stderr proves that Python entered a traceback at the `plugin-rollover-prepare` invocation, but the captured stream ends after `Traceback (most recent call last):` and PowerShell's wrapper metadata. The exception type, message, traceback frame, and failing invariant/sub-operation are therefore not recoverable from the retained bytes. No speculation or installer retry was performed.

## Fresh authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Fresh authority HEAD before execution: `b79c0f3d61cf8c68d1ea0c5626cbb07d3ea088df`
- Task: `CNX-20260904-246`
- Parent: `CNX-20260904-245`
- Reviewed Task-245 report HEAD: `5984e3dfe3503bee37c218cb1f34eff16a071bef`
- Exact candidate: `18a51b15768fb3d2196e65f1ef470c34aeef7f36`
- Candidate plugin fingerprint: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

The fresh `ACTIVE.md` and `STATUS.md` both authorized forensic-only Task 246 with a zero-effect budget and required stopping after report publication.

## Evidence preservation

Task-245 temporary roots were present:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx245-install-evidence-20260904T
C:/Users/CDQ-P/AppData/Local/Temp/cnx245-runner-20260904T
```

They were copied, without editing or deletion, to:

```text
C:/Users/CDQ-P/AppData/Local/CogentNexus-OpenClaw/forensics/CNX-20260904-246/
```

Preservation manifest:

```text
C:/Users/CDQ-P/AppData/Local/CogentNexus-OpenClaw/forensics/CNX-20260904-246/preservation-manifest.json
```

- artifacts copied: `34`
- missing source artifacts: `0`
- source/destination SHA-256 equality: `34/34`
- source and destination sizes matched for every copied file
- originals were not deleted or modified

The archive is the forensic working copy. Relevant preserved files include complete `child-stderr.txt`, `child-stdout.txt`, `runner-transcript.txt`, `runner-result.json`, `runner-started.json`, `launch-manifest.json`, `observation.log`, post-check JSON files, frozen runner source, and the corresponding hashes.

The preservation manifest itself was generated in the designated non-temp forensic archive; its source/destination hash records are the byte-identity proof for the copy operation.

## Exact retained terminal evidence

Evidence archive subtree:

```text
C:/Users/CDQ-P/AppData/Local/CogentNexus-OpenClaw/forensics/CNX-20260904-246/cnx245-install-evidence-20260904T/
```

Exact relevant hashes:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `child-stderr.txt` | 1,281 | `7bae8839042611332a600e113122a0c6faa06fdcae62868c0beb72739c907836` |
| `child-stdout.txt` | 3,431 | `bc41c573f4bf89ca2a3b6d8e9c2b5e3421404a1fd1370904732890e749cadfab` |
| `runner-transcript.txt` | 4,741 | `ac8c13fcc6e40d1df3034509e6fa847aff12a58b8d98fb7c5a0eaee102de671b` |
| `runner-started.json` | 1,470 | `35cac78e35b3eecc6c87099b67077860ec9c20e0a194c5bc24f1bc7eec4dfdb3` |
| `runner-result.json` | 985 | `7529bb0550297c198f76723e73f83b477eb8765096adb309694400deefe3dd11` |
| `launch-manifest.json` | 1,217 | `d00e5061aaf73ca902f63f2aa367dfbc88a0064551e13b017f61d83a0b68869a` |

The retained `runner-result.json` states:

```text
outcome = child_nonzero_exit
childStarted = true
childExitCode = 1
transcriptWriteSucceeded = true
fallbackWriteSucceeded = false
```

The retained `runner-transcript.txt` and `child-stdout.txt` show:

```text
CNXCLAW_INSTALL_STAGE_COMPLETE stage=ticket-db-bootstrap ... exit_code=0
CNXCLAW_INSTALL_STAGE_COMPLETE stage=plugin-npm-pack ... exit_code=0
CNXCLAW_INSTALL_STAGE_START stage=plugin-rollover-prepare ...
```

The complete retained `child-stderr.txt` contains only npm warnings followed by:

```text
python.exe : Traceback (most recent call last):
At C:\Users\CDQ-P\AppData\Local\Temp\cnx244-exact-source-20260904T\scripts\install.ps1:401 char:35
+ ... reOutput = (& python (Join-Path $targetSkill "scripts\\namespace_owner ...
+                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Traceback (most recent call last)::String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
```

No exception class, message, source frame, or final traceback line exists in the preserved stderr/transcript bytes. The runner itself had no exception (`exceptionType=null`, `exceptionMessage=null`); it correctly recorded the child's nonzero exit.

The manifest remains bound to the exact candidate installer:

```text
childExecutable = C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe
-File C:/Users/CDQ-P/AppData/Local/Temp/cnx244-exact-source-20260904T/scripts/install.ps1
sourceCandidateSha = 18a51b15768fb3d2196e65f1ef470c34aeef7f36
runnerSha256 = 0c2da0cb5877ca9493e4921c3a7b5492dd884841a2bd68c3fb63032b6e42eb98
```

Task 245's exact source and manifest-binding proof are accepted and are not reopened.

## Rollover-prepare source correlation

The exact candidate source defines `prepare_plugin_rollover_transaction()` in:

```text
skills/cogentnexus-openclaw/scripts/namespace_ownership.py:877
```

The ordered operations are:

1. resolve root, workspace, and application-data paths;
2. derive expected paths;
3. require passthrough mode;
4. verify the ownership manifest;
5. resolve and prove the retired plugin payload;
6. validate the expected replacement fingerprint;
7. validate the external application-data boundary;
8. validate the backup token;
9. resolve the retired npm project;
10. reject an invalid/existing backup destination;
11. create the external backup directory and copy the retired project;
12. hash retired and backup project trees;
13. assert tree-hash equality;
14. return the transaction object.

The installer invokes this function through `install.ps1:401`. The installer writes the rollover transaction JSON only after this call returns successfully. The absence of a new Task-245 transaction therefore proves that successful return was not reached, but the incomplete traceback cannot identify which ordered operation raised.

## Backup-domain inventory

Inventory archive:

```text
C:/Users/CDQ-P/AppData/Local/CogentNexus-OpenClaw/forensics/CNX-20260904-246/backup-and-staging-inventory.json
```

### External rollover-generation backups

Path:

```text
C:/Users/CDQ-P/AppData/Local/CogentNexus-OpenClaw/plugin-generation-rollover-backups
```

There are `8` directory entries. No new entry bearing a Task-245 backup token was created. Known retained entries include Task-237 token `c6aaf93db7c34f718d01302477a292e1` and older tokens `8469daf5669242189f18e8c87ed9a86c`, `844361ed770342d68f41a4258ee56031`, `930460abc1c746dfaadd66ab67f6fa7f`, and `0473c508e8df45068886403662cf7d7d`.

Candidate-compatible tree hashes:

| Entry | Files | Bytes | Tree SHA-256 |
|---|---:|---:|---|
| `cogentnexus-openclaw-0473c508e8df45068886403662cf7d7d` | 33,648 | 317,355,890 | `9931812482a92e47da34e1169f2278440032397e57ebe9ed55819d507e11a04d` |
| `cogentnexus-openclaw-06548e9a584845cca8be6c087c5b53b4` | 33,654 | 317,368,975 | `7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a` |
| `cogentnexus-openclaw-630c4ad0820249639f991af00a21bc4d` | 33,656 | 317,374,069 | `900ac13f85a6de75e40a632a534f2b0ceef53def1e8387fc3530c02a7413de58` |
| `cogentnexus-openclaw-6fd674b03760470a997723a8fef5697b` | 33,656 | 317,374,069 | `900ac13f85a6de75e40a632a534f2b0ceef53def1e8387fc3530c02a7413de58` |
| `cogentnexus-openclaw-844361ed770342d68f41a4258ee56031` | 33,650 | 317,363,009 | `1f79454b62ff9976a5e11cf4f297736170f9b55e658d0ca7f25c342413b39298` |
| `cogentnexus-openclaw-8469daf5669242189f18e8c87ed9a86c` | 33,654 | 317,368,975 | `7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a` |
| `cogentnexus-openclaw-930460abc1c746dfaadd66ab67f6fa7f` | 33,648 | 317,356,500 | `cf80d399b3ebe2a1f9549d3dc5ca6179ef7e75870f4a83ed68661ad904b4f222` |
| `cogentnexus-openclaw-c6aaf93db7c34f718d01302477a292e1` | 33,656 | 317,374,069 | `900ac13f85a6de75e40a632a534f2b0ceef53def1e8387fc3530c02a7413de58` |

The current live plugin tree hash is also `900ac13f85a6de75e40a632a534f2b0ceef53def1e8387fc3530c02a7413de58`. This is supporting current-state evidence only; it is not used to infer historical equality.

### Workspace install/skill backups

Path:

```text
C:/Users/CDQ-P/.openclaw/workspace/.cogentnexus-openclaw/install-backups
```

There are `19` entries: `10` AGENTS snapshots and `9` skill directories. The installer-created entry is:

```text
cogentnexus-openclaw-20260904-195413
```

It has `124` files, `1,531,514` bytes, and candidate-compatible tree hash:

```text
11bbf1c8585b22eed92f70784931dddfc487031f11d5a5782aa84353ac833f73
```

Its creation time is `2026-09-04 12:54:13 UTC`, immediately before the recorded `plugin-rollover-prepare` start at `2026-09-04 12:54:23 UTC`. The stdout explicitly says:

```text
Backed up existing skill to ...install-backups\\cogentnexus-openclaw-20260904-195413
Installed CogentNexus-OpenClaw skill to ...workspace\\skills\\cogentnexus-openclaw
CogentNexus-OpenClaw validation: PASS
```

This is an installer workspace skill backup, not an external generation-rollover backup. It does not prove that rollover preparation succeeded.

## Staging inventory

Path:

```text
C:/Users/CDQ-P/.openclaw/workspace/.cogentnexus-openclaw/install-staging
```

There are `8` retained files: four plugin inventories and four transaction JSONs, all for historical tokens `0473c508...`, `844361ed...`, `8469daf...`, and `930460ab...`. No Task-245 transaction JSON or partial transaction with a new Task-245 token exists. The inventory and transaction files were not deleted, edited, normalized, or rewritten.

## Live safety checks

The preserved Task-245 postflight checks are read-only and report:

- Gateway: `READY`, exit `0`, `stateChanged=false`
- Provider: `READY`, exit `0`, `stateChanged=false`
- Model: `READY`, exit `0`, `stateChanged=false`
- Storage: `READY`, SQLite `integrity_check=ok`, exit `0`, `stateChanged=false`
- Recovery: `READY`, no active maintenance marker/incident/replay, exit `0`, `stateChanged=false`
- Delivery: `READY`, pending terminal deliveries `0`, exit `0`, `stateChanged=false`
- controller: `passthrough`, generation `39`
- selected provider: `ollama`
- installed canonical plugin: predecessor fingerprint `e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386` as recorded by Task 245 pre/post evidence; plugin remained disabled

The live plugin tree remained `900ac13f85a6de75e40a632a534f2b0ceef53def1e8387fc3530c02a7413de58`. No live repair, restore, enablement, managed-mode transition, replay, or semantic operation was performed by Task 246.

## Effect ledger

```text
scripts/install.ps1 invocations = 0
installer Scheduled Task registrations = 0
installer starts = 0
rollover-prepare/finalize invocations = 0
openclaw plugins install = 0
plugin/runtime/Gateway/DB mutation = 0
Dashboard/Discord/API semantic sends = 0
recovery replay/resend = 0
process termination = 0
historical evidence deletion/cleanup = 0
production/source/test/workflow edits = 0
release/tag/asset mutation = 0
force-push/history rewrite = 0
```

The only authorized non-report write was the byte-identical copy into the designated forensic archive. Repository mutation was limited to this report publication.

## Decision

`BLOCKED_EXACT_EXCEPTION_UNPROVEN` is the narrow supported result. The evidence proves the installer reached `plugin-rollover-prepare` and did not return a transaction, but it cannot prove the exact failing invariant or Python exception. A future diagnosis/repair task must explicitly authorize the next evidence-producing method; Task 246 authorizes no installer retry or successor execution.

STOP for independent ChatGPT review.
