# CNX-20260926-451 — Soft Context Pressure Must Not Block Dashboard Turns

Status: `COMPLETE`
Owner: ChatGPT
Executor: ChatGPT
GitHub issue: `#43`
Baseline/main SHA: `520d07d5bdb26be22fc03fd48a241c91bc3436ea`
Baseline release: `v0.9.8` (immutable)
Working branch: `cnx-451-soft-context-pressure-live-v2`

## Production evidence

- Dashboard session: `agent:main:dashboard:f6d5474d-df42-44c4-af8a-f4bfb68dfee8`.
- Turn 1 completed normally.
- Turn 2 completed normally after four Ollama model calls.
- Turn 3 Ticket: `CNXT-d4189017-56de-42b2-aec8-a0cf6f0be482`.
- Turn 3 pressure: `21093 / 24576 = 85.8%`, level `soft`, source `fresh-session-counter`.
- Event `context_pressure_deferred` was immediately followed by Ticket `failed/permanent` with `blocked by cogentnexus-openclaw`.
- No model call or inference attempt started for turn 3.

## Root cause

`v091-context-guard.ts` treats every non-normal pressure level as a blocking barrier. OpenClaw 2026.9.5 interprets `before_agent_run outcome=block` as terminal send failure, not as a resumable/deferred turn primitive. The soft-pressure path therefore converts a proactive safety hint into a user-visible permanent failure.

## Required semantics

1. Normal pressure: pass.
2. Soft pressure: pass current owner inference; do not set Ticket interrupted/permanent; do not enqueue Direct recovery; do not create blocking context-maintenance authority.
3. Record durable soft-pressure observation for diagnostics.
4. Hard pressure: preserve the existing barrier/maintenance/recovery behavior in this task.
5. Keep CNX-426 turn-budget/model-switch authority unchanged.
6. Keep CNX-448 terminal authority and CNX-449 long-running lease behavior unchanged.
7. `v0.9.8` remains immutable.

## TDD acceptance

- RED fixture reproduces `21093/24576` soft pressure and currently sees `outcome=block`.
- GREEN returns `outcome=pass`.
- Ticket stays `accepted` with no failure mutation.
- No `cnx_direct_recovery` or `cnx_context_maintenance` row is created for soft pressure.
- Durable `context_pressure_soft_observed` event is recorded.
- Hard-pressure fixture still blocks and queues maintenance/recovery.
- Full plugin/Python/build/CI/install-over/live Dashboard validation.

## Local qualification checkpoint

- RED reproduced the live soft-pressure permanent block.
- GREEN focused CNX-451 + CNX-426: `8/8 PASS`.
- Full Python: `747 passed, 5 skipped, 38 subtests passed`.
- Full Vitest: `95 files / 444 tests PASS`.
- build/evaluation/plugin validation/audit/diff-check: PASS.
- evaluation evidence SHA-256: `3f7aa713ef6987c0d6e72e96ac277dc8b060c18728aa79e15aea1e4b0f7b026a`.

## Resume checkpoint after CNX-453

- implementation candidate `09eec4113b371d39334d90a332fa9a6455530db0` passed exact-SHA CI 3/3 and physical install-over;
- CNX-453 repaired the long-running supervisor/recovery blocker and is closed GREEN on main `520d07d5bdb26be22fc03fd48a241c91bc3436ea`;
- `OLLAMA_KEEP_ALIVE=6h` is persistent and physically active;
- remaining gate: fresh live soft-pressure owner turn plus exactly-once settlement.


## Fresh live soft-pressure acceptance

Dedicated owner session:

- session key: `agent:main:dashboard:cnx451-soft-live-v2-01`;
- OpenClaw session id: `9fc97be5-22d6-4ea9-bb9e-a5b878bd4458`;
- native provider/model: `ollama/qwen3:1.7b`;
- `OLLAMA_KEEP_ALIVE=6h` remained live.

Context was increased only through supported owner turns. Prime plus probes A-C remained normal. Probe D produced the required physical soft-pressure topology:

- Ticket: `CNXT-411507aa-8653-4b47-9aea-7bd8d4a69c82`;
- run: `bc68c747-ea31-489a-a43d-fdc3e6e145f2`;
- projected context: `30866 / 40960` (`75.356%`);
- soft limit: `30310`;
- hard limit: `36864`;
- level: `soft`;
- source: `fresh-session-counter`;
- durable event: `context_pressure_soft_observed`;
- policy: `observe-and-pass`.

Immediately after the soft observation the same Ticket entered `direct_model_call_started` and canonical `inference_attempt_started`; it was not blocked and no failure state was written.

No `cnx_direct_recovery` row and no `cnx_context_maintenance` row were created for the soft observation.

The model call completed after `346916 ms` and the exact terminal chain was:

`direct_model_call_ended -> inference_attempt_ended -> response_ready -> direct_response_durable -> delivery_confirmed -> completed`

Exactly-once counts for the acceptance Ticket:

- `context_pressure_soft_observed`: 1;
- model-call start/end: 1/1;
- inference-attempt start/end: 1/1;
- `response_ready`: 1;
- `direct_response_durable`: 1;
- `delivery_confirmed`: 1;
- `completed`: 1;
- delivery rows: 1 (`direct_result`, `delivered`, attempt_count `0`);
- Ticket outbox rows: 0;
- global pending outbox: 0;
- SQLite integrity: `ok`.

CLI acceptance exited `0` with marker `CNX451_SOFT_PROBE_D_OK` and `stopReason=stop`.

## Final classification

`CNX451_SOFT_CONTEXT_PRESSURE_GREEN`
