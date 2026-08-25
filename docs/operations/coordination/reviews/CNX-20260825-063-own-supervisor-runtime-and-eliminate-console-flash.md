# Review — CNX-20260825-063 Own Supervisor Runtime and Eliminate Console Flash

Decision: `REWORK`

Disposition: `REWORK_WINDOWS_RUNTIME_AUTHORITY_INTEGRATION_DEFECTS`

Reviewed report/result: `PASS_OWNED_RUNTIME_AND_FLASH_FIX_IMPLEMENTED`

Reviewed implementation/report commit:

`5962383ac8e16b1336e0af78f659e2f5fa29dd97`

Execution HEAD reported by Hermes:

`0cabe04e67e14da7f59e8fc4103d87f96e216256`

## Publication and scope verification

Independent compare from execution HEAD to `5962383a...` is ahead by exactly one commit and changes only five in-scope paths:

1. `docs/operations/coordination/reports/CNX-20260825-063-own-supervisor-runtime-and-eliminate-console-flash.md`
2. `scripts/install.ps1`
3. `skills/cogentnexus-openclaw/scripts/runtime_authority.py`
4. `skills/cogentnexus-openclaw/scripts/startup.py`
5. `tests/test_runtime_ownership.py`

No unrelated product/runtime file is present in the published delta. However implementation + tests + report were combined into one commit rather than an implementation commit followed by a report-only publication commit. This is a publication-contract deviation, but it is not the primary reason for REWORK.

## Accepted diagnostic finding

The Phase A trace is useful and accepted as bounded diagnosis evidence:

`FLASH_CHILD_PROCESS`

The live Hermes/uv venv `pythonw.exe` path produces console-subsystem child/base-Python transitions and `conhost.exe` on the natural PT1M supervisor cadence. The current live installation was not mutated by Task 063.

## Blocking source findings

### B1 — Windows background interpreter path construction is invalid

`runtime_authority._interpreter_paths()` contains:

```python
background = scripts / ("pythonw.exe",) if os.name == "nt" else (scripts / "python3",)
```

On Windows, `("pythonw.exe",)` is a tuple. `pathlib.Path.__truediv__` does not accept a tuple path component, so real Windows provisioning reaches a `TypeError` before a valid background interpreter can be returned.

The focused tests did not execute this production Windows provisioning path.

### B2 — installer/CLI app-data contract duplicates the product root

`scripts/install.ps1` defines:

```powershell
$applicationDataRoot = Join-Path $localAppData "CogentNexus-OpenClaw"
```

and invokes:

```powershell
runtime_authority.py ensure-runtime --app-data $applicationDataRoot
```

But `runtime_authority._cli()` maps that argument to `LOCALAPPDATA`, while `app_data_root()` then appends `CogentNexus-OpenClaw` again.

Therefore the runtime authority attempts to provision beneath:

`%LOCALAPPDATA%\CogentNexus-OpenClaw\CogentNexus-OpenClaw\runtime\python`

while the installer immediately requires:

`%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python\Scripts\python.exe`

A fresh Windows install would therefore fail even if B1 were corrected.

### B3 — startup silently reintroduces arbitrary executor ownership

`startup.py::python_background()` catches all exceptions from `runtime_authority.require_background_interpreter()` and falls back to registration-time `sys.executable` / sibling `pythonw.exe`.

That recreates the original architectural defect if the owned runtime is missing/corrupt and `enable` is invoked through Hermes/Codex/another venv. The Task 063 contract explicitly required persistent execution to fail closed and prohibited silent fallback to an arbitrary registration-time venv.

The bootstrap/runtime-provisioning exception must live only inside the installer provisioning boundary. Startup registration itself must require an already-verified product-owned runtime.

### B4 — tests are too structural to verify the Windows integration

Tests 02/03 assert source strings rather than executing the installer/runtime/startup contract. Consequently they passed despite B1-B3.

The full suite also was not demonstrated clean in the executor environment: four modules failed import because `pytest` was missing. The report established those failures were pre-existing, but before live reinstall the successor must run the canonical/dev dependency environment and obtain a complete fresh pass or bind a repository-defined accepted exception.

## Required correction

Do not uninstall/reinstall yet.

A successor source-only task must:

- correct the interpreter-path type error;
- define one unambiguous argument contract: either local app-data base or exact CogentNexus application-data root, with names/tests matching that contract;
- make Windows startup registration fail closed when the owned runtime is missing/corrupt;
- keep transient bootstrap authority confined to installer provisioning only;
- add real Windows/temp-boundary integration tests that provision a runtime in a temporary application-data root and validate foreground/background interpreter paths + manifest;
- execute the generated launcher contract against a temporary fixture where practical rather than checking source strings alone;
- exercise startup task-template substitution against an owned temp runtime without creating/changing the live Scheduled Task;
- test the missing-runtime case proves no executor-venv fallback;
- use an exit-only probe for `pythonw.exe` if stdio is unavailable under the Windows GUI interpreter;
- run focused tests plus the complete repository test suite with dev requirements installed in an isolated test environment;
- preserve the accepted `FLASH_CHILD_PROCESS` diagnosis and no-console spawn audit.

## Live safety decision

The pre-authorized clean uninstall/reinstall remains authorized in principle, but its gate is **not satisfied** by Task 063. The current live installation must remain unchanged until the corrected source is independently reviewed.

No release/merge/live reinstall is accepted from commit `5962383a...`.
