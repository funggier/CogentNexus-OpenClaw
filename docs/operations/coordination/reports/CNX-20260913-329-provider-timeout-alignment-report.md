# CNX-20260913-329 — Persistent Provider Timeout Alignment Report

## Decision

**BLOCKED / NOT FIXED**

The requested timeout values were applied and persisted, but the original Web Session acceptance could not be completed. Fresh evidence shows that the current limiting layer is not the configured 2700-second provider HTTP timeout alone:

1. the controlled retest routed to `http://127.0.0.1:11434/chat/completions` and received HTTP 404 in 6 ms, so that run did not reach model inference;
2. prior `qwen3.8:27b` Web Session logs show an independent `LLM idle timeout (120s): no response from model` watchdog and model-silent retries.

Therefore this report does **not** claim the timeout issue is fixed.

## Release protection

This is a post-release local runtime configuration investigation. It did not modify:

- published v0.9.5 source;
- tag `v0.9.5`;
- GitHub Release `v0.9.5`;
- repository source files;
- provider ownership semantics;
- selected model.

Published baseline remains:

`50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`

## Configuration before

Read from the live OpenClaw configuration before mutation:

- `agents.defaults.timeoutSeconds`: path absent; OpenClaw documentation for this version states the default agent runtime ceiling is 172800 seconds (48 hours) when no explicit value or run-specific override applies.
- `models.providers.ollama.timeoutSeconds`: path absent.
- selected model: `ollama/qwen3.8:27b`.
- raw config contained no explicit `models.providers.ollama` object.
- an unrelated `models.providers.lmstudio_local.timeoutSeconds` value of 600 was present and was not changed.

The observed Web Session evidence described an approximately 45-minute agent ceiling, but that value was not present in the persisted config and could not be independently read back as `agents.defaults.timeoutSeconds`. The prior Web Session logs also exposed a separate 120-second model-idle watchdog.

## Configuration after

Using OpenClaw's CLI in dry-run mode first, then applying the exact requested bounded alignment:

```text
agents.defaults.timeoutSeconds = 2700
models.providers.ollama.timeoutSeconds = 2700
```

Read-back after write:

```text
2700
2700
```

`openclaw config validate` returned:

```text
Config valid: ~\\.openclaw\\openclaw.json
```

No manual JSON edit was used. No model list was added. The selected model remained `ollama/qwen3.8:27b`.

## Gateway restart

Executed:

```text
openclaw gateway restart
```

Result: scheduled task restarted successfully.

Post-restart verification:

- Gateway runtime: running, state Ready;
- connectivity probe: ok;
- listening: `127.0.0.1:18789`;
- model status default: `ollama/qwen3.8:27b`;
- timeout values read back as 2700 / 2700.

Gateway logs confirmed the new provider transport budget was applied:

```text
[model-fetch] ... timeoutMs=2700000 ...
```

## Controlled qwen3.8:27b retest

Test command used the exact model and an explicit 2700-second agent timeout.

- start UTC: `2026-09-13T16:02:17.843942+00:00`
- end UTC: `2026-09-13T16:02:23.368825+00:00`
- elapsed: `5.525 seconds`
- model: `ollama/qwen3.8:27b`
- result: failed before inference
- provider response: HTTP 404 from `http://127.0.0.1:11434/chat/completions`
- OpenClaw classification: `model_not_found`
- no retry/fallback result was accepted

This is not a valid long-first-token regression result because the request did not reach model inference.

## Historical Web Session evidence

Fresh log inspection for the same model shows a different lower-level boundary in previous Web Session attempts:

```text
[llm-idle-timeout] ollama/qwen3.8:27b produced no reply before the idle watchdog
rawErrorPreview: LLM idle timeout (120s): no response from model
```

The logs show repeated model-silent timeout events around:

- `2026-09-13T22:40:16 +07:00`
- `2026-09-13T22:44:04 +07:00`
- `2026-09-13T22:50:28 +07:00`
- `2026-09-13T22:52:29 +07:00`

The earlier Web Session result recorded two 120-second timeouts and no readable model response. This identifies an independent 120-second idle watchdog / model-silence boundary. The historical approximately 4m05s report is therefore not the only effective lower ceiling.

## Runtime health

At the time of verification:

- selected provider: Ollama;
- selected model: `ollama/qwen3.8:27b`;
- Ollama installed/reachable/healthy/ready;
- Gateway healthy;
- no provider switch was performed;
- no credential change was performed.

## Root-cause boundary and next required action

The timeout alignment itself is persisted correctly, but Web Session acceptance remains blocked by two unresolved runtime issues:

1. **Transport routing:** the controlled OpenClaw request used `/chat/completions` and received 404 from the Ollama endpoint. The provider route/base URL/API contract must be diagnosed before another model test; no unrelated provider configuration was changed here.
2. **Idle watchdog:** prior Web Session runs were terminated by an explicit 120-second model-idle watchdog before the 2700-second provider/agent ceilings could help. The source of that watchdog must be identified and aligned or explicitly documented before claiming acceptance.

Do not increase more timeouts blindly. Do not claim the original failure shape has been eliminated until a real `qwen3.8:27b` Web Session survives beyond the historical boundary and produces the expected durable result.

## Final verification state

| Assertion | Result |
|---|---|
| Agent timeout equals Ollama provider timeout | PASS: 2700 = 2700 |
| Config validates | PASS |
| Gateway restart/health | PASS |
| Ollama reachable/healthy | PASS |
| Selected model remains qwen3.8:27b | PASS |
| Historical ~4m05s cutoff disproven | NOT PROVEN |
| Web Session acceptance | BLOCKED; current retest hit 404, prior runs hit 120s idle watchdog |
| Source changed | NO |
| v0.9.5 tag/release changed | NO |

The local runtime configuration change is intentionally recorded as an operational experiment, not as a product-release fix.
