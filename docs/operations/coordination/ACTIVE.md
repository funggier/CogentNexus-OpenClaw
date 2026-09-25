# Active Coordination

Status: `IN_PROGRESS`
State: `CNX447_V098_RELEASE_PREPARATION_BASELINE`
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

## Immediate next gates

1. inventory all current version/baseline/release references;
2. inspect the exact release workflow and packaging/checksum contract;
3. prove public v0.9.7 remains unchanged;
4. update version/release documentation coherently to v0.9.8;
5. locally qualify the exact release candidate before any publication;
6. no tag/release/main mutation until exact-SHA candidate gates are GREEN.

## Safety boundary

Any production-code change beyond release/version metadata reopens semantic/live qualification. v0.9.7 is immutable.
