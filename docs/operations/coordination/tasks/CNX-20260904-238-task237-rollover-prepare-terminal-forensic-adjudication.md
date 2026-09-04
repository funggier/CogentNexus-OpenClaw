# CNX-20260904-238 — Task237 Rollover-Prepare Terminal Forensic Adjudication

Status: `READY_FOR_HERMES`
Executor: Hermes / authenticated Windows operator
Coordinator / independent reviewer: ChatGPT
Parent task: `CNX-20260904-237`
Repository/TDD parent: `CNX-20260903-235`
Installer safety / attestation repair parent: `CNX-20260902-226`
Historical direct-extension ownership repair: `CNX-20260829-140`
Historical installer failure lineage: `CNX-20260902-223`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-04 ICT

## Authority

Task-237 report disposition:

`FAIL_INSTALLER_TERMINAL`

Independent Task-237 review verdict:

`ACCEPT_FAIL_INSTALLER_TERMINAL__ROLLOVER_PREPARE_EXACT_INVARIANT_UNPROVEN__READ_ONLY_FORENSIC_SUCCESSOR_REQUIRED`

Exact accepted repository candidate remains:

`ffb0dd4ed47affe2e496c17b74ca74d358905bd7`

Expected candidate plugin fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Predecessor live plugin fingerprint after Task 237:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

Task-237 post-failure live boundary to preserve:

```text
controller = passthrough
generation = 39
Gateway healthy
provider = ollama
Delivery READY, pending = 0
Recovery READY
SQLite integrity = ok
candidate plugin not installed
semantic submissions = 0
```

Fresh GitHub/live evidence supersedes this summary if newer authority appears.

## Objective

Determine the **exact failing invariant** inside Task-237 `plugin-rollover-prepare` from retained evidence, without invoking the installer, `rollover-prepare`, plugin lifecycle, semantic delivery, or manual lifecycle recovery.

This task is read-only forensic adjudication plus repository/source analysis only. It does not authorize another live installation attempt.

## Why this task exists

Task 237 proves only the installer wrapper error:

`ownership-safe plugin generation rollover pre-install proof failed`

The exact candidate installer captures Python command stdout in `$prepareOutput`, but on nonzero exit throws the generic wrapper message without persisting/emitting `$prepareOutput`. Therefore the report does not yet prove whether the Python prepare failed at direct-storage validation, payload validation, external backup boundary, copy, backup destination, project-tree attestation, transaction persistence, or another exact invariant.

Do not infer recurrence of Task-139/140 or Task-223/226 solely from the wrapper message.

## Hard fences

### Authorized

- fresh GitHub/Actions/source reads;
- read-only Windows/runtime/status/process/SQLite inspection;
- read-only inspection and hashing of Task-237 evidence roots;
- read-only inventory/hashing of `plugin-generation-rollover-backups` and `install-staging`;
- read-only inspection/hashing of current predecessor direct plugin tree;
- read-only inspection of ownership manifest/controller/startup state;
- read-only comparison of file lists, sizes, hashes, mtimes and payload identities;
- offline repository/source analysis;
- creation of disposable copies of already-read evidence under a Task-238 temp evidence root when needed for comparison, provided originals are untouched;
- coordination report publication.

### Not authorized

- installer task registration/start/invocation;
- direct `rollover-prepare`, `rollover-finalize`, plugin install/enable/disable/uninstall;
- manual managed re-enable or lifecycle/Gateway repair;
- manual ownership manifest edit;
- deletion/rename/move/edit of Task-237/Task-223/Task-233 evidence;
- manual Ticket/outbox/recovery/SQLite writes;
- process termination;
- provider/model substitution;
- Dashboard/Discord semantic submissions or API sends;
- recovery replay/resend;
- reset/uninstall/reinstall;
- Release/tag/asset mutation;
- force push/history rewrite.

Semantic budget: `0`.
Installer invocation budget: `0`.
Live product mutation budget: `0`.

## Phase A — fresh authority and preservation proof

Fresh-fetch branch HEAD, `ACTIVE.md`, `STATUS.md`, Task-237 report/review, candidate ancestry and public `v0.9.3` tag.

Confirm no unexpected product/source/test/workflow drift after candidate `ffb0dd4...` other than any separately reviewed repair authority.

Capture current live state read-only and require no unexplained mutation since Task 237. The expected fail-closed boundary is passthrough generation 39 with predecessor plugin still effective, Delivery pending 0, Recovery READY, SQLite OK, Gateway/Ollama healthy.

If the evidence boundary materially drifted before forensic capture, stop:

`BLOCKED_FORENSIC_STATE_DRIFT`

Do not normalize it.

## Phase B — preserve exact Task-237 evidence

