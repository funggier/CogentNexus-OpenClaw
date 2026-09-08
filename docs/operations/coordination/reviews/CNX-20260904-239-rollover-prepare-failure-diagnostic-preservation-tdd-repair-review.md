# CNX-20260904-239 — Independent Review

## Verdict

`REJECT_PASS_CROSS_PLATFORM_VALIDATION_REGRESSION__PRODUCTION_DIAGNOSTIC_REPAIR_ACCEPTED_AS_FUNCTIONAL_CANDIDATE__TEST_HARNESS_PORTABILITY_REPAIR_REQUIRED`

## Authority reviewed

- Task report head entering review: `b70606460c6ea3d8d37a3a8317946aa5b1ceec35`
- Task-239 RED commit: `2c5d68384df11e38b9cea5e565c247324c4c5f44`
- Task-239 production repair commit: `ec29020632091aae3b50149b51303a36fde26310`
- Candidate plugin fingerprint remains: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- Public `v0.9.3` remains immutable at `26ce64a624255278a3a0266ad38746e0e6ed2e31`.

## TDD adjudication

The RED commit is test-only and the production repair commit is its direct child. The RED test exposes the missing stderr merge and bounded diagnostic contract while preserving the nonzero fail-closed assertion.

The production repair is narrow:

- `rollover-prepare` capture now uses `2>&1 | Out-String`;
- child output is bounded to 4096 characters;
- empty output has a deterministic placeholder;
- overlong output preserves head and tail with a truncation marker;
- the existing nonzero failure remains fail-closed;
- rollover arguments, ownership semantics, backup/hash/transaction semantics, ordering, and retry cardinality are unchanged.

The production repair is therefore accepted as a functional repository candidate. No additional production change is authorized by this review.

## Validation defect discovered by independent review

Task-239 report claimed PASS, but the authority required exact-SHA Actions GREEN. Fresh GitHub evidence does not satisfy that gate:

1. The intermediate repair SHA `ec29020632091aae3b50149b51303a36fde26310` has no direct Actions runs because the pushed tip was the later report commit.
2. Report HEAD `b70606460c6ea3d8d37a3a8317946aa5b1ceec35` has:
   - PS5.1 Acceptance Smoke: SUCCESS
   - Windows Installer Pack Smoke: SUCCESS
   - Validate: FAILURE
3. Validate fails on Ubuntu and macOS at `tests/test_task239_rollover_diagnostics.py::test_bounded_diagnostic_helper_behavior_is_real_and_deterministic` because the test unconditionally executes `powershell.exe`.
4. The exact Ubuntu failure is `FileNotFoundError: [Errno 2] No such file or directory: 'powershell.exe'`.
5. Windows Python 3.11 and 3.14 matrices pass the same test and full validation.

This is a test-harness portability regression introduced by Task 239, not evidence that the production diagnostic repair is incorrect.

## Live boundary

Task 239 remained repository-only. The retained live evidence boundary from Task 238/237 must remain untouched:

```text
controller = passthrough
generation = 39
Gateway healthy
provider = ollama
Delivery READY / pending 0
Recovery READY
SQLite integrity = ok
candidate plugin not installed
predecessor plugin fingerprint = e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
```

No installer, rollover, semantic send, replay, lifecycle normalization, or forensic-evidence mutation is authorized until the validation regression is repaired and independently reviewed.

## Successor requirement

Open a repository-only successor to repair only the portability of `tests/test_task239_rollover_diagnostics.py`.

The successor must:

- treat current non-Windows CI failure as the existing RED;
- make the PowerShell behavioral test capability-aware (for example, execute an available PowerShell runtime, or skip the runtime-execution subtest when no suitable PowerShell executable exists while retaining static contract checks);
- preserve Windows behavioral execution;
- not modify `scripts/install.ps1` or any production/runtime source;
- run focused tests and full repository validation;
- obtain fresh Actions SUCCESS for Validate, Windows Installer Pack Smoke, and PS5.1 Acceptance Smoke on the final successor SHA;
- preserve plugin fingerprint `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`;
- keep live installer and semantic budgets at zero.

Only after that successor passes independent review may live install-over requalification be reconsidered.
