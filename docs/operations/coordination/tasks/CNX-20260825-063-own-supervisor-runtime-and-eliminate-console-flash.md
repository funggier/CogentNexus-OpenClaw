# CNX-20260825-063 — Own Supervisor Runtime and Eliminate Console Flash

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_FIX_WITH_READ_ONLY_FLASH_DIAGNOSIS`

Current authorization: `OWNED_RUNTIME_AND_FLASH_FIX_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes after the operator's manual continuation signal

## Goal

Remove the executor-specific Python dependency from CogentNexus-OpenClaw and eliminate the visible recurring Windows console/window flash observed by the operator.

The durable startup/runtime chain must be owned by CogentNexus-OpenClaw itself, not by Hermes, Codex, another agent venv, or whichever Python happens to invoke `cnxclaw enable`.

This task fixes source/tests only after a bounded read-only process-start diagnosis of the flashing symptom. It does **not** uninstall/reinstall or mutate the current live Scheduled Task. After this implementation is reviewed and accepted, the operator has explicitly authorized a separate successor to clean-uninstall the current installation and reinstall the reviewed fixed build from the project release path.

## Accepted predecessor

Task 062 report commit:

`13ee5ddb5d88a9deb657f325026611286b1b2e33`

Task 062 review disposition:

`ACCEPT_DIAGNOSIS_ROOT_CAUSE_BOUND_WITH_MULTI_REBOOT_SCOPE_CORRECTION`

Task 062 review commit:

`28947721cb002304d638536c5c143e919116ad77`

Accepted facts:

- Task 062 F1 was a two-byte AGENTS managed-block removal verification mismatch; no AGENTS repair is required.
- Task 062 F2 was `CONFIG_READ_SURFACE_MISMATCH`; the full managed config is persisted under `plugins.entries.cogentnexus-openclaw`; no config repair is required.
- Current live Windows Scheduled Task executes `C:\Users\CDQ-P\AppData\Local\hermes\hermes-agent\venv\Scripts\pythonw.exe` and passes installed `host_control_v092.py`.
- `startup.py::python_background()` derives the persistent interpreter from registration-time `sys.executable`, so an executor venv can become a long-lived product dependency.
- The operator observed a recurring visible window/console flash while the supervisor task repeats at `PT1M`.
- The operator clarified that the machine passed through multiple reboot boundaries after Task 061. Latest-boot recovery is accepted; per-boot historical behavior is not separately reconstructible.

## Operator intent

The operator explicitly requires a definitive repair:

- CogentNexus must not depend on Hermes or another executor environment for normal runtime/supervision.
- The recurring flash must disappear; it is not accepted as normal background behavior.
- After source review, the current installation should be removed cleanly and installed again using the reviewed fixed release path without requiring another authorization prompt.

## Root-cause boundary already established

Current installer/startup surfaces use ambient Python authority:

- `scripts/install.ps1` requires and invokes bare `python` repeatedly;
- the generated `cnxclaw.cmd` currently invokes bare `python`;
- `startup.py` persists registration-time `sys.executable`/sibling `pythonw.exe` into the Windows Scheduled Task.

This makes execution context leak into durable product ownership.

The fix must establish one explicit CogentNexus-owned Python runtime authority and route the installed launcher + startup adapter through it.

## Required repository source

Use a fresh isolated full clone of:

`funggier/CogentNexus-OpenClaw`

branch:

`agent/v0.9.3-recovery-reality-tests`

Before diagnosis/editing require:

- local HEAD equals remote branch HEAD;
- clone clean;
- Task 062 report commit `13ee5ddb5d88a9deb657f325026611286b1b2e33` ancestor;
- Task 062 review commit `28947721cb002304d638536c5c143e919116ad77` ancestor;
- `ACTIVE.md`, `STATUS.md`, and this task agree on `READY_FOR_HERMES` / `OWNED_RUNTIME_AND_FLASH_FIX_AUTHORIZED`;
- no matching Task 063 report exists.

Never edit/commit from the primary OpenClaw workspace repository.

