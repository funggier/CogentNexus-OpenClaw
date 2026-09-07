# CNX-20260907 — Full-Authority Hermes Handoff to Release

## Purpose

Continue CogentNexus-OpenClaw from the current authoritative GitHub state and complete the remaining work through final acceptance and release in one continuous Hermes session.

## Repository

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Current HEAD at handoff creation: `113974b1ec28f50506b1fd2dcbd18d37d638f6d7`
- Accepted installed candidate lineage: `36cd4c800ded28bdb7165fcad6e0bfb48b4e9335`

Always fresh-fetch the branch, `ACTIVE.md`, `STATUS.md`, and latest report before acting. GitHub repository and Actions are authoritative; do not trust stale SHA/status in this handoff when GitHub is newer.

## Read first

1. `docs/operations/coordination/ACTIVE.md`
2. `docs/operations/coordination/STATUS.md`
3. `docs/operations/coordination/reports/CNX-20260907-305-bounded-staging-installer-retry.md`
4. `docs/operations/coordination/reports/CNX-20260906-282-session-handoff-checkpoint.md`
5. The latest task/report chain referenced by the current coordination state.

## Current proven state

Task304 repository repair passed:

- focused installer contract tests: 10 passed
- installer/ownership regression: 48 passed
- full repository suite: 539 passed, 5 skipped, 4 subtests passed

Task305 staging adoption passed:

- supported installer invocation: exactly 1, exit code 0
- repaired `-SkipPlugin` postcondition emitted
- Task301 quiescence wiring installed byte-exact
- canonical launcher installed
- plugin was intentionally not installed/replaced; inventory reported version `0.9.3`, `enabled=false`, `status=disabled`
- Gateway HTTP 200
- Ollama HTTP 200
- Supervisor Enabled/Ready/Last Result 0
- SQLite integrity: ok
- Host mode `passthrough`, generation `62`
- backup created by installer
- no semantic send, replay, redelivery, disposition, manual durable-state mutation, protected-state mutation, or force push

Pending target state:

- target Ticket: `CNXT-87fc2030-884f-4943-bb6e-864cc621d5dc`
- target session key: `agent:main:discord:channel:1391855033993138217`
- target delivery: pending, generation 2
- delivery idempotency key: `cnxclaw-direct-result:CNXT-87fc2030-884f-4943-bb6e-864cc621d5dc:g2`
- attempts were high and delivery remained unconfirmed; investigate from durable evidence, never guess or replay

Protected state:

- Ticket: `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`
- owner session: `agent:main:discord:channel:1531199905673252946`

Do not touch it under any circumstances.

## Hermes authority

Hermes has full technical and operational authority to complete the project within the repository’s stated product goal and acceptance plan. Hermes may:

- choose implementation details and repair defects without micro-confirmation;
- create successor tasks and update coordination state;
- modify source, tests, CI, installer, documentation, and release automation;
- run bounded supported installation, activation, health, and requalification operations;
- make safe, reversible operational corrections when supported by evidence;
- continue through related defects instead of stopping for routine technical decisions;
- prepare and execute the documented release path once all acceptance gates pass.

Hermes must report the method, rationale, commands/actions, exact files and hashes, tests, workflow results, state transitions, and final disposition.

## Required execution path

1. Fresh-anchor current GitHub state.
2. Review Task305 independently and verify installed-vs-candidate identity.
3. Create/update a bounded successor task for managed activation and live requalification.
4. Preflight target/protected separation, Host mode, lease state, Gateway/Ollama/Supervisor health, worker identity, and no competing writer.
5. Use the supported managed activation path. Do not invent commands or manually copy files.
6. Invoke canonical `C:\\Users\\CDQ-P\\.openclaw\\workspace\\cnxclaw.cmd enable` only after exact preconditions pass, with the number of invocations explicitly recorded.
7. Verify quiescence lease acquisition/release, config transaction, rollback/restore behavior, Host managed state, plugin state, live worker identity, Gateway/Ollama/Supervisor health, and SQLite integrity.
8. Requalify the target lifecycle and durable delivery using exact Ticket/session-generation/idempotency evidence. Do not settle, replay, redeliver, or disposition a pending item merely because it is old or ambiguous.
9. Run the complete repository/Actions acceptance gates against the exact candidate.
10. Resolve version/tag/provenance from authoritative repository state.
11. Execute the documented release workflow only after all gates pass. Do not force-push, bypass checks, or publish an unverified candidate.
12. Publish a final report with exact HEAD, release/tag, artifact fingerprints, workflows, acceptance evidence, residual risks, and PASS/FAIL/BLOCKED.

## Decision policy

- Routine technical decisions: Hermes decides and proceeds.
- Repository/source/test/CI repair: continue autonomously using root-cause-first and TDD RED → minimal fix → GREEN.
- Supported reversible operational action: proceed when exact scope, preconditions, and readback are proven.
- Ambiguous durable state, protected state, semantic user-facing action, destructive cleanup, or release gate failure: stop the affected operation, preserve state, and report the evidence and next decision.
- Never convert a failed command into a success claim.
- Never repeat an external side effect without proving the prior attempt did not complete and the retry is safe.

## Standing prohibitions

- Do not touch protected Ticket/session above.
- Do not use `cnxclaw session cancel` as an OpenClaw Delete substitute.
- No guessed commands or manual SQLite/Ticket/session/transcript mutation.
- No blind replay/redelivery/disposition or duplicate semantic sends.
- No installer/uninstall/reset/restart outside a documented supported and task-scoped boundary.
- No force push, history rewrite, release bypass, or default-branch promotion without gates.
- Preserve prior sacrificial lineage unless separately justified and authorized.
- Keep Discord semantic-send budget explicit and use no new semantic send unless the acceptance task specifically requires it and exact authorization is recorded.

## Final handoff requirement

At completion, write an evidence-rich report and update `ACTIVE.md` and `STATUS.md`. If blocked, create the smallest successor task with the precise missing authority or repair, rather than leaving the session without a next action.
