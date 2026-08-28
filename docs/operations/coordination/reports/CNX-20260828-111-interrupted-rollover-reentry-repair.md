# CNX-20260828-111 — Interrupted Rollover Re-entry Repair

## Verdict

`PASS` — source-only TDD repair completed and verified. No live Windows lifecycle mutation was performed or authorized.

## Reconciliation and safety boundary

- Remote branch was reconciled before editing.
- Task `CNX-20260828-111` was confirmed active in both `ACTIVE.md` and `STATUS.md` as `READY_FOR_HERMES / SOURCE_ONLY_TDD`.
- Reconciled remote HEAD before editing: `00aa1413397604f31c4d24582cece3225128b491`.
- The Task-110 accepted source boundary was `25d229cd496a11af37ea2ff556a0126dfc194377`; no unexplained production drift was present before this task.
- No real-Windows install-over, reset, uninstall, reinstall, lifecycle/recovery replay, live SQLite/config mutation, Dashboard semantic Send, credential access, process kill, reboot, merge, tag, release, or force push was performed.

## Root cause and Task-107-shaped reproduction

The preserved Task-107 boundary has a normal ownership manifest whose `pluginPath` points to the previous managed npm generation. The external local archive install had already removed that generation and registered the replacement before the old rollover operation failed.

At the accepted source boundary, `recovery_preflight()` returned `OWNERSHIP_PRESENT` whenever the normal manifest existed. Attested `classify_install()` then called `verify_manifest()` with `require_artifacts=True`, which required the missing manifest-owned plugin path and failed closed before the rollover/action logic could determine that an exact replacement was already active.

The missing capability was a narrow re-entry classification, not generic partial-state adoption.

## Separate RED commit and evidence

The required test-only RED commit was pushed before production edits:

- RED commit: `a7dace1ed86580c6ab39d72283eace3d7e76a02d`
- Test file: `tests/test_plugin_generation_rollover.py`
- Exact RED command:

```text
uv run --no-project --with pytest python -m pytest tests/test_plugin_generation_rollover.py -k 'interrupted_rollover_reentry_classifies_exact_active_replacement' -q
```

- Exact result: `1 failed, 35 deselected`
- Exact failure boundary: `verify_manifest(... require_artifacts=True)` raised `RuntimeError: owned installation is incomplete; refusing mutation` because the manifest-owned old plugin path was missing.

The RED fixture modeled a coherent old manifest, one exact active replacement, removal of the old managed npm generation while preserving the manifest and non-plugin owned artifacts, and actual attested classification. It failed because the current source could not safely classify the valid interrupted-rollover state.

## Minimal production repair

Production fix commit, separate from RED:

- Fix commit: `f4c8c993be80eaf54468f5b2630fd107050a1385`
- Production file: `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`
- Related tests: `tests/test_plugin_generation_rollover.py`

Added a bounded `_classify_interrupted_rollover_reentry()` path. It is reachable only after:

1. exact manifest metadata passes with plugin artifact existence temporarily excluded;
2. controller mode is exactly `passthrough`;
3. the manifest-owned plugin path is specifically missing;
4. state root, skill identity, launcher, and other non-plugin owned artifacts remain present;
5. no legacy/mixed namespace is present;
6. `_active_registered_plugin()` proves exactly one contained canonical registration with exact id, package, version, and payload;
7. the active replacement fingerprint equals the installer-supplied candidate fingerprint;
8. exactly one canonical payload candidate exists and is the active replacement.

The result is explicit `upgrade`, `pendingRollover=False`, `pluginAlreadyExact=True`, and `interruptedRolloverReentry=True`. Existing action semantics therefore produce `installPlugin=False` and `rolloverPlugin=False`, avoiding a redundant second external install. The later existing ownership create/verify path binds the active replacement before any MANAGED authority.

