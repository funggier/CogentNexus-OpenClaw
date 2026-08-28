# CNX-20260828-106 — npm 12 Installer Contract Regression Repair

Status: `PASS`

## Task identity

- Task ID: `CNX-20260828-106`
- Branch: `agent/v0.9.3-full-stabilization`
- Executor: Hermes/Codex
- Source worktree: `C:\Users\CDQ-P\AppData\Local\Temp\cnx106-state-20260828T064720Z\clone`
- Implementation commit: `80a48f73d3c525565a15e07ed1ed37a7c4fc4ad3`
- Task-105 failure evidence was preserved; no live recovery was attempted.

## Accepted ancestry verified

The required commits were present and verified in the source clone:

- `e0b6173d2ed888303bae3e31fd023b24e201c167` — RED structural installer-path regression
- `c676c50cb19378541a8223263a609fb7d18ed5a8` — minimal npm12-safe production fix
- `5e41c0c3a8b9da920571b828c9a863f5591af86b` — npm12 production-shaped regression

## Change scope

Only the three task-authorized test files were modified:

1. `tests/test_fresh_transaction_failure_coverage.py`
   - updated the F2 installer-position lookup to locate `plugins install $packagePath --force`;
   - preserved plugin-success flag ordering and post-commit policy ordering assertions.
2. `tests/test_namespace_install_contract.py`
   - updated the Windows install-order lookup to `openclaw plugins install $packagePath --force`;
   - preserved install → inventory → rollover plan → apply → resolve ordering and guards.
3. `tests/test_npm_pack_installer_boundary.py`
   - positively requires the local archive invocation;
   - negatively rejects the former `npm-pack:` executable invocation;
   - preserved resolver, exact artifact existence, and cleanup assertions.

`git diff --check` passed. The diff fence confirmed no changes to `scripts/install.ps1`, `.github/workflows/windows-installer-pack-smoke.yml`, plugin/source files, version files, or dependencies.

## Verification results

All commands ran from the source clone and were captured under:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx106-state-20260828T064720Z\evidence`

- Focused tests, initially attempted with the Hermes Python environment: root exit `1` because `pytest` was not installed.
- Focused tests rerun with ephemeral `uv run --no-project --with 'pytest>=8,<10' --with 'PyYAML>=6,<7'`:
  - `32 passed in 4.35s`
  - root exit `0`
- Full pytest with the same ephemeral environment:
  - `420 passed, 3 skipped, 4 subtests passed in 79.51s`
  - root exit `0`
- `python scripts/check_namespace_isolation.py`:
  - `CogentNexus-OpenClaw namespace isolation: PASS`
  - root exit `0`
- `python scripts/check_baseline_consistency.py`:
  - `CogentNexus-OpenClaw v0.9.3 baseline consistency: PASS (Bridge v0.9.3)`
  - root exit `0`

Evidence files:

- `focused-pytest-uv.txt`
- `full-pytest-uv.txt`
- `namespace-isolation.txt`
- `baseline-consistency.txt`
- `a source-only diff/commit was verified before report publication`

## Live-machine safety confirmation

Task 106 performed no live-machine action. Specifically:

- no install/install-over/uninstall/reset/cleanup;
- no CNX, OpenClaw Gateway, Supervisor, or Ollama start/stop/restart/enable/disable;
- no live SQLite/config/session/runtime mutation;
- no npm, Node, OpenClaw, or Ollama version change;
- no Dashboard semantic Send;
- no credential/token/password access or re-entry;
- no reboot, merge, tag, Release, or force push.

The live state remains the Task-105 preserved state: CogentNexus-OpenClaw `PASSTHROUGH`, generation `25`, Gateway healthy, Ollama healthy, SQLite healthy.

## Final verdict

`PASS`

The stale structural assertions were repaired with the smallest test-only patch. Focused and full verification passed, namespace and baseline checks passed, and production source/workflow plus the live runtime were unchanged by Task 106.

After publishing this report, stop for independent ChatGPT review. No next task was invented or started.
