# Coordination Status

Status: `IDLE`
State: `NO_ACTIVE_TASK`
Last completed task: `CNX-20260927-454-provider-model-catalog-refresh.md`
Last completed classification: `CNX454_PROVIDER_MODEL_CATALOG_REFRESH_GREEN_WITH_OPENAI_ROUTE_BOUNDARY`
Baseline release: `v0.9.8` (immutable)

## Accepted state

- CNX-451: GREEN and closed.
- CNX-452: GREEN and closed.
- CNX-453: GREEN and closed.
- CNX-454: OpenAI + Ollama model catalog refresh GREEN with an explicit OpenAI route boundary.
- OpenAI visible: `gpt-6-astra`, `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, `gpt-5.5`.
- OpenAI aliases: `gpt -> gpt-6-astra`, `gpt-mini -> gpt-5.6-luna`.
- GPT-6 Sol/Luna are not exposed on the current OpenClaw 2026.9.5 Codex ChatGPT-auth route after physical Luna rejection.
- Ollama Qwen 3.5 models are selectable with bounded 24k operational context.
- default model: `ollama/qwen3.8:27b`.
- `OLLAMA_KEEP_ALIVE=6h`: persistent and physically active.
- Gateway: healthy.
- provider ownership: OpenClaw.
- CNX-450: backlog only.
- historical orphan inference-attempt rows: 2, unchanged.
- `v0.9.8`: immutable.

## Current state

No active task.
