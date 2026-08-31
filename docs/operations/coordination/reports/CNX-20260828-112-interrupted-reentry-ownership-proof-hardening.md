# CNX-20260828-112 — Interrupted Re-entry Ownership-Proof Hardening

## Verdict

`PASS` — source-only TDD repair completed, validated, and published. No live Windows lifecycle mutation was performed or authorized.

## Reconciliation and safety boundary

- Remote coordination branch was reconciled before editing.
- `ACTIVE.md` and `STATUS.md` both authorized Task `CNX-20260828-112` as `READY_FOR_HERMES / SOURCE_ONLY_TDD`.
- Reconciled starting HEAD: `00aa1413397604f31c4d24582cece3225128b491`.
- Task-111 candidate `f4c8c993be80eaf54468f5b2630fd107050a1385` and artifact `9683680142` were treated as historical evidence only.
- No real-Windows install-over/reset/uninstall/reinstall/recovery replay, manual cleanup, live SQLite/config/session mutation, credential access, process kill, reboot, merge, tag, release, or force push was performed.

## Root cause

Task 111 added a narrow interrupted-rollover re-entry shortcut for the state where the old manifest-owned plugin path is missing and one exact replacement is active. The shortcut proved the child payload, active registration, containment, candidate count, and candidate fingerprint, but did not prove the replacement's storage/ownership boundary.

For an OpenClaw npm-project replacement, an exact CogentNexus child payload could therefore be accepted inside a foreign/shared wrapper containing unrelated dependency evidence. This violated the no-generic-adoption and no-shared-wrapper invariant.

## Separate RED commit and semantic failure

The mandatory test-only RED commit was pushed before production edits:

- RED commit: `bb8212584b1b7934cc2d9e1d7bc6b5e0303699f2`
- Test file: `tests/test_plugin_generation_rollover.py`
- Exact RED command:

```text
uv run --no-project --with pytest python -m pytest tests/test_plugin_generation_rollover.py -k 'foreign_shared_wrapper' -q
```

- Exact result: `1 failed, 36 deselected`
- Semantic failure: `Failed: DID NOT RAISE RuntimeError`

The fixture modeled a coherent Task-107-shaped interrupted state, removed the old manifest-owned npm generation, kept one exact active replacement child, then added `foreign-user-package` to the replacement wrapper's `package.json`. Task 111 incorrectly returned the successful re-entry classification instead of rejecting the foreign/shared wrapper.

## Minimal production repair

- Production fix commit: `023be1a8075c0aa602adda357db9924c170ffb8e`
- Modified production file: `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`

After the existing exact active child payload and candidate-count checks, the shortcut now proves the active storage boundary:

1. The active root is accepted directly only when it equals the exact canonical path `<openclaw-state>/extensions/cogentnexus-openclaw`.
2. Otherwise, it must be an exact npm-project child accepted by `_npm_project_for_plugin(...)`.
3. `_npm_project_for_plugin(...)` reuses `_managed_wrapper_proof(...)`, preserving all existing wrapper checks for project naming, package fields, dependency ownership, OpenClaw metadata, overrides, lockfile binding, and exact package/version.
4. Any other contained-but-noncanonical root fails closed with no mutation.

The fix does not weaken the wrapper contract, change Task-111's missing-retired-path requirement, alter candidate attestation/uniqueness, or change Task-110 finalization checks.

## GREEN targeted validation

Exact observed results:

```text
uv run --no-project --with pytest python -m pytest tests/test_plugin_generation_rollover.py -k 'interrupted_rollover_reentry' -q
4 passed, 33 deselected in 0.28s

uv run --no-project --with pytest python -m pytest tests/test_plugin_generation_rollover.py tests/test_namespace_ownership.py tests/test_installer_transaction_wiring.py tests/test_namespace_install_contract.py tests/test_fresh_install_transaction_recovery.py tests/test_fresh_transaction_failure_coverage.py tests/test_npm_pack_installer_boundary.py -q
131 passed, 1 skipped in 9.10s

python -m py_compile skills/cogentnexus-openclaw/scripts/namespace_ownership.py
exit 0

git diff --check
passed
```

