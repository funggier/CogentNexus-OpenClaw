# CNX-20260825-065 — Close Installer Runtime-Authority Gaps

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_REWORK_TDD_INSTALLER_INTEGRATION`

Current authorization: `INSTALLER_RUNTIME_AUTHORITY_CLOSURE_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes after the operator's continuation signal

## Goal

Close the remaining installer-facing runtime-authority defects found during independent review of Task 064, without changing the live CogentNexus-OpenClaw installation.

This task is intentionally narrow. Do not redesign CogentNexus, provider logic, plugin lifecycle, Ticket behavior, or supervisor cadence.

The corrected source must be safe to use for the already-authorized clean uninstall/fresh reinstall successor.

## Accepted predecessor evidence

Task 064 report result:

`PASS_WINDOWS_RUNTIME_AUTHORITY_REWORK_VERIFIED`

Task 064 implementation HEAD:

`6e4245112a38dab3e6614e6f91d3e37ac85f2afe`

Task 064 report HEAD:

`f3a4731b87f8a530dd71eed3826a93f963a9de34`

Independent review:

`REWORK_INSTALLER_RUNTIME_AUTHORITY_EXECUTION_GAPS`

Review commit:

`5fe706d89f41083fda37d2032c17bc0ba6e1d353`

The Task 063 diagnosis remains accepted as `FLASH_CHILD_PROCESS`. Task 064's B1-B3 corrections in `runtime_authority.py` / `startup.py` are useful and should not be reverted unless a failing regression proves necessity.

## Blocking defects to correct

### B5 — production installer contains a broken runtime-authority script path

The Task 064 implementation commit contains a literal line break inside the path:

```powershell
& python (Join-Path $targetSkill "scripts\
untime_authority.py") ensure-runtime ...
```

The production installer must resolve exactly:

`<targetSkill>\scripts\runtime_authority.py`

with no embedded CR/LF or other malformed character.

### B6 — installer skips validation when python.exe merely exists

Current source invokes `ensure-runtime` only when `$ownedPython` does not exist.

This is insufficient. The product runtime must be validated on every install/install-over before any durable launcher or Scheduled Task definition can reference it.

If the manifest is missing/corrupt, foreground/background interpreter is missing, or a validation/probe fails, the supported install path must deterministically recreate/repair the runtime inside the exact CogentNexus application-data boundary or fail closed before durable authority changes.

Do not treat `Test-Path python.exe` as runtime validity.

### B7 — post-provision product execution still uses ambient bare python unnecessarily

After owned runtime authority is established, the installer still invokes normal stdlib-capable CogentNexus paths with bare `python`, including lifecycle enable/status and ownership helpers.

Audit each post-provision Python call. Use the exact `$ownedPython` for every product operation that runs correctly with the product runtime, especially:

- `cnxclaw_v093.py ... enable --provider ollama`;
- final `cnxclaw_v093.py ... status`;
- `namespace_ownership.py` resolve/create/verify/rollover operations if its imports are stdlib-only;
- `runtime.py supervisor doctor` if its normal imports are supported by the owned runtime.

A bootstrap Python may remain only for operations that necessarily precede provisioning or require an explicitly documented installer-only dependency such as PyYAML. Such bootstrap execution must never be persisted into launcher/task/runtime manifest authority.

Do not install developer-only packages into the product runtime merely to eliminate a harmless bootstrap-only pre-provision check.

## Required method — strict TDD

Use a fresh isolated clone/worktree at current branch HEAD.

Before production edits:

1. verify `ACTIVE.md`, `STATUS.md`, this task, and review 064 agree;
2. verify no Task 065 report exists;
3. write regression tests for B5, B6, and B7;
4. run them against current Task 064 source and observe the intended RED failures;
5. make the minimum cohesive production corrections;
6. run focused GREEN, existing installer/runtime tests, full canonical tests, validators, and diff checks;
7. publish implementation commit(s), then a separate report-only commit.

No production edit before the relevant failing test is observed.

## Required production behavior

### 1. One explicit runtime-authority script variable

In `scripts/install.ps1`, resolve the installed script once, e.g.:

```powershell
$runtimeAuthorityScript = Join-Path $targetSkill "scripts\runtime_authority.py"
```

Before invoking it, prove `Test-Path -LiteralPath $runtimeAuthorityScript` and fail with an actionable message if absent.

The committed source must not split the relative path across lines.

### 2. Unconditional runtime ensure/validation before durable definitions

Once the target skill containing `runtime_authority.py` exists, invoke the runtime authority on every install/install-over, not only when `python.exe` is absent.

Preferred shape:

```powershell
$runtimeManifestJson = (& python $runtimeAuthorityScript ensure-runtime --application-data-root $applicationDataRoot | Out-String)
if ($LASTEXITCODE -ne 0) { throw ... }
$runtimeManifest = $runtimeManifestJson | ConvertFrom-Json
$ownedPython = [string]$runtimeManifest.foregroundInterpreter
$ownedPythonw = [string]$runtimeManifest.backgroundInterpreter
```

Equivalent implementation is allowed, but it must consume a validated/probed runtime result rather than infer validity from file existence alone.

Before launcher/task/lifecycle enable, require both owned interpreter paths to exist under the exact application-data runtime boundary.

