# CNX-20260907-294 — Diagnose Gateway `chat.history` No-JSON Boundary

## Disposition

`NEEDS_CHATGPT__NO_DETERMINISTIC_REPOSITORY_DEFECT_PROVEN__DETACHED_WORKER_TRANSPORT_DIAGNOSIS_REQUIRED__NO_MUTATION`

Task293 recorded repeated delivery failures reporting exit 0 with empty stdout/stderr from `chat.history`. This task performed only read-only source inspection and isolated Gateway probes. The installed Gateway contract and transcript are healthy, and the same direct Node transport succeeds repeatedly. The failure remains specific to the detached delivery-worker execution path and is not proven to be a deterministic repository defect.

## Authority and scope

- remote authority at re-anchor: `64f4b0b3d85a47025724986480f6ab9048d93ac5`
- branch: `agent/v0.9.3-full-stabilization`
- candidate SHA: `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`
- target session key: `agent:main:discord:channel:1391855033993138217`
- target session ID: `2b841ed6-c2dc-4699-b5ac-9e2716e6d5d5`
- target CNX generation: `2`
- pending Ticket: `CNXT-87fc2030-884f-4943-bb6e-864cc621d5dc`
- no semantic send, retry/replay/redelivery/disposition, Ticket mutation, SQLite mutation, session mutation, credential change, reset, deletion, or creation was performed

## Installed contract and caller inspection

Installed OpenClaw `2026.7.1-2` handles `chat.history` by validating params, resolving the exact session key, reading the session store, loading the bounded history page, and responding with a JSON object containing `sessionKey`, `sessionId`, and `messages`. The inspected installed handler is:

- `C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\chat-pg-BxhF6.js`
- handler lines 2079–2225
- registration lines 2227–2233

The target's local transcript exists and contains the exact new session identity plus both user and assistant messages:

- transcript: `C:\Users\CDQ-P\.openclaw\agents\main\sessions\2b841ed6-c2dc-4699-b5ac-9e2716e6d5d5.jsonl`
- size: `1560` bytes
- SHA-256: `1b665e7f61ec372beff3a2b78e6d4d2e586ba8356d9f1d7326a6b2438ba784d3`
- assistant message is present and the transcript ends with the expected assistant record

The CNX delivery caller is `host_delivery.py` through the preferred `host_delivery_v092.py` wrapper:

- `host_delivery.py::history_contains` calls `gateway_rpc("chat.history", {sessionKey, limit: 24, maxChars: 120000})`
- `host_delivery.py::gateway_rpc` invokes the OpenClaw CLI with `--json` and parses stdout, then valid JSON on stderr as fallback
- `host_delivery_v092.py` replaces the Windows npm-shim invocation with direct `node.exe openclaw.mjs` invocation
- the wrapper rebinds `base.gateway_rpc` and `base.mark_failed` before entering `base.main()`

The deployed v0.9.2 wrapper is byte-identical to the repository candidate:

- repository wrapper size/SHA-256: `4847` / `a93161416558c566d2227a0c8abaeb1cbf747ef73e39bc4c8bdc4299195d4d61`
- installed wrapper size/SHA-256: `4847` / `a93161416558c566d2227a0c8abaeb1cbf747ef73e39bc4c8bdc4299195d4d61`

## Isolated read-only probes

Exact command shape used:

```text
openclaw.cmd gateway call chat.history --params {"sessionKey":"agent:main:discord:channel:1391855033993138217","limit":24,"maxChars":120000} --json
```

The probe returned:

- exit: `0`
- stdout: `4057` bytes
- stderr: `0` bytes
- valid JSON
- messages: `2`
- sessionId: `2b841ed6-c2dc-4699-b5ac-9e2716e6d5d5`

The same command succeeded `5/5` in sequential probes. A concurrent read-only probe with 10 simultaneous calls also succeeded `10/10`; each returned exit `0`, `4057` stdout bytes, `0` stderr bytes, and valid JSON. Direct `node.exe openclaw.mjs` transport succeeded `3/3` with the same result.

These results establish that:

1. the Gateway has the target session;
2. the Gateway can read the target transcript;
3. the installed `chat.history` response contract produces JSON;
4. the direct Node transport is currently functional; and
5. the failure is not reproducible by the same foreground or concurrent command under the current interactive environment.

## Durable failure correlation

While the probes were run, the pending delivery row continued to record the detached-worker error:

```json
{
  "status": "pending",
  "attempt_count": 276,
  "last_error": "OpenClaw Gateway RPC chat.history returned no JSON output (exit=0, stdout=none, stderr=empty)",
  "delivered_at": null
}
```

Recent `assistant_delivery_retry` events continued at approximately 36-second intervals, with the same empty-output diagnostic. The discrepancy between successful foreground/direct probes and failing detached-worker attempts is the strongest available evidence of an execution-environment, process-lifetime, output-capture, or detached-worker race boundary. It does not identify one root cause conclusively.

## Root-cause conclusion

**Not proven as a deterministic repository defect.** The repository already contains the v0.9.2 mitigation that avoids the Windows npm command shim and invokes `node.exe` directly. That exact wrapper is installed byte-for-byte. The supported Gateway handler and target transcript are healthy, and isolated direct calls are consistently successful.

The remaining hypothesis requiring a separately authorized task is detached-worker-specific behavior, such as:

- the detached worker resolving a different Python/Node/OpenClaw executable or environment than the interactive shell;
- process-tree or command-shim lifetime/stream inheritance under the supervisor;
- an overlapping worker/lease lifecycle not represented in the current captured evidence; or
- a transient Gateway/CLI process exit path that returns code 0 without emitting the response.

No hypothesis above should be promoted to fact without retained detached-worker evidence.

## Exact missing decision

ChatGPT must decide whether to authorize a separate bounded read-only instrumentation task that captures, without credentials or payload secrets:

- resolved executable paths and versions inside the detached worker;
- sanitized argv shape (session key redacted/hash only);
- child PID/process-tree ownership and start/exit timestamps;
- raw stdout/stderr availability and byte lengths at the worker boundary; and
- Gateway/CLI correlation timestamps.

That task must not retry, inject, replay, redeliver, mutate durable state, or settle the pending Ticket. No source repair is justified by Task294 alone.

## Health and safety post-check

- Gateway health: HTTP `200`
- Ollama health: HTTP `200`; `qwen3.5:9b` present
- SQLite integrity: `ok`
- protected Ticket/session was not touched
- pending Ticket remained pending; no delivery confirmation was synthesized

## Evidence paths

- `C:\Users\CDQ-P\AppData\Local\Temp\cnx-task293-sessions-after.json`
- `C:\Users\CDQ-P\.openclaw\agents\main\sessions\2b841ed6-c2dc-4699-b5ac-9e2716e6d5d5.jsonl`
- `C:\Users\CDQ-P\.openclaw\workspace\skills\cogentnexus-openclaw\scripts\host_delivery.py`
- `C:\Users\CDQ-P\.openclaw\workspace\skills\cogentnexus-openclaw\scripts\host_delivery_v092.py`
- installed OpenClaw handler listed above
