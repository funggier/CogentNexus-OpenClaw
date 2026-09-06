# CNX-20260906-278 — Exact Candidate Live Install-Over Authorization Gate

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260906-277`
Executor: `Hermes`
Reviewer: `ChatGPT`

## Candidate

`36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`

## Human authorization

Fresh human approval was explicitly granted in chat on 2026-09-06 ICT with the instruction:

`อนุญาต Task278`

Authorization record:

`docs/operations/coordination/reviews/CNX-20260906-278-human-live-authorization.md`

Decision:

`AUTHORIZED_BOUNDED_EXACT_CANDIDATE_INSTALL_OVER`

## Authorized live scope

Hermes may now:

1. perform exactly one supported install-over of the accepted candidate from an exact candidate checkout/artifact;
2. allow only the installer-owned managed Gateway transition required by the supported installer;
3. perform post-install read-only installed-payload fingerprint verification;
4. perform post-install read-only Gateway/Ollama/Host/Supervisor health checks;
5. perform read-only durable-state verification that the protected old Ticket and Task272 sacrificial session were not semantically disposed, replayed, redelivered, cancelled, reset, Deleted, or manually mutated;
6. publish a live deployment report with exact candidate, installer result, installed fingerprint, runtime health, preservation evidence, and PASS/FAIL/BLOCKED;
7. stop for ChatGPT review before any Task272 Delete/recreation acceptance resumes.

## Not authorized

- semantic Discord/Dashboard sends;
- OpenClaw session Delete/reset;
- Ticket cancellation/disposition/replay/redelivery;
- manual SQLite mutation;
- uninstall/reset;
- ad-hoc process kills outside the supported installer;
- Scheduled Task mutation;
- release/tag/default-branch promotion;
- force push/history rewrite.

Task272's prior Delete/test-message authority remains parked and separate. Do not consume it during Task278.

## Completion

Publish:

`docs/operations/coordination/reports/CNX-20260906-278-exact-candidate-live-install-over.md`

Then set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop.
