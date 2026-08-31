# CNX-20260828-106 — npm 12 Installer Contract Regression Repair

**Status:** `READY_FOR_HERMES`  
**Execution mode:** `SOURCE_ONLY_TDD`  
**Owner / reviewer:** ChatGPT  
**Executor:** Hermes/Codex  
**Branch:** `agent/v0.9.3-full-stabilization`

## Purpose

Close the source-test regression exposed after Task 105 identified a real Windows installer incompatibility between OpenClaw `2026.7.1-2` and npm `12.0.2` when the installer used the OpenClaw `npm-pack:` metadata path.

This is a **source-only** task. It must not touch the live Windows runtime.

## Accepted root cause and repair context

Task 105 failed during install-over after the existing MANAGED deployment safely handed off to PASSTHROUGH. The real machine is intentionally preserved in PASSTHROUGH generation 25.

The verified root cause is:

- the machine uses npm `12.0.2`;
- npm 12 returns keyed-object `npm pack --json` metadata;
- OpenClaw `2026.7.1-2` commit `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c` expects the legacy/direct package metadata shape in its `npm-pack:` path;
- OpenClaw therefore emits `npm pack metadata read produced incomplete package metadata`;
- this is an OpenClaw `2026.7.1-2` × npm 12 compatibility failure, not a malformed CogentNexus-OpenClaw package.

Accepted repair commits already present in branch history:

1. RED structural regression: `e0b6173d2ed888303bae3e31fd023b24e201c167`
   - Windows Installer Pack Smoke rejects the old `npm-pack:` invocation and requires a plain local package archive path.
   - RED run `33148334137` failed at the intended assertion.
2. Minimal production fix: `c676c50cb19378541a8223263a609fb7d18ed5a8`
   - `scripts/install.ps1` changed only the OpenClaw install invocation from `npm-pack:<path>` to the exact local `.tgz` path and updated the error label.
3. Production-shaped npm 12 regression: `5e41c0c3a8b9da920571b828c9a863f5591af86b`
   - Windows smoke pins npm `12.0.2`;
   - proves keyed-object `npm pack --json` output;
   - exercises `Resolve-NpmPackArtifact` on that exact shape;
   - requires the npm12-safe local archive invocation;
   - validates the resulting package contents.
   - Windows Installer Pack Smoke run `33148715184` is SUCCESS through every npm12-specific step.

Do not revert, broaden, or redesign these accepted changes in Task 106.

## Current failing gate

Validate run `33148715162` for exact source `5e41c0c3a8b9da920571b828c9a863f5591af86b` reaches `python -m pytest -q` and fails only three stale structural assertions:

1. `tests/test_fresh_transaction_failure_coverage.py::test_f2_structural_plugin_inverse_and_policy_order`
2. `tests/test_namespace_install_contract.py::test_windows_installer_applies_verified_rollover_before_single_candidate_resolution`
3. `tests/test_npm_pack_installer_boundary.py::test_install_wires_single_normalizer_and_exact_artifact`

Observed aggregate result:

`3 failed, 390 passed, 30 skipped, 4 subtests passed`

All three failures hard-code the former string:

`openclaw plugins install ("npm-pack:" + $packagePath) --force`

The behavioral/ordering invariants those tests protect remain valid and must stay protected.

## Required changes

Use the smallest possible test-only patch.

### 1. Fresh transaction inverse/order test

In `tests/test_fresh_transaction_failure_coverage.py`, update only the installer-position lookup in `test_f2_structural_plugin_inverse_and_policy_order` so it finds the current local-archive invocation:

`openclaw plugins install $packagePath --force`

Preserve the existing assertion that the successful plugin installation occurs before `$script:FreshPluginInstalled = $true`, and preserve the policy-after-commit assertion.

### 2. Namespace install ordering test

In `tests/test_namespace_install_contract.py`, update the Windows installer `install = source.index(...)` expression in `test_windows_installer_applies_verified_rollover_before_single_candidate_resolution` to use:

`openclaw plugins install $packagePath --force`

Preserve all existing install → inventory → plan → apply → resolve ordering assertions and guards.

Do not change the POSIX installer contract in this task unless an independently failing test proves a real analogous defect. The Task-105 failure and accepted repair are Windows/npm12-specific.

### 3. npm-pack artifact boundary test

In `tests/test_npm_pack_installer_boundary.py`, update `test_install_wires_single_normalizer_and_exact_artifact` so it positively requires:

`openclaw plugins install $packagePath --force`

and negatively rejects the former exact executable invocation:

`openclaw plugins install ("npm-pack:" + $packagePath) --force`

Continue to require:

- `resolve-npm-pack-artifact.ps1`;
- `Resolve-NpmPackArtifact`;
- exact package-path existence proof;
- removal of the temporary package artifact.

Do not weaken npm11-array or npm12-keyed-object helper tests.

## Verification

Before publishing the report, run at minimum:

```text
python -m pytest -q tests/test_fresh_transaction_failure_coverage.py tests/test_namespace_install_contract.py tests/test_npm_pack_installer_boundary.py
python -m pytest -q
python scripts/check_namespace_isolation.py
python scripts/check_baseline_consistency.py
```

If practical in the executor environment, also run the plugin build/validation commands used by CI. Do not claim GitHub Actions success from local execution; simply push the bounded test repair and allow Actions to run on the exact resulting commit.

## Diff fence

Task 106 may modify only these files unless a newly observed failure requires an explicitly documented additional test-only correction:

- `tests/test_fresh_transaction_failure_coverage.py`
- `tests/test_namespace_install_contract.py`
- `tests/test_npm_pack_installer_boundary.py`
- the Task-106 report itself

Do **not** modify:

- `scripts/install.ps1`;
- `.github/workflows/windows-installer-pack-smoke.yml`;
- plugin/package source;
- lifecycle/runtime source;
- baseline/version files;
- dependency versions.

If the required focused tests cannot pass without changing production code, stop and report `BLOCKED`; do not expand scope.

## Hard live fence

Task 106 does **not** authorize any live-machine mutation. Specifically do not:

- install/install-over/uninstall/reset CogentNexus-OpenClaw;
- enable/disable/start/stop/restart CogentNexus-OpenClaw, OpenClaw Gateway, Supervisor, or Ollama;
- change npm/Node/OpenClaw/Ollama versions on the user's machine;
- modify live SQLite/config/session/runtime state;
- send a Dashboard semantic message;
- access/re-enter credentials/tokens/passwords;
- reboot;
- merge/tag/publish a GitHub Release/force-push.

The preserved live state remains PASSTHROUGH generation 25 until a later explicitly authorized acceptance task.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260828-106-npm12-installer-contract-regression-repair.md`

The report must contain:

- `PASS`, `FAIL`, or `BLOCKED`;
- exact implementation commit SHA;
- exact changed-file list/diff summary;
- focused-test results;
- full pytest result;
- namespace/baseline check results;
- confirmation that production source/workflow were unchanged by Task 106;
- confirmation that no live-machine action was performed.

After pushing the report, stop for independent ChatGPT review. Do not start or invent the next live task.