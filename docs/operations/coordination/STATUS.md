# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Execution mode:** `SINGLE_HERMES_EXECUTOR__TASK278_EXACT_CANDIDATE_LIVE_INSTALL_OVER`
**Updated:** 2026-09-06 ICT — human explicitly authorized Task278 for one supported install-over of the exact accepted candidate
**Transport:** GitHub repository / Actions authoritative
**Active task:** `CNX-20260906-278`
**Parent:** `CNX-20260906-277`
**Parent umbrella:** `CNX-20260831-188`
**Disposition:** `HUMAN_AUTHORIZED__EXACT_CANDIDATE_INSTALL_OVER_READY`

**Routine executor:** `Hermes`
**Current execution owner:** `Hermes`
**Review owner after report:** `ChatGPT`
**Protocol:** `docs/operations/coordination/HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`

Accepted candidate: `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`.

Human authorization is recorded at:
`docs/operations/coordination/reviews/CNX-20260906-278-human-live-authorization.md`

Hermes may execute exactly one supported install-over from an exact candidate checkout/artifact, including only installer-owned managed Gateway transition required by the supported installer. Afterward Hermes must verify installed fingerprint and Gateway/Ollama/Host/Supervisor health read-only, verify the protected old Ticket and Task272 sacrificial session were not semantically disposed or manually mutated, publish PASS/FAIL/BLOCKED, and stop for ChatGPT review.

Not authorized: semantic sends, OpenClaw session Delete/reset, Ticket cancellation/disposition/replay/redelivery, manual SQLite mutation, uninstall/reset, ad-hoc process kills outside the supported installer, Scheduled Task mutation, release/tag/default-branch promotion, or force push/history rewrite.

Task272 live session Delete/test-message authority remains parked and unconsumed.
