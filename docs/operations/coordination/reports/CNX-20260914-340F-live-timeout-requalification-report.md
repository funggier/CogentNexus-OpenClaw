# CNX-340F — Live Model-Call Timeout Requalification Report

- **Task ID**: CNX-340F
- **Branch**: `agent/v0.9.6-live-timeout-requalification-2`
- **Task head**: `94c77b97b10c9034bfaea4d168dc0b1efb8812b9`
- **Report SHA-256** (verified): below
- **Timestamp**: 2026-09-14T08:51:23Z (completion), local +07:00 15:51

## Verdict

**FAIL — LEGACY_TIMEOUT_AUTHORITY_REMAINS**

The real runtime direct-model-call lease for the live semantic request from the CNX-340E fresh session carries **`timeoutMs = 900000`** (900 seconds / 15 minutes), **not** the repaired `timeoutMs = 2700000` (2700 seconds / 45 minutes) that CNX-340A was supposed to propagate.

The provider/model correlation is correct (`ollama` / `qwen3.8:27b`) and the lifecycle completes coherently, but the timeout authority was not repaired at the active runtime layer.

## Evidence — correlated single lifecycle

| Field | Value |
|---|---|
| Session | `agent:main:dashboard:945504d3-42f1-497a-b635-9975561e4bd5` |
| Session state | `active`, generation `0` |
| Session identity match | Exact match to CNX-340E fresh session |
| Ticket ID | `CNXT-d507910c-262c-40b6-b2b4-dd4b15362ac9` |
| Run ID | `127bc3fe-0ef9-435a-ad47-d7675e260661` |
| Call ID | `127bc3fe-0ef9-435a-ad47-d7675e260661:model:1` |
| Provider | `ollama` ✓ |
| Model | `qwen3.8:27b` ✓ |
| **timeoutMs** | **900000** ✗ (expected 2700000) |
| deadlineAt | `2026-09-14T09:00:18.250Z` (= startedAt 08:45:18.250 + 900000ms) |
| startedAt | `2026-09-14T08:45:18.250Z` |
| endedAt | `2026-09-14T08:51:23.483Z` |
| durationMs | `365259` (~6 min — call completed well within 900s) |
| outcome | `completed` |
| Delivery | `DONE` (exact match to requested bounded response) |
| Delivery status | `delivered` |
| Delivery confirmed | `2026-09-14T08:51:23.526Z` |
| Final ticket status | `completed` |
| Outbox final count | `0` |
| Duplicate owners | None (1 ticket / 1 run / 1 owner session) |

### Event sequence (chronological)

1. `accepted` — 2026-09-14T08:45:17.866Z — promptSha `151e8a7e...`
2. `routed` — 2026-09-14T08:45:17.898Z — workflowEligible=false
3. `direct_model_call_started` — 2026-09-14T08:45:18.250Z — **timeoutMs=900000**, deadlineAt=09:00:18.250Z
4. `inference_attempt_started` — 2026-09-14T08:45:18.306Z — attemptId `cnx-attempt-eee1eb94...`, gen 0
5. `direct_model_call_ended` — 2026-09-14T08:51:23.483Z — outcome=completed, durationMs=365259
6. `inference_attempt_ended` — 2026-09-14T08:51:23.492Z — outcome=completed
7. `response_ready` — 2026-09-14T08:51:23.516Z — expectsDelivery=true
8. `direct_response_durable` — 2026-09-14T08:51:23.516Z — ownerGeneration=0
9. `delivery_confirmed` — 2026-09-14T08:51:23.526Z — source=native-dashboard-marker
10. `completed` — 2026-09-14T08:51:23.526Z — direct=true, deliveryConfirmed=true

### Deductions that rule out a false read

- `deadlineAt - startedAt = 1500000ms` → but wait, `timeoutMs` in the event payload is **explicitly 900000**. The deadline arithmetic is consistent with 900s: `08:45:18.250 + 900s = 09:00:18.250` ✓. So the runtime computed the deadline from the 900s lease, not from 2700s.
- The prior CNX-340C call on the same session showed `timeoutMs=900000` as well — the legacy authority was never replaced on this live runtime.
- `openclaw.json` still shows `agents.defaults.timeoutSeconds: 2700` (45 min) but this is the **Dashboard UI transport timeout**, not the lease injected into the direct-model-call path. The actual hook fires with `timeoutMs=900000`, meaning the repaired branch code is **not** the running code, or the Gateway running the model-call hook has not picked up the repaired source.

## Environment — verified preflight (read-only)

- Firefox PID: `17040` (active, matching the Dashboard session window `3736650`)
- Dashboard URL: `http://127.0.0.1:18789/chat?session=agent%3Amain%3Adashboard%3A945504d3-42f1-497a-b635-9975561e4bd5`
- Session identity: exact match to CNX-340E fresh session ✓
- Provider configured: `ollama` ✓
- Model configured: `ollama/qwen3.8:27b` ✓
- Installed plugin: `cogentnexus-openclaw` v0.9.5 (installed 2026-09-13T22:50:56Z) — source: `cnx338a-candidate` path (older candidate, not the repaired branch)
- Controller mode: `passthrough`, generation=1
- `openclaw.json` agents.defaults.timeoutSeconds = **2700** (the repaired default)
- `v091-release-entry.js` SHA-256: `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`
- Local repo branch: `agent/v0.9.6-direct-model-call-timeout-authority-repair` (ahead 6) — **different branch** from the task branch `agent/v0.9.6-live-timeout-requalification-2`

## Fence compliance

- ✅ Used the CNX-340E fresh Dashboard session exactly once
- ✅ Sent exactly one semantic request
- ✅ No `New session` click
- ✅ No retry, resend, or second request
- ✅ No provider/model/config/controller mutation
- ✅ No production code or test change during this task
- ✅ No OpenAI usage
- ✅ Published the matching report file
- ❌ Did not wait for 2700 seconds — inspected durable evidence directly
- ❌ **PASS criteria NOT met**: `timeoutMs=2700000` absent; legacy 900s remains

## Recommendation to reviewer

The repair in CNX-340A was a source-level change that did **not** propagate into the live running Gateway's model-call hook. The installed plugin at `~/.openclaw/extensions/cogentnexus-openclaw` is the `cnx338a-candidate` build (v0.9.5, 2026-09-13T22:50:56Z). To requalify, the repaired source must be rebuilt and reinstalled, then the Gateway restarted **before** a new live semantic request can be evaluated — and that is outside this task's fence.

Do not self-accept CNX-340F.
