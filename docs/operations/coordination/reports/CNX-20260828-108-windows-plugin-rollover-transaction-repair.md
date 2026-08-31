# CNX-20260828-108 — Windows Plugin Rollover Transaction Repair

Status: `BLOCKED`

## Task and source boundary

- Task ID: `CNX-20260828-108`
- Branch: `agent/v0.9.3-full-stabilization`
- Task mode: `SOURCE_ONLY_TDD`
- Executor: Hermes/Codex
- Source candidate commit: `f034cebe5cbe94116c10a81b89c2ef30de6646a8`
- Predecessor Task-107 report commit: `582acb72dd09d1e3753452afcb5f76aa72929d5d`
- Predecessor Task-107 review commit: `b0487da1aacb5cd3663a6e7e6b2f3caed1db1ef0`

No live Windows lifecycle, OpenClaw/Ollama mutation, Dashboard semantic activity, credential access, or live runtime/config/SQLite mutation was performed.

## Root cause confirmed

Task 107 reached the repaired local archive command:

```powershell
openclaw plugins install $packagePath --force
```

OpenClaw `2026.7.1-2` can remove/replace the old plugin generation during that external mutation. The previous installer then called the ownership rollover planner, which required the old manifest-owned root to still exist and correctly failed closed with `owned installation is incomplete`.

The integration transaction therefore needed to preserve the old owned generation before the external mutation, prove the new generation afterward, and commit durable ownership only after that post-mutation proof.

## RED regression

RED commit:

`686598e68a0be7b38bf983a43e72fa163796b614`

The commit contained tests only:

- `test_rollover_transaction_survives_external_replacement_of_old_generation`
- `test_rollover_transaction_rejects_unexpected_replacement_without_commit`

The tests modelled a valid old manifest-owned generation, a separate replacement generation, removal of the old project at the external-install boundary, and the required post-install replacement proof. Before the production change, the exact targeted command failed as expected:

```text
uv run --no-project --with pytest python -m pytest tests/test_plugin_generation_rollover.py -k 'rollover_transaction' -q

2 failed, 29 deselected
AttributeError: module 'rollover_ownership' has no attribute 'prepare_plugin_rollover_transaction'
```

This was a real missing-contract failure, not a syntax or unrelated test failure.

## Minimal production fix

Implementation commit:

`f034cebe5cbe94116c10a81b89c2ef30de6646a8`

Changed files:

- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`
  - added `prepare_plugin_rollover_transaction`;
  - validates PASSTHROUGH, exact manifest/owned payload, source attestation and external backup boundary;
  - snapshots the old managed npm project before external mutation;
  - added `finalize_plugin_rollover_transaction`;
  - validates active replacement fingerprint, transaction/manifest binding and backup proof;
  - commits replacement ownership only after post-install proof and restores the prior manifest on commit verification failure;
  - added CLI `rollover-prepare` and `rollover-finalize`.
- `scripts/install.ps1`
  - resolves the exact npm pack artifact;
  - prepares the transaction before the one `openclaw plugins install $packagePath --force` call;
  - captures post-install inventory and finalizes the transaction afterward;
  - no longer invokes the old post-mutation `rollover-plan` path for this install-over boundary.
- `scripts/analyze-installer-lifecycle-ast.ps1`
  - recognizes the new transaction commands for structural lifecycle analysis.
- `tests/test_plugin_generation_rollover.py`
  - production-shaped RED/GREEN transaction tests.
- `tests/test_installer_transaction_wiring.py`
- `tests/test_namespace_install_contract.py`
  - updated structural assertions for prepare/install/finalize ordering.

The local archive invocation remains exactly:

```powershell
openclaw plugins install $packagePath --force
```

The old `npm-pack:` executable invocation was not restored.

## GREEN validation

Targeted validation:

```text
uv run --no-project --with pytest python -m pytest \
  tests/test_plugin_generation_rollover.py \
  tests/test_installer_transaction_wiring.py \
  tests/test_namespace_install_contract.py \
  tests/test_npm_pack_installer_boundary.py \
  tests/test_fresh_transaction_failure_coverage.py -q

70 passed
```

Full repository validation in an isolated environment:

```text
uv run --no-project --with pytest --with 'PyYAML>=6,<7' \
  python -m pytest -q

422 passed, 3 skipped, 4 subtests passed
```

Plugin package validation with native Node/npm PATH pinned:

```text
npm ci
npm run plugin:validate
```

Observed result: PASS. Package validation reported `packedFileCount: 178`; the local npm audit/install-script warnings were retained as warnings and were not used as a success substitute.

Additional checks:

- `git diff --check`: PASS
- PowerShell installer AST analysis: PASS through the updated transaction-aware test
- no live mutation: PASS (zero live acceptance actions were attempted)

## Exact CI gate

All runs were triggered by the exact source commit `f034cebe5cbe94116c10a81b89c2ef30de6646a8`:

| Required workflow | Run ID | Observed status | Conclusion |
|---|---:|---|---|
| Validate | `33158517228` | `in_progress` after bounded wait | unavailable |
| Windows Installer Pack Smoke | `33158517190` | `in_progress` after bounded wait | unavailable |
| PS5.1 Acceptance Smoke | `33158517168` | `completed` | `success` |

The two in-progress runs showed active steps rather than completed-but-unreported state:

- Validate remained in `pytest`/plugin validation matrix steps;
- Windows Installer Pack Smoke remained in plugin dependency installation.

The executor waited through multiple bounded windows and did not cancel or rerun these exact candidate workflows.

## Package proof

A new exact package-proof artifact identity/hashes/fingerprint could not be recorded because the required Windows Installer Pack Smoke run `33158517190` did not complete during the bounded execution windows. No prior Task-107 artifact was reused, and no locally rebuilt package was promoted as CI proof.

Therefore the following required CI/package fields remain **unproven**:

- new package-proof artifact ID and name;
- outer artifact digest/SHA256;
- inner v0.9.3 ZIP SHA256;
- tar.gz SHA256;
- CI-produced `PACKAGE_IDENTITY.json` source binding;
- CI-produced payload fingerprint attestation.

## Safety and scope confirmations

- Task-107 destructive phases were not replayed.
- No real-Windows install-over/reset/uninstall/reinstall/lifecycle/recovery was run.
- No OpenClaw or Ollama update/reinstall/uninstall was run.
- No Dashboard semantic nonce/message/Send was run.
- No credentials, tokens, passwords, private session payloads, live SQLite edits or live config edits were accessed.
- No process-tree kill, reboot, merge, tag, release publication or force push occurred.
- Source-only changes were limited to the transaction repair and directly related tests/AST contract.

## Final verdict

`BLOCKED`

The source repair is locally RED/GREEN validated and the exact candidate is pushed, but Task 108 cannot be marked PASS because two of the three mandatory exact-commit CI gates remain in progress and the new package proof is unavailable. Independent review must classify the CI stall and determine whether a newly authorized source/CI action is needed. No real-Windows acceptance task is authorized from this report.
