# CNX-20260926-452 — Hard Context Pressure Compact/Resume Report

Status: `IN_PROGRESS`
Classification: `CNX452_LOCAL_GREEN_CI_PENDING`
GitHub issue: `#44`
Working branch: `cnx-452-hard-context-pressure-compact-resume`
Baseline SHA: `a03dadecc2a95550046978d18ba3590c56ceb615`
Baseline release: `v0.9.8` (immutable)

## Production defect

OpenClaw 2026.9.5 interprets `before_agent_run outcome=block` as terminal send failure. The pre-CNX-452 hard-pressure path used that hook result as if it were a resumable defer primitive, so the accepted owner turn could fail before queued context maintenance had a chance to resume it.

Physical evidence came from Dashboard session `agent:main:dashboard:f6d5474d-df42-44c4-af8a-f4bfb68dfee8`:

- Ticket `CNXT-c142a517-1a26-4122-bdb6-3c6426c92181`;
- run `394d8002-672b-4b77-bfd2-2034662895b6`;
- hard pressure `23548/24576 = 95.8%`;
- accepted -> routed -> context-pressure defer -> failed/permanent;
- no owner inference began.

## Repair

`v091-context-guard.ts` now treats hard pressure as an inline, authority-fenced pre-inference maintenance boundary instead of a background defer:

1. persist `context_pressure_hard_observed` and a hard-required maintenance row under the exact active Ticket/session generation;
2. claim that maintenance authority synchronously inside `before_agent_run`;
3. run bounded `sessions.compact` maintenance before owner inference;
4. preserve the stored/effective turn budget as authoritative even when the physical session reports a larger context window;
5. re-describe the exact owner session after compaction;
6. recompute pressure from the fresh owner-session counter plus the current prompt/system instead of stale pre-compaction transcript messages;
7. return `outcome=pass` only when the post-maintenance pressure is below hard;
8. keep the same Ticket accepted and create no Direct-recovery authority for a successfully resolved hard-pressure turn;
9. fail closed as `cnxclaw_context_pressure_unresolved` if bounded maintenance cannot prove a safe postcondition.

The existing bounded hard-trim/capsule fallback inside `maintain()` remains available when semantic compaction is insufficient. The maintenance service remains event/timer driven for pre-existing durable rows; the old `queueMicrotask(()=>pulse?.())` defer from the `before_agent_run` hard path is intentionally removed.

## Regression coverage

Focused CNX-452/CNX-451/CNX-426/wiring qualification: `15/15 PASS`.

The new CNX-452 fixtures prove:

- hard pressure + successful semantic compaction -> same owner turn returns `outcome=pass`;
- exactly one semantic compaction request on the happy path;
- Ticket remains `accepted` with no failure mutation;
- no `cnx_direct_recovery` row is created;
- maintenance reaches `done / semantic-compact` with before/after evidence;
- durable `context_pressure_hard_observed` and `context_pressure_inline_resolved` events exist;
- unresolved hard pressure remains fail-closed without mutating the Ticket into permanent failure or creating Direct recovery.

CNX-451 soft observe-and-pass and CNX-426 effective model-window authority remain green. The v091 wiring contract was updated to assert the new inline hard-pressure boundary while retaining the prohibition on periodic `setInterval` polling.

## Local validation

- Full Python: `754 passed, 5 skipped, 38 subtests passed`.
- Full plugin Vitest: `96 files / 446 tests PASS`.
- Build: PASS.
- Evaluation: PASS; evidence SHA-256 `088e235bcc3df923519918e30a5d301f88e961f73b7a3e3bf37349e1103bb660`.
- Plugin validation: PASS (`46` config properties, `5` tools, `9` required Ticket DB tables, `300` packed files).
- Production dependency audit: `0 vulnerabilities`.
- `git diff --check`: PASS.

## Accepted predecessors preserved

- CNX-451 soft context-pressure fix: GREEN.
- CNX-453 supervisor/recovery fix: GREEN.
- CNX-449 Ollama long-running lease: preserved.
- `OLLAMA_KEEP_ALIVE=6h`: persistent and physically active.
- `v0.9.8`: immutable.

## Remaining gates

1. commit/push exact candidate SHA;
2. GitHub exact-SHA CI;
3. physical install-over and source/installed parity;
4. fresh live hard-pressure owner-session acceptance;
5. verify inline compaction occurs before inference, the same Ticket/run proceeds, and terminal/delivery settlement remains exactly once.

## Current classification

`CNX452_LOCAL_GREEN_CI_PENDING`
