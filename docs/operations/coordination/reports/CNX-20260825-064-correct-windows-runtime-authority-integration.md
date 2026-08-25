# CNX-20260825-064 — Correct Windows Runtime Authority Integration Report

Result: `PASS_WINDOWS_RUNTIME_AUTHORITY_REWORK_VERIFIED`

Executor: Hermes (manual operator continuation signal)
Fetched execution HEAD: `0b4933227ff92da3ab3ad103dcfe9bacb6e8a5e1` (`coord: move channel to Task 064 runtime-authority rework`; local == remote at fetch; Task 063 review commit `ba4e03ca…` verified ancestor)
Implementation HEAD: `6e4245112a38dab3e6614e6f91d3e37ac85f2afe` (`fix: correct Windows runtime-authority integration (CNX-20260825-064)`)
Publication fence: this final commit adds ONLY this report file relative to implementation HEAD `6e424511…`; independently verified after push via `git ls-remote`.

## RED reproduction of B1–B3

Executable regression tests were written first and run against the Task 063 implementation (`5962383a…`) with an isolated dev venv:

- T1/B2 RED — `runtime_root_from_application_data` did not exist; CLI `--app-data` duplicated the product directory.
- T2/B1 RED — real provisioning crashed on the tuple-as-Path bug (`("pythonw.exe",)`).
- T3/B3 RED — `startup.python_background()` silently returned the executor venv sibling instead of raising.

## Defect corrections

### B1 — invalid Windows background path
`_interpreter_paths()` now constructs both interpreters as plain `Path` objects: `<runtime>\Scripts\python.exe` and `<runtime>\Scripts\pythonw.exe`. Covered by a REAL provisioning test (T2) asserting both files exist under the exact product boundary, plus a foreground stdlib probe and a console-independent sentinel-file probe for `pythonw.exe`.

### B2 — duplicated application-data root
Explicit two-API contract, no ambiguous argument:
- `app_data_root(env)` derives `<LOCALAPPDATA>\CogentNexus-OpenClaw`;
- `runtime_root_from_application_data(exact_root)` appends only `runtime\python`;
- installer CLI uses `--application-data-root <exact-product-root>` (install.ps1 passes `$applicationDataRoot` verbatim).
T1 asserts both forms produce exactly `<root>\runtime\python` and that `CogentNexus-OpenClaw\CogentNexus-OpenClaw` never appears (including in real CLI output). Manifest validation now uses resolved-path ancestry (`Path.resolve()` + `relative_to`), rejecting sibling names such as `CogentNexus-OpenClaw-evil`.

### B3 — startup foreign-venv fallback
Removed entirely. `startup.py::python_background()` is now a fail-closed delegate to `require_background_interpreter(app_data_root())`: missing/corrupt runtime raises `RuntimeProvisioningError`; there is no `sys.executable`/sibling-pythonw path left in the file. T3 proves an executor-venv `sys.executable` can never be selected. Additionally `win_enable` was proven (T4-guarded write test) to fail BEFORE any task XML write when the runtime is absent.

## Executable integration coverage (tests/test_runtime_authority_integration.py)

| Test | Proof |
|---|---|
| T1 (4 cases) | exact product-root contract, env vs explicit forms identical, no duplication incl. live CLI run |
| T2 | REAL temp-boundary provisioning: both interpreters exist, ancestry under exact root, manifest validates, base ≠ executor venv, foreground probe exit 0, background sentinel probe exit 0 |
| T3 | startup raises with patched `executor\venv` executable; owned interpreter selected when provisioned |
| T4 | task-definition preparation fails closed before any `.xml` write without a valid runtime; with runtime, selection == owned pythonw |
| T5 | generated launcher executed a marker script whose observed `sys.executable` equals the owned foreground interpreter byte-for-byte; installer source interpolates `$ownedPython`, never bare `python` |
| T6 | owned interpreter imports the normal `cnxclaw_v093` CLI surface (stdlib-only venv sufficient; no dev deps installed into product runtime) |
| T7 | `host_control`, `cnxclaw`, `runtime` spawn helpers all apply `CREATE_NO_WINDOW` on Windows (Task 063 `FLASH_CHILD_PROCESS` diagnosis preserved unchanged) |
| T8 | runtime root strictly inside uninstall's application-data deletion authority; validate_runtime rejects foreign paths; install-over recreates corrupt/missing manifest deterministically at the same root |

Unit-level checks retained/updated in `tests/test_runtime_ownership.py`.

## Test environment and verification results

Isolated developer test venv at `<evidence-parent>/devtest-venv` (outside clone, outside product root); bootstrap/base interpreter: uv CPython 3.11.15 (`cpython-3.11-windows-x86_64-none`); installed `requirements-dev.txt` (PyYAML 6.x, pytest 9.1.1). Dev dependencies never written into product artifacts.

| Step | Command | Result |
|---|---|---|
| RED (B1–B3) | `pytest tests/test_runtime_authority_integration.py` vs Task 063 code | failed as designed |
| GREEN focused | same after fixes | 14 passed |
| Unit + integration | `pytest tests/test_runtime_ownership.py tests/test_runtime_authority_integration.py` | 21 passed |
| FULL suite (dev venv) | `pytest tests/ -q` | **295 passed, 2 skipped, 0 failed** (previous pytest-import errors eliminated by the isolated dev venv) |
| Canonical validator | `python scripts/check_baseline_consistency.py` | PASS (Bridge v0.9.3) |
| Whitespace fence | `git diff --check` | clean |
| Tree state after impl commit | `git status --porcelain` | clean |

## Live mutation accounting

No live `cnxclaw` lifecycle command; no install/install-over/uninstall/reset; no Scheduled Task change/run/end; no Gateway/Ollama/provider/plugin/config/AGENTS/ownership/SQLite mutation; no process termination; no primary-workspace git mutation. All provisioning tests used temporary roots outside `%LOCALAPPDATA%\CogentNexus-OpenClaw`.

## Commits

1. Implementation/tests: `6e4245112a38dab3e6614e6f91d3e37ac85f2afe`
2. Report-only publication commit: this commit (verified to add only this file).

## Result

`PASS_WINDOWS_RUNTIME_AUTHORITY_REWORK_VERIFIED`