Existing/altered retired paths do not enter this shortcut; they remain on normal rollover handling. Corrupt metadata, missing non-plugin artifacts, wrong controller mode, foreign/out-of-bound payloads, mismatched fingerprint, duplicate/ambiguous registrations, and mixed state remain fail-closed.

## GREEN validation

Exact observed results:

```text
uv run --no-project --with pytest python -m pytest tests/test_plugin_generation_rollover.py -k 'interrupted_rollover_reentry' -q
3 passed, 33 deselected in 0.75s

uv run --no-project --with pytest python -m pytest tests/test_plugin_generation_rollover.py tests/test_fresh_install_transaction_recovery.py tests/test_installer_transaction_wiring.py tests/test_namespace_install_contract.py tests/test_npm_pack_installer_boundary.py -q
67 passed in 6.21s

powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/resolve-plugin-lifecycle-actions.ps1 -Mode upgrade -PluginAlreadyExact
{"mode":"upgrade","pendingRollover":false,"pluginAlreadyExact":true,"skipPlugin":false,"installPlugin":false,"rolloverPlugin":false}

uv run --no-project --with pytest --with 'PyYAML>=6,<7' python -m pytest -q
427 passed, 3 skipped, 4 subtests passed

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

The targeted tests include the positive interrupted-rollover re-entry, fingerprint mismatch rejection, altered-retired-path non-shortcut behavior, prior rollover prepare/finalize/failure cases, namespace ownership, installer wiring, fresh transaction, npm-12 local archive, and action resolver coverage.

## Exact candidate and Actions proof

- Exact candidate source: `f4c8c993be80eaf54468f5b2630fd107050a1385`
- Remote HEAD was verified equal to this candidate before CI evidence collection.

All required workflows completed successfully for the exact same SHA:

| Workflow | Run ID | Conclusion |
|---|---:|---|
| Validate | `33166203340` | `success` |
| Windows Installer Pack Smoke | `33166203285` | `success` |
| PS5.1 Acceptance Smoke | `33166203316` | `success` |

Job-level verification showed all Validate matrix jobs and package dry-run successful, the Windows `npm-pack` job successful, and the PS5.1 serializer job successful.

## New package proof

A new artifact was obtained from the exact candidate. Task-110 artifact `9683127656` was not reused:

- Artifact ID: `9683680142`
- Artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-f4c8c993be80eaf54468f5b2630fd107050a1385`
- Outer artifact ZIP SHA256: `096b194423b83d14adf4dd26eb000612d53d31ef3f7f8c5385eb00e74756b422`
- Inner v0.9.3 ZIP SHA256: `9ebbaac9c222f79d2291b6dfeb54791777abe1052b9c71614a9cff21239ade2e`
- tar.gz SHA256: `503be3b917993ce3d22d5ca8f5bb8bc878eee0b8048582e52c9dd6b13c1a483e`
- `PACKAGE_IDENTITY.json` source commit: `f4c8c993be80eaf54468f5b2630fd107050a1385`
- Package version: `0.9.3`
- Payload file count: `178`
- Payload V2 fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- `PAYLOAD_IDENTITY.json` agrees on version, count, and fingerprint.
- `SHA256SUMS.txt` agrees with both archive hashes.

Packaged source inspection confirmed:

- `scripts/install.ps1` retains the exact required local archive invocation `openclaw plugins install $packagePath --force` for installation-required paths;
- installer action wiring retains `PluginAlreadyExact` and prepare/finalize rollover behavior;
- packaged ownership source contains `interruptedRolloverReentry` and the exact active replacement checks;
- Task-110 exact retired-state checks remain packaged;
- the recovery harness is present with Git blob SHA `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`.

## Residual uncertainty and stop gate

This proves source behavior, repository validation, exact same-source CI, and new package provenance only. It does not prove the live machine still has the Task-107 residue or that a live re-entry/install acceptance will succeed. Any future live task must first re-prove the machine read-only and must be separately authorized.

Per the coordination contract, stop after publishing this report for independent ChatGPT review. Do not create or execute a live Windows acceptance task.