## Required method

Use systematic debugging + TDD:

1. bind the visible flash to an exact process creation path before changing source;
2. write failing regression tests for runtime ownership and, where testable, Windows no-console process semantics;
3. run RED and record the expected failure;
4. implement the smallest cohesive ownership fix;
5. run focused GREEN tests;
6. run relevant existing startup/installer/host-control tests;
7. run the full Python suite and canonical validations;
8. publish one implementation report and stop.

No production-code edit before the relevant regression test has been observed failing.

## Phase A — read-only flash diagnosis

The live product is currently MANAGED and its existing supervisor task runs once per minute. Task 063 may observe it but must not modify or manually invoke it.

Create one retained evidence directory:

`%LOCALAPPDATA%\Temp\cnx063-owned-runtime-flash-<UTC-token>`

For at least two natural supervisor intervals, capture process-start evidence using a read-only Windows mechanism such as a bounded `Win32_ProcessStartTrace`/CIM/WMI subscription or equivalent transient observer. Do not use Procmon Task 027/038 and do not enable new persistent Windows auditing.

Capture only bounded fields needed for this diagnosis:

- timestamp;
- process name/PID/parent PID;
- parent process name where resolvable;
- bounded command line for processes causally descended from the CogentNexus supervisor tick;
- Scheduled Task LastRunTime/LastTaskResult for correlation.

Do not dump unrelated process command lines.

Determine the narrowest supported flash classification:

- `FLASH_SUPERVISOR_INTERPRETER` — visible window originates at the scheduled interpreter itself;
- `FLASH_CHILD_PROCESS` — interpreter is windowless but a child command opens a visible console/window;
- `FLASH_TASK_WRAPPER` — task/shell wrapper opens the window;
- `FLASH_NOT_BOUND` — trace did not identify the visible process.

If `FLASH_NOT_BOUND`, continue the source ownership fix but do not claim the flash is fixed merely because `pythonw.exe` is used. Add source-level no-console hardening only where evidence/source audit supports it.

## Architecture requirement — CogentNexus-owned runtime

Implement one stable product runtime root on Windows under the product application-data boundary, for example:

`%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python`

The exact internal directory name may differ if existing repository conventions require it, but it must remain under the CogentNexus-OpenClaw application-data ownership boundary and must not live under Hermes, Codex, OpenClaw npm projects, a temp directory, or the user's arbitrary active venv.

### Runtime provisioning semantics

The Windows installer must provision/verify this owned runtime before generating the installed launcher or enabling MANAGED startup.

Required behavior:

1. Resolve bootstrap Python explicitly.
2. If bootstrap execution is inside a venv, identify a valid base interpreter using Python runtime metadata (`sys.base_prefix`, `_base_executable`, or another verified standard mechanism), not by accepting the venv path as durable authority.
3. Create/update a **CogentNexus-owned runtime environment** under the application-data boundary using that verified base interpreter.
4. Prefer a product-owned `pythonw.exe` for Windows background supervisor execution and a product-owned `python.exe` for foreground CLI/runtime execution.
5. Validate that the owned interpreter paths exist and can execute a minimal standard-library probe before committing launcher/task definitions.
6. Persist a small product-owned runtime manifest containing non-secret interpreter provenance/version and exact owned runtime paths so install-over can validate/recreate the runtime deterministically.
7. Fail closed with an actionable error if the owned runtime cannot be provisioned or verified.
8. Do not silently fall back to Hermes/agent/current arbitrary venv for persistent execution.
9. Do not hard-code username, drive letter, Hermes, uv, Python patch version, or machine-specific paths.

A dedicated venv under the CogentNexus application-data boundary is acceptable if it is deliberately provisioned by the product from a verified non-venv base interpreter and the product treats that environment as its runtime dependency. The implementation must document that the system/base Python remains an installation prerequisite if that is the chosen architecture. Do not pretend a venv is fully standalone if it is not.

If repository evidence supports a stronger self-contained mechanism without materially expanding scope, it may be used, but do not introduce a download/build system redesign in this task without necessity.

