# Independent Review — CNX-20260902-226 Rollover-Prepare Attestation Fail-Closed Repair

Date: 2026-09-02 ICT  
Coordinator / final reviewer: ChatGPT

## Verdict

`ACCEPT_PASS_REPAIR_GREEN__ALREADY_EXACT_REENTRY_REQUALIFICATION_REQUIRED`

Task 226 is accepted as a complete repository/source/test/CI repair of the producer-side non-atomic attestation defect proven by Task 225.

The repair is sufficient to prevent future `rollover-prepare` success when the retired project tree and copied backup tree are not identical under `_project_tree_sha256()` semantics.

This review does **not** authorize reuse or manual repair of the retained Task-223 transaction. It also corrects one successor assumption in the Task-226 report: the current Task-223 partial Windows state must not blindly create a fresh same-path rollover transaction before retry. Current source contains an already-exact re-entry path that must be requalified first.

## Fresh authority

Fresh branch HEAD before this review:

`4cce730136227e1125538197e3cb3f94159e2fc4`

Task-226 report disposition:

`PASS_REPAIR_GREEN_WINDOWS_REQUALIFICATION_REQUIRED`

Public `v0.9.3` remains outside this repair boundary and no Release/tag/asset mutation is authorized.

## Accepted TDD evidence

Contract RED:

`d8700ff82ba81ba12ba631f76be02d10a297dd9b`

Validate run:

`33617282033`

Ubuntu/Python 3.11 job:

`100206047934`

Expected failure:

```text
Failed: DID NOT RAISE RuntimeError
1 failed, 475 passed, 33 skipped, 4 subtests passed
```

The failure proved that the predecessor producer could return successfully after source/backup tree divergence instead of failing closed.

## Accepted minimal repair

Accepted production repair commit:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Production file:

`skills/cogentnexus-openclaw/scripts/namespace_ownership.py`

Fresh compare from contract RED baseline `d8700ff...` to accepted repair `9a8510f...` proves:

```text
files changed: 1
namespace_ownership.py: +6 / -2
```

The accepted behavior is:

1. copy the manifest-owned retired project to the external backup;
2. calculate retired project-tree SHA once;
3. calculate backup project-tree SHA once;
4. raise `RuntimeError("pre-install backup project-tree attestation mismatch")` when they differ;
5. serialize those already-computed hashes only when they are equal.

The finalizer predicates and `_project_tree_sha256()` coverage were not weakened.

The earlier nonminimal contents-API write `a8f5c6aa...` is explicitly rejected as repair authority; its comment/docstring churn is absent from the accepted final tree.

## GREEN evidence

Validated repaired-tree checkpoint:

`dc8485f544524c6549e6cc50585e9d788fa4ccf1`

Authoritative workflow results:

```text
Validate                 33618100236  SUCCESS
PS5.1 Acceptance Smoke   33618100318  SUCCESS
Windows Installer Pack   33618100472  SUCCESS
```

Representative full Python result:

`476 passed, 33 skipped, 4 subtests passed`

Representative plugin result:

`56 files / 280 tests passed`

Evaluation, production npm audit, package dry-run, plugin validation, Windows PowerShell syntax/serializer/root-exit checks, and all Ubuntu/macOS/Windows Python 3.11/3.14 matrix jobs passed.

The report-close HEAD `4cce730136227e1125538197e3cb3f94159e2fc4` was also rechecked independently and all three branch workflows completed SUCCESS:

```text
Validate                 33618214321  SUCCESS
PS5.1 Acceptance Smoke   33618214340  SUCCESS
Windows Installer Pack   33618214303  SUCCESS
```

## Retained Task-223 state remains obsolete evidence

Task 224 proved the retained transaction is internally inconsistent:

```text
transaction:
C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\install-staging\plugin-rollover-transaction-8469daf5669242189f18e8c87ed9a86c.json

backup:
C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\plugin-generation-rollover-backups\cogentnexus-openclaw-8469daf5669242189f18e8c87ed9a86c

backup actual / backupProjectTreeSha256:
7394401cb0ae9791c1c9b98661a9bf9df47ecb83c0b139b46cd742b17ee7342a

retiredProjectTreeSha256:
ca74a262293d49b058fce6221db2fa5311214cde567ebb331ff845670c5a2cab
```

The old transaction was produced before the Task-226 repair and must never be passed to `rollover-finalize`, rewritten, or treated as valid authority.

## Successor correction — do not create B -> B rollover blindly

Task 223 already installed the accepted candidate payload at the canonical direct path:

```text
C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw
fingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
```

The ownership manifest remained unchanged and points to that same direct path. Therefore the current live shape is materially different from the original pre-install A -> B transition: the plugin bytes at the manifest-owned direct path are already candidate B.

Current source explicitly handles a single manifest-owned canonical candidate whose fingerprint equals the expected source fingerprint as:

```text
mode = upgrade
pendingRollover = false
pluginAlreadyExact = true
```

`scripts/resolve-plugin-lifecycle-actions.ps1` maps that exact state to:

```text
installPlugin = false
rolloverPlugin = false
```

This is important because the finalizer intentionally rejects direct same-path rollover when:

```text
expected fingerprint == retired fingerprint
```

with:

`direct same-path rollover requires a fingerprint transition from the retired fingerprint`

Consequently, a fresh `rollover-prepare` against the already-installed B payload followed by a B -> B replacement is not the correct default recovery path.

## Required successor

Open Task 227 as a bounded Windows **already-exact re-entry requalification**.

Before any installer mutation it must prove current live state still matches the preserved Task-223/224 state and specifically prove:

1. candidate source fingerprint equals current canonical direct plugin fingerprint;
2. exactly one canonical product payload remains at the manifest-owned direct path;
3. attested `classify-install` returns `upgrade + pendingRollover=false + pluginAlreadyExact=true`;
4. production action resolver returns `installPlugin=false + rolloverPlugin=false`;
5. the stale Task-223 transaction/backup remain unchanged and are classified `OBSOLETE_PRODUCER_DEFECT_EVIDENCE`;
6. no installer code automatically discovers or consumes stale rollover transaction files; only the per-invocation transaction path is used when `rolloverPlugin=true`;
7. if all gates pass, one separately bounded installer re-entry may be considered without plugin installation, rollover prepare, or rollover finalize;
8. if any gate differs, stop without mutation and adjudicate the drift.

The stale transaction and backup should be preserved in place through requalification unless a later cleanup task explicitly authorizes archival/removal. Their mere presence is evidence, not authority.

## Runtime / Discord boundary

Until Task 227 explicitly reaches its mutation gate:

```text
old rollover-finalize invocations: 0
fresh rollover-prepare invocations: 0
plugin install/uninstall/enable actions: 0
manual ownership writes: 0
manual transaction/backup edits or deletions: 0
cnxclaw lifecycle actions: 0
Gateway restarts: 0
SQLite writes: 0
process terminations: 0
provider/model substitutions: 0
Discord Sends/API semantic traffic: 0
Release/tag/asset mutations: 0
force push/history rewrite: forbidden
```

## Disposition

`ACCEPT_PASS_REPAIR_GREEN__ALREADY_EXACT_REENTRY_REQUALIFICATION_REQUIRED`
