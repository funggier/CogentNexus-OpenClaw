# CNX-20260902-226 — Rollover-Prepare Attestation Fail-Closed Repair

Date: 2026-09-02 ICT  
Task: `CNX-20260902-226`  
Parent: `CNX-20260902-225`

## Status

`VALIDATION_IN_PROGRESS`

Repository-only TDD repair has reached the GREEN-validation phase. Live Windows state remains untouched.

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

All prerequisite namespace/baseline/self-test/py_compile steps passed before pytest.

## Repair

Final minimal production repair commit:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Production file:

`skills/cogentnexus-openclaw/scripts/namespace_ownership.py`

Behavioral change:

1. copy the retired project to the external backup;
2. compute retired source project-tree SHA exactly once;
3. compute backup project-tree SHA exactly once;
4. fail closed with `RuntimeError("pre-install backup project-tree attestation mismatch")` if they differ;
5. serialize the already-computed equal attestations only when the invariant holds.

The finalizer predicates and `_project_tree_sha256()` coverage are unchanged.

## Minimality recovery

An initial contents-API source write at:

`a8f5c6aa0a866411b2b36111c2ada912bc72f5dc`

contained the intended logic but also removed 70 lines of comments/docstrings and was rejected as the accepted repair because it violated the minimal-fix requirement.

A temporary repository-only workflow checkpoint at:

`68822a7dc4095da97c2238e338198b8667f9dd92`

restored the exact `d8700ff...` source file and applied only the bounded repair. Its generated commit `9a8510f...` removed the temporary workflow from the resulting tree.

Fresh GitHub compare `d8700ff...` → `9a8510f...` reports:

```text
files changed: 1
namespace_ownership.py: +6 / -2
```

Therefore the rejected non-functional churn is absent from the accepted final source tree.

## Validation pending

The `github-actions[bot]` repair commit does not itself trigger downstream workflows through `GITHUB_TOKEN`. This documentation checkpoint intentionally triggers normal branch workflows against the exact repaired source tree plus this report.

Final workflow IDs/results, exact HEAD, and final disposition will be appended after authoritative GitHub Actions completion.

## Mutation ledger so far

```text
live installer invocations: 0
live rollover-prepare invocations: 0
live rollover-finalize invocations: 0
manual lifecycle actions: 0
Gateway restarts: 0
live plugin/config/ownership/transaction/backup writes: 0
SQLite writes: 0
process terminations: 0
provider/model substitutions: 0
Discord Sends/API semantic traffic: 0
Release/tag/asset mutations: 0
force pushes/history rewrites: 0
```
