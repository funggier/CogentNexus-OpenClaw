# CogentNexus Coordination Layer

GitHub remote coordination state is the durable handoff surface between Hermes, ChatGPT, and the human operator.

## Canonical standing model

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Current authority: remote `ACTIVE.md` + `STATUS.md`
- Default repository-capable executor/coordinator/reviewer: **ChatGPT**
- Local/live machine executor: **Hermes**
- Async dependency behavior: **persistent delayed self-recheck; GitHub Actions default 5 minutes**
- Human operator: final authority

Read `SESSION_EXECUTION_MODEL_GUIDELINES.md` first for current operator workflow preferences. When Hermes is assigned, use `HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`; use `DELAYED_RECHECK_QUEUE.md` for CI/external waits.

`HERMES_DUAL_AGENT_BATON_PROTOCOL.md` is retained for historical interpretation only. Its Luna/Musethree alternating baton no longer governs new work after the single-agent protocol publication commit.

## Intended loop

```text
ChatGPT / human defines or updates the goal
    -> if ChatGPT can safely execute with current tools: ChatGPT does the work directly
    -> if local/live machine access is required: bounded Hermes task
       -> same task/phase: prefer same Hermes session
       -> new task/phase: prefer a fresh Hermes session bootstrapped from GitHub
    -> Hermes report when Hermes was required
    -> WAITING_FOR_CHATGPT_REVIEW
    -> ChatGPT independent review / direct successor work
       -> ACCEPT / REWORK / bounded successor
       -> missing human authority -> WAITING_FOR_USER_AUTHORITY
       -> final goal -> ChatGPT final acceptance
```

## Standing documents

- `SESSION_EXECUTION_MODEL_GUIDELINES.md` — current operator preferences for ChatGPT-first execution, Hermes session reuse/new-session choice, and model-strength escalation.
- `HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md` — Hermes execution/review/successor rules when a Hermes task is assigned.
- `DELAYED_RECHECK_QUEUE.md` — persistent five-minute CI/external wait queue, stale-wake, dedupe, retry, and stalled-CI rules.
- `EXECUTION_OWNERSHIP.md` — ownership/race/live-authority boundaries.
- `EXECUTOR_ANALYSIS_REVIEW_MODEL.md` — Hermes execution + ChatGPT independent-review model.
- `EXECUTOR_REPORT_CONTRACT.md` — report/evidence interface.
- `CODEX_BOOTSTRAP.md` — Hermes startup rules.
- `WATCH_MODE.md` — unattended Hermes task pickup and wait-owner rechecks.
- `PROBLEM_LOOP.md` — blocker handling.
- `SIGNALS.md` — operator signals.
- `HERMES_DUAL_AGENT_BATON_PROTOCOL.md` — historical dual-agent protocol; superseded for future work.

## Key invariants

- ChatGPT should directly perform repository/source/review/documentation work it can safely complete with current tools.
- Hermes is reserved primarily for local/live/environment-specific execution that ChatGPT cannot perform.
- Hermes never independently accepts its own completed report.
- ChatGPT reviews Hermes reports and owns acceptance/rework/successor framing.
- Prefer a fresh Hermes session for a new bounded task/phase; reuse the existing Hermes session for direct continuation where local context materially helps.
- ChatGPT should proactively flag when a task is too complex for a lighter model and recommend a stronger reasoning model.
- Remote GitHub truth outranks local checkout and conversational memory.
- Source/test/CI work may continue autonomously within the active task authority.
- Waiting for queued/in-progress CI does not terminate the task; Hermes retains ownership and self-wakes.
- Every delayed wake starts with fresh remote authority and is discarded if stale.
- Five-minute polling must not multiply scheduled jobs or create heartbeat commits.
- Live/destructive/semantic actions still require explicit bounded task authority.
- Unknown user intent is never inferred.
- No force push.
- No duplicated external side effect after a matching completion report.

## Typical states

```text
READY_FOR_HERMES
    -> Hermes executes assigned task

WAITING_FOR_CI_RECHECK
    -> Hermes retains task ownership
    -> persistent wake ~5 min
    -> success: resume task
    -> still pending: enqueue next ~5 min wake
    -> failure: diagnose/repair, do not blind-wait

CI_STALLED_DIAGNOSIS
    -> bounded diagnosis + continued recheck if legitimately active

WAITING_FOR_CHATGPT_REVIEW
    -> Hermes task/report complete
    -> no further Hermes mutation of that completed task
    -> ChatGPT independently reviews

WAITING_FOR_USER_AUTHORITY
    -> required live/destructive/semantic/fresh-intent authority is missing

GOAL_COMPLETE_PENDING_CHATGPT_FINAL
    -> historical state may still exist; under current model ChatGPT performs final acceptance when present
```

Exact task-specific tokens may be more descriptive, but `Assigned executor`, `Review owner`, and any wait owner must make ownership unambiguous.

## Report/review rule

Hermes publishes an evidence-rich final report only after required acceptance gates are terminal. ChatGPT verifies critical claims independently before accepting or opening a successor.

A task may record an interim wait state while CI is pending, but that is not a final PASS report and not a ChatGPT-review handoff.

When new human intent or wider disruptive authority is required, neither Hermes nor ChatGPT may invent it; the missing authority is surfaced explicitly to the human operator.

## Historical compatibility

Completed historical tasks/reports/reviews remain valid. Luna/Musethree actor labels and dual-agent handoffs remain factual history, but the single Hermes + ChatGPT model governs prospectively from its publication commit.
