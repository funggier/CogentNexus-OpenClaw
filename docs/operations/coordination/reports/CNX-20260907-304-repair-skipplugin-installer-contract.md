# CNX-20260907-304 — Repair Staging Installer SkipPlugin Contract

## Disposition

`PASS_REPOSITORY_TDD_REPAIR_GREEN__LIVE_RETRY_FORBIDDEN`

Task304 repaired the repository installer contract exposed by Task303. The repair is repository-only. The live installer was not retried and `cnxclaw enable` was not invoked.

## Root cause

Task303's supported staging invocation used `-SkipPlugin -SkipGatewayRestart -SkipAgentsPolicy`. The installer correctly performed an earlier `preflight-skip-plugin` check, but after copying the skill and writing the launcher it unconditionally called `resolve-plugin`, converted its result, and compared `installedPluginFingerprint.ToLowerInvariant()` with `$expectedPluginFingerprint.ToLowerInvariant()`.

With the skip path, plugin identity is deliberately not re-resolved or mutated. A null/absent resolution therefore reached the unconditional comparison and produced the observed PowerShell error at line 506:

```text
You cannot call a method on a null-valued expression.
```

This was a control-path defect after repository-owned mutation, not evidence that the normal plugin path was invalid.

## TDD method

### RED

Added regression tests before the production change for both installers:

```text
python -m pytest tests/test_namespace_install_contract.py::test_windows_skip_plugin_short_circuits_post_copy_plugin_resolution tests/test_namespace_install_contract.py::test_posix_skip_plugin_short_circuits_post_copy_plugin_resolution -q

2 failed
```

The failures were the expected missing post-copy SkipPlugin guards. One test assertion was corrected because it initially looked for the inverse guard; the production tests remained red until the implementation was changed.

### Minimal GREEN repair

- `scripts/install.ps1`: wrap post-copy plugin resolution, fingerprint comparison, ownership-manifest creation, and ownership verification in the normal `else` path; the SkipPlugin path emits an explicit staging postcondition and performs no plugin resolution/ownership mutation.
- `scripts/install.sh`: apply the equivalent conditional for cross-platform contract parity.
- Existing preflight remains before the first mutation and still requires a coherent exact-plugin upgrade for SkipPlugin.
- Normal plugin installation, fingerprint binding, rollback, and ownership verification code remains unchanged in its non-skip path.

Focused GREEN result:

```text
python -m pytest tests/test_namespace_install_contract.py -q
10 passed in 0.04s
```

Installer/ownership regression result:

```text
48 passed in 4.79s
```

Full repository result:

```text
539 passed, 5 skipped, 4 subtests passed in 164.41s (0:02:44)
```

## Changed-file evidence at source checkout

```text
scripts/install.ps1
33173 bytes
SHA-256: 41f199c1959491c2c6a72932eff0f286db66dde75e60b4b5c5cf846978aa71e2

scripts/install.sh
13793 bytes
SHA-256: d97f90433ae269cb83f64c6dd37103eb9fef4828f8b50116b84f0f571ed2d0fb

tests/test_namespace_install_contract.py
7766 bytes
SHA-256: e201d1feeb4fcc1c9b2f633b732631265b09a58e0e0be70b6d785d3eb52ae6fe
```

## Live boundary

No live action was performed under Task304 after the Task303 partial adoption. In particular:

- no installer retry
- no `cnxclaw enable`
- no plugin install/replace
- no Gateway/service/Scheduled Task mutation
- no config/Ticket/SQLite/session mutation
- no semantic send, replay, redelivery, or disposition
- no protected-state mutation
- no force push

Task301 wiring remains adopted in live from Task303, but managed activation and worker requalification remain unproven. Durable Discord delivery remains pending/unconfirmed and was not touched.

## Safety accounting

```text
repository source/test writes: 3 files
live installer invocations during Task304: 0
live installer retries after Task303: 0
cnxclaw enable: 0
plugin install/replace: 0
Gateway restart/reload: 0
Scheduled Task/service mutation: 0
manual durable-state mutation: 0
semantic external sends: 0
replay/redelivery/disposition: 0
protected-state mutation: 0
force push: 0
```

## Next bounded task

The next task must separately authorize one bounded staging installer retry using the repaired exact candidate and require read-only preflight plus postflight. It must not infer managed activation authority from repository GREEN. A later task must separately authorize `cnxclaw enable` and live requalification only after the repaired installer returns a terminal success and the exact installed candidate identity is re-proven.
