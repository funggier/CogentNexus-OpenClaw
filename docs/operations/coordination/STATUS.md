# Coordination Status

Status: `COMPLETE`
State: `CNX449_LONG_RUNNING_OLLAMA_GUARD_GREEN`
Task: `CNX-20260926-449-long-running-model-lease-guard.md`
Branch: `cnx-449-long-running-model-lease-guard`
Executor: `ChatGPT`
Baseline release: `v0.9.8` (immutable)
Baseline SHA: `bffa539a59f8d0318cbffb062a73b205c8cb8705`
Candidate product SHA: `dfb3706e7c11e61cc7987a7e4928f3c5d7203435`

## Result

- Ollama default durable Direct model-call lease: 45 minutes.
- Non-Ollama default remains 15 minutes.
- Explicit timeout override remains authoritative within existing bounds.
- Unexpired active Direct lease fences probe-only Gateway hard-hang restart.
- Exact candidate CI: 3/3 workflows SUCCESS.
- Physical install-over: PASS.
- Source/installed payload: 296 files, exact fingerprint match.
- Fresh qwen3.8:27b live call: completed after 1,210,862 ms (~20m10.9s), beyond the old 15-minute boundary, with no premature Gateway restart.
- Final runtime: MANAGED generation 36, Gateway/Ollama/supervisor healthy, pending outbox 0.

## Follow-up backlog

`CNX-20260926-450-headless-agent-durable-settlement.md` / GitHub issue `#42`: define durable settlement for headless `openclaw agent` return-to-caller responses. This is separate from Task 449.

## Final classification

`CNX449_LONG_RUNNING_OLLAMA_GUARD_GREEN`
