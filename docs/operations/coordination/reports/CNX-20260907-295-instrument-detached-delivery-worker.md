# CNX-20260907-295 — Instrument Detached Delivery Worker Boundary

## Disposition

`NEEDS_CHATGPT__ENVIRONMENT_DIVERGENCE_CONFIRMED__CAUSALITY_NOT_PROVEN__NO_MUTATION`

Task295 performed bounded read-only instrumentation only. No retry, replay, redelivery, disposition, Ticket/session/SQLite/transcript mutation, message send, reset, deletion, or creation occurred.

## Authority and target

- remote authority at re-anchor: `707a22d6c296c4828327dd028d3e8a6eb2aae4ab`
- branch: `agent/v0.9.3-full-stabilization`
- candidate: `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`
- session key: `agent:main:discord:channel:1391855033993138217`
- session key hash prefix: `f9746f9ce80bf408`
- session ID: `2b841ed6-c2dc-4699-b5ac-9e2716e6d5d5`
- CNX generation: `2`
- pending Ticket: `CNXT-87fc2030-884f-4943-bb6e-864cc621d5dc`

## Detached-equivalent worker instrumentation

A detached-equivalent child was launched with stdin disconnected and a new process session. The request was read-only `chat.history`; payload contents and session key were not printed, only the key hash prefix.

```json
{
  "start_utc": "2026-09-07T05:41:29.002837+00:00",
  "end_utc": "2026-09-07T05:41:33.171020+00:00",
  "elapsed_ms": 4168,
  "child_pid": 11448,
  "exit": 0,
  "stdout_none": false,
  "stdout_bytes": 4219,
  "stderr_none": false,
  "stderr_bytes": 0,
  "stdout_sha256": "8306035dfa23ecd776d4e9c9eba848c290e9c4158843c5abcb7cce4462becc76",
  "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "python": "C:\\Users\\CDQ-P\\AppData\\Local\\hermes\\hermes-agent\\venv\\Scripts\\python.exe",
  "python_version": "3.11.15",
  "worker_node": "C:\\Users\\CDQ-P\\AppData\\Local\\hermes\\node\\node.exe",
  "worker_node_version": "v22.23.2",
  "openclaw_entry": "C:/Users/CDQ-P/AppData/Roaming/npm/node_modules/openclaw/openclaw.mjs",
  "openclaw_entry_exists": true
}
```

The sanitized argv shape was:

```text
[node.exe, openclaw.mjs, gateway, call, chat.history, --params, <JSON_REDACTED>, --json]
```

The child returned valid JSON with the target session ID and two messages. No `chat.inject` or other mutating Gateway method was called.

## Process/environment correlation

Read-only process inspection showed the Gateway server is a different Node installation:

```text
Gateway server PID 13832:
C:\Program Files\nodejs\node.exe C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\index.js gateway --port 18789

Detached-equivalent worker:
C:\Users\CDQ-P\AppData\Local\hermes\node\node.exe ... openclaw.mjs gateway call chat.history ...
```

This confirms a concrete Node/runtime-path divergence between the Gateway server and the worker. The interactive `openclaw.cmd` probe also resolves through the Hermes Node path. This is a verified lead, not proof that the divergence causes empty output.

## Reproduction results

Read-only probes against the same exact session succeeded:

- foreground `openclaw.cmd gateway call chat.history`: `5/5`, each exit `0`, stdout `4057` bytes, stderr `0`, valid JSON, `2` messages;
- 10 simultaneous foreground calls: `10/10`, each exit `0`, stdout `4057` bytes, stderr `0`;
- direct `node.exe openclaw.mjs gateway call chat.history`: `3/3`, valid JSON;
- detached-equivalent direct Node call: `1/1`, exit `0`, stdout `4219` bytes, stderr `0`, valid JSON.

The target transcript is present:

```text
path: C:\Users\CDQ-P\.openclaw\agents\main\sessions\2b841ed6-c2dc-4699-b5ac-9e2716e6d5d5.jsonl
size: 1560 bytes
SHA-256: 1b665e7f61ec372beff3a2b78e6d4d2e586ba8356d9f1d7326a6b2438ba784d3
```

The installed `host_delivery_v092.py` wrapper is byte-identical to the repository version:

```text
size: 4847 bytes
SHA-256: a93161416558c566d2227a0c8abaeb1cbf747ef73e39bc4c8bdc4299195d4d61
```

## Correlation with pending delivery

During instrumentation, the pending delivery continued recording the detached-worker diagnostic:

```text
OpenClaw Gateway RPC chat.history returned no JSON output
(exit=0, stdout=none, stderr=empty)
```

The delivery remained pending and was not settled. Therefore the evidence shows a discrepancy between the actual detached worker invocation that records empty streams and all reproducible probes run under the diagnostic shell. The exact failing invocation was not captured at the process boundary, so causal attribution remains unresolved.

## Classification and missing decision

Classification: **environment/worker-boundary divergence confirmed; deterministic source defect not proven.**

A future task would need explicit authority to instrument the actual detached worker invocation, retaining only sanitized executable paths, versions, PID ancestry, process start/exit times, raw stream presence/lengths/hashes, and Gateway correlation timestamps. It must not retry, inject, replay, redeliver, settle, or mutate state. Alternatively, ChatGPT may authorize a separately reviewed TDD repair that explicitly binds the worker to the same Node runtime as the Gateway, but Task295 alone does not justify that repair.

## Health and safety

- Gateway listener: `127.0.0.1:18789`, PID `13832`
- Gateway health: previously verified HTTP `200`
- Ollama health: previously verified HTTP `200`, model `qwen3.5:9b`
- SQLite integrity: previously verified `ok`
- pending Ticket remained pending; no delivery confirmation synthesized
- protected Ticket/session untouched
