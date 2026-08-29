# ChatGPT Session Handoff

Updated: 2026-08-30 ICT

This file lets a new ChatGPT conversation recover active CogentNexus development context from GitHub instead of depending on a previous chat context window.

## Bootstrap instruction for a new ChatGPT conversation

The operator can say:

```text
ต่อ CogentNexus จาก GH coordination
```

The new ChatGPT conversation should read, in this order:

1. `docs/operations/coordination/README.md`
2. `docs/operations/coordination/EXECUTION_OWNERSHIP.md`
3. `docs/operations/coordination/SIGNALS.md`
4. current remote branch HEAD for the named stabilization branch
5. `docs/operations/coordination/ACTIVE.md` from that remote revision
6. `docs/operations/coordination/STATUS.md` from that remote revision
7. the active task referenced by `ACTIVE.md`
8. the matching report under `docs/operations/coordination/reports/`, if present
9. the matching review under `docs/operations/coordination/reviews/`, if present
10. `docs/operations/STATUS.md`, `ROADMAP.md`, `WORKLOG.md`, and `DECISIONS.md` as supporting narrative/context

GitHub remote coordination state is the durable handoff authority. Do not infer current task identity from this handoff file, an older chat, a default branch, or an arbitrary local checkout.

## Current coordination model

The human conversation remains primarily in ChatGPT.

ChatGPT is coordinator/reviewer **and the default repository-capable executor**. When repository/source/test/CI evidence is sufficient, ChatGPT should directly diagnose, implement, run/inspect GitHub CI, review, and record durable evidence without creating an unnecessary machine task.

Hermes/Codex is the **local/live executor**. ChatGPT creates a narrow task when proof/action genuinely requires the operator's real machine, live runtime, supported installer lifecycle, filesystem/runtime state, Dashboard/browser interaction, hardware/device integration, permissions, or another environment-specific boundary.

See `EXECUTION_OWNERSHIP.md` for the exact escalation and race-prevention policy.

## Dynamic active task rule

This file intentionally does **not** name a fixed current Task ID. `ACTIVE.md` and `STATUS.md` on the verified remote working branch are the only current coordination gates.

A new session must not preserve an old task pointer here. This prevents session handoff documentation from becoming a stale authority.

## Remote-vs-local rule

A local clone/worktree is never authoritative merely because it exists on the operator's machine.

Before judging coordination state:

- fetch the named working branch from GitHub;
- verify remote HEAD;
- read remote `ACTIVE.md` / `STATUS.md`;
- compare local worktree state only afterward.

If a local checkout is stale, do not ask ChatGPT to rewrite already-current remote gates. If local work is uncertain/uncommitted, preserve it and use a fresh clone/worktree rather than destructive reset.

## Continuation rule

A new ChatGPT session should not ask the operator to restate project history before checking GitHub coordination state.

Then:

- if the active work is repository-capable, ChatGPT should continue it directly where safe;
- if a matching executor report exists, review it before creating successor work;
- if an active `READY_FOR_HERMES` task requires local/live evidence and has no completed matching report, the operator may signal Hermes/Codex with `ต่อ`;
- do not duplicate an already-running executor's production changes; observe/review until the report or explicit ownership transition.
