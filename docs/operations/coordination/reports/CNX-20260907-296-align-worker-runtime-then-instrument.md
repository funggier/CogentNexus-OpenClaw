# CNX-20260907-296 — Align Worker Runtime Then Instrument Actual Invocation

## Disposition

`NEEDS_CHATGPT__TDD_REPAIR_GREEN__ALIGNED_RUNTIME_READONLY_PROBE_PASS__LIVE_WORKER_NOT_INSTALLED`

Phase A completed with strict RED → minimal GREEN TDD. Phase B used the repaired resolver for a read-only Gateway probe with the Gateway server's exact Node runtime. No live install, worker delivery flush, retry, replay, redelivery, Ticket disposition, or durable-state mutation was performed.

## Authority and scope

- remote authority at re-anchor: `7e4149ff9779eec90de9f5d742e150b3cbfb43e0`
- branch: `agent/v0.9.3-full-stabilization`
- accepted candidate: `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`
- task: `CNX-20260907-296`
- target session key hash prefix: `f9746f9ce80bf408`
- target session ID: `2b841ed6-c2dc-4699-b5ac-9e2716e6d5d5`
- pending Ticket: `CNXT-87fc2030-884f-4943-bb6e-864cc621d5dc`

## Phase A — TDD runtime alignment

### RED

Added `test_host_delivery_v092.py` with two behavior tests:

1. configured `OPENCLAW_GATEWAY_NODE_PATH` is preferred;
2. a configured missing path fails closed with a diagnostic naming the configuration.

Command:

```text
python -m unittest -v test_host_delivery_v092.py
```

Observed RED result:

```text
AttributeError: module 'host_delivery_v092' has no attribute '_resolve_node_executable'
Ran 2 tests ... FAILED (errors=2)
```

### Minimal GREEN repair

Changed only:

```text
skills/cogentnexus-openclaw/scripts/host_delivery_v092.py
```

Added `_resolve_node_executable()`:

- if `OPENCLAW_GATEWAY_NODE_PATH` is set, require that exact path to be a file and return it;
- if configured path is absent, raise `FileNotFoundError` naming `OPENCLAW_GATEWAY_NODE_PATH`;
- otherwise preserve existing PATH resolution behavior;
- `_openclaw_node_command()` now calls this resolver.

No delivery semantics, retry policy, payload handling, or durable-state code was changed.

GREEN result:

```text
Ran 2 tests ... OK
```

Repair evidence:

```text
host_delivery_v092.py: 5290 bytes
SHA-256: 8da7912bd2e104faa07cfe17133d3f86bb41a3176be5db75cd08078a3baae114

test_host_delivery_v092.py: 1003 bytes
SHA-256: 041a253d383a2a533ba252caa842077aaccd844ab36f4b617c137996de369b20
```

## Phase B — aligned-runtime read-only probe

The repository-repaired module was loaded without installing or copying it into the live worker. `OPENCLAW_GATEWAY_NODE_PATH` was set only for this isolated process to the observed Gateway runtime:

```text
C:\Program Files\nodejs\node.exe
```

The repaired `gateway_rpc("chat.history", ...)` was invoked once with sanitized evidence capture. Result:

```json
{
  "resolved_node": "C:\\Program Files\\nodejs\\node.exe",
  "entry": "C:\\Users\\CDQ-P\\AppData\\Roaming\\npm\\node_modules\\openclaw\\openclaw.mjs",
  "method": "chat.history",
  "session_key_sha256_16": "f9746f9ce80bf408",
  "json": true,
  "sessionId": "2b841ed6-c2dc-4699-b5ac-9e2716e6d5d5",
  "messages": 2
}
```

Probe interval:

```text
2026-09-07T06:15:53.249135+00:00 → 2026-09-07T06:15:57.968008+00:00
```

This proves the repair selects the Gateway's Node runtime when explicitly configured and that aligned-runtime `chat.history` works. It does not prove the live detached worker has adopted the repair, because live installation and service mutation are prohibited by Task296.

## Pending-state post-readback

Read-only SQLite post-readback showed the pending Ticket was not settled by the probe:

```json
{
  "delivery_status": "pending",
  "attempt_count": 360,
  "delivered_at": null,
  "ticket_status": "accepted",
  "delivery_confirmed_at": null
}
```

The attempt count reflects the independently running delivery worker and was not changed by the diagnostic process. No delivery confirmation was synthesized.

## Assessment

- TDD runtime alignment candidate: **GREEN**
- Aligned-runtime read-only `chat.history`: **PASS**
- Live detached worker adoption: **NOT PERFORMED** (installer/service mutation forbidden)
- No-JSON production failure resolved: **UNPROVEN**
- Deterministic repository defect: **not established**

The exact next decision is whether ChatGPT authorizes a separate bounded live deployment/requalification task for this already-tested resolver, followed by a fresh read-only observation. That task must explicitly define install/service scope and preserve the no-retry/no-redelivery fence.

## Hard-fence ledger

```text
semantic send: 0
chat.inject: 0
session create/delete/reset: 0
retry/replay/redelivery/disposition: 0
Ticket/SQLite/session/transcript mutation: 0
installer/install-over/uninstall: 0
Gateway/service mutation: 0
protected state mutation: 0
force push/history rewrite: 0
```
