# CogentNexus Coordination Layer

This directory is the GitHub-based handoff surface between ChatGPT, Codex, and the human operator.

It is intentionally simple, reviewable, and durable. GitHub is the shared source of coordination truth; local execution remains on the operator's machine through Codex or other explicitly authorized tools.

## Purpose

Use this layer when ChatGPT designs or reviews work but cannot directly execute on the local Windows machine, while Codex can execute locally and can read/write the repository.

The intended loop is:

```text
Human intent
   -> ChatGPT task specification
   -> GitHub coordination task
   -> Codex local execution
   -> GitHub execution report + evidence references
   -> ChatGPT review
   -> next task / close
```

## Ownership model

To reduce merge conflicts, each side owns different files.

- **ChatGPT owns**
  - `ACTIVE.md`
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

## State model

The coordination state is descriptive, not execution authority.

Typical lifecycle:

```text
DRAFT
  -> READY
  -> EXECUTING
  -> PASS | FAIL | BLOCKED
  -> REVIEWED
  -> CLOSED | REWORK
```

`ACTIVE.md` points to the task ChatGPT currently wants executed or reviewed.

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

## Human trigger

The normal human-to-Codex instruction can be as short as:

> Read `docs/operations/coordination/ACTIVE.md`, follow `docs/operations/coordination/README.md`, execute the active task exactly, and write the required report back to GitHub.

The human should not need to copy the full task body into Codex when Codex has repository access.

## Relationship to the rest of `docs/operations`

This directory is the execution/handoff layer only.

- `../STATUS.md` describes where the project is now.
- `../ROADMAP.md` describes short-, medium-, and long-term direction.
- `../WORKLOG.md` records major project progress.
- `../DECISIONS.md` records architectural and process decisions.

Coordination records may be temporary or superseded. Accepted technical truth must still be grounded in code, tests, evidence, and release/acceptance documentation.
