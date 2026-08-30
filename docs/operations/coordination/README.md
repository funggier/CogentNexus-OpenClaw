# CogentNexus Coordination Layer

This directory is the GitHub-based handoff surface between ChatGPT, **Hermes/Codex**, and the human operator.

GitHub is the durable coordination source of truth. Local execution remains on the operator's machine only through the exact executor and permissions authorized by an active task.

See [`EXECUTION_OWNERSHIP.md`](EXECUTION_OWNERSHIP.md) for the standing rule that repository/source/test/CI work stays with ChatGPT by default and Hermes/Codex is reserved for irreducibly local/live proof or an explicit operator-requested handoff.

## Canonical current contract

- Repository: `funggier/CogentNexus-OpenClaw`
- Current stabilization branch: `agent/v0.9.3-full-stabilization`
- READY gate: `READY_FOR_HERMES`
- Executor role: `Hermes/Codex`
- Manual trigger: `ต่อ`
- ChatGPT owns tasks, reviews, `ACTIVE.md`, and `STATUS.md`
- ChatGPT may directly execute repository/source/test/CI work when GitHub evidence is sufficient
- ChatGPT may review its own repository-capable work through a distinct durable self-review checkpoint when operator policy permits
- Hermes/Codex owns matching local/live execution reports when a handoff is actually required
- Human operator remains final authority

`READY_FOR_HERMES` is an executor handoff gate, not a requirement that every development or review step pass through Hermes/Codex.

## Intended loop

The default loop is hybrid:

```text
Human talks primarily with ChatGPT
        ↓
ChatGPT reads GitHub and performs repository-capable work directly
(source / tests / docs / CI / review)
        ↓
Does the current result need a review checkpoint?
        ├─ yes → ChatGPT records a durable review checkpoint
        │          (self-review is explicitly labeled when ChatGPT also executed the work)
        └─ no  → continue within the active task contract
        ↓
Is real-machine/live proof or an explicit operator-requested handoff required?
        ├─ no → ChatGPT continues from durable GitHub evidence
        └─ yes
             ↓
        ChatGPT publishes narrow active task
             ↓
        ACTIVE.md = READY_FOR_HERMES
             ↓
        Human sends authorized executor: ต่อ
             ↓
        Hermes/Codex synchronizes remote GitHub and executes exact task
             ↓
        Executor pushes matching report/evidence references
             ↓
        ChatGPT reviews and publishes next disposition
```

The human is a trigger and final authority, not a courier for task details or logs.

## Optional continuous watch loop

For repeated local execution, an authorized executor may use the Scheduled-task mode defined in [`WATCH_MODE.md`](WATCH_MODE.md).

Continuous execution never bypasses task-specific safety gates, invents tasks, or repeats completed side effects.

## Ownership model

- **ChatGPT owns**
  - `ACTIVE.md`
  - `STATUS.md`
  - `tasks/*.md`
  - `reviews/*.md`
  - repository-capable diagnosis, source/test/docs/CI repair, exact-SHA CI inspection, and durable review checkpoints
- **Hermes/Codex owns**
  - `reports/*.md` for delegated machine/local/live execution
  - only source/runtime changes explicitly authorized by the active task
- **Human operator** may intervene anywhere and is the final authority.

The executor should not rewrite task specifications merely to reflect progress. Progress/results belong in the matching report.

## Review identity and self-review policy

Reviewer identity separation is not a standing requirement for repository-capable work.

ChatGPT may execute and review the same repository-capable task when the operator has allowed that workflow, provided that:

- the review is recorded as a distinct durable Task/Review checkpoint;
- the review cites exact commits, tests, CI runs, reports, or other durable evidence sufficient for the disposition;
- the review identifies itself as `ChatGPT self-review` when ChatGPT also executed the work;
- a same-actor review is never described as `independent`;
- task safety fences, acceptance criteria, evidence thresholds, exact-SHA requirements, and fail-closed behavior are unchanged;
- a separate reviewer is used when the active task or operator explicitly requires one.

Do not create a Hermes/Codex handoff solely to manufacture reviewer identity separation. Hermes/Codex should be used when real-machine/live proof is irreducible, when an authorized action needs that executor surface, or when the operator explicitly requests the handoff.

## Diagnosis, fix, and proof ownership

The default technical-role split is:

- **ChatGPT leads and executes repository-capable cause/fix work** when durable repository evidence and CI are sufficient.
- **Hermes/Codex executes local/live proof** when machine access, current runtime state, GUI, hardware, permissions, or disruptive lifecycle behavior is essential, or when the operator explicitly requests that handoff.
- ChatGPT should not create an executor task merely to run work that GitHub Actions can prove adequately or merely to obtain a different reviewer identity.
- Contrary machine evidence overrides a repository hypothesis. The executor records the contradiction without broadening authority; ChatGPT revises the task/disposition.

See [`EXECUTION_OWNERSHIP.md`](EXECUTION_OWNERSHIP.md) for escalation and race-prevention rules.

## Task identity

Every delegated task has a stable ID such as:

```text
CNX-20260822-001
```

The same ID is used across `tasks/`, `reports/`, and `reviews/`.

Repository-only ChatGPT work does not need an artificial Hermes task/report cycle when commits + exact-SHA CI + durable review evidence are sufficient.

## Handoff state model

```text
READY_FOR_HERMES
    ↓ manual signal: ต่อ OR authorized AUTO pickup
EXECUTING
    ↓ report pushed
REPORT_READY
    ↓ ChatGPT review
CHATGPT_REVIEWING
    ↓
READY_FOR_HERMES | CLOSED | BLOCKED
```

`ACTIVE.md` is the single pointer to the current delegated executor handoff state/task.

The executor must not repeat a task whose report already records completion. If `ACTIVE.md` is not `READY_FOR_HERMES`, synchronize, report/read status as appropriate, and stop unless the active task explicitly authorizes another action.

## Remote authority rule

The current remote stabilization branch is authoritative. A local checkout is only a working copy.

Hermes/Codex must fetch the named remote branch and verify its remote HEAD before using local `ACTIVE.md` or `STATUS.md` as authority. If local state is stale or uncertain, prefer a fresh worktree/clone; do not reset away uncommitted work and never force-push to solve freshness.

## Minimal human signals

See [`SIGNALS.md`](SIGNALS.md).

`ต่อ` means: synchronize current remote GitHub coordination truth, read the active task/report/safety gates, execute only the exact authorized READY task, publish its report, and stop for review.

`สถานะ` is read-only coordination status. `หยุด` means do not begin a new coordination task.

## Problem resolution

See [`PROBLEM_LOOP.md`](PROBLEM_LOOP.md).

A safe stop must not become a silent dead end. The executor publishes the matching problem report; ChatGPT reviews it, classifies the blocker, and selects the narrowest safe next disposition or an exact human-decision gate.

## Progress communication contract

During a running delegated task:

- announce objective/current phase at execution start;
- provide meaningful progress at milestones and before/after authorized mutations;
- report blockers immediately;
- expose actions/evidence/outcomes, not private reasoning;
- in AUTO mode continue unless a safety/authority/permission/required-information gate blocks execution;
- finish with actions taken, evidence, side effects, remaining unproven items, and durable next state.

## Evidence rule

Evidence must distinguish what was executed, what was observed, what commit/run/report records the result, and what remains unproven. Do not convert assumptions into PASS.

For disruptive tests, preserve the task's safety invariants. If required preconditions are not satisfied, report `BLOCKED` rather than improvising.

## Source and revision rule

Tasks may name an exact commit, ancestor requirement, or branch requirement. Verify exact revision constraints before execution. A documentation-only coordination commit must not silently redefine the implementation candidate being tested.

Before GitHub writes, re-read branch HEAD. Before moving the branch ref, race-check again and use fast-forward history only.

## Report contract

A delegated executor report should include at minimum:

```text
Task ID
Status
Repository path
Branch
HEAD
Commands/actions executed
Observed result
Evidence paths / hashes / commits
Safety notes
Unproven or blocked items
Recommended next step
```

## Review contract

ChatGPT review files record one of:

```text
ACCEPT
REWORK
BLOCKED
SUPERSEDED
```

Every review states its reviewer identity. If ChatGPT also executed the reviewed work, record it as self-review rather than independent review. ChatGPT explains why and points to the next Task ID/disposition when needed.

## Standing executor rule

For every `ต่อ`, Hermes/Codex must re-read the **remote working branch** rather than relying on stale conversational memory or an old local checkout. Current remote `ACTIVE.md`, `STATUS.md`, task file, report state, and task-specific safety gates determine what may execute.

After publishing the matching report, the executor stops. It does not invent the next task.

## Relationship to `docs/operations`

This directory is the execution/handoff layer only. Living status/roadmap/decisions remain under `docs/operations/`; historical task/report/review evidence remains historical. Accepted technical truth is grounded in code, tests, evidence, and release/acceptance gates.
