# CNX-20260826-073 — Correct Clean-Fresh Recovery Preflight Semantics

Result: `PASS_CLEAN_FRESH_RECOVERY_PREFLIGHT_CORRECTED`

Executor: Hermes (after the operator's continuation signal)

## Heads

- Fetched coordination HEAD at execution start: `99a22c6` (`coord: publish Task 073 recovery preflight status`)
- Implementation HEAD: `79b51ed06363f6e8862c491ee0a313ddb412c806`
- Report HEAD: this commit (report-only publication fence)
- Fresh isolated worktree from `99a22c6`; clean tree; no prior Task-073 report existed
- Evidence: `%LOCALAPPDATA%\Temp\cnx073-preflight-114609\` (d01-red-evidence.txt, d02–d08 gate logs)

## Corrected state table

| State | Manifest | Marker | New inventory | recovery_preflight() | CLI exit |
|---|---|---|---|---|---|
| Clean fresh (R1) | no | no | `[]` | **`CLEAN_FRESH`** (new success status) | 0, valid JSON, zero mutation |
| Unmarked partial residue (R2) | no | no | non-empty | RuntimeError (fail-closed) | nonzero; nothing adopted/deleted |
| Valid incomplete marker + residue (R3) | no | incomplete | recorded | `RECOVERED_FRESH` bounded rollback; shared parents/siblings survive → classify `fresh` | 0 |
| Valid incomplete marker, nothing created | no | incomplete | `[]` | `RECOVERED_FRESH` | 0 |
| Coherent ownership (R4) | yes | any | — | `OWNERSHIP_PRESENT`, no rollback authority | 0 |

## T1–T7 RED/GREEN evidence

New suite: `tests/test_recovery_preflight_semantics.py`.

- RED vs pre-fix code (`d01-red-evidence.txt`): **4 failed / 5 passed** —
  T1, T1b (clean fresh raised / CLI nonzero), T6 (clean-fresh could not feed a gate),
  T7 (no allowlist in installer). T2/T3/T4/T5b passed pre-fix because the
  fail-closed and regression behaviors were already correct.
- GREEN after fix: **all 9 passed**.

Per-gate:

- T1/T1b: empty workspace + non-existent exact app-data path → `status == "CLEAN_FRESH"`, CLI exit 0, no marker created, no filesystem mutation.
- T2: one real new-namespace residue path without marker → raises; sentinel files untouched; nothing adopted or deleted.
- T3: production begin/record surfaces with state/skill/app-data residue → `RECOVERED_FRESH`, transaction-created residue removed exactly, shared `<ws>\skills` parent + sibling sentinel preserved, classification returns `fresh`.
- T4: coherent production manifest fixture → `OWNERSHIP_PRESENT`, no rollback/mutation.
- T5: structural ordering — `recovery-preflight --workspace` precedes `classify-install --workspace` precedes `transaction-begin --workspace`; executable extracted-gate harness proves nonzero exit throws with original output visible and unknown success statuses stop before classification/body entry.
- T6: real CLI clean-fresh JSON feeds the gate shape → accepted, `T6_OK CLEAN_FRESH`.
- T7: installer zone contains the explicit allowlist `CLEAN_FRESH`, `RECOVERED_FRESH`, `OWNERSHIP_PRESENT`.

## Installer correction (R5)

`scripts/install.ps1` recovery gate now:

```powershell
$recoveryJson = (& python $ownershipScript recovery-preflight ... 2>&1 | Out-String)
$recoveryExit = $LASTEXITCODE
if ($recoveryExit -ne 0) { throw "Recovery preflight failed (exit $recoveryExit); refusing to proceed to classification: $recoveryJson" }
$recovery = $recoveryJson | ConvertFrom-Json
if ($recovery.status -notin @("CLEAN_FRESH","RECOVERED_FRESH","OWNERSHIP_PRESENT")) {
    throw "Recovery preflight returned unrecognized successful status '$($recovery.status)'; failing closed."
}
```

Ordering unchanged (R6): preflight still before classification and before any fresh transaction begin/mutation.

## Regression gates

| Gate | Result |
|---|---|
| Full pytest (isolated dev venv) | **352 passed, 2 skipped**, 4 subtests passed; 4 failed (see note below) |
| PowerShell syntax parse of install.ps1 | SYNTAX_OK, zero errors |
| npm 12.0.2: `npm ci` / `plugin:validate` / `npm test` | exit 0 each |
| npm 11.16.0: `npm ci` / `plugin:validate` / `npm test` | exit 0 each |
| devDependency `openclaw`: `2026.7.1-2`; plugin version `0.9.3` | exact |
| `check_baseline_consistency.py` | PASS |
| `git diff --check` | clean |
| Clean worktree after implementation commit | yes |

### Note on the 4 pytest failures (pre-existing live-state coupling, not a regression)

`test_r1b/r2/r3_rollback_removes_only_created_paths` (fresh-install-recovery suite) and
`test_p7_production_crash_rerun_recovery` (installer wiring) call
`classify_install()`/`recovery-preflight` WITHOUT `--app-data`, so their inventory includes
the default `%LOCALAPPDATA%\CogentNexus-OpenClaw` root — which now exists on this machine
because the accepted Task-072 live install created it. Verified NOT caused by this change:
running the same tests against a pristine `99a22c6` checkout reproduces the identical
4 failures (4 failed / 11 passed there). The failure mode is environmental coupling of older
fixtures to the now-installed live machine, out of scope for this source-only task and left as
follow-up evidence for review rather than silently "fixed" by touching live state.

All other suites — including the Task 069/070/071 coverage, mode-isolation, and wiring tests — pass in full.

## No-live-mutation accounting

Source/tests only. The healthy Task-072 live installation was not touched:
no install/install-over/uninstall/reset/lifecycle command; no Scheduled Task,
Gateway, Ollama, plugin, config, AGENTS, or SQLite mutation; no process
termination; no reboot; no merge/tag/release; no semantic LLM smoke. All test
fixtures ran under `%TEMP%` pytest directories and isolated worktrees.

## Publication fence

Implementation/tests commit `79b51ed`; this report-only commit adds exactly one file:
`docs/operations/coordination/reports/CNX-20260826-073-correct-clean-fresh-recovery-preflight.md`.
