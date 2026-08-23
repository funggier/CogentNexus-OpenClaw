# Coordination Reports

Execution reports are written by Codex after reading an active task from `../tasks/`.

A report is evidence-oriented. It should state what actually happened, not what was intended to happen.

## Recommended report format

```markdown
# CNX-YYYYMMDD-NNN — Execution Report

Status: PASS | FAIL | BLOCKED | EXECUTING
Executor: Codex

## Source state
- Repository path:
- Branch:
- HEAD:

## Actions executed

## Observations

## Evidence
- Files:
- SHA256:
- Commits:

## Safety notes

## Unproven / not executed

## Recommended next step
```

For a disruptive task, explicitly record the target process identity and the safety checks performed before any process termination.

Do not mark a task PASS if a required scenario was skipped.
