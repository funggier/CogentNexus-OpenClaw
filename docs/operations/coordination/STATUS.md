# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Execution mode:** `SINGLE_HERMES_EXECUTOR__TASK264_LIFECYCLE_IDENTITY_FENCE_REWORK`
**Updated:** 2026-09-05 ICT — ChatGPT completed Task263 review and opened Task264 rework
**Transport:** GitHub repository / Actions authoritative
**Active task:** `CNX-20260905-264`
**Parent:** `CNX-20260905-263`
**Parent umbrella:** `CNX-20260831-188`
**Disposition:** `TASK263_REWORK_REQUIRED__TASK264_READY_FOR_HERMES`

**Routine executor:** `Hermes`
**Current execution owner:** `Hermes`
**Review owner after report:** `ChatGPT`
**Protocol:** `docs/operations/coordination/HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`
**Delayed recheck:** `docs/operations/coordination/DELAYED_RECHECK_QUEUE.md`

## Task263 ChatGPT review

Review artifact:

`docs/operations/coordination/reviews/CNX-20260905-263-chatgpt-lifecycle-recreation-review.md`

Verdict:

`REWORK_REQUIRED__LIFECYCLE_IDENTITY_FENCE_INCOMPLETE`

Accepted evidence remains valid: Task263 migration/delete/recreation direction, TDD lineage, full local validation, exact-candidate CI 3/3, and no-live hard-fence compliance.

Blocking defect: once lifecycle `B` is active, `reactivateSessionForLifecycle()` returns the active owner state even for stale/different lifecycle `A`/`C`, while `session_start` treats active state as non-refusal. The test also expects stale `A` to see `state=active`, so it does not establish the required identity fence.

## Active Task264

`docs/operations/coordination/tasks/CNX-20260905-264-task263-lifecycle-identity-fence-rework.md`

Required repair:

- explicit lifecycle match/acceptance predicate;
- active B + B accepted idempotently;
- active B + A/C rejected without mutation;
- deleted A + B reactivates exactly once;
- deleted A + A rejected;
- migration-safe active NULL lifecycle behavior;
- `before_agent_run` fails closed when `ctx.sessionId` is not the current lifecycle for `ctx.sessionKey`;
- current lifecycle remains admitted;
- old-generation Ticket/recovery/delivery/workflow suppression unchanged.

Hermes must use RED -> minimal fix -> GREEN and exact-SHA CI. After report, state returns to `WAITING_FOR_CHATGPT_REVIEW`; no peer-bot review exists under the new standing model.

## Hard fences

No live OpenClaw session delete/reset, Discord/Dashboard semantic sends, manual live DB/recovery mutation, installer/Gateway lifecycle, release/tag/default-branch mutation, force push, or history rewrite is authorized by Task264.
