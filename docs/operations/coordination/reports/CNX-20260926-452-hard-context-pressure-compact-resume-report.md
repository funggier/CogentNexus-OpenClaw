# CNX-20260926-452 — Hard Context Pressure Compact/Resume Report

Status: `COMPLETE`
Classification: `CNX452_HARD_CONTEXT_COMPACT_RESUME_GREEN`
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

## Final qualification

Product candidate: `b116fa188d41d1acb8110e59fca4bf056a160643`.

Exact-SHA CI:

- Validate `36267805183`: SUCCESS;
- PS5.1 Acceptance Smoke `36267805207`: SUCCESS;
- Windows Installer Pack Smoke `36267805221`: SUCCESS.

Source/installed payload parity: `300/300` files, fingerprint `7e66e09fc475959dfdb2d675debf168211aed1eb1d8713781a99d29d4f5d31cc`.

A setup run using `openclaw agent --timeout 900` ended at ~900 seconds and was classified as qualification-harness timeout rather than product failure. The final live acceptance used `--timeout 3600`.

Fresh live round-2 hard-pressure acceptance:

- owner: `agent:main:dashboard:cnx452-r2-live-hard`;
- Ticket: `CNXT-20ab5f72-61e6-4003-b630-8504cceef59b`;
- run: `821c949a-22ff-49a9-8ebe-84a2a90fe578`;
- provider/model: `ollama/qwen3:1.7b`;
- pressure before maintenance: `37808/40960` (`hard`);
- `context_pressure_hard_observed` persisted before inference;
- inline action: `hard-trim-200`;
- verified post-trim pressure: `23497/40960` (`normal`);
- `context_pressure_inline_resolved` persisted before the first model call;
- maintenance: `done`, one attempt, no error;
- no Direct recovery row;
- model call completed in `156059 ms`;
- final visible marker: `CNX452_R2_HARD_OK`;
- `stopReason=stop`;
- response durable, delivery confirmed exactly once, Ticket completed.

Final runtime invariants:

- SQLite integrity `ok`;
- nonterminal Tickets `0`;
- pending outbox `0`;
- active Direct model calls `0`;
- `OLLAMA_KEEP_ALIVE=6h` physically active.

## Final classification

`CNX452_HARD_CONTEXT_COMPACT_RESUME_GREEN`

## Live qualification round 1 — physical failure and repair evidence

The first installed-candidate live acceptance on the original Dashboard owner session did **not** pass, so Task 452 remained open.

- Ticket: `CNXT-94a53d84-511f-45bb-ab60-04d83962bb9d`
- run: `325bae4f-45cc-49b4-96ee-0d7ef67bc326`
- owner: `agent:main:dashboard:f6d5474d-df42-44c4-af8a-f4bfb68dfee8`
- pressure: `23838/24576 = 96.997%`, level `hard`
- `context_pressure_hard_observed` occurred before any model call.
- maintenance ended `context_pressure_inline_unresolved`; OpenClaw then converted hook `outcome=block` into `failed/permanent`.
- no model call/inference attempt started for that failed turn.

Physical OpenClaw contract evidence:

- semantic `sessions.compact` during `before_agent_run` is rejected because the same session already has an active run;
- line trim `maxLines=60` returned `{ok:true, compacted:false, kept:23}`;
- line trim `maxLines=20` returned `{ok:true, compacted:false, kept:20}`;
- the transcript physically reduced to 20 transcript events / 12 logical messages;
- bounded post-trim estimate was `9642/24576 = 39.2%`, below safe limit `21626`.

Therefore `compacted` is semantic-checkpoint evidence and is not authoritative for bounded `maxLines` trimming. Hard-trim safety authority is now:

1. `ok=true`;
2. valid integer `kept <= maxLines`;
3. fresh post-trim session tokens when available, otherwise bounded transcript estimation;
4. verified token count below the effective turn-window safety limit.

A second defect was proven: TS source already contained a deeper hard-trim ladder while packaged/installed `dist/v091-context-guard.js` still contained the older `200 -> 120 -> 60` ladder. Package-to-installed parity therefore did not prove source-to-dist semantic parity.

Round-2 repair:

- `v090-context-api.ts` accepts physical line-trim results without requiring `compacted=true`, then verifies post-trim occupancy;
- v090/v091 guards require `cnxVerification` and verified token evidence before accepting hard trim;
- missing/unknown post-trim occupancy is not auto-accepted;
- v090/v091 hard-trim ladders converge below 60 lines;
- CNX-426 fixture models the verified line-trim contract;
- physical-schema regression `ok:true, compacted:false, kept:20` is covered.

Round-2 validation so far:

- focused: 5 files / 25 tests PASS;
- full Vitest: 96 files / 448 tests PASS;
- build: PASS; compiled `dist/v091-context-guard.js` contains the deep ladder and verified-evidence gate;
- evaluation: PASS, evidence SHA-256 `51d56575225b9e1b10238b8c46b50113facf4de2ebc12b313c6d986dcea0535d`;
- plugin validation: PASS, 300 packed files;
- production dependency audit: 0 vulnerabilities;
- full Python: `754 passed, 5 skipped, 38 subtests passed`.
