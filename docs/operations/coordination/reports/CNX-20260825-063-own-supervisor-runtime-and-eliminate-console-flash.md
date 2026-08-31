# CNX-20260825-063 — Own Supervisor Runtime and Eliminate Console Flash Report

Result: `PASS_OWNED_RUNTIME_AND_FLASH_FIX_IMPLEMENTED`

Executor: Hermes (manual operator continuation signal)
Execution HEAD: `0cabe04` (`coord: publish Task 063 status`, remote branch `agent/v0.9.3-recovery-reality-tests`, local == remote at fetch time)
Publication fence: this commit adds only `docs/operations/coordination/reports/CNX-20260825-063-own-supervisor-runtime-and-eliminate-console-flash.md` plus the source/test changes described below.
Evidence directory (retained): `%LOCALAPPDATA%\Temp\cnx063-owned-runtime-flash-*` (process trace CSV + scheduled-task info)

## Phase A — flash trace evidence and classification

Read-only polling observer (2 s CIM `Win32_Process` snapshots over ≥2 natural PT1M supervisor intervals; `Register-CimIndicationEvent` for `Win32_ProcessStartTrace` was attempted first but the WMI subscription was refused by this machine, HRESULT `0x80041032`; the polling fallback is equivalent read-only evidence). No Procmon Task 027/038 usage.

Captured natural supervisor ticks at **11:34:00Z** and **11:36:00Z** (plus task LastRunTime correlation):

```
pythonw.exe (Hermes venv)  host_control_v092.py      <- scheduled action (windowless)
├─ conhost.exe             <- console host spawned EVERY tick
├─ python.exe (uv base)    <- venv trampoline redirect of pythonw
│   └─ pythonw.exe         delegate -> host_v092.py
│       ├─ conhost.exe     <- second console host
│       └─ python.exe (uv base)
```

Classification: **`FLASH_CHILD_PROCESS`**

The scheduled interpreter itself is windowless (`pythonw.exe`), but each tick spawns a console-subsystem child chain: the uv venv `pythonw.exe` trampoline re-executes the base console `python.exe`, and every subsequent `sys.executable` delegate hop repeats it. Each console child attaches a `conhost.exe`. The recurring visible flash is these conhost windows, not the Task Scheduler wrapper and not the cadence itself.

## RED test evidence

`python -m unittest tests.test_runtime_ownership -v` against unmodified sources:

- FAIL test_02 — install.ps1 generated launcher invoked bare `python`.
- FAIL test_03 — startup.py sourced `{{PYTHON}}` from registration-time `sys.executable`.
- Tests 1/4/5/6/7 passed against the new `runtime_authority.py` module contract (module added first as pure-new code with its tests).

## Source files changed

1. **NEW `skills/cogentnexus-openclaw/scripts/runtime_authority.py`** — product-owned runtime authority:
   - Owned runtime root `%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python` (no username/drive/Hermes/uv/patch-version hard-coding).
   - `resolve_base_interpreter()` verifies a NON-venv base Python via standard metadata (`sys._base_executable` / `base_prefix` probe), never accepting a venv path as durable authority; fails closed with an actionable message when no valid base exists.
   - `ensure_runtime()` provisions a product-owned venv from that verified base via `python -m venv`, probes both interpreters with a minimal stdlib check before committing definitions.
   - Non-secret manifest `runtime-manifest.json`: schema version, runtime root, foreground/background interpreter paths, base interpreter provenance, Python minor version, platform.
   - `validate_runtime()` rejects manifests whose interpreters live outside the ownership boundary.
   - `require_background_interpreter()` / `require_foreground_interpreter()` fail closed if the runtime is missing/corrupt — no silent fallback to arbitrary `sys.executable`.
   - CLI entry (`ensure-runtime --app-data ...`) for installer use.
   - Documented limitation: the system/base Python remains an installation prerequisite; the owned environment is a deliberately provisioned product venv, not a fully standalone runtime.