The focused re-entry matrix explicitly covered the valid exact direct/replacement path, foreign/shared wrapper rejection, candidate fingerprint mismatch, and altered-retired-path non-shortcut behavior. Existing related contract tests cover duplicate/ambiguous candidates, non-unique registrations, out-of-bound roots, wrong identity/version, controller mode, manifest metadata, missing skill/launcher, and mixed legacy/new state.

Action resolver proof remained:

```json
{"mode":"upgrade","pendingRollover":false,"pluginAlreadyExact":true,"skipPlugin":false,"installPlugin":false,"rolloverPlugin":false}
```

## Full repository validation

```text
uv run --no-project --with pytest --with 'PyYAML>=6,<7' python -m pytest -q
428 passed, 3 skipped, 4 subtests passed in 79.63s

powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/analyze-installer-lifecycle-ast.ps1 -Installer scripts/install.ps1
exit 0

npm ci
completed successfully

npm run plugin:validate
completed successfully; mixed-plugin artifact verification PASS (45 config properties, 5 tools); ticket DB bootstrap PASS (9 required tables + v095 registration fence); packedFileCount 178

git diff --check
passed
```

## Exact same-source CI proof

- Exact candidate SHA: `023be1a8075c0aa602adda357db9924c170ffb8e`
- All three required workflows were run on this exact SHA.

The first Validate run had an unrelated Windows-only timing/flakiness failure in existing TypeScript tests (`ticket-runtime` 20-second timeout and `evaluation` assertion), while the other Validate matrix jobs and both smoke workflows passed. Local Windows `npm test` then passed all `50` test files and `268` tests, including both failing cases. The failed Validate workflow was rerun without changing source or rerunning lifecycle operations.

Authoritative final rerun state:

| Workflow | Run ID | Conclusion |
|---|---:|---|
| Validate | `33167878659` | `completed / success` |
| Windows Installer Pack Smoke | `33167878626` | `completed / success` |
| PS5.1 Acceptance Smoke | `33167878630` | `completed / success` |

Job-level verification showed every Validate matrix job and package dry-run successful, Windows `npm-pack` successful, and PS5.1 serializer successful.

## New package proof

A new artifact was obtained from the exact candidate; Task-111 artifact `9683680142` was not reused:

- Artifact ID: `9684336683`
- Artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-023be1a8075c0aa602adda357db9924c170ffb8e`
- Outer artifact ZIP SHA256: `2be47e00db355be28a782096bd1ab866c787b768f8eb0c3ecaa131a3802e91bf`
- Inner v0.9.3 ZIP SHA256: `2240348a163c356fc7958c04f645b9a1f406db6c842fdbd86b4dd3efdeecc8c5`
- tar.gz SHA256: `b6433b4a6c3d91a6185b3048146243b079b66015d5f7a76564ddf726fc4e81e0`
- Source commit in `PACKAGE_IDENTITY.json`: `023be1a8075c0aa602adda357db9924c170ffb8e`
- Package version: `0.9.3`
- Payload file count: `178`
- Payload V2 fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- `PAYLOAD_IDENTITY.json` and `SHA256SUMS.txt` agree with the identity and archive hashes.

Packaged-source inspection confirmed:

- strict `_npm_project_for_plugin` and `_managed_wrapper_proof` are present;
- the interrupted re-entry storage-ownership rejection is packaged;
- Task-110 `retiredProjectTreeSha256` exactness remains packaged;
- installer retains `openclaw plugins install $packagePath --force` when installation is actually required;
- recovery harness Git blob remains `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`.

## Residual uncertainty and stop gate

This proves source behavior, focused negative coverage, full local validation, exact same-source CI, and new package provenance. It does not prove the current live Windows machine still has the historical Task-107 residue or authorize a live re-entry. Any future live operation requires a separate authorized task and fresh read-only machine preflight.

Per the coordination contract, stop after publishing this report for independent ChatGPT review. Do not create or execute a live Windows acceptance task.
