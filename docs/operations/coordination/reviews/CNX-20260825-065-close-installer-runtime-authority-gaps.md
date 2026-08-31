# CNX-20260825-065 — Close Installer Runtime-Authority Gaps Review

Decision: `ACCEPT`

Disposition: `ACCEPT_INSTALLER_RUNTIME_AUTHORITY_GAPS_CLOSED`

Reviewed report result: `PASS_INSTALLER_RUNTIME_AUTHORITY_GAPS_CLOSED`

Fetched execution HEAD: `77dd425d00b9d627943f7f4c9c60e6c9d2873851`
Implementation HEAD: `21686f70520c5e0263e8aea4d644d2c87324e872`
Report HEAD: `8c74686dfe4c6817e2dcc9cbe27e2a8670c24c76`

## Independent publication fence

Execution HEAD -> implementation HEAD: ahead 1 / behind 0; only `scripts/install.ps1`, `skills/cogentnexus-openclaw/scripts/runtime_authority.py`, and `tests/test_installer_runtime_authority.py` changed.

Implementation HEAD -> report HEAD: ahead 1 / behind 0; only `docs/operations/coordination/reports/CNX-20260825-065-close-installer-runtime-authority-gaps.md` was added.

## Accepted source findings

- `install.ps1` resolves exactly `scripts\runtime_authority.py` through one explicit variable and verifies the script exists.
- `ensure-runtime --application-data-root <exact product root>` runs unconditionally on install/install-over before durable launcher/startup authority is written.
- the installer consumes the returned manifest and requires both owned foreground/background interpreters.
- existing-runtime reuse capability-probes both `python.exe` and `pythonw.exe`; a broken background interpreter is not accepted as healthy.
- generated `cnxclaw.cmd` binds the exact owned foreground interpreter.
- post-provision plugin ownership, MANAGED enable, supervisor doctor, and final status use `$ownedPython` rather than ambient bare `python`.
- accepted Task 064 Windows startup remains fail-closed and has no registration-time `sys.executable` fallback.

## Test review

Task 065 closed the Task 064 installer-facing blind spot with RED-first regression coverage. Hermes recorded focused GREEN `7 passed`, full developer suite `302 passed, 2 skipped, 0 failed`, baseline validator PASS, and clean `git diff --check`.

The installer-facing CLI `ensure-runtime` boundary was executed against temporary application-data roots. Stale manifest with an existing `python.exe` was repaired/revalidated, and a missing/broken `pythonw.exe` could not be accepted as healthy.

## Live boundary

Task 065 was source/tests only. The current machine remains on the old live installation. The operator still observes the recurring window flash; this is expected pre-reinstall evidence and does not contradict Task 065 because no live repair has occurred yet.

## Decision

`ACCEPT`

Disposition: `ACCEPT_INSTALLER_RUNTIME_AUTHORITY_GAPS_CLOSED`

The source is accepted for the already-authorized bounded clean uninstall/fresh reinstall successor. That successor must independently prove preservation, exact owned-runtime binding, no Hermes/agent path, and no recurring console flash across multiple natural supervisor ticks before live repair can be accepted.