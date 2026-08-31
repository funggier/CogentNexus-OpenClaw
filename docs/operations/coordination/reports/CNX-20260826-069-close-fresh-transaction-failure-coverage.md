# CNX-20260826-069 — Close Fresh Transaction Failure Coverage

Result: `PASS_FRESH_TRANSACTION_FAILURE_COVERAGE_CLOSED`

Executor: Hermes (after the operator's continuation signal)

## Heads and provenance

- Fetched coordination HEAD at execution start:
  `6163a54a` (`origin/agent/v0.9.3-recovery-reality-tests`, `coord: publish Task 069 fresh transaction failure coverage status`)
- Implementation HEAD:
  `7f48bb803fe3ca46b7a786e50abe8df22da857fc`
- Report HEAD: this commit (report-only publication fence respected)
- Isolated fresh worktree from `origin/agent/v0.9.3-recovery-reality-tests`; task file, ACTIVE.md, and STATUS.md re-read from remote truth before editing.

## Exact production fresh failure boundary (B1)

`scripts/install.ps1` now opens ONE `try {` block immediately after
successful `transaction-begin` (guarded by `$isFreshTransaction`) and closes
it with a single `catch` that routes EVERY caught failure through
`Invoke-FreshTransactionRollback -WorkspacePath $Workspace -OriginalError $_.Exception.Message`.

- The old standalone rollback call sites at ownership create/verify are gone;
  those failures now plain-throw inside the protected region and reach the same
  single catch.
- The helper retains the original error and rethrows it after bounded
  recovery; if rollback itself fails, both errors are reported in one throw.
- Non-fresh (upgrade/legacy) installs never enter the rollback path — a guard
  inside the try rethrows without touching transaction state.
- New pre-commit steps added in the future automatically fall inside recovery.

## Application-data authority contract (B2)

In `namespace_ownership.py`:

- The marker schema gains exactly one field, `applicationDataPreexisting`
  (bool), proven at begin time; the marker's recorded `applicationData` is
  authoritative for record/rollback/recovery, so isolated custom `--app-data`
  test roots validate against themselves rather than an environment-derived
  path.
- `_validate_application_data_root()` allows only a root named exactly
  `CogentNexus-OpenClaw`; `%LOCALAPPDATA%` (or any custom parent) itself,
  its siblings, and workspace parents/siblings are rejected.
- The exact product root participates in `createdPaths` ONLY when begin proved
  it did not preexist; descendants within it are permitted as containment.
- `transaction-record` rejects unsafe paths AT RECORD TIME with
  `createdPaths` unchanged (F5) instead of failing later during deletion.
- Rollback of a non-`incomplete` marker is refused fail-closed (F6b).

## External-effect handling (B3)

- Managed AGENTS policy application (`policy apply`) moved AFTER
  transaction-commit: a failed pre-commit install can no longer leave a
  managed block.
- Fresh plugin registration carries an exact supported inverse:
  `openclaw plugins uninstall cogentnexus-openclaw --force`, executed by the
  rollback helper only when this attempt set `$script:FreshPluginInstalled`
  (set strictly after this attempt's successful `plugins install npm-pack:…`
  call). No broad config deletion and no arbitrary project-directory removal.
- Ticket DB/state live under owned filesystem roots already covered by the
  marker boundaries; runtime/application-data provisioning is covered by the
  exact app-data root boundary.

## F1–F8 results

New suite: `tests/test_fresh_transaction_failure_coverage.py`.

| Gate | Test(s) | RED vs Task-068 code | GREEN |
|---|---|---|---|
| F1 | structural boundary + executable PowerShell harness injecting exit-3 after state/skill creation through the actual extracted production helper | failed (no boundary / no auto-rollback) | PASS — rollback invoked in same caught execution, exact residue removed, original error propagated, unrelated `USER-SENTINEL.md` + shared `<ws>\skills` survive, `classify-install` → `fresh` |
| F2 | harness with shimmed supported `openclaw` command; plugin registered then failure | failed | PASS — exact supported inverse `plugins uninstall cogentnexus-openclaw --force` observed on the shim log; with `$FreshPluginInstalled=$false` no uninstall is issued |
| F3 | `test_f3_exact_app_data_root_recorded_then_removed` | failed (marker boundary rejection) | PASS — exact root removed, sibling sentinel + app-data parent + shared parents survive, classification fresh |
| F4 | `test_f4_preexisting_app_data_survives_caught_failure` | failed | PASS — preexisting root not recorded; sentinel intact after caught-failure rollback |
| F5 | parametrized record-time rejection (workspace parent, sibling skill, arbitrary temp, app-data sibling, app-data parent) | failed | PASS — immediate rejection, `createdPaths` unchanged; exact root remains recordable (F5b) |
| F6 | `test_f6*` | failed/partial | PASS — commit requires verified ownership (stays `incomplete` otherwise); committed-marker rollback refused; structural proof commit sits between verify gate and single catch |
| F7 | `test_f7_crash_rerun_recovery_covers_app_data` | failed | PASS — production `recovery-preflight` recovers workspace AND app-data artifacts, siblings survive, `classify-install` → `fresh` |
| F8 | structural post-commit zone check | n/a | PASS — no external-effect operations between commit and boundary exit |

RED evidence captured before implementation: 17 failed / 1 passed
(`%LOCALAPPDATA%\Temp\cnx069-fresh-coverage-<token>\a01-red-evidence.txt`).

## Full verification (all run fresh in the isolated worktree)

1. F1–F8 focused RED/GREEN: above.
2. Task 067/068 suites: `tests/test_fresh_install_transaction_recovery.py`
   10 passed; `tests/test_installer_transaction_wiring.py` 7 passed
   (P3/P7 preserved; P4 anchor tightened to invocation text only).
3. Full pytest (`requirements-dev.txt` venv): **337 passed, 2 skipped**
   (2 pre-existing environment skips, unchanged from prior accepted runs),
   4 subtests passed, 61.36s.
4. npm gates under node v22.23.2 / PATH pinned to `C:\Program Files\nodejs`:
   - npm 12.0.2: clean `npm ci` exit 0; `npm run plugin:validate` exit 0
     (exact plugin `openclaw-plugin-cogentnexus-openclaw@0.9.3`, OpenClaw devDependency `2026.7.1-2`).
   - npm 11.16.0 (npx pin): clean `npm ci` exit 0; `npm run plugin:validate` exit 0.
   - Shared `<workspace>\skills` parent preservation and malicious/tampered/
     unmarked marker tests all green inside the pytest run above.
5. Canonical plugin build/validate/pack exercised via both toolchains' `plugin:validate`
   (176 packed files each).
6. `python scripts/check_baseline_consistency.py`: **PASS** (Bridge v0.9.3).
7. `git diff --check`: clean.
8. Worktree clean after implementation commit (`git status --porcelain` empty
   before report-only commit).

## No-live-mutation accounting

Source/tests only. No install/uninstall/reset/lifecycle command executed on
the live machine; no Scheduled Task, Gateway, Ollama, plugin, config, AGENTS,
or SQLite mutation; no process termination; no primary-workspace mutation;
no reboot; no merge/tag/release. All fixtures ran under
`%TEMP%\pytest-of-*` and the isolated worktree at
`%LOCALAPPDATA%\Temp\cnx069-fresh-coverage-*\wt`. The Task-066 live residue
remains intentionally untouched.

## Successor note

Per the pre-authorized successor clause, if ChatGPT independently accepts
this result, Task 070 may perform the one-time bounded cleanup of the exact
Task-066 residue, fresh-install the accepted source, prove owned runtime /
no-Hermes binding, observe ≥3 natural PT1M no-flash ticks, and complete final
MANAGED health acceptance without another confirmation.
