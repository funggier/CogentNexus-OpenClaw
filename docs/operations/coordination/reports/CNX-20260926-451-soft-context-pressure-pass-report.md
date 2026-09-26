# CNX-20260926-451 — Soft Context Pressure Must Not Block Dashboard Turns Report

Status: `IN_PROGRESS`
Classification: `CNX451_LIVE_SOFT_ACCEPTANCE_PENDING`
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

## Remaining gate

Fresh live Dashboard-equivalent owner-session soft-pressure acceptance: durable `context_pressure_soft_observed`, no terminal block, inference starts, no soft-created recovery/maintenance authority, and terminal result settles exactly once with zero pending outbox.

## Current classification

`CNX451_LIVE_SOFT_ACCEPTANCE_PENDING`
