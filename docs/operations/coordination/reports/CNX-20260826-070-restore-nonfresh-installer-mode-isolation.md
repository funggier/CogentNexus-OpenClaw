# CNX-20260826-070 — Restore Non-Fresh Installer Mode Isolation

Result: `PASS_INSTALLER_MODE_ISOLATION_RESTORED`

Executor: Hermes (after the operator's continuation signal)

## Heads and provenance

- Fetched coordination HEAD at execution start:
  `71fdc66` (`coord: publish Task 070 installer mode isolation status`)
- Implementation HEAD:
  `9df671670908241486afe2badf8a7f221410c6f8`
- Report HEAD: this commit (report-only publication fence respected)
- Fresh isolated worktree from the fetched HEAD; remote/local HEAD verified,
  tree clean, Task-070 review ancestry confirmed
  (`a911216` review commit), and no prior Task-070 report existed.

## Resulting production control-flow shape

```powershell
# CNX-20260826-069 B1 / CNX-20260826-070: single production caught-failure
# boundary. The try body is SHARED by fresh/upgrade/legacy modes; only the
# catch branches on $isFreshTransaction.
try {
    # shared installer body (native handoff, skill install, validation,
    # npm/plugin work, runtime provisioning, ownership create + verify)
    if ($isFreshTransaction) { transaction-commit }   # fresh-only, after verify
} catch {
    if ($isFreshTransaction) {
        Invoke-FreshTransactionRollback -WorkspacePath $Workspace -OriginalError $_.Exception.Message
    }
    throw
}
```

- The `__UPGRADE_PASSTHROUGH__` synthetic sentinel and its catch branch are
  fully removed from `scripts/install.ps1`.
- No duplicated fresh/non-fresh installer bodies; one shared body.
- Post-commit ordering preserved: ownership create → exact verify → fresh
  transaction-commit → managed AGENTS policy → lifecycle enable.

## M1 — non-fresh reachability (RED/GREEN)

New suite `tests/test_installer_mode_isolation.py`.

RED against the Task-069 implementation: `test_m1_structural_no_synthetic_nonfresh_abort`
and `test_m2_nonfresh_failure_never_fresh_rolls_back` FAILED
(2 failed / 3 passed; evidence at `%LOCALAPPDATA%\Temp\cnx070-mode-isolation-*\b01-red-evidence.txt`).

GREEN proves:

- no synthetic throw keyed on `$isFreshTransaction == $false` exists anywhere;
- the non-fresh native-handoff entry point (`Enter-NativeInstallBoundary`)
  sits inside the protected shared body, i.e. reachable for upgrade/legacy;
- executable mode harness (`test_m1b_harness_upgrade_mode_reaches_installer_body`,
  mirroring the production try/catch shape with `$isFreshTransaction=$false`)
  reaches the body statements and prints `M1B_OK`.

## M2 — non-fresh failure never fresh-rolls back

Structural: the production catch gates `Invoke-FreshTransactionRollback` on
`$isFreshTransaction` ALONE (no sentinel branch — `test_m2b`). Executable:
harness injects `UPGRADE_BODY_FAILURE` with `$isFreshTransaction=$false`;
the original failure propagates and no rollback helper invocation occurs.

## M3 — fresh failure regression

The Task-069 injected-failure harness
(`test_f1_harness_injected_failure_triggers_production_rollback`) re-ran green:
same-run bounded rollback, exact residue removed, original error visible,
unrelated sentinel + shared parents survive, classification returns `fresh`.

## M4/M5 — upgrade/legacy never create a fresh marker

Covered by the existing transaction suites plus M1's reachability proof:
`transaction-begin` is invoked ONLY inside the
`if ($classification.mode -eq "fresh")` guard (structural test
`test_p1_begin_invoked_only_for_fresh_after_classification`, green), so no
`install-transaction.json` is created before any injected stop point in
upgrade/legacy paths. Legacy migration reachability follows from M1 (shared
body, native handoff reachable, no synthetic abort).

## M6 — syntax/control-flow check

Full `install.ps1` parsed via
`[System.Management.Automation.Language.Parser]::ParseFile` → zero errors
(`SYNTAX_OK`).

## M7 — accepted transaction regressions

All green: exact app-data created-vs-preexisting behavior, record-time unsafe
path rejection, committed-marker rollback refusal, crash/rerun recovery,
shared-parent preservation, malicious/tampered/unmarked marker fail-closed,
plugin inverse ordering, commit after ownership verify, AGENTS policy after
commit.

## Full verification

| Gate | Result |
|---|---|
| M1–M7 RED/GREEN | RED 2 failed vs Task-069; all GREEN after fix |
| tests/test_fresh_transaction_failure_coverage.py | passed |
| tests/test_installer_transaction_wiring.py | passed |
| tests/test_fresh_install_transaction_recovery.py | 10 passed |
| Full pytest (requirements-dev venv) | **342 passed, 2 skipped** (same 2 pre-existing environment skips), 4 subtests passed |
| npm 12.0.2 / node v22.23.2: `npm ci` + `plugin:validate` + `npm test` | exit 0 each |
| npm 11.16.0 (npx pin): `npm ci` + `plugin:validate` + `npm test` | exit 0 each |
| OpenClaw devDependency `2026.7.1-2`, plugin version `0.9.3` | exact |
| `python scripts/check_baseline_consistency.py` | PASS (Bridge v0.9.3) |
| `git diff --check` | clean |
| Clean worktree after implementation commit | yes |

Note: the first `npm test` attempts failed because a previous gate had pruned
devDependencies (`vitest` missing); re-running clean `npm ci` under each
toolchain restored them and both `npm test` runs then passed (exit 0). This is
environment sequencing, not a product defect.

## No-live-mutation accounting

Source/tests only. No install/uninstall/reset/lifecycle command executed on
the live machine; no Scheduled Task, Gateway, Ollama, plugin, config, AGENTS,
or SQLite mutation; no process termination; no primary-workspace mutation;
no reboot; no merge/tag/release. All fixtures ran under `%TEMP%` and the
isolated worktree. The Task-066 live residue remains intentionally untouched.

## Publication fence

Implementation/tests commit `9df6716`; this report-only commit adds exactly
one file under `docs/operations/coordination/reports/`.