### 3. Existing-runtime validation must probe both interpreters

If `runtime_authority.ensure_runtime()` reuses an existing manifest, it must validate executable capability of both foreground `python.exe` and background `pythonw.exe`, not only file existence/foreground execution.

If a probe fails, either recreate the runtime safely within the product boundary or fail closed with clear evidence. Do not register a broken `pythonw.exe` merely because the file exists.

### 4. Post-provision authority

After a valid owned runtime is established, use `$ownedPython` for normal stdlib-capable product operations.

At minimum, MANAGED `enable` and final `status` must execute under `$ownedPython`.

The generated `cnxclaw.cmd` must continue to invoke the exact owned foreground interpreter.

Windows Scheduled Task creation must continue to resolve only the validated owned background interpreter via `startup.py` and must not regain any `sys.executable` fallback.

## Mandatory regression coverage

Add/update tests so the production installer-facing defects cannot recur.

### T1 — exact committed runtime-authority path

Test the real `scripts/install.ps1` source contract and fail on an embedded newline/CR or malformed relative path.

At minimum assert the resolved literal is exactly `scripts\runtime_authority.py`. Prefer executing a small PowerShell extraction/helper if practical; a focused source assertion is acceptable for this literal corruption only when combined with T2 executable coverage.

RED against Task 064 must fail because of B5.

### T2 — actual installer runtime ensure boundary

Exercise the same production runtime-ensure helper/block used by `install.ps1` against a temporary application-data root.

The test must demonstrate all of:

1. fresh runtime provisioning succeeds;
2. deleting/corrupting `runtime-manifest.json` while leaving `Scripts\python.exe` present causes install-facing ensure to run and recreate/validate the manifest;
3. removing/corrupting `pythonw.exe` cannot be accepted as healthy merely because `python.exe` exists;
4. exact runtime root remains `<temp>\CogentNexus-OpenClaw\runtime\python`.

Do not satisfy this test solely by calling `runtime_authority.ensure_runtime()` directly without exercising the installer-facing call boundary; that was the Task 064 blind spot.

If necessary, factor only the small runtime-bootstrap portion into a dedicated testable script/helper used by production `install.ps1`. Avoid broad installer refactoring.

### T3 — post-provision enable/status authority

Verify the production `install.ps1` path for MANAGED enable and final status uses `$ownedPython`, not bare `python`.

Where practical, use a marker interpreter/helper in a non-mutating temp harness. Otherwise combine a narrow source contract assertion with executable tests proving the owned interpreter can execute `cnxclaw_v093.py --help`/import surface.

### T4 — background corruption behavior

Provision a real temp runtime, then make the background interpreter unusable in a reversible temp-only way or construct an equivalent isolated fixture. Verify existing-runtime validation does not return it as healthy.

### T5 — preserve prior Task 064 coverage

Keep passing coverage for:

- exact product-root semantics;
- real Windows foreground/background provisioning;
- startup fail closed with foreign executor `sys.executable`;
- owned launcher execution;
- normal product CLI import/start capability;
- Windows no-console spawn flags;
- v0.9.2 startup target `host_control_v092.py`.

## Verification

Use an isolated developer test environment with `requirements-dev.txt`; do not alter the live product runtime or global Python.

Record fresh results for:

1. B5/B6/B7 RED tests before source correction;
2. focused GREEN tests;
3. existing runtime/startup/install/ownership/host-control tests;
4. full `pytest tests/ -q` with exact pass/skip/fail/error counts;
5. `python scripts/check_baseline_consistency.py`;
6. any existing PowerShell/installer validation relevant to `install.ps1`;
7. `git diff --check`;
8. clean worktree after implementation commit.

Do not claim PASS from a test suite that never executes or checks the production installer boundary that failed review.

## Live hard fence

Task 065 is source/tests only.

No live:

- install/install-over/uninstall/reset;
- `cnxclaw` lifecycle operation;
- Scheduled Task create/update/delete/run/end;
- Gateway/Ollama/provider/plugin/config/AGENTS/ownership/SQLite mutation;
- process kill;
- primary workspace git mutation;
- merge/tag/release;
- HermesAgent project mutation.

All runtime tests must use temporary directories outside the live product boundary.

## Publication discipline

Use separate commits:

1. implementation/tests commit(s);
2. final report-only commit adding only:

`docs/operations/coordination/reports/CNX-20260825-065-close-installer-runtime-authority-gaps.md`

The report must state fetched execution HEAD, implementation HEAD, report HEAD/publication fence, RED/GREEN evidence, exact installer/runtime behavior, full suite results, and explicit no-live-mutation accounting.

## Result tokens

Exactly one:

- `PASS_INSTALLER_RUNTIME_AUTHORITY_GAPS_CLOSED`
- `BLOCKED_INSTALLER_RUNTIME_AUTHORITY`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

A PASS remains source-only evidence. It does not mean the current machine has been repaired.

## Pre-authorized successor

If ChatGPT independently accepts `PASS_INSTALLER_RUNTIME_AUTHORITY_GAPS_CLOSED`, proceed immediately to the already-authorized bounded clean uninstall/fresh reinstall task, with preservation evidence, exact owned-runtime binding verification, and multiple natural supervisor ticks proving no recurring console flash. No additional human confirmation is required for that successor.
