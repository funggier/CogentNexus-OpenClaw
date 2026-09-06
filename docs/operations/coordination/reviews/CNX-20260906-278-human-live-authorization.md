# CNX-20260906-278 — Human Live Authorization

## Decision

`AUTHORIZED_BOUNDED_EXACT_CANDIDATE_INSTALL_OVER`

On 2026-09-06 ICT, the human owner explicitly authorized Task278 in chat with:

`อนุญาต Task278`

## Exact candidate

`36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`

## Authorized scope

This authorization permits exactly one supported install-over of the exact accepted candidate from an exact candidate checkout/artifact, including only the installer-owned managed Gateway transition required by the supported installer.

After the installer completes, only read-only verification is authorized for:

- installed payload fingerprint/identity;
- Gateway health/version/listen/PID as observable;
- Ollama/provider reachability/readiness/model;
- CogentNexus Host/Supervisor health/state;
- durable-state preservation of the protected old Ticket and Task272 sacrificial session.

## Explicit exclusions

This authorization does not permit:

- Discord/Dashboard semantic sends;
- OpenClaw session Delete/reset;
- Ticket cancellation/disposition/replay/redelivery;
- manual SQLite mutation;
- uninstall/reset;
- ad-hoc process kills outside the supported installer;
- Scheduled Task mutation;
- release/tag/default-branch promotion;
- force push/history rewrite.

Task272's previously authorized session Delete/test-message path remains parked and separate and must not be consumed during Task278.

## Completion boundary

Hermes must publish a Task278 deployment report and stop for ChatGPT review before any later Task272 session Delete/recreation acceptance action.
