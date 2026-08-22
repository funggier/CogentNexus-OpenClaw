# CogentNexus Coordination Layer

This directory is the GitHub-based handoff surface between ChatGPT, Codex, and the human operator.

It is intentionally simple, reviewable, and durable. GitHub is the shared source of coordination truth; local execution remains on the operator's machine through Codex or other explicitly authorized tools.

## Purpose

Use this layer when ChatGPT designs or reviews work but cannot directly execute on the local Windows machine, while Codex can execute locally and can read/write the repository.

The intended loop is:

```text
Human talks primarily with ChatGPT
        ↓
ChatGPT publishes/reviews task in GitHub
        ↓
ACTIVE.md = READY_FOR_CODEX
        ↓
Human sends Codex: ต่อ
        ↓
Codex syncs GitHub and executes active task
        ↓
Codex pushes execution report/evidence references
        ↓
Human tells ChatGPT that Codex has returned, or simply asks to continue
        ↓
ChatGPT reads GitHub report, reviews evidence, and publishes next task
        ↓
repeat
```

The human is a **trigger**, not a courier for task details. Full task specifications and execution reports live in GitHub.

## Optional continuous watch loop

For repeated work, Codex may use the Scheduled-task mode defined in [`WATCH_MODE.md`](WATCH_MODE.md).

```text
ChatGPT publishes ACTIVE task with Execution mode: AUTO
        ↓
Codex Scheduled task detects it on the next poll
        ↓
Codex validates and executes the exact task
        ↓
Codex pushes the matching report and stops that run
        ↓
ChatGPT reviews and publishes the next authorized task
```

This removes the repeated `ต่อ` relay. It does not allow Codex to invent tasks, bypass safety gates, or repeat a completed task.

Manual `ต่อ` remains supported. Continuous local execution requires a confirmed enabled Scheduled task, the Windows machine powered on, and the ChatGPT desktop app running.

## Ownership model

To reduce merge conflicts, each side owns different files.

- **ChatGPT owns**
  - `ACTIVE.md`
  - `STATUS.md`
  - `tasks/*.md`
  - `reviews/*.md`
- **Codex owns**
  - `reports/*.md`
- **Human operator** may intervene anywhere and is the final authority.

Codex should not rewrite task specifications merely to reflect progress. Progress and results belong in the matching report file.

## Task identity

Every task has a stable ID:

```text
CNX-YYYYMMDD-NNN
```

Example:

```text
CNX-20260822-001
```

The same ID must be used across:

```text
tasks/CNX-20260822-001-*.md
reports/CNX-20260822-001-*.md
reviews/CNX-20260822-001-*.md
```

## Handoff state model

The coordination state is descriptive, not runtime recovery authority.

Normal handoff states are:

```text
READY_FOR_CODEX
    ↓ human signal: ต่อ
CODEX_EXECUTING
    ↓ report pushed
REPORT_READY
    ↓ ChatGPT review
CHATGPT_REVIEWING
    ↓
READY_FOR_CODEX | CLOSED | BLOCKED
```

`ACTIVE.md` is the single pointer to the current handoff state and task.

Codex must **not** repeat a task whose report already records completion merely because the operator sends `ต่อ` again. If `ACTIVE.md` is not `READY_FOR_CODEX`, Codex should synchronize, report the state, and stop unless the active task explicitly authorizes another action.

## Minimal human signals

See [`SIGNALS.md`](SIGNALS.md).

The normal execution trigger is now only:

```text
ต่อ
```

Codex interprets that as: synchronize from GitHub, read the current coordination records, execute the currently authorized task exactly, push the required report, and stop.

`สถานะ` is read-only coordination status. `หยุด` means do not begin a new coordination task.

## Evidence rule

A report must distinguish:

- what command or action was actually executed;
- what was observed;
- what evidence file or Git commit records the result;
- what remains unproven.

Do not convert assumptions into PASS.

For disruptive tests, Codex must preserve the safety invariants defined by the task. If the requested preconditions are not satisfied, report `BLOCKED` rather than improvising a dangerous workaround.

## Source and revision rule

Tasks may name an exact commit, an exact code ancestor, or a branch requirement.

When a task says that a commit must be an ancestor, Codex should verify it before execution, for example:

```powershell
git merge-base --is-ancestor <required-sha> HEAD
if ($LASTEXITCODE -ne 0) { throw 'Required code baseline is not present in HEAD.' }
```

This allows later documentation-only coordination commits without invalidating the code baseline being tested.

## Report contract

A Codex report should include at minimum:

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

The report should be concise but exact enough that ChatGPT can review it without relying on hidden local state.

## Review contract

ChatGPT review files should record one of:

```text
ACCEPT
REWORK
BLOCKED
SUPERSEDED
```

A review should explain why and, when needed, point to the next Task ID.

## Standing Codex rule

Once Codex has been told to use this coordination layer, later operator messages such as `ต่อ` should not require the full bootstrap prompt again.

For every `ต่อ`, Codex must re-read GitHub rather than relying on stale conversational memory. The current `ACTIVE.md`, task file, report state, and task-specific safety gates are the authority for what to execute next.

Codex stops after publishing the report. It does not autonomously invent the next task; ChatGPT reviews and publishes the next authorized task through GitHub.

## Relationship to the rest of `docs/operations`

This directory is the execution/handoff layer only.

- `../STATUS.md` describes where the project is now.
- `../ROADMAP.md` describes short-, medium-, and long-term direction.
- `../WORKLOG.md` records major project progress.
- `../DECISIONS.md` records architectural and process decisions.

Coordination records may be temporary or superseded. Accepted technical truth must still be grounded in code, tests, evidence, and release/acceptance documentation.
