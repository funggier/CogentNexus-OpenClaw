# CNX-20260828-110 — Rollover Retired-State Exactness Repair

## Verdict

`PASS` — source-only TDD repair completed and verified. No live Windows lifecycle mutation was performed or authorized.

## Reconciliation and scope

- Remote branch: `agent/v0.9.3-full-stabilization`
- Reconciled remote HEAD before editing: `07d7147bd363ad49147661544b26cd742490b321`
- `ACTIVE.md` and `STATUS.md` both authorized `CNX-20260828-110` as `READY_FOR_HERMES / SOURCE_ONLY_TDD`.
- Diff from the Task-109 report boundary `2b198632bc2cbe7b485ce56e0ac046b0ceb545e7` to the reconciled HEAD contained only the four stated coordination files: `ACTIVE.md`, `STATUS.md`, the Task-109 review, and the Task-110 task specification. No unexplained production drift was present.
- No install-over, reset, uninstall, reinstall, lifecycle/recovery replay, Dashboard semantic Send, live SQLite/config mutation, credential access, process kill, reboot, merge, tag, release, or force push was performed.

## Root cause

Task 109 changed finalization so a missing retired project caused the normal ownership manifest to be quarantined. However, it still restored `manifestBefore` whenever `retiredProjectRoot.exists()` was true. A retired directory can remain present while its payload/tree has been altered, partially removed, replaced, or otherwise no longer matches the exact pre-mutation state proved by `rollover-prepare`. Restoring `manifestBefore` in that state reasserts ownership without re-proving the generation that manifest describes.

## Separate RED commit and evidence

The required test-only RED commit was pushed before any production edit:

- RED commit: `edec90ac455cf3cf6b3b9842e5ca3fe5c0014338`
- Test changed: `tests/test_plugin_generation_rollover.py`
- Exact RED command:

```text
uv run --no-project --with pytest python -m pytest tests/test_plugin_generation_rollover.py -k 'altered_retired_manifest' -q
```

- Exact result: `1 failed, 32 deselected in 0.79s`
- Failing assertion: `assert not manifest_path.exists()`
- Failure observed: the current implementation restored `manifestBefore`, leaving `ownership.json` present, even though the retired directory remained but its owned `dist/ticket-store.js` payload file had been removed after transaction preparation.

This was a real semantic boundary test: valid old ownership was prepared and backed up, the retired tree was altered while its path remained, replacement finalization reached the replacement manifest commit path, final verification was injected to fail, and the stale old manifest was incorrectly restored by the pre-fix implementation.

## Minimal production repair

Production fix commit, pushed separately after RED verification:

- Fix commit: `25d229cd496a11af37ea2ff556a0126dfc194377`
- File changed: `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`

The exception path now restores `manifestBefore` only when both exact proofs succeed:

1. `_project_tree_sha256(retiredProjectRoot)` equals the transaction's recorded `retiredProjectTreeSha256`;
2. the retired plugin payload fingerprint equals the transaction's recorded `retiredFingerprint`.

If the retired path is missing, altered, incomplete, foreign, or cannot be re-proved, the normal ownership manifest is quarantined/removed instead. The operation remains non-zero, replacement ownership is not declared successful, backup evidence remains durable, and the external install is never rerun.

## GREEN validation

Exact observed results:

```text
uv run --no-project --with pytest python -m pytest tests/test_plugin_generation_rollover.py -k 'altered_retired_manifest or does_not_restore_missing_retired_manifest or apply_rolls_back_project_and_manifest_when_final_verification_fails' -q
3 passed, 30 deselected in 0.30s

uv run --no-project --with pytest python -m pytest tests/test_plugin_generation_rollover.py tests/test_installer_transaction_wiring.py tests/test_namespace_install_contract.py tests/test_npm_pack_installer_boundary.py tests/test_fresh_transaction_failure_coverage.py -q
72 passed in 8.18s

uv run --no-project --with pytest --with 'PyYAML>=6,<7' python -m pytest -q
424 passed, 3 skipped, 4 subtests passed in 76.08s

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

The targeted set includes both required failure cases (retired project absent and retired project present but altered) plus the valid exact rollback case, and all prior rollover/installer/namespace/npm-12/fresh-transaction protections remained green.

## Exact candidate and CI

- Exact candidate source: `25d229cd496a11af37ea2ff556a0126dfc194377`
- Remote HEAD was verified equal to the candidate before CI evidence collection.

All required workflows completed successfully for this exact SHA:

| Workflow | Run ID | Conclusion |
|---|---:|---|
| Validate | `33164787392` | `success` |
| Windows Installer Pack Smoke | `33164787432` | `success` |
| PS5.1 Acceptance Smoke | `33164787396` | `success` |

Job-level verification also showed all Validate matrix jobs and package dry-run successful, the Windows `npm-pack` job successful, and the PS5.1 serializer job successful.

## New package proof

A new artifact was obtained from the exact candidate; Task-109 artifact `9681526010` was not reused:

- Artifact ID: `9683127656`
- Artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-25d229cd496a11af37ea2ff556a0126dfc194377`
- Outer artifact ZIP SHA256: `90a9e329c040312ded336de4c7dd6f81b1c546aceb7869d6d284a119d7a87b25`
- Inner `cogentnexus-openclaw-v0.9.3.zip` SHA256: `898413145589f4faede6cb04f3d478b956ab83492942747467ca674f13b890e3`
- `cogentnexus-openclaw-v0.9.3.tar.gz` SHA256: `b6a6056bb3d2472531000c1212621c878269a6f4f5d583164a3fb280c65ac047`
- `PACKAGE_IDENTITY.json` source commit: `25d229cd496a11af37ea2ff556a0126dfc194377`
- Package version: `0.9.3`
- Payload file count: `178`
- Payload V2 fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- `PAYLOAD_IDENTITY.json` agrees on version, count, and fingerprint.
- `SHA256SUMS.txt` agrees with both archive hashes.

Packaged source inspection confirmed:

- `scripts/install.ps1` retains `openclaw plugins install $packagePath --force`;
- packaged installer retains `rollover-prepare` and `rollover-finalize`;
- packaged `namespace_ownership.py` contains the exact retired-tree/fingerprint fail-closed repair (`retiredProjectTreeSha256` and `retiredFingerprint` checks);
- recovery harness is present with Git blob SHA `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`.

## Publication

This report is the only file in the report publication commit and must be pushed to:

`docs/operations/coordination/reports/CNX-20260828-110-rollover-retired-state-exactness-repair.md`

## Residual uncertainty

This proves source behavior, test/validation results, exact same-source CI, and package provenance only. It does not prove live Windows install-over or lifecycle acceptance. Those actions remain outside Task 110 scope and require a separately reviewed and explicitly authorized task.

Per the coordination contract, stop after publishing this report for independent ChatGPT review. Do not create or execute a live-Windows acceptance task.
