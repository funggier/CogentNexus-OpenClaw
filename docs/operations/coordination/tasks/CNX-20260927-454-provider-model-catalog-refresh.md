# CNX-20260927-454 — Provider Model Catalog Refresh

Status: `COMPLETE`
GitHub Issue: #46
Classification: `CNX454_PROVIDER_MODEL_CATALOG_REFRESH_GREEN`

## Objective

Refresh the selectable OpenAI and Ollama model catalog used by the live OpenClaw/CogentNexus runtime without changing provider ownership or the default model.

## Starting baseline

- main baseline: `08d55d4da5a8ee4513c30b17dc42049a2a30509b`
- prior coordination state: `IDLE / NO_ACTIVE_TASK`
- default model: `ollama/qwen3.8:27b`
- OpenClaw: `2026.9.5`
- CogentNexus: MANAGED / active
- `v0.9.8`: immutable

## Completed changes

### OpenAI

Selectable/configured:
- `openai/gpt-5.5`
- `openai/gpt-5.6-luna`
- `openai/gpt-5.6-sol`
- `openai/gpt-5.6-terra`
- `openai/gpt-6-astra`
- `openai/gpt-6-luna`
- `openai/gpt-6-sol`

Removed stale selectable entries:
- `openai/gpt-5.4`
- `openai/gpt-5.4-mini`

Aliases:
- `gpt -> openai/gpt-6-sol`
- `gpt-mini -> openai/gpt-6-luna`

OpenClaw 2026.9.5 hosted catalog did not natively register GPT-6 Sol/Luna, so the OpenAI provider received explicit model registration while retaining OpenClaw provider/auth ownership.

### Ollama

Selectable/configured local catalog:
- `qwen3.8:27b`
- `qwen3.6:27b`
- `qwen3:1.7b`
- `qwen3.5:9b`
- `qwen3.5:4b`
- `qwen3.5:0.8b`

New Qwen 3.5 entries use bounded operational context `24576` instead of native 262k to avoid unnecessary memory/context pressure on this host.

Default remains:
`ollama/qwen3.8:27b`

## Required configuration layers repaired

Updating only the visible model list was insufficient. The complete runtime contract required all of:

1. `agents.defaults.models`
2. `agents.defaults.modelPolicy.allow`
3. `models.providers.ollama.models[]`
4. explicit `models.providers.openai.models[]` registration for current OpenAI models
5. model aliases

The stale `modelPolicy.allow` was the reason GPT-6 initially appeared in `models list` but was rejected by an actual model override.

## Qualification

- `openclaw config validate`: PASS
- OpenAI model list: 7 available/configured
- Ollama model list: 6 available
- Runtime allowlist: current OpenAI + Ollama entries present
- stale GPT-5.4 / GPT-5.4-mini absent from runtime allowlist
- Gateway: HTTP 200
- CogentNexus: MANAGED / active
- provider ownership: OpenClaw
- Supervisor: Ready, LastTaskResult 0
- SQLite integrity: ok
- nonterminal Tickets: 0
- active Direct model calls: 0
- pending outbox: 0
- historical orphan inference attempts: 2 unchanged
- User `OLLAMA_KEEP_ALIVE=6h`: unchanged
- physical Qwen 3.5 route: `qwen3.5:0.8b` loaded by OpenClaw with context 24576 and 6-hour retention

## OpenAI execution probe note

After policy/provider registration, a GPT-6 Luna isolated `agent exec` run passed model resolution and ended with `stopReason=stop`.

The CLI still returned an error during isolated-agent cleanup:
`Codex one-shot client cleanup could not be confirmed`.

A Qwen 3.5 isolated probe likewise reached the requested provider/model and `stopReason=stop`, then hit an EBUSY cleanup error on the temporary agent SQLite files.

These cleanup failures are separate from model catalog/routing and were not repaired under CNX-454.

## Runtime disturbance observed during qualification

A Gateway restart performed during early diagnosis entered a temporary unresponsive state. The runtime recovered, and the final model updates were completed through OpenClaw's supported hot config application without another restart.

Final Gateway health is GREEN.

## Invariants preserved

- `providerOwnership=openclaw`
- default remains `ollama/qwen3.8:27b`
- Ollama keep-alive remains 6h
- no direct SQLite mutation
- no force push
- no published tag/release mutation
- `v0.9.8` remains immutable
- CNX-450 remains backlog only
- CNX-451/452/453 remain closed GREEN
