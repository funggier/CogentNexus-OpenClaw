# CNX-20260825-064 — Correct Windows Runtime Authority Integration

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_REWORK_TDD_WINDOWS_INTEGRATION`

Current authorization: `RUNTIME_AUTHORITY_REWORK_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes after the operator's manual continuation signal

## Goal

Correct the blocking Windows integration defects found during independent review of Task 063 before any live uninstall/reinstall.

The corrected implementation must prove, by executable Windows/temp-boundary tests rather than source-string inspection, that CogentNexus can provision and use its owned runtime at exactly:

`%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python`

and that persistent startup registration can never fall back to Hermes/Codex/another executor venv.

This is source/tests only. The current live installation and Scheduled Task remain untouched.

## Accepted predecessor evidence

Task 063 implementation/report commit:

`5962383ac8e16b1336e0af78f659e2f5fa29dd97`

Task 063 review decision:

`REWORK`

Task 063 review disposition:

`REWORK_WINDOWS_RUNTIME_AUTHORITY_INTEGRATION_DEFECTS`

Task 063 review commit:

`ba4e03ca7d5719075daba23a9dad3a2f89a76bc7`

The Task 063 Phase A diagnosis remains accepted:

`FLASH_CHILD_PROCESS`

The live Hermes/uv venv `pythonw.exe` chain is correlated with console-subsystem child/base-Python transitions and `conhost.exe` on natural PT1M supervisor ticks. Do not repeat the live trace in Task 064 unless static/executable source correction unexpectedly contradicts that diagnosis.

## Blocking defects to correct

### B1 — invalid Windows background path

Task 063 currently contains:

```python
background = scripts / ("pythonw.exe",) if os.name == "nt" else (scripts / "python3",)
```

The Windows operand is a tuple. Correct this and cover it with a real Windows path/provisioning test.

### B2 — duplicated application-data root

`install.ps1` passes exact product root `%LOCALAPPDATA%\CogentNexus-OpenClaw` to an option named `--app-data`, while the CLI treats it as `LOCALAPPDATA` and appends `CogentNexus-OpenClaw` again.

Define one explicit contract and use it consistently. Preferred contract:

- environment-derived API: `app_data_root(env)` accepts `LOCALAPPDATA` base and derives the product root;
- installer CLI: use an explicit `--application-data-root <exact-product-root>` argument when the installer already has `$applicationDataRoot`.

If an equivalent clearer contract is implemented, tests must prove no duplicated product directory appears.

### B3 — startup foreign-venv fallback

`startup.py::python_background()` catches runtime-authority failures and silently falls back to registration-time `sys.executable`/sibling `pythonw.exe`.

Remove this persistent fallback. `win_enable()` / Windows startup registration must require a validated product-owned background interpreter or fail closed.

Transient bootstrap Python is allowed only to provision/repair the owned runtime inside the installer boundary before any durable launcher/task definition is written. It is not an allowed startup-registration authority.

### B4 — inadequate tests / incomplete canonical environment

Task 063 tests 02/03 inspect strings rather than executing the real contracts. They therefore passed despite B1-B3.

Task 064 must create executable integration coverage and run the complete repository test environment with `requirements-dev.txt` installed in an isolated test venv/worktree environment. Do not install test dependencies into the user's global Python or the live CogentNexus runtime.

## Required repository source

Use a fresh isolated full clone/worktree of:

`funggier/CogentNexus-OpenClaw`

branch:

`agent/v0.9.3-recovery-reality-tests`

Before editing require:

- local HEAD equals current remote branch HEAD;
- Task 063 review commit `ba4e03ca7d5719075daba23a9dad3a2f89a76bc7` is an ancestor;
- clone/worktree is clean;
- `ACTIVE.md`, `STATUS.md`, and this task agree on `READY_FOR_HERMES` / `RUNTIME_AUTHORITY_REWORK_AUTHORIZED`;
- no Task 064 report already exists.

Never edit the primary OpenClaw workspace repository.

## Method — strict TDD

For each B1-B3 defect:

1. write the executable regression test first;
2. run it against current Task 063 implementation and record the expected RED failure;
3. make the smallest production correction;
4. run focused GREEN;
5. proceed to the next defect.

