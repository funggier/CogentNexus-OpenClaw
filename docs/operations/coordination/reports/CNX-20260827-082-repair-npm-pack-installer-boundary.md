# CNX-20260827-082 — Repair npm Pack Installer Boundary

Result: `PASS_NPM_PACK_INSTALLER_BOUNDARY_REPAIRED`

## Scope and live fence

Task 082 was executed as source/test-only work. The Task-081 partial live installation was inspected read-only and was not repaired or normalized.

Live mutation accounting:

- live install/install-over: `0`
- live uninstall/reset/cleanup: `0`
- controller/plugin/startup/Supervisor/AGENTS/ownership/runtime/config mutation: `0`
- live SQLite/Ticket/session mutation: `0`
- Dashboard/WebChat semantic messages: `0`
- CLI semantic runs: `0`
- direct Ollama/provider probes: `0`
- provider/model/timeout changes: `0`
- reboot/merge/tag/release: `0`

Evidence directory:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx082-preflight-20260826T174516Z`

## Lineage and publication heads

Execution HEAD before implementation:

`52c86bc756f57cd8ee8c1806ba2f26cc59cb8639`

Task-081 report and accepted blocker review were present in the execution ancestry. The accepted semantic candidate lineage was preserved:

`70d02e76233ca1084da445d488f88b628455f4aa`

Implementation commit:

`df412ed10522d79a722e1b48d681e7553cb79ae2`

Implementation changes are limited to:

- `scripts/resolve-npm-pack-artifact.ps1`
- `scripts/install.ps1`
- `tests/test_npm_pack_installer_boundary.py`

## Phase A — toolchain and boundary inspection

Windows PowerShell parser check:

- PowerShell: `5.1.19041.6456`

Accepted compatibility paths:

- npm 11 path: Node `v24.18.0`, npm `11.16.0`
- npm 12 path: Node `v22.23.2`, npm `12.0.2`

The inspected production boundary was the following pre-repair logic in `scripts/install.ps1`:

```powershell
$packed = $packOutput | ConvertFrom-Json
$packedItems = @($packed)
if ($packedItems.Count -ne 1 -or -not $packedItems[0].filename) {
    throw "npm pack did not return exactly one package artifact"
}
```

The existing `verify-package-contents.mjs` already normalized npm 11 array output and npm 12 keyed-object output, but the installer did not.

## Gate R — raw npm pack evidence and RED reproduction

Raw evidence files:

- `npm11/versions.json`
- `npm11/pack.stdout.utf8`
- `npm11/pack.stderr.utf8`
- `npm11/pack.meta.json`
- `npm12/versions.json`
- `npm12/pack.stdout.utf8`
- `npm12/pack.stderr.utf8`
- `npm12/pack.meta.json`

### npm 11

- PowerShell: `5.1.19041.6456`
- Node: `v24.18.0`
- npm: `11.16.0`
- JSON top-level type: array
- array count: `1`
- stderr length: `0`
- artifact: `openclaw-plugin-cogentnexus-openclaw-0.9.3.tgz`
- artifact bytes: `5130`
- artifact SHA-256: `347a3e29fe52db3d39e6557c5ee26055fbbdc1a1fe575511716d0bf0d76605b1`

### npm 12

- PowerShell: `5.1.19041.6456`
- Node: `v22.23.2`
- npm: `12.0.2`
- JSON top-level type: object
- keyed package names: `openclaw-plugin-cogentnexus-openclaw`
- key count: `1`
- stderr length: `0`
- artifact: `openclaw-plugin-cogentnexus-openclaw-0.9.3.tgz`
- artifact bytes: `5130`
- artifact SHA-256: `347a3e29fe52db3d39e6557c5ee26055fbbdc1a1fe575511716d0bf0d76605b1`

The exact pre-fix production parser was run against the captured npm 12 keyed output. It observed:

```json
{
  "topType": "PSCustomObject",
  "itemCount": 1,
  "filename": "",
  "reproducesFailure": true
}
```

This reproduced the Task-081 failure boundary before production code was edited.

Initial RED test result after adding the contract tests and before creating the helper:

- `4 failed, 2 passed`
- failures were the expected missing-helper and missing-installer-wiring failures

## Gate P — canonical resolver

Added `scripts/resolve-npm-pack-artifact.ps1` with one production/test boundary:

`Resolve-NpmPackArtifact -PackJson <text> -PluginDir <directory>`

The helper:

- accepts npm 11 array shape with exactly one item;
- accepts npm 12 single-entry keyed-object shape through `PSObject.Properties` normalization;
- rejects zero entries, multiple entries, unsupported shapes and invalid JSON;
- requires a non-empty string `filename`;
- rejects absolute paths, path separators, traversal and unsafe filename characters;
- requires `.tgz` package-artifact naming;
- resolves the artifact inside the plugin directory;
- verifies the exact file exists before installation;
- returns the exact `{ filename, path }` pair used by the installer.

The installer now dot-sources and calls this helper after successful `npm pack --json`, before rollover planning. It passes only the resolver-returned path to:

```powershell
openclaw plugins install ("npm-pack:" + $packagePath) --force
```

The existing `finally` cleanup boundary remains in place and removes the exact resolved artifact after the install attempt. No arbitrary pre-existing `*.tgz` is selected.

## Gate P2 — PowerShell 5.1 GREEN

Production helper harness:

`ps51-green-harness.ps1`

Result: both captured real pack outputs resolved successfully to:

`openclaw-plugin-cogentnexus-openclaw-0.9.3.tgz`

Actual artifact proof:

`actual-artifact-proof.json`

- npm 11 generated artifact path resolved exactly;
- npm 12 generated artifact path resolved exactly;
- both artifacts were `5130` bytes;
- both SHA-256 values were `347a3e29fe52db3d39e6557c5ee26055fbbdc1a1fe575511716d0bf0d76605b1`;
- isolated generated `.tgz` artifacts were removed after evidence capture.

PowerShell syntax parsing passed for both:

- `scripts/install.ps1`
- `scripts/resolve-npm-pack-artifact.ps1`

## Gate I — installer wiring tests

Added `tests/test_npm_pack_installer_boundary.py` covering:

- npm 11 array success;
- npm 12 keyed-object success;
- zero artifacts;
- multiple artifacts;
- missing/empty filename;
- invalid JSON/unsupported shapes;
- unsafe traversal and path-separator filenames;
- missing artifact existence failure;
- exact helper invocation/wiring;
- exact plugin install path;
- cleanup presence;
- artifact resolution before rollover.

Focused result after implementation:

`6 passed`

## Gate C and full verification

### Node 24 / npm 11

- clean `npm ci`: passed
- full plugin tests: `49 files, 257 tests passed`
- `npm run plugin:validate`: passed
- mixed-plugin artifact verification: PASS
- ticket DB bootstrap: PASS
- package contents: PASS, `176` files

### Node 22 / npm 12

- clean `npm ci`: passed
- full plugin tests: `49 files, 257 tests passed`
- `npm run plugin:validate`: passed
- mixed-plugin artifact verification: PASS
- ticket DB bootstrap: PASS
- package contents: PASS, `176` files

### Python and regression suites

- full Python suite: `362 passed, 2 skipped, 4 subtests passed`
- targeted installer/recovery plus npm-pack boundary suite: `58 passed`
- baseline consistency: `PASS`
- `git diff --check`: passed

## Read-only live partial-state confirmation

Evidence: `live-preservation.txt`.

The Task-081 partial installation remained untouched:

- `namespace_ownership.py verify`: passed
- `recovery-preflight`: `OWNERSHIP_PRESENT`
- classification: `upgrade`
- controller: `passthrough`, generation `13`
- AGENTS managed markers: `0/0`
- canonical plugin generation: version `0.9.3`, disabled
- Supervisor Scheduled Task: absent
- SQLite integrity: `ok`
- tickets: `0`
- outbox: `0`
- Gateway task remained present

No live repair or restoration was attempted. The next separately authorized recovery task may perform exactly one supported normal install-over from this implementation.

## Final disposition

`PASS_NPM_PACK_INSTALLER_BOUNDARY_REPAIRED`

Independent review is required before the successor live recovery task. That successor must use the exact implementation commit above, re-prove the partial state, perform one supported install-over only, restore MANAGED/startup/Supervisor/AGENTS through installer-supported behavior, and complete its own no-flash and owner-surface gates.
