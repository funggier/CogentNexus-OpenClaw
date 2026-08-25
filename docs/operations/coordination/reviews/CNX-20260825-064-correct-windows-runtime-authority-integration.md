# CNX-20260825-064 — Correct Windows Runtime Authority Integration Review

Decision: `REWORK`

Disposition: `REWORK_INSTALLER_RUNTIME_AUTHORITY_EXECUTION_GAPS`

Reviewed report result: `PASS_WINDOWS_RUNTIME_AUTHORITY_REWORK_VERIFIED`

Fetched execution HEAD: `0b4933227ff92da3ab3ad103dcfe9bacb6e8a5e1`
Implementation HEAD: `6e4245112a38dab3e6614e6f91d3e37ac85f2afe`
Report HEAD: `f3a4731b87f8a530dd71eed3826a93f963a9de34`

## Accepted evidence

Task 064 correctly separates implementation and report publication. Independent compare verified:

- `0b493322...` -> `6e424511...`: exactly one implementation commit touching only `scripts/install.ps1`, `runtime_authority.py`, `startup.py`, and the two runtime-authority test files;
- `6e424511...` -> `f3a4731b...`: exactly one report-only commit adding only the Task 064 report.

The source corrections for the original Task 063 B1-B3 defects are directionally valid:

- `_interpreter_paths()` now forms Windows `python.exe` and `pythonw.exe` as real `Path` objects;
- exact product-root vs LOCALAPPDATA-base semantics are separated;
- manifest path validation uses ancestry rather than raw prefix matching;
- Windows startup interpreter selection is fail-closed and no longer intentionally falls back to registration-time `sys.executable`;
- real temporary Windows runtime provisioning and owned-runtime CLI import coverage were added;
- the reported isolated dev environment ran `295 passed, 2 skipped`.

The accepted Task 063 flash diagnosis remains `FLASH_CHILD_PROCESS`. No live installation mutation occurred in Task 064.

## Blocking findings

### B5 — committed production installer path is broken

The actual implementation commit patch contains:

```powershell
& python (Join-Path $targetSkill "scripts\
untime_authority.py") ensure-runtime --application-data-root "$applicationDataRoot" | Out-Null
```

The newline is present in the committed `scripts/install.ps1`; it is not a display-only artifact. PowerShell therefore constructs a path containing a line break rather than `scripts\runtime_authority.py`.

A fresh installation that reaches owned-runtime provisioning will fail before the owned runtime can be created.

This alone blocks the pre-authorized live clean reinstall.

### B6 — installer does not actually validate/recreate a corrupt existing runtime

The production installer calls `ensure-runtime` only when:

```powershell
if (-not (Test-Path $ownedPython)) { ... }
```

If `<applicationDataRoot>\runtime\python\Scripts\python.exe` exists while `runtime-manifest.json` is missing/corrupt, or while the background interpreter is invalid, the installer skips runtime validation/provisioning entirely.

Task 064 T8 proves `runtime_authority.ensure_runtime()` can recreate a deleted manifest when called directly, but it does not prove that `scripts/install.ps1` actually calls that validation path during install-over. Therefore the report overstates the install-over integration guarantee.

### B7 — durable-authority transition remains incomplete in `install.ps1`

After `$ownedPython` is established, several normal CogentNexus Python operations in the installation transition still use ambient bare `python`, including ownership resolution/creation/verification, `cnxclaw_v093.py enable`, supervisor doctor, and final status.

This does not by itself re-persist the executor interpreter now that `startup.py` fails closed, but it does not satisfy Task 064's stronger intended authority transition: after provisioning, product Python operations that can safely run under the owned runtime should use `$ownedPython`, especially MANAGED enable/status paths.

The successor should close this boundary rather than leave the product installation dependent on the invoking executor for post-provision execution.

## Test-gap finding

The 295-pass suite does not execute the production installer runtime-provisioning block. T1 invokes `runtime_authority.py` directly; T5 constructs a launcher independently using the intended shape; T8 invokes `ensure_runtime()` directly. Consequently the committed newline defect and the installer-level corrupt-runtime bypass were not exercised.

A successor must add an installer-facing regression boundary capable of failing on these exact production defects, not merely another duplicated representation of intended behavior.

## Review decision

`REWORK`

Task 064 is accepted as useful diagnosis and partial source correction, but it is **not accepted as live-installable evidence**. Do not uninstall or reinstall the current CogentNexus-OpenClaw yet.

Required successor scope is narrow:

1. repair the exact committed installer provisioning path;
2. make installer runtime validation unconditional before durable launcher/task creation, so stale/corrupt product runtime state is validated/recreated deterministically;
3. switch post-provision CogentNexus Python operations that are safe to the exact `$ownedPython` authority;
4. add regression coverage against the actual installer-facing contract so the B5/B6 class cannot pass again;
5. rerun focused + complete canonical tests and preserve a separate report-only publication fence;
6. no live installation mutation in that correction task.

If that successor is accepted, proceed immediately to the already-authorized clean uninstall/fresh reinstall task without another operator confirmation.
