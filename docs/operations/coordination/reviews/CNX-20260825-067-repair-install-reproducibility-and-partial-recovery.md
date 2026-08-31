# Review — CNX-20260825-067 Repair Install Reproducibility and Partial-Install Recovery

Decision: `REWORK`

Disposition: `REWORK_INSTALLER_TRANSACTION_NOT_WIRED_AND_ROLLBACK_PARENT_BOUNDARY`

Reviewed report result: `PASS_INSTALL_REPRODUCIBILITY_AND_PARTIAL_RECOVERY_FIXED`

Report commit: `30075a3a3e646f24e0144f74aac9104c0ce1e888`

Implementation HEAD: `ec51d7b20c228070a95a6cf0987cebd7e71cbfaf`

## Publication fence

Independent compare confirms:

- execution HEAD `347c6d7798f324060094a1e2bbfaf1536cd49c78` → implementation HEAD is one implementation commit changing only plugin package/lock validation, `install.ps1`, `namespace_ownership.py`, and the new recovery test;
- implementation HEAD → report HEAD `30075a3a3e646f24e0144f74aac9104c0ce1e888` is one report-only commit adding only the Task 067 report.

Publication discipline is ACCEPTED.

## Accepted D1 evidence

The lockfile/reproducibility correction is materially supported and should be preserved:

- `openclaw` devDependency is pinned to exact `2026.7.1-2`;
- lockfile was regenerated rather than relying on permissive npm behavior;
- report records clean `npm ci`, plugin validation, tests and pack under npm 11.16.0 and npm 12.0.2;
- plugin target/version remain v0.9.3 / OpenClaw 2026.7.1-2.

Disposition for D1: `ACCEPT_LOCKFILE_REPRODUCIBILITY_FIX`.

## Blocking D2 finding 1 — production installer never begins the transaction

The implementation/report says `install.ps1` begins a fresh transaction before residue-capable mutation. Independent inspection contradicts that claim.

The exact Task 067 `install.ps1` patch adds only `recovery-preflight` before `classify-install`. The complete production file contains no invocation of:

- `transaction-begin`;
- `transaction-record`;
- `transaction-commit`;
- a fresh-install rollback command/surface.

After classification, production execution proceeds directly through `Enter-NativeInstallBoundary`, target skill directory/copy/move, validation, host init, policy application, `npm ci`, plugin installation, runtime/launcher creation and ownership creation.

Therefore a fresh install can still fail after creating state/skill residue without ever having written an incomplete transaction marker. A rerun then sees unmarked residue and remains fail-closed exactly as Task 066 did. The new recovery implementation is not connected to the failing production path.

This violates Task 067 D2 requirements 1, 4, 5 and 6 and mandatory R1/R3.

## Blocking D2 finding 2 — R1/R1b tests do not exercise installer ordering

`tests/test_fresh_install_transaction_recovery.py` calls `begin_fresh_transaction(workspace)` directly and then creates synthetic residue via `_make_residue()`.

That proves the Python transaction API can work when a caller uses it correctly, but it does not prove that production `scripts/install.ps1` invokes the API before its first residue-capable mutation. Consequently the focused tests pass while the real installer does not begin a transaction.

Task 067 explicitly required the production fresh-install transaction begin surface / installer ordering to be exercised or extracted. That evidence is missing.

## Blocking D2 finding 3 — rollback can remove a generic non-product parent

`rollback_transaction()` removes `skillPath`/`stateRoot` and then walks upward while paths remain under the workspace. For `skillPath = <workspace>\skills\cogentnexus-openclaw`, this can remove `<workspace>\skills` when it becomes empty.

`<workspace>\skills` is a shared OpenClaw/user namespace, not a CogentNexus-owned boundary. `recovery_preflight()` also contains parent-removal logic that can remove the same generic parent when empty.

Deletion authority must stop at the exact owned roots; an empty shared parent is still not CogentNexus-owned.

Current R3 protects an unrelated file at `<workspace>\USER.md` but does not assert preservation of an empty/preexisting `<workspace>\skills` directory, so this escaped testing.

## Required correction

A narrow successor source task must:

1. preserve the accepted D1 lock/package fix;
2. wire the fresh transaction into the real installer after `classify-install` has proven `fresh` and before the first fresh residue-capable mutation;
3. record every recoverable fresh-created owned artifact/root before or atomically with creation, with no authorization outside exact CNX roots/launcher/application-data boundary;
4. ensure normal success commits/retires the marker only after ownership verification;
5. ensure caught fresh-install failure invokes bounded rollback, while process crash/power loss is handled by rerun `recovery-preflight`;
6. make production installer-facing tests fail if `transaction-begin`/record/commit/rollback wiring is removed or moved after residue creation;
7. stop rollback cleanup at exact CNX-owned roots and never remove generic `<workspace>\skills` or other parent namespaces;
8. add sentinels proving shared parent directories and unrelated contents survive rollback/recovery;
9. run full Python and both npm toolchain validations again;
10. keep the current live Task-066 residue untouched.

## Live gate

Do NOT perform Task 068 live cleanup/reinstall yet. The current live state remains native OpenClaw with Task-066 partial residue and no CogentNexus supervisor/launcher/plugin registration.

A later live successor is authorized only after the corrected installer transaction wiring is independently accepted.
