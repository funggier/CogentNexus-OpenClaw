# Active Coordination

Status: `IN_PROGRESS`
State: `CNX447_V098_PUBLISHED_MAIN_CONVERGENCE_PENDING`
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

## Immediate next gates

1. commit/push the post-release docs-only convergence;
2. prove current remote `main` is an ancestor of the accepted release lineage;
3. fast-forward `main` without force;
4. reread public current-facing docs from `main`;
5. perform final live runtime/ownership/Ticket health verification;
6. publish final coordination closeout without moving either release tag.

## Safety boundary

Any production-code change beyond release/version metadata reopens semantic/live qualification. v0.9.7 is immutable.
