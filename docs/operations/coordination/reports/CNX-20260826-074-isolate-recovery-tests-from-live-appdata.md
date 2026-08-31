# CNX-20260826-074 — Isolate Recovery Tests from Live Application Data

Result: `PASS_RECOVERY_TESTS_ISOLATED_FROM_LIVE_APPDATA`

Executor: Hermes (after the operator's continuation signal)

## Heads

- Fetched coordination HEAD at execution start: `7172c2c` (`coord: publish Task 074 recovery test isolation status`)
- Test-only implementation HEAD: `8fc2f4640a761204e9614d2a2fbcfb55cc23d311`
- Task-073 production correction preserved untouched at `79b51ed06363f6e8862c491ee0a313ddb412c806` (no production source changed in this task)
- Report HEAD: this commit (report-only publication fence)
- Evidence: `%LOCALAPPDATA%\Temp\cnx074-isolation-121016\`
  (e01-live-before.txt, e02-red-evidence.txt, e03-pytest-full.txt,
  e04-live-after.txt, e05-baseline.txt, e06-syntax.txt, e07–e10 npm gates)

## I1 — coupling reproduced (RED evidence)

With the live `%LOCALAPPDATA%\CogentNexus-OpenClaw` present (Task-072 install),
the pristine branch failed exactly the four reported cases
(`e02-red-evidence.txt`: **4 failed / 11 passed**):

- `test_fresh_install_transaction_recovery.py::test_r1b_marker_written_before_artifact_creation`
- `test_fresh_install_transaction_recovery.py::test_r2_incomplete_transaction_recovery_restores_fresh`
- `test_fresh_install_transaction_recovery.py::test_r3_rollback_removes_only_created_paths`
- `test_installer_transaction_wiring.py::test_p7_production_crash_rerun_recovery`

Failure mode confirmed as default-application-data inventory observing the real
live product root (e.g. `classify_install()` raised on the live ownership-manifest
absence because inventory was non-empty via the default boundary). The live root
was NOT deleted, renamed, hidden, or mutated to obtain RED/GREEN.

## I2/I3 — isolated fixture strategy and preserved assertions

Test-only change in the two affected files:

- `_isolated_app_root(tmp_path)` builds the exact isolated root
  `<tmp>/appdata-local/CogentNexus-OpenClaw`;
- `_make_residue()` gained an `app_data` passthrough so the caller's isolated
  root flows through `record_transaction_path(...)` consistently;
- `test_r1b/r2/r3` pass `app_data=` into `begin_fresh_transaction`,
  `classify_install`, `current_inventory`, `recovery_preflight`, and
  `rollback_transaction`;
- the P7 PowerShell harness passes `--app-data` on every CLI invocation
  (`transaction-begin`, `transaction-record` ×3, `recovery-preflight`,
  `classify-install`).

No production API monkeypatching. No assertion weakened — all original
semantic checks remain: marker before mutation; recovery → coherent fresh;
rollback removes only transaction-created paths; unrelated sentinel + shared
`<ws>\skills` parent survive; P7 crash/rerun recovery works.

Affected files (within the task fence): `tests/test_fresh_install_transaction_recovery.py`,
`tests/test_installer_transaction_wiring.py`. No other file showed this coupling.

## I4 — live-state independence proof

Focused corrected suites: **15 passed** while the live product root remained present.
Full-file SHA-256 inventories of `%LOCALAPPDATA%\CogentNexus-OpenClaw` taken before
(`e01-live-before.txt`) and after (`e04-live-after.txt`) the focused AND full test runs:
identical (`LIVE-ROOT-UNCHANGED`). No config/task/runtime mutation by the tests.

## I5 — Task-073 focused regressions

`tests/test_recovery_preflight_semantics.py` re-run green inside the full suite
(all T1–T7 pass).

## I6 — full suite gate

Full `pytest tests/ -q` (isolated dev venv): **356 passed, 2 skipped, 0 FAILED**
(59s). The only skips are the two established environment skips carried by every
previously accepted run. Zero failures satisfies the acceptance requirement.

## I7 — non-Python gates

| Gate | Result |
|---|---|
| PowerShell syntax parse of scripts/install.ps1 | SYNTAX_OK, zero errors |
| npm 12.0.2: clean `npm ci` / `plugin:validate` / `npm test` | exit 0 each |
| npm 11.16.0: clean `npm ci` / `plugin:validate` / `npm test` | exit 0 each |
| OpenClaw devDependency `2026.7.1-2`; plugin version `0.9.3` | exact |
| `python scripts/check_baseline_consistency.py` | PASS (Bridge v0.9.3) |
| `git diff --check` | clean |
| Clean worktree after tests commit | yes |

## No-live-mutation accounting

Test/evidence only; zero production changes. The Task-072 MANAGED installation
was not touched: no install/install-over/uninstall/reset/lifecycle command; no
Scheduled Task/Gateway/Ollama/plugin/config/AGENTS/SQLite mutation; no process
termination; no reboot; no semantic LLM smoke; no merge/tag/release. All
fixtures ran under `%TEMP%` pytest directories and isolated worktrees.

## Publication fence

Test-only commit `8fc2f46`; this report-only commit adds exactly one file:
`docs/operations/coordination/reports/CNX-20260826-074-isolate-recovery-tests-from-live-appdata.md`.
