# CogentNexus Coordination Layer

This directory is the GitHub-based handoff surface between ChatGPT, **Hermes/Codex**, and the human operator.

GitHub is the durable coordination source of truth. Local execution remains on the operator's machine through the exact executor and permissions authorized by the active task.

## Canonical current contract

- Repository: `funggier/CogentNexus-OpenClaw`
- Current stabilization branch: `agent/v0.9.3-full-stabilization`
- READY gate: `READY_FOR_HERMES`
- Executor role: `Hermes/Codex`
- Manual trigger: `ต่อ`
- ChatGPT owns tasks, reviews, `ACTIVE.md`, and `STATUS.md`
- Hermes/Codex owns matching execution reports
- Human operator remains final authority

The READY gate names the handoff state; it does not require that only the Hermes implementation can execute. An explicitly authorized Hermes or Codex executor may execute the exact READY task.

## Intended loop

```text
Human talks primarily with ChatGPT
        ↓
ChatGPT publishes/reviews task in GitHub
        ↓
ACTIVE.md = READY_FOR_HERMES
        ↓
Human sends authorized executor: ต่อ
        ↓
Hermes/Codex synchronizes GitHub and executes exact active task
        ↓
Executor pushes matching execution report/evidence references
        ↓
ChatGPT reads report, reviews evidence, and publishes next disposition
        ↓
repeat
```

The human is a trigger, not a courier for task details. Full task specifications and execution reports live in GitHub.

## Optional continuous watch loop

For repeated work, an authorized executor may use the Scheduled-task mode defined in [`WATCH_MODE.md`](WATCH_MODE.md).

```text
ChatGPT publishes ACTIVE task with Execution mode: AUTO
        ↓
Scheduled Hermes/Codex task detects it on the next poll
        ↓
Executor validates and executes the exact task
        ↓
Executor pushes the matching report and stops that run
        ↓
ChatGPT reviews and publishes the next authorized task
```

Manual `ต่อ` remains supported. Continuous execution never bypasses task-specific safety gates, invents tasks, or repeats completed side effects.

## Ownership model

- **ChatGPT owns**
  - `ACTIVE.md`
  - `STATUS.md`
  - `tasks/*.md`
  - `reviews/*.md`
- **Hermes/Codex owns**
  - `reports/*.md`
- **Human operator** may intervene anywhere and is the final authority.

The executor should not rewrite task specifications merely to reflect progress. Progress/results belong in the matching report.

## Diagnosis, fix, and proof ownership

The default technical-role split is:

- **ChatGPT leads cause/fix specification** when repository evidence is sufficient: inspect durable evidence/source, establish the narrow root cause, define remediation and safety gates, and publish an exact task/patch specification.
- **Hermes/Codex leads execution proof**: execute the authorized diagnostic/change, capture commands/evidence, validate the proposed fix, and report contradictions or remaining uncertainty.
- ChatGPT may explicitly delegate deeper local diagnosis or implementation when machine access/capability is essential.
- Contrary machine evidence overrides a hypothesis. The executor records the contradiction without broadening authority; ChatGPT revises the task/disposition.

This role split changes who leads work, not the evidence standard or human authority.

## Task identity

Every task has a stable ID such as:

```text
CNX-20260822-001
```

The same ID is used across `tasks/`, `reports/`, and `reviews/`.

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

`ACTIVE.md` is the single pointer to the current handoff state/task.

The executor must not repeat a task whose report already records completion. If `ACTIVE.md` is not `READY_FOR_HERMES`, synchronize, report/read status as appropriate, and stop unless the active task explicitly authorizes another action.

## Minimal human signals

See [`SIGNALS.md`](SIGNALS.md).

`ต่อ` means: synchronize current GitHub coordination truth, read the active task/report/safety gates, execute only the exact authorized READY task, publish its report, and stop for review.

`สถานะ` is read-only coordination status. `หยุด` means do not begin a new coordination task.

## Problem resolution

See [`PROBLEM_LOOP.md`](PROBLEM_LOOP.md).

A safe stop must not become a silent dead end. The executor publishes the matching problem report; ChatGPT reviews it, classifies the blocker, and selects the narrowest safe next disposition or an exact human-decision gate.

## Progress communication contract

During a running task:

- announce objective/current phase at execution start;
- provide meaningful progress at milestones and before/after authorized mutations;
- report blockers immediately;
- expose actions/evidence/outcomes, not private reasoning;
- in AUTO mode continue unless a safety/authority/permission/required-information gate blocks execution;
- finish with actions taken, evidence, side effects, remaining unproven items, and durable next state.

## Evidence rule

A report must distinguish what was executed, what was observed, what evidence/commit records the result, and what remains unproven. Do not convert assumptions into PASS.

For disruptive tests, preserve the task's safety invariants. If required preconditions are not satisfied, report `BLOCKED` rather than improvising.

## Source and revision rule

Tasks may name an exact commit, ancestor requirement, or branch requirement. Verify exact revision constraints before execution. A documentation-only coordination commit must not silently redefine the implementation candidate being tested.

## Report contract

An executor report should include at minimum:

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

ChatGPT explains why and points to the next Task ID/disposition when needed.

## Standing executor rule

For every `ต่อ`, Hermes/Codex must re-read GitHub rather than relying on stale conversational memory. Current `ACTIVE.md`, task file, report state, and task-specific safety gates determine what may execute.

After publishing the matching report, the executor stops. It does not invent the next task.

## Relationship to `docs/operations`

This directory is the execution/handoff layer only. Living status/roadmap/decisions remain under `docs/operations/`; historical task/report/review evidence remains historical. Accepted technical truth is grounded in code, tests, evidence, and release/acceptance gates.