Do not weaken assertions to make current code pass.

## Required production design

### 1. Runtime path API

Keep one canonical product-owned runtime root:

`<exact applicationDataRoot>\runtime\python`

Provide APIs whose names make the distinction explicit, for example:

```python
application_data_root_from_env(env) -> Path
runtime_root_from_application_data(application_data_root: Path) -> Path
ensure_runtime(application_data_root: Path | None = None, bootstrap: Path | None = None, ...) -> dict
```

Exact names may differ, but no function/CLI argument may ambiguously mean both `LOCALAPPDATA` base and already-appended product root.

Manifest validation must use path ancestry semantics (`Path.resolve()` / parent relationship where safe), not a raw string-prefix test that could accept sibling names such as `CogentNexus-OpenClaw-evil`.

### 2. Windows interpreter paths

The provisioned runtime must resolve:

- foreground: `<runtime>\Scripts\python.exe`
- background: `<runtime>\Scripts\pythonw.exe`

Both must be `Path` objects and exist after provisioning.

Foreground verification may capture/parse stdout.

Background `pythonw.exe` verification must not assume console stdio exists. Use an exit-only standard-library probe or a temporary sentinel-file probe whose cleanup is bounded to the test/provisioning directory.

### 3. Base-interpreter provenance

When bootstrap runs in an executor venv, resolve a verified non-venv base interpreter from runtime metadata. Do not persist the executor venv as `baseInterpreter`.

Test with the actual current Windows Python/venv mechanism where possible in a temp test venv, in addition to unit fixtures.

### 4. Product runtime capability

The owned runtime is deliberately a product-owned local venv and may depend on the machine's base Python installation. Do not claim it is self-contained.

After provisioning, prove the actual scripts needed for normal `cnxclaw` runtime can start under the owned foreground interpreter using a non-mutating command such as `--help` / parser import / bounded equivalent.

Audit production imports. Do not install dev-only dependencies into the product runtime. If a third-party dependency is truly required during normal runtime, define and provision an explicit runtime dependency set; otherwise keep the owned runtime stdlib-only and prove that the normal CLI/control import path works.

### 5. Installer authority transition

`scripts/install.ps1` may use an ambient/bootstrap Python only until the owned runtime is successfully provisioned.

After provisioning, all CogentNexus Python operations that are part of the installed product transition and can safely run under the owned runtime should use `$ownedPython`, especially launcher generation and MANAGED enable/status paths. If a pre-provisioning operation must remain on bootstrap Python, document why it occurs before durable authority and ensure it cannot be persisted into launcher/task definitions.

At minimum, no durable artifact may contain bootstrap/agent Python.

### 6. Startup fail-closed contract

On Windows, `python_background()` or its replacement must return only the validated product-owned background interpreter.

If manifest/runtime is missing/corrupt:

- `win_enable()` fails before task XML replacement/creation;
- no `sys.executable` fallback occurs;
- no foreign-venv task action can be registered.

Keep `startup_v092.py` targeting `host_control_v092.py`.

Cross-platform behavior may keep its existing explicitly documented contract if changing it would expand untested scope; do not make Windows safety depend on the cross-platform fallback.

## Mandatory executable tests

Update/replace `tests/test_runtime_ownership.py` and add focused helpers/tests as needed.

### T1 — exact product-root contract

Using a temporary local app-data base such as:

`<temp>\Local`

prove derived product root is exactly:

`<temp>\Local\CogentNexus-OpenClaw`

and the exact-product-root CLI/API form produces runtime root exactly:

`<temp>\Local\CogentNexus-OpenClaw\runtime\python`

Assert `CogentNexus-OpenClaw\CogentNexus-OpenClaw` never appears.

RED must fail against Task 063 B2.

### T2 — real Windows temp provisioning

On Windows, provision an actual owned runtime under a temporary exact application-data root using a verified base Python.

Assert:

- foreground/background are real files;
- both are under the exact product boundary;
- manifest validates;
- manifest base interpreter is not the temporary executor/test venv when test is launched from one;
- foreground stdlib probe exits 0;
- background exit-only/sentinel probe exits 0;
- cleanup removes only the temp test root.

RED must expose B1 on Task 063.

### T3 — startup fail closed

