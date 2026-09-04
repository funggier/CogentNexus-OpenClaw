# CNX-20260904-240 — Task-239 Cross-Platform PowerShell Test Harness Portability Repair

## Objective

Close the Task-239 validation regression without changing the accepted production diagnostic-preservation repair.

## Parent and authority

- Parent task: `CNX-20260904-239`
- Parent independent review: `REJECT_PASS_CROSS_PLATFORM_VALIDATION_REGRESSION__PRODUCTION_DIAGNOSTIC_REPAIR_ACCEPTED_AS_FUNCTIONAL_CANDIDATE__TEST_HARNESS_PORTABILITY_REPAIR_REQUIRED`
- Production diagnostic repair candidate: `ec29020632091aae3b50149b51303a36fde26310`
- Task-239 report head: `b70606460c6ea3d8d37a3a8317946aa5b1ceec35`
- Entering coordination authority after review: `88425ab8bfa34c7e7657214ee972305a3891b3fd`
- Candidate plugin fingerprint: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- Public `v0.9.3`: `26ce64a624255278a3a0266ad38746e0e6ed2e31` (immutable)

Fresh GitHub state wins if anything above has changed.

## Existing RED

GitHub Actions Validate run `33830388146` on report HEAD `b70606460c6ea3d8d37a3a8317946aa5b1ceec35` is the authoritative existing RED.

Observed matrix behavior:

```text
windows-latest / Python 3.11: PASS
windows-latest / Python 3.14: PASS
ubuntu-latest / Python 3.11: FAIL
ubuntu-latest / Python 3.14: FAIL
macos-latest / Python 3.11: FAIL
macos-latest / Python 3.14: FAIL
```

The failing test is:

`tests/test_task239_rollover_diagnostics.py::test_bounded_diagnostic_helper_behavior_is_real_and_deterministic`

Confirmed Ubuntu exception:

`FileNotFoundError: [Errno 2] No such file or directory: 'powershell.exe'`

Root cause: the new test hard-codes `powershell.exe` even on non-Windows runners.

## Authorized scope

This is a **test-only portability repair**.

Allowed production/source changes:

```text
NONE
```

Specifically, do not modify:

- `scripts/install.ps1`
- rollover implementation
- plugin source/payload
- runtime/lifecycle/ownership code
- workflows merely to mask the test failure

The preferred minimal repair is to make the runtime-execution portion of `tests/test_task239_rollover_diagnostics.py` capability-aware while preserving the static assertions on every platform and preserving real PowerShell execution on Windows.

Acceptable examples include resolving an available PowerShell executable (`powershell.exe` and/or `pwsh`) or skipping only the runtime-execution subtest when no suitable PowerShell runtime exists. Do not skip the entire Task-239 regression file.

## Required verification

1. Reproduce/record the existing CI RED before editing.
2. Make the smallest test-only change.
3. Focused regression on Windows must execute the helper and pass.
4. Non-Windows validation must no longer fail merely because `powershell.exe` is absent.
5. Full Python validation must pass on the available local operator environment.
6. Plugin tests/validation must remain unchanged and pass where normally required.
7. `git diff --check` must pass.
8. Compute plugin fingerprint; it must remain exactly:

   `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

9. Publish a final candidate SHA and obtain fresh GitHub Actions on that exact SHA:
   - Validate = SUCCESS
   - Windows Installer Pack Smoke = SUCCESS
   - PS5.1 Acceptance Smoke = SUCCESS

Do not claim PASS from a descendant docs-only SHA if the final candidate SHA itself has no direct Actions evidence. If the repository push mechanics would otherwise batch commits, arrange publication so the final test-repair candidate SHA is actually exercised by Actions before publishing the report.

## Live evidence boundary

Task 240 is repository-only. Preserve the retained live state from Task 237/238:

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

No live normalization is authorized.

## Zero-effect budget

```text
live installer registrations/starts/invocations: 0
live rollover-prepare/finalize: 0
manual plugin mutation: 0
manual controller/Gateway/lifecycle mutation: 0
manual Ticket/outbox/recovery/SQLite writes: 0
Dashboard semantic submissions: 0
Discord semantic submissions: 0
direct Discord/API sends: 0
recovery replay/resend: 0
process termination: 0
provider/model substitution: 0
forensic evidence cleanup/mutation: 0
release/tag/asset mutation: 0
force push/history rewrite: 0
```

## Report and stop boundary

Publish:

`docs/operations/coordination/reports/CNX-20260904-240-task239-cross-platform-powershell-test-harness-portability-repair.md`

Report exact changed files, candidate SHA, plugin fingerprint, focused/full tests, exact Actions run IDs/conclusions, zero-effect ledger, and final disposition.

Then STOP for independent ChatGPT review. Do not rerun the live installer or begin semantic requalification in Task 240.
