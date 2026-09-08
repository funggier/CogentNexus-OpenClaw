# CNX-20260904-246 — Task-245 Rollover-Prepare Terminal Forensic / Evidence Preservation

## Status
`READY_FOR_HERMES`

## Purpose
Preserve and adjudicate the exact Task-245 `plugin-rollover-prepare` terminal failure before any installer retry. This task is forensic-only. It authorizes no installer execution, no rollover execution, and no semantic action.

## Authority
- Repo: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Parent: `CNX-20260904-245`
- Reviewed Task-245 report HEAD: `5984e3dfe3503bee37c218cb1f34eff16a071bef`
- Accepted review verdict: `ACCEPT_FAIL_INSTALLER_TERMINAL__MANIFEST_BINDING_AND_ONE_SHOT_EXECUTION_PROVEN__ROLLOVER_PREPARE_EXACT_EXCEPTION_UNPROVEN__READ_ONLY_FORENSIC_REQUIRED_BEFORE_ANY_RETRY`
- Exact executable candidate: `18a51b15768fb3d2196e65f1ef470c34aeef7f36`
- Candidate plugin fingerprint: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- Parent umbrella: `CNX-20260831-188`

## Accepted Task-245 boundary

```text
installer task registrations = 1
installer starts = 1
installer child invocations = 1
installer retries = 0
terminal stage = plugin-rollover-prepare
child exit = 1
transaction JSON = no new Task-245 transaction observed
installed plugin = predecessor e3bcce04...
controller = passthrough generation 39
semantic actions = 0
```

Task 245 used a frozen manifest-bound runner and proved the exact detached candidate installer path before start. Do not reopen scheduler/quoting hypotheses unless fresh evidence contradicts that proof.

## Critical evidence-preservation rule
Task-245 runner evidence currently resides under `%LOCALAPPDATA%\Temp`. Temp content may disappear with time. Before broad analysis:

1. locate the exact Task-245 evidence root `cnx245-install-evidence-20260904T` and runner root `cnx245-runner-20260904T` if still present;
2. record file inventory, sizes, timestamps, and SHA-256 of every relevant artifact;
3. copy relevant Task-245 evidence byte-identically to a new non-temp forensic archive under `%LOCALAPPDATA%\CogentNexus-OpenClaw\forensics\CNX-20260904-246\`;
4. rehash copied files and require source/destination SHA-256 equality;
5. evidence preservation is copy-only: do not edit or delete originals.

If the temp artifact is already missing, record exactly which files are unavailable and continue with retained evidence only. Do not reconstruct missing text from guesses.

## Required forensic reads
Preserve and inspect, when present:
- `child-stderr.txt` complete bytes/text;
- `child-stdout.txt` complete bytes/text;
- `runner-transcript.txt`;
- `runner-result.json`;
- `runner-started.json`;
- `launch-manifest.json` and its SHA;
- frozen runner source and SHA;
- installer stage diagnostics/timestamps.

Report the exact Python exception type, message, traceback frames, and final relevant line if recoverable. Redact secrets only if any unexpectedly appear; preserve hashes of original bytes.

## Rollover-prepare boundary analysis
Against exact candidate source, correlate the failure with the ordered path in `prepare_plugin_rollover_transaction()`:

1. passthrough proof;
2. ownership manifest verification;
3. retired plugin payload proof;
4. replacement fingerprint validation;
5. external app-data boundary validation;
6. backup token validation;
7. retired storage-root resolution;
8. rollover backup destination validation;
9. backup parent/create/copytree;
10. retired tree hash;
11. backup tree hash;
12. tree equality assertion;
13. successful return, after which CLI writes transaction JSON.

No new Task-245 transaction means successful return was not reached.

## Backup inventory
Read-only inventory both distinct backup domains:

### A. Rollover-generation backups
`%LOCALAPPDATA%\CogentNexus-OpenClaw\plugin-generation-rollover-backups`

Record all entries with creation/write times, names/tokens, sizes and tree hashes. Reconcile known historical evidence including retained Task-237 token `c6aaf93db7c34f718d01302477a292e1` and Task-223 artifacts. Identify whether Task 245 created a new rollover backup.

If a Task-245 rollover backup exists:
- do not mutate it;
- hash its exact project tree using the candidate-compatible algorithm or a byte-equivalent independent verifier;
- hash the current retired storage tree read-only;
- record equality/differences and path-level differing entries;
- do not infer historical equality solely from current equality unless the raw error confirms it.

### B. Workspace install/skill backups
`%USERPROFILE%\.openclaw\workspace\.cogentnexus-openclaw\install-backups`

Inspect `cogentnexus-openclaw-20260904-195413` and identify from source/log timing which installer operation created it. Keep this evidence distinct from rollover-generation backup evidence.

## Staging inventory
Read-only inventory:
`%USERPROFILE%\.openclaw\workspace\.cogentnexus-openclaw\install-staging`

Record transaction JSONs, temp files, timestamps and hashes. Prove whether any new Task-245 transaction or partial temp transaction exists. Do not delete or normalize stale artifacts.

## Live safety checks
Read-only only:
- controller mode/generation;
- canonical installed plugin path/status/fingerprint/tree hash;
- Gateway/provider/model health;
- Delivery pending count/readiness;
- Recovery readiness/no active replay;
- SQLite integrity only if the standard read-only check is available.

Do not enable the plugin, restore managed mode, restart Gateway, replay recovery, or repair anything.

## Hard zero-effect budget
```text
scripts/install.ps1 invocations = 0
installer Scheduled Task registrations = 0
installer starts = 0
rollover-prepare/finalize invocations = 0
openclaw plugins install = 0
plugin mutation = 0
controller/Gateway/lifecycle mutation = 0
manual DB/Ticket/outbox/recovery mutation = 0
Dashboard semantic submissions = 0
Discord semantic submissions = 0
direct Discord/API sends = 0
recovery replay/resend = 0
process termination = 0
historical evidence deletion/cleanup = 0
release/tag/asset mutation = 0
production/source/test/workflow edits = 0
force push/history rewrite = 0
```

## Decision output
Classify one of:
- `PASS_EXACT_ROLLOVER_PREPARE_ROOT_CAUSE_PROVEN`
- `BLOCKED_TEMP_EVIDENCE_LOST`
- `BLOCKED_EXACT_EXCEPTION_UNPROVEN`
- `BLOCKED_EVIDENCE_CONFLICT`

A PASS requires exact error evidence plus source correlation sufficient to name the failing invariant/sub-operation without speculation.

## Report
Publish:
`docs/operations/coordination/reports/CNX-20260904-246-task245-rollover-prepare-terminal-forensic-evidence-preservation.md`

Then STOP for independent ChatGPT review. Do not open or execute an installer successor from this task.
