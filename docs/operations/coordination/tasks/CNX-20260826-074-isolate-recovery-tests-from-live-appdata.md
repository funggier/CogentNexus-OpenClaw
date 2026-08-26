# CNX-20260826-074 — Isolate Recovery Tests from Live Application Data

Status: `READY_FOR_HERMES`

Execution mode: `TEST_ONLY_TDD_LIVE_APPDATA_ISOLATION`

Current authorization: `RECOVERY_TEST_ISOLATION_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes after the operator's continuation signal

## Goal

Close the only remaining Task-073 acceptance blocker by making the recovery/transaction regression suite deterministic on a machine where the valid Task-072 live installation has created `%LOCALAPPDATA%\CogentNexus-OpenClaw`.

This is test/evidence only unless a newly demonstrated production defect requires stopping and reporting. Preserve Task-073 production correction at implementation HEAD `79b51ed06363f6e8862c491ee0a313ddb412c806`.

## Accepted predecessor behavior

Preserve:

- clean markerless fresh preflight returns `CLEAN_FRESH`;
- markerless partial residue remains fail-closed;
- valid incomplete marker recovery returns `RECOVERED_FRESH`;
- coherent ownership returns `OWNERSHIP_PRESENT`;
- installer stops on nonzero recovery-preflight before classification;
- unknown successful recovery status fail-closes;
- recovery/classification/transaction ordering remains correct;
- npm 11/npm 12 reproducibility, exact OpenClaw `2026.7.1-2`, plugin `0.9.3`;
- upgrade/legacy isolation and fresh rollback semantics;
- Task-072 live runtime/no-flash state.

## Blocking defect

Older temp-workspace tests call `begin_fresh_transaction()`, `classify_install()`, `current_inventory()`, `recovery_preflight()` or `rollback_transaction()` without consistently providing a temp application-data product root. Production then legitimately resolves its default application-data boundary to the real user `%LOCALAPPDATA%\CogentNexus-OpenClaw`, which currently exists because Task 072 installed the product.

The Task-073 report observed four full-suite failures from this coupling, including fresh-install recovery tests and the production crash/rerun wiring test.

Tests must not depend on whether CogentNexus happens to be installed on the executor machine.

## Required correction

### I1 — reproduce the coupling

Before editing tests, run the four reported failing cases (or exact current equivalents) against the current branch/live-installed environment and capture RED evidence showing that the failure is caused by default application-data inventory observing the real live product root.

Do not delete, rename, hide, or mutate the live application-data root to obtain RED/GREEN.

### I2 — isolated application-data fixture

For every affected temp-workspace test, create an exact isolated application-data root shaped like:

`<tmp>/appdata-local/CogentNexus-OpenClaw`

and pass it consistently to all production surfaces whose application-data inventory/transaction semantics participate in that test.

Where a production function supports `app_data=...`, use that argument. Where a helper in the test currently hides such calls, update the test helper so its caller-supplied isolated root flows through consistently.

Do not monkeypatch production global behavior merely to force an empty inventory if the production API already provides an `app_data` boundary.

### I3 — preserve semantic assertions

The corrected tests must still prove their original behaviors:

- marker exists before residue-capable mutation;
- incomplete transaction recovers to coherent fresh;
- caught rollback removes only transaction-created paths;
- unrelated workspace/shared parents survive;
- production crash/rerun recovery works;
- unmarked/tampered residue remains fail-closed.

Do not weaken `current_inventory()["new"] == []`, fresh classification, rollback or preservation assertions merely to make tests pass.

### I4 — live-state independence proof

Prove the focused corrected tests pass while the real Task-072 `%LOCALAPPDATA%\CogentNexus-OpenClaw` remains present and untouched.

Record that live product root exists before and after the focused tests and that its tree/config/task/runtime were not mutated by the tests.

### I5 — Task-073 focused regressions

Re-run `tests/test_recovery_preflight_semantics.py` and prove all T1-T7 remain green.

### I6 — full suite gate

Run full `pytest tests/ -q` in the isolated dev environment. Acceptance requires **zero failed tests**. Explain only skips that are established environment skips.

A report with any failed tests must use `BLOCKED_TEST_OR_VALIDATION_FAILURE`.

### I7 — non-Python regression gates

Re-run:

- PowerShell syntax parse of `scripts/install.ps1`;
- npm 11.16.0 clean `npm ci` + `plugin:validate` + `npm test`;
- npm 12.0.2 clean `npm ci` + `plugin:validate` + `npm test`;
- exact OpenClaw devDependency `2026.7.1-2` and plugin `0.9.3`;
- `python scripts/check_baseline_consistency.py`;
- `git diff --check`;
- clean worktree after tests commit.

## Change fence

Prefer test-only changes. Expected files are limited to affected tests/helpers, likely:

- `tests/test_fresh_install_transaction_recovery.py`
- `tests/test_installer_transaction_wiring.py`

If another test file has the same proven live-appdata coupling, it may be corrected narrowly and must be listed in the report.

Do not alter production source merely to accommodate a test fixture. If a new production defect is demonstrated, STOP and report instead of bundling it into this task.

## Live hard fence

The current Task-072 MANAGED installation must remain untouched.

No live install/install-over/uninstall/reset/lifecycle command; no Scheduled Task/Gateway/Ollama/plugin/config/AGENTS/SQLite mutation; no process termination; no reboot; no HermesAgent mutation; no semantic LLM smoke; no merge/tag/release.

## Publication discipline

Use separate commits:

1. test-only correction commit(s);
2. report-only commit adding exactly:

`docs/operations/coordination/reports/CNX-20260826-074-isolate-recovery-tests-from-live-appdata.md`

Report must include execution HEAD, test-only implementation HEAD, RED/GREEN evidence, exact isolated app-data fixture strategy, affected tests/files, live-state independence proof, full pytest result, npm gates, no-live-mutation accounting and publication fence.

## Result tokens

Use exactly one:

- `PASS_RECOVERY_TESTS_ISOLATED_FROM_LIVE_APPDATA`
- `BLOCKED_TEST_FIXTURE_ISOLATION`
- `BLOCKED_NEW_PRODUCTION_DEFECT`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Pre-authorized successor

If Task 074 is independently accepted, Task 075 may perform one supported install-over from the exact accepted Task-073 production correction onto the current Task-072 MANAGED installation, with no clean uninstall/manual cleanup. Task 075 must prove source/live parity, ownership/plugin generation correctness, owned runtime binding, MANAGED health and at least three natural PT1M no-flash ticks.

Only after Task 075 acceptance may Task 076 perform the final semantic flow:

`user message -> durable Ticket -> Ollama LLM -> durable result/delivery -> user-visible response`.
