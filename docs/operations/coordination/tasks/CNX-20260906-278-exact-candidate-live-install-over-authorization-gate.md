# CNX-20260906-278 — Exact Candidate Live Install-Over Authorization Gate

## Status

`WAITING_FOR_HUMAN_AUTHORIZATION`

Parent: `CNX-20260906-277`
Executor after authorization: `Hermes`
Reviewer: `ChatGPT`

## Candidate

`36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`

## Requested live authority

After explicit human approval, perform exactly one supported install-over of the accepted candidate from an exact candidate checkout/artifact.

Authorized scope, if approved:

1. one supported install-over only;
2. installer-owned managed Gateway transition only as required by the supported installer;
3. post-install read-only fingerprint verification;
4. post-install read-only Gateway/Ollama/Host/Supervisor health checks;
5. read-only durable-state verification that the protected old Ticket and Task272 sacrificial session were not semantically disposed or manually mutated.

## Not authorized by this gate

- semantic Discord/Dashboard sends;
- OpenClaw session Delete/reset;
- Ticket cancellation/disposition/replay/redelivery;
- manual SQLite mutation;
- uninstall/reset;
- ad-hoc process kills outside the supported installer;
- Scheduled Task mutation;
- release/tag/default-branch promotion;
- force push/history rewrite.

Task272's prior Delete/test-message authority remains parked and separate.

## Completion after authorization

Hermes publishes a live deployment report with exact candidate, installer result, installed fingerprint, runtime health, durable-state preservation, and PASS/FAIL/BLOCKED, then stops for ChatGPT review before any Task272 session Delete/test message.
