# CNX-20260904-249 — Task-248 Retired Project Transient-Mutation Forensic

## Status

`READY_FOR_HERMES`

## Parent

- Task: `CNX-20260904-248`
- Reviewed report HEAD: `06b7bc01161efe2c8bbb97fe0e0511d79ff8d62b`
- Independent review verdict:
  `ACCEPT_FAIL_INSTALLER_TERMINAL__TASK247_DIAGNOSTIC_REPAIR_PROVEN__TASK226_FAIL_CLOSED_ATTESTATION_TRIGGERED__TRANSIENT_RETIRED_TREE_MUTATION_ACTOR_UNPROVEN__READ_ONLY_MUTATION_FORENSIC_REQUIRED`
- Review commit: `061ba41bb10e89c97fa94debf5fdec7665d275da`
- Parent umbrella: `CNX-20260831-188`

## Objective

Determine, using read-only Windows/filesystem/process/log evidence, which path and if possible which process/actor caused the retired plugin npm project to differ transiently from the Task-248 generation-rollover backup during `prepare_plugin_rollover_transaction()`.

Do **not** change the fail-closed attestation semantics and do **not** rerun the installer.

## Accepted facts

Task 248 proved all of the following:

```text
exact executable candidate = 6c11a5e8f417300835e85441b88e0f37e3897353
Task247 native-stderr repair worked in live execution
Scheduled Task registration/start = 1 / 1
scripts/install.ps1 invocation = 1
retry after start = 0
terminal stage = plugin-rollover-prepare
exception = RuntimeError: pre-install backup project-tree attestation mismatch
candidate installed = no
controller = passthrough generation 39
live canonical plugin = disabled predecessor e3bcce04...
semantic sends = 0
```

Task-248 retained external generation-rollover backup:

```text
C:/Users/CDQ-P/AppData/Local/CogentNexus-OpenClaw/plugin-generation-rollover-backups/cogentnexus-openclaw-fc6fb357dd4a4c9688e4eb0116c10033
```

Its later read-only full-tree hash and the later current retired-project full-tree hash both equalled:

```text
900ac13f85a6de75e40a632a534f2b0ceef53def1e8387fc3530c02a7413de58
```

That equality is post-failure only. It does not prove historical equality at the failed comparison.

No Task-248 rollover transaction JSON was persisted.

## Safety invariant that MUST remain intact

`tests/test_task225_rollover_prepare_attestation.py` explicitly proves that a non-payload source mutation after the backup copy must cause:

```text
RuntimeError: pre-install backup project-tree attestation mismatch
```

The current full-tree digest covers path/type/size/content/symlink state. It does not hash mtime.

Therefore Task 249 MUST NOT recommend any of the following as a fix:

- ignore the mismatch;
- reduce proof to package payload only;
- exclude an observed changed path merely to make install pass;
- retry hashes until they become equal;
- add sleeps/retries around the mismatch as a success mechanism;
- delete the retained backup and try again.

Those would weaken Task-226 fail-closed safety.

## Phase A — fresh authority and immutable evidence inventory

1. Fetch/re-read GitHub branch authority, this Task, Task-248 report, Task-248 review, and `ACTIVE.md` / `STATUS.md`.
2. Reconfirm public `v0.9.3` tag unchanged.
3. Reconfirm the Task-248 forensic root and rollover backup still exist.
4. Resolve the exact retired project root from current ownership manifest / existing source logic using read-only inspection only.
5. Record before doing anything else:
   - current full-tree hash of retired project;
   - current full-tree hash of Task-248 rollover backup;
   - complete per-path inventory for both trees: relative path, object type, size, content SHA-256 for regular files, symlink target where applicable;
   - file timestamps/attributes as supporting metadata only;
   - package payload membership vs non-payload membership where determinable from `package.json` / package files contract.
6. Write forensic outputs only under a new non-temp task evidence directory, for example:

```text
%LOCALAPPDATA%/CogentNexus-OpenClaw/forensics/CNX-20260904-249/
```

Writing forensic output there is allowed. Do not alter source/backup trees.

## Phase B — historical mutation evidence

Focus on the Task-248 installer window beginning approximately:

```text
2026-09-04T15:34:42.0554329Z
```

Use available read-only evidence to identify writes/renames/creates/deletes under the exact retired project root near that window.

Inspect, where available and bounded:

- NTFS/USN change-journal evidence for the retired project paths;
- Windows event logs relevant to filesystem/PowerShell/Task Scheduler/Defender;
- OpenClaw logs around the Task-248 window;
- npm/plugin logs and any installer child logs already retained;
- process command-line/start-time evidence that survives for candidate actors;
- antivirus/security history if it records file activity under the retired project;
- retained Task-248 runner/transcript/stdout/stderr evidence;
- directory/file timestamps that can narrow candidate paths (supporting evidence only, never as the attestation cause by themselves).

Do not dump an unbounded USN journal. If journal access exists, constrain/filter as tightly as practical to the retired project and relevant time window. Record access limitations honestly.

## Phase C — classify likely mutable paths

Build a table of any path that is plausibly mutable at runtime or was touched near the Task-248 window. For each candidate path record:

```text
relative path
payload / non-payload classification
current source SHA/size/type
Task248 backup SHA/size/type
relevant timestamps
historical write/create/delete/rename evidence
candidate actor/process
confidence
```

Do not infer an actor from filename alone.

## Phase D — bounded passive observation if historical evidence is insufficient

If the historical evidence does not identify the actor, a strictly read-only passive observation is allowed for up to approximately 120 seconds:

1. repeatedly compute the retired-project full-tree digest and a per-path digest inventory;
2. do not launch or stimulate OpenClaw/CogentNexus/npm/plugin operations;
3. do not restart/stop/start Gateway/controller/provider/model;
4. if the digest changes spontaneously, immediately record before/after per-path differences and contemporaneous read-only process/log evidence;
5. do not attempt to stabilize, lock, copy, modify, rename, or delete the retired tree.

This observation is diagnostic only. Absence of a mutation during the window does not prove immutability during Task 248.

## Required adjudication

Finish with one of these evidence-backed classifications or a more precise equivalent:

### A. Actor/path proven

`PASS_TRANSIENT_MUTATION_PATH_AND_ACTOR_PROVEN`

Only if the historical/passive evidence identifies the changed path and a defensible actor/process causally associated with the mutation.

### B. Path proven, actor unresolved

`BLOCKED_TRANSIENT_MUTATION_PATH_PROVEN__ACTOR_UNRESOLVED`

### C. Historical evidence insufficient

`BLOCKED_TRANSIENT_MUTATION_ACTOR_UNPROVEN__TDD_MISMATCH_INSTRUMENTATION_REQUIRED`

If C, explicitly recommend a **separate repository-only TDD successor** that augments mismatch diagnostics with source-vs-backup per-path digest differences before raising, while preserving the existing exception/fail-closed behavior. Do not implement that instrumentation in Task 249.

## Hard fences / effect budget

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

Read-only hashing, enumeration, logs/event queries, and creation of Task-249 forensic evidence files outside the protected source/backup trees are allowed.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260904-249-task248-retired-project-transient-mutation-forensic.md`

The report must include:

- exact GitHub authority and report publication HEAD;
- exact retired project root and Task-248 backup root;
- before/after full-tree hashes;
- per-path current comparison summary;
- historical evidence queried and any access gaps;
- candidate mutable paths with evidence/confidence;
- passive-observation results if used;
- effect ledger proving all hard fences;
- explicit statement that Task-226 fail-closed attestation remains unchanged;
- PASS/BLOCKED classification;
- no installer retry authorization.

Then STOP for independent ChatGPT review.
