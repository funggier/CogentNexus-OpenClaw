# Coordination Channel Status

**State:** ACTIVE  
**Updated:** 2026-08-22 20:30 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator  

## Participants

- **ChatGPT** — task design, evidence review, next-step decisions
- **Codex** — local-machine execution and execution reports
- **Human operator** — final authority, triggers Codex and may intervene at any point

## Active task

`CNX-20260822-001` — Gateway Durable Recovery Convergence

See [`ACTIVE.md`](ACTIVE.md).

## Current handoff state

```text
ChatGPT task published
        ↓
ACTIVE.md points to CNX-20260822-001
        ↓
awaiting Codex execution/report
        ↓
ChatGPT review pending
```

## Channel health rule

The coordination layer is considered usable when both sides can independently read the active task from GitHub and can write only their owned output area without force-pushing or rewriting the other side's records.

A task execution result is not accepted merely because a report exists. ChatGPT must review the report and referenced evidence before advancing the active pointer.
