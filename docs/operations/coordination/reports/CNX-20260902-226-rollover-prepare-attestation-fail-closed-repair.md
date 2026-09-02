# CNX-20260902-226 — Rollover-Prepare Attestation Fail-Closed Repair

Date: 2026-09-02 ICT  
Task: `CNX-20260902-226`  
Parent: `CNX-20260902-225`

## Disposition

`PASS_FAIL_CLOSED_REPAIR_GREEN__AWAIT_INDEPENDENT_REVIEW`

Task 226 is complete at the repository/source/test/CI boundary.

The Task-225 proven `SOURCE_DEFECT_NONATOMIC_ATTESTATION` is repaired by making `rollover-prepare` fail closed before returning a transaction whenever the retired source project-tree attestation differs from the newly-created backup project-tree attestation.

No live Windows installer, rollover, lifecycle, ownership, transaction, backup, plugin, Gateway, SQLite, process, provider/model, Discord, Release, tag, or asset mutation occurred in Task 226.

## Accepted contract RED

Commit:

`d8700ff82ba81ba12ba631f76be02d10a297dd9b`

Validate run:

`33617282033`

Ubuntu/Python 3.11 job:

`100206047934`

Target failure:

```text
Failed: DID NOT RAISE RuntimeError
1 failed, 475 passed, 33 skipped, 4 subtests passed
```

All prerequisite namespace/baseline/self-test/py_compile steps passed before pytest. This proved that current source returned success instead of failing closed when a non-package-payload retired-tree entry changed after top-level backup copy.

## Minimal production repair

Accepted production repair commit:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Production file:

`skills/cogentnexus-openclaw/scripts/namespace_ownership.py`

Behavioral change:

1. copy the retired project to the external backup;
2. compute retired source project-tree SHA exactly once;
3. compute backup project-tree SHA exactly once;
4. compare the two attestations before returning transaction success;
5. fail closed with `RuntimeError("pre-install backup project-tree attestation mismatch")` if they differ;
6. when equal, serialize the already-computed matching hashes into the transaction.

The finalizer predicates are unchanged. `_project_tree_sha256()` coverage is unchanged. No non-payload project entries were excluded to force equality.

## Minimality recovery

An initial contents-API source write at:

`a8f5c6aa0a866411b2b36111c2ada912bc72f5dc`

contained the intended logic but also removed 70 lines of comments/docstrings. It was explicitly rejected as the accepted repair because it violated the minimal-fix requirement.

A temporary repository-only workflow checkpoint at:

`68822a7dc4095da97c2238e338198b8667f9dd92`

restored the exact `d8700ff...` source file and applied only the bounded repair. Its generated commit `9a8510f...` removed the temporary workflow from the resulting tree.

Fresh GitHub compare `d8700ff...` → `9a8510f...` showed:

```text
files changed: 1
namespace_ownership.py: +6 / -2
```

Therefore the rejected non-functional churn is absent from the accepted repaired source tree.

## Authoritative GREEN validation

The `github-actions[bot]` source repair commit does not itself trigger downstream workflows through `GITHUB_TOKEN`. Coordination checkpoint commit:

`dc8485f544524c6549e6cc50585e9d788fa4ccf1`

triggered the normal branch workflows against the exact repaired source tree plus the Task-226 report.

### Validate

Run:

`33618100236`

Head SHA:

`dc8485f544524c6549e6cc50585e9d788fa4ccf1`

Conclusion:

`SUCCESS`

Successful jobs:

```text
package dry-run (no publish)               100208607326
validate (macos-latest, 3.11)              100208607610
validate (ubuntu-latest, 3.11)             100208607623
validate (windows-latest, 3.14)            100208607635
validate (ubuntu-latest, 3.14)             100208607696
validate (windows-latest, 3.11)            100208607708
validate (macos-latest, 3.14)              100208607722
```

Representative Ubuntu/Python 3.11 full pytest result:

```text
476 passed, 33 skipped, 4 subtests passed in 5.55s
```

The same Validate matrix completed successfully across Ubuntu, macOS, and Windows on Python 3.11/3.14, including:

- namespace isolation;
- baseline consistency;
- `validate.py --workspace-singleton`;
- Cogent/runtime/workflow self-tests;
- `py_compile`, including `namespace_ownership.py`;
- full `python -m pytest -q`;
- benchmark validator self-test;
- plugin path migration helper;
- POSIX installer syntax where applicable;
- Windows PowerShell syntax/PS5.1 serializer/root-process exit smoke where applicable;
- `npm ci`;
- `npm test` — representative Linux job: 56 files / 280 tests passed;
- `npm run evaluation`;
- `npm audit --omit=dev` — representative Linux job: 0 vulnerabilities;
- `npm run plugin:validate`.

### PS5.1 Acceptance Smoke

Run:

`33618100318`

Conclusion:

`SUCCESS`

### Windows Installer Pack Smoke

Run:

`33618100472`

Conclusion:

`SUCCESS`

The pack smoke passed npm 12 production-shape validation, dependency/build/plugin validation, installer local-archive path checks, and exact Windows pack inspection.

## Files / commits relevant to Task 226

```text
d8700ff82ba81ba12ba631f76be02d10a297dd9b  test: require rollover prepare to fail closed on attestation drift
9a8510f1317c8e53c01c233b080ec20357cd22df  fix: apply minimal rollover attestation gate
dc8485f544524c6549e6cc50585e9d788fa4ccf1  docs(coordination): record Task 226 repair checkpoint
```

Primary files:

```text
tests/test_task225_rollover_prepare_attestation.py
skills/cogentnexus-openclaw/scripts/namespace_ownership.py
docs/operations/coordination/reports/CNX-20260902-226-rollover-prepare-attestation-fail-closed-repair.md
```

Rejected/non-authoritative repair attempts retained only as history/evidence:

```text
a8f5c6aa0a866411b2b36111c2ada912bc72f5dc  rejected non-minimal contents-API source edit
68822a7dc4095da97c2238e338198b8667f9dd92  temporary repair helper workflow checkpoint
```

## Mutation ledger

```text
live installer invocations: 0
live rollover-prepare invocations: 0
live rollover-finalize invocations: 0
manual lifecycle actions: 0
Gateway restarts: 0
live plugin/config mutations: 0
live ownership/transaction/backup repairs: 0
SQLite writes: 0
process terminations: 0
provider/model substitutions: 0
Discord Sends/API semantic traffic: 0
Release/tag/asset mutations: 0
force pushes/history rewrites: 0
```

## Important retained-state boundary

The Task-223 retained transaction was created by the pre-repair producer and is already proven internally inconsistent:

```text
backupProjectTreeSha256 != retiredProjectTreeSha256
```

Task 226 does not make that historical transaction valid. It must not be passed to `rollover-finalize`, manually edited, or treated as repairable evidence.

A successor Windows requalification task must first re-read the retained state, classify/retire the obsolete failed transaction and backup under an explicitly-authorized bounded recovery procedure, and only then create a fresh prepare transaction using repaired source if the current machine state still satisfies all preconditions.

## Required next step

Independent ChatGPT review must verify Task 226 minimality and authoritative GREEN evidence. If accepted, open a bounded Windows requalification successor. No live Windows installer retry is authorized by this report alone.
