# CogentNexus Coordination Layer

GitHub remote coordination state is the durable handoff surface between Luna, Musethree, ChatGPT, and the human operator.

## Canonical standing model

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Current authority: remote `ACTIVE.md` + `STATUS.md`
- Primary agent: **Luna**
- Supporting/alternate agent: **Musethree**
- Routine workflow: **alternating peer baton**
- ChatGPT: **escalation/adjudication/final-acceptance layer**
- Human operator: final authority

Read `HERMES_DUAL_AGENT_BATON_PROTOCOL.md` first. It supersedes older language that requires ChatGPT review between every future task.

## Intended loop

```text
Luna task -> Luna report -> handoff Musethree
Musethree review -> Musethree successor/task -> Musethree report -> handoff Luna
Luna review -> Luna successor/task -> Luna report -> handoff Musethree
... repeat ...

cannot safely decide / needs new authority
    -> WAITING_FOR_CHATGPT
    -> tell human to notify ChatGPT

final overall goal reached
    -> GOAL_COMPLETE_PENDING_CHATGPT_FINAL
    -> tell human to notify ChatGPT
```

## Standing documents

- `HERMES_DUAL_AGENT_BATON_PROTOCOL.md` — authoritative actor alternation, handoff, successor, escalation, and final-completion rules.
- `EXECUTION_OWNERSHIP.md` — ownership/race/live-authority boundaries.
- `EXECUTOR_ANALYSIS_REVIEW_MODEL.md` — evidence and independent peer-review model.
- `EXECUTOR_REPORT_CONTRACT.md` — report/evidence interface.
- `CODEX_BOOTSTRAP.md` — Hermes startup rules.
- `WATCH_MODE.md` — unattended baton pickup.
- `PROBLEM_LOOP.md` — blocker handling.
- `SIGNALS.md` — operator signals.

## Key invariants

- Luna is primary/default entry actor, but only current baton ownership grants mutation authority.
- Actors alternate; the receiving peer reviews predecessor work before continuing.
- No actor independently accepts its own report.
- Remote GitHub truth outranks local checkout and conversational memory.
- Source/test/CI work may continue autonomously within active authority.
- Live/destructive/semantic actions still require explicit bounded task authority.
- Unknown user intent is never inferred.
- No force push.
- No duplicated external side effect after a matching completion report.
- If the peer cannot select one safe authorized continuation, escalate instead of guessing.

## Handoff states

Typical conceptual states:

```text
READY_FOR_LUNA / READY_FOR_MUSETHREE
    -> assigned execution
    -> report
HANDOFF_TO_MUSETHREE / HANDOFF_TO_LUNA
    -> peer review
    -> accepted successor/rework assigned to receiving peer
    -> execution

WAITING_FOR_CHATGPT
    -> no further autonomous project mutation

GOAL_COMPLETE_PENDING_CHATGPT_FINAL
    -> no invented extra work; human notifies ChatGPT
```

Exact task-specific tokens may be more descriptive, but `Assigned executor`, `Handoff from`, and `Next actor` must make baton ownership unambiguous.

## Report/review rule

The executing actor publishes an evidence-rich report. The peer verifies critical claims and publishes the independent review. The peer may then open/execute the next bounded task when the continuation is deterministic and already authorized by project intent/policy.

When a new architecture/semantic choice, fresh human consent, or wider disruptive authority is required, the peer must not invent it; escalate to ChatGPT.

## Historical compatibility

Completed historical tasks/reports/reviews remain valid. The dual-agent baton model applies prospectively from its publication commit.
