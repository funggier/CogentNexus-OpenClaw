# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_ONE_SHOT_SUPPORTED_INSTALL_TASK093_095_SOURCE`
Current authorization: `TASK095_ACCEPTED_ONE_SHOT_LIVE_INSTALL_AUTHORIZED`
Task ID: `CNX-20260827-096`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260827-096-live-install-repaired-staging-and-restore-parity.md`](tasks/CNX-20260827-096-live-install-repaired-staging-and-restore-parity.md)

## Task 095 accepted

Implementation:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Report:

`1e66f8f563b9809cb823fdcd6ea69987a49861ad`

Independent decision: `ACCEPT`

Disposition:

`ACCEPT_WINDOWS_REPARSE_POINT_PAYLOAD_ATTESTATION_REPAIRED`

Review:

[`reviews/CNX-20260827-095-repair-windows-reparse-point-payload-attestation.md`](reviews/CNX-20260827-095-repair-windows-reparse-point-payload-attestation.md)

Publication fence is accepted. Task 095 closes the Windows junction/reparse-point gap while preserving Task-094 v2 fingerprint semantics and the Task-093 Dashboard durable-staging repair.

## Exact deploy source

Task 096 must deploy exactly:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Do not deploy a report/review/coordination HEAD.

Task-095 reported candidate v2 fingerprint:

`df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`

Recompute it before mutation rather than trusting old evidence.

## Task 096 one-shot contract

Exactly one supported normal install-over is authorized.

Before mutation Task 096 must prove with the real production classifier and action boundary:

- one coherent currently installed generation;
- live pre-Task093 payload v2 fingerprint differs from candidate;
- `mode=upgrade`;
- `pendingRollover=false`;
- `pluginAlreadyExact=false`;
- `installPlugin=true`;
- `rolloverPlugin=true`.

The one supported installer must then prove actual npm-pack package installation and ownership-safe rollover, converge to exactly one candidate-exact generation, restore MANAGED/startup/Supervisor/AGENTS/ownership/source parity and preserve unrelated OpenClaw/Ollama state.

Task 092 retired semantic Ticket/run/session/transcript evidence must remain unchanged. Do not assume Ticket count is zero; snapshot and prove Task 096 creates no new semantic rows.

## Hard live/semantic fence

Authorized live effect: exactly one normal supported install-over from the exact implementation SHA.

No retry, manual plugin lifecycle repair, manual generation deletion/move, ownership rewrite, reset/uninstall/cleanup, SQLite mutation, Task-092 repair, provider/model/timeout change, reboot, merge/tag/release or force push.

Task 096 sends zero semantic messages and performs zero direct Ollama/provider inference/probes.

## Required post-install gates

For PASS Task 096 must prove:

- real package install happened; not an already-exact no-op;
- final one-generation source/live v2 parity;
- MANAGED/startup/Supervisor/AGENTS/ownership/Gateway/SQLite/Ollama health;
- Task-092 retired evidence unchanged and no new semantic/provider activity;
- at least five natural PT1M ticks with `NO_FLASH_MULTI_TICK_REPROVEN`;
- authenticated Dashboard owner/control readiness with no send, token `DASHBOARD_OWNER_FRESH_SESSION_READY_NO_SEND`.

## Successor gate

Only independent acceptance of:

`PASS_REPAIRED_STAGING_LIVE_INSTALLED_PARITY_READY`

may authorize one new final authenticated fresh-session semantic attempt. That future task must use one brand-new nonce once, prove a genuinely fresh session, Ticket-before-provider ordering, durable payload staging, delivery settlement to `completed`, and a second New Session transition with no additional semantic/provider effect.