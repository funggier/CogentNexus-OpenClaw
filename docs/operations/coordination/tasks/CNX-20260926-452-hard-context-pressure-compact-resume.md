# CNX-20260926-452 — Hard Context Pressure Compact/Resume

Status: `COMPLETE`
Owner: ChatGPT
Executor: ChatGPT
GitHub issue: `#44`
Baseline SHA: `a03dadecc2a95550046978d18ba3590c56ceb615`
Baseline release: `v0.9.8` (immutable)
Working branch: `cnx-452-hard-context-pressure-compact-resume`

## Production evidence

- Original Dashboard session: `agent:main:dashboard:f6d5474d-df42-44c4-af8a-f4bfb68dfee8`.
- Hard-pressure Ticket: `CNXT-c142a517-1a26-4122-bdb6-3c6426c92181`.
- Run: `394d8002-672b-4b77-bfd2-2034662895b6`.
- Pressure: `23548/24576 = 95.8%`, level `hard`.
- Sequence: accepted -> routed -> context_pressure_deferred -> failed/permanent -> failure_delivery_suppressed.
- No model call or inference attempt started.

## Root semantic conflict

`before_agent_run outcome=block` is terminal failure in OpenClaw 2026.9.5. The v091 context guard currently uses that outcome as if it were a resumable defer primitive: it queues `cnx_context_maintenance` / `cnx_direct_recovery`, then OpenClaw closes the current turn before maintenance can resume it.

## Required semantics

1. Preserve hard overflow safety: never simply pass an unsafe hard-pressure turn.
2. Do not use hook `block` as the normal compact/resume mechanism.
3. For hard pressure, perform owner-session compaction under the current Ticket/session-generation authority before inference.
4. Re-describe the physical owner session after compaction and re-evaluate the effective turn budget including the current prompt.
5. Pass the same owner turn only when the post-compaction pressure is below hard.
6. If semantic compaction is insufficient, use the existing bounded hard-trim/capsule path before deciding the turn is safe.
7. Do not enqueue Direct recovery merely because context is hard if inline maintenance resolves it.
8. Preserve exactly-once inference/delivery, CNX-426 effective-window authority, CNX-448 terminal authority, CNX-449 long-running lease guard, CNX-451 soft observe-and-pass, and CNX-453 supervisor recovery fixes.
9. Fail closed if compaction cannot establish a safe postcondition; do not silently exceed the model window.
10. `v0.9.8` remains immutable.

## TDD acceptance

- RED: hard-pressure fixture currently returns `outcome=block` even when `sessions.compact` can reduce context to a safe level.
- GREEN: the same fixture compacts synchronously, revalidates exact Ticket/session authority, and returns `outcome=pass`.
- Exactly one semantic compaction request for the happy path.
- Post-compaction pressure must be below hard using the stored/effective turn budget; stale larger physical session windows must not override CNX-426 authority.
- Ticket remains `accepted`, with no permanent failure mutation.
- No `cnx_direct_recovery` row is created on successful inline resolution.
- Maintenance row reaches `done` with durable before/after/action evidence.
- Hard-trim fallback remains bounded and authority-fenced.
- Unresolved/exhausted hard pressure remains fail-closed and does not start inference.
- Existing soft-pressure fixture remains observe-and-pass.
- Full plugin/Python/build/evaluation/audit/CI/install-over/live owner-session qualification.

## Local qualification checkpoint

- hard-pressure inline compact/resume fixture: PASS;
- unresolved hard pressure remains fail-closed without Ticket permanent-failure mutation or Direct recovery;
- focused CNX-452/CNX-451/CNX-426/wiring: `15/15 PASS`;
- full Python: `754 passed, 5 skipped, 38 subtests passed`;
- full Vitest: `96 files / 446 tests PASS`;
- build/evaluation/plugin validation/audit/diff-check: PASS;
- evaluation evidence SHA-256: `088e235bcc3df923519918e30a5d301f88e961f73b7a3e3bf37349e1103bb660`;
- packed plugin payload: `300` files.

## Live qualification round 1 / repair round 2

Physical live hard-pressure acceptance reached `23838/24576` before inference but failed because OpenClaw 2026.9.5 rejects semantic `sessions.compact` during the same active run and reports bounded `maxLines` trimming as `compacted:false` even when the transcript is actually trimmed. A `maxLines=20` probe physically reduced the transcript to 20 events / 12 logical messages with bounded estimate `9642/24576`, safely below the `21626` limit.

Round-2 repair treats `compacted` as semantic-checkpoint metadata rather than line-trim authority, requires verified post-trim token evidence, deepens the compatibility trim ladder, and rebuilds `dist` from the repaired TS source.

Round-2 validation:

- focused: `5 files / 25 tests PASS`;
- full Python: `754 passed, 5 skipped, 38 subtests passed`;
- full Vitest: `96 files / 448 tests PASS`;
- build/evaluation/plugin validation/audit: PASS;
- evaluation evidence SHA-256: `51d56575225b9e1b10238b8c46b50113facf4de2ebc12b313c6d986dcea0535d`;
- packed plugin payload: `300` files;
- compiled dist inspection: deep v091 ladder + verified post-trim evidence gate present.

## Live round-2 acceptance — GREEN

Exact product candidate: `b116fa188d41d1acb8110e59fca4bf056a160643`.

Exact-SHA GitHub CI:

- Validate `36267805183`: SUCCESS;
- PS5.1 Acceptance Smoke `36267805207`: SUCCESS;
- Windows Installer Pack Smoke `36267805221`: SUCCESS.

Installed payload parity:

- source: `300` files / `7e66e09fc475959dfdb2d675debf168211aed1eb1d8713781a99d29d4f5d31cc`;
- installed: `300` files / the same fingerprint.

Live owner session: `agent:main:dashboard:cnx452-r2-live-hard`.

A preceding setup run used qualification-harness `--timeout 900` and therefore terminated at ~900 seconds before the final hard-pressure acceptance turn. This was a harness timeout, not a CNX-452 product failure; no duplicate retry was performed and durable state settled with no active call/outbox residue. The final acceptance used `--timeout 3600`.

Final hard-pressure Ticket:

- Ticket: `CNXT-20ab5f72-61e6-4003-b630-8504cceef59b`;
- run: `821c949a-22ff-49a9-8ebe-84a2a90fe578`;
- provider/model: `ollama/qwen3:1.7b`;
- before: `37808/40960 = 92.3%`, level `hard`;
- `context_pressure_hard_observed` occurred before inference;
- inline maintenance action: `hard-trim-200`;
- after: `23497/40960 = 57.4%`, level `normal`;
- `context_pressure_inline_resolved` occurred before `direct_model_call_started`;
- maintenance: `done`, `hard_required=1`, one attempt, no error;
- Direct recovery rows: `0`;
- model call outcome: `completed`, duration `156059 ms`;
- final marker: `CNX452_R2_HARD_OK`;
- completion: `stopReason=stop`;
- response durable, delivery confirmed exactly once, Ticket completed.

Post-acceptance runtime:

- SQLite integrity: `ok`;
- nonterminal Tickets: `0`;
- pending outbox: `0`;
- active Direct model calls: `0`;
- `OLLAMA_KEEP_ALIVE=6h` physically active.

## Current classification

`CNX452_HARD_CONTEXT_COMPACT_RESUME_GREEN`