## Installed launcher ownership

Update Windows `scripts/install.ps1` so generated `cnxclaw.cmd` invokes the exact CogentNexus-owned foreground interpreter, not bare `python`.

The launcher must remain relocatable with respect to username/drive by writing the resolved installed product runtime path at install time; it must not resolve execution from ambient PATH on every invocation.

Install-over must refresh the launcher if the owned-runtime path changes through a supported migration.

## Startup adapter ownership

Update `skills/cogentnexus-openclaw/scripts/startup.py` so Windows Scheduled Task `{{PYTHON}}` comes from the verified CogentNexus-owned runtime authority, never directly from registration-time `sys.executable`.

`startup_v092.py` must continue to bind the runtime script to `host_control_v092.py`.

The Scheduled Task verification must check the expected owned `pythonw.exe`/fallback product-owned interpreter exactly.

Do not accept a foreign venv action as healthy merely because the executable exists.

## Cross-platform behavior

Inspect `install.sh`, systemd generation, and launchd generation for the same ambient-`sys.executable` class.

Do not force the Windows product-runtime design onto other platforms without tests, but avoid leaving an obvious executor-venv persistence bug in the same shared selector. If minimal shared runtime-authority plumbing safely fixes all platforms, do so. Otherwise document Windows as the repaired platform and open a bounded follow-up rather than introducing an untested broad rewrite.

## Eliminate visible periodic console/window flash

The Windows supervisor must be genuinely background/no-console.

Mandatory invariants after the fix:

- Scheduled Task action uses product-owned background Python (`pythonw.exe`) when available.
- Every subprocess/Popen path reachable from a healthy periodic supervisor tick on Windows must use `CREATE_NO_WINDOW` or equivalent no-console semantics when spawning console applications.
- `.cmd`/PowerShell shell wrappers must not be introduced into the periodic supervisor action.
- Task Scheduler `<Hidden>true</Hidden>` may remain, but it is not considered sufficient proof by itself.
- Existing PT1M cadence may remain unless process-trace evidence proves cadence itself is the problem; do not hide the symptom merely by making the task less frequent.

Audit the actual supervisor call graph (`host_control_v092.py` → v0.9.1/v0.9.2 Host/supervisor layers → provider/runtime/OpenClaw probes) for subprocess creation helpers. Consolidate only if needed; avoid unrelated refactoring.

If Phase A binds a specific child as the visible flash source, add a regression test or source-level assertion for that exact creation path and fix it at the process-spawn boundary.

## Mandatory tests — runtime ownership

Create focused tests, preferably:

`tests/test_runtime_ownership.py`

and/or:

`tests/test_startup_interpreter_selection.py`

At minimum cover:

### Test 1 — installer invoked from arbitrary venv

Simulate/fixture an executor interpreter path like:

`X:\executor\venv\Scripts\python.exe`

with a valid non-venv base Python.

Expected result: product runtime is selected/provisioned beneath the CogentNexus application-data runtime root; no generated durable launcher/task path contains `executor\venv`.

This test must be RED against current behavior.

### Test 2 — launcher is not PATH-dependent

Generated `cnxclaw.cmd` must contain/use the exact owned runtime foreground interpreter and must not invoke bare `python`.

### Test 3 — startup task uses owned background interpreter

Windows task substitution must select the product-owned `pythonw.exe` when present and never registration-time venv `pythonw.exe`.

### Test 4 — owned runtime missing/corrupt fails closed

Do not fall back to current arbitrary `sys.executable` for persistent execution.

### Test 5 — product runtime manifest/provenance validation

A valid manifest/runtime pair is accepted; a path outside the product application-data ownership boundary is rejected.

### Test 6 — no-console Windows process semantics

For the process helper(s) on the healthy supervisor path, assert `CREATE_NO_WINDOW`/equivalent behavior is applied on Windows. If Phase A identifies a specific unguarded spawn, test that exact production helper.

### Test 7 — v0.9.2 startup target preserved

`startup_v092.py` still resolves `host_control_v092.py` as the supervisor script.

