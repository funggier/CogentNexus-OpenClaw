# Current Project Status

**Updated:** 2026-09-21
**Active task:** CNX-443 — documentation convergence, MIT License, and v0.9.6 release
**Current source/release line:** v0.9.6
**Working branch:** `cnx-357-openai-dashboard-ticket-first-requalification-v2`
**Latest physical OpenClaw acceptance:** `2026.9.5 (ec9c1a1)`
**Regression/dev OpenClaw pin:** `2026.7.1-2`
**Managed provider:** Ollama
**Cloud/model/auth routing:** OpenClaw-owned pass-through
**License target:** MIT

## Current accepted runtime position

CNX-442 is final live GREEN. The accepted architecture now owns same-session queued input at the durable pre-dispatch boundary rather than allowing OpenClaw's follow-up queue to dequeue a cancelled successor after Stop.

Final live proof established:

- first owner Ticket bound to one physical Host run;
- second owner Ticket persisted and held before Host queue admission;
- second Ticket remained `bound_run_id=NULL` with zero model/inference activity;
- user Stop advanced generation exactly once;
- active + held Tickets became `cancelled`;
- held Ticket was silently consumed before Host queue admission;
- Host trajectory contained no successor run;
- no new `blocked by cogentnexus-openclaw` error appeared;
- Gateway/Discord remained healthy.

See `docs/CURRENT_STATE.md` and the final CNX-442 coordination report for exact evidence IDs.

## Current task: CNX-443

CNX-443 must:

1. audit every tracked Markdown file and separate current guidance from historical evidence;
2. converge current docs on v0.9.6 / CNX-442 / OpenClaw compatibility facts;
3. retire stale hard-coded branch/watch instructions;
4. add the MIT License;
5. align exact v0.9.6 release metadata and release tests/workflow;
6. run complete local/repository release gates;
7. publish and verify GitHub Release v0.9.6.

## Coordination model

The retired one-minute Codex `legacy coordination watch` automation has been removed. Do not recreate it from historical instructions.

Current execution model:

- ChatGPT performs repository/documentation/review work directly when tools permit.
- Hermes is used for bounded local/live execution when needed.
- `ACTIVE.md` / `STATUS.md` carry the current durable coordination task.
- Historical watcher/baton documents remain interpretable history but are not standing authority.

## Release topology

The current working branch includes the previous default-branch history plus the current development line. Release publication uses `.github/workflows/release.yml` with an exact validated candidate SHA.

No force push. Tag/release publication must fail closed if:

- v0.9.6 metadata disagree;
- required release notes are absent;
- exact candidate validation is not acceptable;
- tag/release already exists;
- package/checksum verification fails.

## Known boundaries still outside full production proof

- long high-concurrency soak;
- disk-full / DB-corruption hardening;
- universal exactly-once external side effects;
- arbitrary future OpenClaw versions beyond explicitly tested evidence.

Historical evidence remains in coordination tasks/reports/reviews and release notes; it is not rewritten merely to make old wording look current.
