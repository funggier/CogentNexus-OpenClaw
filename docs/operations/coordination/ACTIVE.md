# Active Coordination

Status: `IDLE`
State: `NO_ACTIVE_TASK`
Last completed task: `CNX-20260927-454-provider-model-catalog-refresh.md`
Last completed classification: `CNX454_PROVIDER_MODEL_CATALOG_REFRESH_GREEN_WITH_OPENAI_ROUTE_BOUNDARY`
Baseline release: `v0.9.8` (immutable)

## Current state

OpenAI and Ollama selectable model catalogs are refreshed and physically qualified.

OpenAI runtime-visible models:
- GPT-6 Astra
- GPT-5.6 Sol / Terra / Luna
- GPT-5.5

GPT-6 Sol/Luna are available in the OpenAI API but are not exposed in this OpenClaw 2026.9.5 ChatGPT-auth route because the physical Codex route rejects GPT-6 Luna.

Ollama includes the installed Qwen 3.5 models with bounded 24k operational context.

Default remains `ollama/qwen3.8:27b`. Gateway and CogentNexus runtime are healthy. CNX-450 remains backlog only.