With missing/corrupt manifest, call the pure interpreter-selection/task-definition preparation surface and assert a `RuntimeProvisioningError` (or explicit equivalent) occurs.

Patch `sys.executable` to a path containing `executor\venv`; assert it never becomes `{{PYTHON}}`.

RED must expose B3.

### T4 — task definition uses exact owned pythonw

With a valid temp runtime/manifest, generate the Windows task definition in memory or a temp file without creating a Scheduled Task.

Assert exact `<Command>` points to owned `pythonw.exe`, arguments point to `host_control_v092.py` through the v0.9.2 adapter path, and no executor/venv path occurs.

### T5 — generated launcher executable contract

Refactor launcher rendering into a testable surface if needed. Generate a temp launcher or exact command line and assert it invokes the owned `python.exe`, not bare `python`.

Where safe on Windows, execute a generated temp launcher against a harmless test script and assert the interpreter observed by the script equals the owned runtime interpreter.

### T6 — normal CLI import/start capability

Using the owned foreground interpreter, run a non-mutating normal product entry/import surface and assert exit 0. This prevents a stdlib-only product venv that cannot actually run CogentNexus.

### T7 — no-console semantics preserved

Keep/strengthen tests showing every Windows subprocess helper on the accepted healthy supervisor path applies `CREATE_NO_WINDOW` or equivalent. Preserve the Task 063 `FLASH_CHILD_PROCESS` diagnosis; do not claim live flash elimination until the later live reinstall task verifies natural ticks.

### T8 — uninstall/reset/install-over boundary

Run source/integration tests proving the new runtime remains inside existing CogentNexus application-data deletion authority, uninstall cannot target foreign Python, reset semantics are explicit, and install-over can validate/recreate a missing/corrupt owned runtime without changing deletion authority.

## Test environment and verification

Create an isolated developer test venv in the isolated clone/temp boundary and install:

`requirements-dev.txt`

Record exact bootstrap/base interpreter used for tests. This developer test venv is not a product runtime and must never be written into product artifacts.

Required fresh verification:

1. each RED test before production correction;
2. focused GREEN tests;
3. existing startup/host-control/install/ownership tests;
4. full `python -m unittest discover -s tests` with all required imports available;
5. repository pytest suite if repository/canonical CI invokes pytest;
6. `scripts/check_baseline_consistency.py` and other canonical validators applicable to changed files;
7. `git diff --check`;
8. clean isolated working tree after implementation commit.

Record exact pass/skip/fail/error counts. Any failure must be resolved or classified before PASS.

## Publication discipline

Use at least two commits:

1. implementation/tests commit(s);
2. final report-only commit.

The final report commit must add only:

`docs/operations/coordination/reports/CNX-20260825-064-correct-windows-runtime-authority-integration.md`

relative to the reviewed implementation HEAD.

Report must state both the fetched execution HEAD and the implementation HEAD, then independently verify the report-only publication fence.

## Live hard fence

No live `cnxclaw` lifecycle command; no install/install-over/uninstall/reset; no Scheduled Task create/update/delete/run/end; no Gateway/Ollama/provider/plugin/config/AGENTS/ownership/SQLite mutation; no process termination; no primary-workspace Git mutation; no HermesAgent project mutation; no merge/tag/release.

All runtime provisioning tests must use temporary directories outside the live `%LOCALAPPDATA%\CogentNexus-OpenClaw` product root.

## Result tokens

Use exactly one:

- `PASS_WINDOWS_RUNTIME_AUTHORITY_REWORK_VERIFIED`
- `BLOCKED_RUNTIME_AUTHORITY_INTEGRATION`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

A PASS is source-only evidence and does not repair the current live installation.

## Pre-authorized successor

If ChatGPT independently accepts `PASS_WINDOWS_RUNTIME_AUTHORITY_REWORK_VERIFIED`, the user's previously granted authorization remains in force for the next bounded task to clean-uninstall the current CogentNexus-OpenClaw installation and fresh-install the reviewed corrected build, with preservation evidence and multi-tick no-flash verification. No additional confirmation is required.

Report meaningful progress approximately every 3 minutes and immediately after RED reproduction, real temp-runtime provisioning, startup fail-closed proof, full suite, implementation publication, or blocker.
