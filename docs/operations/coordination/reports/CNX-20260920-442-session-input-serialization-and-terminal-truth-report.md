# CNX-20260920-442 — Session Input Serialization and Terminal Truth Report

Status: `SOURCE_QUALIFIED`

Classification:

`CNX442_SESSION_SERIALIZATION_TERMINAL_TRUTH_SOURCE_GREEN`

## Trigger

A live owner turn on Discord run `673cb634-58e2-4706-94d8-0a45e7740784` failed after native `/context` changed the same session transcript during the active run. OpenClaw ended the run with:

`SQLite transcript changed while preparing rewrite for 06e736f1-01e5-45b7-8c0b-bbaa9ed6f700`

CNX had already recorded the owning Ticket as `completed` even though no final assistant answer was delivered.

Two native command turns (`/context`, `/context detail`) were also admitted as conversational CNX Tickets.

## Repair

CNX-442 makes the contract provider- and surface-independent.

### Native command bypass

`reply_dispatch` now excludes Host-native commands before CNX Ticket admission. OpenClaw command facts and its own command detector are used; ordinary text that merely resembles a slash command is not excluded.

### Same-session serialization

Owner conversational sessions use OpenClaw's supported session API and are normalized to:

`queueMode=followup`

This applies to eligible owner sessions regardless of Discord, Dashboard/WebChat, or another supported ingress sharing the same session pipeline. Internal/subagent/cron-style sessions remain excluded.

### Authoritative terminal truth

CNX no longer treats `agent_end success` as sufficient proof that an owner Ticket completed when user-visible delivery is unresolved.

The reconciler reads exact per-run `session.ended` evidence from the owning agent's Host database:

`<agent-dir>\openclaw-agent.sqlite`

The implementation intentionally does not use `session.resolveStorePath()` for this proof because OpenClaw 2026.9.5 resolves that surface to legacy `sessions.json`, not the trajectory SQLite database.

Semantics:

- Host success + visible assistant output: existing durable delivery/receipt path remains authoritative.
- Host success + no visible output: complete only after Host terminal success, without emitting duplicate `response_ready`.
- Host terminal error before confirmed delivery: retract unconfirmed response-ready state and atomically create Direct Recovery.
- confirmed or transport-accepted delivery evidence: fail closed as a conflict; do not rewrite user-visible history.

## Status UI

Operator decision: out of scope. No changes were made to decorative host status phrases such as `Cracking…` or `Shelling…`.

## Validation

- CNX-442 focused suite: 13 PASS;
- CNX-440 + Discord/WebChat durable delivery: 11 PASS;
- CNX-427 + reply-dispatch/Ticket-first admission: 22 PASS;
- Host claim/session ingress fences: 8 PASS;
- index integration: 42 PASS;
- v0.9.5 behavior/delivery/session/no-reply matrix: 21 PASS.

Total targeted/integration regressions:

`117 PASS`

Additional qualification:

- `npm run plugin:validate` — PASS;
- TypeScript/plugin build — PASS;
- mixed-plugin artifact verification — PASS;
- Ticket DB bootstrap — PASS;
- package contents verification — PASS (278 packed files);
- `git diff --check` — PASS.

## Live deployment state

Not yet installed at the time of this source-qualified report section.

Next gate is one supported install-over from the exact committed candidate, followed by read-only/live runtime qualification. No semantic Discord message will be sent by the executor.
