# Active Coordination

Status: `COMPLETE`
State: `CNX447_V098_RELEASE_GREEN`
Task: `CNX-20260925-447-v098-release-preparation-and-publication.md`
Assigned executor: `ChatGPT`
Review owner: `ChatGPT independent final verification`
Human final authority: `Operator`
Working branch: `cnx-447-v098-release-preparation`
Target release: `v0.9.8`
Production-code authority: `b908efe9f82550bc3cc071ad24c0f2d1d41cc4ec`

## Accepted predecessor

Task 446 is COMPLETE/PASS.

The Dashboard Direct terminal-final defect is repaired and independently live-qualified on OpenClaw 2026.9.5. The accepted production behavior preserves native Ollama fallback and includes the two installer compatibility repairs discovered during real install-over qualification.

## Current live baseline

- exact production-code candidate: `b908efe9f82550bc3cc071ad24c0f2d1d41cc4ec`;
- exact-SHA Validate / PS5.1 Acceptance Smoke / Windows Installer Pack Smoke: GREEN;
- real exact-candidate install-over: PASS, exit 0;
- Host: active, generation 30, provider ownership OpenClaw;
- plugin: enabled / activated / loaded, diagnostics empty;
- Gateway: OpenClaw 2026.9.5, HTTP 200, native connectivity healthy;
- runtime attestation: `runnerReady=true`, `globalHookCount=7`;
- v092 supervisor: Ready / Enabled / Hidden / `LastTaskResult=0`;
- Ticket DB: no non-terminal Tickets, zero outbox rows;
- installed/source Host and terminal-boundary dist SHA-256 parity: PASS;
- fresh post-install Codex run `cnx446-live-codex-c-send-v1`: terminal-boundary GREEN;
- native Ollama run `cnx446-ollama-live-a`: GREEN.

## Current objective

Prepare a coherent v0.9.8 release candidate from the accepted Task 446 production behavior, requalify the exact release SHA, publish only through the repository release workflow, independently verify public artifacts/checksums, and converge `main` without rewriting v0.9.7.

## Local release-candidate preparation

Stage 1-3 local preparation is GREEN:

- public v0.9.7/tag identity re-proven unchanged;
- release workflow/package/checksum contract audited;
- v0.9.8 metadata/docs/release notes aligned;
- dependency lifecycle suppression extended across candidate-preparation surfaces;
- focused contracts: 40/40 PASS;
- full Python: 745 passed, 5 skipped, 38 subtests;
- Vitest: 93 files / 436 tests PASS;
- evaluation / production audit / plugin validation: PASS;
- PowerShell / PS5.1 / POSIX syntax gates: PASS;
- payload identity: `173d6f95de3d5eaef420b47faf27d0d98f52190e570b8109dcc49f078423f9c0` / 294 files;
- `git diff --check`: PASS.

## Pre-publication authority

Exact release candidate: `4f9b07d6e29e2051a44d2681cce0f8ecf5f47037`.

Completed:

- no-force push and local/remote SHA equality: PASS;
- Validate `36144053827`: SUCCESS;
- PS5.1 Acceptance Smoke `36144053553`: SUCCESS;
- Windows Installer Pack Smoke `36144053896`: SUCCESS;
- real v0.9.7 -> v0.9.8 install-over: PASS / exit 0;
- installed/source payload parity: PASS, 294 files, fingerprint `173d6f95de3d5eaef420b47faf27d0d98f52190e570b8109dcc49f078423f9c0`;
- runtime/plugin/Gateway/supervisor/Ticket health: PASS;
- fresh Codex progress -> tool -> terminal acceptance: PASS;
- clean-reinstall/reset baseline review: no additional destructive cycle required.

## Publication result

- accepted Release run: `36159455993` — SUCCESS;
- tag `v0.9.8` -> exact candidate `4f9b07d6e29e2051a44d2681cce0f8ecf5f47037`;
- public/non-draft/non-prerelease: PASS;
- independent TAR/ZIP/SHA256SUMS verification: PASS;
- v0.9.7 immutability re-proven.

The earlier run `36159246629` was cancelled before publication because it executed the stale default-branch workflow definition.

## Main convergence checkpoint

Post-release docs commit `8d2204a6f1f0978873ef6c00bc3035cf3e664dc6` was pushed and `main` was fast-forwarded without force from `17e60d1f53fce4f37c7bc8cbec6ccb6bca14222e`.

Independent verification after the fast-forward:

- remote `main` = `8d2204a6...`;
- public README/CURRENT_STATE/v0.9.8 release notes read from `main` show the published v0.9.8 authority correctly;
- live ownership/plugin = `0.9.8`;
- controller = active/MANAGED generation 32;
- Gateway OpenClaw 2026.9.5 connectivity = healthy;
- plugin = enabled/loaded, diagnostics empty;
- runtime runner ready / global hooks 7;
- supervisor = Ready/Enabled/Hidden / `LastTaskResult=0`;
- SQLite integrity = `ok`, non-terminal Tickets 0, pending outbox 0.

Main Validate run `36160610790` then exposed a docs-contract-only regression: `tests/test_install_docs_authority.py` still parsed the old pre-publication section heading `Development-candidate source install`. The public docs had correctly changed that heading to `Exact release/source-tree install`.

The contract was updated to parse the published heading. Post-repair proof:

- focused docs/release contract suite: `15 passed`;
- full Python suite: `745 passed, 5 skipped, 38 subtests passed`;
- no production/runtime/workflow source changed.

## Final closeout

Post-release docs-contract repair commit:

`af90ff5c3259f2fb82228a1089f20cafe62cecc2`

Branch exact-SHA gates:

- Validate `36162086121` — SUCCESS;
- PS5.1 Acceptance Smoke `36162086188` — SUCCESS;
- Windows Installer Pack Smoke `36162086282` — SUCCESS.

`main` was fast-forwarded without force from `8d2204a6...` to the same exact repair SHA.

Main exact-SHA gates:

- Validate `36163150015` — SUCCESS;
- PS5.1 Acceptance Smoke `36163150106` — SUCCESS;
- Windows Installer Pack Smoke `36163150135` — SUCCESS.

No production/runtime/workflow source changed in the repair. The immutable v0.9.8 release tag remains `4f9b07d6e29e2051a44d2681cce0f8ecf5f47037`; v0.9.7 remains unchanged.

CNX-447 is complete.

## Safety boundary

Any production-code change beyond release/version metadata reopens semantic/live qualification. v0.9.7 is immutable.
