# CNX-20260926-451 — Soft Context Pressure Must Not Block Dashboard Turns Report

Status: `COMPLETE`
Classification: `CNX451_SOFT_CONTEXT_PRESSURE_GREEN`
GitHub issue: `#43`
Working branch: `cnx-451-soft-context-pressure-live-v2`
Baseline/main SHA: `520d07d5bdb26be22fc03fd48a241c91bc3436ea`
Baseline release: `v0.9.8` (immutable)

## Production defect

Dashboard session `agent:main:dashboard:f6d5474d-df42-44c4-af8a-f4bfb68dfee8` completed turns 1 and 2 normally, but turn 3 (`ขอแบบเจาะลึกลงรายละเอียดครับ`) failed before inference.

Turn 3 Ticket: `CNXT-d4189017-56de-42b2-aec8-a0cf6f0be482`.

Observed event sequence:

- accepted;
- ingress persisted/run-bound;
- routed Direct;
- `context_pressure_deferred` with `21093/24576`, ratio `0.8582763671875`, level `soft`, source `fresh-session-counter`;
- immediate `failed/permanent`: `Your message could not be sent: blocked by cogentnexus-openclaw`;
- failure delivery suppressed;
- no model-call row;
- no inference-attempt row.

## Root cause

`v091-context-guard.ts` mapped every non-normal pressure level to `before_agent_run outcome=block`. In OpenClaw 2026.9.5 that hook result is a terminal send failure, not a resumable defer primitive. A proactive soft-pressure signal was therefore converted into a permanent user-visible turn failure.

## Repair

Soft pressure is now observation-only:

- revalidate exact active session authority and current Direct Ticket;
- record durable `context_pressure_soft_observed` evidence;
- mark policy `observe-and-pass`;
- return `outcome=pass`;
- do not create `cnx_direct_recovery`;
- do not create blocking `cnx_context_maintenance` authority;
- do not mutate Ticket failure state.

Hard pressure remains on the pre-existing barrier/maintenance/recovery path. CNX-426 effective turn-budget authority remains unchanged.

## TDD

RED production-topology fixture reproduced `21093/24576` and failed with:

`expected { outcome: 'block', ... } to deeply equal { outcome: 'pass' }`

The hard-pressure control passed during RED, proving the fixture distinguished soft from hard behavior.

GREEN focused qualification:

- CNX-451: 2/2 PASS;
- CNX-426: 6/6 PASS;
- total focused: 8/8 PASS;
- soft fixture returns pass, Ticket remains accepted, no recovery/maintenance row, one durable soft observation;
- hard fixture still blocks and queues hard maintenance/recovery.

## Local validation

- Full Python: `747 passed, 5 skipped, 38 subtests passed`.
- Full plugin Vitest: `95 files / 444 tests PASS`.
- Build: PASS.
- Evaluation: PASS; evidence SHA-256 `3f7aa713ef6987c0d6e72e96ac277dc8b060c18728aa79e15aea1e4b0f7b026a`.
- Plugin validation: PASS (`46` config properties, `5` tools, `9` required Ticket DB tables, `298` packed files).
- Production dependency audit: `0 vulnerabilities`.
- `git diff --check`: PASS.

## Accepted gates since local qualification

- implementation candidate `09eec4113b371d39334d90a332fa9a6455530db0` committed/pushed;
- exact-SHA CI 3/3 SUCCESS;
- physical install-over exit `0` and package/installed parity accepted;
- CNX-453 infrastructure blocker repaired and closed GREEN on main `520d07d5bdb26be22fc03fd48a241c91bc3436ea`;
- `OLLAMA_KEEP_ALIVE=6h` confirmed live.

## Final gate status

Fresh live Dashboard-equivalent owner-session soft-pressure acceptance: `ACCEPTED`. Durable soft observation, non-blocking inference start, zero soft-created recovery/maintenance authority, exactly-once terminal settlement, and zero pending outbox were all physically proven.


## Fresh live soft-pressure acceptance — GREEN

After CNX-453 was closed GREEN, CNX-451 was re-qualified on a fresh dedicated owner session without direct DB manipulation.

Session:

- key: `agent:main:dashboard:cnx451-soft-live-v2-01`;
- session id: `9fc97be5-22d6-4ea9-bb9e-a5b878bd4458`;
- provider/model: `ollama/qwen3:1.7b`;
- keep-alive: `6h` physically active.

Context was built using supported OpenClaw owner turns only. Prime and probes A-C remained normal. Probe D was sized from the live context-guard estimator and entered the required soft range without touching hard pressure.

Acceptance Ticket:

- Ticket `CNXT-411507aa-8653-4b47-9aea-7bd8d4a69c82`;
- run `bc68c747-ea31-489a-a43d-fdc3e6e145f2`;
- projected tokens `30866 / 40960` = `75.356%`;
- soft limit `30310`;
- hard limit `36864`;
- level `soft`;
- source `fresh-session-counter`;
- policy `observe-and-pass`.

Durable sequence:

`accepted -> routed -> context_pressure_soft_observed -> direct_model_call_started -> inference_attempt_started -> direct_model_call_ended -> inference_attempt_ended -> response_ready -> direct_response_durable -> delivery_confirmed -> completed`

The soft observation therefore did not terminate or defer the user turn. Native Ollama inference started immediately after the observation.

Negative-authority proof:

- `cnx_direct_recovery` rows for Ticket: `0`;
- `cnx_context_maintenance` rows for Ticket: `0`;
- failure class/message: null;
- Ticket outbox rows: `0`;
- global pending outbox: `0`.

Exactly-once proof:

- each soft/model/attempt/response/delivery/completed event count: exactly `1`;
- delivery table: one `direct_result`, status `delivered`, attempt_count `0`;
- model-call duration: `346916 ms`;
- CLI exit: `0`;
- final marker: `CNX451_SOFT_PROBE_D_OK`;
- terminal `stopReason=stop`;
- SQLite integrity: `ok`.

This closes the production regression originally observed on Dashboard session `f6d5474d`: soft pressure is now observable but non-blocking. Hard-pressure compact/resume semantics remain intentionally separate under CNX-452 / GitHub issue #44.

## Final classification

`CNX451_SOFT_CONTEXT_PRESSURE_GREEN`
