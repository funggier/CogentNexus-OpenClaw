# CNX-20260927-454 — Provider Model Catalog Refresh

Status: `COMPLETE`
GitHub Issue: #46
Classification: `CNX454_PROVIDER_MODEL_CATALOG_REFRESH_GREEN_WITH_OPENAI_ROUTE_BOUNDARY`

## Objective

Refresh the selectable OpenAI and Ollama models used by the live OpenClaw/CogentNexus runtime while preserving provider ownership, the default model, and existing runtime policy.

## Starting baseline

- main baseline: `08d55d4da5a8ee4513c30b17dc42049a2a30509b`
- OpenClaw: `2026.9.5`
- CogentNexus: MANAGED / active
- default model: `ollama/qwen3.8:27b`
- `v0.9.8`: immutable

## Final OpenAI catalog for this live route

Selectable and runtime-allowed:
- `openai/gpt-6-astra`
- `openai/gpt-5.6-sol`
- `openai/gpt-5.6-terra`
- `openai/gpt-5.6-luna`
- `openai/gpt-5.5`

Removed stale selectable entries:
- `openai/gpt-5.4`
- `openai/gpt-5.4-mini`

Aliases:
- `gpt -> openai/gpt-6-astra`
- `gpt-mini -> openai/gpt-5.6-luna`

### GPT-6 Sol/Luna boundary

OpenAI's API currently exposes `gpt-6-sol` and `gpt-6-luna`, but they are not retained in the final selector for this machine's current OpenClaw/Codex ChatGPT-auth route.

Physical Gateway probe for `openai/gpt-6-luna` returned HTTP 400 from the Codex route:

`The 'gpt-6-luna' model is not supported when using Codex with a ChatGPT account.`

OpenClaw `2026.9.5` uses `@openclaw/codex 2026.9.5`, which pins `@openai/codex 0.154.0`.
The current `@openclaw/codex 2026.9.6` requires OpenClaw `>=2026.9.6`, so no unsupported cross-version plugin update or node_modules override was performed.

## Final Ollama catalog

Selectable and runtime-allowed:
- `ollama/qwen3.8:27b`
- `ollama/qwen3.6:27b`
- `ollama/qwen3:1.7b`
- `ollama/qwen3.5:9b`
- `ollama/qwen3.5:4b`
- `ollama/qwen3.5:0.8b`

The new Qwen 3.5 entries are bounded to operational `contextWindow/num_ctx = 24576` instead of native 262144 to avoid unnecessary memory/context pressure.

Default remains:
`ollama/qwen3.8:27b`

## Required configuration layers

The completed update covers:
1. hosted model catalog refresh,
2. `agents.defaults.models`,
3. `agents.defaults.modelPolicy.allow`,
4. `models.providers.ollama.models[]`,
5. model aliases.

An attempted explicit OpenAI provider registration for GPT-6 Sol/Luna was removed after physical qualification proved the current ChatGPT-auth Codex route does not support Luna.

## Physical qualification

PASS:
- `openclaw config validate`
- GPT-6 Astra Gateway turn: requested/effective/response model all `openai/gpt-6-astra`, no fallback, exact marker returned.
- GPT-5.6 Luna Gateway turn with `thinking=low`: requested/effective/response model all `openai/gpt-5.6-luna`, no fallback, exact marker returned.
- Qwen 3.5 Gateway turn: requested/effective/response model all `ollama/qwen3.5:0.8b`, no fallback.
- `ollama ps` physically showed Qwen 3.5 loaded with context 24576 and 6-hour retention.
- Gateway HTTP 200 after final hot configuration.
- CogentNexus remains MANAGED / active.
- `providerOwnership=openclaw`.
- default remains `ollama/qwen3.8:27b`.
- User `OLLAMA_KEEP_ALIVE=6h` unchanged.

Expected/qualified boundary:
- GPT-6 Luna physical Gateway turn is rejected by the current Codex ChatGPT-account route and is therefore not exposed in the final selector.
- GPT-6 Sol is likewise deferred with Luna rather than exposed without route qualification.

## Cleanup

- CNX-454 accepted-only smoke Ticket was cancelled through host controller.
- CNX-454 live test sessions were deleted through `openclaw sessions delete`.
- OpenClaw retained deleted-session archives according to its normal retention lifecycle.
- temporary `cnx454-*` files under `~/.openclaw` were removed.
- no direct SQLite mutation was performed.

## Observed separate debt

`openclaw agent exec` one-shot qualification can finish the model turn but fail cleanup:
- Codex shared-client release may not settle.
- temporary SQLite WAL/SHM cleanup can return EBUSY.

Gateway-based qualification was used for final route evidence. This cleanup behavior was not repaired under CNX-454.

## Invariants preserved

- provider ownership remains OpenClaw
- no force push
- no published tag/release mutation
- `v0.9.8` remains immutable
- CNX-450 remains backlog only
- CNX-451/452/453 remain closed GREEN
