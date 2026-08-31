# CNX-20260826-073 — Correct Clean-Fresh Recovery Preflight Semantics

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_REPAIR_TDD_RECOVERY_PREFLIGHT_SEMANTICS`

Current authorization: `RECOVERY_PREFLIGHT_CORRECTION_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes after the operator's continuation signal

## Goal

Correct the installer recovery-preflight semantics exposed during accepted Task 072: a truly clean markerless fresh state must be a successful preflight outcome, while unmarked partial residue, tampered markers, incomplete rollback, and any other genuine recovery error must remain fail-closed and must stop the installer before classification/mutation.

This task is source/tests only. Do not mutate the now-healthy live CogentNexus installation.

## Accepted predecessor

Task 072 report result:

`PASS_FRESH_INSTALL_OWNED_RUNTIME_NO_FLASH_VERIFIED`

Report HEAD:

`19d3ae6bf090e58aaf9b45da52fe3ae6f4f7d11a`

Independent review:

Decision `ACCEPT`

Disposition:

`ACCEPT_LIVE_INSTALL_OWNED_RUNTIME_NO_FLASH_WITH_PREFLIGHT_FOLLOWUP`

Review commit:

`9811272b8826ade6bf3d12f6091d2fcb8ff044ab`

Accepted production source currently installed live:

`9df671670908241486afe2badf8a7f221410c6f8`

## Root cause already established

Production `namespace_ownership.py::recovery_preflight()` currently computes inventory, then:

```python
if manifest_path(paths["stateRoot"]).exists():
    return {"status": "OWNERSHIP_PRESENT", "inventory": inventory}
if payload is None:
    raise RuntimeError(
        "no valid incomplete install transaction marker; "
        "unowned partial installation residue must not be adopted or deleted"
    )
```

This conflates two different states:

1. clean fresh: no ownership, no marker, `inventory["new"] == []` — should succeed;
2. unmarked partial residue: no ownership, no marker, `inventory["new"] != []` — must fail closed.

Production `scripts/install.ps1` currently invokes `recovery-preflight` but only processes the result when `$LASTEXITCODE -eq 0`; it does not explicitly stop on nonzero recovery-preflight exit. Task 072 therefore installed successfully despite a spurious clean-fresh preflight error.

## Required corrected contract

### R1 — clean markerless fresh is success

For no manifest, no transaction marker, and no new product inventory:

`recovery_preflight()` must return a deterministic success status, preferably:

`CLEAN_FRESH`

with the observed inventory. The CLI command must exit 0 and emit valid JSON.

Do not create a marker or mutate anything during this read/recovery preflight.

### R2 — unmarked partial residue remains fail-closed

For no manifest, no marker, but any new product inventory/residue, `recovery_preflight()` must still fail nonzero and must not adopt/delete/mutate it.

Preserve the exact ownership-safety principle established in Tasks 067-071.

### R3 — valid incomplete transaction recovery remains unchanged

A valid incomplete marker plus recorded residue must still perform bounded recovery and return `RECOVERED_FRESH`; shared parents and unrelated siblings survive.

### R4 — coherent ownership remains unchanged

A valid installed ownership state must continue returning `OWNERSHIP_PRESENT` without rollback authority.

### R5 — installer must fail closed on preflight error

`scripts/install.ps1` must capture recovery-preflight output/exit status and explicitly throw/stop BEFORE `classify-install` if recovery-preflight exits nonzero.

Clean fresh will no longer hit this branch because R1 exits 0.

Do not rely on later `classify-install` as the safety backstop for a failed recovery step.

The installer may accept successful statuses `CLEAN_FRESH`, `RECOVERED_FRESH`, and `OWNERSHIP_PRESENT` as appropriate. Unknown successful status should fail closed rather than silently continue.

### R6 — no mutation ordering regression

The corrected preflight must remain before classification and before any fresh transaction begin/residue-capable mutation. Fresh transaction begin/record/commit behavior from Tasks 067-071 must remain unchanged.

## Strict TDD method

Use a fresh isolated worktree from the current coordination HEAD. Use the project's established isolated dev environment. No production code change before the relevant RED is observed.

### T1 — clean fresh RED/GREEN

Add a focused test against the production `recovery_preflight()` and CLI:

1. create empty temp workspace and exact temp `.../CogentNexus-OpenClaw` app-data path that does not exist;
2. assert no state/skill/launcher/app-data/plugin inventory and no marker;
3. RED against current code: production call raises / CLI exits nonzero;
4. GREEN: returns `status == "CLEAN_FRESH"`, CLI exit 0, no filesystem mutation and no marker created.

### T2 — unmarked residue fail-closed

Create the same clean fixture, then add one actual production new-namespace residue path without a marker. Assert production recovery preflight raises / CLI exits nonzero, sentinel files are untouched, and no path is deleted or adopted.

### T3 — valid incomplete recovery regression

Use production transaction-begin/record surfaces, create bounded state/skill/app-data residue, then call production recovery preflight. Assert `RECOVERED_FRESH`, exact transaction-created residue removed, shared parents/siblings preserved, and classification returns `fresh`.

### T4 — ownership-present regression

Create a coherent ownership fixture using production manifest surfaces. Assert recovery preflight returns `OWNERSHIP_PRESENT` and performs no rollback/mutation.

### T5 — installer fail-closed executable/structural proof

Add an installer-facing test/harness that proves:

- `recovery-preflight` invocation occurs before `classify-install` and `transaction-begin`;
- a deterministic nonzero recovery-preflight result causes the installer recovery gate to throw before classification/body entry;
- the original recovery error/output remains visible;
- no fresh transaction marker/body mutation is reached.

A pure string check alone is insufficient; pair ordering inspection with an executable extracted production gate/helper or narrowly refactor the gate into a testable production helper if necessary.

### T6 — successful clean-fresh installer gate

Exercise the same production gate with a real clean-fresh recovery-preflight result. Assert it accepts `CLEAN_FRESH` and proceeds to the classification boundary without stderr/exception from recovery.

### T7 — unknown success status fail-closed

If the installer decodes a success JSON status outside the allowlist, prove it stops before classification/mutation.

## Regression gates

Preserve and rerun:

- fresh transaction begin/record/commit/recovery tests;
- application-data created-vs-preexisting tests;
- malicious/tampered/unmarked marker protections;
- shared parent preservation;
- plugin inverse and AGENTS post-commit ordering;
- upgrade/legacy mode-isolation tests from Tasks 070-071;
- PowerShell syntax parse;
- npm 11.16.0 and npm 12.0.2 clean `npm ci` + `plugin:validate` + `npm test`;
- exact OpenClaw devDependency `2026.7.1-2`, plugin version `0.9.3`;
- full `pytest tests/ -q`;
- `python scripts/check_baseline_consistency.py`;
- `git diff --check`;
- clean worktree after implementation commit.

## Publication discipline

Use separate commits:

1. implementation/tests commit(s);
2. report-only commit adding only:

`docs/operations/coordination/reports/CNX-20260826-073-correct-clean-fresh-recovery-preflight.md`

Report must include:

- fetched coordination/execution HEAD;
- implementation HEAD;
- exact T1-T7 RED/GREEN evidence;
- corrected state table for CLEAN_FRESH / unmarked partial / incomplete marker / owned install;
- installer nonzero/unknown-status fail-closed evidence;
- full test/npm gates;
- no-live-mutation accounting;
- report-only publication fence.

## Live hard fence

The Task-072 installation is healthy and must remain untouched in this source task.

No live install/install-over/uninstall/reset; no lifecycle command; no Scheduled Task/Gateway/Ollama/plugin/config/AGENTS/SQLite mutation; no process termination; no reboot; no HermesAgent mutation; no merge/tag/release; no semantic LLM smoke.

## Result tokens

Use exactly one:

- `PASS_CLEAN_FRESH_RECOVERY_PREFLIGHT_CORRECTED`
- `BLOCKED_CLEAN_FRESH_SEMANTICS`
- `BLOCKED_INSTALLER_PREFLIGHT_FAIL_CLOSED`
- `BLOCKED_RECOVERY_SAFETY_REGRESSION`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Pre-authorized successor

If Task 073 is independently accepted, Task 074 may perform one supported bounded install-over from the exact accepted correction commit onto the current Task-072 MANAGED installation, with no clean uninstall and no manual cleanup. Task 074 must prove source/live parity, ownership/plugin generation correctness, owned runtime binding, MANAGED health, and at least three natural PT1M no-flash ticks after install-over.

Only after Task 074 acceptance should Task 075 perform the final semantic flow:

`user message -> durable Ticket -> Ollama LLM -> durable result/delivery -> user-visible response`.