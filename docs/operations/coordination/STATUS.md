# Coordination Status

Status: `COMPLETE`
State: `CNX447_V098_RELEASE_GREEN`
Task: `CNX-20260925-447-v098-release-preparation-and-publication.md`
Branch: `cnx-447-v098-release-preparation`
Executor: `ChatGPT`
Target release: `v0.9.8`
Production-code authority: `b908efe9f82550bc3cc071ad24c0f2d1d41cc4ec`

## Task 446 result

`CNX446_DASHBOARD_DIRECT_TERMINAL_BOUNDARY_GREEN`

The live defect is no longer reproducible. Codex/App-Server progress and tool writes remain non-terminal; the exact mirrored `runTerminal=true` final alone becomes the durable Direct result. Native Ollama fallback remains GREEN.

## Release-preparation baseline

The accepted production-code candidate has:

- exact-SHA GitHub CI GREEN;
- real OpenClaw 2026.9.5 install-over PASS;
- installed/source production-file parity PASS;
- Host active generation 30;
- plugin loaded with empty diagnostics;
- Gateway healthy;
- runtime hook runner ready;
- v092 supervisor healthy;
- no non-terminal Tickets/outbox residue;
- fresh installed-candidate Codex acceptance GREEN.

## Current phase

Stages 1-5 pre-publication qualification: GREEN.

The exact v0.9.8 candidate is frozen at `4f9b07d6e29e2051a44d2681cce0f8ecf5f47037`, exact-SHA GitHub gates are GREEN, real v0.9.7 -> v0.9.8 install-over is GREEN, installed/source payload parity is exact, and a fresh installed-candidate Codex terminal-final acceptance is GREEN.

Validation summary:

- focused release contracts: 40/40 PASS;
- full Python: 745 passed, 5 skipped, 38 subtests;
- Vitest: 93 files / 436 tests PASS;
- evaluation: PASS;
- production audit: 0 vulnerabilities;
- plugin/package validation: PASS, 294 packed files;
- payload identity: `173d6f95de3d5eaef420b47faf27d0d98f52190e570b8109dcc49f078423f9c0`;
- PowerShell/PS5.1/POSIX syntax/self-tests: PASS;
- `git diff --check`: PASS.

v0.9.8 is published at immutable tag SHA `4f9b07d6e29e2051a44d2681cce0f8ecf5f47037`, and `main` has already fast-forwarded to post-release docs commit `8d2204a6f1f0978873ef6c00bc3035cf3e664dc6`.

## Next gate

The stale docs-parser contract found by main Validate `36160610790` was repaired in `af90ff5c3259f2fb82228a1089f20cafe62cecc2`. Branch CI (`36162086121`, `36162086188`, `36162086282`) and main CI (`36163150015`, `36163150106`, `36163150135`) are all SUCCESS. CNX-447 is complete and v0.9.8 remains immutable at release/tag SHA `4f9b07d6e29e2051a44d2681cce0f8ecf5f47037`.
