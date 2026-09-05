# CogentNexus Coordination Layer

GitHub remote coordination state is the durable handoff surface between Luna, Musethree, ChatGPT, and the human operator.

## Canonical standing model

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Current authority: remote `ACTIVE.md` + `STATUS.md`
- Primary agent: **Luna**
- Supporting/alternate agent: **Musethree**
- Routine workflow: **alternating peer baton**
- Async dependency behavior: **persistent delayed self-recheck; GitHub Actions default 5 minutes**
- ChatGPT: **escalation/adjudication/final-acceptance layer**
- Human operator: final authority

Read `HERMES_DUAL_AGENT_BATON_PROTOCOL.md` first and `DELAYED_RECHECK_QUEUE.md` for CI/external waits. They supersede older language that requires ChatGPT review or a human wake between every future task.

## Intended loop

```text
Luna task
  -> CI pending? self-wake every ~5 min until terminal
  -> Luna report -> handoff Musethree
Musethree review
  -> CI pending? self-wake every ~5 min until terminal
  -> Musethree successor/task -> report -> handoff Luna
Luna review -> successor/task -> ... repeat ...

cannot safely decide / needs new authority
    -> WAITING_FOR_CHATGPT
    -> tell human to notify ChatGPT

final overall goal reached
    -> GOAL_COMPLETE_PENDING_CHATGPT_FINAL
    -> tell human to notify ChatGPT
```

## Standing documents

- `HERMES_DUAL_AGENT_BATON_PROTOCOL.md` — authoritative actor alternation, handoff, successor, escalation, and final-completion rules.
- `DELAYED_RECHECK_QUEUE.md` — persistent five-minute CI/external wait queue, stale-wake, dedupe, retry, and stalled-CI rules.
- `EXECUTION_OWNERSHIP.md` — ownership/race/live-authority boundaries.
- `EXECUTOR_ANALYSIS_REVIEW_MODEL.md` — evidence and independent peer-review model.
- `EXECUTOR_REPORT_CONTRACT.md` — report/evidence interface.
- `CODEX_BOOTSTRAP.md` — Hermes startup rules.
- `WATCH_MODE.md` — unattended baton pickup and wait-owner rechecks.
- `PROBLEM_LOOP.md` — blocker handling.
- `SIGNALS.md` — operator signals.

## Key invariants

- Luna is primary/default entry actor, but only current baton ownership grants mutation authority.
- Actors alternate; the receiving peer reviews predecessor work before continuing.
- No actor independently accepts its own report.
- Remote GitHub truth outranks local checkout and conversational memory.
- Source/test/CI work may continue autonomously within active authority.
- Waiting for queued/in-progress CI does not terminate the task; the current actor retains baton and self-wakes.
- Every delayed wake starts with fresh remote authority and is discarded if stale.
- The same wait identity is deduplicated; five-minute polling must not multiply scheduled jobs or create heartbeat commits.
- Live/destructive/semantic actions still require explicit bounded task authority.
- Unknown user intent is never inferred.
- No force push.
- No duplicated external side effect after a matching completion report.
- If the peer cannot select one safe authorized continuation, escalate instead of guessing.

## Handoff and wait states

Typical conceptual states:

```text
READY_FOR_LUNA / READY_FOR_MUSETHREE
    -> assigned execution

WAITING_FOR_CI_RECHECK
    -> same actor retains baton
    -> persistent wake ~5 min
    -> success: resume task
    -> still pending: enqueue next ~5 min wake
    -> failure: diagnose/repair, do not blind-wait

CI_STALLED_DIAGNOSIS
    -> bounded diagnosis + continued recheck if legitimately active

report complete
    -> HANDOFF_TO_MUSETHREE / HANDOFF_TO_LUNA
    -> peer review
    -> accepted successor/rework assigned to receiving peer
    -> execution

WAITING_FOR_CHATGPT
    -> no further autonomous project mutation

GOAL_COMPLETE_PENDING_CHATGPT_FINAL
    -> no invented extra work; human notifies ChatGPT
```

Exact task-specific tokens may be more descriptive, but `Assigned executor`, `Handoff from`, `Next actor`, and any wait owner must make ownership unambiguous.

## Report/review rule

The executing actor publishes an evidence-rich final report only after required acceptance gates are terminal. The peer verifies critical claims and publishes the independent review. The peer may then open/execute the next bounded task when the continuation is deterministic and already authorized by project intent/policy.

A task may record an interim wait state while CI is pending, but that is not a final PASS report and not a peer handoff.

When a new architecture/semantic choice, fresh human consent, or wider disruptive authority is required, the peer must not invent it; escalate to ChatGPT.

## Historical compatibility

Completed historical tasks/reports/reviews remain valid. The dual-agent baton and delayed-recheck model applies prospectively from their publication commits.
