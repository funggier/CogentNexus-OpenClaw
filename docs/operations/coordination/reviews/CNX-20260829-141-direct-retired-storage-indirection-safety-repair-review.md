# CNX-20260829-141 — Direct Retired-Storage Indirection Safety Repair Review

- **Task:** `CNX-20260829-141`
- **Report:** `docs/operations/coordination/reports/CNX-20260829-141-direct-retired-storage-indirection-safety-repair.md`
- **Reviewed report commit:** `28be1b3fb3362fccac913167732fc38c9dd25860`
- **Reviewed production repair:** `138759d111fe27a0cda75f59ad108d11caf19120`
- **Disposition:** **ACCEPT**
- **Review date:** 2026-08-29 ICT

## Review verdict

Task 141 closes the specific filesystem-indirection safety gap that blocked acceptance of Task 140. The RED is meaningful, the repair is narrow at the owning boundary, the legitimate direct-extension topology remains supported, managed npm-project ownership remains strict, and exact-repair-SHA CI is GREEN across Windows, Linux, and macOS validation.

This review accepts the **offline source repair only**. It does not itself claim that the repaired candidate is installed on the user's live Windows runtime and does not authorize Dashboard semantic acceptance.

## Independently verified evidence

### 1. The RED matches the rejected Task-140 behavior

The report records a real Windows junction fixture at the canonical direct extension path. Against the Task-140 implementation, `prepare_plugin_rollover_transaction()` did not raise and proceeded far enough to authorize/create backup state. That reproduces the exact review finding: root-level indirection identity was erased before authorization.

The fixture is not merely a mocked metadata test. It exercises the actual prepare boundary with a coherent manifest and an in-state redirected retired payload.

### 2. The production change is narrow

Commit `138759d111fe27a0cda75f59ad108d11caf19120` changes only:

- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`;
- `tests/test_plugin_generation_rollover.py`.

The source change:

1. adds `_is_reparse_point(path)` using non-resolving symlink/junction/reparse evidence;
2. retains the manifest plugin path lexically until direct-root authorization;
3. authorizes the canonical direct root only when that lexical root is not a symlink/junction/reparse point;
4. resolves only after that attestation and rechecks state-boundary containment;
5. routes every non-direct path through the unchanged strict `_npm_project_for_plugin()` ownership proof.

No arbitrary extension directory is newly authorized and no managed npm wrapper rule is weakened.

### 3. Positive and negative behavior are both covered

The new regression rejects the indirected canonical direct root before backup creation. The accepted Task-140 regression still proves a normal real direct extension directory is allowed. Existing rollover tests retain managed npm-project success and foreign/shared/ambiguous/boundary rejection behavior.

The same test file is executed by the full repository pytest matrix. On Windows, the test can create a junction with `mklink /J` when ordinary symlink creation is unavailable. On Linux/macOS, ordinary symlink construction exercises the portable path.

### 4. Fresh exact-SHA CI evidence is GREEN

For exact repair SHA `138759d111fe27a0cda75f59ad108d11caf19120`:

- PS5.1 Acceptance Smoke run `33256641609`: `completed / success`;
- Windows Installer Pack Smoke run `33256641648`: `completed / success`;
- Validate run `33256641615`: `completed / success`.

The Validate matrix includes Windows Python 3.11 and 3.14 jobs; both ran full `python -m pytest -q`, PowerShell syntax/acceptance smoke, npm test, and `plugin:validate` successfully. Linux/macOS validation also ran full pytest and plugin validation successfully.

### 5. Candidate ancestry is coherent

GitHub comparison proves `138759d111fe27a0cda75f59ad108d11caf19120` is a descendant of the accepted Dashboard durable-capture repair `16f5c396e9be0af8d1bd34824fe2993613501a6f` (`ahead`, behind `0`). Therefore the exact candidate for a later deployment proof contains both the Dashboard repair and the subsequently accepted installer ownership-safety lineage.

## Accepted Task-141 verdict

`PASS` is accepted for the offline repair/validation scope.

The Task-140 `REWORK` blocker is closed by this successor. Task 140's functional direct-extension fix plus Task 141's lexical root attestation are accepted together as the installer repair lineage.

## Deployment boundary

The next safe step is one controlled live install-over retry from a detached worktree at exact source commit:

`138759d111fe27a0cda75f59ad108d11caf19120`

The live retry must **not** manually normalize the Task-139 post-failure state first. It must begin with read-only state capture; if the observed state has materially drifted from the accepted predecessor boundary, it must stop before mutation. If coherent, it may invoke the supported installer exactly once and then prove both plugin/runtime provenance and installed skill-script provenance.

No Dashboard semantic Send belongs in that deployment-proof task.
