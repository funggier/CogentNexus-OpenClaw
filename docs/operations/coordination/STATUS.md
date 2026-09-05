# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Execution mode:** `SINGLE_HERMES_EXECUTOR__TASK269_HOST_ACTIONABLE_DURABLE_WORK_HINT_REPAIR`
**Updated:** 2026-09-06 ICT — ChatGPT accepted Task268 causal proof and opened Task269 source repair
**Transport:** GitHub repository / Actions authoritative
**Active task:** `CNX-20260906-269`
**Parent:** `CNX-20260905-268`
**Parent umbrella:** `CNX-20260831-188`
**Disposition:** `TASK268_CHATGPT_ACCEPTED_CAUSAL_PROOF__TASK269_OPEN`

**Routine executor:** `Hermes`
**Current execution owner:** `Hermes`
**Review owner after report:** `ChatGPT`
**Protocol:** `docs/operations/coordination/HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`
**Delayed recheck:** `docs/operations/coordination/DELAYED_RECHECK_QUEUE.md`

## Task268 accepted

Review:

`docs/operations/coordination/reviews/CNX-20260906-268-chatgpt-causal-root-review.md`

Verdict:

`ACCEPT_CAUSAL_PROOF__SOURCE_ACTIONABILITY_REPAIR_REQUIRED`

The user's recurring APPSTARTING/busy cursor is causally bound to the one-minute supervisor process wave: 6/6 natural ticks aligned, no off-cycle APPSTARTING occurred, and Gateway/Ollama PIDs remained stable.

The cadence is not itself the defect. The Host already has a lightweight idle fast path. The narrowed defect is that `durable_work_hint()` treats stale/non-due Direct durable state as actionable more broadly than the plugin's Direct-recovery eligibility contract.

Current Direct-recovery contract includes a 15-minute owner-session liveness fence, exact owner generation, active owner state, Direct-lane shape, due `next_attempt_at`, and model-call recovery fence. The live stale Ticket/recovery does not satisfy that recovery liveness contract but still wakes Host heavy reconciliation every minute.

## Task269

`docs/operations/coordination/tasks/CNX-20260906-269-host-actionable-durable-work-hint-repair.md`

Required repair:

- TDD RED first;
- stale/non-due Direct state must not wake heavy Host reconciliation;
- fresh exact-generation due Direct recovery must still wake;
- genuine durable workflow/delivery/recovery work must remain actionable;
- healthy steady state with only stale Direct evidence must return Host `idle` fast path;
- hard-hang recovery must not regress;
- preserve `PT1M` supervisor cadence.

The old Ticket remains read-only evidence. No cancel/redeliver/dispose/replay is authorized.

## Hard fences

No install, Gateway/provider lifecycle mutation, session Delete/reset, semantic send, live DB/recovery mutation, Scheduled Task mutation, process kill, release/tag/default-branch mutation, force push, or history rewrite is authorized by Task269.

After report: `WAITING_FOR_CHATGPT_REVIEW`.