Hash and inventory at minimum:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx237-preflight-20260904T
C:\Users\CDQ-P\AppData\Local\Temp\cnx237-install-evidence-20260904T
C:\Users\CDQ-P\AppData\Local\Temp\cnx237-post-20260904T
C:\Users\CDQ-P\AppData\Local\Temp\cnx237-registration.json
C:\Users\CDQ-P\AppData\Local\Temp\cnx237-registration-readback.json
C:\Users\CDQ-P\AppData\Local\Temp\cnx237-installer-runner.ps1
```

Inspect transcript, runner output, terminal JSON, PowerShell error records and any redirected stdout/stderr for Python traceback/message that may not have been summarized in the report.

Search specifically for:

- `RuntimeError:`
- `pre-install backup project-tree attestation mismatch`
- `rollover backup destination`
- `manifest-owned prior plugin payload`
- `expected source fingerprint`
- `application-data root`
- `backup token`
- direct-extension / managed-project boundary messages
- Python exit/error stream records.

Do not mutate evidence files.

## Phase C — recover Task-237 rollover identity

From installer logs/command traces/staging names/timestamps, recover the Task-237 `rolloverId` / backup token if possible.

Read-only inventory:

```text
%LOCALAPPDATA%\CogentNexus-OpenClaw\plugin-generation-rollover-backups
%USERPROFILE%\.openclaw\workspace\.cogentnexus-openclaw\install-staging
```

For every entry capture:

```text
full path
name/token
creation time
last-write time
file/dir count
full-tree SHA-256 using the same project-tree contract where possible
payload fingerprint where applicable
```

Distinguish historical Task-223 artifacts from any artifact first created during the Task-237 UTC execution window `2026-09-04T00:46:05Z`–`00:53:08Z`.

No cleanup is allowed.

## Phase D — artifact-state decision tree

### Case 1: matching Task-237 transaction exists

Read and validate it without finalizing. Compare its fields against current/live/backup identities. Determine whether prepare actually persisted successfully and the wrapper failure came from a later persistence/command boundary.

### Case 2: Task-237 backup exists but matching transaction does not

This strongly localizes failure to the interval after backup directory creation/copy and before transaction persistence. Compute:

- backup tree hash;
- current predecessor storage tree hash;
- backup payload fingerprint;
- current predecessor payload fingerprint;
- exact path-level differences between backup and current retired storage.

If the payload fingerprints match but full-tree hashes differ, identify non-payload files/metadata represented by the project-tree hashing contract. Correlate timestamps to Task-237 execution.

Do not call this `pre-install backup project-tree attestation mismatch` unless source ordering plus artifact evidence proves that is the earliest consistent invariant.

### Case 3: no Task-237 backup and no matching transaction

Reconstruct every prepare precondition read-only in source order using current/preserved evidence:

1. passthrough mode;
2. manifest readable/exact;
3. retired plugin payload exact;
4. expected replacement fingerprint syntactically valid;
5. external application-data boundary valid;
6. backup token safe;
7. retired storage root accepted by Task-140 boundary repair;
8. backup destination did not pre-exist at execution time where provable.

Determine the earliest unproven/failed invariant. If exact failure still cannot be proven, disposition must remain `BLOCKED_EXACT_PREPARE_ERROR_UNPROVEN`.

## Phase E — source/observability adjudication

Independently inspect exact candidate `scripts/install.ps1` and `namespace_ownership.py`.

Prove whether the installer currently loses actionable `rollover-prepare` diagnostic output on nonzero exit because `$prepareOutput` is captured but not emitted/persisted.

Classify:

- `OBSERVABILITY_DEFECT_PROVEN` if source conclusively swallows actionable output;
- `OBSERVABILITY_DEFECT_NOT_PROVEN` otherwise.

If proven, specify the minimal TDD repair required for a later repository task: preserve/emit a bounded diagnostic without changing rollover semantics or weakening fail-closed behavior. Do **not** edit production source in Task 238.

## Phase F — historical comparison

Compare the exact failure evidence against:

- Task 140 direct-extension ownership-boundary failure/repair;
- Task 223/224/225/226 backup-attestation lineage.

The successor report must explicitly say whether Task 237 is:

- recurrence of a known defect;
- expected fail-closed detection of a live mutation/race;
- a new source defect;
- an evidence/observability gap preventing exact adjudication.

Do not collapse different lineages based on similar wrapper text.

## Required disposition

Use one of:

- `PASS_EXACT_PREPARE_ROOT_CAUSE_PROVEN__OBSERVABILITY_DEFECT_PROVEN`
- `PASS_EXACT_PREPARE_ROOT_CAUSE_PROVEN__OBSERVABILITY_DEFECT_NOT_PROVEN`
- `BLOCKED_EXACT_PREPARE_ERROR_UNPROVEN`
- `BLOCKED_FORENSIC_STATE_DRIFT`
- `BLOCKED_EVIDENCE`

A PASS must name the exact failing invariant and show the evidence chain that excludes earlier alternatives.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260904-238-task237-rollover-prepare-terminal-forensic-adjudication.md`

Include:

- fresh authority;
- live preservation state;
- Task-237 evidence hashes/inventory;
- recovered rollover id/token if any;
- backup/transaction inventory and timestamps;
- exact tree/payload comparison;
- source-order invariant elimination;
- exact root-cause classification or explicit evidence blocker;
- observability-defect classification;
- retry ledger for read-only tooling only;
- zero-mutation/zero-semantic ledger;
- final disposition.

Then STOP for independent ChatGPT review.
