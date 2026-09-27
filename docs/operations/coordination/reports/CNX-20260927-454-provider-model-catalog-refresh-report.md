# CNX-20260927-454 — Provider Model Catalog Refresh Report

Date: 2026-09-27
Status: `PASS`
Classification: `CNX454_PROVIDER_MODEL_CATALOG_REFRESH_GREEN`
GitHub Issue: #46

## Result

The live OpenClaw/CogentNexus model catalog was refreshed for both OpenAI and Ollama while preserving OpenClaw provider ownership and the existing default route.

### Final OpenAI catalog

- `openai/gpt-5.5`
- `openai/gpt-5.6-luna`
- `openai/gpt-5.6-sol`
- `openai/gpt-5.6-terra`
- `openai/gpt-6-astra`
- `openai/gpt-6-luna`
- `openai/gpt-6-sol`

Aliases:
- `gpt -> openai/gpt-6-sol`
- `gpt-mini -> openai/gpt-6-luna`

Retired/stale selectable entries `openai/gpt-5.4` and `openai/gpt-5.4-mini` were removed from both selectable configuration and runtime model policy.

GPT-6 Sol/Luna required explicit provider registration because OpenClaw 2026.9.5's hosted catalog had not yet natively registered those two model IDs.

### Final Ollama catalog

- `ollama/qwen3:1.7b`
- `ollama/qwen3.5:0.8b`
- `ollama/qwen3.5:4b`
- `ollama/qwen3.5:9b`
- `ollama/qwen3.6:27b`
- `ollama/qwen3.8:27b`

New Qwen 3.5 models are registered with operational `contextWindow/num_ctx = 24576`.

Default remains `ollama/qwen3.8:27b`.

## Root cause of incomplete initial visibility

OpenClaw model availability has multiple independent layers.

The initial refresh updated the catalog/config but an actual GPT-6 override was rejected because `agents.defaults.modelPolicy.allow` still contained the old GPT-5.4 entries.

After updating the runtime policy, GPT-6 Sol/Luna then exposed a second OpenClaw 2026.9.5 compatibility gap: they were not present in the native OpenAI provider catalog. Explicit OpenAI provider model registration resolved model resolution.

## Physical evidence

Ollama:
- OpenClaw isolated probe selected `ollama/qwen3.5:0.8b`.
- `ollama ps` physically showed the model loaded.
- context: `24576`
- retention: `6 hours from now`
- run reached `stopReason=stop`.

OpenAI:
- initial probe correctly exposed the stale model-policy fence.
- second probe correctly exposed missing native provider registration.
- after both repairs, GPT-6 Luna passed model resolution and run reached `stopReason=stop`.
- final CLI envelope was lost to an unrelated isolated-agent cleanup failure.

## Separate observed debt

`openclaw agent exec` cleanup can fail after a completed run:
- Codex one-shot shared-client cleanup may not settle.
- temporary agent SQLite WAL/SHM deletion can return EBUSY.

This did not prevent model selection/routing qualification and is not classified as a model-catalog defect.

## Final health

- Gateway HTTP: 200
- CogentNexus mode: MANAGED / active
- desired Gateway: running
- provider ownership: OpenClaw
- Supervisor: Ready
- Supervisor LastTaskResult: 0
- config validation: PASS
- SQLite integrity: ok
- nonterminal Tickets: 0
- pending outbox: 0
- active Direct model calls: 0
- historical orphan inference-attempt rows: 2, unchanged
- Ollama User keep-alive: 6h
- default model: `ollama/qwen3.8:27b`

## Conclusion

`CNX454_PROVIDER_MODEL_CATALOG_REFRESH_GREEN`