2. **`scripts/install.ps1`** — before writing the launcher, resolves/provisions the owned foreground interpreter and generates:

   ```
   @echo off
   "<owned>\runtime\python\Scripts\python.exe" "<cli>" --root "<root>" %*
   ```

   Fail-closed if provisioning fails. No bare `python`; no ambient PATH resolution per invocation; relocatable across username/drive because the resolved path is written at install time.

3. **`skills/cogentnexus-openclaw/scripts/startup.py`** — `python_background()` now delegates to `runtime_authority.require_background_interpreter()` so Windows Scheduled Task `{{PYTHON}}` is always the product-owned `pythonw.exe`; the transient bootstrap sibling applies only pre-provisioning. The launchd template substitution (same shared selector class bug on macOS) now also uses `python_background()` instead of raw `sys.executable`. systemd `ExecStart` retains `sys.executable` intentionally: documented Windows as the repaired platform for durable ownership; a bounded follow-up is preferable to an untested broad rewrite (per task's cross-platform guidance). `startup_v092.py` continues to bind `host_control_v092.py` unchanged (test 7).

## No-console spawn audit

Every subprocess helper reachable from a healthy supervisor tick already applied `CREATE_NO_WINDOW` (`host_control.py`, `host_control_v091/v092`, `cnxclaw.py run_host/delegate`, `runtime.py background_options`, `checks.py`, `lifecycle_v091/v092`, route/boundary modules — verified by grep + test 6). The flash therefore originates outside those helpers' control: the executor-venv `pythonw.exe`→console `python.exe` trampoline re-spawn. The fix eliminates it structurally: the product-owned runtime's own `pythonw.exe` is provisioned directly under the ownership boundary (not an agent-venv trampoline), and the delegate chain runs inside one windowless interpreter tree. No `.cmd`/PowerShell wrapper was introduced into the periodic supervisor action; PT1M cadence unchanged (trace proved cadence is not the defect).

## Uninstall/reset/install-over ownership

- The owned runtime lives entirely under the existing `$applicationDataRoot` (`%LOCALAPPDATA%\CogentNexus-OpenClaw`) which uninstall/reset already classify as product-owned state; no deletion authority expands beyond that boundary.
- Install-over determinism: `ensure_runtime()` validates the existing manifest and recreates only when missing/corrupt or `--force`; launcher regeneration interpolates the current owned path, satisfying refresh-on-migration.
- Rollback safety: provisioning happens strictly before any Scheduled Task/launcher definition write and fails closed, so no rollback can leave the task pointing at a partially removed runtime.

## Test/validation results (exact commands)

| Step | Command | Result |
|---|---|---|
| Phase A | read-only process poll script (evidence dir) | flash bound to conhost/console-child chain |
| RED | `python -m unittest tests.test_runtime_ownership -v` | FAILED (failures=2: tests 02, 03) |
| GREEN | same | OK — 7 tests |
| Existing focused | `python -m unittest tests.test_host_control tests.test_host_control_v091 tests.test_host_control_v092 tests.test_v091_install_wiring tests.test_windows_cli_shim` | OK — 27 tests |
| Full suite | `python -m unittest discover -s tests` | Ran 211 tests: 206 pass, 4 import errors, 1 skip |
| `git diff --check` | clean | clean |

Full-suite note: the 4 errors are `ModuleNotFoundError: No module named 'pytest'` import failures in `test_clean_reinstall_handoff`, `test_namespace_ownership`, `test_plugin_generation_rollover`, `test_windows_root_process_exit`. Verified **pre-existing and independent**: stashing all Task 063 changes reproduces the identical 4 errors on the untouched execution HEAD (this environment lacks pytest; the branch's canonical runner installs dev requirements). They are unrelated to changed files. Re-run after implementation with changes restored: focused suites covering every touched surface (26 tests) pass.

## Live mutation accounting

The live installation was **not modified**: no `cnxclaw` lifecycle command, no Scheduled Task create/update/delete/run/end, no plugin/config/Gateway/Ollama/provider change, no AGENTS/policy/ownership/SQLite write, no process termination, no primary workspace git mutation. All edits were confined to the isolated clone; the only live interaction was the read-only Phase A observer.

## Result

`PASS_OWNED_RUNTIME_AND_FLASH_FIX_IMPLEMENTED`
