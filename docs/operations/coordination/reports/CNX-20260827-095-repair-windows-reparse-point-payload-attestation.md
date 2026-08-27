# CNX-20260827-095 — Repair Windows Reparse-Point Payload Attestation

Result: `PASS_WINDOWS_REPARSE_POINT_PAYLOAD_ATTESTATION_REPAIRED`

## Scope and live fence

This task was executed source/test-only. No live install-over, uninstall, reset, cleanup, plugin-generation mutation, controller/startup/Supervisor/AGENTS/config/runtime/SQLite edit, provider/model/timeout change, semantic message, direct provider probe, restart, merge, tag, or release was performed.

Task-092 semantic artifacts remain retired and were not reused or modified.

## Phase A — real Windows reparse RED

- Coordination branch was fetched/reset before work.
- Execution HEAD before source edits: `4946bdc6365f5d73c1dd4f07db422205a8489d40`
- Task-094 implementation/report and independent rework disposition were present in ancestry.
- Host: Windows 10 build `10.0.19045.6466`.
- A fresh external fixture was created outside the product/live roots.
- A real directory junction was created with native `mklink /J` beneath declared `dist/` content, targeting a directory outside the physical package directory.
- `fsutil reparsepoint query` proved the actual Windows reparse metadata:

```text
Reparse Tag Value : 0xa0000003
Tag value: Mount Point
```

- Python reported `junction.is_symlink() == False` and `junction.is_dir() == True`.
- Against the Task-094 predecessor source, `plugin_fingerprint()` accepted/traversed the junction and returned a fingerprint. This established the real RED, not a monkeypatch-only simulation.

## Gate R — mandatory RED

The regression test `test_package_payload_rejects_real_windows_directory_junction` uses the real production helper, creates a native Windows directory junction, verifies it is a directory but not a symbolic link, and requires fingerprint rejection.

Before the production edit it failed as intended:

```text
Failed: DID NOT RAISE RuntimeError
```

This proves the predecessor followed the reparse-point boundary.

The existing symbolic-link rejection remains represented separately. The symlink fixture is platform-gated and was skipped on this host because ordinary symlink creation is unavailable under the test process permissions; the real junction fixture ran successfully and is the mandatory Windows case.

## Gate F — minimal production fix

Added `_filesystem_metadata(path, relative)` to `namespace_ownership.py`.

The predicate:

- reads metadata using `Path.lstat()` without following the target;
- rejects symbolic links;
- on Windows requires `st_file_attributes` and rejects `FILE_ATTRIBUTE_REPARSE_POINT` (including directory junctions);
- fails closed when required metadata is unavailable;
- runs before file/directory classification and before recursive `scandir()` traversal;
- applies to `package.json`, every declared package entry and every recursively discovered child;
- does not resolve a target and then whitelist it;
- does not change the v2 digest framing, package contract, classifier, rollover or Dashboard staging semantics.

## Gate G — GREEN and preservation

After the fix:

- real Windows junction test passed;
- focused payload/path/security suite: `6 passed, 1 skipped`;
- ownership and rollover focused suites: `73 passed, 1 skipped`;
- full Python suite: `382 passed, 3 skipped, 4 subtests passed`;
- `python -m py_compile skills/cogentnexus-openclaw/scripts/namespace_ownership.py`: pass;
- baseline consistency: pass;
- `git diff --check`: pass.

The v2 candidate fingerprint remained unchanged from Task 094, proving digest framing and package ownership semantics were preserved:

```text
df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4
```

Canonical file count remained `176`.

## npm package-set equivalence

The canonical enumerator and actual `npm pack --dry-run --json --ignore-scripts` path sets remained exactly equal:

- Node 24.18.0 / npm 11.16.0: `176` packed, `176` canonical, missing `[]`, extra `[]`;
- Node 22.23.2 / npm 12.0.2: `176` packed, `176` canonical, missing `[]`, extra `[]`.

No tarball container bytes were used as fingerprint authority.

## Node/plugin verification

Node 24.18.0 / npm 11.16.0:

- clean `npm ci --ignore-scripts`: exit `0`;
- full plugin suite: `49 files`, `257 tests passed`;
- `npm run plugin:validate`: exit `0`;
- build, schema, bootstrap and package-content verification: pass;
- packed file count: `176`.

Node 22.23.2 / npm 12.0.2 isolated execution path:

- clean `npm ci --ignore-scripts`: exit `0`;
- full plugin suite: `49 files`, `257 tests passed`;
- `npm run plugin:validate`: exit `0`;
- build, schema, bootstrap and package-content verification: pass;
- packed file count: `176`.

Task-093 Dashboard verified-delivery/re-registration tests remained green in both plugin runs.

## Publication fence

Source/tests implementation commit was pushed first:

```text
32212a4331e1f32b5a130bd30d271d4cbc56f6c1
```

This report is the only file intended for the report-only publication commit.

The next allowed successor gate is independent acceptance of:

```text
PASS_WINDOWS_REPARSE_POINT_PAYLOAD_ATTESTATION_REPAIRED
```

Only that acceptance may authorize the next one-shot supported live install-over. Task 095 itself performed zero live mutation and sent zero semantic/provider messages.