## Installer/update/uninstall ownership

Because the operator intends a clean reinstall after review, source ownership must already support removal correctly.

Inspect uninstall/reset/install-over code and ensure the new owned runtime is classified as CogentNexus product-owned state:

- `uninstall` must remove the product-owned Python runtime after startup/lifecycle safety handoff and only inside the CogentNexus application-data ownership boundary;
- `reset` semantics must be explicit: preserve/recreate runtime as appropriate for a reset, but must never delete foreign Python;
- install-over must validate/reuse or replace the exact owned runtime deterministically;
- rollback must not leave the Scheduled Task pointing at a partially removed runtime;
- ownership checks must not expand deletion authority outside product boundaries.

Add tests for any new deletion/migration boundary.

## Test/verification commands

Record exact commands and outputs for:

1. Phase A process-start observation result and classification;
2. focused new regression test RED;
3. focused GREEN after implementation;
4. existing installer/startup/host-control tests relevant to changed code;
5. ownership/reset/uninstall tests affected by the new runtime boundary;
6. full Python test suite for the branch with exact pass/fail counts;
7. canonical repository validation/workflows reasonably required by the changed files;
8. `git diff --check` and clean working-tree state after commit.

If any existing test fails independently, bind the evidence; do not hide it.

## Live-state hard fence

Task 063 may observe natural supervisor process starts but must not mutate the installed product.

No live:

- `cnxclaw enable/disable/start/stop/restart/reset/uninstall`;
- installer/install-over;
- Scheduled Task create/update/delete/run/end;
- plugin config/set/enable/disable/install/uninstall;
- Gateway/Ollama/provider start/stop/restart;
- AGENTS/policy/ownership/SQLite writes;
- process termination;
- primary workspace Git mutation;
- Procmon Task 027/038 action;
- HermesAgent project mutation;
- merge/tag/release publication.

## Publication contract

Publish only:

`docs/operations/coordination/reports/CNX-20260825-063-own-supervisor-runtime-and-eliminate-console-flash.md`

The report must include:

- fetched execution HEAD;
- publication fence;
- Phase A flash trace evidence/classification;
- RED test evidence;
- exact source files changed and design;
- owned runtime root and manifest semantics;
- launcher/startup behavior before vs after;
- no-console spawn audit and exact flash fix;
- uninstall/reset/install-over ownership behavior;
- focused/full test commands and results;
- workflows/validation status;
- explicit statement that the live Scheduled Task and installation were not changed;
- exactly one result token.

Allowed result tokens:

- `PASS_OWNED_RUNTIME_AND_FLASH_FIX_IMPLEMENTED`
- `BLOCKED_FLASH_ROOT_CAUSE_NOT_BOUND`
- `BLOCKED_RUNTIME_OWNERSHIP_DESIGN_UNSAFE`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

A PASS is source acceptance evidence only. It does not mean the current live installation has been repaired.

## Pre-authorized successor after review

If ChatGPT reviews and accepts `PASS_OWNED_RUNTIME_AND_FLASH_FIX_IMPLEMENTED`, the operator has already authorized a separate successor to:

1. prepare/use the reviewed fixed release artifact/path;
2. capture final pre-uninstall preservation evidence;
3. run supported `cnxclaw uninstall` with required explicit confirmation;
4. prove CogentNexus-owned live surfaces are cleanly removed while unrelated OpenClaw/Ollama/user state is preserved;
5. install the reviewed fixed release fresh;
6. prove the new launcher and Scheduled Task use the CogentNexus-owned runtime and no Hermes/agent venv;
7. observe multiple natural supervisor ticks and prove no visible-console child process is created by the fixed path;
8. prove MANAGED/Gateway/Ollama/plugin/ownership/SQLite health after reinstall.

No additional operator confirmation is required for that bounded clean uninstall/reinstall successor because the operator explicitly requested it in this conversation.

Report meaningful progress approximately every 3 minutes and immediately after flash binding, RED, ownership design, GREEN/full tests, commit/publication, or blocker.
