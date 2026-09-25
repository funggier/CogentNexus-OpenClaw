# Coordination Status

Status: `IN_PROGRESS`
State: `CNX447_V098_RELEASE_PREPARATION_BASELINE`
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

Stage 1 — release baseline and scope audit.

No version/tag/release/main mutation has been authorized by evidence yet. The next work is to enumerate version references, inspect release.yml/package contracts, and establish the minimal metadata/documentation delta for v0.9.8.

## Next gate

Create a complete release-reference inventory and confirm the repository publication workflow before changing version metadata.
