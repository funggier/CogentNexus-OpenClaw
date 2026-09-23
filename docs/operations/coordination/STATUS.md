# Coordination Status

Status: `IN_PROGRESS`
State: `CNX444_V097_INTERRUPTED_ATTEMPT_CLOSE_EXACT_SHA_GREEN_LIVE_REACCEPTANCE_PENDING`
Task: `CNX-20260922-444-v097-gateway-interruption-direct-recovery.md`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Executor: `ChatGPT`

## Current phase

v0.9.7 development continues under CNX-444. Durable delivery is now physically proven exactly once. A fresh real Direct interruption on `3c0db0c6...` also reached exactly-one recovery/result/delivery, but exposed that the canonical inference-attempt ledger remained active after the Direct call was interrupted. Current exact HEAD `036eef28842044499fec2588ab6c8605ad6bdd7c` repairs that boundary by ending only the exact matching active attempt and emitting `inference_attempt_ended`; exact-SHA Validate, PS5.1 Acceptance Smoke, and Windows Installer Pack Smoke are GREEN and the repaired source is installed. The next gate is one fresh post-`036eef` controlled interruption, not a replay of the consumed Tickets. See `reports/CNX-20260923-445-session-handoff-checkpoint.md`. v0.9.6 remains the published accepted baseline.

Final accepted candidate/tag SHA:

`db8433676c2412706ef3b3966c97e3509f2255c8`

Release workflow `35705294805` completed SUCCESS. Public `v0.9.6` is non-draft/non-prerelease, required assets are present, independent checksum verification passed, and `main` was fast-forwarded without force to the accepted release SHA before post-release coordination closeout.

## Accepted baseline carried forward

CNX-442 final physical Stop acceptance is GREEN. It must not be reopened or reinterpreted merely because release/docs work is continuing.

Validated/current live OpenClaw runtime baseline: `2026.9.5 (ec9c1a1)`.

Regression/dev OpenClaw dependency pin remains `2026.7.1-2` for repository test/development compatibility only; it is not the current live runtime baseline.

## Watcher retirement

The old Codex `CogentNexus coordination watch` automation and stale catalog/session entries were removed on 2026-09-21. Current coordination does not require or assume a persistent one-minute watcher.
