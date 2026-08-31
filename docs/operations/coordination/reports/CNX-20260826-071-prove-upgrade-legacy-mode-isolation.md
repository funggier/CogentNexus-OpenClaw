# CNX-20260826-071 — Prove Upgrade/Legacy Mode Isolation

Result: `PASS_UPGRADE_LEGACY_MODE_ISOLATION_PROVEN`

Executor: Hermes (after the operator's continuation signal)

## Heads and provenance

- Fetched coordination HEAD at execution start:
  `d903ed1` (`coord: publish Task 071 mode-specific isolation status`);
  remote branch HEAD equals local execution HEAD.
- Worktree clean; Task-070 review commit `3b3cea20d02e66e34704bd3ee8d1ed79f1610b79`
  verified as an ancestor; ACTIVE/STATUS name Task 071; no prior Task-071 report existed.
- Implementation/tests HEAD (test-only commit):
  `7a55980e662b50f2d2979eb77a3ac1f89da7912f`
- Report HEAD: this commit. Production `scripts/install.ps1` required NO
  correction — no new RED demonstrated a defect, so per the task's strict
  method this is a test-only implementation commit.

## U1 — coherent upgrade classification fixture

New suite: `tests/test_upgrade_legacy_mode_isolation_proof.py`.

Fixture builds the REAL production ownership contract on disk in a temp
workspace: exact expected paths (`<ws>\skills\cogentnexus-openclaw` with SKILL.md,
`cnxclaw.cmd`, `<ws>\.cogentnexus-openclaw`), an ownership manifest written by
the actual `build_manifest()`/`write_manifest()`, and an exact v0.9.3 plugin
payload (`openclaw.plugin.json` id/version + `package.json` name/version +
`scripts/bootstrap-ticket-db.mjs` + `dist/ticket-store.js`) under
`<state>/extensions/`.

- `verify_manifest(state, workspace=...)` passes on the real surfaces before any assertion.
- `classify_install(workspace, app_data=...)[\"mode\"] == "upgrade"` — via the
  production classifier only; nothing is hand-assigned.
- No `install-transaction.json` exists before or after classification.

Controlled fixture substitution: plugin verification runs against real files
under the OpenClaw state boundary rather than a live OpenClaw install — the
narrowest substitution that still executes full `classify_install()` +
`verify_manifest()` semantics without duplicating the classifier.

## U2 — upgrade failure isolation

Executable PowerShell harness derives `$isFreshTransaction` from a live
production `classify-install` invocation (never hand-set), enters the shared
body (`BODY_REACHED` printed), then injects `UPGRADE_INJECTED_FAILURE`.
Observed: original failure propagates; `Invoke-FreshTransactionRollback`
stub would abort loudly and is never reached; no rollback/inverse command
runs; no fresh marker appears; sentinel file unchanged.

## L1 — valid legacy classification fixture

Fixture satisfies the actual `prove_legacy_ownership()` contract with three
independent identities: legacy skill metadata, legacy controller structure
(mode `passthrough`), and legacy launcher content referencing `.cogent`.

Observed production result: `mode == "legacy"`,
`legacyMode == "passthrough"`, evidence array length 3
(`legacy-skill-metadata`, `legacy-controller-structure`,
`legacy-launcher-content`). Classification creates no marker.

## L2 — legacy reachability and no fresh marker

Harness again derives `$isFreshTransaction` from the production legacy
classification result. Proven: shared body reached past the Task-069 boundary
opening (`LEGACY_BODY_REACHED`), native-handoff entry point reachable
(`LEGACY_HANDOFF_ENTRY_REACHABLE`), then injected `LEGACY_INJECTED_FAILURE`
propagates through the ordinary non-fresh catch path — no fresh rollback, no
plugin inverse, no `install-transaction.json`. Harness stops before any real
migration mutation. The Task-069 `__UPGRADE_PASSTHROUGH__` sentinel text is
absent from production (structural check `test_l2b` also confirms
transaction-begin remains under the fresh-mode guard).

## F1 — fresh regression

The accepted Task-069 harness
(`test_f1_harness_injected_failure_triggers_production_rollback`) re-ran
green: same-run bounded rollback, exact workspace/app-data residue removed,
original error visible, unrelated sentinel and shared parents survive,
classification returns coherent `fresh`.

## F2 — marker/authority regressions

All focused suites re-run green: transaction begin/record/commit/recovery;
exact app-data created-vs-preexisting; record-time unsafe path rejection;
committed-marker rollback refusal; crash/rerun recovery; shared-parent
preservation; malicious/tampered/unmarked fail-closed; plugin inverse
ordering; AGENTS policy after commit.

## Full verification

| Gate | Result |
|---|---|
| U1/U2/L1/L2/F1/F2 focused | 5 passed (+ F1 within coverage suite) |
| tests/test_installer_mode_isolation.py | passed |
| tests/test_fresh_transaction_failure_coverage.py | passed |
| tests/test_installer_transaction_wiring.py | passed |
| tests/test_fresh_install_transaction_recovery.py | 10 passed |
| Full pytest (isolated dev venv) | **347 passed, 2 skipped** (same 2 pre-existing environment skips), 4 subtests passed |
| PowerShell syntax parse of scripts/install.ps1 (M6) | SYNTAX_OK, zero errors |
| npm 12.0.2 / node v22.23.2: `npm ci`, `plugin:validate`, `npm test` | exit 0 each |
| npm 11.16.0 (npx pin): `npm ci`, `plugin:validate`, `npm test` | exit 0 each |
| Plugin version `0.9.3`; OpenClaw devDependency exactly `2026.7.1-2` | confirmed in package.json |
| `python scripts/check_baseline_consistency.py` | PASS (Bridge v0.9.3) |
| `git diff --check` | clean |
| Clean worktree after tests commit | yes |

No skips beyond the two pre-existing environment skips carried by all prior
accepted runs.

## No-live-mutation accounting

Tests/evidence only; zero production source changes. No install/uninstall/
reset/lifecycle command executed on the live machine; no Scheduled Task,
Gateway, Ollama, plugin, config, AGENTS, or SQLite mutation; no process
termination; no primary-workspace mutation; no reboot; no merge/tag/release.
All fixtures ran under `%TEMP%` pytest dirs and isolated worktrees. The
Task-066 live residue remains intentionally untouched.

## Publication fence

Test-only commit `7a55980`; this report-only commit adds exactly one file:
`docs/operations/coordination/reports/CNX-20260826-071-prove-upgrade-legacy-mode-isolation.md`.
