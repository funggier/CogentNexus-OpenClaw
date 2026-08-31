# CNX-20260828-113 — Interrupted Re-entry Conflicting-Wrapper Matrix Closure

## Verdict

`PASS` — source-only TDD repair completed and published. No live Windows lifecycle mutation was performed or authorized.

## Reconciliation and boundary

- Task 113 was confirmed `READY_FOR_HERMES / SOURCE_ONLY_TDD` in both authoritative coordination files.
- Starting reconciled HEAD: `1896050d73b69b722eb8d6ad46a88e6269c1eed9`.
- Task-112 candidate `023be1a8075c0aa602adda357db9924c170ffb8e` and artifact `9684336683` were historical evidence only.
- No install-over/reset/uninstall/reinstall/recovery replay, manual cleanup, live state/config/SQLite/session mutation, credential access, process kill, reboot, merge, tag, release, or force push was performed.

## Root cause

Task 112 proved the storage boundary of the active replacement, but it did not prove that all other CogentNexus-specific OpenClaw storage evidence was absent or attributable to that same replacement. A separate wrapper declaring the CogentNexus package, without an exact child payload, was therefore ignored by the re-entry shortcut.

This caused both production-shaped states to be incorrectly accepted:

- exact canonical direct extension plus a separate shared wrapper;
- exact managed npm replacement plus a separate shared wrapper.

## Separate test-only RED matrix commit

- Matrix RED commit: `fe72982c89c10dfd5fbc447c89d6bfc827e68e61`
- Changed file in the RED commit: `tests/test_plugin_generation_rollover.py` only
- Exact RED command:

```text
uv run --no-project --with pytest python -m pytest tests/test_plugin_generation_rollover.py -k 'conflicting_wrapper or direct_extension_without_conflict or interrupted_rollover_reentry' -q
```

- Exact result: `2 failed, 5 passed, 33 deselected`
- Both failures were semantic `Failed: DID NOT RAISE RuntimeError` results for direct-active and managed-active replacement plus a separate conflicting wrapper.
- No production file changed in this RED commit.

The same test-only commit also added explicit direct canonical success coverage and retained the existing direct classification surface for fingerprint mismatch, altered retired path, and prior re-entry cases. Existing direct ownership/installer tests cover the remaining matrix dimensions (duplicate/ambiguous candidates, non-unique registration, out-of-bound root, identity/package/version, controller mode, manifest metadata, missing skill/launcher, and mixed namespace).

## Minimal production repair

- Production fix commit: `d8c5f5f5e7936e673a6731f5a8a0f17e7bd39a06`
- Modified production file: `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`

The re-entry shortcut now obtains all product evidence through `product_plugin_inventory(...)` after proving the active storage shape. It permits only:

- direct active root: `{directPlugin}`;
- managed active child: `{npmPackage:<active-project>, npmWrapper:<active-project>}`.

Any additional direct extension, product package, or product wrapper evidence raises a fail-closed ambiguity error. The fix reuses the existing strict wrapper proof and does not delete or normalize conflicting state, weaken payload/manifest/containment checks, change Task-110 finalization, or re-enable redundant external installation.

## GREEN and full validation

```text
uv run --no-project --with pytest python -m pytest tests/test_plugin_generation_rollover.py -k 'interrupted_reentry or interrupted_rollover_reentry' -q
7 passed, 33 deselected in 0.46s

uv run --no-project --with pytest python -m pytest tests/test_plugin_generation_rollover.py tests/test_namespace_ownership.py tests/test_installer_transaction_wiring.py tests/test_namespace_install_contract.py tests/test_fresh_install_transaction_recovery.py tests/test_fresh_transaction_failure_coverage.py tests/test_npm_pack_installer_boundary.py -q
134 passed, 1 skipped in 9.34s

uv run --no-project --with pytest --with 'PyYAML>=6,<7' python -m pytest -q
431 passed, 3 skipped, 4 subtests passed in 77.40s

python -m py_compile skills/cogentnexus-openclaw/scripts/namespace_ownership.py
exit 0

powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/analyze-installer-lifecycle-ast.ps1 -Installer scripts/install.ps1
exit 0

npm ci
completed successfully

npm run plugin:validate
completed successfully; mixed-plugin artifact verification PASS (45 config properties, 5 tools); ticket DB bootstrap PASS (9 required tables + v095 registration fence); packedFileCount 178

git diff --check
passed
```

Action resolver remained exact for valid re-entry:

```json
{"mode":"upgrade","pendingRollover":false,"pluginAlreadyExact":true,"skipPlugin":false,"installPlugin":false,"rolloverPlugin":false}
```

## Exact same-source CI and attempt history

Exact candidate: `d8c5f5f5e7936e673a6731f5a8a0f17e7bd39a06`.

First CI attempt was successful for both smoke workflows and all Validate jobs except Windows npm tests, where an existing TypeScript test timed out at 15 seconds. All other jobs passed. The failed Validate workflow was rerun without source changes; the rerun passed. This is recorded as test-timing flakiness, not masked as a source failure.

Authoritative final workflow state, all on the exact candidate SHA:

| Workflow | Run ID | Final result |
|---|---:|---|
| Validate | `33170454396` | `completed / success` on rerun |
| Windows Installer Pack Smoke | `33170454132` | `completed / success` |
| PS5.1 Acceptance Smoke | `33170454130` | `completed / success` |

Job-level verification showed all Validate matrix jobs, package dry-run, Windows `npm-pack`, and PS5.1 serializer successful on the final attempt.

## New package proof

A new artifact was obtained from this exact candidate; Task-112 artifact `9684336683` was not reused:

- Artifact ID: `9685376213`
- Artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-d8c5f5f5e7936e673a6731f5a8a0f17e7bd39a06`
- Outer artifact ZIP SHA256: `20b0c096061363509045d7c93dad97068a2c3cae084fd2ba54c7e9e9a0b57731`
- Inner v0.9.3 ZIP SHA256: `76b363dbb7ab49137d4335e5c08ee7d381fea06f4ed265743d2482708b151499`
- tar.gz SHA256: `32627e56a411092e03b74017741ba714d9f801843205e2bb0a902fe084b616dd`
- `PACKAGE_IDENTITY.json` source commit: `d8c5f5f5e7936e673a6731f5a8a0f17e7bd39a06`
- Package version: `0.9.3`
- Payload file count: `178`
- Payload V2 fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- `PAYLOAD_IDENTITY.json` and `SHA256SUMS.txt` agree with the package identity and archive hashes.

Packaged-source inspection confirmed the conflicting product-evidence rejection, strict active wrapper proof, Task-110 `retiredProjectTreeSha256` proof, exact required local install command `openclaw plugins install $packagePath --force`, and recovery harness blob `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`.

## Residual uncertainty and stop gate

This proves source behavior, direct/managed conflict handling, full local validation, exact same-source CI, and package provenance. It does not prove that historical Task-107 residue remains on the live Windows machine and does not authorize live re-entry. Any future live action requires a separate task and fresh read-only preflight.

Per the coordination contract, stop after publishing this report for independent ChatGPT review. Do not create or execute a live-Windows acceptance task.
