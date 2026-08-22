# Coordination Tasks

Task specifications are written by ChatGPT (or the human operator acting as task designer) and consumed by Codex.

Codex should treat task files as immutable instructions for that execution attempt. If execution reveals a problem, write it in the matching `../reports/` file instead of editing the task.

## Recommended task format

```markdown
# CNX-YYYYMMDD-NNN — Short title

Status: READY
Owner: ChatGPT
Executor: Codex

## Objective

## Why this task exists

## Required source state

## Preconditions

## Allowed actions

## Forbidden actions

## Procedure

## PASS criteria

## FAIL / BLOCKED criteria

## Evidence required

## Report destination
```

Tasks should be executable from the repository and should avoid relying on unstated chat context.
