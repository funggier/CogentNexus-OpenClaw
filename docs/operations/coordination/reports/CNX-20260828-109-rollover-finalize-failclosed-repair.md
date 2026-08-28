# CNX-20260828-109 — Rollover Finalize Fail-Closed Repair

## Verdict

`PASS` — source-only TDD repair completed and verified. No live Windows lifecycle action was performed or authorized.

## Scope and safety boundary

Executed only the authorized `SOURCE_ONLY_TDD` task on branch `agent/v0.9.3-full-stabilization`. No install-over, reset, uninstall, reinstall, stop/start/restart, recovery replay, Dashboard semantic Send, live SQLite/config mutation, credential access, process kill, reboot, merge, tag, release, or force push was performed.

## Reconciliation

- Active task: `CNX-20260828-109`
- Authoritative files confirmed:
  - `docs/operations/coordination/ACTIVE.md`
  - `docs/operations/coordination/STATUS.md`
- Predecessor reviewed: Task 108 report and independent review.
- Reviewed Task-108 descendant: `dc5e7a87867d03501b80b662e11aeaab833e0280`
- Current production drift before editing: none beyond the authorized Task-109 source/test work.

## Root cause

`finalize_plugin_rollover_transaction` wrote the replacement ownership manifest and then performed final verification. When that verification failed after the external OpenClaw install had already removed the retired generation, the exception handler restored `manifestBefore`. That could durably reassert ownership of a plugin path that no longer existed, violating the fail-closed invariant.

## RED evidence

A production-shaped regression was added in `tests/test_plugin_generation_rollover.py` and executed before the production change. It modeled:

1. a valid old manifest-owned generation;
2. successful rollover preparation and backup proof;
3. external removal of the old generation;
4. replacement finalization reaching the manifest commit path;
5. injected final verification failure;
6. assertion that the stale old ownership claim must not be restored.

The pre-fix run exited non-zero (`2 failed, 29 deselected` in the transaction-focused RED run), demonstrating the real semantic failure rather than a string-order-only failure: the old implementation restored the pre-mutation manifest even though the retired project had been removed.

## Minimal fix

Changed only:

- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`
- `tests/test_plugin_generation_rollover.py`

In `finalize_plugin_rollover_transaction` failure handling:

- if the retired project still exists, the prior manifest may be restored;
- if the retired project no longer exists, the normal ownership manifest is removed instead of being restored to the missing path;
- the operation remains non-zero/fail-closed;
- replacement ownership is not reported successful when final verification fails;
- transaction backup/evidence remains available for later authorized recovery;
- the external OpenClaw install is not rerun.

## GREEN validation

Exact commands and observed results:

```text
uv run --no-project --with pytest python -m pytest tests/test_plugin_generation_rollover.py -k 'rollover_transaction or final_verification_failure' -q
3 passed, 29 deselected in 0.28s

uv run --no-project --with pytest python -m pytest tests/test_plugin_generation_rollover.py tests/test_installer_transaction_wiring.py tests/test_namespace_install_contract.py tests/test_npm_pack_installer_boundary.py tests/test_fresh_transaction_failure_coverage.py -q
71 passed in 7.88s

uv run --no-project --with pytest --with 'PyYAML>=6,<7' python -m pytest -q
423 passed, 3 skipped, 4 subtests passed in 78.46s

npm ci
completed successfully

npm run plugin:validate
completed successfully; mixed-plugin artifact verification PASS (45 config properties, 5 tools); ticket DB bootstrap PASS (9 required tables + v095 registration fence); packedFileCount 178

git diff --check
passed
```

The targeted regression and all Task-108 prepare/finalize, rollover, installer wiring, namespace, npm-12 local-archive, and fresh transaction coverage passed.

## Exact candidate and publication

- Branch: `agent/v0.9.3-full-stabilization`
- Exact source candidate: `dcca49d43d95a0a34d8d460a4b9ab5ad88d036ce`
- Published by non-force push; remote HEAD was verified equal to this SHA.
- Commit: `fix: fail closed after rollover verification failure`

## Exact GitHub Actions evidence

All required workflows completed successfully for the exact candidate SHA:

| Workflow | Run ID | Conclusion |
|---|---:|---|
| Validate | `33160761306` | `success` |
| Windows Installer Pack Smoke | `33160761364` | `success` |
| PS5.1 Acceptance Smoke | `33160761392` | `success` |

Validate job-level results were all successful, including Ubuntu, macOS, Windows, Python 3.11/3.14, and package dry-run jobs. Windows Installer Pack Smoke's `npm-pack` job and PS5.1 Acceptance Smoke's serializer job were successful.

## New package proof

New artifact; Task-108 artifact `9680707129` was not reused:

- Artifact ID: `9681526010`
- Artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-dcca49d43d95a0a34d8d460a4b9ab5ad88d036ce`
- Outer artifact ZIP SHA256: `f68fc895dfd5e8a12b9ab98e0681e2ebd1e8a7e18018edcfcc61c18728ea0436`
- `cogentnexus-openclaw-v0.9.3.zip` SHA256: `9773d5d2b0b2a906a7300b1e09f5ac2a9412f8815566e976e1cc3dcb296d4575`
- `cogentnexus-openclaw-v0.9.3.tar.gz` SHA256: `bee99e7d600d2946309d8f363dd7dd1fab6737f441d3f927635191798b4a1d30`
- `PACKAGE_IDENTITY.json` source commit: `dcca49d43d95a0a34d8d460a4b9ab5ad88d036ce`
- Package version: `0.9.3`
- Payload file count: `178`
- Payload V2 fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- `PAYLOAD_IDENTITY.json` agrees with the same count, version, and fingerprint.
- `SHA256SUMS.txt` agrees with both archive hashes.

Packaged source inspection confirmed that the package retains the local archive invocation `openclaw plugins install $packagePath --force` and the `rollover-prepare` / `rollover-finalize` transaction contract in the packaged installer/ownership sources. The packaged recovery harness is present and its source Git blob identity is `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`.

## Residual uncertainty

This report proves source behavior, repository validation, exact same-source CI, and new package provenance only. It does not prove a live Windows install-over or lifecycle acceptance; those actions remain outside Task 109 scope and require a separately reviewed and explicitly authorized task.

Per the coordination contract, stop here for independent ChatGPT review. Do not create or execute the next live acceptance task.
