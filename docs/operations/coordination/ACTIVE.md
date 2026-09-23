# Active Coordination

Status: `IN_PROGRESS`
State: `CNX444_V097_INTERRUPTED_ATTEMPT_CLOSE_EXACT_SHA_GREEN_LIVE_REACCEPTANCE_PENDING`
Task: `CNX-20260922-444-v097-gateway-interruption-direct-recovery.md`
Assigned executor: `ChatGPT`
Review owner: `ChatGPT independent final verification`
Human final authority: `Operator`
Working branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Current objective

CNX-444 is the v0.9.7 successor task. Repair the production continuity gap where a confirmed Gateway hard-hang restart physically interrupts an active Direct model call but leaves the CNX model-call lease `active`, preventing exact Direct recovery and eventually exposing the OpenClaw whole-run timeout.

The repair must use exact Gateway-interruption evidence and must not restore timer-only destructive recovery.

The exact `742248ca...` candidate was installed over the live machine with source/installed parity, active plugin state, canonical Supervisor restoration, OpenClaw 2026.9.5 health, and route preservation. That install proved the UTF-8 capture and age-independent wake repairs were present, but the preserved durable `CNX444_RECOVERY_OK` delivery still did not move: canonical wake classification returned delivery authority, while the production Supervisor fell through to the legacy heavy health path, which never invokes `host_delivery.flush_deliveries()`.

The durable-delivery path has now been physically settled exactly once, and a fresh controlled interruption on candidate `3c0db0c6...` recovered and delivered successfully. That fresh run exposed one remaining ledger defect: the original canonical `cnx_inference_attempt` stayed active after its Direct model call was authoritatively interrupted. Exact repair `036eef28842044499fec2588ab6c8605ad6bdd7c` closes only the matching active attempt inside the same quiesced classification transaction, fails closed on ambiguity, and records `inference_attempt_ended`. Exact-SHA CI is GREEN and the repaired source is installed. The next gate is one fresh post-`036eef` controlled interruption proving the canonical attempt closes exactly once before final lifecycle/release acceptance.

Durable reconnect checkpoint: `reports/CNX-20260923-445-session-handoff-checkpoint.md`.

## Current accepted predecessor

CNX-443 / v0.9.6 is complete and remains immutable. CNX-442 is also complete and final live GREEN.

Authoritative predecessor evidence:

- final production repair candidate: `8dee9cd635ca3dfcbf96f2f4161b5026355dbcf9`;
- final documentation acceptance commit: `aa46f7041ef32f00d34c4c5b72720d8552520775`;
- validated/current live OpenClaw runtime baseline: `2026.9.5 (ec9c1a1)`;
- no-successor Host run after authoritative Stop: accepted;
- held queued Ticket zero-inference cancellation: accepted.

## Coordination rule

The retired Codex `CogentNexus coordination watch` one-minute automation is not current authority and must not be recreated.

Use this file plus `STATUS.md`, the linked CNX-444 task, and `reports/CNX-20260922-444-v097-gateway-interruption-direct-recovery-report.md` as the current durable handoff.

Historical tasks/reports/reviews remain evidence only.

## Final CNX-443 release authority

- classification: `CNX443_V096_DOCUMENTATION_LICENSE_RELEASE_GREEN`;
- accepted release/tag SHA: `db8433676c2412706ef3b3966c97e3509f2255c8`;
- GitHub Release: `v0.9.6`, public, non-draft, non-prerelease;
- release workflow run: `35705294805`, SUCCESS;
- exact-SHA Validate / PS5.1 Acceptance Smoke / Windows Installer Pack Smoke: SUCCESS;
- physical lifecycle: install-over PASS, clean reinstall PASS, reset PASS, final same-version install-over PASS;
- live baseline: OpenClaw/Gateway `2026.9.5`, active/MANAGED, pending outbox zero;
- route preserved: `ollama/qwen3.8:27b`, OpenClaw-owned model/auth routing;
- release assets and independent SHA-256 verification: PASS;
- `main` was fast-forwarded without force to the accepted release SHA before this post-release coordination closeout.
