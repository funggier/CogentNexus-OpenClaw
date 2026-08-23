# Coordination Channel Status

**State:** `READY_FOR_CODEX`  
**Updated:** 2026-08-22 20:36 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator  
**Execution trigger:** `ต่อ`  

## Participants

- **ChatGPT** — primary conversation, task design, evidence review, next-step decisions
- **Codex** — local-machine execution and execution reports
- **Human operator** — final authority and minimal trigger between the two execution contexts

## Active task

`CNX-20260822-001` — Gateway Durable Recovery Convergence

See [`ACTIVE.md`](ACTIVE.md).

## Current handoff state

```text
ChatGPT task published
        ↓
ACTIVE.md = READY_FOR_CODEX
        ↓
operator sends Codex: ต่อ
        ↓
Codex syncs GitHub, executes active task, pushes report
        ↓
REPORT_READY
        ↓
ChatGPT reviews report and publishes next authorized state/task
```

## Conversation model

The operator can keep the substantive project conversation in ChatGPT.

Task details do not need to be copied into Codex. Once [`CODEX_BOOTSTRAP.md`](CODEX_BOOTSTRAP.md) has been accepted by the Codex session, future execution triggers may be the single word `ต่อ`.

Codex must re-read GitHub on each trigger so that ChatGPT and Codex communicate through durable repository state instead of depending on the operator to relay technical instructions.

## Channel health rule

The coordination layer is considered usable when both sides can independently read the active task from GitHub and can write only their owned output area without force-pushing or rewriting the other side's records.

A task execution result is not accepted merely because a report exists. ChatGPT must review the report and referenced evidence before advancing the active pointer.

A repeated trigger must not repeat already-completed disruptive side effects while review is pending.
