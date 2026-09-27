# CNX-20260927-454 — Provider Model Catalog Refresh Report

Date: 2026-09-27
Status: `PASS`
Classification: `CNX454_PROVIDER_MODEL_CATALOG_REFRESH_GREEN_WITH_OPENAI_ROUTE_BOUNDARY`
GitHub Issue: #46

## Result

The live OpenClaw/CogentNexus model catalog was refreshed and physically qualified without changing the default model or provider ownership.

## Final OpenAI models exposed by this runtime

- `openai/gpt-6-astra`
- `openai/gpt-5.6-sol`
- `openai/gpt-5.6-terra`
- `openai/gpt-5.6-luna`
- `openai/gpt-5.5`

Aliases:
- `gpt -> openai/gpt-6-astra`
- `gpt-mini -> openai/gpt-5.6-luna`

Stale GPT-5.4 entries were removed.

### GPT-6 Sol/Luna are intentionally not exposed

OpenAI's API catalog has GPT-6 Sol/Luna, but the current live OpenClaw route uses the Codex plugin with ChatGPT-account authentication.

A physical Gateway turn for `openai/gpt-6-luna` returned:

`400 invalid_request_error: The 'gpt-6-luna' model is not supported when using Codex with a ChatGPT account.`

The initial compatibility experiment that manually registered GPT-6 Sol/Luna was therefore rolled back.

Current dependency boundary:
- OpenClaw: `2026.9.5`
- `@openclaw/codex`: `2026.9.5`
- bundled `@openai/codex`: `0.154.0`
- latest discovered `@openclaw/codex`: `2026.9.6`, requiring OpenClaw `>=2026.9.6`

No unsupported dependency override was applied.

## Final Ollama models exposed

- `ollama/qwen3:1.7b`
- `ollama/qwen3.5:0.8b`
- `ollama/qwen3.5:4b`
- `ollama/qwen3.5:9b`
- `ollama/qwen3.6:27b`
- `ollama/qwen3.8:27b`

New Qwen 3.5 entries use operational context 24576.

Default remains `ollama/qwen3.8:27b`.

## Physical evidence

### OpenAI GPT-6 Astra
Gateway smoke:
- status: OK
- requested: `openai/gpt-6-astra`
- effective: `openai/gpt-6-astra`
- response model: `gpt-6-astra`
- fallback used: false
- exact marker returned

### OpenAI GPT-5.6 Luna
Gateway smoke with `thinking=low`:
- status: OK
- requested/effective/response model: `openai/gpt-5.6-luna`
- fallback used: false
- exact marker returned

### Ollama Qwen 3.5
Gateway smoke:
- requested/effective/response model: `ollama/qwen3.5:0.8b`
- fallback used: false
- run completed successfully
- the 0.8B model did not follow the exact-marker instruction, which is a model-quality result rather than a route failure

`ollama ps`:
- `qwen3.5:0.8b` loaded
- context: 24576
- keep-alive: 6 hours

## Final runtime health

- config validation: PASS
- OpenAI visible model count: 5
- Ollama visible model count: 6
- Gateway HTTP: 200
- CogentNexus mode: MANAGED / active
- desired Gateway: running
- provider ownership: OpenClaw
- default model: `ollama/qwen3.8:27b`
- User `OLLAMA_KEEP_ALIVE=6h`: unchanged
- active Direct model calls after qualification: 0
- CNX-454 accepted-only smoke Ticket: cancelled through host controller
- historical orphan inference attempts from 2026-09-22/23: unchanged

## Cleanup and disturbance notes

An early Gateway restart during qualification temporarily became unresponsive. The runtime recovered and final catalog updates were completed using supported hot configuration without another restart.

CNX-454 live test sessions were deleted using the Gateway session lifecycle. Retained deleted-session archives remain subject to OpenClaw's normal retention behavior.

`openclaw agent exec` showed a separate one-shot cleanup defect; final qualification used normal Gateway turns instead.

## Conclusion

`CNX454_PROVIDER_MODEL_CATALOG_REFRESH_GREEN_WITH_OPENAI_ROUTE_BOUNDARY`
