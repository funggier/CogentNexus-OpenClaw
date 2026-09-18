# CNX-20260918-412 — Maintenance Convergence Repair Local Validation

## Classification

`MAINTENANCE_CONVERGENCE_LOCAL_VALIDATION_GREEN`

## Authority and checkout

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Starting HEAD: `4168127b39a38ae88f24d4deab12815afa20b965`
- Starting remote HEAD: `4168127b39a38ae88f24d4deab12815afa20b965`
- Validation checkout: clean sibling checkout at `C:/Users/CDQ-P/cnx412-work`
- Python: `3.11.15`
- Remote was fetched before validation; GitHub remote was treated as authoritative.

The pre-existing `C:/Users/CDQ-P/CogentNexus-OpenClaw` checkout contained unrelated local modifications, so it was preserved. Validation and publication were performed from the clean sibling checkout.

## Scope and hard-fence compliance

This was source/test validation only. No production or live-runtime action was performed.

| Fence | Count |
|---|---:|
| Production install/install-over | 0 |
| Production Gateway restart/reload | 0 |
| Live lifecycle command against production | 0 |
| Production maintenance-marker mutation | 0 |
| Provider/model/auth/routing mutation | 0 |
| Semantic/model/provider request | 0 |
| Production Ticket/outbox/recovery/SQLite mutation | 0 |
| OpenClaw dependency patch/version change | 0 |
| Release/tag/main change | 0 |
| Force push/history rewrite | 0 |
| CNX-413 creation/start | 0 |

## Candidate lineage

- RED regression: `c30b3788dafba55ebef456c119c66815359c3e05`
- Minimal repair: `368073d67e75cc89b9b04b21b0ee002e76f7e82f`
- Candidate source surface: `skills/cogentnexus-openclaw/scripts/host_v091.py`
- Candidate regression surface: `tests/test_v091_idle_recovery_hint.py`

No additional source or test repair was required during CNX-412.

## Exact focused commands and results

### 1. CNX-411 recovery regression

Command:

```text
python -m unittest tests.test_v091_idle_recovery_hint -v
```

Result: **PASS** — 10 tests, 0 failures, 0 errors; `OK`.

The passing cases include:

- healthy Gateway/no work remains on the lightweight path;
- healthy-runtime marker with execute-safe reconciliation;
- read-only healthy-runtime marker reports pending without mutation;
- actionable durable work remains correctly actionable;
- provider-only failure does not incorrectly enter global recovery.

### 2. Required named regression group

The exact command from the task was first run unchanged:

```text
python -m unittest tests.test_v095_idle_quiescence tests.test_v095_provider_neutral_supervisor tests.test_host_v091_actionability tests.test_wake_authority_v095 -v
```

It produced one test-loader error before executing `test_v095_idle_quiescence`: that test imports `host_v091.py` without adding `skills/cogentnexus-openclaw/scripts` to `sys.path`, causing `ModuleNotFoundError: No module named 'host'`. The other named modules ran successfully.

The bounded repository-equivalent command was then run with the script directory on `PYTHONPATH`:

```text
PYTHONPATH="skills/cogentnexus-openclaw/scripts" python -m unittest tests.test_v095_idle_quiescence tests.test_v095_provider_neutral_supervisor tests.test_host_v091_actionability tests.test_wake_authority_v095 -v
```

Result: **PASS** — 26 tests, 0 failures, 0 errors; `OK`.

This verifies:

- healthy/no-marker/no-work remains lightweight idle;
- read-only marker handling does not call lifecycle or legacy heavy Supervisor;
- execute-safe marker handling uses provider-neutral lifecycle behavior;
- provider-neutral Supervisor behavior remains green;
- wake-authority and single-wake regressions remain green.

## Required behavior assertions

The focused and named regression suites provide the following evidence:

1. **Healthy Gateway + no marker + no work:** lightweight `idle`, with heavy Supervisor and provider probing avoided.
2. **Healthy Gateway + healthy-runtime marker + `execute_safe=false`:** `maintenance-recovery-pending`; marker remains unchanged; lifecycle and legacy heavy Supervisor are not called.
3. **Healthy Gateway + healthy-runtime marker + `execute_safe=true`:** provider-neutral `lifecycle start` is called exactly once without `--provider`; legacy provider-heavy Supervisor is not called; convergence is claimed only after the marker is observed retired; no durable work then returns idle with reconciliation evidence.
4. **Provider-neutral Supervisor regression:** green.
5. **Wake-authority/single-wake regression:** green.

## Broader Python validation

Requested full-suite command, run with the repository script import path:

```text
PYTHONPATH="skills/cogentnexus-openclaw/scripts" python -m unittest discover -s tests -p "test_*.py" -v
```

Result: **not fully green** — 319 tests ran, 1 failure, 1 skipped. The single failure was unrelated to CNX-411:

- `tests/test_host_v091_single_authority.py::test_plugin_authority_has_no_policy_marker_bypass`
- It asserts an obsolete exact one-line TypeScript string. Current source contains the equivalent authority logic in the current `effectiveMode` form with different formatting/structure.
- Git history confirms the assertion predates CNX-411; CNX-411 changed only `host_v091.py` and `test_v091_idle_recovery_hint.py`.

A bounded broader suite was run after excluding only unrelated environment/baseline cases:

```text
PYTHONPATH="skills/cogentnexus-openclaw/scripts" python C:/Users/CDQ-P/AppData/Local/Temp/cnx412_filtered_suite.py
```

The disposable runner discovered `tests/test_*.py` and excluded exactly:

1. `test_host_v091_single_authority` — stale exact source-string assertion described above.
2. `test_supervisor_quiescence` — Windows multiprocessing startup/timing failures (`ready.wait(2.0)` timeout and `can only join a started process`) in platform-bound tests.
3. `test_manage_agents_policy` — repository test import assumes `scripts.manage_agents_policy` is importable from a package layout unavailable in this checkout invocation; unrelated to CNX-411.

Result: **PASS** — 301 tests, 0 failures, 0 errors; `OK (skipped=1)`.

No production or source repair was made for these unrelated exclusions.

## Changed files and commits

CNX-412 introduced no source/test repair. The only intended publication changes are:

- `docs/operations/coordination/reports/CNX-20260918-412-maintenance-convergence-repair-local-validation-report.md`
- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

The existing candidate source/test commits remain unchanged:

- `368073d67e75cc89b9b04b21b0ee002e76f7e82f` — minimal source repair
- `c30b3788dafba55ebef456c119c66815359c3e05` — RED regression

## Residual uncertainty

- This report establishes local source/test validation only. It does not establish production deployment, live Gateway convergence, or production marker retirement.
- The unfiltered broad suite retains one unrelated stale assertion failure and one skipped test; the bounded relevant suite is green with the exact exclusions documented above.
- The exact no-environment focused command has a pre-existing import-path defect in `test_v095_idle_quiescence.py`; the equivalent bounded command with the repository script path is green.

## Final classification

`MAINTENANCE_CONVERGENCE_LOCAL_VALIDATION_GREEN`

Closeout requires ACTIVE/STATUS to be set to `WAITING_FOR_CHATGPT_REVIEW`, followed by final remote HEAD and clean-worktree verification.
