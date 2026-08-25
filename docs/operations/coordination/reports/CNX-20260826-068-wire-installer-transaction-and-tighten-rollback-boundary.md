# CNX-20260826-068 — Wire Installer Transaction and Tighten Rollback Boundary

Result: `PASS_PRODUCTION_INSTALLER_TRANSACTION_WIRED`

Executor: Hermes
Report date: 2026-08-26 ICT
Fetched execution HEAD: `85352bb073bb3be1b1a563db40a57f37e892b152` (== local HEAD at start; Task 067 review commit `38b46a4` verified ancestor; no prior Task 068 report)
Isolated worktree: `%LOCALAPPDATA%\Temp\cnx068-worktree`, branch `cnx068-wiring`
Implementation HEAD: `2a0ca9fd9abda07765e3da222f7fc4d7730d3d30`

Task 067 D1 lockfile fix is preserved unchanged (`package.json`/`package-lock.json` untouched in this task).

## D2c — exact-root deletion boundary

### P5 RED (baseline `85352bb`)

`tests/test_p5_exact_root_boundary.py`: rollback/recovery removed the shared preexisting `<workspace>\skills` parent after deleting the owned skill root. RED captured: `test_p5b_recovery_preflight_preserves_shared_parent` failed with "shared parent <workspace>\skills must survive recovery".

### Fix

Removed the upward empty-parent walk from `rollback_transaction()` and the upward `parent.rmdir()` pass from `recovery_preflight()`. Deletion authority now stops at the exact owned roots (`stateRoot`, `skillPath`); only a now-empty owned root itself may be removed; shared parents are never touched.

### GREEN

Both P5 tests pass: owned skill root removed; `<workspace>\skills` survives; unrelated sibling content intact.

## D2a/D2b — production installer wiring

### P1/P2/P3/P4 RED (baseline `85352bb`)

`tests/test_installer_transaction_wiring.py` structural assertions against the actual production `scripts/install.ps1` all failed: no fresh-guarded `transaction-begin`, no record coverage, no rollback helper, no verification-gated commit.

### Production behavior now implemented in scripts/install.ps1

Ordered control path:

1. `classify-install` proves mode;
2. **fresh-only guard**: `transaction-begin --workspace --app-data` invoked only when `$classification.mode -eq 'fresh'` (upgrade/legacy paths never begin a transaction), after classification and before the first residue-capable mutation (`New-Item`/staging/copy of skill);
3. **recording before/at creation**: `transaction-record` for `targetSkill`, `cogentNexusOpenClawRoot`, launcher (`cnxclaw.cmd`, recorded immediately before `Set-Content`), and `%LOCALAPPDATA%\CogentNexus-OpenClaw` when it does not yet exist;
4. **caught-failure rollback**: ownership-manifest creation and exact-verification failures invoke `Invoke-FreshTransactionRollback`, which runs `transaction-rollback` and reports BOTH the original install error and any rollback error/state (never masks either); hard crashes remain covered by rerun `recovery-preflight`;
5. **commit ordering**: `transaction-commit` is invoked strictly AFTER ownership create + exact `verify` success, so the marker never authorizes cleanup before coherent ownership exists.

New production CLI surface added to `namespace_ownership.py`: `transaction-rollback`.

Plugin registration / Scheduled Task / gateway effects are NOT represented as filesystem deletions — rollback stays bounded to filesystem roots recorded by the transaction.

### GREEN evidence

- All 5 installer wiring tests pass (P1 begin ordering + fresh-only guard; P2 record coverage for state/skill/launcher/app-data; P3 rollback helper contract reporting both errors; P4 verify-gated commit ordering; executable checks).
- Removing any required `transaction-record` call or the fresh guard makes the tests fail (assertions require each literal call site).
- P6: Task 067 R1–R7 suite still fully green (10/10) including malicious-marker rejection and unmarked-residue fail-closed.

## P7 — crash/rerun production integration

Executable PowerShell harness (real `python` invocations of the same production surfaces the installer wires): transaction-begin → create host/controller.json + skill dir with transaction-record per artifact → simulated hard crash (no caught rollback) → production `recovery-preflight` returns `RECOVERED_FRESH` → `classify-install` returns `fresh` → owned residue removed → shared `skills` parent preserved. PASS (`P7_OK`).

## D1 regression gate (both toolchains, clean node_modules)

| Gate | npm 11.16.0 / node v24.18.0 | npm 12.0.2 / node v22.23.2 |
|---|---|---|
| clean `npm ci` | PASS | PASS |
| `npm run plugin:validate` | PASS | PASS |
| `npm test` | 237/237 passed | 237/237 passed |
| lock/package drift after ci | none (`git diff --exit-code`) | none |

Exact OpenClaw dependency `2026.7.1-2`, plugin version `0.9.3` unchanged.

## Full verification

- `pytest tests/ -q` (isolated venv, requirements-dev installed): **319 passed, 2 skipped** (pre-existing platform-gated skips), 4 subtests.
- `python scripts/check_baseline_consistency.py`: PASS (Bridge v0.9.3).
- `git diff --check`: clean.
- Worktree clean after implementation commit.

## No-live-mutation accounting

Live machine re-verified after execution: Task-066 partial residue untouched at both reported roots; no Supervisor Scheduled Task; no launcher/plugin registration; Gateway/Ollama/AGENTS/SQLite/config untouched. All testing used the isolated worktree, temp dirs, and PowerShell harnesses.

## Publication fence

This commit adds ONLY:
`docs/operations/coordination/reports/CNX-20260826-068-wire-installer-transaction-and-tighten-rollback-boundary.md`

Implementation commit: `2a0ca9fd9abda07765e3da222f7fc4d7730d3d30` (parent `85352bb...`).
