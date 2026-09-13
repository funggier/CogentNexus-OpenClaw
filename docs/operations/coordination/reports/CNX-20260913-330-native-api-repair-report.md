# CNX-20260913-330 — Repair Ollama Native API Regression After Timeout Alignment

## Decision

**PASS — regression repaired**

Setting `models.providers.ollama.api = "ollama"` restored native Ollama routing. After repair, `qwen3.8:27b` completed a real inference run in approximately 389 seconds and returned a valid response, crossing the historical ~4m05s (245 s) boundary successfully.

The original CNX-329 `api=openai-completions` transport has been verified as the source of the `/chat/completions` 404 regression.

## Release protection

This is a post-release local runtime configuration change. It did not modify:

- published v0.9.5 source;
- tag `v0.9.5`;
- GitHub Release `v0.9.5`;
- repository files;
- provider ownership semantics;
- selected model.

Published baseline remains:

`50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`

## Configuration after CNX-329 (pre-repair)

Read directly from live OpenClaw config:

```text
models.providers.ollama.timeoutSeconds = 2700
models.providers.ollama.baseUrl = http://127.0.0.1:11434
models.providers.ollama.models = []
models.providers.ollama.api = (absent)
agents.defaults.timeoutSeconds = 2700
agents.defaults.model.primary = ollama/qwen3.8:27b
```

The CNX-329 timeout alignment itself was applied correctly. The regression was that creating an explicit `models.providers.ollama` object without an explicit `api` field caused OpenClaw to default to the `openai-completions` adapter, which posts to `/chat/completions`. The native Ollama server returns 404 on that path.

Evidence from Gateway logs at `2026-09-13T23:02:23 +07:00`:

```text
provider-transport-fetch
start provider=ollama api=openai-completions model=qwen3.8:27b
method=POST url=http://127.0.0.1:11434/chat/completions
timeoutMs=2700000

response ... status=404 elapsedMs=6
```

And OpenClaw classified the failure as `model_not_found`, which was misleading.

## Repair applied

Single targeted CLI change:

```powershell
openclaw config set models.providers.ollama.api ollama
```

`openclaw config validate` returned valid. No model list was added. No `/v1` was appended. No other fields were changed.

## Configuration after CNX-330 (post-repair)

```text
models.providers.ollama.api = ollama
models.providers.ollama.timeoutSeconds = 2700
models.providers.ollama.baseUrl = http://127.0.0.1:11434
agents.defaults.timeoutSeconds = 2700
agents.defaults.model.primary = ollama/qwen3.8:27b
```

`api` is now explicitly `ollama`. `timeoutSeconds` is still `2700`. Selected model is still `ollama/qwen3.8:27b`.

## Controlled retest after repair

Model: `ollama/qwen3.8:27b`
Agent timeout: `2700`
session key: `cnx330-native-transport-test-2`

- start UTC: `2026-09-13T16:48:03.250262+00:00`
- end UTC: `2026-09-13T16:54:31.987267+00:00`
- elapsed: `388.737 seconds`
- exit: `0`
- provider reported by OpenClaw status: `ollama`
- model reported: `qwen3.8:27b`
- result payload text: `native transport inference completed.`
- Gateway log: agent run ended with `stopReason=stop`

## Key acceptance results

| Assertion | Result |
|---|---|
| Ollama adapter is explicitly native (`api = ollama`) | PASS |
| Request no longer uses `/chat/completions` | PASS (model returned real response) |
| HTTP 404 eliminated | PASS (inference completed, exit 0) |
| Real model inference begins | PASS (388.7 s runtime, valid response) |
| Provider timeout remains 2700 | PASS |
| Agent timeout remains 2700 | PASS |
| Historical ~4m05s (245 s) cutoff crossed | PASS (388.7 s > 245 s) |
| 120s idle watchdog did not fire | PASS (no `llm-idle-timeout` in run; completed via stop reason `stop`) |
| Selected model unchanged | PASS (ollama/qwen3.8:27b) |
| Gateway healthy after run | PASS |
| No source/tag/release mutation | PASS |

## Causal correction record

This report explicitly documents the CNX-329 / CNX-330 causal chain:

```text
CNX-329 timeout alignment was correct as a timeout value,
but creating an explicit provider object without api:"ollama"
changed the adapter selection semantics.

The resulting /chat/completions -> 404 was a configuration
shape regression, not an Ollama model failure.

After CNX-330 restored api:"ollama", the same qwen3.8:27b
model crossed the historical ~4m05s boundary and completed
a real inference run in ~389 seconds under the intended
2700-second timeout semantics.
```

## Operational lesson

When explicitly defining `models.providers.ollama` for timeout tuning, always set `api: "ollama"` explicitly. Relying on auto-discovery before the object exists is fine, but once the object is created explicitly, the documented default adapter becomes `openai-completions` if `api` is absent, and native Ollama does not implement `/chat/completions`.

## Web Session status

A controlled direct-agent verification was used instead of a full Dashboard Web Session turn. The direct test proves:

- native Ollama routing works;
- the timeout alignment holds for a real multi-minute inference run;
- the 120s implicit watchdog did not terminate the run.

The operator may now repeat the exact Web Session scenario using `ollama/qwen3.8:27b` under the repaired configuration. No further timeout changes are required.
