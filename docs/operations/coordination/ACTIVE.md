# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SINGLE_HERMES_EXECUTOR__TASK279_MANAGED_REENTRY_OR_BOUNDED_REINSTALL_RECOVERY`
Current disposition: `HUMAN_AUTHORIZED__PREFER_ENABLE__REINSTALL_IF_PROVEN_NECESSARY`
Task ID: `CNX-20260906-279`
Parent task: `CNX-20260906-278`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-06 ICT — human authorized Task279 recovery, including supported reinstall/install-over of the exact candidate only if evidence proves it necessary; human also directed final release after all acceptance gates pass

Assigned executor: `Hermes`
Review owner after report: `ChatGPT`
Coordination protocol: `docs/operations/coordination/HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`

## Accepted candidate

`36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`

## Human authorization

`docs/operations/coordination/reviews/CNX-20260906-279-human-recovery-and-final-release-authorization.md`

## Active Task279

`docs/operations/coordination/tasks/CNX-20260906-279-managed-reentry-after-partial-install.md`

Hermes shall use root-cause-first ordering: re-prove exact payload/ownership/PASSTHROUGH health, prefer one canonical `cnxclaw.cmd enable` if valid, and use at most one supported reinstall/install-over of the same exact candidate only if evidence proves enable alone is not sufficient or a single enable attempt fails into a coherent reinstallable state.

Task272 session Delete/test-message authority remains parked and separate. No semantic send, session Delete/reset, Ticket/recovery disposition, manual SQLite mutation, clean uninstall/reset, broad cleanup, release promotion during Task279, or force push is authorized.

The human has conditionally authorized release as the final closing action after all final acceptance gates pass. That release occurs only in a later bounded release task after independent final acceptance.
