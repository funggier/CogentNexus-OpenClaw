# Coordination Status

Status: `IN_PROGRESS`
State: `CNX444_V097_SUPERVISOR_DELIVERY_DISPATCH_LOCAL_GREEN_CANDIDATE_PENDING`
Task: `CNX-20260922-444-v097-gateway-interruption-direct-recovery.md`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Executor: `ChatGPT`

## Current phase

v0.9.7 development continues under CNX-444. Exact candidate `742248ca...` was installed over the live Windows machine and proved parity, active/MANAGED health, canonical Supervisor restoration, OpenClaw 2026.9.5 health, and `ollama/qwen3.8:27b` route preservation. The preserved durable response remained pending without any new inference. Live tracing then exposed a final wiring gap: canonical delivery wake authority was correct, but `host_v091.supervisor_tick()` routed that wake into the legacy health supervisor instead of the Host delivery bridge. A TDD repair now dispatches canonical assistant-delivery wakes directly to bounded `host_delivery.flush_deliveries()`. Full local qualification is GREEN. The next gate is a new exact candidate + exact-SHA CI + install-over + durable delivery settlement + fresh exactly-once recovery acceptance. v0.9.6 remains the published accepted baseline.

Final accepted candidate/tag SHA:

`db8433676c2412706ef3b3966c97e3509f2255c8`

Release workflow `35705294805` completed SUCCESS. Public `v0.9.6` is non-draft/non-prerelease, required assets are present, independent checksum verification passed, and `main` was fast-forwarded without force to the accepted release SHA before post-release coordination closeout.

## Accepted baseline carried forward

CNX-442 final physical Stop acceptance is GREEN. It must not be reopened or reinterpreted merely because release/docs work is continuing.

Validated/current live OpenClaw runtime baseline: `2026.9.5 (ec9c1a1)`.

Regression/dev OpenClaw dependency pin remains `2026.7.1-2` for repository test/development compatibility only; it is not the current live runtime baseline.

## Watcher retirement

The old Codex `CogentNexus coordination watch` automation and stale catalog/session entries were removed on 2026-09-21. Current coordination does not require or assume a persistent one-minute watcher.
