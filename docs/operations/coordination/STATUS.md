# Coordination Status

Status: `IN_PROGRESS`
State: `CNX446_LIVE_GREEN_INSTALLER_TIMEOUT_REPAIR_LOCAL_GREEN_COMMIT_PENDING`
Task: `CNX-20260925-446-dashboard-direct-terminal-final-boundary.md`
Branch: `cnx-446-dashboard-direct-terminal-final-boundary`
Executor: `ChatGPT`
Target release line: `v0.9.8`

## Current phase

The terminal-final delivery defect is live GREEN on both the Codex/App-Server mirror path and native Ollama fallback. A real candidate install-over then exposed a post-mutation OpenClaw 2026.9.5 plugin CLI hang, so release qualification remains open while that installer compatibility repair is exact-SHA requalified.

## Confirmed terminal-boundary evidence

Codex/App-Server:

- run `cnx446-live-codex-b-send-v1`;
- Ticket `CNXT-c4e850f7-a7bd-48ec-9839-3264350d7a6c`;
- commentary `09:51:53.454Z`: no `runTerminal`;
- tool call `09:51:55.781Z`: no `runTerminal`;
- tool result `09:51:55.829Z`;
- true final `09:51:57.932Z`: `runTerminal=true`;
- `response_ready` `09:51:57.950Z`;
- completion `09:51:57.957Z`;
- final/payload SHA-256: `64c8c4897e62f937e87121309b6cbc056838c1d359999573a7251bedbe7a0f2a`;
- exactly one direct-result delivery.

Native Ollama:

- run `cnx446-ollama-live-a`;
- Ticket `CNXT-ca68602c-ef77-49a2-aa83-31dff08b137d`;
- model `ollama/qwen3.8:27b`, native `openclaw` runtime;
- final `CNX446_OLLAMA_NATIVE_OK` at `09:56:38.515Z`;
- no mirror metadata and no `runTerminal`;
- `response_ready` `09:56:38.555Z`;
- completion `09:56:38.567Z`;
- final/payload SHA-256: `e6805dd942c32903d50b030863c01aadeb04d6784d029c90ac7e1788042167a3`;
- exactly one direct-result delivery.

## Installer timeout hardening

The production Host still uses the normal checked 180-second `openclaw plugins enable|disable` call. Only `TimeoutExpired` is reconciled, and only when OpenClaw's canonical config, refreshed registry, and plugin inspector all agree on the requested state. Config mismatch, registry refresh failure, inspector mismatch, or reconciliation timeout remain failures.

Validation:

- focused timeout tests: 6/6 PASS;
- Host/installer regression: 90/90 PASS;
- live non-mutating parser probe against OpenClaw 2026.9.5: PASS;
- full Python: 742 passed, 5 skipped, 38 subtests passed;
- `git diff --check`: PASS.

## Current next gate

Commit/push the new installer-compatible SHA and require exact-SHA CI GREEN before another real install-over. After install-over, re-prove installed runtime health and rerun the Codex terminal-boundary live gate before v0.9.8 publication.
